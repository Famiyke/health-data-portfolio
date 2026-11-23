# Canadian retail sales forecasting

## Research question
How do Canadian retail sales vary by region and season, and how accurately can established time-series baselines forecast the next six months?

This project analyses monthly retail sales across Canada and all provinces and territories, quantifies regional growth and seasonal demand patterns, and tests two forecasting methods using rolling-origin validation before producing six-month forecasts.

## Coverage
1,806 official observations; 117 unadjusted months per jurisdiction (January 2017 to September 2026) and the latest 12 seasonally adjusted months. Six-month forecasts for all 14 geographies, including Canada separately.

## Official sources
- Statistics Canada 20-10-0056-01: https://www150.statcan.gc.ca/n1/tbl/csv/20100056-eng.zip

Source snapshot retrieved 22 November 2026; see source_manifest.json for file hashes and source URLs.

## Methods and data quality
Forecasts use monthly unadjusted positive nominal sales. Compare seasonal naive (the same month one year earlier) with a log-linear trend and 11 month indicators fitted using least squares. Four six-month rolling validation windows run from October 2023 to September 2025. Model choice minimizes validation WAPE, with seasonal naive winning ties. Two later six-month holdout windows run from October 2025 to September 2026 and are excluded from selection. Models are refitted at each origin using observations already available, and the selected model is refit through September 2026 for forecasts October 2026 to March 2027. WAPE is the sum of absolute errors divided by the sum of actuals, multiplied by 100. MAE is reported in CAD millions. Retrospective evaluation uses the downloaded vintage, which may contain revisions. Regional forecasts are independent, so they are not constrained to sum to the national forecast.

SQL analyses: regional seasonally adjusted sales, same-month year-over-year nominal sales growth, independent holdout WAPE/MAE recomputation and six-month forecast export. Forecasts and observed rows remain separate in the downloadable data.

## Key findings
- Canada’s seasonally adjusted retail sales were $75.31 billion in September 2026.
- For Canada, the validation-selected Log trend + month effects model achieved holdout WAPE of 1.72%; seasonal naive holdout WAPE was 3.81%. Lower is better.
- Across 2021–2025, May had the highest average national seasonal index (108.4). Manitoba’s October 2026 portfolio-model forecast was $2.589 billion.

## Independent validation
1,806 source records independently reconciled to official CSV rows or Excel cells. See validation.json and analysis_results.json.

## Reproduce analysis
Unzip the workflow. Run `python run_analysis.py .` to execute SQL against the included CSV snapshots.

To recreate from original files, install requirements.txt and run:

    python build_expansion.py --raw-dir raw --output-dir rebuilt --project retail --download
    python validate_expansion.py --raw-dir raw --output-dir rebuilt --project retail

The current public release may differ from the recorded source hashes; review revisions.

## BI project
The packaged Tableau workbook contains Canadian and Manitoba historical/forecast views, regional sales and national model accuracy. Open retail-forecast.twbx in Tableau Desktop or Tableau Public Desktop. Desktop execution was not available here. The web dashboard is independently tested.

## Interpretation and limitations
Nominal aggregate retail sales include price changes. These are broad market indicators, not individual store revenue or inventory demand. Model selection uses one historical release rather than first-release data vintages, so backtests do not establish real-time operational accuracy. Structural changes, economic shocks and revisions may affect forecasts. All future estimates are point forecasts without a probability interval.
