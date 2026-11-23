# Business process improvement and reporting automation

The case study is based on the portfolio owner’s December 2025–April 2026 volunteer experience at Opportunities for Employment (OFE), Winnipeg. The duties are supported by the owner’s CV, including frontline intake and attendance collection, record validation, document organization, file hygiene, and support for advisor and reporting workflows. The two experience outcomes were previously reported by the owner and are included as self-reported summaries. OFE’s public website provides organization context only.

## Research question
How can consistent intake procedures, data validation and a structured reporting workflow support reliable program operations?

## Reported outcomes
- Participants supported through intake: 500+. Previously reported by the portfolio owner for OFE volunteer experience; no participant records are published.
- Report preparation time per cycle: Under 40 minutes. Previously reported by the portfolio owner; no pre-change baseline or time log is published.

## Portfolio deliverables
The process map and requirements traceability matrix are generalized portfolio deliverables based on the reported activities. They illustrate possible controls and acceptance criteria. The reporting prototype uses aggregate reporting-cycle counts, validates unique non-personal cycle identifiers, required fields, nonnegative values and reconciliation, and produces a JSON summary with validation rate and mean preparation time. The empty CSV template carries no participant-level data. Test fixtures are artificial and serve only to test the code.

- `process_map.csv`: five workflow stages and suggested controls.
- `requirements_traceability.csv`: five business needs, controls and acceptance criteria.
- `aggregate_cycle_template.csv`: empty, Excel-ready input.
- `data_dictionary.csv`: field definitions and validation rules.
- `reporting.py`: runnable aggregate reporting prototype.
- `test_reporting.py`: artificial unit-test fixtures; not business observations.

## Run the prototype
Open the template in Excel or another spreadsheet application, enter authorized aggregate cycle counts, save as CSV, then execute `python reporting.py aggregate_cycle_template.csv --output summary.json`. The blank template returns No data entered, not a zero-performance report. Run `python -m unittest -v test_reporting.py` to reproduce the checks. Standard Python 3.10+ is sufficient.

## Limitations
The case study uses the portfolio owner’s reported experience and generalizes the workflow to protect privacy. It does not establish a verified before/after improvement percentage. The prototype is a proposed reusable tool, and its tests use clearly designated artificial inputs. OFE’s public website provides organization context only.
