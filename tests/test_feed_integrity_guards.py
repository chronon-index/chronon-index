"""B-uc2-15/16: the two live-feed integrity guards from ruling B-uc2-02(c).

Both traps were observed live before being guarded: the EU panel's ragged
edge (one country at the nominal max week) and the US ~8-week backfill
(newest week printing ~half its final value)."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from tly.eurostat import parse_eurostat_weekly, weekly_panel_edge
from tly.us_weekly import (
    CdcFormatError,
    latest_mature_week,
    mature_series,
    parse_cdc_weekly,
)

REPO = Path(__file__).resolve().parent.parent
EU_CUBE = REPO / "data" / "snapshots" / "2026-08-17" / "eurostat_demo_r_mwk_ts.json"
CDC = REPO / "data" / "snapshots" / "2026-08-24" / "cdc_r8kw7aab_us_weekly.json"

D = Decimal


def test_eu_panel_edge_cuts_the_ragged_tail():
    """The safe edge must sit BELOW the nominal max week: at the snapshot's
    pull, the last weeks had only a handful of reporting countries."""
    cells = parse_eurostat_weekly(EU_CUBE)
    nominal = max((c.year, c.time) for c in cells)
    edge = weekly_panel_edge(cells, min_countries=20)
    assert edge < nominal  # the ragged tail is real and gets cut
    assert edge >= (2026, 20)  # but the panel is genuinely current-year
    # tightening the requirement can only move the edge back
    assert weekly_panel_edge(cells, min_countries=25) <= edge


def test_eu_panel_edge_fail_closed():
    cells = parse_eurostat_weekly(EU_CUBE, countries={"DEU"})
    with pytest.raises(Exception, match="no week reaches"):
        weekly_panel_edge(cells, min_countries=20)  # one country can't qualify


def test_cdc_parse_and_censoring():
    cells = parse_cdc_weekly(CDC)
    assert len(cells) == 346
    assert cells[0].week_ending == date(2020, 1, 4)
    immature = [c for c in cells if not c.mature]
    assert len(immature) == 8  # exactly the censor window
    assert all(c.week_ending > date(2026, 6, 1) for c in immature)


def test_cdc_immature_tail_is_really_immature():
    """The live-observed artifact: the newest (censored) week prints far
    below the mature level — proof the censor window is load-bearing."""
    cells = parse_cdc_weekly(CDC)
    newest = cells[-1]
    assert not newest.mature
    mature_last = latest_mature_week(cells)
    assert newest.total_deaths < mature_last.total_deaths * D("0.7")
    assert mature_last.total_deaths > D(35_000)  # sane US weekly level


def test_mature_series_is_aggregation_safe():
    cells = parse_cdc_weekly(CDC)
    series = mature_series(cells)
    assert all(c.mature and c.total_deaths is not None for c in series)
    assert series[-1].week_ending < cells[-1].week_ending


def test_cdc_disorder_rejected(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(
        '[{"end_date":"2026-01-10T00:00:00.000","total_deaths":"1"},'
        '{"end_date":"2026-01-03T00:00:00.000","total_deaths":"2"}]'
    )
    with pytest.raises(CdcFormatError, match="out of order"):
        parse_cdc_weekly(bad)
