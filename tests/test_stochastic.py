"""S-04 / P3: stochastic fan + coverage backtest, pinned."""

from __future__ import annotations

import json
from pathlib import Path

from tly.stochastic import _fit_world, coverage_backtest, simulate_fan

REPO = Path(__file__).resolve().parent.parent


def test_jump_diffusion_separation_finds_covid():
    fit, drift, sigma, jumps = _fit_world(2023)
    assert len(fit.ages) == 101 and len(fit.kt) == 14
    assert drift < -1.0  # mortality improves on quiet years
    assert sigma < 1.0 < fit.sigma  # robust sigma well below COVID-contaminated raw
    assert 2020 in jumps and 2021 in jumps


def test_fan_is_deterministic_and_sane():
    a = simulate_fan(n_paths=50)
    b = simulate_fan(n_paths=50)
    assert a.p50 == b.p50  # seeded LCG: byte-stable
    assert a.p5[10] < a.p50[10] < a.p95[10]
    # 90% band at 10y stays within +-8% of central (trend risk is small)
    assert a.p95[10] / a.p50[10] < 1.08 and a.p5[10] / a.p50[10] > 0.92


def test_coverage_backtest_matches_committed_and_is_honest():
    committed = json.loads((REPO / "docs" / "reports" / "stochastic_results.json").read_text())[
        "coverage_backtest"
    ]
    cov = coverage_backtest(fit_through=2018, n_paths=500)
    assert cov.inside_90 == committed["inside_90"]
    # the honest shape: non-shock years covered, COVID years outside
    by_year = dict(zip(cov.tested_years, cov.inside_90))
    assert by_year[2019] and by_year[2022] and by_year[2023]
    assert not by_year[2020] and not by_year[2021]
