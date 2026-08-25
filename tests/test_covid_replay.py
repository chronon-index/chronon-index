"""C-uc6-07: the replay's numbers must regenerate from committed
artifacts — the report is a rendering, never a source."""

from __future__ import annotations

from decimal import Decimal as D

import pytest

from tly.covid_replay import run_replay


@pytest.fixture(scope="module")
def replay():
    return run_replay()


def test_final_figures_pinned(replay):
    assert replay["ALB"]["final"].excess_2020 == D("5813.0")
    assert replay["DEU"]["final"].excess_2020 == D("24501.8")


def test_jan_2021_carried_the_wrong_sign_for_germany(replay):
    """Finding 1: the earliest true vintage nets NEGATIVE German excess
    (50 immature weeks + a 4-year baseline) — err −106.5%."""
    p = replay["DEU"]["2021-01-14"]
    assert p.excess_2020 == D("-1598.00")
    assert p.fit_years == (2016, 2017, 2018, 2019)  # no 2015 in that vintage
    err, pct = p.error_vs(replay["DEU"]["final"])
    assert pct.quantize(D("0.1")) == D("-106.5")


def test_convergence_final_exact_by_dec_2021(replay):
    for iso3 in ("ALB", "DEU"):
        for vintage in ("2021-12-31", "2022-06-29"):
            assert replay[iso3][vintage].excess_2020 == replay[iso3]["final"].excess_2020


def test_albania_unit_switch_recorded(replay):
    assert replay["ALB"]["2021-01-14"].time_unit == "weekly"
    assert replay["ALB"]["2021-06-29"].time_unit == "monthly"


def test_fit_year_floor_refuses_thin_baselines():
    from tly.covid_replay import replay_point
    from tly.wmd import DeathsCell

    cells = [
        DeathsCell(
            iso3="ALB", country="Albania", year=y, time=1, time_unit="monthly", deaths=D(100)
        )
        for y in (2018, 2019, 2020)
    ]
    with pytest.raises(ValueError, match="below the 4-year floor"):
        replay_point(cells, "thin", "ALB")
