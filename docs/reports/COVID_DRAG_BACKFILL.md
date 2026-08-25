# COVID-drag backfill report (B-uc2-13 / SPEC#2 AC-2.3)

Module-produced by tly.backfill.covid_gate_report — never hand-typed.
Methodology v0.5.0-reconstruction; policy: excess-age-profile: 0.7 at exact age 75.5 + 0.3 at 85.5 on the epoch structure-year table (backfill burn conversion).
Inputs (committed, manifested): WPP World annual fixture 2010-2023; WMD
panel (127 countries); OWID/WPP world deaths. Generated 2026-08-25.

## The gate

| Quantity | Value |
|---|---|
| Backfill series | 570 consecutive Mondays ending 2026-08-24 (the archived epoch) |
| Measured panel burn, 2020+2021 | **63.4M life-years** (WMD panel, no imputation) |
| Panel coverage of world deaths (2019) | **36.10%** (panel observed / WPP world — both measured) |
| Coverage-adjusted global estimate | **175.5M life-years** |
| Gate band (RALPH §7, recalibrated) | 120-360M |
| **Verdict** | **INSIDE the band** (176M) |
| Worst measured week | 2020-W50: 1.21M life-years |

P7 discipline: the measured figure and the imputation factor are published
separately and never conflated. The adjustment has zero free parameters —
it divides one measured quantity by another. Implied global excess deaths
≈ 18.5M
vs WHO's modeled 14.83M: the uniform-rate scaling runs somewhat above the
WHO model (non-panel countries likely had different excess rates) — an
estimator difference, stated, not hidden.

## Drag visibility (both channels)

Annual deltas of S (B life-years/yr), from measured WPP structures:

| Into year | ΔS |
|---|---|
| 2015 | +3.615 |
| 2016 | +3.980 |
| 2017 | +3.453 |
| 2018 | +4.007 |
| 2019 | +3.427 |
| 2020 | -4.243 |
| 2021 | -6.018 |
| 2022 | +14.892 |
| 2023 | +4.429 |

Pre-COVID trend ≈ +3.7B/yr; **S FALLS into 2020 (−4.24B) and again into
2021 (−6.02B)** — the drag is not a slowdown but an outright contraction,
followed by the 2022 rebound (+14.89B). The weekly burn overlay peaks at
1.21M life-years in 2020-W50.

## Series conventions (real-time-vintage)

- Structure year = min(epoch_year − 1, 2023): exactly what a live index
  would have held; the 2024+ plateau weeks carry flat, flagged carried=True
  (139 of 570 weeks).
- Weekly path: E11-scheduled annual deltas, exact P6 closure at year ends.
- Burn: measured attribution only; residual-exposure semantics (E4/E5) —
  no double-counting against the annual deltas.
