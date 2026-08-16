"""B-uc2-03a: World Mortality Dataset parser tests (committed 1.1MB snapshot)."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from tly.wmd import DeathsCell, coverage, country_series, latest_observation, parse_wmd

REPO = Path(__file__).resolve().parent.parent
WMD = REPO / "data" / "snapshots" / "2026-08-17" / "wmd_world_mortality.csv"


def test_full_parse_shape():
    cells = parse_wmd(WMD)
    assert len(cells) == 34423
    assert len({c.iso3 for c in cells}) == 127
    assert {c.time_unit for c in cells} == {"weekly", "monthly"}
    assert all(isinstance(c.deaths, Decimal) for c in cells)


def test_first_row_pinned():
    cells = parse_wmd(WMD, countries={"ALB"}, years={2015})
    first = country_series(cells, "ALB")[0]
    assert first == DeathsCell(
        iso3="ALB",
        country="Albania",
        year=2015,
        time=1,
        time_unit="monthly",
        deaths=Decimal("2490"),
    )


def test_country_series_sorted_single_unit():
    cells = parse_wmd(WMD, countries={"DEU"})
    series = country_series(cells, "DEU")
    keys = [(c.year, c.time) for c in series]
    assert keys == sorted(keys)
    assert {c.time_unit for c in series} == {"weekly"}


def test_latest_observation_and_staleness_fact():
    """The observed 2024-12 data edge — the staleness fact recorded in the
    manifest. If a refetch ever pushes past 2024, this pin must be updated
    WITH the manifest (new snapshot date), not silently."""
    cells = parse_wmd(WMD)
    cov = coverage(cells)
    assert max(year for year, _ in cov.values()) == 2024
    uzb = latest_observation(cells, "UZB")
    assert (uzb.year, uzb.time, uzb.deaths) == (2024, 12, Decimal("15586"))


def test_filters_and_errors():
    with pytest.raises(ValueError, match="no rows matched"):
        parse_wmd(WMD, countries={"XXX"})
    cells = parse_wmd(WMD, countries={"ALB"})
    with pytest.raises(ValueError, match="no observations"):
        country_series(cells, "DEU")


def test_malformed_period_rejected(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text(
        "iso3c,country_name,year,time,time_unit,deaths\nAAA,Testland,2020,54,weekly,100\n"
    )
    with pytest.raises(ValueError, match="week 54 out of range"):
        parse_wmd(bad)
    bad.write_text("iso3c,country_name,year,time,time_unit,deaths\nAAA,Testland,2020,1,daily,100\n")
    with pytest.raises(ValueError, match="unknown time_unit"):
        parse_wmd(bad)
