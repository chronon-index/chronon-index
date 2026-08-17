"""C-uc5-01: gons engine core — integer exactness, O(1) rebase semantics."""

from __future__ import annotations

from decimal import Decimal

import pytest

from tly.gons import G_TOTAL, GonsError, GonsLedger

D = Decimal
S0 = D("362412641743.4670")  # genesis M = kappa * S0, kappa = 1


def _ledger() -> GonsLedger:
    lg = GonsLedger(S0)
    lg.transfer_gons("GENESIS", "alice", 3 * 10**29)
    lg.transfer_gons("GENESIS", "bob", 10**29)
    return lg


def test_genesis_and_conservation():
    lg = _ledger()
    assert lg.total_gons() == G_TOTAL  # exact int, always
    assert lg.gons("alice") == 3 * 10**29
    assert lg.share("alice") == (3 * 10**29, G_TOTAL)


def test_rebase_touches_no_wallet():
    lg = _ledger()
    before = lg.wallets()
    mult = lg.rebase(S0 * D("2"))
    assert lg.wallets() == before  # not a single gon moved
    assert mult == D("0.5")  # F halves when M doubles
    lg.rebase(S0 * D("0.9"))
    assert lg.wallets() == before
    assert lg.total_gons() == G_TOTAL


def test_shares_invariant_under_rebase_path():
    lg = _ledger()
    s_alice = lg.share("alice")
    for m in (S0 * D("1.5"), S0 * D("0.3"), S0, S0 * D("42")):
        lg.rebase(m)
    assert lg.share("alice") == s_alice  # integer pair, bit-identical


def test_balance_scales_with_m():
    lg = _ledger()
    b1 = lg.balance("alice")
    lg.rebase(S0 * D("2"))
    assert lg.balance("alice") == b1 * D("2")  # 30% of M, M doubled


def test_transfer_balance_truncates_to_gons():
    lg = _ledger()
    moved = lg.transfer_balance("alice", "carol", D("1000"))
    assert isinstance(moved, int)
    assert lg.gons("carol") == moved
    assert lg.total_gons() == G_TOTAL  # conservation through conversion
    # truncation: carol's balance is <= requested, within one gon's value
    assert lg.balance("carol") <= D("1000")
    one_gon_value = lg.m / D(G_TOTAL)
    assert D("1000") - lg.balance("carol") < one_gon_value * 2


def test_illegal_operations_raise():
    lg = _ledger()
    with pytest.raises(GonsError, match="insufficient"):
        lg.transfer_gons("bob", "alice", G_TOTAL)
    with pytest.raises(GonsError, match="integers"):
        lg.transfer_gons("alice", "bob", D("5"))  # type: ignore[arg-type]
    with pytest.raises(GonsError, match="positive"):
        lg.transfer_gons("alice", "bob", 0)
    with pytest.raises(GonsError, match="must be positive"):
        lg.rebase(D("0"))
    with pytest.raises(GonsError, match="below one gon"):
        lg.transfer_balance("alice", "bob", D("1e-25"))


def test_precision_analysis_bounds_hold():
    """The documented analysis: F at genesis fits far inside prec 34, and
    one gon is economic dust."""
    lg = GonsLedger(S0)
    assert D("1e18") < lg.f < D("1e19")
    one_gon_tokens = lg.m / D(G_TOTAL)
    assert one_gon_tokens < D("1e-18")
