"""Publish self-contained, corrected browser dashboards.

Runs in GitHub Actions from source datasets in checked-out public repositories.
The Power BI PBIX and Tableau Public workbooks are NOT edited by this script.
Every page distinguishes official published aggregates from generated records.
"""
from pathlib import Path
from collections import defaultdict
import html
import json
import csv
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "dashboards"
OUT.mkdir(exist_ok=True)

PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light"><title>__TITLE__</title>
<style>
:root{--ink:#183133;--muted:#496367;--teal:#116b72;--soft:#e8f2f1;--line:#d7e3e0;--paper:#f6f8f6;--white:#fff}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,Segoe UI,Arial,sans-serif}
a{color:var(--teal)}.wrap{width:min(1120px,calc(100% - 36px));margin:auto}header{background:#103f44;color:#fff;padding:18px 0}
header a{color:#e1f4ee}h1{font-size:clamp(24px,4vw,40px);line-height:1.18;margin:28px 0 10px}
h2{font-size:20px;margin:10px 0 14px}.sub{color:var(--muted);margin:0 0 20px;max-width:860px}
.notice{border:2px solid #266773;background:#e7f2f2;padding:16px 20px;border-radius:10px;margin:20px 0;font-weight:700}
.source{font-size:13px;color:var(--muted);overflow-wrap:anywhere;margin:14px 0 26px}
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:18px 0 30px}.card,.panel{background:#fff;border:1px solid var(--line);border-radius:12px;padding:20px}
.card .value{font-size:clamp(21px,3vw,30px);font-weight:800;color:var(--teal);font-variant-numeric:tabular-nums}
.card .label{font-size:13px;color:var(--muted)}
main{padding-bottom:50px}.panel{margin-bottom:18px}.controls{display:flex;gap:16px;flex-wrap:wrap;align-items:end;margin:12px 0 22px}
.controls label{display:grid;gap:5px;font-size:14px;font-weight:700}.controls select{border:1px solid #a3b9b5;border-radius:7px;background:white;padding:9px;min-width:160px;color:var(--ink)}
.graph{display:grid;gap:10px}.bar{display:grid;grid-template-columns:minmax(105px,200px) 1fr 88px;gap:10px;align-items:center;font-size:14px}
.bar .track{background:#eaf0ee;border-radius:4px;height:19px;overflow:hidden}.bar .fill{background:var(--teal);height:100%;min-width:1px}
.bar .number{text-align:right;font-variant-numeric:tabular-nums;font-weight:700}
table{width:100%;border-collapse:collapse;font-size:14px}th,td{padding:9px;border-bottom:1px solid var(--line);text-align:left}
th{background:#f0f5f4}td.num{text-align:right;font-variant-numeric:tabular-nums}
.table-scroll{overflow-x:auto}.small{font-size:13px;color:var(--muted)}footer{padding:18px 0 40px;border-top:1px solid var(--line)}
:focus-visible{outline:3px solid #b25610;outline-offset:3px}
@media(max-width:700px){.cards{grid-template-columns:1fr 1fr}.bar{grid-template-columns:110px minmax(0,1fr) 60px;gap:6px;font-size:12px}.wrap{width:min(100% - 20px,1120px)}.card,.panel{padding:14px}}
@media(max-width:400px){.cards{grid-template-columns:1fr}.bar{grid-template-columns:85px minmax(0,1fr) 58px;gap:4px}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
</style></head>
<body>
<header><div class="wrap"><a href="../index.html">← Portfolio home</a> &nbsp; | &nbsp; <a href="index.html">Dashboards</a></div></header>
<main class="wrap">
<h1>__TITLE__</h1><p class="sub">__SUBTITLE__</p>
<div class="notice" role="note">__NOTICE__</div>
<div class="source">Source and reproducibility: <a href="__SOURCEURL__" target="_blank" rel="noopener noreferrer">__SOURCELABEL__</a> · <a href="__REPURL__" target="_blank" rel="noopener noreferrer">View data and code</a></div>
<section class="cards" id="cards" aria-label="Summary indicators"></section>
<section class="panel" aria-label="Interactive analytical comparison">
<h2>Explore the data</h2>
<div class="controls"><label for="view">Indicator<select id="view"></select></label><label for="year">Reporting year<select id="year"></select></label></div>
<p id="explain" class="small"></p>
<div class="graph" id="graph" aria-label="Bar chart, values also listed in a table below"></div>
</section>
<section class="panel"><h2>Accessible data table</h2><div class="table-scroll"><table><thead><tr><th scope="col">Group</th><th scope="col">Value</th><th scope="col">Observations / population</th></tr></thead><tbody id="table-body"></tbody></table></div></section>
<section class="panel"><h2>Interpretation and limitations</h2><p>__LIMITS__</p></section>
</main><footer class="wrap">Portfolio analysis. The source type and method limitations are stated above. Never use fictional comparisons to make real clinical or public-policy decisions.</footer>
<script>
const CFG = __DATA__;
const views = document.getElementById('view'), years=document.getElementById('year');
const graph=document.getElementById('graph'),tbody=document.getElementById('table-body');
const explain=document.getElementById('explain'),cards=document.getElementById('cards');
function textnode(tag,cls,value){const el=document.createElement(tag);if(cls)el.className=cls;el.textContent=String(value);return el;}
CFG.cards.forEach(c=>{const box=textnode('div','card','');box.append(textnode('div','value',c.value),textnode('div','label',c.label));cards.append(box);});
CFG.views.forEach((v,i)=>{const opt=document.createElement('option');opt.value=String(i);opt.textContent=v.name;views.append(opt)});
function yearOptions(){const v=CFG.views[+views.value];years.replaceChildren();(v.years||['All']).forEach(y=>{const o=document.createElement('option');o.value=String(y);o.textContent=String(y);years.append(o)});years.value=String((v.years||['All']).at(-1));}
function render(){
const view=CFG.views[+views.value],selected=years.value;
const data=view.rows.filter(r=>String(r.year||'All')===selected).filter(r=>r.value!==null);
const max=Math.max(0.001,...data.map(x=>Number(x.value)));
graph.replaceChildren();tbody.replaceChildren();
explain.textContent=view.explain;
data.forEach(r=>{
const row=textnode('div','bar','');const label=textnode('div','',r.label);
const track=textnode('div','track','');const fill=textnode('div','fill','');fill.style.width=Math.max(0,100*Number(r.value)/max)+'%';track.append(fill);
row.append(label,track,textnode('div','number',Number(r.value).toLocaleString(undefined,{maximumFractionDigits:view.digits??1})));graph.append(row);
const tr=document.createElement('tr');const a=document.createElement('th');a.scope='row';a.textContent=r.label;
tr.append(a,textnode('td','num',Number(r.value).toLocaleString(undefined,{maximumFractionDigits:view.digits??1})),textnode('td','num',r.n??'—'));tbody.append(tr);
});
if(!data.length)graph.append(textnode('p','','No groups meet the disclosure rule for this selection.'));
}
views.addEventListener('change',()=>{yearOptions();render()});years.addEventListener('change',render);
yearOptions();render();
</script></body></html>
"""


def page(file_name, *, title, subtitle, notice, source_url, source_label, repo_url, cards, views, limits):
    out = PAGE
    mapping = {
        "__TITLE__": html.escape(title),
        "__SUBTITLE__": html.escape(subtitle),
        "__NOTICE__": html.escape(notice),
        "__SOURCEURL__": html.escape(source_url, quote=True),
        "__SOURCELABEL__": html.escape(source_label),
        "__REPURL__": html.escape(repo_url, quote=True),
        "__LIMITS__": html.escape(limits),
        "__DATA__": json.dumps({"cards": cards, "views": views}, ensure_ascii=False).replace("</", "<\\/"),
    }
    # Replace JSON placeholder last to preserve string literals in embedded data.
    for key, value in mapping.items():
        out = out.replace(key, value)
    (OUT / file_name).write_text(out, encoding="utf-8")
    print("Wrote", file_name, len(out), "bytes")


def real_diabetes():
    p = ROOT / "_sources/chronic/official_ns_diabetes_2000_2022.csv"
    zones = ROOT / "_sources/chronic/official_ns_diabetes_zone_2000_2022.csv"
    with p.open(newline="", encoding="utf-8") as f:
        province=list(csv.DictReader(f))
    with zones.open(newline="", encoding="utf-8") as f:
        zr=list(csv.DictReader(f))
    assert len(province)==23 and len(zr)==92
    province_view=[{"year":"All","label":r["year"],"value":float(r["crude_diabetes_prevalence_percent"]),
                    "n":f'{int(r["diabetes_prevalent_count"]):,} cases / {int(r["population"]):,} people'} for r in province]
    zone_view=[{"year":r["year"],"label":r["health_zone"].replace("Zone ","").split(" - ")[-1],
                "value":float(r["crude_diabetes_prevalence_percent"]),
                "n":f'{int(r["diabetes_prevalent_count"]):,} / {int(r["population"]):,}'} for r in zr]
    page("diabetes.html", title="Diabetes surveillance · Nova Scotia",
         subtitle="Observed published administrative strata · 2000–2022 · crude prevalence among adults aged 20+",
         notice="REAL PUBLIC DATA. These are Government of Nova Scotia CCDSS-derived aggregate statistics, NOT simulated CCHS records or national PHAC figures.",
         source_url="https://data.novascotia.ca/datasets/cumi-sw99",source_label="Nova Scotia Open Data, diabetes prevalence",
         repo_url="https://github.com/Famiyke/chronic-disease-surveillance-canada/blob/main/OFFICIAL_NS_DIABETES_FINDINGS.md",
         cards=[{"value":f'{float(province[-1]["crude_diabetes_prevalence_percent"]):.2f}%',"label":"Crude prevalence in 2022"},
                {"value":f'{float(province[0]["crude_diabetes_prevalence_percent"]):.2f}%',"label":"Crude prevalence in 2000"},
                {"value":"1,288","label":"Official source strata validated"}],
         views=[{"name":"Provincial annual crude prevalence (%)","years":["All"],"rows":province_view,
                 "explain":"Aggregate source counts divided by population; crude rates include population age-composition effects.","digits":2},
                {"name":"Health-zone crude prevalence (%)","years":sorted(set(r["year"] for r in zr)),"rows":zone_view,
                 "explain":"Health-zone rates are count-weighted from sex- and age-specific published strata, not a simple mean of rates.","digits":2}],
         limits="Published provincial administrative data for Nova Scotia only, ages 20 and older. No age-standardization, causal inference, patient-level data, or evidence of specific intervention effects.")


def real_ontario():
    path=ROOT/"_sources/ontario/official_ontario_fao_surgery_2019_2022.csv"
    with path.open(newline="", encoding="utf-8") as f: data=list(csv.DictReader(f))
    assert len(data)==276
    views=[]
    for metric,desc,explain,digits in [
        ("surgeries_performed","Surgeries performed (count)","FAO Table A-1, annual surgery counts by surgical service area. Total excluded from bars to avoid double-counting.",0),
        ("average_waitlist","Average surgical waitlist (persons)","FAO Table A-2. The 2022 average covers January–September only.",0),
        ("fao_estimated_wait_months","FAO-estimated waiting time (months)","FAO Table A-3. Aggregate estimate based on average waitlist and surgical throughput, NOT patient Wait 2 medians.",1)]:
        rows=[{"year":r["year"],"label":r["service_area"],"value":float(r["value"]),
               "n":f'Source table {r["source_table"]}'} for r in data if r["metric"]==metric and r["service_area"]!="Total"]
        assert len(rows)==88
        views.append({"name":desc,"years":["2019","2020","2021","2022"],"rows":rows,"digits":digits,"explain":explain})
    page("ontario.html",title="Ontario surgery · Official aggregate tables",
         subtitle="FAO Ontario 2023 report · data from Ontario Health · 2019–2022",
         notice="REAL PUBLISHED AGGREGATES. The waiting-month measure is an FAO ESTIMATE, not patient-level Wait 2. This is NOT the archived fictional hospital-ranking Tableau dashboard.",
         source_url="https://fao-on.org/en/report/health-2023/",source_label="Financial Accountability Office Ontario, Tables A-1 to A-3",
         repo_url="https://github.com/Famiyke/ontario-wait-times/blob/main/OFFICIAL_ONTARIO_SURGERY_FINDINGS.md",
         cards=[{"value":"649,299","label":"Surgeries, 2019"},{"value":"555,487","label":"Surgeries, 2022"},{"value":"5.5 mo","label":"FAO estimated 2022 wait (not median Wait 2)"}],
         views=views,
         limits="Source report published in 2023, last data year 2022. 2022 average waitlist uses January–September. No provider or hospital rankings, patient-level waiting times, 2026 status, or causal effects.")


def synthetic_mental():
    df=pd.read_csv(ROOT/"_sources/mental/cchs_data.csv")
    assert len(df)==5000
    assert (df["mh_rating"].isin([1,2,3]).astype(int)==df["good_mh"]).all()
    assert (df["mh_rating"].isin([4,5]).astype(int)+df["good_mh"]==1).all()
    groupviews=[]
    for col,name in [("province","Province, groups with n ≥ 30"),("income_group","Income band, groups with n ≥ 30"),("age_group","Age band, groups with n ≥ 30")]:
        g=df.groupby(col,dropna=False).agg(rate=("good_mh","mean"),n=("good_mh","size")).reset_index()
        rec=[{"year":"All","label":str(r[col]),"value":round(100*float(r["rate"]),3),"n":int(r["n"])} for _,r in g.iterrows() if int(r["n"])>=30]
        assert rec
        groupviews.append({"name":name,"years":["All"],"rows":rec,"digits":1,
                           "explain":"Percentage reporting good or better in a fictional sample, not a weighted CCHS estimate. Groups with n < 30 are omitted."})
    cards=[{"value":f'{100*df["good_mh"].mean():.1f}%',"label":"Generated good-or-better rating"},
           {"value":f'{100*(1-df["good_mh"].mean()):.1f}%',"label":"Generated fair/poor rating"},
           {"value":f'{100*df["unmet_need"].mean():.1f}%',"label":"Generated unmet need (not CCHS)"}]
    page("mental-health.html",title="Mental health indicators · Synthetic demonstration",
         subtitle="5,000 generated records · corrected category coding · small-group suppression",
         notice="SIMULATED DATA ONLY. Not Statistics Canada CCHS, not real patients, and not representative Indigenous or provincial health findings. No identity-comparison visual is presented.",
         source_url="https://github.com/Famiyke/mental-health-outcomes-canada/blob/main/simulate_cchs.py",source_label="Reproducible synthetic generator",
         repo_url="https://github.com/Famiyke/mental-health-outcomes-canada/blob/main/DASHBOARD_CORRECTION_GUIDE.md",
         cards=cards,views=groupviews,
         limits="All percentages originate from fictional records. Self-reported ratings 1–3 versus 4–5 are exhaustive in this simulation. Groups with fewer than 30 generated rows are suppressed. Findings are not population estimates and support no real policy or group comparisons.")


def synthetic_readmission():
    df=pd.read_csv(ROOT/"_sources/hospital/cihi_hospital.csv")
    assert len(df)>100
    views=[]
    for col,name in [("province","Synthetic province illustration"),("diagnosis","Synthetic diagnosis illustration")]:
        grouped=df.groupby(["year",col],as_index=False)[["readmissions","separations"]].sum()
        rec=[{"year":str(int(r["year"])),"label":str(r[col]),
              "value":round(100*r["readmissions"]/r["separations"],3),"n":int(r["separations"])} for _,r in grouped.iterrows()]
        views.append({"name":name,"years":sorted(set(r["year"] for r in rec)),"rows":rec,
                      "digits":2,"explain":"Synthetic readmission count / synthetic separations. Rankings do not represent CIHI province or provider data."})
    page("readmissions.html",title="Hospital readmissions · Synthetic methods demo",
         subtitle="Fictional province × diagnosis × year dataset · 2018–2022",
         notice="SIMULATED DATA ONLY. No official CIHI provincial readmission ranking, hospital comparison or measured cost savings. This demonstration does NOT use real patient data.",
         source_url="https://github.com/Famiyke/hospital-readmission-canada/blob/main/simulate_cihi_data.py",source_label="Synthetic Python generator",
         repo_url="https://github.com/Famiyke/hospital-readmission-canada/blob/main/SOURCE_VALIDATION.md",
         cards=[{"value":f"{len(df):,}","label":"Generated observation rows"},
                {"value":"2018–22","label":"Synthetic analysis periods"},
                {"value":"0","label":"Official patient-level records used"}],
         views=views,
         limits="All baseline rates, diagnosis multipliers and counts are assumed demonstration parameters. Do not infer actual regional healthcare quality, intervention effects, clinical outcomes or financial savings.")


def index():
    items=[
        ("diabetes.html","Nova Scotia diabetes surveillance","REAL DATA","Government-published CCDSS-derived age-20+ crude prevalence."),
        ("ontario.html","Ontario surgical access","REAL DATA","Official FAO published surgery activity, waitlists and estimated waiting months."),
        ("mental-health.html","Mental health indicator demo","SIMULATED","Generated records, corrected mental-health categories and small-group suppression."),
        ("readmissions.html","Hospital readmissions demo","SIMULATED","Constructed province/diagnosis scenarios, no real performance rankings."),
    ]
    cards="".join(f'<li class="panel"><strong><a href="{url}">{html.escape(title)}</a></strong> — {kind}<p>{html.escape(desc)}</p></li>' for url,title,kind,desc in items)
    output=f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Verified and simulated portfolio dashboards</title>
<style>body{{font:17px/1.6 system-ui,sans-serif;background:#f6f8f6;color:#183133;max-width:850px;padding:20px;margin:20px auto}}a{{color:#126871}}.panel{{background:white;border:1px solid #d7e3e0;border-radius:12px;padding:18px;margin:14px 0}}ul{{padding:0;list-style:none}}</style></head><body>
<a href="../index.html">← Portfolio homepage</a><h1>Healthcare analytics dashboards</h1>
<p>These browser dashboards are corrected and explicitly identify real-data findings versus simulated examples. They do not replace the legacy Power BI Desktop or published Tableau workbooks.</p><ul>{cards}</ul></body></html>'''
    (OUT/"index.html").write_text(output,encoding="utf-8")
    print("Wrote dashboard index")


if __name__=="__main__":
    real_diabetes()
    real_ontario()
    synthetic_mental()
    synthetic_readmission()
    index()
