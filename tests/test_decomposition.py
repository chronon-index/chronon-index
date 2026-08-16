"""B-uc1-10: E4/E5 decomposition — exact split + identity form with exposed residual.

Pinned values computed from the committed fixtures (World/Japan 2019→2023,
WPP single-age tables); the synthetic-input tests prove the arithmetic
independently of any data source.
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from tly.decomposition import exact_decomposition, identity_decomposition
from tly.guard import FloatContaminationError
from tly.stock import LocationStock, compute_location_stock
from tly.wpp import (
    ex_anchors,
    parse_life_table_ex,
    parse_population_single_age,
    population_by_age,
)

REPO = Path(__file__).resolve().parent.parent
SNAP17 = REPO / "data" / "snapshots" / "2026-08-17"
POP_FIX = SNAP17 / "fixtures" / "wpp_pop_single_age_fixture.csv.gz"
LT_FIX = SNAP17 / "fixtures" / "wpp_lt_complete_fixture.csv.gz"

ULP_BOUND = Decimal("1e-15")  # life-years; see decomposition module docstring


def _stock(location: str, year: int) -> LocationStock:
    pop = parse_population_single_age(POP_FIX, {year}, locations={location})
    lt = parse_life_table_ex(LT_FIX, {year}, locations={location})
    return compute_location_stock(
        population_by_age(pop, location, year),
        ex_anchors(lt, location, year),
        location=location,
        year=year,
        sex="total",
    )


def _synthetic(location: str, year: int, s: str, n: str) -> LocationStock:
    return LocationStock(
        location=location,
        iso3=None,
        year=year,
        sex="total",
        s_life_years=Decimal(s),
        n_persons=Decimal(n),
    )


def test_exact_decomposition_synthetic_closes_exactly():
    """With division-free Ē (N chosen to divide S), closure is literally 0."""
    a = _synthetic("X", 2000, "4000", "100")  # Ē = 40 exactly
    b = _synthetic("X", 2001, "4515", "105")  # Ē = 43 exactly
    d = exact_decomposition(a, b)
    assert d.ds == Decimal("515")
    assert d.population_term == Decimal("200")  # 40 · 5
    assert d.revision_term == Decimal("300")  # 100 · 3
    assert d.cross_term == Decimal("15")  # 5 · 3
    assert d.closure == 0


def test_exact_decomposition_fixture_world_pinned():
    d = exact_decomposition(_stock("World", 2019), _stock("World", 2023))
    B = Decimal(10) ** 9
    q = Decimal("0.0001")
    assert str((d.ds / B).quantize(q)) == "9.0602"
    assert str((d.population_term / B).quantize(q)) == "12.7255"
    assert str((d.revision_term / B).quantize(q)) == "-3.5383"
    assert str((d.cross_term / B).quantize(q)) == "-0.1270"
    assert abs(d.closure) < ULP_BOUND


def test_exact_decomposition_fixture_japan_shrinks():
    """Japan 2019→2023: S falls via BOTH terms (population decline and
    COVID-era Ē dip) — a real negative-dS case."""
    d = exact_decomposition(_stock("Japan", 2019), _stock("Japan", 2023))
    assert d.ds < 0
    assert d.population_term < 0
    assert d.revision_term < 0
    assert abs(d.closure) < ULP_BOUND


def test_identity_decomposition_residual_exposed():
    a = _synthetic("X", 2000, "4000", "100")
    b = _synthetic("X", 2001, "4515", "105")
    d = identity_decomposition(a, b, births=Decimal("10"), e0=Decimal("50"))
    assert d.mint == Decimal("500")
    assert d.spend == Decimal("-100")
    assert d.drift == Decimal("300")  # N_t · ΔĒ = 100 · 3
    assert d.burn == 0
    # residual = 515 − (500 − 100 + 300 − 0) = −185; exposed, not hidden
    assert d.residual == Decimal("-185")


def test_identity_decomposition_burn_moves_residual_not_ds():
    a = _synthetic("X", 2000, "4000", "100")
    b = _synthetic("X", 2001, "4515", "105")
    no_burn = identity_decomposition(a, b, births=Decimal("10"), e0=Decimal("50"))
    with_burn = identity_decomposition(
        a, b, births=Decimal("10"), e0=Decimal("50"), burn=Decimal("35")
    )
    assert with_burn.ds == no_burn.ds  # ΔS is data, not convention
    assert with_burn.residual == no_burn.residual + Decimal("35")


def test_identity_decomposition_rejects_floats_and_mixed_locations():
    a = _synthetic("X", 2000, "4000", "100")
    b = _synthetic("Y", 2001, "4515", "105")
    with pytest.raises(ValueError, match="one location"):
        identity_decomposition(a, b, births=Decimal("10"), e0=Decimal("50"))
    c = _synthetic("X", 2001, "4515", "105")
    with pytest.raises(FloatContaminationError):
        identity_decomposition(a, c, births=10.0, e0=Decimal("50"))
