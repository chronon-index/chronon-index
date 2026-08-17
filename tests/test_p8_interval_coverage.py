"""C-uc6-06 / AC-6.1 / invariant P8: interval coverage — harness validation.

HONESTY (per amended AC-6.1, stated here as required): published intervals
do not exist until the P3 stochastic index, so P8 today validates the
measurement HARNESS on synthetic data whose true coverage is known by
construction. This test is NEVER skipped — it runs on every build; when P3
lands, real-backtest coverage joins it, and these synthetic cases remain
as harness regression checks.
"""

from __future__ import annotations

import random
from decimal import Decimal

import pytest

from tly.interval_coverage import measure_coverage

D = Decimal


def _synthetic(n: int, coverage_period: int) -> tuple[list, list]:
    """n values; every ``coverage_period``-th one deliberately OUTSIDE its
    interval — true coverage is exactly (period−1)/period by construction."""
    intervals, realized = [], []
    for i in range(n):
        lower, upper = D(0), D(10)
        value = D(5) if i % coverage_period else D(99)  # every k-th misses
        intervals.append((lower, upper))
        realized.append(value)
    return intervals, realized


def test_p8_interval_coverage():
    """Named per RP Part X — never skipped. Exact-construction case: 90%
    true coverage measured as exactly 0.9; the harness accepts a matching
    nominal and rejects a miscalibrated one."""
    intervals, realized = _synthetic(1000, 10)
    result = measure_coverage(intervals, realized, nominal=D("0.9"))
    assert result.hits == 900
    assert result.empirical == D("0.9")  # exact, by construction
    assert result.within_tolerance  # nominal 0.9 vs empirical 0.9

    overclaiming = measure_coverage(intervals, realized, nominal=D("0.99"))
    assert not overclaiming.within_tolerance  # 0.9 real vs 0.99 claimed: caught


def test_p8_harness_on_noisy_synthetic():
    """Seeded stochastic case: ~90% coverage from a random draw stays
    inside the binomial tolerance band around 0.9."""
    rng = random.Random(20260817)
    intervals, realized = [], []
    for _ in range(2000):
        intervals.append((D(0), D(9)))
        realized.append(D(rng.randint(0, 9)) if rng.random() < 0.5 else D(rng.randint(0, 10)))
    # true coverage: 0.5·1.0 + 0.5·(10/11) ≈ 0.9545
    result = measure_coverage(intervals, realized, nominal=D("0.9545"))
    assert result.within_tolerance
    assert not measure_coverage(intervals, realized, nominal=D("0.80")).within_tolerance


def test_p8_bounds_are_inclusive():
    result = measure_coverage([(D(1), D(2))], [D(2)], nominal=D("0.5"))
    assert result.hits == 1  # upper bound inclusive, matching the print schema


def test_p8_harness_input_discipline():
    with pytest.raises(ValueError, match="one interval per"):
        measure_coverage([(D(0), D(1))], [], nominal=D("0.9"))
    with pytest.raises(ValueError, match="coverage of nothing"):
        measure_coverage([], [], nominal=D("0.9"))
    with pytest.raises(ValueError, match=r"in \(0, 1\)"):
        measure_coverage([(D(0), D(1))], [D(1)], nominal=D("1"))
