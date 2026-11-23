# Manitoba regional health equity

## Purpose
How do health indicators and healthcare use vary across Manitoba’s health regions and income groups?
This project compares Manitoba’s health regions and income groups using published estimates from Statistics Canada’s Canadian Community Health Survey (CCHS) and administrative indicators from Manitoba’s 2025 health status report.

## Source snapshot (22 November 2026)
Statistics Canada Table 13-10-0972-01, released 6 May 2026, and Manitoba's 2025 Health Status of Manitobans Report. Reference periods are retained by measure.

The dataset contains 255 published observations. It covers seven survey indicators for Manitoba and its five health regions across five two-year periods, plus 45 report values on regional and income-related health outcomes.

- statcan_health_13100972.zip: https://www150.statcan.gc.ca/n1/tbl/csv/13100972-eng.zip (SHA-256 in source_manifest.json)
- mb_health_status2025.pdf: https://www.gov.mb.ca/asset_library/en/cppho/docs/health-status-2025.pdf (SHA-256 in source_manifest.json)

## Findings
- In the 2023/2024 CCHS, the Northern Health Region’s self-reported diabetes prevalence was 13.8%, compared with 8.7% for Manitoba. The difference of 5.1 percentage points is descriptive, and the Northern estimate has a wide confidence interval.
- In 2023, urban residents in the lowest income quintile had 465 emergency department visits per 1,000 people, compared with 209 in the highest quintile. The descriptive rate ratio was 2.22.
- During 2018–2022, the Manitoba report recorded 5.39 heart attack hospitalizations and deaths per 1,000 residents aged 40 and older in the Northern Health Region, compared with 2.25 in Winnipeg.

## Methods and validation
- Official CSV extraction for Manitoba and its five health regions
- Extraction of published chart values with report page references
- Reporting of survey confidence intervals and SQL calculations of percentage-point differences and rate ratios
- Independent source checks matched 255 normalized observations to the downloaded files.
- Null values represent unavailable/suppressed estimates. Use-with-caution flags are preserved.
- Confidence intervals come from the publishers, where provided. No synthetic patient or respondent records are included.

## Files and reproduction
- data.csv: normalized published aggregates, with source row/vector/page and URL.
- source_manifest.json: original download filenames, URLs, sizes and SHA-256 hashes.
- validation.json: independent row-level check results.
- analysis.sql and analysis_results.json: SQLite analysis and executed outputs.
- extract_public_data.py: source extraction, transformation and integrity assertions.
- validate_public_data.py: independent validation against Statistics Canada CSV records and Manitoba report chart labels.
- run_analysis.py: executes the SQL against data.csv.

To run SQL using the included exact snapshot:

    python run_analysis.py .

To re-extract source data, download the named source files above into downloads/. Install requirements.txt. Also install Poppler's pdftotext command.

    python extract_public_data.py --project manitoba --raw-dir downloads --output-dir rebuilt
    python validate_public_data.py --project manitoba --raw-dir downloads --data-dir rebuilt

Copy analysis.sql into rebuilt/manitoba/, then:

    python run_analysis.py rebuilt/manitoba

Publishers may revise the download files. The included source hashes identify this exact release. Reconcile revisions before comparing across vintages.

## Interpretation and limitations
The CCHS estimates use self-reported data from adults aged 18 and older. The survey may exclude or underrepresent some populations, particularly people living on reserves. Consider confidence intervals and differences in regional age structure. Statistics Canada’s 2022 survey redesign requires caution when comparing earlier and later survey cycles. The report-based indicators use distinct definitions and reporting periods. These regional associations cannot establish causes or individual risks.

This project uses public aggregate data and demonstrates portfolio analysis. It does not establish treatment effects or individual clinical risk.
