"""Weekly epoch calendar + annual-flow scheduling (SPEC#2; B-uc2-08).

Epochs are the actual Mondays 12:00 UTC of a calendar year — 52 or 53
depending on the year; the calendar never pretends otherwise. Annual
identity flows (mint, spend, drift, burn) are split across the year's
epochs by equal division with largest-remainder quantum distribution
(RP Part IX E11), so the weekly increments sum to the annual flow EXACTLY —
the registered ``p6_closure`` policy is "exact-0", and the P6 invariant
test asserts equality with no tolerance.
"""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

from tly.guard import assert_decimal

LIFE_YEAR_QUANTUM = Decimal("0.000001")  # micro-life-year scheduling quantum


def monday_epochs(year: int) -> list[str]:
    """All Monday-12:00-UTC epoch stamps of ``year`` (52 or 53)."""
    d = date(year, 1, 1)
    d += timedelta(days=(0 - d.weekday()) % 7)  # first Monday
    epochs = []
    while d.year == year:
        epochs.append(f"{d.isoformat()}T12:00:00+00:00")
        d += timedelta(days=7)
    return epochs


def allocate_equal(
    total: Decimal, parts: int, quantum: Decimal = LIFE_YEAR_QUANTUM
) -> list[Decimal]:
    """Split ``total`` into ``parts`` near-equal quantum-multiples that sum
    to ``total`` exactly (E11, equal-weight case).

    Works for signed totals; the first ``k`` parts carry one extra quantum
    (deterministic — no fractional-remainder comparison needed since all
    weights are equal).
    """
    assert_decimal(total, "total")
    if parts <= 0:
        raise ValueError("parts must be positive")
    if total % quantum != 0:
        raise ValueError(f"total {total} is not a multiple of quantum {quantum}")
    total_quanta = int(total / quantum)
    base, extra = divmod(abs(total_quanta), parts)
    sign = 1 if total_quanta >= 0 else -1
    shares = [sign * (base + (1 if i < extra else 0)) * quantum for i in range(parts)]
    return shares


def schedule_annual_flow(total: Decimal, year: int) -> dict[str, Decimal]:
    """{epoch_stamp: weekly increment} over the year's actual Mondays;
    Σ increments == total exactly (p6_closure = exact-0)."""
    epochs = monday_epochs(year)
    return dict(zip(epochs, allocate_equal(total, len(epochs))))
