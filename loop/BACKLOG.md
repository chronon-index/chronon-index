# loop/BACKLOG.md — ordered atomic tasks

Created at Iteration 0, 2026-08-16 (RALPH_LOOP.md section 4). Governing-doc
context: SPEC.md, METHODOLOGY_v0.md and the seed/ artifacts this backlog
builds on are "Reconstructed 2026-08-16 from DECISIONS.md, RESEARCH_PROGRAM.md
and RALPH_LOOP.md after loss of the original; pending Ben's review" —
ratification is task A-16 and gates the first public print.

Line format (RALPH_LOOP section 2):
`- [ ] <id> | deps: <ids or -> | refs: <doc anchors> | <task>`
`HUMAN:` prefix in the task text = only Ben can do it; the loop never
executes or fakes these. Refs shorthand: SPEC#n = SPEC.md capability n,
AC-n.m = its acceptance criterion, RP#... = RESEARCH_PROGRAM.md part,
RALPH#n = RALPH_LOOP.md section, DEC#n = DECISIONS.md locked point,
METH = METHODOLOGY_v0.md, CALC#n = seed/CALC_REPORT_v0.txt section.
Priority rule: lowest unchecked non-HUMAN task with satisfied deps.

## Phase A — bootstrap

- [x] A-01 | deps: - | refs: RALPH#5, RP#VII | git init + scaffold commit 27e4dac: governing docs, .gitignore, ralph.sh (done in bootstrap 2026-08-16)
- [x] A-02 | deps: A-01 | refs: RALPH#5 | Python 3.12 package skeleton: pyproject.toml (pytest/ruff dev extras) + tly/__init__.py (done in bootstrap 2026-08-16)
- [x] A-03 | deps: A-01 | refs: RALPH#5, RP#VII | CI workflows: ci.yml (lint+tests on push) and print.yml (Mondays 12:00 UTC; placeholder honestly labeled not-official until SPEC#4 lands) (done in bootstrap 2026-08-16)
- [x] A-04 | deps: A-01 | refs: RALPH#5 | .pre-commit-config.yaml with ruff + ruff-format (config only; hooks not installed — see A-15) (done in bootstrap 2026-08-16)
- [x] A-05 | deps: A-01 | refs: RALPH#5 | LICENSE Apache-2.0 for code, CC BY 4.0 for docs stated in README; README with principles (done in bootstrap 2026-08-16)
- [x] A-06 | deps: A-01 | refs: RP#VII, SPEC#3 AC-3.5 | docs/LICENSING.md upstream table, one row per source, all rows (verify), ACLED/EM-DAT marked HUMAN (done in bootstrap 2026-08-16)
- [x] A-07 | deps: A-01 | refs: DEC#7, RP#VI | ledger/CORRECTIONS.md forward-only correction ledger, seeded with C-0001 (napkin g=+2.9%/yr correction) (done in bootstrap 2026-08-16)
- [x] A-08 | deps: A-01 | refs: RALPH#1, DEC, RP | Reconstruct SPEC.md (7 capabilities, AC-n.m verifiers, P1–P10 traceability) with reconstruction header; pending ratification A-16 (done in bootstrap 2026-08-16)
- [x] A-09 | deps: A-08 | refs: RALPH#1, RP#IX, RP#VIII | Reconstruct METHODOLOGY_v0.md (E2 estimator, transport identity §4, neutrality proof §6 — section numbers load-bearing) with reconstruction notice; pending ratification A-16 (done in bootstrap 2026-08-16)
- [x] A-10 | deps: A-09 | refs: RALPH#5, RP#IX-E2, CALC | Reconstruct seed calculator: seed/tly_v0_calc.py + snapshot data/snapshots/2026-08-16/ with manifest.json (sha256/URL/timestamp per file) + seed/results_v0.json + seed/CALC_REPORT_v0.txt + tests/test_golden.py; verifier: pytest 2 passed, offline recompute byte-identical (P5) (done in bootstrap 2026-08-16)
- [x] A-11 | deps: A-10 | refs: RALPH#4, RALPH#2 | Iteration 0: create loop/BACKLOG.md, loop/JOURNAL.md, loop/LEARNINGS.md (this file; iteration 0, 2026-08-16)
- [x] A-12 | deps: A-10 | refs: RALPH#5, CALC#1, SPEC#0 G1 | Port seed parsers + Decimal context into tly/ modules (context prec 34 ROUND_HALF_EVEN; GHO JSON parse_float=Decimal; OWID CSV→Decimal), stdlib only, unit tests on the committed snapshot (done 2026-08-17)
- [x] A-13 | deps: A-12 | refs: RALPH#5, RP#IX-E2 | Port E2 estimator into tly/ as a module; PACKAGE golden test: package output equals seed/results_v0.json to 4 decimal places (the ground-truth anchor every refactor keeps green) (done 2026-08-17)
- [x] A-14 | deps: A-12 | refs: RALPH#5, SPEC#3, RP#VI | Port snapshot fetcher into tly/ module writing data/snapshots/<date>/manifest.json (sha256, source URL, retrieval timestamp, bytes per file); User-Agent, backoff+jitter, few-and-large requests (done 2026-08-17)
- [x] A-15 | deps: A-02 | refs: RALPH#5 | Make lint real locally: install pre-commit hooks into .git/hooks; ruff check + ruff format --check green over the repo (done 2026-08-17)
- [ ] A-16 | deps: A-08, A-09, A-10 | refs: RALPH#0, DEC#9 | HUMAN: review + ratify the reconstructed SPEC.md, METHODOLOGY_v0.md and seed/ artifacts (they replaced lost originals) — gates the first public print (P1) and the golden-anchor commit B-uc1-13
- [ ] A-17 | deps: A-01 | refs: RP#VII | HUMAN: create GitHub org/repo under Praevex, add remote, push; confirm ci.yml runs green in public Actions (until then CI has never actually run)

