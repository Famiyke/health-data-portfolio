param([string]$InstallPath, [string]$EvidenceDir)
$ErrorActionPreference='Stop'
New-Item -ItemType Directory -Force $EvidenceDir | Out-Null
$portFile = $null
for ($i=0;$i -lt 18;$i++) {
    $portFile = Get-ChildItem "$env:LOCALAPPDATA\Microsoft\Power BI Desktop\AnalysisServicesWorkspaces" -Filter msmdsrv.port.txt -Recurse -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($portFile) { break }
    Start-Sleep 5
}
if (-not $portFile) { throw 'No native Power BI Analysis Services workspace was opened.' }
$port = (Get-Content $portFile.FullName -Raw).Trim() -replace '[^0-9]',''
if (-not $port) { throw 'Power BI workspace did not expose its model port.' }
Write-Host "Power BI local model port: $port"
$bin = Split-Path $InstallPath -Parent
$adomd = Get-ChildItem $bin -Filter 'Microsoft.AnalysisServices.AdomdClient.dll' -Recurse | Select-Object -First 1
if (-not $adomd) { throw 'Power BI ADOMD client assembly not found.' }
Add-Type -Path $adomd.FullName
function Read-Model {
    $conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection "Data Source=localhost:$port"
    $conn.Open()
    try {
        $catalogs = $conn.GetSchemaDataSet("DBSCHEMA_CATALOGS", $null).Tables[0]
        if ($catalogs.Rows.Count -gt 0) { $conn.ChangeDatabase([string]$catalogs.Rows[0].CATALOG_NAME) }
        $command = $conn.CreateCommand()
        $command.CommandTimeout=90
        $command.CommandText = @'
EVALUATE ROW(
    "VacancyIndustry", COUNTROWS('VacancyIndustry'),
    "VacancyRegion", COUNTROWS('VacancyRegion'),
    "WageIndustry", COUNTROWS('WageIndustry'),
    "Overtime", COUNTROWS('Overtime'),
    "SickLeave", COUNTROWS('SickLeave'),
    "NurseSupply", COUNTROWS('NurseSupply'),
    "ManitobaLatestVacancy", CALCULATE([Latest regional vacancy rate], 'VacancyRegion'[Category] = "Manitoba", 'VacancyRegion'[Period] = "2026 Q2"),
    "LatestAggregateOvertime", CALCULATE([Latest hospital overtime rate], 'Overtime'[Category] = "Provinces/territories with available data", 'Overtime'[Period] = "2024–2025")
)
'@
        $reader=$command.ExecuteReader()
        if (-not $reader.Read()) { throw 'DAX query returned no row.' }
        $data=[ordered]@{}
        for ($i=0;$i -lt $reader.FieldCount;$i++) {
            $name=$reader.GetName($i).Trim('[',']')
            $data[$name]=if($reader.IsDBNull($i)){$null}else{$reader.GetValue($i)}
        }
        $reader.Close()
        return $data
    } finally { $conn.Close() }
}
function Test-Model($data) {
    return ($data -and $data.VacancyIndustry -eq 176 -and $data.VacancyRegion -eq 196 -and $data.WageIndustry -eq 176 -and $data.Overtime -eq 57 -and $data.SickLeave -eq 57 -and $data.NurseSupply -eq 65 -and $null -ne $data.ManitobaLatestVacancy -and [math]::Abs([double]$data.ManitobaLatestVacancy-4.3) -lt 0.000001 -and $null -ne $data.LatestAggregateOvertime -and [math]::Abs([double]$data.LatestAggregateOvertime-4.4973861) -lt 0.000001)
}
$data=$null
try { $data=Read-Model } catch { Write-Host "Initial DAX query: $($_.Exception.Message)" }
if (-not (Test-Model $data)) {
    # A PBIP lacks a cached model. If the Desktop refresh did not populate it,
    # refresh using the running application's native Analysis Services model.
    $core=Get-ChildItem $bin -Filter 'Microsoft.AnalysisServices.Core.dll' -Recurse | Select-Object -First 1
    $tabular=Get-ChildItem $bin -Filter 'Microsoft.AnalysisServices.Tabular.dll' -Recurse | Select-Object -First 1
    if (-not $tabular) { throw 'Native Tabular client assembly not found.' }
    if ($core) { Add-Type -Path $core.FullName }
    Add-Type -Path $tabular.FullName
    $server = New-Object Microsoft.AnalysisServices.Tabular.Server
    $server.Connect("localhost:$port")
    try {
        $db=$server.Databases | Where-Object { $_.Model.Tables.Count -ge 6 } | Select-Object -First 1
        if (-not $db) { throw 'The workforce semantic model was not loaded.' }
        $db.Model.RequestRefresh([Microsoft.AnalysisServices.Tabular.RefreshType]::Full)
        $db.Model.SaveChanges() | Out-Null
        Write-Host 'Refreshed the model through the running Power BI Desktop engine.'
    } finally { $server.Disconnect() }
    $data=Read-Model
}
$data | ConvertTo-Json | Set-Content -Encoding utf8 (Join-Path $EvidenceDir 'native-dax-results.json')
Write-Host ($data | ConvertTo-Json -Compress)
if (-not (Test-Model $data)) { throw 'Power BI Desktop model results differ from the embedded source.' }
Write-Host 'PASS: Power BI Desktop engine loaded all six tables and returned the expected DAX values.'
