"""C-uc6-03 / B-uc2-19: Lee-Carter fits with fetched replication targets.

The IT targets come from the B-uc2-02 ruling's verified reference run
(drift -2.0330, sigma 2.4981, explained 0.9270 — fetched, never
invented). Our fit runs on a LATER Eurostat pull (2026-08-25 vs the
ruling's 2026-08-20) and a same-algorithm-different-code path, so exact
equality is not expected: per the D4 doctrine, live-fetch vintage runs
reproduce-or-journal. Both are asserted — proximity to the ruling's
targets with stated tolerances, and byte-exact pins of OUR fit as the
regression anchor.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tly.leecarter import lee_carter, log_mx_matrix

REPO = Path(__file__).resolve().parent.parent
S = REPO / "data" / "snapshots" / "2026-08-25"
MAGEC = S / "eurostat_demo_magec_it_de_se.json"
PJAN = S / "eurostat_demo_pjan_it_de_se.json"


def _fit(geo: str):
    return lee_carter(log_mx_matrix(MAGEC, PJAN, geo, range(1990, 2025)))


def test_it_replicates_ruling_targets_within_vintage_drift():
    fit = _fit("IT")
    # ruling targets (2026-08-20 pull) vs our 2026-08-25 pull:
    assert abs(fit.drift - (-2.0330)) < 0.05  # observed |delta| 0.024
    assert abs(fit.sigma - 2.4981) < 0.25  # sigma is last-point-sensitive
    assert abs(fit.explained - 0.9270) < 0.02
    # OUR values, pinned exactly as the regression anchor:
    assert f"{fit.drift:.4f}" == "-2.0574"
    assert f"{fit.sigma:.4f}" == "2.7027"
    assert f"{fit.explained:.4f}" == "0.9123"


def test_three_country_fits_and_identification():
    for geo, drift_pin, expl_min in (
        ("IT", "-2.0574", 0.85),
        ("DE", "-1.2572", 0.80),
        ("SE", "-1.7769", 0.55),
    ):
        fit = _fit(geo)
        assert f"{fit.drift:.4f}" == drift_pin
        assert fit.drift < 0  # mortality improves everywhere
        assert fit.explained > expl_min
        # identification constraints hold to machine precision
        assert abs(sum(fit.bx) - 1.0) < 1e-9
        assert abs(sum(fit.kt)) < 1e-9
        assert len(fit.ages) == 101 and len(fit.years) == 35


def test_forecast_is_rw_with_drift():
    fit = _fit("IT")
    path = fit.forecast_kt(5)
    assert len(path) == 5
    steps = [b - a for a, b in zip([fit.kt[-1]] + path, path)]
    assert all(abs(s - fit.drift) < 1e-12 for s in steps)
    # projected log-rates move DOWN over time at (almost) all ages
    now = fit.log_mx_hat(fit.kt[-1])
    later = fit.log_mx_hat(path[-1])
    falls = sum(1 for a, b in zip(now, later) if b < a)
    assert falls > 90  # bx has small negative entries at a few ages


def test_ragged_grid_rejected():
    grid = log_mx_matrix(MAGEC, PJAN, "SE", range(2000, 2005))
    del grid[50][2003]
    with pytest.raises(ValueError, match="ragged"):
        lee_carter(grid)
