# Canadian retail sales forecasting

## Research question
How do Canadian retail sales vary by season and geography, and how accurately can two time-series models forecast them?

Uses monthly retail sales to compare regional growth, examine seasonal patterns and forecast six months ahead. Two models are compared on rolling validation periods and evaluated on a separate holdout period.

## Coverage
1,806 official observations; 117 unadjusted months per jurisdiction (January 2017 to September 2026) and the latest 12 seasonally adjusted months. Six-month forecasts for all 14 geographies, including Canada separately.

## Official sources
- Statistics Canada 20-10-0056-01: https://www150.statcan.gc.ca/n1/tbl/csv/20100056-eng.zip

Source snapshot retrieved 22 November 2026; see source_manifest.json for file hashes and source URLs.

## Methods and data quality
Forecasts use monthly unadjusted positive nominal sales. Compare seasonal naive (the same month one year earlier) with a log-linear trend and 11 month indicators fitted using least squares. Four six-month rolling validation windows run from October 2023 to September 2025. Model choice minimizes validation WAPE, with seasonal naive winning ties. Two later six-month holdout windows run from October 2025 to September 2026 and are excluded from selection. Models are refitted at each origin using observations already available, and the selected model is refit through September 2026 for forecasts October 2026 to March 2027. WAPE is the sum of absolute errors divided by the sum of actuals, multiplied by 100. MAE is reported in CAD millions. Retrospective evaluation uses the downloaded vintage, which may contain revisions. Regional forecasts are independent, so they are not constrained to sum to the national forecast.

SQL analyses: regional seasonally adjusted sales, same-month year-over-year nominal sales growth, independent holdout WAPE/MAE recomputation and six-month forecast export. Forecasts and observed rows remain separate in the downloadable data.

## Key findings
- Canada’s seasonally adjusted retail sales reached $75.31 billion in September 2026.
- For Canada, the selected log-trend model with month effects had a holdout weighted absolute percentage error (WAPE) of 1.72%, compared with 3.81% for the seasonal naive model.
- May had the highest average national seasonal index (108.4) across 2021–2025. The model forecasts $2.589 billion in Manitoba retail sales for October 2026.

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
Sales are nominal aggregates, so changes include price effects. The forecasts describe broad retail markets. Backtests use one historical data release, which may include revisions. Economic shocks and structural changes can reduce forecasting accuracy. Forecasts are point estimates without probability intervals.