## Phase B — the index (SPEC capabilities 1–4)

### SPEC#1 — baseline stock engine

- [x] B-uc1-01 | deps: A-13 | refs: SPEC#1 AC-1.3, SPEC#0 G1 | Float quarantine: published-path guard module rejecting float inputs end to end; test_no_float_in_published_path injects a float and asserts rejection (done 2026-08-17)
- [x] B-uc1-02 | deps: A-14 | refs: SPEC#1 AC-1.5, RALPH#6 | Offline-only compute: loader raises on missing/mismatched manifest sha256; no network access during compute; tests for both failure modes (done 2026-08-17)
- [x] B-uc1-03 | deps: A-14 | refs: SPEC#1, RP#II-D1, SPEC#0 G6 | Identify + snapshot a keyless WPP 2024 source for population by single year of age × sex × country (population.un.org/wpp CSV downloads (verify)); manifest rows; few-and-large requests (done 2026-08-17)
- [x] B-uc1-04 | deps: A-14 | refs: SPEC#0 G5, RP#II-D2, RP#VII | Identify + snapshot WPP 2024 life tables (licensed source of record, CC BY 3.0 IGO (verify)) — abridged and single-age availability checked, not assumed; manifest rows (done 2026-08-17)
- [x] B-uc1-05 | deps: B-uc1-03 | refs: SPEC#1 | Parser: WPP single-age population → Decimal structures keyed (age, sex, country); unit tests against snapshot fixtures (done 2026-08-17)
- [x] B-uc1-06 | deps: B-uc1-04 | refs: SPEC#1, SPEC#0 G5 | Parser: WPP life tables → e(x) anchors per (sex, country); WHO GHO path retained as triangulation-only; unit tests (done 2026-08-17)
- [x] B-uc1-07 | deps: A-13 | refs: SPEC#1 AC-1.4, RP#M5 | Versioned interpolation policy: "linear-on-anchors, flat-tail" policy string emitted in output metadata; CI guard fails any policy change without a methodology version bump (done 2026-08-17)
- [x] B-uc1-08 | deps: B-uc1-05, B-uc1-06, B-uc1-07 | refs: SPEC#1, RP#IX-E1, SPEC#0 G4 | E1 stock engine at country × sex × single-age: global + per-country S, E-bar, Decimal end to end, outputs stamped with methodology version + snapshot manifest hashes (done 2026-08-17)
- [x] B-uc1-09 | deps: B-uc1-08 | refs: SPEC#1 AC-1.1, RP#X-P3 | test_p3_reconciliation: sum of per-country dS equals global dS per epoch, exactly, in Decimal (done 2026-08-17)
- [x] B-uc1-10 | deps: B-uc1-08 | refs: SPEC#1, RP#IX-E4, RP#IX-E5 | Decomposition engine: mint B·e(0), spend −N, drift N·dĒ/dt, burn — E4 identity and E5 discrete accounting; fixture tests (done 2026-08-17)
- [x] B-uc1-11 | deps: B-uc1-10 | refs: SPEC#1 AC-1.2, CALC#4 | Close the mint gap (−0.0026%): run the CALC_REPORT h1/h2/h3 checks (UN WPP demographic-indicators births 2023; window/year convention; WHOSIS_000001 e(0)); reproduce mint +9.6606B or journal the honest residual — never tune (done 2026-08-17: h1/h2/h3 ALL REFUTED; residual stands documented)
- [x] B-uc1-12 | deps: B-uc1-10 | refs: SPEC#1 AC-1.2, CALC#4, METH | Drift + g: propose the vintage pair + differencing convention (the definition was lost with the original METHODOLOGY), implement, target drift +1.0394B / g +0.7197%/yr; if no defensible convention reproduces them, mark BLOCKED for Ben — never tune (done 2026-08-17: convention RECOVERED — WHO (2019-2015)/4 at fixed 2023 structure = 1.0394B exact; g chain reproduces; pending A-16 ratification)
- [ ] B-uc1-13 | deps: B-uc1-09, B-uc1-11, B-uc1-12, A-16 | refs: SPEC#1 AC-1.2, RALPH#5 | Golden anchor: regenerate the golden file matching DECISIONS.md key numbers to 4 dp on the v0-equivalent snapshot; commit as the new ground-truth anchor (post-ratification)

