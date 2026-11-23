# Manitoba regional health equity

## Purpose
How do health indicators and healthcare utilization vary across Manitoba health regions and income groups?
Combines the current Statistics Canada CCHS two-year health-region table with exact administrative and income-related values in Manitoba's 2025 health-status report.

## Source snapshot (22 November 2026)
Statistics Canada Table 13-10-0972-01, released 6 May 2026, and Manitoba's 2025 Health Status of Manitobans Report. Reference periods are retained by measure.

255 published observations. Seven survey indicators for five health regions plus Manitoba across five two-year periods, and 45 official report values on regional and income-related health outcomes.

- statcan_health_13100972.zip: https://www150.statcan.gc.ca/n1/tbl/csv/13100972-eng.zip (SHA-256 in source_manifest.json)
- mb_health_status2025.pdf: https://www.gov.mb.ca/asset_library/en/cppho/docs/health-status-2025.pdf (SHA-256 in source_manifest.json)

## Findings
- In the 2023/2024 CCHS, Northern Health Region's self-reported diabetes estimate was 13.8% versus 8.7% for Manitoba. The 5.1-point gap is descriptive and the Northern estimate has a wide confidence interval.
- In 2023, urban emergency department visits were 465 versus 209 per 1,000 for the lowest and highest urban income quintiles. The descriptive rate ratio was 2.22.
- The Manitoba report shows heart attack hospitalizations and deaths of 5.39 per 1,000 residents aged 40+ in Northern and 2.25 in Winnipeg during 2018–2022.

## Methods and validation
- Official CSV filtering to Manitoba and its five health regions
- Published chart-label extraction with report page tracing
- Survey confidence intervals and SQL descriptive gap/ratio calculations
- Independent source checks matched 255 normalized observations to the downloaded files.
- Null values represent unavailable/suppressed estimates. Use-with-caution flags are preserved.
- Confidence intervals come from the publishers, where provided. No synthetic patient or respondent records are included.

## Files and reproduction
- data.csv: normalized published aggregates, with source row/vector/page and URL.
- source_manifest.json: original download filenames, URLs, sizes and SHA-256 hashes.
- validation.json: independent row-level check results.
- analysis.sql and analysis_results.json: SQLite analysis and executed outputs.
- extract_public_data.py: source extraction, transformation and integrity assertions.
- validate_public_data.py: independent check using openpyxl, CSV and separately verified PDF labels.
- run_analysis.py: executes the SQL against data.csv.

To run SQL using the included exact snapshot:

    python run_analysis.py .

To re-extract source data, download the named source files above into downloads/. Install requirements.txt. For the Manitoba case also install Poppler's pdftotext command.

    python extract_public_data.py --project manitoba --raw-dir downloads --output-dir rebuilt
    python validate_public_data.py --project manitoba --raw-dir downloads --data-dir rebuilt

Copy analysis.sql into rebuilt/manitoba/, then:

    python run_analysis.py rebuilt/manitoba

Publishers may revise the download files. The included source hashes identify this exact release. Reconcile revisions before comparing across vintages.

## Interpretation and limitations
The CCHS estimates are self-reported for adults 18+ and may exclude or underrepresent some populations, particularly on-reserve residents. Survey confidence intervals and differing age structures matter. The 2022 CCHS redesign requires caution when comparing earlier and later cycles. Report-based measures have distinct definitions and years. Regional associations do not establish causes or individual-level risks.

This project uses public aggregate data and demonstrates portfolio analysis. It does not establish treatment effects or individual clinical risk.
