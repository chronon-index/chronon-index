"""A-12 unit tests: tly.parsers against the committed 2026-08-16 snapshot.

Cross-checks parsed values against seed/results_v0.json (the golden anchor)
so the package parsers provably read the snapshot the same way the frozen
seed script does.
"""

from __future__ import annotations

import json
from decimal import Decimal, getcontext
from pathlib import Path

import pytest

from tly import numeric
from tly.parsers import (
    GHO_AGE_ANCHORS,
    parse_births,
    parse_gho_life_tables,
    parse_population_bands,
    read_manifest,
)

REPO = Path(__file__).resolve().parent.parent
SNAPSHOT = REPO / "data" / "snapshots" / "2026-08-16"
GOLDEN = json.loads((REPO / "seed" / "results_v0.json").read_text(encoding="utf-8"))


def test_decimal_context_is_project_standard():
    ctx = getcontext()
    assert ctx.prec == numeric.PRECISION == 34
    assert ctx.rounding == numeric.ROUNDING == "ROUND_HALF_EVEN"


def test_gho_anchor_map_shape():
    # 19 abridged anchors: 0, 1, 5, 10, ..., 80, 85
    assert sorted(GHO_AGE_ANCHORS.values()) == [0, 1] + list(range(5, 90, 5))


def test_parse_gho_life_tables_matches_golden():
    tables = parse_gho_life_tables(SNAPSHOT, (2019, 2021))
    assert set(tables) == {2019, 2021}
    for year in (2019, 2021):
        assert sorted(tables[year]) == sorted(GHO_AGE_ANCHORS.values())
        for e in tables[year].values():
            assert isinstance(e, Decimal)
    assert str(tables[2019][0]) == GOLDEN["achieved"]["e0_2019"]
    assert str(tables[2021][0]) == GOLDEN["achieved"]["e0_2021"]


def test_parse_gho_rejects_incomplete_table():
    with pytest.raises(ValueError, match="incomplete GHO life table"):
        parse_gho_life_tables(SNAPSHOT, (2019, 2020))  # 2020 not in snapshot


def test_parse_population_bands_matches_golden():
    bands = parse_population_bands(SNAPSHOT, 2023)
    assert len(bands) == 21  # 0-4 ... 95-99, 100+
    total = sum(b.count for b in bands)
    assert str(total) == GOLDEN["achieved"]["N_persons"]
    by_label = {b.label: b for b in bands}
    assert by_label["0-4"].midpoint == Decimal("2.5")
    assert by_label["95-99"].midpoint == Decimal("97.5")
    assert by_label["100+"].midpoint == Decimal("102.5")
    for b in bands:
        assert isinstance(b.count, Decimal)
    # golden band_detail rows are (label, mid, N, e_mid, term)
    golden_rows = {row[0]: row for row in GOLDEN["band_detail"]["2019"]}
    for b in bands:
        assert str(b.midpoint) == golden_rows[b.label][1]
        assert str(b.count) == golden_rows[b.label][2]


def test_parse_population_missing_year_raises():
    with pytest.raises(ValueError, match="no OWID_WRL row for 1800"):
        parse_population_bands(SNAPSHOT, 1800)


def test_parse_births_matches_golden():
    births = parse_births(SNAPSHOT, 2023)
    assert isinstance(births, Decimal)
    assert str(births) == GOLDEN["achieved"]["births_2023"]


def test_parse_births_absent_year_is_none():
    assert parse_births(SNAPSHOT, 1800) is None


def test_manifest_covers_all_parsed_files():
    manifest = read_manifest(SNAPSHOT)
    for name in (
        "gho_ex_global_btsx_2019_2021.json",
        "owid_population_5yr_world.csv",
        "owid_births_deaths_world.csv",
    ):
        entry = manifest["files"][name]
        assert entry["sha256"] and entry["source_url"] and entry["retrieved_utc"]
