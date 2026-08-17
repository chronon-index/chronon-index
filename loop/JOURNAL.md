# loop/JOURNAL.md — append-only iteration journal

One entry per iteration: `## <iso-datetime> | <task-id> | DONE|BLOCKED|PARTIAL`
then 3–6 lines. Never edit or delete old entries. The first four entries
record what the 2026-08-16 bootstrap session actually did, at the real
timestamps, before the loop existed.

## 2026-08-16T18:19:45+02:00 | A-01..A-07 | DONE
- Scaffold commit 27e4dac (15 files, 1163 insertions): governing docs
  (DECISIONS.md, RESEARCH_PROGRAM.md, RALPH_LOOP.md), pyproject + tly/
  skeleton, ci.yml + print.yml (print job honestly labeled not-official until
  SPEC#4), pre-commit config, Apache-2.0 LICENSE + README (docs CC BY 4.0),
  docs/LICENSING.md (all rows (verify); ACLED/EM-DAT HUMAN), ledger/CORRECTIONS.md with C-0001.
- Verifier: files on disk + `git show --stat 27e4dac`.
- The original SPEC.md, METHODOLOGY_v0.md and seed/ artifacts were not
  recoverable from disk anywhere; reconstruction follows in A-08..A-10.

## 2026-08-16T18:25:00+02:00 | A-08 | DONE
- SPEC.md reconstructed from DECISIONS.md + RESEARCH_PROGRAM.md +
  RALPH_LOOP.md; reconstruction note in the header; pending Ben's review (A-16).
- Seven capabilities with AC-n.m acceptance criteria, global conventions
  G1–G8, and the P1–P10 / gates traceability table.
- Verifier: document task — cross-read against the three surviving governing
  docs; lost-anchor figures taken only from DECISIONS.md "Key numbers".

## 2026-08-16T18:28:00+02:00 | A-09 | DONE
- METHODOLOGY_v0.md reconstructed with reconstruction notice; section
  numbering kept load-bearing (RP cites METH §4 transport identity, §6
  wealth-neutrality proof — do not renumber).
- Every number is (a) verbatim from DECISIONS.md/CORRECTIONS.md, (b) a
  Decimal-reverified arithmetic consequence, or (c) marked (verify).
- Pending Ben's ratification (A-16); not ground truth until re-anchored.

## 2026-08-16T18:31:00+02:00 | A-10 | DONE
- Reconstructed seed/tly_v0_calc.py (Python 3.12, stdlib, Decimal prec 34),
  snapshot data/snapshots/2026-08-16/ (6 requests, UA, manifest with sha256 +
  URL + timestamp per file), seed/results_v0.json, seed/CALC_REPORT_v0.txt,
  tests/test_golden.py.
- Verifier: pytest 2 passed; offline recompute run twice, byte-identical (P5).
- Achieved vs target (CALC_REPORT §3): S 362.4126B (2019) / 348.1905B (2021),
  E-bar 44.7880, N 8.0917B, spend −8.0917B all exact at 4 dp; mint 9.6603B vs
  target 9.6606B (−0.0026%, hypotheses h1–h3 recorded unverified); drift
  +1.0394B and g +0.7197%/yr NOT REPRODUCED — need the vintage-pair
  convention lost with the original METHODOLOGY (backlog B-uc1-12).

## 2026-08-16T18:40:00+02:00 | A-11 | DONE
- Iteration 0 (RALPH_LOOP §4): created loop/BACKLOG.md (118 tasks, phases
  A–E, deps + refs per line, 13 HUMAN tasks incl. ratification A-16),
  loop/JOURNAL.md, loop/LEARNINGS.md (§6 hard rules verbatim + gotchas).
- Every [x] in Phase A verified against the filesystem/git this iteration;
  noted: pre-commit hooks NOT installed (A-15 open), tly/ holds only
  __init__.py (port is A-12/A-13), CI has never run (no remote, A-17 HUMAN).
- Verifier: full suite re-run this iteration — 2 passed
  (`~/.venvs/main/bin/python -m pytest -q`).
- Next iteration: A-12 (port seed parsers + Decimal context into tly/) —
  local, no accounts needed.

## 2026-08-17T00:14+02:00 | bootstrap-commit | DONE
- Committed the 2026-08-16 reconstruction bundle (seed+snapshots+golden test;
  SPEC.md; METHODOLOGY_v0.md; loop state). Verifier: suite re-run pre-commit
  this iteration — 2 passed.
- Adversarial consistency review of the reconstructed artifacts (planned
  verify:critic agent) did NOT run — hit the session usage limit 2026-08-16
  18:31 CEST before reading any artifact. No review claims exist. Rescheduled
  as the next iteration's task; A-16 (Ben ratifies reconstructions) still
  gates the first public print regardless.

## 2026-08-17T00:35+02:00 | verify-critic | DONE
- Adversarial consistency review of the reconstructions ran to completion
  (5 findings: 1 high, 1 medium, 3 low). Critic independently re-ran the
  suite: 2 passed; independently recomputed mint from the raw snapshot
  (132,110,264 × 73.123374469 = 9,660,348,305.670449816) confirming the
  committed golden value.
- Fixes applied this iteration: SPEC AC-1.2 amended (golden-anchor conflict:
  now S/Ē/N/spend exact at 4 dp; mint/drift/g reproduce-or-journal per
  B-uc1-11/12; results_v0.json declared THE anchor until B-uc1-13 post-A-16;
  amendment note in-place, flagged for A-16). SPEC dangling refs fixed
  (DECISIONS 13→removed at G5; DECISIONS 11→Key-numbers bullet at AC-5.3;
  grep confirms no DECISIONS n>10 refs remain). METHODOLOGY §1.1 and §5
  "exactly" claims reworded to mutual-consistency-at-4dp. README gained the
  reconstruction/ratification notice.
- CORRECTION to the 2026-08-17T00:14 entry (append-only, not edited): the
  2026-08-16 session limit was hit ~18:41 CEST (per .claude/RESUME.md
  checkpoint 16:41:16Z), not 18:31; and iterations A-08..A-11 were committed
  as one bundle at 2026-08-17T00:12:54+02:00, not per-iteration.
- Verifier: full suite re-run after all edits — see next line for result.
- Suite green after review fixes: 2 passed (2026-08-17T00:35+02:00).

## 2026-08-17T00:45+02:00 | A-12 | DONE
- Ported parsers into the package: tly/numeric.py (Decimal prec-34
  ROUND_HALF_EVEN context, BILLION/Q4 quanta) and tly/parsers.py (GHO ex
  life tables with scope+completeness validation, OWID population bands as
  frozen dataclass with uniform-within-band midpoints, OWID births).
  seed/tly_v0_calc.py untouched (frozen ground truth).
- Verifier: 9 new unit tests cross-check parsed values against
  seed/results_v0.json (e0 anchors, N_persons total, band midpoints/counts
  vs golden band_detail, births) plus error-path tests. Full suite:
  11 passed. ruff check tly/ tests/ seed/: all checks passed.
- Next: A-13 (port E2 estimator; package golden test to 4 dp).

## 2026-08-17T00:52+02:00 | A-13 | DONE
- tly/estimator.py: e_interp (linear-on-anchors, flat-tail — policy string
  versioned per AC-1.4), compute_stock returning frozen StockResult with
  full per-band decomposition, total_population, e_bar, mint.
- Verifier: package golden test at THREE strengths — 4-dp match on
  S/N/Ē/spend/mint (AC-1.2 core), full-precision prec-34 string equality
  vs golden, and per-band term equality vs golden band_detail for both
  years; plus e_interp unit properties. Full suite: 15 passed. ruff clean.
- Next: A-14 (snapshot fetcher module) or A-15 (install pre-commit hooks).

## 2026-08-17T00:58+02:00 | A-14 | DONE
- tly/snapshot.py: fetch_url (User-Agent, exponential backoff + jitter,
  injectable sleep), fetch_snapshot (injectable fetcher — manifest logic
  testable offline; sha256/URL/UTC-timestamp/bytes per file), and
  verify_manifest — the offline integrity gate (SnapshotIntegrityError on
  missing/mismatched files) that AC-1.5 compute paths must call first.
- Verifier: 7 network-free tests — fetch/manifest roundtrip, committed
  2026-08-16 snapshot verifies intact (6 files), tamper + missing-file +
  missing-manifest detection, backoff sequencing (2 sleeps for 3 attempts,
  exponential base). Full suite: 22 passed. ruff clean.
- Next: A-15 (install pre-commit hooks; ruff green already verified).

## 2026-08-17T01:06+02:00 | A-15 | DONE
- pre-commit installed (uv tool; ~/.local/bin — not on default PATH, export
  needed) and hooks installed into .git/hooks. Whole repo formatted; ruff
  check + ruff format --check green.
- Gotcha fixed: hook pin v0.5.7 vs local ruff 0.15.20 flip-flopped
  formatting on tests/test_golden.py — bumped hook rev to v0.15.0 so hook
  and local agree; verified both pass on the same tree.
- seed/tly_v0_calc.py was reformatted (style-only): safe by proof — the
  byte-exact golden recompute test stayed green (output unchanged).
- Verifier: pre-commit run --all-files → both hooks Passed; suite 22 passed.
- Next: A-16/A-17 are HUMAN (ratification; GitHub org). First open non-HUMAN
  task after Phase A per priority rule.

## 2026-08-17T01:14+02:00 | B-uc1-01 | DONE
- tly/guard.py: FloatContaminationError; assert_no_floats (recursive over
  mappings/sequences/sets/dataclasses, path-named errors, fails CLOSED on
  uninspectable objects); assert_decimal (bool/int/str also rejected).
  Wired into estimator entry points: compute_stock guards table+bands,
  e_bar/mint guard scalars.
- Rationale recorded: Python refuses Decimal◦float arithmetic natively, but
  an all-float pipeline never trips that, and Decimal(0.1) launders binary
  error — the guard closes both leaks at the entry boundary.
- Verifier: AC-1.3-named test injects floats at all 6 entry points (all
  raise, with path names); nested/key/opaque cases; real parsed snapshot
  proven float-free. Suite: 27 passed. ruff + format clean.
- Next: B-uc1-02 (offline-only compute wired to verify_manifest).

## 2026-08-17T01:22+02:00 | B-uc1-02 | DONE
- tly/loader.py: load_verified_snapshot — the ONE sanctioned data entry;
  verify_manifest runs BEFORE any parsing; returns frozen VerifiedSnapshot
  (tables, bands, births, manifest).
- Verifier: 6 tests — happy path; hash-mismatch, missing-file,
  missing-manifest all raise SnapshotIntegrityError; corrupted-beyond-
  parsing file fails on INTEGRITY not parse (ordering proof); and the full
  load+compute path runs with socket.socket monkeypatched to raise,
  reproducing S=362.4126/Ē=44.7880 with network physically disabled.
  Suite: 33 passed. ruff clean.
- Next: B-uc1-03 (WPP single-age population source — network task).

## 2026-08-17T01:44+02:00 | B-uc1-03 | DONE
- WPP 2024 single-age population source identified and VERIFIED (not
  assumed): the wpp site is an Angular SPA with no static links; its own
  assets/downloads.json index lists the CSV_FILES bulk paths. Target:
  assets/Excel Files/1_Indicator (Standard)/CSV_FILES/
  WPP2024_PopulationBySingleAgeSex_Medium_1950-2023.csv.gz (de facto 1 July,
  single ages 0..100+, per country and sex, thousands).
- Downloaded (one request, 62,082,217 bytes, 32s), gz-valid, 4,148,070 rows.
  Manifest with sha256 committed; the .gz itself is gitignored (large-file
  policy: object storage HUMAN task pending) — in_git:false recorded.
- TRIANGULATION (RP#VI rule 4): World 2023 PopTotal sums to 8,091,734,933
  persons — equals golden N (OWID/WPP 5-yr bands) EXACTLY, to the person.
  Two independent WPP surfaces agree; recorded in manifest note.
- Verifier: full-file scan + sum above; suite 33 passed (manifest-format
  compatibility with tly.snapshot preserved).
- Next: B-uc1-04 (WPP life tables — paths already sighted in the same
  index: WPP2024_Life_Table_{Abridged,Complete}_Medium_*_1950-2023.csv.gz).

## 2026-08-17T02:00+02:00 | B-uc1-04 | DONE
- WPP 2024 life tables snapshotted from the verified CSV_FILES base:
  Abridged Medium 1950-2023 (144.5MB, 2,710,620 rows, 22 age groups,
  Sex∈{Total,Male,Female}) and Complete Medium Both 1950-2023 (200.0MB,
  4,148,070 rows, 101 single ages, Sex=Total). Availability CHECKED for
  both forms, as the task demanded. Full life-table columns incl. mx..ex,ax
  (everything RP#I M1 needs). Manifests with sha256 committed; .gz files
  gitignored (in_git:false).
- DISCREPANCY RECORDED, not reconciled (RP#VI rule 4): WPP world e0
  2019=72.6093 / 2021=70.865 vs WHO GHO 73.123374469 / 71.368699065
  (~0.5yr, ~0.7%). Different estimators. The G5 switch to WPP as licensed
  source of record will be a documented level change via versioning.
- License status: WPP CC BY 3.0 IGO remains (verify) in docs/LICENSING.md —
  clearing it needs the terms page read + recorded (separate gate task).
- Verifier: gz-valid full scans with row counts + column checks + world e0
  extraction above; suite 33 passed.
- Next: B-uc1-05 per backlog.

## 2026-08-17T02:14+02:00 | B-uc1-05 | DONE
- Committed fixture extracted from the 62MB source (World/Japan/Nigeria ×
  2019+2023, 606 rows, 11.4KB, deterministic gzip mtime=0) with provenance
  row in manifest (derived_from + parent sha256). .gitignore exception for
  fixtures/*.gz added.
- tly/wpp.py: parse_population_single_age streams the gz → PopulationCell
  (loc_id/iso3/location/year/sex/age/persons); thousands→persons ×1000 in
  Decimal (exact); population_by_age enforces the complete 0..100 age set.
- Verifier: 6 tests — cell counts, ISO3 handling (World has none, JPN
  does), World-2023 fixture sum == golden N to the person, completeness +
  strict-miss errors, M+F≈Total within file rounding (≤1.5 persons/age),
  and a skipif full-file regression (ran locally: passed). Suite: 39 passed.
  ruff clean.
- Next: B-uc1-06 (WPP life-table parser; WHO GHO becomes triangulation-only).

## 2026-08-17T02:28+02:00 | B-uc1-06 | DONE
- Life-table fixtures extracted with provenance (abridged 594 rows/31.9KB;
  complete 909 rows/44.2KB; deterministic gzip; manifest rows with parent
  sha256). tly/wpp.py gained parse_life_table_ex + ex_anchors accepting
  EXACTLY the 22-anchor abridged or 101-anchor complete age set (partial
  tables rejected).
- Cross-granularity check: abridged and complete e(x) agree EXACTLY at all
  22 shared anchors (World 2023) — one underlying WPP table, two surfaces.
- RP#VI rule 4 as a TEST: test_wpp_who_discrepancy_is_preserved_not_averaged
  pins WPP e0(2019)=72.6093 ≠ WHO 73.123374469; silently "fixing" either
  source now fails the suite. WHO GHO path retained, triangulation-only.
- Verifier: 6 new tests; suite 45 passed; ruff + format clean.
- Next: B-uc1-07 per backlog.

## 2026-08-17T02:40+02:00 | B-uc1-07 | DONE
- tly/methodology.py: METHODOLOGY_VERSION=v0.1.0-reconstruction; three
  policy strings (interpolation, band_midpoint, decimal); append-only
  VERSION_POLICY_REGISTRY pinning version→policies; output_metadata() stamp
  for every published artifact. docs/METHODOLOGY_CHANGELOG.md started.
  estimator.INTERPOLATION_POLICY now re-exported from the canonical home.
- The AC-1.4 guard is a TEST PAIR: live policies must equal the registry
  pin for the current version (policy edit without bump → fail), and the
  v0.1.0 entry is byte-pinned (editing history → fail). Changelog must
  mention the current version (also tested).
- Verifier: 5 new tests; suite 50 passed; ruff clean.
- Next: B-uc1-08 (E1 stock engine, country × sex × single-age).

## 2026-08-17T02:56+02:00 | B-uc1-08 | DONE
- tly/stock.py: E1 engine. compute_location_stock does Σ N(a)·e(a+0.5)
  under the registered midpoint+interpolation policies (same policy strings
  at every resolution — no bump needed); LocationStock (frozen) with
  e_bar/s_billions_4dp; build_report + stamp() emitting methodology version
  + policies + per-file sha256 of every input snapshot (manifests
  re-verified at stamp time).
- verify_manifest gained require_all: files the manifest itself declares
  in_git:false may be ABSENT (fresh-clone/CI reality) but must match their
  hash when present; committed files must always exist. Stamp uses
  require_all=False; the AC-1.5 loader keeps the strict default.
- Computed & pinned (fixtures, WPP single-age tables): World 2023
  S=363.5117B Ē=44.9238; Japan 4.8031B/38.6189 (aged), male-via-abridged
  2.2660B/37.3313; Nigeria 9.6041B/42.1448 (young); World 2019 354.4515B.
  v0 WHO-based 362.4126B stands alongside — sources recorded apart, tested
  apart (test_world_2019_wpp_vs_v0_who_recorded_apart).
- Verifier: 7 new tests incl. stamp content + float rejection + mixed
  year/sex rejection; suite 57 passed; ruff clean.
- Next: B-uc1-09 (test_p3_reconciliation — needs all-countries run from the
  full 62MB+200MB snapshots; design note: World-direct vs Σ countries).

## 2026-08-17T03:12+02:00 | B-uc1-09 | DONE
- Parsers gained loc_types filter (LocTypeName; 'Country/Area' selects the
  237-country universe). tly/stock.py gained aggregate_stocks (exact
  Decimal sum; rejects mixed year/sex) and reconcile_delta (Σ per-location
  dS vs global dS; rejects location-universe mismatch — a country entering/
  leaving is an explicit data event, never silently netted).
- test_p3_reconciliation green on the fixture universe AND at full scale:
  all 237 Country/Area locations, 2022→2023, from the full 62MB+200MB
  snapshots — per-location dS == global dS EXACTLY (44.7s run, skipif when
  snapshots absent).
- DATA measurement (separate from the engine invariant): WPP published
  World 2023 = 8,091,734,933 persons vs Σ 237 countries = 8,091,736,565 —
  gap 1,632 persons (~0.00002%), within the ±0.5-person/cell rounding
  bound; asserted < 100k in the skipif test, recorded here exactly.
- Verifier: 4 new tests; suite 61 passed (60 fast + full-universe ran
  once); ruff clean.
- Next: B-uc1-10 per backlog.

## 2026-08-17T03:30+02:00 | B-uc1-10 | DONE
- tly/decomposition.py: two strictly-separated views. (1) exact_
  decomposition: ΔS = Ē·ΔN + N·ΔĒ + ΔN·ΔĒ — algebraically exact; honest
  note that prec-34 Ē division leaves ULP closure (~1e-23 observed on
  world-scale; bounded <1e-15 life-years in tests; literally 0 on
  division-free synthetic inputs). (2) identity_decomposition: E4/E5 form
  mint B·e(0) + spend −N + drift N·ΔĒ − burn, with residual EXPOSED as a
  property — burn shifts the residual, never ΔS (tested).
- Fixture pins (World 2019→2023, WPP tables): dS +9.0602B = pop +12.7255B
  + revision −3.5383B (COVID-era Ē dip) + cross −0.1270B. Japan: negative
  through BOTH terms (shrinking + Ē dip) — a real down-rebase-shaped case.
- Verifier: 6 new tests (synthetic exact-zero closure, pinned fixtures,
  residual exposure, burn semantics, float/mixed-location rejection);
  suite 66 passed; ruff clean.
- Next: B-uc1-11 (mint-gap h1/h2/h3 checks — network task).

## 2026-08-17T03:52+02:00 | B-uc1-11 | DONE (residual stands)
- All three CALC_REPORT §4 hypotheses RUN against live sources and REFUTED:
  h1 — WPP DemInd World births 2023 = 132,110,264, IDENTICAL to OWID (the
  mirror is faithful); h2 — 2022/2024 births move mint AWAY from target
  (9.6870/9.6820); h3 — WHOSIS e0 2019 = 73.123374470 vs ex 73.123374469
  (last-digit rounding; no 4-dp effect).
- Conclusion journaled: 9.6603B is THE reproducible mint; 9.6606B (implied
  +3,442 births or +0.0026yr e0) is unreproducible from any tested source
  pair — provenance lost with the original. Residual documented per
  amended AC-1.2; nothing tuned. Forward-only addendum §7 appended to
  seed/CALC_REPORT_v0.txt; evidence snapshots manifested (DemInd 16.6MB
  in_git:false; WHOSIS 13KB committed; World-rows fixture committed).
- Verifier: 4 pinning tests (mirror fidelity, year conventions, WHOSIS
  equivalence, residual arithmetic); suite 70 passed; ruff clean.
- Next: B-uc1-12 (drift/g vintage-pair convention — the harder lost piece).

## 2026-08-17T04:15+02:00 | B-uc1-12 | DONE (convention recovered)
- Exhaustive search across 18 candidate conventions: 8 e0-proxies (miss,
  1.13-4.29B), 5 WPP-table fixed-structure (miss, 0.06-8.16B; also
  anachronistic — WPP tables not in v0 snapshot), 5 WHO-vintage fixed-
  structure (GHE 2000/2010/2015/2019/2021 — v0's only table family).
- RECOVERED: drift = [S(pop2023, WHO2019) − S(pop2023, WHO2015)]/4 =
  (362.4126 − 358.2550)/4 = 1.0394B EXACT at 4dp. Reading: annualized
  pre-COVID WHO-vintage revision gain at fixed structure — exactly what an
  organic-drift term should be (COVID routes through burn, not drift).
- g chain: with DECISIONS mint 9.6606 → g = 0.7197 (RECORDED g REPRODUCES);
  with reproducible mint 9.6603 → 0.7196 (mint residual propagates, both
  stated). WHO 2015 S = 358.2550B pinned.
- Honesty: recovered-by-search ≠ proven-original; flagged for A-16. Rivals
  pinned as non-matches (test_rejected_conventions_stay_rejected) so the
  convention can't be quietly swapped. Evidence json committed+manifested;
  CALC_REPORT addendum §8.
- Verifier: 4 tests recomputing the full chain from committed snapshots;
  suite 74 passed; ruff clean.
- Next: B-uc1-13 blocked on A-16 (HUMAN); move to B-uc2 (nowcast) chain.

## 2026-08-17T04:35+02:00 | B-uc2-01 | DONE (access not keyless — routed to HUMAN)
- STMF access VERIFIED by live probe: /File/GetDocument/Public/STMF/Outputs/
  stmf.csv responds 302 → /Account/Login; free registration required. The
  pre-2022 keyless route is gone. G6 (keyless) cannot be satisfied by HMD
  STMF directly.
- License VERIFIED (better than assumed): HMD User Agreement states
  HMD-constructed data — which includes STMF outputs — are CC BY 4.0;
  input data excluded. Old "redistribution restricted" row corrected in
  docs/LICENSING.md with evidence pointer (snapshot committed+manifested).
- Routed per task instruction: B-uc2-02 (HUMAN) updated with the decision
  Ben must make — HMD credentials would violate the no-secrets rule;
  options framed: (a) World Mortality Dataset (GitHub, keyless) as the
  automated feed + STMF as manually-refreshed triangulation, or (b) a
  version-gated G6 relaxation for one read-only account.
- Verifier: probe outputs quoted above; suite unchanged (74 passed prior);
  no code touched.
- Next: B-uc2-03 depends on B-uc2-01 only for the route — but the route is
  HUMAN-gated; WMD (keyless) exploration can proceed as the next task if
  backlog ordering allows, else first open non-HUMAN task.

## 2026-08-17T04:48+02:00 | backlog-split(B-uc2-03) | DONE
- Per RALPH §3.4 the split IS this iteration's work. B-uc2-03 (STMF fetch)
  cannot execute keylessly (verified 302→Login); re-depped on HUMAN
  B-uc2-02 and annotated BLOCKED. Inserted B-uc2-03a: World Mortality
  Dataset via GitHub raw (keyless) — license verification + snapshot +
  parser. WMD serves EITHER outcome of Ben's B-uc2-02 ruling: as the
  automated feed (option a) or as triangulation beside STMF (option b).
  B-uc2-04 re-depped onto B-uc2-03a so the nowcast chain isn't
  human-gated.
- Verifier: backlog re-read; deps re-validated by inspection (no dangling
  IDs introduced; B-uc2-03a deps satisfied).
- Next: B-uc2-03a.

## 2026-08-17T05:05+02:00 | B-uc2-03a | DONE
- WMD verified + snapshotted keylessly from GitHub raw: LICENSE = MIT
  (evidence committed; LICENSING.md row VERIFIED), world_mortality.csv
  1.1MB / 34,423 rows / 127 countries / weekly+monthly, committed +
  manifested. tly/wmd.py: strict parser (unknown unit / out-of-range
  period → raise), country_series (single-unit enforced), coverage() — the
  staleness map P7 will publish per print.
- HONEST LIMITATION observed and pinned: the dataset's edge is 2024-12
  (92/127 countries through 2024) — 20 months stale for a 2026 nowcast.
  No explanation invented; whether fresher data exists elsewhere is
  (verify) in the manifest. This materially weakens option (a) of the
  B-uc2-02 decision and belongs in front of Ben.
- Verifier: 6 tests (shape, pinned first/latest rows, sorted single-unit
  series, filter errors, malformed-period rejection); suite 80 passed;
  ruff clean.
- Next: B-uc2-04 (baseline expected-deaths method on the WMD feed).

## 2026-08-17T05:28+02:00 | B-uc2-04 | DONE
- tly/baseline.py: Karlinsky-Kobak per-period linear baseline (fit
  2015-2019, closed-form least squares in Decimal), excess_series
  (observed − expected), CoverageRecord (P7: measured vs imputed periods
  per country-year, measured_share). Incomplete fit windows (e.g. week 53)
  are EXCLUDED not silently fit — they surface as imputed.
- METHODOLOGY BUMP EXERCISED FOR REAL: baseline is a new policy →
  v0.2.0-reconstruction appended to the registry + changelog entry; the
  guard tests fired exactly as designed (2 stamp-shape tests failed until
  consciously updated). The bump machinery works.
- Real-feed fact: DEU 2020 excess (weekly, kk-linear) = 24,501.8 — pinned
  exactly (deterministic from committed snapshot); lower than headline
  estimates because the linear trend absorbs aging-driven increase and the
  Dec-2020 wave books into 2021. My initial >30k threshold was a wrong
  guess, corrected to the computed pin — the data was never touched.
- Verifier: 6 new tests (exact linear recovery, exact excess, incomplete-
  window exclusion, coverage math, policy versioning, real-DEU pin); suite
  86 passed; ruff clean.
- Next: B-uc2-05 (burn term Σ excess×e(a) — E4, exact fixture test).

## 2026-08-17T05:52+02:00 | B-uc2-05 | DONE
- tly/burn.py: burn_life_years = Σ excess(a)·e(a+0.5) under the SAME
  registered midpoint+interpolation policies as the stock engine (one
  policy set, both flow directions); signed (deficit → negative burn).
  Plus allocate_largest_remainder (RP#IX E11) — exact-conservation
  age attribution; weights must sum to exactly 1; total must be a
  quantum multiple; deterministic tie-break. distribute_excess wraps it
  for shock feeds (per-feed weight profiles are later versioned tasks).
- test_burn_term_e4 (the named AC-2.6 verifier) exact:
  100·e(0.5)+50·e(5.5) = 10256.25 on a division-free table. My first
  expected constant was a hand-addition slip (9256.25) — the code was
  right; test corrected, journaled per honesty rule.
- E11 conservation tested incl. a case where naive rounding loses a
  quantum; end-to-end DEU-scale excess → 70/30 old-age split → WHO-table
  burn, conservation + determinism asserted.
- Verifier: 7 tests; suite 93 passed; ruff+format clean.
- Next: first open task in the backlog (uc2 chain continues).

## 2026-08-17T06:05+02:00 | B-uc2-06 | DONE
- tly/prints.py: WeeklyPrint (frozen — a constructed print is FINAL, P4);
  epoch discipline enforced at construction AND at consumer-side schema
  validation (Monday 12:00:00 UTC exactly, explicit UTC only); series
  labels SETTLEMENT|INFORMATIONAL (DECISIONS dual-series); Decimal-only
  numeric fields; deterministic render (sorted keys, Decimal-as-string —
  P5). validate_print_dict is the consumer/recomputer gate; it already
  REQUIRES coverage.measured_share (P7) and provenance with
  methodology_version + snapshots — B-uc2-07's named test comes next.
- Verifier: 8 tests (roundtrip+schema, 5 bad epochs, label/type
  discipline, FrozenInstanceError on mutation, byte-identical renders,
  missing-coverage + missing-provenance schema failures); suite 100
  passed; ruff+format clean.
- Next: B-uc2-07 (test_p7_coverage_honesty — the named invariant test).

## 2026-08-17T06:18+02:00 | B-uc2-07 | DONE
- coverage_block() added to tly/baseline.py: aggregates CoverageRecords
  into the print's P7 block (plain measured/total aggregate — population
  weighting would be a versioned upgrade; per-country shares + period
  universes carried for full honesty; deterministic country ordering).
- test_p7_coverage_honesty (named per RP#X) green on REAL data: DEU+ALB
  2021 coverage from the WMD feed → honest print passes schema; stripping
  measured_share fails with the exact P7 message; stripping the whole
  coverage block fails required-fields. Real-value checks: ALB monthly
  2021 fully measured (share 1), DEU weekly >0.9.
- Verifier: 3 tests; suite 103 passed; ruff+format clean.
- Next: B-uc2-08 (test_p6_identity_closure — 52 weekly prints vs annual E5).

## 2026-08-17T06:40+02:00 | B-uc2-08 | DONE
- tly/weekly.py: monday_epochs (the year's ACTUAL Mondays — 52 or 53,
  never pretended), allocate_equal (E11 equal-weight case, signed,
  micro-life-year quantum, exact conservation), schedule_annual_flow.
- Methodology v0.3.0: p6_closure policy = "exact-0" registered + changelog;
  the stated tolerance is ZERO — stronger than "within tolerance"; any
  future nonzero tolerance (mixed-source weekly burn) needs a bump. Stamp-
  shape tests updated consciously (the guard fired again, as designed).
- test_p6_identity_closure (named per RP#X) green: real World 2019→2023 dS
  (fixture-computed, long fractional tail) scheduled across 2026 (52
  Mondays) and 2024 (53 Mondays); Σ weekly == annual EXACTLY; every epoch
  stamp passes validate_epoch.
- Verifier: 4 tests; suite 107 passed; ruff+format clean.
- Next: first open task in backlog (uc2 chain tail / uc3).

## 2026-08-17T06:55+02:00 | B-uc2-10 | DONE
- DualSeries added to tly/prints.py: settlement slot REQUIRES a
  SETTLEMENT-labeled print and is the sole source of settlement_value (no
  code path from the cohort model to that number — structural, not
  conventional); informational slot optional (absent pre-P2/D-04), must be
  INFORMATIONAL-labeled and share the epoch; both prints frozen;
  deterministic render.
- Verifier: 5 tests — settlement reads settlement-only even when the
  cohort print carries a different (higher) S; optional slot; label
  discipline in both slots; epoch-mismatch rejection; deterministic
  render. Suite 112 passed; ruff+format clean.
- Next: B-uc2-09 needs D-03 (error budget); B-uc2-11/12 need STMF (HUMAN).
  Next open executable is in the uc3 chain or D-03 — follow priority rule.

## 2026-08-17T07:10+02:00 | B-uc3-01 | DONE
- tly/manifest_schema.py: bidirectional validator — disk→manifest (orphan
  files fail) and manifest→fields (sha256+bytes always; provenance either
  fetched [source_url+retrieved_utc] or derived [derived_from+parent-sha
  cross-checked+derivation]; present files hash- and size-verified; absent
  files must be marked in_git:false). Returns ALL violations, not first.
- test_real_snapshots_fully_manifested IS the CI gate (pytest runs in CI)
  and passed on first run over both committed snapshot dirs — the
  manifest discipline from A-14 onward held with zero retrofits.
- Verifier: 6 tests (real-tree gate + 5 synthetic failure modes incl.
  parent-hash cross-check); suite 118 passed; ruff clean.
- Next: B-uc3-02 (snapshot immutability vs manifest history).

## 2026-08-17T07:22+02:00 | B-uc3-02 | DONE
- tests/test_snapshot_immutability.py: three history gates against git
  itself — (1) no tracked snapshot file (manifests excepted) ever appears
  as Modified/Deleted in any commit; (2) manifests are append-only
  ledgers: across every consecutive committed version pair, each
  (file, sha256) row survives unchanged (additions fine, rewrites fail);
  (3) the WORKTREE may only extend HEAD's manifests — a rewrite is caught
  before it can even be committed.
- All three passed against the real 29-commit history on first run: no
  snapshot has ever been modified or deleted, and every manifest evolution
  was purely additive.
- Verifier: 3 tests; suite 121 passed; ruff clean.
- Next: continue uc3 chain per backlog.

## 2026-08-17T07:38+02:00 | B-uc3-03 | DONE
- tly/pipeline.py: the end-to-end unit of reproducibility — committed
  snapshots → verified load → E1 stock → real WMD coverage block → stamped
  WeeklyPrint; `python -m tly.pipeline <epoch>` renders to stdout for
  cross-process diffing.
- test_p5_reproducibility (named per RP#X): two in-process builds render
  byte-identically and pass the print schema; PLUS two cold OS processes
  with PYTHONHASHSEED=0 vs 42 produce byte-identical stdout — hash
  randomization, import order, and hidden nondeterminism all covered.
- Verifier: 2 tests; suite 123 passed; ruff clean.
- Next: B-uc3-04 (version-bump guard is largely built at B-uc1-07 —
  verify what remains: tolerances/ensemble-weights registry coverage).

## 2026-08-17T07:55+02:00 | B-uc3-04 | DONE
- Guard completed beyond B-uc1-07: the two quanta (scheduling 1e-6,
  attribution 0.001) were governed constants living only in code —
  registered as the v0.4.0 "quanta" policy (registry + changelog + stamp
  tests updated; the guard fired on the shape tests again as designed).
- tests/test_version_bump_guard.py: governed code constants (FIT_YEARS,
  LIFE_YEAR_QUANTUM, distribute_excess quantum default via signature
  inspection, Decimal PRECISION) must appear in current policy strings;
  every registry version must be in the changelog; registry keys ascending
  with current == newest; policy keys only ever GROW across versions; and
  an executable reminder that ensemble weights (RP#V Q1) MUST enter the
  registry when the P2 ensemble lands.
- Verifier: 5 tests; suite 128 passed; ruff+format clean.
- Next: B-uc3-05 (correction-ledger parser + test_p10).

## 2026-08-17T08:12+02:00 | B-uc3-05 | DONE
- tly/corrections.py: ledger parser (strictly increasing C-NNNN IDs,
  non-decreasing dates, fenced-code-aware — the ledger documents its own
  format in a code block, which the first parser version choked on) and
  find_restatements: ANY changed or dropped historical epoch between
  vintages is a violation, ledger entry or not — a correction licenses the
  forward fold, never the rewrite (DECISIONS #7 as code).
- test_p10_correction_completeness (named per RP#X): real ledger parses
  (C-0001 napkin correction present); entry blocks byte-identical across
  every committed version AND into the worktree (append-only enforced
  against git, same pattern as manifests); restatement checker exercised
  on forward-fold/restate/drop cases; parser rejection tests.
- Verifier: 3 tests; suite 131 passed; ruff+format clean.
- Next: B-uc3-06 (clear the UN WPP LICENSING row — network task).

## 2026-08-17T08:32+02:00 | B-uc3-06 | DONE
- UN WPP LICENSING row CLEARED — the first row to reach CLEARED status.
  Evidence chain, both files snapshotted + manifested: (1) the UN's own
  downloads index (wpp_downloads_index.json) states verbatim "Copyright ©
  2024 by United Nations, made available under a Creative Commons license
  CC BY 3.0 IGO"; (2) the CC BY 3.0 IGO deed confirms share/adapt "for any
  purpose, even commercially", irrevocable, attribution required. Note:
  /wpp/copyright 404s — the license statement lives in the index the site
  itself serves, which is stronger evidence anyway (it governs the exact
  files we fetched).
- Commercial condition: attribution + UN suggested citation form —
  recorded in the row.
- Verifier: manifest-schema + immutability gates re-run green (9 passed)
  over the extended manifest; the licensing row carries evidence pointers.
- Next: B-uc3-07 (OWID row).

## 2026-08-17T08:48+02:00 | B-uc3-07 | DONE
- OWID LICENSING row CLEARED (second row). Evidence snapshotted+manifested
  (owid_about.html): "Our charts, articles, and data are licensed under
  CC BY, unless stated otherwise"; third-party data subject to upstream
  licenses. The layer analysis matters: our WPP-via-OWID series is
  third-party data, so the GOVERNING license is the UN's CC BY 3.0 IGO
  (cleared B-uc3-06) with OWID's processing layer CC BY on top — both
  permissive, chain clean. Attribution: cite both (citation strings are in
  the committed grapher metadata).
- Note: the row previously assumed "CC BY 4.0"; the about page says
  "CC BY" without pinning a version on the data statement — recorded as
  stated, not embellished.
- Verifier: manifest+immutability gates green (9 passed).
- Next: B-uc3-08 (WHO GHO terms — the non-commercial clause check).

## 2026-08-17T09:02+02:00 | B-uc3-08 | DONE
- WHO GHO terms VERIFIED, both pages snapshotted+manifested: publications
  CC BY-NC-SA 3.0 IGO (copyright page); data policy grants access "on
  terms that allow non-commercial, not-for-profit use of the Data for
  public health purposes". The non-commercial clause the architecture
  assumed is REAL — WHO cannot feed a commercial index; the G5 decision
  (WPP source of record, WHO triangulation-only) is now evidence-backed
  from both directions (WPP cleared permissive; WHO confirmed restricted).
- Row status: VERIFIED-RESTRICTED (a row can be honestly settled without
  being cleared FOR commercial use — the table now distinguishes these).
  v0 research use remains compatible.
- IMPLICATION recorded for A-16/B-uc1-13: the v0 golden anchor is computed
  from a WHO table — fine as research/reconstruction ground truth, but the
  COMMERCIAL settlement series must move to WPP tables (the G5 switch,
  with its documented ~0.5yr e0 level change) before any commercial print.
- Verifier: manifest+immutability gates green (9 passed).
- Next: B-uc3-09 (HMD/STMF redistribution terms — partially done at
  B-uc2-01; formalize the derived-indicators policy in the table).

## 2026-08-17T09:15+02:00 | B-uc3-09 | DONE
- HMD/STMF redistribution policy formalized from the ALREADY-COMMITTED
  evidence (hmd_user_agreement.html — no refetch needed): constructed data
  (exposure-to-risk, death rates, life tables, STMF outputs) = CC BY 4.0
  redistributable with attribution + specified citation + download-date
  note (manifest retrieved_utc satisfies the date requirement by design);
  INPUT data "remain under each provider's distribution license" — never
  redistribute inputs (STMFinput.zip explicitly out of scope).
- The old "derived indicators only" assumption was REFINED, not confirmed:
  the restriction binds inputs, not outputs — outputs are fully
  redistributable. Rows set CLEARED-CONSTRUCTED-ONLY; a status vocabulary
  section added to LICENSING.md ((verify) / VERIFIED-RESTRICTED /
  CLEARED-CONSTRUCTED-ONLY / CLEARED / HUMAN).
- LICENSING table state: WPP CLEARED, OWID CLEARED, WHO VERIFIED-
  RESTRICTED, HMD+STMF CLEARED-CONSTRUCTED-ONLY, WMD VERIFIED (MIT) — 6 of
  14 rows evidence-settled; ACLED/EM-DAT remain HUMAN; rest (verify).
- Verifier: table re-read; no code changes; suite state unchanged (131).
- Next: B-uc3-14 (methodology change process doc) or next open per rule.
