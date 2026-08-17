"""C-uc5-05 / AC-5.5 / DEC#3: shares change only by transfer, and by
exactly the transferred amount — the log is the complete causal record."""

from __future__ import annotations

import random
from decimal import Decimal

from tly.gons import GonsLedger

D = Decimal
S0 = D("362412641743.4670")


def _shares(lg: GonsLedger) -> dict[str, tuple[int, int]]:
    return {w: lg.share(w) for w in lg.wallets()}


def test_transfer_only_share_change():
    """Named per the backlog. Leg 1: an epoch sequence with ZERO transfers
    leaves the share vector bit-identical and the log empty. Leg 2: with
    transfers, every wallet's gons delta equals the NET of its logged
    transfers, exactly — no other cause of share change exists."""
    lg = GonsLedger(S0)
    lg.transfer_gons("GENESIS", "alice", 3 * 10**29)
    lg.transfer_gons("GENESIS", "bob", 10**29)
    baseline_log_len = len(lg.transfer_log())
    before = _shares(lg)

    rng = random.Random(7)
    for _ in range(50):  # 50 epochs of pure rebasing — no transfers
        lg.rebase(lg.m * D(str(rng.uniform(0.95, 1.05))).quantize(D("0.0001")))
    assert _shares(lg) == before
    assert len(lg.transfer_log()) == baseline_log_len  # nothing logged

    gons_before = {w: lg.gons(w) for w in list(lg.wallets()) + ["carol"]}
    lg.transfer_gons("alice", "carol", 10**28)
    lg.rebase(lg.m * D("1.01"))  # interleave a rebase
    lg.transfer_gons("bob", "carol", 5 * 10**27)
    lg.transfer_gons("carol", "alice", 10**27)

    net: dict[str, int] = {w: 0 for w in gons_before}
    for src, dst, amount in lg.transfer_log()[baseline_log_len:]:
        net[src] -= amount
        net[dst] += amount
    for wallet, before_g in gons_before.items():
        assert lg.gons(wallet) == before_g + net[wallet], wallet


def test_log_is_append_only_and_complete():
    lg = GonsLedger(S0)
    lg.transfer_gons("GENESIS", "a", 10**29)
    log1 = lg.transfer_log()
    lg.transfer_gons("a", "b", 10**28)
    log2 = lg.transfer_log()
    assert log2[: len(log1)] == log1  # strictly extends
    assert log2[-1] == ("a", "b", 10**28)
    # the log is a copy — mutating the returned tuple's source is impossible,
    # and re-reading yields the same history
    assert lg.transfer_log() == log2


def test_balance_unit_transfers_appear_in_log():
    lg = GonsLedger(S0)
    lg.transfer_gons("GENESIS", "a", 10**29)
    moved = lg.transfer_balance("a", "b", D("1000"))
    assert lg.transfer_log()[-1] == ("a", "b", moved)
