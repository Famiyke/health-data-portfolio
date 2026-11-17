"""Build conservatively labelled native PBIX review copies.

This edits only Report/Layout in a NEW, separate PBIX ZIP. It does not modify
a DataModel, DAX expressions or Power Query. Existing PBIX files are untouched.
Power BI Desktop opening/visual verification remains mandatory.
"""
from pathlib import Path
from copy import deepcopy
import json, zipfile, uuid, sys

ROOT=Path(__file__).resolve().parent
INPUTS=[
    ("_native/mental/mental_health_outcomes.pbix","mental_health_REVIEW_SIMULATED.pbix"),
    ("_native/chronic/canada_chronic_disease_burden_monitor.pbix","chronic_disease_REVIEW_SIMULATED.pbix"),
]
OUT=ROOT/"native_review_copies"
OUT.mkdir(exist_ok=True)

def config_of(container):
    return json.loads(container.get("config","{}"))

def layout_from(blob):
    return json.loads(blob.decode("utf-16-le"))

def make_banner(template, width, start_y, title):
    result=deepcopy(template)
    cfg=config_of(result)
    cfg["name"]=uuid.uuid4().hex[:20]
    cfg["layouts"]=[{"id":0,"position":{"x":8,"y":start_y,"z":999990,
                                "width":max(100,width-16),"height":56,"tabOrder":999990}}]
    visual=cfg["singleVisual"]
    assert visual["visualType"]=="textbox"
    visual.setdefault("objects",{}).setdefault("general",[{"properties":{}}])
    visual["objects"]["general"][0].setdefault("properties",{})["paragraphs"]=[
        {"textRuns":[{"value":title,"textStyle":{"fontWeight":"bold","fontSize":"14pt","color":"#B42318"}}]}
    ]
    if "vcObjects" in visual:
        visual["vcObjects"]["background"]=[{"properties":{"show":{"expr":{"Literal":{"Value":"true"}}},
                                 "color":{"solid":{"color":{"expr":{"Literal":{"Value":"'#FFF0ED'"}}}}},
                                 "transparency":{"expr":{"Literal":{"Value":"0D"}}}}}]
    result["config"]=json.dumps(cfg,separators=(",",":"),ensure_ascii=False)
    return result

def replace_first_footer(layout):
    sec=layout["sections"][0]
    replaced=0
    for v in sec.get("visualContainers",[]):
        cfg=config_of(v)
        if cfg.get("singleVisual",{}).get("visualType")!="textbox":continue
        paragraphs=cfg["singleVisual"].get("objects",{}).get("general",[{}])[0].get("properties",{}).get("paragraphs",[])
        old="".join(t.get("value","") for p in paragraphs for t in p.get("textRuns",[]))
        if "Statistics Canada" not in old:continue
        cfg["singleVisual"]["objects"]["general"][0]["properties"]["paragraphs"]=[
           {"textRuns":[{"value":"SIMULATED DATA ONLY | 5,000 generated records | NOT Statistics Canada CCHS",
                         "textStyle":{"fontWeight":"bold","fontSize":"10pt","color":"#B42318"}}]}
        ]
        v["config"]=json.dumps(cfg,separators=(",",":"),ensure_ascii=False)
        replaced+=1
    assert replaced==1, f"Expected exactly one misleading source textbox, found {replaced}"

def review_pbix(path, target, mental_template=None):
    with zipfile.ZipFile(path) as original:
        assert original.testzip() is None
        old=layout_from(original.read("Report/Layout"))
        sections=old.get("sections",[])
        assert len(sections)==4
        if mental_template is None:
            t=next((v for p in sections for v in p.get("visualContainers",[])
                    if config_of(v).get("singleVisual",{}).get("visualType")=="textbox"),None)
        else: t=mental_template
        assert t is not None, "No available textbox layout template"
        if "mental" in str(path).lower():
            replace_first_footer(old)
        for section in sections:
            original_name=section["displayName"]
            height=int(section["height"])
            width=int(section["width"])
            assert width>900 and height>450
            section["height"]=height+75
            section["displayName"]="DEMO | "+original_name
            warning="SIMULATED DATA. Not official Canada health statistics. Embedded legacy model. Refresh and validate before use."
            banner=make_banner(t,width,height+6,warning)
            section["visualContainers"].append(banner)
        newbytes=json.dumps(old,separators=(",",":"),ensure_ascii=False).encode("utf-16-le")
        with zipfile.ZipFile(target,"w") as out:
            for item in original.infolist():
                contents=newbytes if item.filename=="Report/Layout" else original.read(item.filename)
                out.writestr(item,contents)
    with zipfile.ZipFile(target) as review:
        assert review.testzip() is None
        check=layout_from(review.read("Report/Layout"))
        assert len(check["sections"])==len(sections)==4
        for page in check["sections"]:
            assert page["displayName"].startswith("DEMO | ")
            banners=[config_of(v) for v in page["visualContainers"]
                     if config_of(v).get("singleVisual",{}).get("visualType")=="textbox"]
            assert any("SIMULATED DATA." in json.dumps(v) for v in banners)
        assert review.read("DataModel")==original_datamodel
        print("STRUCTURAL PASS",target.name,target.stat().st_size,"bytes",len(check["sections"]),"pages")

with zipfile.ZipFile(ROOT/INPUTS[0][0]) as original:
    layout=layout_from(original.read("Report/Layout"))
    template=next(v for pg in layout["sections"] for v in pg["visualContainers"]
                  if config_of(v).get("singleVisual",{}).get("visualType")=="textbox")
for input_path, filename in INPUTS:
    src=ROOT/input_path
    with zipfile.ZipFile(src) as orig:
        original_datamodel=orig.read("DataModel")
    review_pbix(src,OUT/filename,template)
print("WARNING: Verified package integrity only. Neither PBIX has been opened in Power BI Desktop.")
