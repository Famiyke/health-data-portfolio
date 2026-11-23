# Canadian hospital readmissions

## Purpose
How do 30-day urgent readmission rates vary by geography, patient group and year?
Analyses the official CIHI Indicator Library using risk-adjusted overall, medical, surgical, pediatric and obstetric readmission rates, with national, provincial and selected Manitoba views.

## Source snapshot (22 November 2026)
Official CIHI no-breakdowns XLSX. Selected workbook rows have refresh date 25 August 2026. The indicator page reports a September 2026 update.

952 source observations, 937 numeric rates and 15 withheld. Eleven fiscal years. National/provincial indicators, Manitoba overall region and selected facility results.

- cihi_indicators.xlsx: https://www.cihi.ca/sites/default/files/document/indicator-library-indicator-data-no-breakdowns-en.xlsx (SHA-256 in source_manifest.json)

## Findings
- Canada's published overall rate was 9.7 per 100 in 2025–2026, a 0.5 percentage-point increase from 9.2 in 2015–2016.
- Manitoba reported 9.1 per 100 in 2025–2026, 0.6 percentage points below the published Canada benchmark. The source provides confidence intervals and comparison flags.
- The national medical-patient indicator was 14.2 per 100 in 2025–2026. The latest workbook contains 12 jurisdictions, with Québec unavailable.

## Methods and validation
- Streamed official workbook extraction and precise row tracing
- Risk-adjusted indicator comparison with confidence intervals
- SQLite comparisons by period and jurisdiction with suppression audit
- Independent source checks matched 952 normalized observations to the downloaded files.
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

    python extract_public_data.py --project readmissions --raw-dir downloads --output-dir rebuilt
    python validate_public_data.py --project readmissions --raw-dir downloads --data-dir rebuilt

Copy analysis.sql into rebuilt/readmissions/, then:

    python run_analysis.py rebuilt/readmissions

Publishers may revise the download files. The included source hashes identify this exact release. Reconcile revisions before comparing across vintages.

## Interpretation and limitations
CIHI calculates the rate using observed and expected readmissions and a Canadian reference rate. Case mix, coverage, small volumes, reporting changes and peer groups matter. No individual risk prediction, causal inference or direct calculation of preventable readmissions. Québec has no 2025–2026 record in the downloaded extract.

This project uses public aggregate data and demonstrates portfolio analysis. It does not establish treatment effects or individual clinical risk.
