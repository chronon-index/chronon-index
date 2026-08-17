"""Gons rebase engine core (SPEC#5; RP Part IX E10; RP M4; C-uc5-01).

The Ampleforth pattern, exact by construction:

- Every wallet holds GONS — integers, fixed at transfer time only. The
  total gons supply G is constant forever.
- The visible balance is ``balance_i = gons_i / F`` where F is ONE global
  factor. A rebase to a new money supply M sets ``F = G / M`` — equivalently
  multiplies F by (M_old / M_new) — touching no wallet. O(1), exact.
- Shares ``s_i = gons_i / G`` are integers over a constant integer: they
  cannot change under ANY rebase path (invariant P2), and Σ gons == G after
  every operation (invariant P1 at the ledger layer) because transfers are
  integer moves.

PRECISION / OVERFLOW ANALYSIS (documented per the task):

- Gons are Python ints: arbitrary precision, no overflow, no rounding —
  conservation and share invariance are exact integer facts, independent of
  any Decimal context.
- G = 10**30 gons. With S₀ ≈ 3.6e11 life-years and κ = 1 token/life-year,
  M ≈ 3.6e11, so F = G/M ≈ 2.8e18 — comfortably inside Decimal prec 34
  (34 significant digits); F is stored as an exact fraction (G, M) and
  only realized as a Decimal division at display time.
- Display balances gons/F round at prec 34 per wallet, so Σ display
  balances can differ from M by wallet-count × ULP. The DISPLAY layer
  therefore uses largest-remainder allocation (E11, C-uc5-02) so displayed
  balances sum to M exactly; the ledger itself never rounds.
- Smallest representable share: 1 gon = 1e-30 of supply ≈ 3.6e-19 tokens
  at genesis M — dust far below any economic quantum.
"""

from __future__ import annotations

from decimal import Decimal

from tly.guard import assert_decimal

G_TOTAL = 10**30  # constant forever; exact int


class GonsError(ValueError):
    """Illegal ledger operation."""


class GonsLedger:
    """Integer-gons ledger with a global rebase factor."""

    def __init__(self, initial_m: Decimal):
        assert_decimal(initial_m, "initial_m")
        if initial_m <= 0:
            raise GonsError("money supply must be positive")
        self._gons: dict[str, int] = {"GENESIS": G_TOTAL}
        self._m = initial_m

    # -- supply ------------------------------------------------------------
    @property
    def m(self) -> Decimal:
        """The money supply M(t) — the ONLY rebase-adjustable quantity."""
        return self._m

    @property
    def f(self) -> Decimal:
        """Global factor F = G / M, realized as Decimal at read time."""
        return Decimal(G_TOTAL) / self._m

    def rebase(self, new_m: Decimal) -> Decimal:
        """Set M (hence F) — touches no wallet; returns the F multiplier
        applied, F_new/F_old = M_old/M_new."""
        assert_decimal(new_m, "new_m")
        if new_m <= 0:
            raise GonsError("money supply must be positive")
        multiplier = self._m / new_m
        self._m = new_m
        return multiplier

    # -- wallets -----------------------------------------------------------
    def gons(self, wallet: str) -> int:
        return self._gons.get(wallet, 0)

    def wallets(self) -> dict[str, int]:
        return dict(self._gons)

    def total_gons(self) -> int:
        return sum(self._gons.values())

    def share(self, wallet: str) -> tuple[int, int]:
        """Exact share as an integer pair (gons_i, G) — no division, no
        rounding; the P2 quantity."""
        return (self.gons(wallet), G_TOTAL)

    def transfer_gons(self, src: str, dst: str, amount_gons: int) -> None:
        """Move integer gons. The only operation that changes shares."""
        if not isinstance(amount_gons, int) or isinstance(amount_gons, bool):
            raise GonsError("gons amounts are integers")
        if amount_gons <= 0:
            raise GonsError("transfer amount must be positive")
        if self.gons(src) < amount_gons:
            raise GonsError(f"insufficient gons in {src!r}")
        self._gons[src] -= amount_gons
        self._gons[dst] = self.gons(dst) + amount_gons
        if self._gons[src] == 0:
            del self._gons[src]

    def transfer_balance(self, src: str, dst: str, amount_balance: Decimal) -> int:
        """Transfer specified in balance units; converts to gons by
        truncation toward zero (the Ampleforth convention) and moves that
        exact integer. Returns the gons moved."""
        assert_decimal(amount_balance, "amount_balance")
        amount_gons = int(amount_balance * Decimal(G_TOTAL) / self._m)
        if amount_gons <= 0:
            raise GonsError("amount below one gon at current F")
        self.transfer_gons(src, dst, amount_gons)
        return amount_gons

    # -- display -----------------------------------------------------------
    def balance(self, wallet: str) -> Decimal:
        """Display balance gons/F (rounds at prec 34 — see the analysis;
        exact-sum display goes through the E11 layer, C-uc5-02)."""
        return Decimal(self.gons(wallet)) * self._m / Decimal(G_TOTAL)
