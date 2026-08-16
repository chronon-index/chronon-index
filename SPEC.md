# SPEC.md — CHRONON / TLY build specification (the seven capabilities)

**SPEC v1.0-draft** | 2026-08-16

> **RECONSTRUCTION NOTE.** Reconstructed 2026-08-16 from DECISIONS.md,
> RESEARCH_PROGRAM.md and RALPH_LOOP.md after loss of the original; pending
> Ben's review. The original SPEC.md, METHODOLOGY_v0.md and seed artifacts
> (tly_v0_calc.py, results_v0.json, CALC_REPORT_v0.txt) exist nowhere on this
> machine. Every criterion below is sourced from the surviving governing
> documents; nothing is invented. Where a lost artifact was the anchor, the
> surviving numbers in DECISIONS.md ("Key numbers") stand in, explicitly.

**Versioning.** This document changes only via the methodology change process
(RESEARCH_PROGRAM.md Part XI): proposal → public comment window → version
bump with changelog. No silent edits. Tasks cite capabilities as `SPEC#<n>`
and criteria as `AC-<n>.<m>`.

**Scope.** Capabilities 1–4 are RALPH_LOOP Phase B (the index); capabilities
5–7 are Phase C (the simulator). Acceptance criteria here are the verifiers,
verbatim — a task is done only when its cited AC passes in CI.

---

## SPEC#0 — Global conventions (bind every capability)

- **G1 Precision.** `Decimal` (precision 34, ROUND_HALF_EVEN) for everything
  supply- or index-adjacent. Floats never touch published numbers.
  (RALPH_LOOP §6; RESEARCH_PROGRAM M5.)
- **G2 Epoch.** Weekly print and rebase, Mondays 12:00 UTC, aligned to HMD
  STMF publication cadence. (DECISIONS defaults.)
- **G3 Immutability.** First print settles. Corrections are forward-only,
  folded into the next epoch via the correction ledger
  (`ledger/CORRECTIONS.md`). No historical value is ever restated.
  (DECISIONS 7; RP Part VI.5.)
- **G4 Verification protocol.** Every number: source URL + retrieval
  timestamp + content hash + runnable code path + methodology version stamp.
  A number without an interval is a convention and must be labeled as one.
  (RP Part VI.)
- **G5 v1 core inputs.** UN WPP population and life tables (licensed source
  of record, CC BY 3.0 IGO), HMD STMF weekly deaths, GBD YLL. WHO GHO is
  triangulation only (non-commercial clause, (verify)). Expansion only via
  governed version bumps. (DECISIONS 6, 13; RP Part VII licensing gate.)
- **G6 Keyless and secretless.** All data sources keyless; no secrets exist
  in this project and none may be added. (RALPH_LOOP §6.)
- **G7 Invariants as tests.** RP Part X invariants P1–P10 each map to a
  named CI test (`test_p1_conservation` … `test_p10_correction_completeness`)
  owned by exactly one capability below; see §8 traceability table.
- **G8 Formulary.** Reference equations are cited by number E1–E12 from
  RP Part IX; implementations carry the equation number in docstring/output
  metadata.

---

## SPEC#1 — Baseline stock engine

**Purpose.** Compute the stock S(t) = Σ over (age, sex, country) of
population × remaining life expectancy (E1), at country × sex × single-age
granularity (RP Part IV P1), with the v0 banded estimator (E2) as the
fallback for abridged inputs; decompose per-epoch change into
mint / spend / drift / burn terms per the identity (E4) and its discrete
accounting form (E5).

**Inputs.** From SPEC#3 content-hashed snapshots only (never live fetch at
compute time): WPP 2024 population by single year of age × sex × country;
WPP life tables (source of record); WHO GHO life tables as triangulation
only; interpolation policy per E2 (piecewise-linear on exact-age e(x)
anchors, flat beyond the last anchor).

