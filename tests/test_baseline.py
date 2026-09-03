"""B-uc2-04: baseline expected-deaths + coverage metadata tests."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from tly.baseline import coverage_metadata, excess_series, fit_baseline
from tly.methodology import METHODOLOGY_VERSION, current_policies
from tly.wmd import DeathsCell, parse_wmd

REPO = Path(__file__).resolve().parent.parent
WMD = REPO / "data" / "snapshots" / "2026-08-17" / "wmd_world_mortality.csv"

D = Decimal


def _cell(iso3, year, time, deaths, unit="monthly"):
    return DeathsCell(
        iso3=iso3, country=iso3, year=year, time=time, time_unit=unit, deaths=D(deaths)
    )


def _synthetic_linear(iso3="TST", a=1000, b=10):
    """deaths(year, period) = a + b·(year−2017) + period — exactly linear."""
    return [
        _cell(iso3, y, p, a + b * (y - 2017) + p)
        for y in (2015, 2016, 2017, 2018, 2019, 2020)
        for p in (1, 2, 3)
    ]


def test_fit_recovers_exact_linear_trend():
    cells = _synthetic_linear()
    bl = fit_baseline(cells, "TST")
    # per-period: intercept = a + p at x̄=2017, slope = b — exact in Decimal
    for p in (1, 2, 3):
        assert bl.fits[p].intercept == D(1000 + p)
        assert bl.fits[p].slope == D(10)
        assert bl.expected(2020, p) == D(1000 + p + 30)


def test_excess_is_observed_minus_expected_exactly():
    cells = _synthetic_linear()
    shocked = cells + [_cell("TST", 2020, 4, 9999)]  # period 4 has no fit-years data
    bl = fit_baseline(shocked, "TST")
    ex = excess_series(shocked, bl, 2020)
    # period 4 lacks a fit -> absent from excess, present as imputed
    assert [e.period for e in ex] == [1, 2, 3]
    for e in ex:
        assert e.excess == 0  # synthetic 2020 follows the line exactly


def test_incomplete_fit_window_excluded():
    cells = [c for c in _synthetic_linear() if not (c.year == 2016 and c.time == 2)]
    bl = fit_baseline(cells, "TST")
    assert set(bl.fits) == {1, 3}  # period 2 dropped, not silently fit on 4 points
    with pytest.raises(ValueError, match="no baseline fit for TST period 2"):
        bl.expected(2020, 2)


def test_coverage_metadata_measured_vs_imputed():
    cells = _synthetic_linear()
    bl = fit_baseline(cells, "TST")
    cov = coverage_metadata(cells, bl, 2020)
    assert cov.measured_periods == (1, 2, 3)
    assert set(cov.imputed_periods) == set(range(4, 13))  # monthly universe
    assert cov.measured_share == D(3) / D(12)


def test_baseline_policy_is_versioned():
    """The baseline method is a registered v0.2.0 policy — changing the fit
    window or model without a bump fails test_methodology."""
    assert METHODOLOGY_VERSION == "v0.7.0"
    assert "kk-linear" in current_policies()["baseline"]
    assert "2015-2019" in current_policies()["baseline"]


def test_real_germany_covid_2020_positive_excess():
    """Factual check on the real feed: Germany 2020 total excess (weekly,
    KK baseline) is positive and materially large."""
    cells = parse_wmd(WMD, countries={"DEU"})
    bl = fit_baseline(cells, "DEU")
    ex = excess_series(cells, bl, 2020)
    total = sum((e.excess for e in ex), D(0))
    # deterministic from the committed snapshot -> exact regression pin;
    # lower than headline German 2020 estimates because the KK linear
    # trend absorbs the aging-driven secular increase (and the Dec-2020
    # wave largely books into 2021)
    assert total == D("24501.8")
    cov = coverage_metadata(cells, bl, 2020)
    assert cov.measured_share > D("0.9")  # Germany's weekly feed is near-complete