### SPEC#2 — weekly mortality nowcast

- [x] B-uc2-01 | deps: A-14 | refs: SPEC#2, SPEC#0 G6, RP#II-D3 | Verify HMD STMF access route + license terms honestly (keyless per G6? registration?); record evidence in docs/LICENSING.md; if registration is unavoidable, journal it and route through HUMAN B-uc2-02 (done 2026-08-17: NOT keyless — 302 to Login; CC BY 4.0 for outputs; routed to B-uc2-02)
- [ ] B-uc2-02 | deps: - | refs: RP#II-D2, RP#II-D3 | HUMAN: register HMD account at mortality.org — CONFIRMED required for STMF too (stmf.csv 302s to Login, 2026-08-17). DECISION for Ben: HMD credentials in the pipeline would violate the no-secrets rule (RALPH#6/G6) — options: (a) World Mortality Dataset (GitHub, keyless) as the automated weekly feed with HMD STMF as manually-refreshed triangulation, or (b) relax G6 for one read-only account via a version gate
- [x] B-uc2-03a | deps: B-uc2-01 | refs: SPEC#2, RP#II-D3, SPEC#0 G6 | World Mortality Dataset (Karlinsky & Kobak, GitHub raw — keyless): verify license honestly, snapshot weekly/monthly deaths CSV, parser → Decimal; manifest rows; unit tests. Serves EITHER B-uc2-02 ruling (as automated feed, or as triangulation) (done 2026-08-17: MIT verified; 34,423 rows/127 countries snapshotted; parser+6 tests; STALENESS observed: data ends 2024-12)
- [ ] B-uc2-03 | deps: B-uc2-01, B-uc2-02 | refs: SPEC#2 | STMF snapshot fetch + parser: weekly deaths by age band, ~38–40 countries → Decimal; manifest rows; unit tests (BLOCKED on HMD account — stmf.csv 302s to Login, verified 2026-08-17)
- [x] B-uc2-04 | deps: B-uc2-03a | refs: SPEC#2, RP#II-D6, RP#X-P7 | Versioned baseline expected-deaths method + per-country coverage metadata (measured vs imputed); tests (works on WMD feed; STMF joins when B-uc2-03 unblocks) (done 2026-08-17: kk-linear policy registered as v0.2.0; coverage P7 records; DEU 2020 excess 24,501.8 pinned)
- [x] B-uc2-05 | deps: B-uc2-04 | refs: SPEC#2 AC-2.6, RP#IX-E4 | Burn term Σ(excess_deaths × e(a)) in Decimal; test_burn_term_e4 on a fixture with known excess deaths and e(a), exact (done 2026-08-17)
- [x] B-uc2-06 | deps: B-uc2-05, B-uc1-08 | refs: SPEC#2, SPEC#0 G2, DEC | Weekly print object: measured-period S, SETTLEMENT label, Monday 12:00 UTC epoch stamp, provenance block; schema (done 2026-08-17)
- [x] B-uc2-07 | deps: B-uc2-06 | refs: SPEC#2 AC-2.2, RP#X-P7 | test_p7_coverage_honesty: a print without the measured-vs-imputed share fails schema validation (done 2026-08-17)
- [x] B-uc2-08 | deps: B-uc2-06, B-uc1-10 | refs: SPEC#2 AC-2.1, RP#X-P6, RP#IX-E5 | test_p6_identity_closure: 52 weekly prints reconcile to the annual E5 identity within the stated versioned tolerance (done 2026-08-17: p6_closure=exact-0 registered as v0.3.0; closure EXACT on 52- and 53-Monday years)
- [x] B-uc2-09 | deps: B-uc2-06, D-03 | refs: SPEC#2 AC-2.4, RP#VIII | Every print embeds the deterministic error-budget accuracy statement (module-produced, never hand-typed); schema check (done 2026-08-17)
- [x] B-uc2-10 | deps: B-uc2-06 | refs: SPEC#2 AC-2.5, DEC | Dual-series plumbing: INFORMATIONAL cohort slot + labels; settlement value never depends on the cohort model; label tests (cohort values arrive with D-04) (done 2026-08-17)
- [ ] B-uc2-11 | deps: B-uc2-03 | refs: SPEC#2 AC-2.3 | Backfill data acquisition: historical STMF (plus World Mortality Dataset if license permits (verify)) snapshots covering ≥ 570 consecutive weeks
- [ ] B-uc2-12 | deps: B-uc2-11, B-uc2-06 | refs: SPEC#2 AC-2.3, RALPH#7 | Backfill engine: ≥ 570 consecutive weekly prints ending at the current epoch
- [ ] B-uc2-13 | deps: B-uc2-12 | refs: SPEC#2 AC-2.3, DEC | COVID-drag gate: drag visible in the backfilled series; cumulative burn inside the recalibrated 120–360M life-years band; report committed