**Outputs.** Global S and per-country S (Decimal); E-bar (life-years per
living person); decomposition terms B·e(0), −N, N·dĒ/dt, −Burn; all values
stamped with methodology version and snapshot manifest hashes.

**Acceptance criteria.**
- **AC-1.1** `test_p3_reconciliation` — sum of per-country dS equals global
  dS per epoch, exactly, in Decimal (invariant P3).
- **AC-1.2** Golden anchor — on the archived v0-equivalent snapshot inputs
  the engine reproduces the surviving DECISIONS.md key numbers to 4 decimal
  places: S = 362.4126B life-years (2019 WHO table × WPP2024 population)
  and 348.1905B (2021 table); E-bar = 44.7880; g = +0.7197%/yr with
  mint +9.6606B, spend −8.0917B, drift +1.0394B. The original
  `seed/results_v0.json` is lost; the regenerated golden file must match
  these surviving figures and is then committed as the new ground-truth
  anchor for the RALPH Phase A golden test.
- **AC-1.3** `test_no_float_in_published_path` — the published-value code
  paths use Decimal (prec 34, ROUND_HALF_EVEN) end to end; a test injects a
  float and asserts rejection (G1).
- **AC-1.4** Interpolation policy is versioned: the E2 policy string
  ("linear-on-anchors, flat-tail") appears in output metadata; changing it
  without a methodology version bump fails CI (RP M5).
- **AC-1.5** Engine consumes snapshots offline only: computing with a
  missing/mismatched manifest hash raises; no network access during compute
  (RALPH_LOOP §6 snapshot-first rule).

---

## SPEC#2 — Weekly mortality nowcast

**Purpose.** Produce the weekly print: nowcast the excess-death burn term
between annual structure updates using HMD STMF, compute the measured-period
settlement series, and (from P2) the informational cohort series — the dual
series. Burn per E4: Σ(excess_deaths × e(a)).

**Inputs.** HMD STMF weekly deaths by age band (~38–40 countries) from
snapshots; baseline expected deaths (versioned method); SPEC#1 stock state;
coverage metadata per country (measured vs imputed, RP Part II D6).

**Outputs.** One print per epoch (G2): measured-period S labeled
`SETTLEMENT`; from P2 onward a cohort S with interval labeled
`INFORMATIONAL` (DECISIONS default 4); measured-vs-imputed coverage share;
the Part VIII error-budget accuracy statement embedded in every print.

**Acceptance criteria.**
- **AC-2.1** `test_p6_identity_closure` — 52 weekly prints reconcile to the
  annual E5 identity within the stated (versioned) tolerance (invariant P6).
- **AC-2.2** `test_p7_coverage_honesty` — every print publishes the measured
  vs imputed share; a print without it fails schema validation (invariant P7).
- **AC-2.3** Backfill gate — ≥ 570 consecutive weekly prints backfilled,
  ending at the current epoch; the COVID drag is visible in the backfilled
  series and its cumulative burn falls within the recalibrated band of
  120–360M life-years (RALPH_LOOP §7 Phase B gate; cf. DECISIONS point
  estimate 148–337M from the WHO 14.83M excess-death anchor).
- **AC-2.4** Error budget on every print — each print embeds the RP Part VIII
  statement: symmetric terms combined in quadrature (~±2% on the v0 level),
  one-sided terms (vintage lag +2–3%, period-vs-cohort +3–8%) listed, never
  netted; produced by the deterministic error-budget module, not hand-typed.
- **AC-2.5** Dual series — from P2, every print carries both series with the
  `SETTLEMENT` / `INFORMATIONAL` labels; the settlement value never depends
  on the cohort model (DECISIONS default 4; RP Part VIII design decision).
- **AC-2.6** `test_burn_term_e4` — the excess-burn computation matches E4 on
  a fixture with known excess deaths and e(a), exactly in Decimal.

---

## SPEC#3 — Methodology & snapshot governance

**Purpose.** Make every figure reproducible forever: content-hashed data
snapshots, versioned methodology, the correction ledger, and the upstream
licensing table. This capability owns the reproducibility spine the other
six hang from.

