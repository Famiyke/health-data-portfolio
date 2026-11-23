> **Historical review, 16–17 November 2026.** The [current portfolio](https://famiyke.github.io/health-data-portfolio/) now uses official-source data for all six case studies. See the [current source documentation](resources/index.html). The following record describes the earlier version.

# Healthcare Analytics Portfolio — Quality Audit

**Audit date:** 16 November 2026  
**Scope:** GitHub Pages homepage and six linked project repositories  
**Audit type:** Static code and documentation inspection, repository file inventory, and limited public-link retrieval.

## Legacy dashboard remediation and safe replacement: 17 November 2026

Four independently navigable, responsive browser dashboards were built from verified repo data sources and reviewed synthetic generators. They require no Power BI service login:

- [Nova Scotia diabetes, real CCDSS-derived data](dashboards/diabetes.html)
- [Ontario surgical access, real FAO public aggregates](dashboards/ontario.html)
- [Mental health, corrected synthetic dataset](dashboards/mental-health.html)
- [Hospital readmissions, simulated methods demonstration](dashboards/readmissions.html)

Each page displays a prominent **REAL PUBLIC DATA / SIMULATED DATA ONLY** disclaimer, source and code links, limitations, keyboard-accessible data controls, data values and accessible tables. The two real-data dashboards use existing officially sourced CSV outputs, while the mental health and readmission versions regenerate the synthetic data from the current Python generator. The mental health page excludes identity disparity charts, ensures rating groups are exhaustive and omits subgroups with fewer than 30 synthetic records.

GitHub Actions `Build and verify reviewed healthcare dashboards` passed and committed all five static HTML pages, including the dashboard index. The dedicated Chromium dashboard test passed for all four dashboards at 375px and 1440px, including interactive filters and no horizontal scrolling.

**Remaining scope limitation:** The original Power BI PBIX and remote Tableau Public dashboards were **not updated in their native editing environments**. Their old visuals, source labels and underlying data may still be wrong if opened directly. The reviewed web dashboards are independent replacements for recruiter-facing presentation, not claims of repaired or refreshed PBIX/TWB files.

## Real-data rebuild completed on 17 November 2026

**Three reproducible official-source case studies were added and passed GitHub Actions tests:**

1. **Health Expenditure:** Real CIHI NHEX 2026 Series A national totals, 52 yearly source-linked records, actual/revised years 1975–2024, forecasts 2025–2026; a separate descriptive analysis reports spending, per capita, GDP share, and nominal growth.
2. **Chronic Disease Surveillance:** Real Government of Nova Scotia CCDSS-derived diabetes prevalence source `cumi-sw99`, 1,288 age/sex/zone/year strata, 23 provincial annual rates and 92 zone-year rates. All source-row rates were checked against count/population arithmetic.
3. **Ontario Surgery:** Real Financial Accountability Office of Ontario tables A-1 to A-3 based on Ontario Health data, 276 metric-year records for 2019–2022, preserving the crucial distinction between observed annual surgery counts and FAO-estimated waiting months.

Project descriptions and portfolio homepage were updated. The homepage hero no longer presents stale, modeled mental-health disparity figures. It now plots actual CIHI expenditure totals through 2024 and clearly identifies a separate 2026 forecast.

[Full source references, reproducibility links and boundaries](REAL_DATA_CASE_STUDIES.md).

**Not rebuilt from official patient-level data:** hospital readmissions, mental health outcomes and Manitoba equity. Their existing demonstration records and dashboards remain synthetic. Ontario's original Tableau facility ranks and the original chronic-disease Power BI visualization do **not** represent the new official-source series.

This marks a substantive improvement in external source provenance, **not** universal verification of the six original dashboard packages.

## Remediation update: 17 November 2026

### Responsive design regression fixed

A Chromium regression test initially found a **375px mobile viewport overflowing to 474px**. The cause was an About-section skills grid that retained a desktop column layout. The CSS was corrected for narrow viewports. The subsequent GitHub Actions run **44081018123 passed** desktop (1440px), tablet (768px), and mobile (375px) horizontal-overflow and page-structure checks. The revised GitHub Pages build also completed successfully.



**Repaired and tested**
- Mental health synthetic generator now uses mutually exclusive/exhaustive five-level self-rated mental-health categories. Generated "good or better" agrees with scale levels 1–3, while "fair or poor" uses 4–5. The analysis asserts that categories sum to 100%, and provincial groups with fewer than 30 generated records are suppressed from printed comparisons.
- Removed the simulation's unsupported imposed Indigenous-related prevalence and unmet-care multipliers. Identity-comparison claims were withdrawn from the updated script.
- Added `validate_demo.py` regression tests and integrated them into GitHub Actions. The latest mental health workflow completed successfully.
- Replaced misleading "published-source" claims in all five affected synthetic data generators with statements distinguishing model assumptions from real extracted data.
- Updated all six project READMEs for accurate run instructions and source status; stopped promoting uncorrected Power BI or Tableau charts as verified reporting.
- Updated the public portfolio page to distinguish an archived Power BI prototype and a source-checked CIHI comparison from unvalidated model outputs.

**Not safe to claim as fixed**
- Existing mental-health and chronic-disease PBIX packages still hold their historical report data/visuals, including misleading captions. Python changes do **not** update embedded Power BI data. They need refresh, corrected DAX/labels and republishing from Power BI Desktop.
- Tableau Public visualizations remain controlled by their publisher and still need prominent on-dashboard synthetic-data warnings, even though README links and homepage promotion have been corrected.
- Archived mental-health screenshots are not evidence of the revised analytical outputs.
- Real-world health-system result verification for the other projects remains incomplete.

**Release interpretation:** The updated GitHub repositories can demonstrate synthetic analytics methods. Do not publish or use the archived dashboard figures as real healthcare findings.

## Follow-up runtime validation (16–17 November 2026)

GitHub Actions clean-environment smoke tests were added and executed in all six project repositories.

**Result: all six passed** the Python compilation, generated-dataset creation and project analysis sequence using Python 3.11 and pinned interpreter family (package versions are currently unpinned). These runs confirm basic reproducibility of the simulated workflow, **not** scientific accuracy against official datasets.

Additional integrity checks of the archive structure of the Power BI PBIX files and readability of the Excel XLSX workbooks passed in all four applicable repositories. Archive integrity does not confirm correct DAX measures, formulas, dashboard design or numerical reconciliation.

A GitHub Actions direct HTTP check of the deployed GitHub Pages homepage passed on 17 November 2026. It verified the featured project heading, experience section ID, methods heading, data-disclosure content and absence of the former '24 Verified Findings' text. The generic web retrieval tool still surfaced cached old HTML. Full visual and accessibility browser testing remains outstanding.

**Outstanding:** validate calculations and interpretability against original government sources, open and interact with Power BI/Tableau dashboards, inspect charts and mobile rendering in a browser, and review accessibility with assistive tools.

## Detailed evidence and dashboard review (17 November 2026)

### Independently checked public-source anchors

- **CIHI NHEX:** CIHI's 2025 data-in-brief publication estimates **$398.8B for 2025** (forecast), while the 2026 release projects **$433B for 2026** and lists 2023 at approximately **$362B**. The portfolio's expenditure workbook displays **$361B for 2023**, a figure consistent with the older CIHI release vintage, but its precise cell mapping remains unverified. Do not combine historical release vintages without a revision note. Sources: https://www.cihi.ca/sites/default/files/document/health-expenditure-data-in-brief-2025-en.pdf ; https://www.cihi.ca/en/national-health-expenditure-trends/nhex-trends-reports/nhex-trends-2026-snapshot
- **PHAC CCDSS:** The standard published age groups differ from the simulated project's groups. PHAC suppresses estimates when underlying unrounded counts are below 10. Source: https://health-infobase.canada.ca/ccdss/Methods
- **Ontario Health:** Official surgical statistics distinguish Wait 1 from Wait 2 and account for procedure, priority and reporting period. The generated hospital dataset is not an observed performance extract. Source: https://www.ontariohealth.ca/system/reporting/wait-times/wait-times-results
- **Statistics Canada CCHS:** Public-use microdata require appropriate survey weighting for population estimates. This project has no validated official weighted results. Source: https://www.statcan.gc.ca/en/statistical-programs/document/3226_D7_T9_V3-eng.pdf
- **Manitoba Health:** The project uses generated RHA records rather than an official compiled extraction. Source catalogue: https://www.gov.mb.ca/health/annstats/

Every project repository now includes `SOURCE_VALIDATION.md` recording what the official source establishes and which project figures remain unverified.

### Dashboard and workbook findings

| Deliverable | Structural inspection | Outstanding presentation/data issue |
|---|---|---|
| Hospital Readmission Tableau | Published page and visualization loaded in headless Chromium | Visible dashboard lacks synthetic-data banner; region and diagnosis figures are simulated |
| Ontario Surgical Wait Times Tableau | Published page and visualization loaded in headless Chromium | Named hospitals and apparent performance rankings lack synthetic-data banner |
| Chronic Disease Power BI | Four report pages; 6, 3, 2 and 2 visual containers | No simulated-data disclosure phrase found in page layout; actual visual rendering and DAX not validated |
| Mental Health Power BI | Four report pages; 7, 3, 3 and 5 visual containers | No simulated-data disclosure phrase found in page layout; actual visual rendering and DAX not validated |
| Health Expenditure Excel | Six original sheets; four charts and 115 formulas retained | Earlier source vintage and source-cell mapping require reconciliation; first provenance sheet now added |
| Manitoba Equity Excel | Four original sheets; two charts and no formulas | Derived figures are stored values rather than spreadsheet formulas; first synthetic-data provenance sheet now added |

Power BI structure scans are evidence of report contents, **not** a substitute for Power BI Desktop visual and data validation. Tableau browser screenshots were captured but a first-visit Tableau promotional dialog overlaid parts of the visualizations, so full visual UX validation is still pending.

### Changes made during this stage

- Added source-specific public reference and validation boundaries to each repository.
- Added a prominent `START HERE` provenance sheet to both Excel files, preserving the initial chart and formula counts through post-save verification.
- Added warnings to the Power BI dashboard guides about missing on-page disclosure.
- Removed direct promotion of an unlabeled Tableau demonstration from the portfolio homepage.
- Added repeatable CIHI source metadata and workbook inspection checks and headless Tableau browser checks.

### Important remaining release blockers

1. Put **"SIMULATED DATA — DEMONSTRATION ONLY. NOT OFFICIAL CANADIAN HEALTH STATISTICS"** visibly on every Tableau and Power BI report page using their respective publisher/editor tools.
2. Reproduce any statistical findings promoted as real using exact source downloads, documentation, matching reference years/denominators, and independent calculations.
3. Confirm DAX logic, actual chart rendering after the banners are added, tooltip precision, filter behavior, and accessibility in the intended viewing environments.
4. Confirm all officially derived workbook numbers against an identifiable CIHI release and exact worksheet/cell references. The 2025 CIHI Series A file could not be downloaded from the guessed historical direct URL; this is a source-reconciliation blocker, not evidence that the workbook is correct or incorrect.

## Follow-up official NHEX reconciliation and Power BI screenshot review

### CIHI expenditure figures reconciled against a real source file

The original 2000–2023 national expenditure series in the portfolio workbook was compared against CIHI's **official 2026 Series A Excel workbook**, downloaded directly from CIHI and read cell by cell. All **24 years** matched on year and the workbook's 10 category totals reconciled internally to within **$0.05 billion** a year.

Comparing the older portfolio release to the revised 2026 CIHI series gave a mean absolute total-spending difference of about **$0.13 billion**, with the largest difference in 2023: **$360.70 billion (portfolio) versus $362.183 billion (CIHI 2026)**. The 2023 public-health category differed more substantially: **$21.37 billion versus $23.29 billion**, respectively. These are **different release vintages**, not proof that the original entry is a mistake.

Detailed year-by-year CSV and method report:
- https://github.com/Famiyke/health-expenditure-canada/blob/main/reconciliation_nhex_2026_vs_portfolio_2000_2023.csv
- https://github.com/Famiyke/health-expenditure-canada/blob/main/OFFICIAL_NHEX_RECONCILIATION.md

### Mental health Power BI screenshots reviewed

The four screenshots in the mental health project were inspected. The National Snapshot screenshot incorrectly labels synthetic records as **"Source: Statistics Canada CCHS | 5,000 respondents."** A two-part mental-health donut has displayed values **66.8** and **26.4**, totaling **93.2%**, which requires investigation of the missing category and denominator. The Equity Analysis screenshot shows an unqualified modeled **4.6× Indigenous unmet-need ratio**. The provincial scorecard includes **PE with only 23 simulated respondents**, and some province-income cells display **100.00%**, making small-group handling important.

These are dashboard-presentation and measurement issues, **not validated CCHS findings**. Correction instructions:
- https://github.com/Famiyke/mental-health-outcomes-canada/blob/main/DASHBOARD_CORRECTION_GUIDE.md
- https://github.com/Famiyke/chronic-disease-surveillance-canada/blob/main/DASHBOARD_CORRECTION_GUIDE.md

The original PBIX files remain unchanged because editing their internal package or layout outside Power BI Desktop could corrupt them. Their pages still require visible simulation banners, updated source descriptions, and DAX validation in Power BI Desktop.

## Executive outcome

**Status: Partially remediated. Not yet independently validated for release as evidence of actual Canadian health-system findings.**

This audit improved transparency and documentation, executed all six Python demonstration workflows, inspected Power BI report-page structure, checked Excel sheets and formulas, and used headless Chromium to view the published Tableau dashboards. It has **not** fully reconciled project-specific findings against original government data, validated Power BI DAX in Desktop, or completed a multi-device accessibility test.

## Confirmed corrective changes

1. Homepage: Added description and social metadata, keyboard skip link, focus-visible styles, motion preferences and safe external-link attributes.
2. Homepage: Preserved three featured and three additional project links, professional experience, methods, about and contact sections.
3. Six project READMEs: Clear simulated-data disclosures, replacement of unverified headline conclusions, run requirements and limitations of direct government-data substitution.
4. Six Python analytical scripts: Replaced definitive closing policy recommendations with explicit simulation-aware interpretation and validation steps. Numerical calculations still operate on generated datasets.
5. Five project written briefs and the Ontario dashboard guide: Rewritten as clearly identified demonstration documents, not official government findings.
6. Project documentation: Reconciled selected case-sensitive filenames, including `Dashboard.md` and `canada_chronic_disease_burden_monitor.pbix`.
7. Repository inventories: Confirmed each repository contains its documented principal Python scripts and its stated downloadable dashboard/workbook where listed.

## Outstanding issues, ordered by risk

### High — Source evidence and analytical validity

- Individual results have **not** been reconciled against original CIHI, PHAC, Statistics Canada, Ontario Health or Manitoba Health files.
- Some code still produces numerical patterns, rankings and cost scenarios from synthetic records. These are methods demonstrations, not observed public-health outcomes.
- A full clinical and epidemiologic validity audit of code formulas, demographic definitions, comparability, weighting, case mix, indicator conventions and scenario assumptions remains necessary.
- In particular, the simulated CCHS respondent records are not a substitute for weighted survey analysis, and an ecological correlation based on five RHAs cannot establish causality.

### High — Runtime and deliverables

- Clean GitHub Actions smoke tests passed for all six demonstration workflows, but independent numeric reconciliation with official sources has not been performed.
- PBIX structural inspection confirmed four pages in each report. Page-text inspection found no embedded simulated-data disclosure on any page. Both Excel workbooks were opened with openpyxl and gained a prominent provenance tab while retaining charts and formulas. Full Power BI DAX and source-value reconciliation remain outstanding.
- Headless browser screenshots confirm both Tableau Public dashboards render. Neither visible dashboard shows an adequate simulated-data warning; the Ontario report presents named hospital rankings. Direct promotion of the hospital Tableau visualization was removed from the homepage pending publisher-side labeling.
- Notebook/script dependencies and input-schema compatibility require a reproducibility test.

### High — Live deployment discrepancy

- A direct HTTP check through GitHub Actions confirmed the revised homepage is served publicly. The text retrieval tool may show stale content; direct deployment verification passed.
- Cross-device visual inspection in a real browser remains outstanding.

### Medium — Accessibility and web UX

- Code inspection confirms an accessibility skip link, focus styling, and reduced-motion CSS, but no independent screen-reader, keyboard-only or device/browser test was completed.
- Visual previews are examples, not verified research visuals. Add screenshots of actual reviewed dashboards only after checking them.
- Audit colour contrast and the mobile navigation in a live browser.

### Medium — Repository presentation

- Some README descriptions, repository metadata and older project comments may still imply a direct analysis of official data. Review repository About descriptions separately.
- Replace generated-only demo metrics with at least one independently reproduced and properly sourced analysis where feasible.

## Release criteria

The portfolio is ready for an evidence-based recruiter review when:

- [x] A direct HTTP smoke test confirmed the current key sections and removal of stale headline claims on the public deployed page.
- [x] All six Python demonstration workflows execute successfully in clean GitHub Actions environments.
- [ ] The PBIX/XLSX deliverables open and their main charts/figures reconcile with their respective analysis inputs.
- [ ] The Tableau dashboards load and plainly disclose synthetic data.
- [ ] All links work from both desktop and mobile browsers.
- [ ] All headline health statistics refer either to a verified official source with precise citation or to an explicitly illustrative simulation.
- [ ] Quantitative assumptions, denominators, years and uncertainty are documented for any findings promoted as factual.
- [ ] Keyboard and screen-reader checks pass and navigation remains usable on narrow screens.

## Important distinction

The repository and homepage changes described above were committed to GitHub. This audit **does not certify** the underlying clinical analyses, scientific validity, live deployment, or interactive dashboards.
