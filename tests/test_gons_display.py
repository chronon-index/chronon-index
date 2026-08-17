"""C-uc5-02 / AC-5.1: E11 display layer — Σ displayed == display supply, exactly."""

from __future__ import annotations

from decimal import Decimal

import pytest

from tly.gons import (
    DISPLAY_QUANTUM,
    GonsError,
    GonsLedger,
    allocate_by_integer_weights,
    display_balances,
)

D = Decimal
S0 = D("362412641743.4670")


def test_allocator_exact_conservation_adversarial():
    """Three equal weights over a non-divisible total: naive rounding loses
    or gains a quantum; largest-remainder cannot."""
    parts = allocate_by_integer_weights(D("100"), {"a": 1, "b": 1, "c": 1}, D("1"))
    assert sum(parts.values()) == D("100")
    assert sorted(parts.values()) == [D("33"), D("33"), D("34")]
    # deterministic tie-break by key: equal remainders -> earliest keys win
    parts2 = allocate_by_integer_weights(D("2"), {"x": 1, "y": 1, "z": 1}, D("1"))
    assert parts2 == {"x": D("1"), "y": D("1"), "z": D("0")}


def test_allocator_huge_weight_skew():
    """A whale and dust wallets: conservation still exact."""
    weights = {"whale": 10**30 - 5, "d1": 1, "d2": 1, "d3": 1, "d4": 1, "d5": 1}
    parts = allocate_by_integer_weights(D("362412641743.467000000"), weights, D("0.000000001"))
    assert sum(parts.values()) == D("362412641743.467000000")
    assert parts["whale"] > D("362412641743")  # nearly everything
    assert all(parts[f"d{i}"] >= 0 for i in range(1, 6))


def test_allocator_rejects_bad_inputs():
    with pytest.raises(GonsError, match="non-empty"):
        allocate_by_integer_weights(D("1"), {}, D("1"))
    with pytest.raises(GonsError, match="non-negative"):
        allocate_by_integer_weights(D("1"), {"a": -1, "b": 2}, D("1"))
    with pytest.raises(GonsError, match="not a multiple"):
        allocate_by_integer_weights(D("1.5"), {"a": 1}, D("1"))


def test_display_balances_sum_exactly():
    lg = GonsLedger(S0)
    lg.transfer_gons("GENESIS", "alice", 3 * 10**29)
    lg.transfer_gons("GENESIS", "bob", 10**29 + 7)  # awkward share on purpose
    lg.transfer_gons("GENESIS", "carol", 12345678901234567890)
    display = display_balances(lg)
    display_supply = (lg.m // DISPLAY_QUANTUM) * DISPLAY_QUANTUM
    assert sum(display.values()) == display_supply  # exact
    assert set(display) == set(lg.wallets())


def test_display_tracks_rebase():
    lg = GonsLedger(S0)
    lg.transfer_gons("GENESIS", "alice", 3 * 10**29)  # 30% share
    before = display_balances(lg)["alice"]
    lg.rebase(S0 * D("2"))
    after = display_balances(lg)["alice"]
    assert after == before * 2  # display follows M through F, shares fixed
    assert sum(display_balances(lg).values()) == (lg.m // DISPLAY_QUANTUM) * DISPLAY_QUANTUM


def test_display_supply_floor_is_stated_not_hidden():
    """M with a sub-quantum tail: the tail is undisplayable by definition;
    the displayed sum equals the floored display supply, never M rounded up."""
    lg = GonsLedger(D("100.0000000005"))  # half a nano-token tail
    display = display_balances(lg)
    assert sum(display.values()) == D("100.000000000")
    assert sum(display.values()) < lg.m
