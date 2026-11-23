# Canadian mental health outcomes

## Purpose
How do perceived mental health, conditions and access to care vary across the Canadian population?
Reproduces weighted Statistics Canada mental health and access-to-care estimates, compares the 2012 and 2022 surveys, and retains published confidence intervals and disclosure flags.

## Source snapshot (22 November 2026)
Statistics Canada Tables 13-10-0465-01 and 13-10-0930-01, released 12 December 2024. Reference years 2012 and 2022.

248 source observations. 225 numeric estimates, including 22 marked use with caution. 23 withheld. National, provincial, age, gender and selected population-group estimates.

- statcan_mh_13100465.zip: https://www150.statcan.gc.ca/n1/tbl/csv/13100465-eng.zip (SHA-256 in source_manifest.json)
- statcan_mh_13100930.zip: https://www150.statcan.gc.ca/n1/tbl/csv/13100930-eng.zip (SHA-256 in source_manifest.json)

## Findings
- Fair or poor perceived mental health was 7.8% in 2012 and 15.3% in 2022, a descriptive increase of 7.5 percentage points.
- In 2022, 4.0% of the surveyed population reported mental health care needs that were not met, compared with 2.1% in 2012.
- In 2022, 16.8% reported professional mental health consultation or service use during the previous 12 months.

## Methods and validation
- Official CSV extraction by table vector and coordinate
- Survey-weighted aggregate estimates with confidence intervals
- SQL percentage-point changes and quality-flag audit
- Independent source checks matched 248 normalized observations to the downloaded files.
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

    python extract_public_data.py --project mental-health --raw-dir downloads --output-dir rebuilt
    python validate_public_data.py --project mental-health --raw-dir downloads --data-dir rebuilt

Copy analysis.sql into rebuilt/mental-health/, then:

    python run_analysis.py rebuilt/mental-health

Publishers may revise the download files. The included source hashes identify this exact release. Reconcile revisions before comparing across vintages.

## Interpretation and limitations
The surveys are repeated cross-sections. Coverage excludes the territories, persons living on reserves and other Indigenous settlements, full-time Canadian Armed Forces personnel and institutionalized populations in 2022. The 2012 interviews were in person and the 2022 interviews were by telephone. The 2022 survey was designed for national and selected population-group estimates. Provincial estimates require attention to confidence intervals and quality flags. Differences are descriptive unless formally tested. No patient-level or causal conclusions.

This project uses public aggregate data and demonstrates portfolio analysis. It does not establish treatment effects or individual clinical risk.
