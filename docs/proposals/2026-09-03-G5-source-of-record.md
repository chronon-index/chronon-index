# Proposal: G5 source-of-record switch (WHO → WPP) — methodology v0.7.0

**Status: ACCEPTED — signed off by Ben 2026-09-04 00:02 CEST ("yes i sign off"), pre-P1 shortcut; posted through 2026-09-17 regardless. Implemented as methodology v0.7.0.**
Proposed 2026-09-03 by the build loop. Refs: SPEC G5, DECISIONS 6,
RP Part VII (licensing gate), `docs/METHODOLOGY_CHANGE_PROCESS.md`.

## What changes

The settlement series' mortality input switches from the WHO GHO global
abridged life table (2019 vintage, 19 band anchors) to the **UN WPP 2024
complete life table** (2023 vintage, single ages 0–100), and the stock
estimator runs at **single-age resolution** instead of band midpoints.
Population stays WPP-derived (it already reconciles person-for-person:
N = 8,091,734,933 on both paths).

## Why

Licensing, not taste. WHO GHO's data policy is **non-commercial** —
`docs/LICENSING.md` row 3, VERIFIED-RESTRICTED — which is why the
commercial licensing gate (`tly/licensing_gate.py`) blocks the current
path by construction and every print carries the research-series
notice. WPP 2024 is **CC BY 3.0 IGO** (CLEARED 2026-08-17): share and
adapt, any purpose, commercial included, attribution required. G5 has
recorded WPP as the intended licensed source of record since DECISIONS;
A-16's closure (2026-09-03) removed the last gate in front of it.

## The level change, computed and decomposed

Dual-run on committed snapshots (2026-08-17 WPP files; v0-original WHO
inputs), Decimal-34, structure year 2023 on both sides:

| leg | S (billions) | Ē (years) |
|---|---|---|
| WHO 2019 table, banded estimator (current settlement) | 362.4126 | 44.7880 |
| WPP 2023 table, banded estimator | 363.5765 | — |
| WPP 2023 table, single-age estimator (proposed) | **363.5117** | **44.9238** |

- **Table effect: +1.1639B** — WHO 2019 → WPP 2023. WPP's World e0
  for 2023 is 73.1694 vs the WHO 2019 table's 73.1234: the 2023 table
  reflects post-COVID recovery beyond the 2019 level. (The previously
  recorded same-year gap — WPP 2019 e0 72.6093 vs WHO 73.1234, snapshot
  note 2026-08-17 — is a different-estimators discrepancy, recorded per
  RP Part VI r4; switching vintage 2019→2023 and source in one governed
  step is exactly what that note anticipated.)
- **Resolution effect: −0.0648B** — single-age exactness vs
  band-midpoint interpolation, comfortably inside the error budget's
  ±0.5% banding term.
- **Net: +1.0991B = +0.3033%** — inside the budget's ±1.87% symmetric
  measurement interval; the series level moves, its stated uncertainty
  already covered it.

## What does NOT change

- **Archived prints.** First-print-settles: every archived epoch stands
  as printed. The new version applies from the first epoch after
  acceptance, forward only.
- **The v0 golden.** AC-1.2 pins the RESTORED original values on the
  frozen `data/snapshots/v0-original/` inputs — a historical anchor,
  not a live-series constraint. It stays green untouched.
- **The keyless rule (G6).** WPP files are keyless public downloads,
  already snapshotted and hash-manifested.

## Implementation (the one-commit bump, after acceptance)

1. `VERSION_POLICY_REGISTRY["v0.7.0"]`: adds policy
   `source_of_record: "UN WPP 2024 (CC BY 3.0 IGO): complete life table
   + single-age population, single-age estimator; WHO GHO demoted to
   triangulation"` — prior policies unchanged.
2. `build_settlement_print` computes S/Ē from the WPP path
   (`tly.wpp` + `tly.stock`, the machinery the reconciliation and P6
   tests already exercise at full scale).
3. Changelog entry; dual-run table published; licensing-gate mode
   check flips for the WPP path (WHO path remains blocked commercially).
4. Attribution line (UN suggested form) added to prints' provenance.

## Comment window (the decision this document requests)

The change process offers two regimes and TODAY sits exactly on their
boundary: the pre-P1 shortcut ("Ben's explicit sign-off, recorded in
the proposal — expires at the first public print") versus the 14-day
public window ("announced wherever prints are published"). The site
went live 2026-09-03 serving the research-series prints.

**Recommendation:** treat the research series as pre-P1 for process
purposes (no settlement consumers exist; the site is hours old), take
Ben's recorded sign-off, AND leave this proposal published on the site
for the 14 days anyway — belt and braces; the effective epoch lands
whenever the sign-off does.

> **Sign-off (Ben):** RECORDED — "yes i sign off", 2026-09-04 00:02 CEST (session 01Qgyk1CmBzRsFSdjjU4Yhda).
