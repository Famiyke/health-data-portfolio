# Canadian hospital readmissions

## Purpose
How do 30-day urgent hospital readmission rates vary by geography, patient group and year?
This project compares CIHI’s risk-adjusted 30-day urgent readmission rates across years, jurisdictions and patient groups, including selected Manitoba health regions and hospitals.

## Source snapshot (22 November 2026)
Official CIHI no-breakdowns XLSX. Selected workbook rows have refresh date 25 August 2026. The indicator page reports a September 2026 update.

The dataset includes 952 observations across 11 fiscal years. It contains 937 published rates and 15 withheld values, covering Canada, provinces and territories, Manitoba health regions and selected hospitals.

- cihi_indicators.xlsx: https://www.cihi.ca/sites/default/files/document/indicator-library-indicator-data-no-breakdowns-en.xlsx (SHA-256 in source_manifest.json)

## Findings
- Canada’s published overall rate rose from 9.2 per 100 in 2015–2016 to 9.7 in 2025–2026, a difference of 0.5 percentage points.
- In 2025–2026, Manitoba’s published rate was 9.1 per 100, 0.6 percentage points below the Canadian benchmark. Consult the published confidence intervals and comparison flags when interpreting this difference.
- The national medical-patient readmission rate was 14.2 per 100 in 2025–2026. The latest workbook includes results for 12 jurisdictions. Québec’s data are unavailable.

## Methods and validation
- Extraction of CIHI workbook data with source-row references
- Comparison of risk-adjusted rates and confidence intervals
- SQLite analysis of reporting periods, jurisdictions and suppressed values
- Independent source checks matched 952 normalized observations to the downloaded files.
- Null values represent unavailable/suppressed estimates. Use-with-caution flags are preserved.
- Confidence intervals come from the publishers, where provided. No synthetic patient or respondent records are included.

## Files and reproduction
- data.csv: normalized published aggregates, with source row/vector/page and URL.
- source_manifest.json: original download filenames, URLs, sizes and SHA-256 hashes.
- validation.json: independent row-level check results.
- analysis.sql and analysis_results.json: SQLite analysis and executed outputs.
- extract_public_data.py: source extraction, transformation and integrity assertions.
- validate_public_data.py: independent validation against CIHI workbook rows.
- run_analysis.py: executes the SQL against data.csv.

To run SQL using the included exact snapshot:

    python run_analysis.py .

To re-extract source data, download the named source files above into downloads/. Install requirements.txt.

    python extract_public_data.py --project readmissions --raw-dir downloads --output-dir rebuilt
    python validate_public_data.py --project readmissions --raw-dir downloads --data-dir rebuilt

Copy analysis.sql into rebuilt/readmissions/, then:

    python run_analysis.py rebuilt/readmissions

Publishers may revise the download files. The included source hashes identify this exact release. Reconcile revisions before comparing across vintages.

## Interpretation and limitations
CIHI calculates risk-adjusted rates using observed and expected readmissions and a Canadian reference rate. Interpret comparisons in the context of patient case mix, data coverage, small volumes, reporting changes and hospital peer groups. These aggregate rates cannot predict individual risk, establish causal effects or measure preventable readmissions directly. Québec has no 2025–2026 record in the downloaded extract.

This project uses public aggregate data and demonstrates portfolio analysis. It does not establish treatment effects or individual clinical risk.
