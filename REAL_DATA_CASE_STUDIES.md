# Verified public-data projects | 17 November 2026

This portfolio includes three newly built, reproducible public-data case studies. Their **source-derived indicators** are distinct from previously constructed, clearly labelled synthetic demonstrations.

## 1. Canadian national health expenditure | actual CIHI NHEX Series A

- **Source:** CIHI, National Health Expenditure Trends 2026, Series A, Summary Table A.1.a, released November 10, 2026
- **Actual/revised observations:** 1975–2024 (50 years); **forecast years:** 2025 and 2026, not observed actuals
- **Dataset:** 52 yearly records with direct source URL, worksheet/table, row, units, current-dollar and 2010 constant-dollar expenditure, per capita and GDP share
- **Check:** Official XLSX downloaded during the workflow, source table and forecast years validated
- **Examples:** Actual/revised 2024 health spending $392.82 billion CAD; 2026 forecast $433.12 billion CAD
- [Real dataset](https://github.com/Famiyke/health-expenditure-canada/blob/main/official_nhex_2026_national.csv)
- [Reproducible extraction](https://github.com/Famiyke/health-expenditure-canada/blob/main/official_nhex_2026.py)
- [Findings and methodology](https://github.com/Famiyke/health-expenditure-canada/blob/main/OFFICIAL_NHEX_2026_FINDINGS.md)
- [Passing CI](https://github.com/Famiyke/health-expenditure-canada/actions/workflows/build-official-nhex.yml)

## 2. Diabetes prevalence in Nova Scotia | CCDSS-derived provincial open data

- **Source:** Government of Nova Scotia Open Data, `cumi-sw99`, diabetes crude prevalence; the publisher identifies CCDSS as its underlying surveillance source
- **Coverage:** 2000–2022, four Nova Scotia health zones, two sex groups, seven age bands, aged 20+
- **Records:** 1,288 published strata; validated all source rates against published counts and population within the source's rate-rounding precision
- **Method:** Count-weighted aggregation (case counts divided by population), **not** simple averaging of subgroup rates
- **Examples:** Nova Scotia crude prevalence aged 20+ of 6.56% in 2000 and 12.43% in 2022
- **Limit:** Crude, non-age-standardized **provincial** rates; not national estimates or causal effects
- [Source-linked provincial data](https://github.com/Famiyke/chronic-disease-surveillance-canada/blob/main/official_ns_diabetes_2000_2022.csv)
- [Four-zone data](https://github.com/Famiyke/chronic-disease-surveillance-canada/blob/main/official_ns_diabetes_zone_2000_2022.csv)
- [Findings](https://github.com/Famiyke/chronic-disease-surveillance-canada/blob/main/OFFICIAL_NS_DIABETES_FINDINGS.md)
- [Passing CI](https://github.com/Famiyke/chronic-disease-surveillance-canada/actions/workflows/build-official-diabetes.yml)

## 3. Ontario surgical access | publicly reported FAO figures based on Ontario Health data

- **Source:** Financial Accountability Office of Ontario's 2023 Health Sector Spending Plan Review, Appendix tables A-1 to A-3
- **Coverage:** 2019–2022, 22 Ontario surgical service areas plus report total
- **Records:** 276 source-linked long-format observations spanning yearly surgeries, average waitlist and FAO-estimated wait months
- **Examples:** Reported annual surgeries fell from 649,299 (2019) to 555,487 (2022). FAO-estimated aggregate waiting months rose from 3.7 to 5.5.
- **Critical definition:** FAO's estimated waiting months are a **Little's Law throughput/waitlist proxy**, not a patient-level Wait 2 outcome. The 2022 average waitlist reflects January–September rather than a full year.
- **Limit:** 2023 report vintage, last data year 2022; not a statement of 2026 waiting times or individual hospital performance
- [Actual published-source data](https://github.com/Famiyke/ontario-wait-times/blob/main/official_ontario_fao_surgery_2019_2022.csv)
- [Extraction and checks](https://github.com/Famiyke/ontario-wait-times/blob/main/official_ontario_fao_surgery.py)
- [Findings](https://github.com/Famiyke/ontario-wait-times/blob/main/OFFICIAL_ONTARIO_SURGERY_FINDINGS.md)
- [Passing CI](https://github.com/Famiyke/ontario-wait-times/actions/workflows/build-official-ontario.yml)

## Boundaries of validation

These pipelines validate the **reproducibility of extraction and arithmetic against published source tables**. They do not establish causal relationships, survey representativeness, age-standardized comparisons, or independent verification of the publishers' original data collection processes.

Three older projects remain **synthetic demonstrations**: hospital readmissions, mental health outcomes, and Manitoba regional equity. The older simulated portions of the expenditure, chronic-disease and Ontario repositories also remain separate, and their legacy Power BI/Tableau files should not be interpreted as the source of the real-data analyses.
