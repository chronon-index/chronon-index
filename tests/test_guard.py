"""B-uc1-01 / AC-1.3: float quarantine on the published path.

The named acceptance test ``test_no_float_in_published_path`` injects
floats at every published-path entry point and asserts rejection.
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from tly.estimator import compute_stock, e_bar, mint
from tly.guard import FloatContaminationError, assert_decimal, assert_no_floats
from tly.parsers import PopulationBand, parse_gho_life_tables, parse_population_bands

REPO = Path(__file__).resolve().parent.parent
SNAPSHOT = REPO / "data" / "snapshots" / "2026-08-16"

D = Decimal
GOOD_TABLE = {0: D("70"), 1: D("69.5"), 5: D("66"), 85: D("6")}
GOOD_BANDS = [PopulationBand("0-4", D("2.5"), D("1000"))]


def test_no_float_in_published_path():
    """AC-1.3: inject a float at each entry point; every one must raise."""
    stock = compute_stock(GOOD_TABLE, GOOD_BANDS, 2019)  # clean baseline passes

    with pytest.raises(FloatContaminationError, match=r"table\[0\]"):
        compute_stock({0: 70.0, 1: D("69.5"), 5: D("66"), 85: D("6")}, GOOD_BANDS, 2019)
    with pytest.raises(FloatContaminationError, match=r"bands\[0\]\.count"):
        compute_stock(GOOD_TABLE, [PopulationBand("0-4", D("2.5"), 1000.0)], 2019)
    with pytest.raises(FloatContaminationError, match=r"bands\[0\]\.midpoint"):
        compute_stock(GOOD_TABLE, [PopulationBand("0-4", 2.5, D("1000"))], 2019)
    with pytest.raises(FloatContaminationError, match="n_total"):
        e_bar(stock, 8.0e9)
    with pytest.raises(FloatContaminationError, match="births"):
        mint(132110264.0, D("73.1"))
    with pytest.raises(FloatContaminationError, match="e0"):
        mint(D("132110264"), 73.1)


def test_assert_no_floats_recurses_and_names_path():
    assert_no_floats({"a": [D("1"), {"b": D("2")}]})  # clean nested passes
    with pytest.raises(FloatContaminationError, match=r"\$\['a'\]\[1\]\['b'\]"):
        assert_no_floats({"a": [D("1"), {"b": 2.0}]})
    with pytest.raises(FloatContaminationError, match=r"\[key 1.5\]"):
        assert_no_floats({1.5: D("1")})  # float used as a mapping key


def test_assert_no_floats_fails_closed_on_uninspectable():
    class Opaque:
        pass

    with pytest.raises(FloatContaminationError, match="uninspectable"):
        assert_no_floats(Opaque())


def test_assert_decimal_rejects_non_decimal():
    assert assert_decimal(D("1.5"), "x") == D("1.5")
    for bad in (1.5, 1, "1.5", True, None):
        with pytest.raises(FloatContaminationError, match="x must be Decimal"):
            assert_decimal(bad, "x")


def test_real_parsed_snapshot_is_float_free():
    """The actual parsed snapshot passes the quarantine — proof the parsing
    layer (parse_float=Decimal, Decimal(str)) admits no float anywhere."""
    tables = parse_gho_life_tables(SNAPSHOT, (2019, 2021))
    bands = parse_population_bands(SNAPSHOT, 2023)
    assert_no_floats(tables, "tables")
    assert_no_floats(bands, "bands")
