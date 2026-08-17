# IOSCO Principles for Financial Benchmarks — mapping table (SKELETON)

Status: **structure only — no principle content yet.** The 2013 IOSCO
document (PD415) could not be fetched this iteration: iosco.org returns
HTTP 403 to non-browser clients (verified 2026-08-17, two user agents).
Per the no-recalled-text rule (RALPH §6), NOTHING from the document is
reproduced here from memory — not principle titles, not even the principle
count. Every row below is created only after the document is fetched and
read.

**Unblock (HUMAN or browser-assisted fetch):** download
`https://www.iosco.org/library/pubdocs/pdf/IOSCOPD415.pdf` in a browser,
save to `data/snapshots/<date>/iosco_pd415_principles_2013.pdf`, add the
manifest row, then fill this table reading from the PDF only.

## How to fill a row (the mapping discipline)

One row per Principle, verbatim-titled from the PDF, mapped to EITHER:
- a SPEC capability (SPEC#1–#7) whose acceptance criteria implement it, or
- a governance doc in this repo (methodology change process, correction
  ledger, dispute log, licensing table, reproduction instructions), or
- a GAP row: what is missing + the phase number (P1–P7) that delivers it.

No row may claim compliance without naming the artifact that evidences it.

## The table

| # | Principle (verbatim from PD415) | Mapped to | Evidence artifact | Gap / phase |
|---|--------------------------------|-----------|-------------------|-------------|
| (rows pending document fetch — see Unblock above) | | | | |

## Candidate mapping inventory (repo side, ready to be mapped)

Prepared so filling the table is a reading exercise, not an archaeology
exercise. These are the artifacts a benchmark administrator would point
at:

- Methodology governance: `docs/METHODOLOGY_CHANGE_PROCESS.md`,
  `docs/METHODOLOGY_CHANGELOG.md`, version-registry guard tests.
- Transparency/reproducibility: `docs/REPRODUCE_FIXING.md`, P5 tests,
  static self-verifying API (`tly/api.py`), print schema with mandatory
  accuracy + coverage blocks.
- Data sufficiency/quality: snapshot manifests + immutability gates,
  licensing table (`docs/LICENSING.md`), P7 coverage honesty.
- Complaints/accountability: dispute log (`tly/disputes.py`, 48h
  log-only), correction ledger (`ledger/CORRECTIONS.md`, forward-only).
- Integrity of determination: fixing records (`tly/fixings.py`,
  provenance-complete, first-print-settles), archive hash chain.
- Known structural gaps to expect: administrator/oversight-function
  separation (entity work, P5 phase per RP Part XI), external audit
  (P5-P6), cessation policy (not yet drafted — will be a gap row).