### SPEC#3 — methodology & snapshot governance

- [x] B-uc3-01 | deps: A-14 | refs: SPEC#3 AC-3.3 | Manifest schema validator in CI: every snapshot file needs a row with sha256 + URL + retrieval timestamp; a file without a row fails the build (done 2026-08-17)
- [x] B-uc3-02 | deps: B-uc3-01 | refs: SPEC#3 AC-3.3, RALPH#6 | Snapshot-immutability CI check: snapshots never deleted or modified (diff against committed manifest history) (done 2026-08-17)
- [x] B-uc3-03 | deps: A-13 | refs: SPEC#3 AC-3.1, RP#X-P5, RP#VI | test_p5_reproducibility in CI: run the pipeline twice from identical snapshot hashes, diff byte-identical (done 2026-08-17)
- [x] B-uc3-04 | deps: B-uc1-07 | refs: SPEC#3 AC-3.4, RP#VI, RP#XI | Version-bump guard: registry of methodology-governed params (interpolation policy, baseline method, tolerances, ensemble weights); CI fails any diff without version bump + changelog entry (done 2026-08-17: quanta registered as v0.4.0; registry-completeness + append-only-order tests; ensemble reminder test)
- [x] B-uc3-05 | deps: A-07 | refs: SPEC#3 AC-3.2, RP#X-P10 | Correction-ledger parser + test_p10_correction_completeness: diff vintage pairs against ledger entries; forward-applied only (done 2026-08-17)
- [x] B-uc3-06 | deps: A-06 | refs: SPEC#3 AC-3.5, RP#VII | Clear LICENSING row UN WPP: fetch current license text (CC BY 3.0 IGO (verify)), record URL + retrieval date, set status CLEARED (done 2026-08-17: CLEARED — UN's own statement + CC deed snapshotted)
- [x] B-uc3-07 | deps: A-06 | refs: SPEC#3 AC-3.5 | Clear LICENSING row OWID grapher: fetch current terms (CC BY 4.0 (verify)), record URL + date (done 2026-08-17: CLEARED — CC BY own layer; upstream WPP layer already cleared)
- [x] B-uc3-08 | deps: A-06 | refs: SPEC#3 AC-3.5, RP#VII | Verify + record WHO GHO terms (non-commercial clause (verify)); confirm triangulation-only status in the table (done 2026-08-17: NC confirmed — CC BY-NC-SA 3.0 IGO + data-policy NC clause; triangulation-only locked)
- [x] B-uc3-09 | deps: A-06 | refs: SPEC#3 AC-3.5, RP#VII | Verify + record HMD / STMF redistribution terms; document the derived-indicators-only policy (done 2026-08-17: constructed-vs-input split documented from committed evidence; rows CLEARED-CONSTRUCTED-ONLY)
- [ ] B-uc3-10 | deps: A-06 | refs: SPEC#3 AC-3.5 | Verify + record remaining non-HUMAN rows: Eurostat, CDC, World Mortality Dataset, UCDP, Economist model, IHME GBD, UBS
- [ ] B-uc3-11 | deps: - | refs: SPEC#3 AC-3.5, RP#II-D4 | HUMAN: purchase ACLED commercial license
- [ ] B-uc3-12 | deps: - | refs: SPEC#3 AC-3.5, RP#II-D4 | HUMAN: obtain EM-DAT commercial-use license
- [ ] B-uc3-13 | deps: B-uc3-06, B-uc3-07, B-uc3-08, B-uc3-09, B-uc3-10 | refs: SPEC#3 AC-3.5, RALPH#7 | Licensing-gate CI check (P1 GATE): public print blocked unless every non-HUMAN licensing row is CLEARED
- [x] B-uc3-14 | deps: A-08 | refs: RP#XI, SPEC#0 | Methodology change process doc: proposal → public comment window → version bump with changelog; wired to the version-bump guard (done 2026-08-17)