**Inputs.** Raw upstream files (fetched snapshot-first with User-Agent,
backoff + jitter, few-and-large requests — RALPH_LOOP §6); methodology
documents; vintage history.

**Outputs.** `data/snapshots/<date>/manifest.json` with, per file: sha256,
source URL, retrieval timestamp, byte size; methodology version stamp on
every artifact; `ledger/CORRECTIONS.md` entries; `docs/LICENSING.md`
one-row-per-source table.

**Acceptance criteria.**
- **AC-3.1** `test_p5_reproducibility` — identical snapshot hashes produce
  byte-identical outputs; CI re-runs the print pipeline twice and diffs
  (invariant P5; RP Part VI.2).
- **AC-3.2** `test_p10_correction_completeness` — every deviation between
  vintages appears in the correction ledger, forward-applied only; the test
  diffs vintage pairs against ledger entries (invariant P10).
- **AC-3.3** Manifest schema — CI validates every manifest row carries
  sha256 + URL + retrieval timestamp; a snapshot file without a manifest row
  fails the build; snapshots are never deleted (RALPH_LOOP §6).
- **AC-3.4** Version-bump guard — any diff to methodology-governed
  parameters (interpolation policy, baseline method, tolerances, ensemble
  weights) without a version bump + changelog entry fails CI (RP Part VI.3,
  Part XI change process).
- **AC-3.5** Licensing gate (P1 GATE) — `docs/LICENSING.md` has one cleared
  row per source before the first public print: WPP = source of record
  (CC BY 3.0 IGO, commercial OK); WHO GHO = triangulation only
  (non-commercial (verify)); HMD redistribution restricted (verify) —
  derived indicators only; ACLED / EM-DAT rows marked HUMAN for license
  purchase (RP Part VII).

---

## SPEC#4 — Publication & static API

**Purpose.** Publish every print in public: the CI run IS the official
computation; artifacts land on a static site + static JSON API;
print hashes are OpenTimestamps-stamped. No server, no keys — the attack
surface is the repo and the data (RP Part XII).

**Inputs.** SPEC#2 prints; SPEC#3 manifests; status/failure signals.

**Outputs.** Static JSON endpoints (latest print, per-epoch history,
per-country breakdown); static site pages (methodology, data & licenses,
changelog, correction ledger, vintage archive per RP Part XI docs map);
status page with stale-print flag; `.ots` proof per print hash.

**Acceptance criteria.**
- **AC-4.1** `test_p9_lineage` — every published value traces to a manifest
  entry (no orphan numbers) and passes non-negativity checks; the test walks
  the published JSON and resolves every figure to manifest hashes
  (invariant P9).
- **AC-4.2** Public computation — the weekly Monday 12:00 UTC CI job
  produces the print with public logs; artifacts hashed and committed; a
  print produced any other way is invalid (RP Part VII).
- **AC-4.3** Timestamping — every print hash has an OpenTimestamps proof
  published alongside it; CI verifies the `.ots` file exists and matches
  the print hash before publish (RP Part VII).
- **AC-4.4** Static-only — the built API is files only; CI asserts the build
  output contains no server runtime and every endpoint is a committed file
  (RP Part VII "deliberately static-friendly").
- **AC-4.5** Stale-print logic — if the Monday print is missed or deferred,
  the status flag flips within the same epoch, following the Part XII
  failure ladder (source down → carry rule → stale flag → deferred fixing);
  test simulates a missing source and asserts the flag.
- **AC-4.6** Labeling — every published S carries the accuracy statement
  (AC-2.4) and either an interval or an explicit "convention" label
  (RP Part VI.6); schema-validated on publish.

---

## SPEC#5 — O(1) gons rebase engine (Mirror simulator)

