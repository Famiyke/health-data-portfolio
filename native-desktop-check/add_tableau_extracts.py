from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree
from copy import deepcopy
import argparse
import csv
import io
import tempfile
from tableauhyperapi import HyperProcess, Telemetry, Connection, CreateMode, TableDefinition, TableName, SqlType, Inserter


def build(source: Path, target: Path):
    name = 'Retail Sales Forecasting.twb'
    with ZipFile(source) as z:
        workbook=etree.fromstring(z.read(name))
        files={n:z.read(n) for n in z.namelist() if n!=name}
    workbook.set('version', '18.1')
    workbook.set('original-version','18.1')
    count=0
    with tempfile.TemporaryDirectory() as tmp, HyperProcess(Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        for datasource in workbook.xpath('./datasources/datasource'):
            datasource.set('version','18.1')
            original_connection=datasource.find('connection')
            filename=original_connection.get('filename')
            data=files['Data/'+filename]
            rows=[(r['Category'],float(r['Value']),r['Status'],r['SourceReference']) for r in csv.DictReader(io.StringIO(data.decode('utf-8-sig')))]
            hyper_name=Path(filename).stem+'.hyper'
            path=Path(tmp)/hyper_name
            with Connection(hyper.endpoint,path,CreateMode.CREATE_AND_REPLACE) as connection:
                connection.catalog.create_schema('Extract')
                table=TableDefinition(TableName('Extract','Extract'),[
                    TableDefinition.Column('Category',SqlType.text()),
                    TableDefinition.Column('Value',SqlType.double()),
                    TableDefinition.Column('Status',SqlType.text()),
                    TableDefinition.Column('SourceReference',SqlType.text()),
                ])
                connection.catalog.create_table(table)
                with Inserter(connection,table) as inserter:
                    inserter.add_rows(rows)
                    inserter.execute()
                actual=[tuple(r) for r in connection.execute_list_query('SELECT "Category", "Value", "Status", "SourceReference" FROM "Extract"."Extract"')]
                assert sorted(actual)==sorted(rows), filename
            target_name='Data/Extracts/'+hyper_name
            files[target_name]=path.read_bytes()
            old=datasource.find('extract')
            if old is not None:datasource.remove(old)
            extract=etree.SubElement(datasource,'extract',count='-1',enabled='true',units='records',object_id='')
            extract.attrib.pop('object_id',None);extract.set('object-id','');extract.set('user-specific','false')
            con=etree.SubElement(extract,'connection',{'access_mode':'readonly','authentication':'auth-none','author-locale':'en_US','class':'hyper','dbname':target_name,'default-settings':'yes','schema':'Extract','sslmode':'','tablename':'Extract','username':'tableau_internal_user'})
            etree.SubElement(con,'relation',name='Extract',table='[Extract].[Extract]',type='table')
            refresh=etree.SubElement(con,'refresh')
            etree.SubElement(refresh,'refresh-event',{'add-from-file-path':filename,'increment-value':'%null%','refresh-type':'create','rows-inserted':str(len(rows))})
            metadata=deepcopy(original_connection.find('metadata-records'))
            for record in metadata.findall('metadata-record'):
                record.find('parent-name').text='[Extract]'
            con.append(metadata)
            count+=len(rows)
            print('Verified extract rows:',filename,len(rows),flush=True)
    assert count==76
    files['README.txt']=("Open the packaged retail workbook in Tableau Desktop or Tableau Desktop Public Edition. It includes four local Hyper extracts and their original CSV snapshots. The extracts preserve all 76 chart data rows, including the historical and forecast status and source references. No sign-in or publication is required to open the local file. Values are CAD billions except model accuracy (WAPE percent). The complete data and modelling workflow is available on the portfolio.\n").encode()
    with ZipFile(target,'w',ZIP_DEFLATED,compresslevel=6) as z:
        z.writestr(name,etree.tostring(workbook,encoding='utf-8',xml_declaration=True,pretty_print=True))
        for n,data in files.items():z.writestr(n,data)
    print('Packaged four Hyper extracts, 76 source rows:',target,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('target',type=Path);a=p.parse_args();build(a.source,a.target)