### SPEC#4 — publication & static API

- [x] B-uc4-01 | deps: B-uc2-06 | refs: SPEC#4 AC-4.6, RP#VI | Print JSON schema: accuracy statement + interval-or-"convention" label mandatory on every published S; schema-validated on publish (done 2026-08-17)
- [x] B-uc4-02 | deps: B-uc4-01 | refs: SPEC#4 AC-4.4 | Static JSON API builder: latest print, per-epoch history, per-country breakdown — committed files only; CI asserts build output contains no server runtime (done 2026-08-17)
- [x] B-uc4-03 | deps: B-uc4-02 | refs: SPEC#4 AC-4.1, RP#X-P9 | test_p9_lineage: walk published JSON, resolve every figure to manifest hashes, non-negativity; no orphan numbers (done 2026-08-17)
- [ ] B-uc4-04 | deps: B-uc4-02, A-17 | refs: SPEC#4 AC-4.2, RP#VII | Wire the real pipeline into print.yml: Monday 12:00 UTC public CI computation, artifacts hashed + committed, placeholder removed; a print produced any other way is invalid
- [x] B-uc4-05 | deps: B-uc4-01 | refs: SPEC#4 AC-4.6, SPEC#2 AC-2.4 | Publish gate: a print failing schema/label/accuracy-statement validation blocks publish; tests (done 2026-08-17)
- [ ] B-uc4-06 | deps: E-02, B-uc4-04 | refs: SPEC#4 AC-4.3, RP#VII | CI verifies a .ots proof exists and matches the print hash before publish
- [ ] B-uc4-07 | deps: E-04, B-uc4-04 | refs: SPEC#4 AC-4.5, RP#XII | Stale-print CI integration: simulate a missing source; status flag flips within the same epoch per the failure ladder
- [x] B-uc4-08 | deps: B-uc4-02 | refs: SPEC#4, DEC#9 | Immutable print storage layout: append-only per-epoch records + hash chain; mutation attempt raises (feeds SPEC#7) (done 2026-08-17)
- [ ] B-uc4-09 | deps: B-uc4-02, E-01 | refs: SPEC#4, RP#XI | Site pages rendered from live artifacts: methodology, data & licenses, changelog, correction ledger, vintage archive
- [x] B-uc4-10 | deps: B-uc4-03, B-uc4-05 | refs: SPEC#4 AC-4.1 | Negative tests: an orphan number, a missing provenance block, and a negative value each fail the lineage/publish checks (done 2026-08-17)

## Phase C — the simulator (SPEC capabilities 5–7)

### SPEC#5 — O(1) gons rebase engine

