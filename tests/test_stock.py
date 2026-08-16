"""B-uc1-08: E1 stock engine — country × sex × single-age, stamped outputs.

Pinned values were computed once from the committed fixtures (2026-08-17
iteration, see loop/JOURNAL.md) and serve as regression anchors; they are
NOT the settlement golden (that remains seed/results_v0.json, AC-1.2).
World 2023 on WPP single-age tables: S = 363.5117B (v0 WHO-based was
362.4126B — different life-table source, ~0.3% apart, both recorded).
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from tly.guard import FloatContaminationError
from tly.methodology import METHODOLOGY_VERSION
from tly.numeric import Q4
from tly.stock import build_report, compute_location_stock
from tly.wpp import (
    ex_anchors,
    parse_life_table_ex,
    parse_population_single_age,
    population_by_age,
)

REPO = Path(__file__).resolve().parent.parent
SNAP17 = REPO / "data" / "snapshots" / "2026-08-17"
SNAP16 = REPO / "data" / "snapshots" / "2026-08-16"
POP_FIX = SNAP17 / "fixtures" / "wpp_pop_single_age_fixture.csv.gz"
LT_COMPLETE = SNAP17 / "fixtures" / "wpp_lt_complete_fixture.csv.gz"
LT_ABRIDGED = SNAP17 / "fixtures" / "wpp_lt_abridged_fixture.csv.gz"


def _stock(location: str, year: int, sex: str = "total", table=LT_COMPLETE):
    pop = parse_population_single_age(POP_FIX, {year}, locations={location})
    lt = parse_life_table_ex(table, {year}, locations={location})
    return compute_location_stock(
        population_by_age(pop, location, year, sex),
        ex_anchors(lt, location, year, sex),
        location=location,
        year=year,
        sex=sex,
    )


def test_world_2023_pinned():
    st = _stock("World", 2023)
    assert str(st.s_billions_4dp) == "363.5117"
    assert str(st.e_bar.quantize(Q4)) == "44.9238"
    assert st.n_persons == Decimal("8091734933.000")


def test_per_country_pinned():
    ja = _stock("Japan", 2023)
    ng = _stock("Nigeria", 2023)
    assert str(ja.s_billions_4dp) == "4.8031"
    assert str(ja.e_bar.quantize(Q4)) == "38.6189"  # aged structure
    assert str(ng.s_billions_4dp) == "9.6041"
    assert str(ng.e_bar.quantize(Q4)) == "42.1448"  # young structure, lower e


def test_sex_specific_via_abridged():
    male = _stock("Japan", 2023, "male", table=LT_ABRIDGED)
    assert str(male.s_billions_4dp) == "2.2660"
    assert str(male.e_bar.quantize(Q4)) == "37.3313"


def test_world_2019_wpp_vs_v0_who_recorded_apart():
    """Same structure year, different table source: WPP-2019 S differs from
    the v0 WHO-based figure — both stand, neither is 'corrected'."""
    st = _stock("World", 2019)
    assert str(st.s_billions_4dp) == "354.4515"  # 2019 population, WPP table
    assert str(st.s_billions_4dp) != "362.4126"  # v0: 2023 pop, WHO 2019 table


def test_engine_rejects_floats():
    pop = {0: 1000.0}
    with pytest.raises(FloatContaminationError):
        compute_location_stock(pop, {0: Decimal("70")}, location="X", year=2023, sex="total")


def test_report_stamp_carries_version_and_manifest_hashes():
    stocks = [_stock("World", 2023), _stock("Japan", 2023)]
    report = build_report(stocks, year=2023, sex="total", snapshot_dirs=[SNAP16, SNAP17])
    meta = report.metadata
    assert meta["methodology_version"] == METHODOLOGY_VERSION
    assert set(meta["policies"]) == {
        "interpolation",
        "band_midpoint",
        "decimal",
        "baseline",
        "p6_closure",
        "quanta",
    }
    # every input file's sha256 is citable from the stamp, incl. uncommitted
    assert "gho_ex_global_btsx_2019_2021.json" in meta["snapshots"]["2026-08-16"]
    s17 = meta["snapshots"]["2026-08-17"]
    assert "fixtures/wpp_pop_single_age_fixture.csv.gz" in s17
    assert "WPP2024_PopulationBySingleAgeSex_Medium_1950-2023.csv.gz" in s17
    assert report.by_location()["World"].location == "World"


def test_report_rejects_mixed_year_or_sex():
    a = _stock("World", 2023)
    b = _stock("Japan", 2019)
    with pytest.raises(ValueError, match="mixed year/sex"):
        build_report([a, b], year=2023, sex="total", snapshot_dirs=[SNAP17])