**Purpose.** Simulate the Mirror monetary rule M(t) = κ·S(t): all balances
rebase pro-rata with S via a single global scaling factor (the gons pattern,
E10); a wallet's share changes only by transfer, never by demographics
(DECISIONS 3); symmetric down-rebase on mortality shocks (DECISIONS 4).

**Inputs.** An S path per epoch (real prints from SPEC#2 or scenarios from
SPEC#6); a wallet transfer log; κ = 1 token per life-year at genesis
(DECISIONS 2).

**Outputs.** Per-epoch balances, share vector, total supply M(t); all exact
per E10/E11; display conversion 1 life-year = 8,766 hours (DECISIONS
defaults).

**Acceptance criteria.**
- **AC-5.1** `test_p1_conservation` — Σ balances = M(t) after every
  operation, exactly; allocation by largest-remainder (E11): floor to
  quantum, distribute residual quanta by descending fractional part, sum of
  parts equals total exactly (invariant P1).
- **AC-5.2** `test_p2_share_invariance` — the share vector is identical
  across any rebase sequence: rebase multiplies the global factor F only;
  gons_i / Σ gons is invariant under any F path (E10; invariant P2).
- **AC-5.3** `test_e12_neutrality` — machine-checked E12 properties:
  wealth neutrality (wallet value = s_i × MarketCap; d(value)/d(rebase) = 0)
  and mortality neutrality (d(s_i)/d(deaths) = 0); a mass-death scenario
  shrinks every balance pro-rata and no share grows (DECISIONS 4, 11).
- **AC-5.4** Performance gate — full simulation of 10,000 wallets ×
  600 epochs completes in < 5 s (RALPH_LOOP §7 Phase C gate); a scaling
  benchmark asserts rebase cost is O(1) — independent of wallet count.
- **AC-5.5** `test_transfer_only_share_change` — across any epoch sequence
  without transfers, every wallet's share is bit-identical; with transfers,
  share deltas equal the transfer amounts exactly (DECISIONS 3).
- **AC-5.6** Genesis calibration — at genesis, M = κ·S with κ = 1 token per
  life-year; supply figures Decimal end to end (G1).

---

## SPEC#6 — Scenario & backtest lab

**Purpose.** Replay history and inject shocks to validate models, intervals
and the engine itself: Lee-Carter (E7) fitting and backtesting, jump
calibration on the 1918 / WWII / HIV / COVID set (E8), COVID replay with
real-time-vintage data, and interval-coverage scoring.

**Inputs.** Vintage archive snapshots (SPEC#3); scenario definitions
(pandemic, conflict, famine — frequency-severity per E8); model
implementations (E7); deterministic seeds.

**Outputs.** Scenario runs labeled `SIMULATION`; backtest reports with bias
stated; interval-coverage statistics; inputs to the Phase D Lee-Carter
report and P2/P3/P4 gates.

**Acceptance criteria.**
- **AC-6.1** `test_p8_interval_coverage` — backtest realized values fall
  inside published intervals at the stated rate (invariant P8, rung 4
  onward). Until stochastic intervals ship (P3), the test must exist, be
  named, and pass by validating the coverage harness on synthetic data with
  known coverage — stated honestly in the test docstring, never skipped.
- **AC-6.2** COVID replay — using only real-time-vintage data (no
  hindsight), the lab reproduces the COVID drag; the error versus the final
  figures is computed and documented (RP Part IV P4 gate mechanism).
- **AC-6.3** Lee-Carter backtest — fit on HMD data through 1990 only,
  project to 2020, compare to realized, publish the bias (RP M2 / Part IV
  P2 gate; feeds the RALPH Phase D report).
- **AC-6.4** `test_deterministic_seeds` — all Monte Carlo uses pinned seeds;
  identical seeds produce identical outputs, byte-for-byte (RP M5).
- **AC-6.5** `test_simulation_isolation` — scenario runs cannot write to
  published print paths; every lab output carries the `SIMULATION` label;
  a write attempt to print storage from lab code raises.

---

## SPEC#7 — Settlement fixing module

**Purpose.** Produce the official per-epoch fixing for cash settlement:
freeze the print into an immutable FINAL fixing record, run the log-only
dispute window, and guarantee an outsider can reproduce any fixing from
public artifacts alone.

**Inputs.** The epoch print (SPEC#2 via SPEC#4); dispute submissions;
snapshot manifest hashes.

**Outputs.** Fixing record per epoch: value (measured-period S series),
epoch timestamp, methodology version, snapshot manifest hashes, source
URLs, status lifecycle DRAFT → FINAL; append-only dispute log;
`docs/REPRODUCE_FIXING.md` outsider instructions.

**Acceptance criteria.**
- **AC-7.1** `test_p4_immutability` — no code path mutates a FINAL print:
  any mutation attempt raises; corrections route to the ledger and the next
  epoch only (invariant P4; DECISIONS 7).
- **AC-7.2** First print settles — the fixing value equals the first
  published print for the epoch, always; a later "better" value never
  replaces it (DECISIONS 7; RP Part VI.5).
- **AC-7.3** Dispute window — 48 h, log-only: filing a dispute appends to
  the dispute log and changes nothing else; the test asserts a filed
  dispute neither alters the fixing nor delays the next epoch's print
  (DECISIONS defaults).
- **AC-7.4** Settlement series discipline — fixings settle exclusively on
  the conservative measured-period S; the cohort/informational series can
  never be a settlement input (DECISIONS default 4).
- **AC-7.5** Outsider reproduction gate — `docs/REPRODUCE_FIXING.md`
  written as if the author will not be there; a CI job simulates the
  outsider: clean environment, public artifacts only (repo + published
  snapshots + instructions), reproduces a chosen fixing byte-identically
  (RALPH_LOOP §7 Phase E / RP Part IV P5 gate).
- **AC-7.6** Radical verifiability — every fixing record embeds its source
  URLs and snapshot hashes; a fixing without a complete provenance block
  fails schema validation (DECISIONS 9).

---

## 8. Traceability — invariants and gates to owners

| Invariant / gate | Owner | Criterion | CI test name |
|---|---|---|---|
| P1 conservation | SPEC#5 | AC-5.1 | `test_p1_conservation` |
| P2 share invariance | SPEC#5 | AC-5.2 | `test_p2_share_invariance` |
| P3 reconciliation | SPEC#1 | AC-1.1 | `test_p3_reconciliation` |
| P4 immutability | SPEC#7 | AC-7.1 | `test_p4_immutability` |
| P5 reproducibility | SPEC#3 | AC-3.1 | `test_p5_reproducibility` |
| P6 identity closure | SPEC#2 | AC-2.1 | `test_p6_identity_closure` |
| P7 coverage honesty | SPEC#2 | AC-2.2 | `test_p7_coverage_honesty` |
| P8 interval coverage | SPEC#6 | AC-6.1 | `test_p8_interval_coverage` |
| P9 lineage | SPEC#4 | AC-4.1 | `test_p9_lineage` |
| P10 correction completeness | SPEC#3 | AC-3.2 | `test_p10_correction_completeness` |
| ≥570-print backfill, COVID drag in 120–360M band | SPEC#2 | AC-2.3 | backfill report check |
| 10k wallets × 600 epochs < 5 s | SPEC#5 | AC-5.4 | perf benchmark |
| Outsider reproduces a fixing | SPEC#7 | AC-7.5 | outsider-sim CI job |
| Error budget on every print | SPEC#2/#4 | AC-2.4 / AC-4.6 | print schema check |
| Dual series | SPEC#2/#7 | AC-2.5 / AC-7.4 | series-label checks |
| Licensing table cleared (P1 GATE) | SPEC#3 | AC-3.5 | licensing table check |

Formulary usage: E1–E5 → SPEC#1/#2; E6–E9 → SPEC#2/#6; E10–E12 → SPEC#5
(RP Part IX). Phase gates verbatim from RALPH_LOOP §7.
