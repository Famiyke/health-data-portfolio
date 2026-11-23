# Business process improvement and reporting automation

The case study is based on the portfolio owner’s December 2025–April 2026 volunteer experience at Opportunities for Employment (OFE), Winnipeg. The duties are supported by the owner’s CV, including frontline intake and attendance collection, record validation, document organization, file hygiene, and support for advisor and reporting workflows. The two experience outcomes were previously reported by the owner and are included as self-reported summaries. OFE’s public website provides organization context only.

## Research question
How can intake and record checks make recurring program reporting more reliable?

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

## Walk through the code

reporting.py reads authorized aggregate cycle counts from the blank CSV template. Each row must have a unique cycle ID, a valid date and nonnegative counts.

The main check is that validated records plus records requiring follow-up equals records received. The script sums the counts and calculates the validation rate and mean preparation time.

test_reporting.py uses artificial test rows to exercise empty input, valid totals and rejected entries. These tests demonstrate the reporting prototype developed for the portfolio.

## Run the prototype
Open the template in Excel or another spreadsheet application, enter authorized aggregate cycle counts, save as CSV, then execute `python reporting.py aggregate_cycle_template.csv --output summary.json`. The blank template returns No data entered, not a zero-performance report. Run `python -m unittest -v test_reporting.py` to reproduce the checks. Standard Python 3.10+ is sufficient.

## Limitations
The workflow is generalized to protect participant privacy. The experience outcomes come from previously reported figures, without a published time log or pre-change baseline. The prototype uses artificial test inputs and illustrates proposed controls. OFE’s website provides organization context.
