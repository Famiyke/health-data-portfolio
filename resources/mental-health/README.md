# Canadian mental health outcomes

## Purpose
How do perceived mental health, mental health conditions and access to care vary across the Canadian population?
This project compares Statistics Canada’s weighted mental health and access-to-care estimates for 2012 and 2022. It retains published 95% confidence intervals and data-quality flags.

## Source snapshot (22 November 2026)
Statistics Canada Tables 13-10-0465-01 and 13-10-0930-01, released 12 December 2024. Reference years 2012 and 2022.

The dataset includes 248 observations, with 225 numerical estimates (22 marked use with caution) and 23 withheld values. Results cover Canada, provinces, age groups, gender and selected population groups.

- statcan_mh_13100465.zip: https://www150.statcan.gc.ca/n1/tbl/csv/13100465-eng.zip (SHA-256 in source_manifest.json)
- statcan_mh_13100930.zip: https://www150.statcan.gc.ca/n1/tbl/csv/13100930-eng.zip (SHA-256 in source_manifest.json)

## Findings
- The estimated percentage of people reporting fair or poor perceived mental health increased from 7.8% in 2012 to 15.3% in 2022, a difference of 7.5 percentage points.
- In 2022, 4.0% of the surveyed population reported unmet mental health care needs, compared with 2.1% in 2012.
- In 2022, 16.8% reported professional mental health consultation or service use in the previous 12 months.

## Methods and validation
- Official CSV extraction with table vector and coordinate references
- Analysis of published survey-weighted estimates and confidence intervals
- SQL calculation of percentage-point changes and validation of quality flags
- Independent source checks matched 248 normalized observations to the downloaded files.
- Null values represent unavailable/suppressed estimates. Use-with-caution flags are preserved.
- Confidence intervals come from the publishers, where provided. No synthetic patient or respondent records are included.

## Files and reproduction
- data.csv: normalized published aggregates, with source row/vector/page and URL.
- source_manifest.json: original download filenames, URLs, sizes and SHA-256 hashes.
- validation.json: independent row-level check results.
- analysis.sql and analysis_results.json: SQLite analysis and executed outputs.
- extract_public_data.py: source extraction, transformation and integrity assertions.
- validate_public_data.py: independent validation against Statistics Canada CSV records.
- run_analysis.py: executes the SQL against data.csv.

To run SQL using the included exact snapshot:

    python run_analysis.py .

To re-extract source data, download the named source files above into downloads/. Install requirements.txt.

    python extract_public_data.py --project mental-health --raw-dir downloads --output-dir rebuilt
    python validate_public_data.py --project mental-health --raw-dir downloads --data-dir rebuilt

Copy analysis.sql into rebuilt/mental-health/, then:

    python run_analysis.py rebuilt/mental-health

Publishers may revise the download files. The included source hashes identify this exact release. Reconcile revisions before comparing across vintages.

## Interpretation and limitations
The two surveys are repeated cross-sectional studies. In 2022, the survey excluded the territories, people living on reserves and other Indigenous settlements, full-time Canadian Armed Forces personnel and institutionalized populations. Interviews took place in person in 2012 and by telephone in 2022. The 2022 survey was designed for national and selected population-group estimates. Interpret provincial estimates using confidence intervals and quality flags. Reported differences are descriptive unless formally tested. The aggregate data cannot establish individual-level or causal conclusions.

This project uses public aggregate data and demonstrates portfolio analysis. It does not establish treatment effects or individual clinical risk.