- [x] C-uc5-01 | deps: A-13 | refs: SPEC#5, RP#IX-E10, RP#M4 | Gons engine core: balance_i = gons_i / F; rebase multiplies the global factor F only; Decimal precision/overflow analysis documented (done 2026-08-17)
- [x] C-uc5-02 | deps: C-uc5-01 | refs: SPEC#5 AC-5.1, RP#IX-E11 | Largest-remainder allocation: floor to quantum, distribute residual quanta by descending fractional part; sum of parts equals total exactly; tests (done 2026-08-17)
- [x] C-uc5-03 | deps: C-uc5-02 | refs: SPEC#5 AC-5.1, RP#X-P1 | test_p1_conservation: Σ balances = M(t) after every operation, exactly (done 2026-08-17)
- [x] C-uc5-04 | deps: C-uc5-01 | refs: SPEC#5 AC-5.2, RP#X-P2 | test_p2_share_invariance: share vector identical across any rebase/F path (done 2026-08-17)
- [x] C-uc5-05 | deps: C-uc5-01 | refs: SPEC#5 AC-5.5, DEC#3 | Transfer log; test_transfer_only_share_change: no transfers → bit-identical shares across any epoch sequence; with transfers → share deltas equal transfer amounts exactly (done 2026-08-17)
- [x] C-uc5-06 | deps: C-uc5-04 | refs: SPEC#5 AC-5.3, RP#IX-E12, DEC#4 | test_e12_neutrality: wealth neutrality (d(value)/d(rebase) = 0) and mortality neutrality (d(s_i)/d(deaths) = 0); mass-death scenario shrinks every balance pro-rata, no share grows (done 2026-08-17)
- [x] C-uc5-07 | deps: C-uc5-01 | refs: SPEC#5 AC-5.6, DEC#2 | Genesis calibration: M = κ·S with κ = 1 token per life-year; display conversion 1 year = 8,766 h; Decimal end to end (done 2026-08-17)
- [x] C-uc5-08 | deps: C-uc5-03, C-uc5-05 | refs: SPEC#5 AC-5.4, RALPH#7 | Perf gate: 10,000 wallets × 600 epochs < 5 s; scaling benchmark asserts rebase cost is O(1) in wallet count (done 2026-08-17: measured 0.003s — 1600x inside the gate)

### SPEC#6 — scenario & backtest lab

- [x] C-uc6-01 | deps: A-13 | refs: SPEC#6 AC-6.4, RP#M5 | Scenario definition format + pinned seeds; test_deterministic_seeds: identical seeds → byte-identical outputs (done 2026-08-17)
- [x] C-uc6-02 | deps: C-uc6-01, B-uc4-08 | refs: SPEC#6 AC-6.5 | test_simulation_isolation: every lab output carries the SIMULATION label; a write attempt to print storage from lab code raises (done 2026-08-17)
- [ ] C-uc6-03 | deps: D-01 | refs: SPEC#6, RP#IX-E7, RP#M2 | Lee-Carter implementation: SVD fit, κ(t) random walk with drift, jump-off bias correction; replicate published parameter estimates for 3 HMD countries — fetch the reference estimates first, never invent them
- [ ] C-uc6-04 | deps: C-uc6-03 | refs: SPEC#6 AC-6.3, RP#IV-P2 | 1990-vintage backtest harness: fit on HMD data through 1990 only, project to 2020, compare to realized, compute bias
- [x] C-uc6-05 | deps: C-uc6-01 | refs: SPEC#6, RP#IX-E8, RP#M3 | Jump-calibration scaffolding for the 1918/WWII/HIV/COVID frequency-severity set; data sources (verify); fixtures honest, no invented calibration values (done 2026-08-17: COVID calibrated from DECISIONS anchors; 1918/WWII/HIV PENDING with (verify) pointers; fitter refuses incomplete sets)
- [x] C-uc6-06 | deps: C-uc6-01 | refs: SPEC#6 AC-6.1, RP#X-P8 | test_p8_interval_coverage: coverage harness validated on synthetic data with known coverage; honesty stated in the docstring; never skipped (done 2026-08-17)
- [ ] C-uc6-07 | deps: C-uc6-02, B-uc2-12 | refs: SPEC#6 AC-6.2, RP#IV-P4 | COVID replay using only real-time-vintage data (no hindsight); error versus final figures computed and documented

