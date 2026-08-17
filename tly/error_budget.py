"""Deterministic error budget (RP Part VIII; SPEC#2 AC-2.4; D-03).

The v0 accuracy statement, module-produced — never hand-typed. Two kinds
of terms with OPPOSITE handling, exactly as Part VIII prescribes:

- SYMMETRIC (measurement) terms combine in quadrature:
    population level/structure ±1.0%, life-table level ±1.5% (the
    conservative end of Part VIII's 1.0–1.5% range), banding/interpolation
    ±0.5% → √(1.0² + 1.5² + 0.5²) = √3.5 ≈ ±1.87%, stated as "~±2%".
- ONE-SIDED (structural) terms are LISTED, never netted and never added
    to the quadrature: vintage lag +2 to +3% (2023 structure read in
    2026), period-vs-cohort +3 to +8% (true cohort stock is higher).

The cohort best-estimate band applies both one-sided lower bounds (+5%)
and both upper bounds (+11%) to the measured level. Note: DECISIONS.md
records the band as "~380–400B"; this module computes ≈381–402B from the
same inputs — the recorded prose rounded the top of the band. The module
emits COMPUTED values; it does not tune to match prose (RALPH §6).

This budget retires at rung 4 when Monte Carlo intervals replace it
(Part VIII last paragraph) — a methodology version bump.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from tly.guard import assert_decimal
from tly.numeric import BILLION

SYMMETRIC_TERMS: dict[str, Decimal] = {
    "population_level_structure_pct": Decimal("1.0"),
    "life_table_level_pct": Decimal("1.5"),
    "banding_interpolation_pct": Decimal("0.5"),
}

ONE_SIDED_TERMS: dict[str, tuple[Decimal, Decimal]] = {
    "vintage_lag_pct": (Decimal("2"), Decimal("3")),
    "period_vs_cohort_pct": (Decimal("3"), Decimal("8")),
}


def quadrature_pct() -> Decimal:
    """√(Σ term²) over the symmetric terms, in Decimal."""
    total = sum((t * t for t in SYMMETRIC_TERMS.values()), Decimal(0))
    return total.sqrt()


@dataclass(frozen=True)
class ErrorBudget:
    s_life_years: Decimal
    symmetric_pct: Decimal
    one_sided: dict[str, tuple[Decimal, Decimal]]

    @property
    def interval(self) -> tuple[Decimal, Decimal]:
        """The symmetric ±quadrature interval around measured S."""
        delta = self.s_life_years * self.symmetric_pct / 100
        return (self.s_life_years - delta, self.s_life_years + delta)

    @property
    def cohort_band(self) -> tuple[Decimal, Decimal]:
        """Both one-sided lower bounds applied, then both upper bounds."""
        low_pct = sum((lo for lo, _ in self.one_sided.values()), Decimal(0))
        high_pct = sum((hi for _, hi in self.one_sided.values()), Decimal(0))
        return (
            self.s_life_years * (1 + low_pct / 100),
            self.s_life_years * (1 + high_pct / 100),
        )

    def statement(self) -> str:
        """The Part VIII honest statement, computed."""
        s_b = (self.s_life_years / BILLION).quantize(Decimal("0.1"))
        lo, hi = self.cohort_band
        lo_b = (lo / BILLION).quantize(Decimal("1"))
        hi_b = (hi / BILLION).quantize(Decimal("1"))
        q = self.symmetric_pct.quantize(Decimal("0.1"))
        return (
            f"Measured-period S = {s_b}B ± ~{q}% (symmetric terms in "
            f"quadrature) on 2023 structure; best-estimate current cohort "
            f"stock ~ {lo_b}-{hi_b}B (one-sided terms listed, never netted: "
            + "; ".join(f"{name} +{lo_}-{hi_}%" for name, (lo_, hi_) in self.one_sided.items())
            + ")."
        )


def build_error_budget(s_life_years: Decimal) -> ErrorBudget:
    assert_decimal(s_life_years, "s_life_years")
    if s_life_years <= 0:
        raise ValueError("S must be positive")
    return ErrorBudget(
        s_life_years=s_life_years,
        symmetric_pct=quadrature_pct(),
        one_sided=dict(ONE_SIDED_TERMS),
    )


def accuracy_block(s_life_years: Decimal) -> dict:
    """The print's accuracy block, module-produced end to end (B-uc2-09):
    the Part VIII statement plus a real interval from the symmetric
    quadrature; the one-sided terms ride along, listed never netted. Any
    hand-typed accuracy text in a print is a defect — prints must call
    this."""
    budget = build_error_budget(s_life_years)
    lo, hi = budget.interval
    return {
        "statement": budget.statement(),
        "uncertainty": {
            "type": "interval",
            "lower": str(lo),
            "upper": str(hi),
        },
        "one_sided_terms_pct": {
            name: [str(lo_), str(hi_)] for name, (lo_, hi_) in budget.one_sided.items()
        },
        "produced_by": "tly.error_budget.accuracy_block",
    }
