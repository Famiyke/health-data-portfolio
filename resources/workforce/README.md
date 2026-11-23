# Canadian workforce and labour market analytics

## Research question
Where are staffing pressures concentrated, and how do labour market indicators compare with hospital staffing measures?

Compares vacancies, offered wages and payroll employment across industries and provinces. Separate CIHI views cover hospital overtime, sick leave, calculated staffing capacity and health professional supply.

## Coverage
3,199 source observations from Statistics Canada quarterly data (2021 Q1 to 2026 Q2), CIHI hospital staffing (2020–2021 to 2024–2025) and 2020–2024 professional supply. Regional labour market comparisons start in 2023.

## Official sources
- Statistics Canada 14-10-0442-01: https://www150.statcan.gc.ca/n1/tbl/csv/14100442-eng.zip
- CIHI Health Workforce Quick Stats 2024: https://www.cihi.ca/sites/default/files/document/health-workforce-quickstats-2024-data-tables-en.xlsx
- CIHI Health Workforce Overview 2020–2024: https://www.cihi.ca/sites/default/files/document/data-file/health-workforce-canada-2020-2024-overview-data-tables-en.xlsx

Source snapshot retrieved 22 November 2026; see source_manifest.json for file hashes and source URLs.

## Methods and data quality
The quarterly survey covers selected industries and jurisdictions. We retain the original Statistics Canada quality indicators A–F and suppression flags. Vacancy-rate reconciliation to published vacancies and payroll employees had a maximum absolute difference of 0.103 percentage points. CIHI overtime-rate reconciliation to regular and overtime hours had a maximum absolute difference of 0.025 percentage points. The published rates are preserved. CIHI hospital staffing, supply and survey metrics use distinct populations and report periods. Paid sick leave hours per FTE is calculated from published hours and calculated FTEs. Source coverage may change.

SQL analyses: latest industry snapshot, same-quarter vacancy-rate changes, sick leave per FTE and selected supply density. The workflow retains unavailable estimates without numerical values.

## Key findings
- Canada reported 548,400 vacancies in the second quarter of 2026. Health care and social assistance accounted for 95,890 (17.5%).
- The vacancy rate in health care and social assistance was 4.3% in Manitoba and 3.7% nationally in 2026 Q2. Both estimates are unadjusted for seasonality.
- Overtime accounted for 4.50% of regular plus overtime hospital worked hours in CIHI’s reporting jurisdictions in 2024–2025.

## Independent validation
3,199 source records independently reconciled to official CSV rows or Excel cells. See validation.json and analysis_results.json.

## Reproduce analysis
Unzip the workflow. Run `python run_analysis.py .` to execute SQL against the included CSV snapshots.

To recreate from original files, install requirements.txt and run:

    python build_expansion.py --raw-dir raw --output-dir rebuilt --project workforce --download
    python validate_expansion.py --raw-dir raw --output-dir rebuilt --project workforce

The current public release may differ from the recorded source hashes; review revisions.

## BI project
The editable Power BI project contains six report pages with reporting-period slicers, embedded data and DAX measures. Extract the ZIP and open Workforce.pbip in a recent Power BI Desktop release. Desktop execution was not available here. The web dashboard is independently tested.

## Interpretation and limitations
Compare unadjusted vacancies across the same quarter of different years. Offered wages describe vacant jobs in current Canadian dollars. CIHI hospital staffing excludes physician hours, and Québec and Nunavut do not report to the CMDB. Supply counts differ from employed full-time equivalents. The sources cover different populations and cannot directly measure a staffing shortfall.
