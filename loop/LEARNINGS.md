# loop/LEARNINGS.md — durable gotchas only (max ~60 lines, prune ruthlessly)

## Hard rules (RALPH_LOOP.md section 6, verbatim)

- Decimal (prec 34, ROUND_HALF_EVEN) for everything supply- or
  index-adjacent. Floats never touch published numbers.
- Verification protocol RP Part VI applies to every number: source URL +
  retrieval hash + runnable path + version stamp. A number without an
  interval is a convention and must be labeled as one.
- Published prints are immutable. Corrections are forward-only, via the
  correction ledger. No exceptions, including for your own bugs.
- Network: snapshot-first, then compute offline. Use a User-Agent, backoff
  with jitter, and cache. World Bank's API WAF-blocked us on 2026-08-16
  after a large catalog pull — prefer OWID grapher CSVs, WHO GHO OData, and
  UN WPP files; keep requests few and large rather than many and small.
- No secrets exist in this project and none may be added. All data sources
  are keyless by design.
- Never force-push; never rewrite JOURNAL history; never delete a snapshot.
- If a source contradicts DECISIONS.md or METHODOLOGY numbers, do not
  silently reconcile: journal the discrepancy, mark the task BLOCKED or add
  a correction-ledger entry, and let the dual-series/versioning machinery
  handle it.
- Cite nothing you have not fetched in-iteration. (verify) markers are
  honorable; invented citations are project-ending.

## Standing status

- SPEC.md, METHODOLOGY_v0.md and seed/ (tly_v0_calc.py, results_v0.json,
  CALC_REPORT_v0.txt) are 2026-08-16 reconstructions after loss of the
  originals — pending Ben's ratification (backlog A-16). No public print
  before ratification; treat their numbers as anchors-to-confirm, not truth.

## Verified gotchas (2026-08-16, seed reconstruction)

- WHO GHO OData works keyless: indicator LIFE_0000000035 = "ex - expectation
  of life at age x" (verified against the live indicator list, snapshotted).
  Parse its JSON with parse_float=Decimal so floats never materialize.
- OWID grapher CSVs work keyless; their .metadata.json carries the WPP-2024
  provenance — always snapshot the metadata file alongside the CSV.
- E2 banding: 100+ open band midpoint convention (102.5) is inert — e() is
  flat beyond the last anchor (85), so any midpoint >= 85 yields e(85).
- drift (+1.0394B) and g (+0.7197%/yr) were NOT reproduced by the seed: they
  need the vintage-pair + differencing convention that only the lost
  METHODOLOGY defined; reconstructing it from DECISIONS.md alone would be
  guessing. Backlog B-uc1-12; never tune to hit the target.
- mint gap −0.0026%: unverified hypotheses h1–h3 with their exact checks are
  in CALC_REPORT_v0.txt §4 (backlog B-uc1-11).
- Local test runner: system python3.12 has no pytest; use
  `~/.venvs/main/bin/python -m pytest -q` (verified 2 passed, 2026-08-16).
- Pre-commit config exists but hooks are NOT installed in .git/hooks (A-15).
- pre-commit lives at ~/.local/bin (uv tool install); export PATH first.
  Hook ruff pin must track local ruff (v0.15.0 now) or formatting flip-flops.
- WPP downloads: SPA; the real file index is /wpp/assets/downloads.json.
  Bulk CSVs under /wpp/assets/Excel Files/1_Indicator (Standard)/CSV_FILES/
  (URL-encode spaces). Single-age pop 1950-2023 gz = 62MB, gitignored;
  manifest-only in git. World 2023 = 8,091,734,933 persons = golden N exact.
