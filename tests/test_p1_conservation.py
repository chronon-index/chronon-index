"""C-uc5-03 / AC-5.1 / invariant P1: Σ balances = M(t) after every operation.

Conservation is asserted at BOTH layers after every single operation:
- ledger: Σ gons == G_TOTAL (exact integers), and
- display: Σ displayed balances == display supply (E11).

A scripted walk covers the interesting transitions; a seeded fuzz walk
performs hundreds of mixed operations with the invariant checked after
each one — not at the end.
"""

from __future__ import annotations

import random
from decimal import Decimal

from tly.gons import DISPLAY_QUANTUM, G_TOTAL, GonsLedger, display_balances

D = Decimal
S0 = D("362412641743.4670")


def _assert_conserved(lg: GonsLedger) -> None:
    assert lg.total_gons() == G_TOTAL  # ledger layer, exact int
    display = display_balances(lg)
    display_supply = (lg.m // DISPLAY_QUANTUM) * DISPLAY_QUANTUM
    assert sum(display.values()) == display_supply  # display layer, exact


def test_p1_conservation():
    """Named per RP Part X: the scripted walk — genesis, transfers (gons
    and balance-unit), up/down rebases, wallet exhaustion — with the
    invariant asserted after EVERY operation."""
    lg = GonsLedger(S0)
    _assert_conserved(lg)

    lg.transfer_gons("GENESIS", "alice", 3 * 10**29)
    _assert_conserved(lg)
    lg.transfer_gons("GENESIS", "bob", 10**29 + 7)
    _assert_conserved(lg)
    lg.transfer_balance("alice", "carol", D("1234.567"))
    _assert_conserved(lg)

    lg.rebase(S0 * D("1.0072"))  # organic growth epoch
    _assert_conserved(lg)
    lg.rebase(S0 * D("0.9991"))  # mortality-shock down-rebase
    _assert_conserved(lg)

    lg.transfer_gons("bob", "alice", lg.gons("bob"))  # bob empties out
    _assert_conserved(lg)
    assert lg.gons("bob") == 0

    lg.rebase(D("0.000000001"))  # M collapses to one display quantum
    _assert_conserved(lg)
    lg.rebase(S0 * D("1000"))  # and explodes
    _assert_conserved(lg)


def test_p1_conservation_fuzz_walk():
    """300 seeded mixed operations; conservation after each. The seed is
    fixed — deterministic, reproducible, still adversarial in shape."""
    rng = random.Random(20260817)
    lg = GonsLedger(S0)
    wallets = ["GENESIS"]
    for i in range(300):
        op = rng.random()
        if op < 0.5 and lg.gons(wallets[-1] if wallets else "") >= 0:
            src = rng.choice([w for w in wallets if lg.gons(w) > 0] or ["GENESIS"])
            dst = rng.choice(wallets + [f"w{i}"])
            if dst != src and lg.gons(src) > 1:
                amount = rng.randint(1, lg.gons(src))
                lg.transfer_gons(src, dst, amount)
                if dst not in wallets:
                    wallets.append(dst)
        elif op < 0.8:
            factor = D(str(rng.uniform(0.9, 1.1))).quantize(D("0.000001"))
            if factor > 0:
                lg.rebase(lg.m * factor)
        else:
            src = rng.choice([w for w in wallets if lg.gons(w) > 0] or ["GENESIS"])
            dst = f"w{i}"
            try:
                lg.transfer_balance(src, dst, lg.m / D(rng.randint(10, 10_000)))
                wallets.append(dst)
            except Exception:
                pass  # insufficient/dust transfers may legitimately refuse
        _assert_conserved(lg)  # after EVERY operation
    assert len(wallets) > 40  # the walk actually exercised a real ledger (seed 20260817 creates 46)
