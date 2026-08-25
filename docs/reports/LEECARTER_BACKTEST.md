# Lee-Carter vintage backtest report (C-uc6-04 / D-02; RP Part IV P2 gate)

Module-produced by tly.backtest — never hand-typed. Methodology
v0.5.0-reconstruction. Generated 2026-08-25 from the committed 2026-08-25
Eurostat snapshots (keyless chain, ruling B-uc2-02(c)).

## Protocol (adaptation stated)

RP prescribes fit-through-1990/project-to-2020 on HMD series reaching to
the 1950s; the keyless registry data BEGINS in 1990. Adapted protocol,
same structure: **fit 1990-2005 (16y), project 2006-2024 (19y
out-of-sample, containing the COVID structural break)**. Jump-off
correction: projections anchored at last observed rates; both paths
computed. Cairns-2009 protocol refinements are reading-gated (R2) and
may supersede this harness via version bump.

## The bias, stated (projected minus realized e0, years)

| Country | Full bias | MAE | Pre-COVID (2006-19) | COVID (2020-21) | 2022+ |
|---|---|---|---|---|---|
| IT | +0.405 | 0.459 | +0.096 | +1.488 | +1.123 |
| DE | -0.420 | 0.495 | -0.598 | -0.079 | +0.181 |
| SE | +0.104 | 0.157 | +0.037 | +0.449 | +0.187 |

## Reading

- **Pre-COVID skill:** 14 out-of-sample years within |bias| ≤ 0.6y for
  all three countries (IT +0.096, DE -0.598, SE +0.037).
- **COVID blindness, quantified:** IT 2020 projected e0 83.83 vs
  realized 82.25 (+1.58y). A period trend model cannot
  foresee shocks — this is WHY the index routes shocks through the
  separate burn/jump channel (E8) and settles on measurement, never on
  the model (dual-series discipline).
- **Jump-off correction measured both ways:** helps IT/SE, hurts DE
  (anchor year 2005 atypical for DE) — recorded, not assumed.
- **Persistent post-COVID gap (IT +1.12y at 2022+):** the model fitted
  through 2005 never learns the 2010s slowdown in improvement; a
  production ensemble (RP Part V Q1) would refit on rolling windows.

Bias figures are pinned as regression anchors in tests/test_backtest.py.
