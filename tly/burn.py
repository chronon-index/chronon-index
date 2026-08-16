"""Burn term (SPEC#2 AC-2.6; RP Part IX E4): life-years lost to excess deaths.

burn = Σ over ages of excess_deaths(a) × e(mid(a)) — an excess death at
single age a (i.e. in [a, a+1)) removes the remaining expectancy at the
band midpoint a + 0.5, under the SAME registered midpoint + interpolation
policies as the stock engine. One policy set, both directions of flow.

Age attribution: shock feeds (WMD, UCDP, EM-DAT…) publish totals, not ages;
an age-at-death distribution must be supplied explicitly. Distribution
CHOICES are per-feed versioned assumptions (RP Part II D4 — later tasks);
this module only enforces their arithmetic: weights sum to 1 exactly, and
allocation conserves the total exactly via largest-remainder rounding
(RP Part IX E11) — no life-year is created or destroyed by attribution.
"""

from __future__ import annotations

from decimal import Decimal

from tly.estimator import e_interp
from tly.guard import assert_no_floats

HALF = Decimal("0.5")
ONE = Decimal(1)


def burn_life_years(excess_by_age: dict[int, Decimal], ex_anchors: dict[int, Decimal]) -> Decimal:
    """Σ excess(a) × e(a + 0.5). Negative excess (mortality deficit) is
    allowed and yields negative burn — the identity is signed."""
    assert_no_floats(excess_by_age, "excess_by_age")
    assert_no_floats(ex_anchors, "ex_anchors")
    total = Decimal(0)
    for age, excess in excess_by_age.items():
        total += excess * e_interp(ex_anchors, Decimal(age) + HALF)
    return total


def allocate_largest_remainder(
    total: Decimal, weights: dict[int, Decimal], quantum: Decimal
) -> dict[int, Decimal]:
    """E11: split ``total`` by ``weights`` in ``quantum`` steps, conserving
    the total EXACTLY.

    Weights must sum to exactly 1. Each share floors to the quantum; the
    leftover quanta go to the largest fractional remainders (ties broken by
    key for determinism). Σ result == total, always — tested as invariant.
    """
    assert_no_floats(weights, "weights")
    if sum(weights.values(), Decimal(0)) != ONE:
        raise ValueError("weights must sum to exactly 1")
    if total % quantum != 0:
        raise ValueError(f"total {total} is not a multiple of quantum {quantum}")
    floors: dict[int, Decimal] = {}
    remainders: list[tuple[Decimal, int]] = []
    allocated = Decimal(0)
    for key in sorted(weights):
        raw = total * weights[key]
        floored = (raw // quantum) * quantum
        floors[key] = floored
        allocated += floored
        remainders.append((raw - floored, key))
    leftover_quanta = int((total - allocated) / quantum)
    remainders.sort(key=lambda t: (-t[0], t[1]))
    for _, key in remainders[:leftover_quanta]:
        floors[key] += quantum
    return floors


def distribute_excess(
    total_excess: Decimal, age_weights: dict[int, Decimal], quantum: Decimal = Decimal("0.001")
) -> dict[int, Decimal]:
    """Age-attribute a total excess via a (versioned, per-feed) weight
    profile, conserving the total exactly (E11)."""
    return allocate_largest_remainder(total_excess, age_weights, quantum)