### SPEC#7 — settlement fixing module

- [x] C-uc7-01 | deps: B-uc4-08 | refs: SPEC#7 AC-7.6, DEC#9 | Fixing record schema: value, epoch timestamp, methodology version, snapshot manifest hashes, source URLs, DRAFT → FINAL lifecycle; incomplete provenance fails validation (done 2026-08-17)
- [x] C-uc7-02 | deps: C-uc7-01 | refs: SPEC#7 AC-7.1, RP#X-P4, DEC#7 | test_p4_immutability: any mutation of a FINAL print raises; corrections route to the ledger and next epoch only (done 2026-08-17)
- [x] C-uc7-03 | deps: C-uc7-01 | refs: SPEC#7 AC-7.2, DEC#7 | First-print-settles enforcement: the fixing equals the first published print for the epoch, always; a later "better" value never replaces it; test (done 2026-08-17)
- [x] C-uc7-04 | deps: C-uc7-01 | refs: SPEC#7 AC-7.3, DEC | Dispute log: 48 h window, append-only, log-only; a filed dispute alters nothing and delays nothing; test (done 2026-08-17)
- [x] C-uc7-05 | deps: C-uc7-01, B-uc2-10 | refs: SPEC#7 AC-7.4, DEC | Settlement-series discipline: the cohort/INFORMATIONAL series can never be a settlement input; test (done 2026-08-17: closed a REAL gap — settle_from_archive had no label check)
- [x] C-uc7-06 | deps: C-uc7-01 | refs: SPEC#7 AC-7.5 | docs/REPRODUCE_FIXING.md: outsider reproduction instructions, written as if the author will not be there (done 2026-08-17)
- [ ] C-uc7-07 | deps: C-uc7-06, B-uc4-04 | refs: SPEC#7 AC-7.5, RP#IV-P5, RALPH#7 | Outsider-sim CI job: clean environment + public artifacts only reproduces a chosen fixing byte-identically

## Phase D — research artifacts

- [ ] D-01 | deps: B-uc2-02 | refs: RP#II-D2, RALPH#5 | Acquire HMD single-age mortality snapshots for ≥ 3 countries for Lee-Carter, respecting redistribution terms (B-uc3-09: derived indicators only)
- [ ] D-02 | deps: C-uc6-04 | refs: RALPH#5, RALPH#7, RP#IV-P2 | Lee-Carter backtest report committed with its bias stated (the P2 gate artifact, 1990-vintage protocol)
- [x] D-03 | deps: A-13 | refs: RP#VIII, SPEC#2 AC-2.4 | Deterministic error-budget module: symmetric terms in quadrature (~±2% on the v0 level), one-sided terms (vintage lag +2–3%, period-vs-cohort +3–8%) listed never netted; emits the Part VIII accuracy statement; tests (done 2026-08-17: quadrature 1.8708%; computed band 381-402B — DECISIONS prose had rounded to 400)
- [ ] D-04 | deps: C-uc6-03, B-uc2-10 | refs: RP#IX-E6, RP#VIII, DEC | Cohort-S series (E6 over the projected mortality surface) published INFORMATIONAL with intervals alongside the measured-period settlement series
- [x] D-05 | deps: A-13 | refs: RP#IX, SPEC#0 G8 | tly/formulary doc-module: E1–E12 as a tested module; implementations cite equation numbers in docstrings/metadata; cross-reference test (done 2026-08-17)
- [x] D-06 | deps: A-08 | refs: RP#XI, RP#III-R4 | IOSCO mapping table skeleton: one row per Principle mapped to a SPEC capability or governance doc, gaps listed with phase numbers; rows stay (verify) until the 2013 IOSCO document is fetched and read — no recalled principle text (done 2026-08-17: skeleton with ZERO recalled content — iosco.org 403s curl; HUMAN/browser fetch unblock documented in the doc)
- [ ] D-06b | deps: D-06 | refs: RP#III-R4 | HUMAN-or-browser: fetch IOSCOPD415.pdf (site 403s curl), snapshot+manifest it, then fill docs/IOSCO_MAPPING.md rows reading from the PDF only
- [ ] D-07 | deps: A-08 | refs: RP#XI | Whitepaper skeleton: the 7 sections of the Part XI outline, structure and pointers only, no invented content
- [ ] D-08 | deps: - | refs: RP#XI | Glossary: chronon, CHRONON, TLY, saeculum, E-bar, mint/spend/drift/burn, epoch, print, fixing, vintage, measured vs cohort series
- [ ] D-09 | deps: D-08 | refs: RP#XI, RP#V | FAQ + one-pager, including the pre-written "you are pricing human lives" response (VSL/QALY precedent: governments already do, in the open)
- [ ] D-10 | deps: E-01 | refs: RP#XI | Docs site map wired: home / methodology / data & licenses / API reference / changelog / correction ledger / governance / vintage archive
- [ ] D-11 | deps: - | refs: RALPH#5, RP#III | Literature NOTES templates for R1–R7: citation slots + empty summaries marked (verify); never fake summaries of unread papers — fetch and read first or leave empty
- [ ] D-12 | deps: - | refs: RP#III | HUMAN: textbook + paper reading program (R1 Preston/Keyfitz/Wachter/Vaupel; R2 mortality models; R3 longevity markets; R4 IOSCO/BMR/Wheatley; R6 mechanism precedents; R7 Becker 1965)
- [ ] D-13 | deps: - | refs: RP#III-R5, RP#IV-P5 | HUMAN: counsel memos — MiCA classification, SEC/Howey analysis, jurisdiction choice (FINMA Zug / Cayman / UK)
- [ ] D-14 | deps: - | refs: RP#III-R5, DEC | HUMAN: trademark clearance CHRONON in Nice classes 9/36/42 (EUIPO + USPTO), likelihood-of-confusion vs Cronos (CRO) / Chronos (CHR), domain + ticker sweep; reserve name SAECULUM if blocked
- [ ] D-15 | deps: D-13 | refs: RP#XI | Terms of use, disclaimer, privacy statement (no personal data anywhere in the pipeline), conflict-of-interest statement — drafts for counsel review

