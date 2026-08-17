"""C-uc5-04 / AC-5.2 / invariant P2: the share vector is identical across
any rebase/F path.

Shares are integer pairs (gons_i, G) — the tests assert bit-identity of the
whole vector across long, extreme, and divergent-then-converging rebase
paths, plus the mortality-neutrality corollary (DECISIONS #4): a down-rebase
shrinks every balance by the same factor and no share grows.
"""

from __future__ import annotations

import random
from decimal import Decimal

from tly.gons import GonsLedger, display_balances

D = Decimal
S0 = D("362412641743.4670")


def _populated() -> GonsLedger:
    lg = GonsLedger(S0)
    lg.transfer_gons("GENESIS", "alice", 3 * 10**29)
    lg.transfer_gons("GENESIS", "bob", 10**29 + 7)
    lg.transfer_gons("GENESIS", "carol", 12345678901234567890)
    return lg


def _share_vector(lg: GonsLedger) -> dict[str, tuple[int, int]]:
    return {w: lg.share(w) for w in lg.wallets()}


def test_p2_share_invariance():
    """Named per RP Part X: 200 seeded rebases spanning 12 orders of
    magnitude; the share vector is bit-identical throughout."""
    lg = _populated()
    original = _share_vector(lg)
    rng = random.Random(20260817)
    for _ in range(200):
        factor = D(str(rng.uniform(0.5, 2.0))).quantize(D("0.000001"))
        lg.rebase(lg.m * factor)
        assert _share_vector(lg) == original  # after EVERY rebase
    lg.rebase(D("0.000000001"))
    assert _share_vector(lg) == original
    lg.rebase(S0 * D("1e12"))
    assert _share_vector(lg) == original


def test_p2_path_independence():
    """Two ledgers, same transfers, wildly different rebase paths ending at
    the same M: identical share vectors AND identical display balances."""
    a, b = _populated(), _populated()
    for factor in ("1.5", "0.25", "3.7", "0.9"):
        a.rebase(a.m * D(factor))
    b.rebase(b.m * D("0.001"))
    b.rebase(b.m * D("1662.75"))  # arbitrary detour
    final_m = S0 * D("1.2345")
    a.rebase(final_m)
    b.rebase(final_m)
    assert _share_vector(a) == _share_vector(b)
    assert display_balances(a) == display_balances(b)


def test_p2_mortality_neutrality_corollary():
    """DECISIONS #4: a mass-death down-rebase shrinks every balance
    pro-rata; nobody's share grows from a shock."""
    lg = _populated()
    before_shares = _share_vector(lg)
    before_display = display_balances(lg)
    lg.rebase(lg.m * D("0.9991"))  # COVID-scale burn epoch
    after_shares = _share_vector(lg)
    after_display = display_balances(lg)
    assert after_shares == before_shares  # d(share)/d(deaths) = 0
    for wallet, bal in after_display.items():
        assert bal <= before_display[wallet]  # everyone shrinks (or dust-equal)


def test_p2_only_transfers_change_shares():
    lg = _populated()
    original = _share_vector(lg)
    lg.rebase(lg.m * D("1.1"))
    assert _share_vector(lg) == original
    lg.transfer_gons("alice", "bob", 10**28)  # a transfer DOES change shares
    changed = _share_vector(lg)
    assert changed != original
    assert changed["alice"][0] == original["alice"][0] - 10**28
    assert changed["bob"][0] == original["bob"][0] + 10**28
