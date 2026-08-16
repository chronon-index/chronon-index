"""B-uc1-06: WPP life-table e(x) parser tests (abridged + complete fixtures).

Also pins the recorded WPP-vs-WHO e0 discrepancy (manifest note, RP#VI r4):
WHO GHO stays triangulation-only; the two sources must remain distinct
facts, never averaged.
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from tly.parsers import parse_gho_life_tables
from tly.wpp import (
    ABRIDGED_ANCHOR_AGES,
    COMPLETE_ANCHOR_AGES,
    ex_anchors,
    parse_life_table_ex,
)

REPO = Path(__file__).resolve().parent.parent
SNAP17 = REPO / "data" / "snapshots" / "2026-08-17"
SNAP16 = REPO / "data" / "snapshots" / "2026-08-16"
ABRIDGED = SNAP17 / "fixtures" / "wpp_lt_abridged_fixture.csv.gz"
COMPLETE = SNAP17 / "fixtures" / "wpp_lt_complete_fixture.csv.gz"


def test_abridged_fixture_shape_and_sexes():
    cells = parse_life_table_ex(ABRIDGED, {2019, 2021, 2023})
    # 3 locations x 3 years x 22 anchors x 3 sexes
    assert len(cells) == 3 * 3 * 22 * 3
    assert {c.sex for c in cells} == {"total", "male", "female"}
    anchors = ex_anchors(cells, "World", 2019)
    assert tuple(sorted(anchors)) == ABRIDGED_ANCHOR_AGES


def test_complete_fixture_shape_total_only():
    cells = parse_life_table_ex(COMPLETE, {2019, 2021, 2023})
    # 3 locations x 3 years x 101 ages x 1 sex (complete file is both-sexes)
    assert len(cells) == 3 * 3 * 101
    assert {c.sex for c in cells} == {"total"}
    anchors = ex_anchors(cells, "Japan", 2023)
    assert tuple(sorted(anchors)) == COMPLETE_ANCHOR_AGES


def test_world_e0_matches_recorded_values():
    """The manifest-recorded WPP world e0 values, as parsed facts."""
    cells = parse_life_table_ex(ABRIDGED, {2019, 2021, 2023}, locations={"World"})
    assert ex_anchors(cells, "World", 2019)[0] == Decimal("72.6093")
    assert ex_anchors(cells, "World", 2021)[0] == Decimal("70.865")
    assert ex_anchors(cells, "World", 2023)[0] == Decimal("73.1694")


def test_abridged_and_complete_agree_at_shared_anchors():
    """Same WPP surface at two granularities: e(x) must agree at shared
    ages for both-sexes (they are published from one underlying table)."""
    ab = ex_anchors(parse_life_table_ex(ABRIDGED, {2023}, locations={"World"}), "World", 2023)
    co = ex_anchors(parse_life_table_ex(COMPLETE, {2023}, locations={"World"}), "World", 2023)
    for age in ABRIDGED_ANCHOR_AGES:
        assert ab[age] == co[age], f"abridged/complete e({age}) disagree"


def test_wpp_who_discrepancy_is_preserved_not_averaged():
    """RP#VI rule 4 as a test: WPP and WHO world e0 are DIFFERENT facts.
    If someone 'fixes' one source to match the other, this fails."""
    wpp = ex_anchors(
        parse_life_table_ex(ABRIDGED, {2019, 2021}, locations={"World"}), "World", 2019
    )
    who = parse_gho_life_tables(SNAP16, (2019, 2021))
    assert wpp[0] == Decimal("72.6093")
    assert who[2019][0] == Decimal("73.123374469")
    assert wpp[0] != who[2019][0]


def test_partial_table_rejected():
    cells = parse_life_table_ex(ABRIDGED, {2019}, locations={"World"})
    trimmed = [c for c in cells if c.age != 50]
    with pytest.raises(ValueError, match="unexpected anchor set"):
        ex_anchors(trimmed, "World", 2019)
    with pytest.raises(ValueError, match="no life-table cells"):
        ex_anchors(cells, "France", 2019)
