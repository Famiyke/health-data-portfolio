# Canadian federal procurement and supplier analytics

How do disclosed contract award values, purchasing routes and supplier-name concentration vary across selected federal reporting entities?

This project uses disclosed federal contract records to compare original award values, procurement methods and supplier-name concentration across six federal reporting entities and three complete fiscal reporting years.

## Data source and cohort
The analysis uses three complete fiscal reporting years (2023–2024 to 2025–2026) and six selected reporting entities: Public Services and Procurement Canada, Employment and Social Development Canada, Health Canada, Public Health Agency of Canada, Transport Canada and Statistics Canada. Included rows have instrument type C (contract or call-up) and original value above CAD $10,000. The reported original value is converted to integer cents for accurate aggregation. Amendments and standing-offer/supply-arrangement agreement records are excluded. Reporting quarters record public disclosure, not actual payment or delivery.

Source: https://open.canada.ca/data/en/dataset/d8f85d91-7dec-4fd1-8055-483b77225d8b

CSV: https://open.canada.ca/data/dataset/d8f85d91-7dec-4fd1-8055-483b77225d8b/resource/fac950c0-00d5-4ec1-a4d3-9cbebf98a305/download/contracts.csv

Schema: https://open.canada.ca/data/recombinant-published-schema/contracts.json

Retrieved 2026-11-23. SHA-256 6826446cf119d939b24d285329f2bd135b77ed2d57a820b2b0c43e77272387bc.

## Methodology
Supplier names are Unicode-normalized, case-normalized and whitespace-collapsed; no fuzzy matching or corporate ownership assumptions are applied. Five-largest supplier-name share equals the sum of original values of the five leading name groups divided by the included original value. Non-competitive share uses code TN only. ACAN, open, traditional and selective tendering are shown separately. Data are unaudited disclosures and subject to revision.

## Independent validation
The complete source had 1,336,110 records; 41,810 matched the reporting-entity and quarter scope. Exclusions: 14,675 amendments, 57 standing-offer/supply-arrangement agreements and 39 C records at or below $10,000. All 27,039 included records independently matched the source, including 767 chart values. Entity and reference-number combinations are unique. The source contains 29 additional rows sharing procurement IDs, which are retained as distinct disclosure records because the publisher allows procurement IDs to be contract, requisition or commitment numbers. 11 C records carry a nonzero amendment field; only original value is used. SQL totals reconcile to exact integer cents.

## Key findings
- In 2025-2026, the six selected entities disclosed 8,559 included original award records with a total original value of $2,468.07 million.
- Public Services and Procurement Canada had the highest disclosed original value in 2025-2026 among the selected entities ($1,926.33 million).
- The five largest normalized supplier-name groups represented 32.8% of the included original value in 2025-2026. Non-competitive code TN represented 38.2% of disclosure records and 11.1% of original value.

## Reproduce
After extracting the ZIP, run `python run_analysis.py .` to reproduce the SQL outputs from the included records. To refresh from the original CSV, run `python build_procurement.py --raw-dir raw --output-dir rebuilt --download`, then `python validate_procurement.py --raw-dir raw --output-dir rebuilt`. Source data may change; verify the source manifest and document revisions. Standard Python 3.10+ is sufficient.

## Limitations
The analysis is limited to six reporting entities and disclosed original award records above CAD $10,000. The source is unaudited, subject to revision and may vary in reporting practices. Original contract value is a commitment, not actual expenditure. Procurement IDs may repeat across separate disclosure rows. Supplier-name normalization does not establish legal ownership, and concentration or award route alone cannot establish misconduct, compliance or value for money.
