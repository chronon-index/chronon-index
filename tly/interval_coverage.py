"""Interval-coverage harness (SPEC#6 AC-6.1; RP Part X P8; C-uc6-06).

P8: backtest realized values must fall inside published intervals at the
stated rate. Published intervals do not exist until the P3 stochastic
index — so, per amended AC-6.1, what runs TODAY is the HARNESS validated
on synthetic data with known true coverage. That honesty is part of the
contract: this module measures coverage; it does not (yet) have real
intervals to measure. When P3 lands, the same functions run on real
backtests and the synthetic tests stay as harness regression checks.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from tly.guard import assert_no_floats


@dataclass(frozen=True)
class CoverageResult:
    nominal: Decimal  # stated coverage, e.g. 0.90
    hits: int
    total: int

    @property
    def empirical(self) -> Decimal:
        return Decimal(self.hits) / Decimal(self.total)

    @property
    def tolerance(self) -> Decimal:
        """Binomial sampling tolerance: 3·sqrt(p(1−p)/n), computed in
        Decimal (sqrt via Decimal.sqrt — exact context arithmetic)."""
        p = self.nominal
        n = Decimal(self.total)
        return 3 * (p * (1 - p) / n).sqrt()

    @property
    def within_tolerance(self) -> bool:
        return abs(self.empirical - self.nominal) <= self.tolerance


def measure_coverage(
    intervals: list[tuple[Decimal, Decimal]],
    realized: list[Decimal],
    nominal: Decimal,
) -> CoverageResult:
    """Count realized values inside their intervals (inclusive bounds —
    the same convention as the print schema's accuracy block)."""
    assert_no_floats(intervals, "intervals")
    assert_no_floats(realized, "realized")
    assert_no_floats(nominal, "nominal")
    if len(intervals) != len(realized):
        raise ValueError("one interval per realized value")
    if not intervals:
        raise ValueError("cannot measure coverage of nothing")
    if not 0 < nominal < 1:
        raise ValueError("nominal coverage must be in (0, 1)")
    hits = sum(1 for (lower, upper), value in zip(intervals, realized) if lower <= value <= upper)
    return CoverageResult(nominal=nominal, hits=hits, total=len(intervals))
