# Manitoba regional health equity

## Purpose
Where do Manitoba’s regions and income groups differ in health outcomes and use of care?
Examines regional differences in chronic disease, mental health and service use, alongside income-related gaps in emergency care and cardiovascular outcomes. Combines Canadian Community Health Survey estimates with Manitoba’s 2025 health status report.

## Source snapshot (22 November 2026)
Statistics Canada Table 13-10-0972-01, released 6 May 2026, and Manitoba's 2025 Health Status of Manitobans Report. Reference periods are retained by measure.

The dataset contains 255 published observations. It covers seven survey indicators for Manitoba and its five health regions across five two-year periods, plus 45 report values on regional and income-related health outcomes.

- statcan_health_13100972.zip: https://www150.statcan.gc.ca/n1/tbl/csv/13100972-eng.zip (SHA-256 in source_manifest.json)
- mb_health_status2025.pdf: https://www.gov.mb.ca/asset_library/en/cppho/docs/health-status-2025.pdf (SHA-256 in source_manifest.json)

## Findings
- In the 2023/2024 survey, self-reported diabetes prevalence was 13.8% in the Northern Health Region and 8.7% province-wide. The Northern estimate has a wide confidence interval.
- In 2023, urban residents in the lowest income quintile had 465 emergency visits per 1,000 people, compared with 209 in the highest quintile (2.22 times as many).
- During 2018–2022, the Manitoba report recorded 5.39 heart attack hospitalizations and deaths per 1,000 residents aged 40 and older in the Northern Health Region and 2.25 in Winnipeg.

## Methods and validation
- Official CSV extraction for Manitoba and its five health regions
- Extraction of published chart values with report page references
- Reporting of survey confidence intervals and SQL calculations of percentage-point differences and rate ratios
- Independent source checks matched 255 normalized observations to the downloaded files.
- Null values represent unavailable/suppressed estimates. Use-with-caution flags are preserved.
- Confidence intervals come from the publishers, where provided. No synthetic patient or respondent records are included.

## Walk through the code

manitoba() extracts regional survey estimates from the Statistics Canada table. extract_mb_report() reads the printed Manitoba report figures with their page references.

The queries compare regional diabetes estimates with the provincial estimate and calculate an emergency visit rate ratio from the lowest and highest income quintiles. The original survey and administrative measures retain their different units and periods.

The validator checks the survey table vectors and the labeled report figures separately.

## Files and reproduction
- data.csv: normalized published aggregates, with source row/vector/page and URL.
- source_manifest.json: original download filenames, URLs, sizes and SHA-256 hashes.
- validation.json: independent row-level check results.
- analysis.sql and analysis_results.json: SQLite analysis and executed outputs.
- extract_public_data.py: project-specific source extraction and validation checks.
- validate_public_data.py: independent validation against Statistics Canada CSV records and Manitoba report chart labels.
- run_analysis.py: executes the SQL against data.csv.

To run SQL using the included exact snapshot:

    python run_analysis.py .

To recreate this project, download its source files into downloads/. Run `python -m pip install -r requirements.txt`. The Manitoba report parser also requires Poppler’s `pdftotext` command. Also install Poppler's pdftotext command.

    python extract_public_data.py --project manitoba --raw-dir downloads --output-dir rebuilt
    python validate_public_data.py --project manitoba --raw-dir downloads --data-dir rebuilt

Copy analysis.sql into rebuilt/manitoba/, then:

    python run_analysis.py rebuilt/manitoba

Publishers may revise the download files. The included source hashes identify this exact release. Reconcile revisions before comparing across vintages.

## Interpretation and limitations
Survey estimates reflect self-reported health among adults aged 18 and older. Some populations, including people on reserves, may be excluded or underrepresented. Consider confidence intervals and regional age structure. The 2022 CCHS redesign affects comparisons across survey cycles. Administrative indicators have their own populations and definitions. These findings describe inequalities without establishing their causes.

This project uses public aggregate data and demonstrates portfolio analysis. It does not establish treatment effects or individual clinical risk.
