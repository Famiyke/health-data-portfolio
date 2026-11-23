# Canadian mental health outcomes

## Purpose
How did mental health and access to care change between the two national surveys?
Compares 2012 and 2022 survey results on perceived mental health, selected conditions and access to care. Published confidence intervals and quality flags accompany the estimates.

## Source snapshot (22 November 2026)
Statistics Canada Tables 13-10-0465-01 and 13-10-0930-01, released 12 December 2024. Reference years 2012 and 2022.

The dataset includes 248 observations, with 225 numerical estimates (22 marked use with caution) and 23 withheld values. Results cover Canada, provinces, age groups, gender and selected population groups.

- statcan_mh_13100465.zip: https://www150.statcan.gc.ca/n1/tbl/csv/13100465-eng.zip (SHA-256 in source_manifest.json)
- statcan_mh_13100930.zip: https://www150.statcan.gc.ca/n1/tbl/csv/13100930-eng.zip (SHA-256 in source_manifest.json)

## Findings
- The estimated share reporting fair or poor mental health rose from 7.8% in 2012 to 15.3% in 2022.
- Reported unmet mental health care needs increased from 2.1% to 4.0%.
- In 2022, 16.8% reported professional mental health consultation or service use in the previous 12 months.

## Methods and validation
- Official CSV extraction with table vector and coordinate references
- Analysis of published survey-weighted estimates and confidence intervals
- SQL calculation of percentage-point changes and validation of quality flags
- Independent source checks matched 248 normalized observations to the downloaded files.
- Null values represent unavailable/suppressed estimates. Use-with-caution flags are preserved.
- Confidence intervals come from the publishers, where provided. No synthetic patient or respondent records are included.

## Walk through the code

mental_health() selects the relevant years and population groups from Statistics Canada. statcan_extract() matches each percentage to its published confidence bounds using the same survey dimensions.

The SQL joins 2012 and 2022 estimates for the same indicator and group before calculating the percentage-point change. A suppressed estimate remains blank; a quality flag stays with its estimate.

The validation script matches the original table vectors and coordinates. It checks both the percentages and the confidence bounds.

## Files and reproduction
- data.csv: normalized published aggregates, with source row/vector/page and URL.
- source_manifest.json: original download filenames, URLs, sizes and SHA-256 hashes.
- validation.json: independent row-level check results.
- analysis.sql and analysis_results.json: SQLite analysis and executed outputs.
- extract_public_data.py: project-specific source extraction and validation checks.
- validate_public_data.py: independent validation against Statistics Canada CSV records.
- run_analysis.py: executes the SQL against data.csv.

To run SQL using the included exact snapshot:

    python run_analysis.py .

To recreate this project, download its source files into downloads/. Run `python -m pip install -r requirements.txt`.

    python extract_public_data.py --project mental-health --raw-dir downloads --output-dir rebuilt
    python validate_public_data.py --project mental-health --raw-dir downloads --data-dir rebuilt

Copy analysis.sql into rebuilt/mental-health/, then:

    python run_analysis.py rebuilt/mental-health

Publishers may revise the download files. The included source hashes identify this exact release. Reconcile revisions before comparing across vintages.

## Interpretation and limitations
The repeat surveys cover different samples. In 2022, the survey excluded territories, people on reserves and other Indigenous settlements, full-time Canadian Armed Forces personnel and institutionalized populations. Interview mode changed from in person to telephone. Provincial and subgroup estimates require attention to confidence intervals and quality flags. Reported changes are descriptive.

This project uses public aggregate data and demonstrates portfolio analysis. It does not establish treatment effects or individual clinical risk.
