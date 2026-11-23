# Canadian hospital readmissions

## Purpose
Which patient groups and jurisdictions have higher reported urgent readmission rates?
Examines CIHI’s risk-adjusted 30-day urgent readmission rates across 11 fiscal years. Compare provinces, patient groups, and selected Manitoba health regions and hospitals.

## Source snapshot (22 November 2026)
Official CIHI no-breakdowns XLSX. Selected workbook rows have refresh date 25 August 2026. The indicator page reports a September 2026 update.

The dataset includes 952 observations across 11 fiscal years. It contains 937 published rates and 15 withheld values, covering Canada, provinces and territories, Manitoba health regions and selected hospitals.

- cihi_indicators.xlsx: https://www.cihi.ca/sites/default/files/document/indicator-library-indicator-data-no-breakdowns-en.xlsx (SHA-256 in source_manifest.json)

## Findings
- Canada’s overall rate increased from 9.2 in 2015–2016 to 9.7 per 100 eligible discharges in 2025–2026.
- Manitoba reported 9.1 per 100 in 2025–2026, compared with Canada’s 9.7. Consider the published confidence intervals and comparison flags.
- The national medical-patient rate was 14.2 per 100 in 2025–2026. Québec has no result in the latest workbook.

## Methods and validation
- Extraction of CIHI workbook data with source-row references
- Comparison of risk-adjusted rates and confidence intervals
- SQLite analysis of reporting periods, jurisdictions and suppressed values
- Independent source checks matched 952 normalized observations to the downloaded files.
- Null values represent unavailable/suppressed estimates. Use-with-caution flags are preserved.
- Confidence intervals come from the publishers, where provided. No synthetic patient or respondent records are included.

## Walk through the code

In extract_public_data.py, readmissions() streams the large CIHI workbook and selects the risk-adjusted rates for the relevant groups and locations. It saves the workbook row, confidence interval and publication status with every observation.

The four queries in analysis.sql cover the national trend, provincial comparisons with Canada, patient groups and publication flags. A provincial rate minus the Canadian rate gives the difference per 100 eligible episodes.

validate_public_data.py reads the workbook with openpyxl and checks the published values and inclusion rules independently of the XML extractor.

## Files and reproduction
- data.csv: normalized published aggregates, with source row/vector/page and URL.
- source_manifest.json: original download filenames, URLs, sizes and SHA-256 hashes.
- validation.json: independent row-level check results.
- analysis.sql and analysis_results.json: SQLite analysis and executed outputs.
- extract_public_data.py: project-specific source extraction and validation checks.
- validate_public_data.py: independent validation against CIHI workbook rows.
- run_analysis.py: executes the SQL against data.csv.

To run SQL using the included exact snapshot:

    python run_analysis.py .

To recreate this project, download its source files into downloads/. Run `python -m pip install -r requirements.txt`.

    python extract_public_data.py --project readmissions --raw-dir downloads --output-dir rebuilt
    python validate_public_data.py --project readmissions --raw-dir downloads --data-dir rebuilt

Copy analysis.sql into rebuilt/readmissions/, then:

    python run_analysis.py rebuilt/readmissions

Publishers may revise the download files. The included source hashes identify this exact release. Reconcile revisions before comparing across vintages.

## Interpretation and limitations
CIHI adjusts rates for patient case mix. Compare hospitals in the context of their peer groups, reporting coverage and discharge volumes. Readmission rates alone cannot establish avoidability or individual risk. Québec has no 2025–2026 record in the extract.

This project uses public aggregate data and demonstrates portfolio analysis. It does not establish treatment effects or individual clinical risk.
