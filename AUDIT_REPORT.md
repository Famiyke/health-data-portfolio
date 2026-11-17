# Healthcare Analytics Portfolio — Quality Audit

**Audit date:** 16 November 2026  
**Scope:** GitHub Pages homepage and six linked project repositories  
**Audit type:** Static code and documentation inspection, repository file inventory, and limited public-link retrieval.

## Follow-up runtime validation (16–17 November 2026)

GitHub Actions clean-environment smoke tests were added and executed in all six project repositories.

**Result: all six passed** the Python compilation, generated-dataset creation and project analysis sequence using Python 3.11 and pinned interpreter family (package versions are currently unpinned). These runs confirm basic reproducibility of the simulated workflow, **not** scientific accuracy against official datasets.

Additional integrity checks of the archive structure of the Power BI PBIX files and readability of the Excel XLSX workbooks passed in all four applicable repositories. Archive integrity does not confirm correct DAX measures, formulas, dashboard design or numerical reconciliation.

A separate live GitHub Pages deployment check was added to the website repository. Refer to its most recent GitHub Actions run for the deployment verdict. The public retrieval tool continued showing a previously published page during this audit, so browser-level confirmation is still necessary.

**Outstanding:** validate calculations and interpretability against original government sources, open and interact with Power BI/Tableau dashboards, inspect charts and mobile rendering in a browser, and review accessibility with assistive tools.

## Executive outcome

**Status: Partially remediated. Not yet independently validated for release as evidence of actual Canadian health-system findings.**

This audit improved transparency, presentation and documentation. It did not execute the six Python workflows, open binary PBIX/XLSX deliverables, perform browser-based mobile testing, or independently reconcile data with original government releases.

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
- PBIX and XLSX container-integrity tests passed. They were not visually opened, recalculated, or cross-checked against authoritative source data.
- Tableau Public dashboard URLs are included but the dashboard content could not be verified with available public retrieval.
- Notebook/script dependencies and input-schema compatibility require a reproducibility test.

### High — Live deployment discrepancy

- The linked GitHub repository contains the revised homepage, while the public website text retrieval returned an older version with unqualified claims such as “24 Verified Findings.” This may reflect stale retrieval or an actual GitHub Pages publishing issue; the exact cause was not established.
- Verify the deployed page directly in a normal browser, including a hard refresh or private window, and compare to `main/index.html`.

### Medium — Accessibility and web UX

- Code inspection confirms an accessibility skip link, focus styling, and reduced-motion CSS, but no independent screen-reader, keyboard-only or device/browser test was completed.
- Visual previews are examples, not verified research visuals. Add screenshots of actual reviewed dashboards only after checking them.
- Audit colour contrast and the mobile navigation in a live browser.

### Medium — Repository presentation

- Some README descriptions, repository metadata and older project comments may still imply a direct analysis of official data. Review repository About descriptions separately.
- Replace generated-only demo metrics with at least one independently reproduced and properly sourced analysis where feasible.

## Release criteria

The portfolio is ready for an evidence-based recruiter review when:

- [ ] The public deployed page is confirmed to match the latest GitHub `index.html`.
- [x] All six Python demonstration workflows execute successfully in clean GitHub Actions environments.
- [ ] The PBIX/XLSX deliverables open and their main charts/figures reconcile with their respective analysis inputs.
- [ ] The Tableau dashboards load and plainly disclose synthetic data.
- [ ] All links work from both desktop and mobile browsers.
- [ ] All headline health statistics refer either to a verified official source with precise citation or to an explicitly illustrative simulation.
- [ ] Quantitative assumptions, denominators, years and uncertainty are documented for any findings promoted as factual.
- [ ] Keyboard and screen-reader checks pass and navigation remains usable on narrow screens.

## Important distinction

The repository and homepage changes described above were committed to GitHub. This audit **does not certify** the underlying clinical analyses, scientific validity, live deployment, or interactive dashboards.
