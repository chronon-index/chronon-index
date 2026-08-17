"""B-uc2-14: the LIVE nowcast feed — Eurostat weekly deaths, current to
~2 weeks, flowing through the existing baseline/coverage machinery."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from tly.baseline import coverage_metadata, excess_series, fit_baseline
from tly.eurostat import (
    EurostatFormatError,
    latest_week,
    parse_eurostat_weekly,
)

REPO = Path(__file__).resolve().parent.parent
CUBE = REPO / "data" / "snapshots" / "2026-08-17" / "eurostat_demo_r_mwk_ts.json"

D = Decimal


def test_parse_shape_and_freshness():
    cells = parse_eurostat_weekly(CUBE)
    assert len(cells) > 20_000
    assert all(c.time_unit == "weekly" for c in cells)
    assert all(isinstance(c.deaths, Decimal) for c in cells)
    year, week = latest_week(cells)
    # THE point of this feed: data reaches into the CURRENT year —
    # something neither WMD (ends 2024) nor login-walled STMF provides.
    assert (year, week) >= (2026, 25), "snapshot no longer current-year fresh"


def test_aggregates_never_become_countries():
    cells = parse_eurostat_weekly(CUBE)
    iso3s = {c.iso3 for c in cells}
    assert "DEU" in iso3s and "FRA" in iso3s and "SWE" in iso3s
    assert all(len(i) == 3 for i in iso3s)  # no EU27_2020 leakage
    assert not any("EU" == i[:2] and i not in {"EST"} for i in iso3s if i != "EST"), iso3s


def test_live_2026_nowcast_end_to_end():
    """The demonstration the whole chain was built for: kk-linear baseline
    fit on 2015-2019 Germany, excess computed FOR 2026 WEEKS from a
    cleared, keyless feed — the index can adjust on current data."""
    cells = parse_eurostat_weekly(CUBE, countries={"DEU"})
    bl = fit_baseline(cells, "DEU")
    ex = excess_series(cells, bl, 2026)
    assert len(ex) >= 25  # weeks of 2026 already measurable
    assert all(e.expected > D(10_000) for e in ex)  # sane German weekly level
    cov = coverage_metadata(cells, bl, 2026)
    assert cov.measured_share > D("0.4")  # mid-year: a real partial-year share
    assert cov.time_unit == "weekly"


def test_compatible_with_wmd_cell_shape():
    """One cell type across feeds: Eurostat cells flow through the same
    machinery WMD cells do — country_series ordering included."""
    from tly.wmd import country_series

    cells = parse_eurostat_weekly(CUBE, countries={"SWE"})
    series = country_series(cells, "SWE")
    keys = [(c.year, c.time) for c in series]
    assert keys == sorted(keys)
    assert series[0].year == 2014  # baseline history reaches the fit window


def test_format_discipline(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text('{"id": ["freq"], "size": [1], "dimension": {}, "value": {}}')
    with pytest.raises(EurostatFormatError, match="geo/time"):
        parse_eurostat_weekly(bad)
