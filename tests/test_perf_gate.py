"""C-uc5-08 / AC-5.4 / RALPH §7 Phase C gate: 10,000 wallets × 600 epochs
in under 5 seconds, and rebase cost O(1) in wallet count."""

from __future__ import annotations

import random
import time
from decimal import Decimal

from tly.gons import G_TOTAL, GonsLedger

D = Decimal
S0 = D("362412641743.4670")


def _ledger_with_wallets(n: int) -> GonsLedger:
    lg = GonsLedger(S0)
    rng = random.Random(20260817)
    share = G_TOTAL // (n * 2)  # leave GENESIS holding the remainder
    for i in range(n):
        lg.transfer_gons("GENESIS", f"w{i}", share + rng.randint(0, 1000))
    return lg


def test_perf_gate_10k_wallets_600_epochs():
    """The RALPH Phase C gate, verbatim: full simulation — 600 epochs, each
    one rebase plus a handful of transfers across a 10,000-wallet ledger —
    completes in < 5 s wall clock."""
    lg = _ledger_with_wallets(10_000)
    rng = random.Random(1)
    start = time.perf_counter()
    for epoch in range(600):
        lg.rebase(lg.m * D("1.000138"))  # weekly organic epoch
        for _ in range(5):
            src = f"w{rng.randrange(10_000)}"
            dst = f"w{rng.randrange(10_000)}"
            if src != dst and lg.gons(src) > 1:
                lg.transfer_gons(src, dst, lg.gons(src) // 2)
    elapsed = time.perf_counter() - start
    assert lg.total_gons() == G_TOTAL  # still conserved after the run
    assert elapsed < 5.0, f"gate failed: {elapsed:.2f}s for 10k x 600"


def test_rebase_is_o1_in_wallet_count():
    """1,000 rebases on a 100-wallet ledger vs a 10,000-wallet ledger:
    per-rebase cost must not scale with wallets (100x wallets, < 3x time —
    generous noise budget on a property that is architecturally exact)."""
    small = _ledger_with_wallets(100)
    large = _ledger_with_wallets(10_000)

    def time_rebases(lg: GonsLedger) -> float:
        start = time.perf_counter()
        for i in range(1_000):
            lg.rebase(lg.m * (D("1.0001") if i % 2 == 0 else D("0.9999")))
        return time.perf_counter() - start

    t_small = time_rebases(small)
    t_large = time_rebases(large)
    assert t_large < t_small * 3 + 0.05, (
        f"rebase scaling with wallet count: {t_small:.4f}s vs {t_large:.4f}s"
    )
