"""B-uc2-08 / AC-2.1 / invariant P6: weekly prints reconcile to the annual
E5 identity — under the registered p6_closure policy, EXACTLY."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from tly.decomposition import exact_decomposition
from tly.methodology import current_policies
from tly.prints import validate_epoch
from tly.stock import compute_location_stock
from tly.weekly import allocate_equal, monday_epochs, schedule_annual_flow
from tly.wmd import parse_wmd  # noqa: F401  (feed import kept close to the chain)
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

D = Decimal
Q = D("0.000001")


def _world_ds() -> Decimal:
    """Real annual-scale dS: World 2019→2023 from the committed fixtures,
    quantized to the scheduling quantum (an input convention, not a fudge)."""
    pop = parse_population_single_age(POP_FIX, {2019, 2023}, locations={"World"})
    lt = parse_life_table_ex(LT_FIX, {2019, 2023}, locations={"World"})
    stocks = {
        y: compute_location_stock(
            population_by_age(pop, "World", y),
            ex_anchors(lt, "World", y),
            location="World",
            year=y,
            sex="total",
        )
        for y in (2019, 2023)
    }
    return exact_decomposition(stocks[2019], stocks[2023]).ds.quantize(Q)


def test_p6_identity_closure():
    """Named per RP Part X: the year's weekly increments sum to the annual
    identity delta EXACTLY (p6_closure = exact-0) — for a 52-Monday year,
    a 53-Monday year, and a real-data dS with a long fractional tail."""
    assert current_policies()["p6_closure"].startswith("exact-0")
    ds = _world_ds()
    for year in (2026, 2024):  # 2026: 52 Mondays; 2024: 53 Mondays
        schedule = schedule_annual_flow(ds, year)
        assert sum(schedule.values(), D(0)) == ds  # exact, no tolerance
        for epoch in schedule:
            validate_epoch(epoch)  # every stamp is a valid Monday epoch


def test_monday_calendar():
    assert len(monday_epochs(2026)) == 52
    assert len(monday_epochs(2024)) == 53  # Jan 1 and Dec 30 are Mondays
    assert monday_epochs(2026)[0] == "2026-01-05T12:00:00+00:00"
    assert monday_epochs(2026)[-1] == "2026-12-28T12:00:00+00:00"


def test_allocate_equal_exact_conservation():
    parts = allocate_equal(D("100.000007"), 52)
    assert sum(parts, D(0)) == D("100.000007")
    assert max(parts) - min(parts) <= Q  # near-equal
    neg = allocate_equal(D("-3.000005"), 7)
    assert sum(neg, D(0)) == D("-3.000005")
    assert all(p < 0 for p in neg)


def test_allocate_equal_rejects_bad_inputs():
    with pytest.raises(ValueError, match="parts must be positive"):
        allocate_equal(D("1"), 0)
    with pytest.raises(ValueError, match="not a multiple of quantum"):
        allocate_equal(D("1.0000005"), 3)
