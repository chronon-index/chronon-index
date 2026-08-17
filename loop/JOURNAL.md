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

## 2026-08-17T09:28+02:00 | B-uc3-14 | DONE
- docs/METHODOLOGY_CHANGE_PROCESS.md: scope (governed policy strings;
  explicitly NOT bug fixes — those are correction-ledger, forward-only);
  procedure (proposal → comment window 14d/7d with an explicit pre-P1
  Ben-sign-off shortcut that EXPIRES at first public print → one-commit
  bump → next-epoch effective date, level breaks published side-by-side);
  enforcement section lists the five live CI tests by name.
- Wired both directions: test_change_process_doc_wired asserts the doc
  names every mechanism + enforcement test, and the changelog header now
  points at the process doc (also asserted). SPEC#3 capability now fully
  green: AC-3.1..3.5 all have live tests or evidence-settled rows.
- Verifier: suite 132 passed; ruff+format clean.
- Next: B-uc4-01 (print JSON schema: accuracy statement mandatory).

## 2026-08-17T09:45+02:00 | B-uc4-01 | DONE
- Print schema now REQUIRES an accuracy block (RP#VI rule 6 as schema):
  non-empty statement + uncertainty typed "interval" (Decimal bounds that
  must actually BRACKET the published S — an S outside its own interval
  fails) or "convention" (with a mandatory WHY note — the label alone is
  not honesty). Validated at construction AND at the consumer-side gate.
- tly/pipeline.py now emits an honestly convention-labeled block: no
  machine-produced interval exists until D-03, and the print says so in
  its own words. Three test-helper constructors updated (the schema change
  correctly broke them until updated).
- Verifier: 7 new tests (valid interval/convention, missing statement,
  unknown type, non-bracketing + inverted intervals, reason-less
  convention, live-pipeline label); suite 139 passed; ruff clean.
- Next: B-uc4-02 (static JSON API builder).

## 2026-08-17T10:05+02:00 | B-uc4-02 | DONE
- tly/api.py: static builder — api/v1/{latest.json, prints/<date>.json,
  countries.json, index.json}. index.json carries every artifact's sha256:
  the API self-describes its own integrity, so a mirror can be verified
  byte-for-byte (verify_api also rejects artifacts the index doesn't
  describe — no rogue files). assert_static_only: JSON-only, parseable, no
  executable bits (AC-4.4 no-server-runtime gate). Deterministic renders
  throughout.
- Verifier: 6 tests — layout+latest+per-epoch schema validation, tamper
  detection, rogue-file detection, static-only gate (a planted server.py
  fails), byte-identical double build, bad-input rejection. Suite 145
  passed; ruff+format clean.
- Next: B-uc4-03 (test_p9_lineage: published figures → manifest hashes).

## 2026-08-17T10:25+02:00 | B-uc4-03 | DONE
- tly/lineage.py: check_lineage walks a published API tree — integrity
  first (verify_api), then per print: every cited (snapshot, file, sha256)
  triple must EXIST in the committed manifests with exactly that hash;
  prints citing nothing are orphans; stocks (S/Ē/N) must be non-negative
  (burn exempt: signed flow). Returns all violations.
- test_p9_lineage (named per RP#X) green on the REAL pipeline print: every
  cited hash resolves to the committed manifests, zero violations. Each
  violation class provoked via an index-consistent rewrite helper (so
  lineage, not the integrity layer, is what fires): citation-hash
  mismatch, unknown snapshot, orphan print, negative stock.
- Verifier: 4 tests; suite 149 passed; ruff+format clean.
- Next: B-uc4-05 (publish gate) — B-uc4-04 needs A-17 (HUMAN, remote).

## 2026-08-17T10:45+02:00 | B-uc4-05 | DONE
- tly/publish.py: publish_prints — the ONE sanctioned publish path. Build
  into staging → run ALL gates (consumer schema per artifact, API
  integrity + closed-world index, static-only, P9 lineage) → atomic swap;
  one prior tree retained as .previous. On ANY failure: staging destroyed,
  PublishBlocked carries every violation, the existing published tree is
  byte-for-byte untouched — a bad print can block a publish but never
  half-publish or damage what is public.
- Tests simulate the realistic bypass (object.__setattr__ on the frozen
  dataclass — future code drift past constructor validation): bad label,
  gutted accuracy, ghost-snapshot lineage each block; happy path,
  previous-tree preservation (byte-compared), staging cleanup, and
  republish retiring the prior tree all verified.
- Verifier: 5 tests; suite 154 passed; ruff+format clean.
- Next: B-uc4-04 needs A-17 (HUMAN); B-uc4-06/07 check deps next
  iteration; else uc5/D-phase per priority rule.

## 2026-08-17T11:05+02:00 | B-uc4-08 | DONE
- tly/archive.py: PrintArchive — per-epoch record files + chain.json where
  record_hash(n) = sha256(prev_hash + rendered print): every print commits
  to the entire history before it. Append refuses duplicate epochs (even
  with different data — prints are FINAL), out-of-order epochs, and
  existing files; there is no delete. verify() recomputes the whole chain
  from the record files and also rejects unchained files (closed-world,
  same as the API index). head_hash is what SPEC#7 fixings and the E-02
  OpenTimestamps stamping will anchor to.
- Verifier: 6 tests — chain build+verify (link n carries hash n-1),
  duplicate-epoch raise, out-of-order raise, edited-record break,
  tampered-metadata break, unchained-file detection. Suite 160 passed;
  ruff+format clean.
- Next: B-uc4-10 (negative lineage tests) or next open per rule.

## 2026-08-17T11:18+02:00 | B-uc4-10 | DONE
- The three AC-4.1 negative classes proven through the full PUBLISH path
  (not just the lineage checker in isolation): orphan number (zero cited
  snapshots), missing provenance block (schema gate catches before
  lineage), negative value (lineage non-negativity) — each raises
  PublishBlocked naming its cause, and each leaves no site directory
  behind. Plus the all-three-at-once case: every violation reported
  together, not first-failure-only.
- Verifier: 4 tests; suite 164 passed; ruff clean.
- SPEC#4 status: AC-4.1/4.4/4.6 green + archive; 4.2/4.3/4.5-CI wait on
  A-17 (remote) / E-02 (OTS) / E-04 (stale flag). Next per priority rule:
  C-uc5-01 (gons engine core) — Phase C begins.

## 2026-08-17T11:40+02:00 | C-uc5-01 | DONE (Phase C opened)
- tly/gons.py: integer-gons ledger (G = 10^30, Python ints — arbitrary
  precision, NO Decimal rounding in the ledger layer, ever). balance_i =
  gons_i/F; rebase sets F = G/M (F multiplier = M_old/M_new), touching no
  wallet; share(wallet) returns the EXACT integer pair (gons_i, G) — the
  P2 quantity with no division anywhere. transfer_balance converts by
  truncation (Ampleforth convention), returns gons moved. Precision/
  overflow analysis documented in the module docstring (F≈2.8e18 inside
  prec 34; 1 gon ≈ 3.6e-19 tokens = dust; display Σ-exactness delegated to
  the E11 layer at C-uc5-02).
- KEY DESIGN: conservation and share-invariance live in INTEGER facts,
  immune to any Decimal context — the exactness P1/P2 demand cannot be
  eroded by a rounding-mode change.
- Verifier: 7 tests (conservation, rebase-touches-nothing, bit-identical
  shares across a 4-rebase path, balance∝M, truncation bounds, 5 illegal
  ops, documented bounds hold). Suite 171 passed; ruff+format clean.
- Next: C-uc5-02 (E11 display layer over the ledger).

## 2026-08-17T12:00+02:00 | C-uc5-02 | DONE
- allocate_by_integer_weights added to tly/gons.py: E11 with EXACT integer
  weights (gons) — divmod arithmetic throughout, so the weights-sum-to-1
  Decimal trap never arises; floors + descending-remainder distribution
  with deterministic key tie-break. display_balances: display supply = M
  floored to the nano-token quantum (sub-quantum tail of M is stated
  undisplayable, never rounded up), Σ displayed == display supply exactly.
- Verifier: 6 tests — adversarial equal-thirds, whale+dust skew at full
  G-scale, bad inputs, exact-sum over awkward shares, display-tracks-
  rebase (×2 exactly, shares fixed), sub-quantum-tail honesty. Suite 177
  passed; ruff+format clean.
- Next: C-uc5-03 (test_p1_conservation named test).

## 2026-08-17T12:15+02:00 | C-uc5-03 | DONE
- test_p1_conservation (named per RP#X) green: conservation asserted at
  BOTH layers (Σ gons == G exact int; Σ display == display supply via E11)
  after EVERY operation — scripted walk (genesis, gons + balance-unit
  transfers, organic up-rebase, shock down-rebase, wallet exhaustion,
  M collapse to one quantum, M ×1000) plus a seeded 300-op fuzz walk
  (seed 20260817, deterministic; 46 wallets created; conservation checked
  after each op, not at the end).
- The one failure in development was my wallet-count sanity threshold
  (46 vs >50), not conservation — corrected with the seed's actual count
  noted. Conservation never broke once.
- Verifier: 2 tests; suite 179 passed; ruff clean.
- Next: C-uc5-04 (test_p2_share_invariance).

## 2026-08-17T12:30+02:00 | C-uc5-04 | DONE
- test_p2_share_invariance (named per RP#X) green: 200 seeded rebases +
  12-orders-of-magnitude extremes, share vector bit-identical after every
  one. Path independence: two ledgers, divergent rebase detours, same
  final M → identical share vectors AND identical display balances.
  Mortality-neutrality corollary (DECISIONS #4): a COVID-scale down-rebase
  leaves shares untouched and shrinks every display balance (none grows).
  Complement: a TRANSFER does change shares, by exactly the gons moved.
- Verifier: 4 tests; suite 183 passed; ruff clean. SPEC#5 AC-5.1/5.2 both
  green; both formal neutrality properties (METHODOLOGY §6) now have
  machine checks.
- Next: C-uc5-05+ per backlog (rebase-from-print wiring / perf gate).

## 2026-08-17T12:45+02:00 | C-uc5-05 | DONE
- GonsLedger gained an append-only transfer log (every transfer_gons entry,
  incl. via transfer_balance) — the COMPLETE causal record of share
  changes per DEC#3.
- test_transfer_only_share_change (named) green: 50 pure-rebase epochs →
  bit-identical shares + empty log delta; with interleaved transfers →
  every wallet's gons delta equals the NET of its logged transfers exactly
  (accounting reconstruction from the log alone). Log strictly extends;
  balance-unit transfers log their truncated gons amount.
- Verifier: 3 tests; suite 186 passed; ruff+format clean.
- Next: C-uc5-06 (test_e12_neutrality) then C-uc5-07/08.

## 2026-08-17T13:00+02:00 | C-uc5-06 | DONE
- test_e12_neutrality (named per AC-5.3) green: wallet values computed in
  EXACT Fraction arithmetic (s_i × exogenous cap — rounding can neither
  manufacture nor hide a violation). Organic weekly epoch (+0.0138%) →
  values identical (wealth neutrality). COVID-scale mass-death down-rebase
  (337M life-years, the DECISIONS upper band) → shares bit-identical
  (d(s)/d(deaths)=0), values identical, every balance shrinks by exactly
  (M−burn)/M — pro-rata, no share grows. Value RATIOS exact-invariant
  under wild rebase paths; the E11 display layer obeys the same shrink.
- The METHODOLOGY §6 proofs (wealth + mortality neutrality) both now have
  machine checks, closing RP#I M4's "write both as machine-checkable
  properties" requirement.
- Verifier: 3 tests; suite 189 passed; ruff clean.
- Next: C-uc5-07 (genesis calibration κ=1, hours display).

## 2026-08-17T13:12+02:00 | C-uc5-07 | DONE
- genesis_ledger (M = κ·S, κ=1) + tokens_to_hours_minutes (1yr = 8,766h,
  floors to the whole minute — display never overstates a holding) added
  to tly/gons.py. Genesis proven against the LIVE pipeline print: M equals
  the pipeline's S at full prec-34 precision, string-equal.
- Verifier: 4 tests (genesis exact vs live print, display convention incl.
  the 52-minute floor case, just-under-a-minute → 0, float/negative
  rejection). Suite 193 passed; ruff clean.
- Next: C-uc5-08 (10k wallets × 600 epochs < 5s perf gate) — the last
  SPEC#5 task.

## 2026-08-17T13:25+02:00 | C-uc5-08 | DONE — SPEC#5 COMPLETE
- Perf gate green with 1600x headroom: 10,000 wallets × 600 epochs (each
  epoch one rebase + 5 transfers) measured 0.003s against the 5s RALPH
  Phase C gate; conservation still exact after the run. O(1) benchmark:
  1,000 rebases at 100 vs 10,000 wallets — no scaling (architecturally
  exact: rebase is a single Decimal multiply; the generous 3x noise budget
  never approached).
- SPEC#5 (Mirror gons engine) COMPLETE: AC-5.1 conservation+E11, AC-5.2
  share invariance, AC-5.3 E12 neutrality, AC-5.4 perf, AC-5.5 transfer
  log, AC-5.6 genesis calibration — all green named tests.
- Verifier: 2 tests; suite 195 passed; ruff clean.
- Next: C-uc6-01 (scenario lab: deterministic seeds).

## 2026-08-17T13:40+02:00 | C-uc6-01 | DONE
- tly/scenarios.py: Scenario as pure DATA (JSON-roundtrippable, pinned int
  seed, validated shocks) + run_scenario as a pure function — RNG only
  from Random(seed), no clocks/entropy/global state. v1 shape: initial S,
  weekly growth, seeded jitter (bp), discrete (epoch, burn) shocks —
  enough to script organic decades and pandemic weeks over the gons
  engine. Deterministic render for byte-diffing.
- test_deterministic_seeds (named per AC-6.4) green: identical seeds →
  byte-identical outputs; different seed diverges (proving the jitter path
  is really seed-driven); JSON roundtrip re-runs identically; jitter_bp=0
  is seed-independent exact compounding (the deterministic backbone).
- Verifier: 4 tests; suite 199 passed; ruff+format clean.
- Next: C-uc6-02+ per backlog (scenario lab continues).

## 2026-08-17T13:55+02:00 | C-uc6-02 | DONE
- Simulation isolation as THREE independent walls: (1) render() itself
  emits series_label=SIMULATION — no caller can forget it; (2)
  PrintArchive.append type-rejects non-WeeklyPrint with an explicit
  "simulations stay in the lab" error, archive verified untouched after
  the attempt; (3) SIMULATION is not a constructible print label — a
  simulation cannot be disguised as a print even deliberately.
- test_simulation_isolation (named per AC-6.5) green + the all-renders-
  labeled sweep. Suite 205 passed; ruff+format clean.
- Next: C-uc6-05 or C-uc6-06 (C-uc6-03/04 need D-01 HMD data — HUMAN-
  gated account); C-uc7 chain also opens.

## 2026-08-17T13:58+02:00 | correction(C-uc6-02 entry) | DONE
- CORRECTION (append-only): the previous entry and commit bb971a3's message
  state "205 tests"; the actual suite output was "201 passed, 1 deselected"
  (2 new isolation tests over 199, = 201). The 205 was my arithmetic slip,
  not a test result. Commit message left as-is (no history rewriting);
  this entry is the record.

## 2026-08-17T14:12+02:00 | C-uc6-05 | DONE
- tly/jumps.py: the E8 historical shock registry. Exactly ONE calibrated
  entry — COVID, carrying only the DECISIONS.md anchors (WHO 14.83M excess;
  148-337M life-year burn band) and the committed-WMD source pointer.
  1918/WWII/HIV are PENDING with (verify)-marked source POINTERS and no
  numbers (Johnson & Mueller, Barro-Ursua-Weng, UNAIDS, HMD
  discontinuities — pointers to fetch, not citations of read works).
- fit_frequency_severity REFUSES while any event is pending, naming every
  missing event + "never invent"; and on a complete set it raises
  NotImplementedError pointing at the successor task — the scaffold cannot
  silently pretend to fit in either direction.
- Verifier: 6 tests incl. pending-carry-no-numbers sweep; suite 207
  passed; ruff clean.
- Next: C-uc6-06 (test_p8_interval_coverage on synthetic data).

## 2026-08-17T14:30+02:00 | C-uc6-06 | DONE — all 10 invariants named+green
- tly/interval_coverage.py: measure_coverage (inclusive bounds, matching
  the print schema) + CoverageResult with Decimal binomial tolerance
  3·sqrt(p(1−p)/n). test_p8_interval_coverage (named, NEVER skipped;
  the pre-P3 honesty stated in the docstring per amended AC-6.1):
  exact-construction 90% case measured as exactly 0.9 with an
  overclaiming nominal (0.99) rejected; seeded noisy case within
  tolerance; inclusive-bounds and input-discipline checks.
- MILESTONE: all ten RP Part X invariants now have green named tests —
  P1 conservation, P2 share invariance, P3 reconciliation, P4 (archive
  immutability errors), P5 reproducibility, P6 identity closure, P7
  coverage honesty, P8 interval coverage (harness), P9 lineage, P10
  correction completeness.
- Verifier: 4 tests; suite 211 passed; ruff+format clean.
- Next: C-uc7 chain (settlement fixing module) per priority rule.

## 2026-08-17T14:48+02:00 | C-uc7-01 | DONE
- tly/fixings.py: Fixing — provenance-complete BY CONSTRUCTION (epoch,
  Decimal value, methodology version, ≥1 snapshot-file sha256 [format-
  checked], http(s)-only source URLs; incomplete provenance cannot exist,
  not merely fail-validate-later). DRAFT→FINAL one-way lifecycle: drafts
  correctable; finalize() computes the canonical-render sha256; after
  FINAL, EVERY attribute write raises with the DEC#7 message (corrections
  → ledger + next epoch). Identical content ⇒ identical fixing hash
  (recomputer comparison anchor).
- Verifier: 4 tests (lifecycle, 8 construction rejections, render field
  coverage, hash-binds-to-content). Suite 215 passed; ruff+format clean.
- Next: C-uc7-02 (test_p4_immutability — the last unnamed invariant test).

## 2026-08-17T15:05+02:00 | C-uc7-02 | DONE
- test_p4_immutability (named per RP#X) green across all three FINAL
  layers: FINAL fixing rejects writes to EVERY attribute incl. status and
  fixing_hash themselves (value verified untouched after all attempts);
  prints are frozen dataclasses; the archive refuses re-opening a
  published epoch with head-hash verified unchanged.
- test_corrections_route_forward_only: the sanctioned path walked end to
  end — FINAL fixing stays as published, ledger entry records the
  deviation (parsed by the real parser), the NEXT epoch absorbs the
  correction, and find_restatements confirms zero restatements. DEC#7 as
  an executable procedure, not a policy sentence.
- Verifier: 2 tests; suite 217 passed; ruff+format clean.
- Next: C-uc7-03 (first-print-settles enforcement).

## 2026-08-17T15:25+02:00 | C-uc7-03 | DONE
- settle_from_archive added to tly/fixings.py: the ONE way to produce a
  fixing — reads the epoch's print from the archive (which admits exactly
  one print per epoch), resolves REAL source URLs from the committed
  manifests the print's hashes cite (derived files resolve through their
  parent's URL; missing manifests/rows fail; my first draft used
  placeholder URLs — rewritten before commit, fabrication-flavored
  evidence is not evidence).
- First-print-settles holds BY COMPOSITION and is tested with the real
  pipeline print: fixing == first print; a "better" recomputation cannot
  enter the archive; re-settling is byte-identical (same fixing hash);
  fixing-before-print raises; fixing URLs really contain the WHO GHO and
  OWID endpoints.
- Verifier: 3 tests; suite 220 passed; ruff+format clean.
- Next: C-uc7-04 (48h dispute log, log-only).

## 2026-08-17T15:45+02:00 | C-uc7-04 | DONE
- tly/disputes.py: append-only JSONL dispute log. 48h window validated
  against the epoch (inclusive at exactly 48h, closed at +1s; cannot
  precede the epoch); caller-supplied timestamps (no clock reads —
  deterministic); every record carries the log-only effect statement.
  Late filings refused loudly, never silently dropped.
- The named property tested end to end with real pipeline prints: dispute
  filed against a FINAL fixing → fixing bit-identical (render compared),
  re-settlement same hash, AND the next epoch archives + settles on
  schedule. A dispute is a record, not a lever.
- Verifier: 4 tests; suite 224 passed; ruff+format clean.
- Next: C-uc7-05 (settlement-series discipline vs INFORMATIONAL).

## 2026-08-17T16:00+02:00 | C-uc7-05 | DONE (real gap closed)
- GAP FOUND AND CLOSED: settle_from_archive read the epoch's print without
  checking series_label — an archived INFORMATIONAL (cohort) print could
  have become a settlement fixing. Now refused with the dual-series rule
  named in the error. Archiving cohort prints stays legitimate (published
  data); settling on them is not.
- Tests: informational-cannot-settle (the gap's regression), settlement-
  still-settles, and the DualSeries accessor belt-to-braces check.
- Verifier: 3 tests; suite 227 passed; ruff clean.
- Next: C-uc7-06+ per backlog.

## 2026-08-17T16:20+02:00 | C-uc7-06 | DONE — SPEC#7 executable ACs complete
- docs/REPRODUCE_FIXING.md: 8 steps for a stranger — tree integrity gates
  first, byte-determinism second, upstream verification with the
  revision-vs-tampering distinction spelled out, fixing-hash comparison as
  the agreement protocol, the 48h dispute path on mismatch, and an
  explicit "what you may NOT conclude" section (agreement proves
  derivation, not truth). Current-state caveats stated (no public remote,
  no official prints yet).
- The doc is TESTED: every load-bearing mechanism named; the step-6 code
  snippet actually executed as a subprocess by an outsider's path and
  produces a 64-hex fixing hash; the honesty sections asserted present.
- SPEC#7 status: AC-7.1..7.6 all have green tests/artifacts (7.5's full
  gate — an external party reproducing WITHOUT assistance — remains a
  P5-phase HUMAN milestone by nature).
- Verifier: 3 tests; suite 230 passed; ruff clean.
- Next: D-03 (error-budget module — unblocks B-uc2-09).

## 2026-08-17T16:45+02:00 | D-03 | DONE
- tly/error_budget.py: symmetric terms (±1.0/±1.5/±0.5%) in Decimal
  quadrature = 1.8708% ("~±2%"); one-sided terms (vintage lag +2–3%,
  period-vs-cohort +3–8%) LISTED never netted, structurally excluded from
  the quadrature set (tested disjoint); interval brackets measured S;
  cohort band = S×1.05 .. S×1.11.
- Module-produced statement: "Measured-period S = 362.4B ± ~1.9% ... 
  cohort stock ~ 381-402B ...". HONEST DEVIATION from DECISIONS prose
  ("380-400B"): 362.4126×1.05 = 380.53B → 381 at whole-billion rounding,
  and ×1.11 = 402.3 → 402. The module emits computed values; the prose had
  rounded loosely. Never tuned; noted in module docstring + backlog.
- Retirement path stated: Monte Carlo intervals replace this at rung 4 via
  version bump.
- Verifier: 6 tests; suite 236 passed; ruff+format clean.
- Next: B-uc2-09 (wire this budget into every print — its dep just
  cleared) per priority rule.

## 2026-08-17T17:05+02:00 | B-uc2-09 | DONE
- accuracy_block() added to tly/error_budget.py; the pipeline's interim
  convention label (honest placeholder since B-uc4-01) is RETIRED — every
  print now embeds the module-produced Part VIII statement + a real
  interval from the quadrature, with one-sided terms listed alongside and
  a produced_by field naming the module.
- The schema check is byte-equality: the pipeline print's accuracy dict
  must EQUAL accuracy_block(S) exactly — hand-typed accuracy text anywhere
  in a print now fails the suite. Interval-brackets-S enforcement was
  already in the schema (B-uc4-01) and now applies to real intervals.
- Verifier: suite 236 passed (accuracy test upgraded in place); ruff+
  format clean.
- CHECKPOINT (usage limit): stopping cleanly at a green suite.

## 2026-08-17T17:25+02:00 | D-05 | DONE
- tly/formulary.py: E1-E12 registry, each with statement + HOME module (or
  honest pending note: E3 derivation lives in METHODOLOGY §4; E6/E7 are P2
  phase pending HMD data). Cross-reference TEST: every claimed home
  imports AND its source cites the equation number — the check found two
  missing citations (E9 in error_budget, E12 in gons) which were added as
  true statements (quadrature = E9's variance-addition at aggregate level;
  gons implements E12 neutrality). 9 implemented, 3 honestly pending.
- Verifier: 4 tests; suite 240 passed; ruff clean.

## 2026-08-17T17:45+02:00 | D-06 | DONE (skeleton; fetch blocked, routed)
- iosco.org 403s both a project UA and a browser UA via curl — the 2013
  Principles PDF could NOT be fetched. Per the no-recalled-text rule, the
  skeleton contains ZERO document content: no titles, not even the
  principle count. What it does contain: the row-filling discipline (no
  compliance claim without a named evidence artifact), the unblock
  procedure, and a repo-side candidate-mapping inventory (methodology
  governance / transparency / data quality / complaints / determination
  integrity artifacts, plus expected structural gaps: administrator
  separation, external audit, cessation policy).
- D-06b added to backlog: browser-assisted fetch + snapshot, then fill
  rows reading from the PDF only.
- Verifier: doc reviewed against the rule (grep for any principle-like
  recalled text: none); no code changes; suite state 240.

## 2026-08-17T18:00+02:00 | D-07 | DONE
- docs/WHITEPAPER_SKELETON.md: the 7 Part XI sections, each with
  must-argue, repo-substance pointers, and READING GATES — sections 1/4/6
  are explicitly blocked on the HUMAN reading program (Vaupel, the
  longevity-market literature, Becker) with (verify) markers; the
  Strauss-Howe never-load-bearing warning preserved. Section 7's risk seed
  list is drawn entirely from repo evidence (incl. the reconstruction
  provenance itself and the WMD staleness). Assembly-order note: 3/5/7 are
  draftable from CI-verified artifacts alone; 4/6 blocked on readings.
- No invented content: zero drafted prose, zero characterized-but-unread
  citations.
- Verifier: doc re-read against the rule; suite state 240; tree clean
  after commit.

## 2026-08-17T18:15+02:00 | D-08 | DONE
- docs/GLOSSARY.md: all 12 mandated terms + gons, every definition
  ASSEMBLED from repo sources with the source cited per entry (DECISIONS /
  RP / module paths); the saeculum entry carries its (verify) on the Roman
  sources and preserves the never-Strauss-Howe rule; drift's entry flags
  its recovered-pending-ratification status.
- Verifier: term list checked against the backlog line (all present);
  no code changes; tree clean after commit.

## 2026-08-17T18:30+02:00 | D-09 | DONE
- docs/FAQ.md: one-pager + 8 FAQ entries + the pre-written pricing-lives
  response. The response argues RP Part V Q5's own line (VSL/QALY
  institutions weigh life-years in public; opacity is worse; TLY holds no
  personal data) while every institutional SPECIFIC (current VSL figure,
  NICE threshold) carries (verify) — the argument is given by the program,
  the numbers wait for the D9 sources. Every FAQ claim maps to a repo
  artifact (neutrality tests, reproduction doc, ledger, dispute log);
  the reconstruction-pending-ratification status is stated in the FAQ
  itself ("Don't trust it — check it").
- Pre-launch status header marked for removal at launch.
- Verifier: claims cross-checked against repo facts; tree clean after
  commit; suite state 240.

## 2026-08-17T18:45+02:00 | D-11 | DONE
- docs/notes/READING_NOTES.md: R1-R7 templates, 24 entries transcribed
  from RP Part III's own reading list (each (verify) until fetched), every
  one Status: UNREAD with Summary: (empty) — verified by script (counts
  match; zero READ claims). Entry-completion format specified. Cross-links
  to the gates each reading unblocks (Vaupel→whitepaper §1, Cairns
  2009→C-uc6-04 backtest protocol, IOSCO→D-06b [fetch-blocked noted],
  Wheatley→dispute-design check, Ampleforth→gons divergence audit,
  Becker→whitepaper §6).
- Verifier: template-discipline script above; tree clean after commit.

## 2026-08-17T18:52+02:00 | correction(D-11 iteration mechanics) | DONE
- CORRECTION: the D-11 verifier script initially FAILED (my regex demanded
  'Status: UNREAD' on one line; two entries line-wrap after 'Status:' —
  the DISCIPLINE held: 24 UNREAD, 24 empty summaries, zero READ claims;
  the check was too strict, re-verified with a whitespace-tolerant regex).
  Worse: my shell chain put the failure-gated steps after a heredoc, so
  the journal append and commit b8a9b5a ran UNCONDITIONALLY while the
  BACKLOG check-off (inside the failed chain) was skipped — commit and
  backlog disagreed until this commit. Both repaired here; lesson for
  LEARNINGS: never place gated steps after a heredoc terminator in one
  Bash invocation.

## 2026-08-17T19:02+02:00 | correction(D-11, second) | DONE
- SECOND CORRECTION, worse than the first: while repairing the D-11 state
  divergence I repeated the identical heredoc-breaks-the-chain mistake —
  commit a106b36 also landed with a failed verifier and no backlog update.
  Root causes now understood by INSPECTION not regex: the notes file has
  exactly 24 entries / 24 empty summaries / zero READ claims (the only
  READ text is the completion template inside a code fence); my verifier
  regexes were counting prose and wrapped lines, not entries. Backlog now
  checked (this commit); the LEARNINGS heredoc rule from a106b36 stands,
  and this commit itself uses no heredocs.

## 2026-08-17T19:20+02:00 | E-01 | DONE
- tly/site.py: files-only generator — 9 pages rendered from committed
  artifacts (README, METHODOLOGY, LICENSING, changelog, correction ledger,
  change process, reproduce doc, glossary, FAQ) into a minimal HTML shell
  with zero JavaScript and all content HTML-escaped: the site cannot
  mangle or inject into a governance document; what renders is
  byte-derived from git. Markdown treatment minimal and total (headers,
  fences, paragraphs; unterminated fences still yield valid HTML).
- Verifier: 4 tests — every page renders, double build byte-identical,
  no-scripts sweep, and load-bearing text faithfulness (C-0001 in the
  ledger page, the pricing-lives response in the FAQ page). Suite 244
  passed; ruff+format clean. No heredocs in this iteration.
- Next: D-10 (site map wiring — deps just cleared).

## 2026-08-17T19:45+02:00 | D-10 | DONE
- The mandated 8-page site map is complete: docs/API_REFERENCE.md written
  (assembled from tly/api.py + the print schema — layout, field semantics,
  integrity procedure, append-only stability rule) and registered; the
  vintage-archive page is SYNTHESIZED from the committed manifests at
  build time (per-vintage file counts, committed-vs-manifest-only split,
  truncated hashes) — the page IS the manifest record restated, nothing
  invented. One complete nav on every page.
- Verifier: test_d10_site_map_complete (all 8 mandated pages, real vintage
  content from both snapshot dates, nav completeness) + the page-set test
  updated for the synthesized page. Suite 245 passed; ruff clean.

## 2026-08-17T20:05+02:00 | E-02 | DONE
- tly/timestamping.py: OTS workflow manager — .hash/.ots layout beside the
  archive; record_target refuses digest overwrites (a new epoch needs a
  new name); stamp() invokes the REAL external ots client and raises
  honestly when none is installed (no  on this machine — verified);
  status() surfaces UNSTAMPED/STAMPED/STALE (stale = live hash diverged
  from the recorded one — surfaced, never hidden). The module never fakes
  a proof.
- Tests use a stub-client local fixture (sh script producing .ots) to
  exercise OUR orchestration without faking cryptography in the module;
  the no-client path is asserted honest; archive head integrates as a
  stampable target. B-uc4-06 (CI verifies proof before publish) remains
  open pending the real client + A-17.
- Verifier: 6 tests; suite 251 passed; ruff+format clean.

## 2026-08-17T20:12+02:00 | correction(E-02 entry) | DONE
- CORRECTION: the E-02 entry reads "no  on this machine" — zsh
  command-substituted a backticked word inside a double-quoted python -c
  string, deleting the client name from the sentence. It should read:
  "no ots client on this machine". Entry appended, not edited.
  LEARNINGS: journal writes go through heredoc-fed python (quoting-safe),
  never shell-interpolated -c strings — inverse of the earlier heredoc
  rule: heredocs for CONTENT, flat chains for CONTROL FLOW.

## 2026-08-17T20:30+02:00 | E-03 | DONE
- tly/vintages.py: ALFRED-style addressing — list_vintages (manifested,
  date-named dirs only), manifest_for(vintage), vintage_as_of(query) =
  latest vintage <= query, with pre-first-vintage queries an ERROR (no
  silent extrapolation into a data world that did not exist).
- Never-delete at the VINTAGE level made explicit:
  test_every_historical_vintage_still_present walks all git history for
  snapshot directories and requires each in HEAD — complementing the
  file-level immutability gates.
- Verifier: 4 tests (real-tree listing, per-vintage manifests, as-of
  resolution incl. future query -> latest, history walk). Suite 255
  passed; ruff+format clean.

## 2026-08-17T20:50+02:00 | E-04 | DONE
- tly/failure_ladder.py: the four-rung ladder as pure decision logic (no
  IO, no clocks — caller supplies per-source availability + carried-epoch
  counts): HEALTHY -> CARRY (outage: carry the named last vintage, keep
  publishing) -> STALE (carried > 2 epochs: publish flagged) -> DEFER
  (carried > 4: the status publishes but THE FIXING DEFERS — settling on
  invented-fresh data is worse than settling late; never blocks the next
  epoch's attempt). Worst source governs the print rung; recovery resets
  (current data age, not grudges); per-source states in the status block.
- Verifier: 8 tests — one per rung + recovery + worst-source-governs +
  input discipline + decision-is-data. Suite 263 passed; ruff+format
  clean.

## 2026-08-17T21:10+02:00 | E-06 | DONE
- tly/zenodo.py: dry-run deposit builder — vintage files + deposition.json
  (Zenodo metadata payload) + CHECKSUMS.sha256, zero network. LICENSE-AWARE
  INCLUSION is the substance: WHO GHO extracts are EXCLUDED from the
  deposit (their confirmed NC clause restricts exactly this open-DOI
  redistribution) but travel as manifest rows — hash + source URL — so
  anyone refetches and verifies independently; UN WPP / OWID / WMD /
  evidence-of-license files included; in_git:false large files manifest-
  only. Every exclusion visible in the metadata with its reason — the
  deposit never claims more completeness than the licenses allow.
- Live upload remains E-05 (HUMAN: Zenodo account).
- Verifier: 5 tests (classification vs licensing table, both vintages
  built, byte-identity of copied files vs manifest hashes, metadata shape,
  unknown vintage). Suite 268 passed; ruff+format clean.

## 2026-08-17T21:35+02:00 | E-13 | DONE (live-verified)
- Dockerfile (python:3.12-slim, package + committed snapshots + seed only;
  .dockerignore excludes loop/tests/docs) built and RUN on this machine
  (daemon 29.6.1, verified live): two --network=none container runs
  byte-identical, AND container output byte-identical to the host run —
  across a DIFFERENT OS and CPython version (Linux/3.12 vs macOS/3.13).
  The strongest P5 evidence yet: byte-identity holds cross-platform.
- REPRODUCE_FIXING.md gained the one-command Docker section (6b) with the
  cross-platform verification recorded.
- Verifier: the two diffs above (both empty); suite unchanged (268).

## 2026-08-17T10:20+02:00 | B-uc3-10 | DONE (session resumed 2026-08-17 morning)
- Remaining licensing rows verified with snapshotted+manifested evidence
  (6 new files): Eurostat/EC content CC BY 4.0 (legal notice) — CLEARED;
  CDC materials mostly public domain (with a per-dataset-exceptions note)
  — CLEARED; UCDP datasets free + CC BY 4.0 redistributable-with-citation
  via BULK downloads — CLEARED, with the important catch that UCDP's API
  is now TOKEN-AUTHENTICATED (second keyless-rule collision after STMF;
  resolved architecturally: bulk downloads only); Economist model repo MIT
  via the GitHub license API — CLEARED; IHME Free-of-Charge NON-COMMERCIAL
  agreement confirmed — VERIFIED-RESTRICTED (triangulation only stands);
  WMD upgraded to CLEARED (confirming B-uc2-03a); UBS row set ROLE-LIMITED
  (cite-only, not in any compute path — no terms fetch needed unless the
  role expands).
- LICENSING TABLE STATE: every non-HUMAN row is now evidence-settled —
  CLEARED×6 (WPP, OWID, WMD, Eurostat, CDC, UCDP, Economist =7),
  CLEARED-CONSTRUCTED-ONLY×2 (HMD, STMF), VERIFIED-RESTRICTED×2 (WHO,
  IHME), ROLE-LIMITED×1 (UBS); HUMAN×2 (ACLED, EM-DAT). B-uc3-13 (the
  licensing CI gate) is now unblocked.
- Verifier: manifest+immutability gates green (9 passed) over the extended
  manifest.

## 2026-08-17T10:45+02:00 | B-uc3-13 | DONE — the P1 licensing gate is live
- tly/licensing_gate.py: the gate reads docs/LICENSING.md ITSELF (the
  table is the law; no second source of truth to drift), maps compute
  files to rows by prefix (unknown files FAIL CLOSED), and applies mode
  semantics: commercial requires CLEARED/CLEARED-CONSTRUCTED-ONLY;
  research additionally tolerates VERIFIED-RESTRICTED; HUMAN blocks both.
- THE HONEST HEADLINE, as a named test: the commercial gate BLOCKS today's
  pipeline (it cites WHO GHO files, confirmed non-commercial) — the gate
  correctly guards the G5 WPP migration; the WPP-only compute path already
  passes commercial mode, so the migration target is gate-legal. Research
  mode passes the current pipeline (the v0 posture). Compute files are
  taken from the print's OWN provenance — the gate audits what the print
  actually cites, not a hand-maintained list.
- Verifier: 7 tests; suite 275 passed; ruff+format clean.
- Backlog state: every executable non-HUMAN task is now DONE. Remaining
  open items are HUMAN gates (A-16/A-17, HMD account+ruling, ACLED/EM-DAT,
  counsel, trademark, readings, accounts) and their dependent chains.

## 2026-08-17T11:05+02:00 | B-uc4-09 | DONE (found by the dep-graph audit)
- The frontier-verification script (dep-graph walk: does every open
  non-HUMAN task transitively root in an open HUMAN gate?) caught
  B-uc4-09 as still executable — my ad-hoc grep filters had hidden it.
  Machine-checking the frontier claim instead of eyeballing it is what
  found the gap.
- Substance beyond E-01/D-10: LIVENESS — test proves an artifact edit
  (a probe entry appended to a staged copy of the correction ledger)
  appears in the next site build, and the vintage-archive page tracks the
  staged manifests (one vintage staged -> one vintage rendered). No stale
  intermediate copies exist between git and the site.
- Verifier: 1 test (staged-repo liveness probe); suite 276 passed;
  ruff+format clean.
- Frontier audit result this iteration: 120 tasks, 86 done -> 87 with
  this one; re-run of the graph walk is next iteration's opening move —
  expect FRONTIER CONFIRMED.

## 2026-08-17T11:20+02:00 | frontier | BLOCKED (all remaining work is Ben's)
- FRONTIER CONFIRMED by dep-graph walk (not eyeballed): 120 tasks, 87
  done, 33 open — 14 HUMAN gates + 19 tasks transitively rooted in them.
  Zero executable non-HUMAN tasks remain. Per RALPH §8, surfacing this
  IS the completed work; the loop should HALT until a HUMAN gate clears.

- WHAT EXISTS (all verified green this session): 276 tests; the seven SPEC
  capabilities built to their executable frontier; all ten P1-P10
  invariants with named green tests; methodology v0.4.0 under a working
  version-bump guard; the licensing table fully evidence-settled with the
  P1 gate LIVE (commercial mode correctly blocks the WHO-based v0 path;
  WPP-only path passes); print->archive->fixing->dispute chain complete;
  static site + self-verifying API + Docker recomputation proven
  byte-identical cross-platform; Zenodo dry-run; OTS workflow; failure
  ladder; vintage addressing; whitepaper/FAQ/glossary/reading scaffolds.

- BEN'S GATES, in dependency order of what they unblock:
  1. A-16 ratify reconstructions -> B-uc1-13 golden anchor.
  2. A-17 GitHub org -> real CI (B-uc4-04/06/07), supply-chain (E-11/12),
     outsider-sim job (C-uc7-07).
  3. B-uc2-02 HMD account + the G6 ruling (WMD-as-feed vs version-gated
     account; note WMD staleness: data ends 2024-12) -> STMF chain
     (B-uc2-03/11/12/13 backfill + COVID-drag gate), D-01 -> Lee-Carter
     (C-uc6-03/04, D-02, D-04 cohort series).
  4. Accounts: E-05 Zenodo, E-07 Cloudflare (+domain, ties to D-14
     trademark), E-09 object storage -> E-08/E-10 deploys.
  5. Licenses/legal/reading: B-uc3-11/12 (ACLED, EM-DAT), D-06b (IOSCO
     PDF via browser), D-12 (reading program), D-13 (counsel), D-14
     (trademark) -> D-15 terms drafts, IOSCO fill, whitepaper drafting.
  6. E-14 recruit external recomputers (the P5 milestone).

- Standing risks already documented in-repo: WPP-vs-WHO ~0.5yr e0 level
  change at the G5 switch; mint residual -0.0026% (unreproducible, all
  hypotheses refuted); drift convention recovered-by-search pending
  ratification; WMD staleness; STMF+UCDP-API keyless regressions
  (UCDP resolved via bulk route).

## 2026-08-17T19:45+02:00 | A-17(partial)+B-uc4-04+E-11 | DONE — FIRST PRINT
- Ben directed "do everything that's left that you can do" — reopening
  routes previously classed HUMAN where a tool-route exists. gh was
  authenticated (HaleMarshall, repo+workflow scopes): created PRIVATE repo
  HaleMarshall/tly, pushed all 90+ commits. First real Actions run FAILED
  (newer ruff selected rules the local pin never ran — EXE001/UP017);
  fixed by pinning the ruff band and freezing lint rule selection in
  pyproject; ci.yml GREEN (run 32051122782). Praevex org + public flip
  remain Ben's (visibility decision).
- B-uc4-04: print.yml placeholder REMOVED. The Monday job now: gates
  (manifest/immutability/P5) -> tly/ci_print (current_epoch derivation,
  injectable + tested; idempotent archive append — P4-safe reruns) ->
  bot-commits archive/. Dispatched manually (GraphQL 503s worked around
  via REST): run 32051511467 SUCCESS, 18s.
- THE FIRST PRINT EXISTS: epoch 2026-08-17T12:00:00+00:00 (today is a
  real Monday), computed IN CI, committed by the bot, chain head
  4533c2b1a90077ea…, verifies locally, S = 362412641743.467008807750 —
  equals the golden value exactly. RESEARCH SERIES pending A-16 + G5
  (notice inline in the workflow; commercial gate still correctly blocks).
- E-11: requirements-dev.lock with sha256 hashes (uv pip compile).
- WMD staleness (verify) RESOLVED: repo actively maintained (2026-08-10
  commit) yet the compiled CSV edge is still 2024-12 — refetched, byte-
  identical file. Fresher weekly data must come from Eurostat/CDC direct
  feeds (both CLEARED, keyless) or STMF (HUMAN).
- Verifier: suite 279 passed locally; both workflows green in Actions;
  chain verified via PrintArchive.verify().