## Phase E — infrastructure

- [ ] E-01 | deps: B-uc4-02 | refs: RP#VII, RP#XI | Static site generator, files only: renders pages from committed artifacts; local build reproducible byte-for-byte
- [ ] E-02 | deps: A-13 | refs: RP#VII, SPEC#4 AC-4.3 | OpenTimestamps module: stamp print hash → .ots + verify tooling; tests with local fixtures
- [ ] E-03 | deps: B-uc3-02 | refs: RP#VII, RP#V | Vintage archive layout (ALFRED-style): every revision retained and addressable by vintage date; never-delete enforced
- [ ] E-04 | deps: B-uc2-06 | refs: SPEC#4 AC-4.5, RP#XII | Status/stale-print logic: failure ladder source down → carry rule → stale flag → deferred fixing; unit tests simulate each rung
- [ ] E-05 | deps: - | refs: RP#VII | HUMAN: Zenodo account (quarterly snapshot-set deposits, one DOI per vintage)
- [ ] E-06 | deps: B-uc3-02 | refs: RP#VII | Zenodo deposit script: package snapshot set + metadata for DOI deposit; dry-run testable without an account (live deposit needs E-05)
- [ ] E-07 | deps: - | refs: RP#VII | HUMAN: Cloudflare Pages account + custom domain (domain choice ties into the D-14 trademark sweep)
- [ ] E-08 | deps: E-01, E-07 | refs: RP#VII | Deploy static site + JSON API to Cloudflare Pages; publish the URL in README
- [ ] E-09 | deps: - | refs: RP#VII | HUMAN: object-storage account (R2/S3) for raw snapshot sets too large for git
- [ ] E-10 | deps: E-09 | refs: RP#VII | Snapshot object-storage uploader; sha256 manifests stay committed in-repo
- [ ] E-11 | deps: A-17 | refs: RP#XII | Dependency hash-pinning + CI supply-chain hardening (lockfile with hashes)
- [ ] E-12 | deps: A-17 | refs: RP#XII | HUMAN: signing keys (sigstore/cosign), branch protection + signed commits on the org repo
- [ ] E-13 | deps: B-uc3-03 | refs: RP#VII, RP#IV-P5 | One-command Docker image for independent recomputation; byte-identical output documented for outsiders
- [ ] E-14 | deps: E-13 | refs: RP#VII, RP#XII | HUMAN: recruit ≥ 2 external recomputers (university demography group, actuarial society student chapter); N-of-M starts at 3-of-3 matching
