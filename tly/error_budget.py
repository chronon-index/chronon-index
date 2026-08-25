"""Deterministic error budget (RP Part VIII; RP Part IX E9; SPEC#2 AC-2.4; D-03).

The quadrature over independent symmetric terms IS the E9 variance-addition
rule applied at aggregate level; full per-age Var(S) propagation arrives at
rung 4 with the Monte Carlo budget.

The v0 accuracy statement, module-produced — never hand-typed. Two kinds
of terms with OPPOSITE handling, exactly as Part VIII prescribes:

- SYMMETRIC (measurement) terms combine in quadrature:
    population level/structure ±1.0%, life-table level ±1.5% (the
    conservative end of Part VIII's 1.0–1.5% range), banding/interpolation
    ±0.5% → √(1.0² + 1.5² + 0.5²) = √3.5 ≈ ±1.87%, stated as "~±2%".
- ONE-SIDED (structural) terms are LISTED, never netted and never added
    to the quadrature: vintage lag +2 to +3% (2023 structure read in
    2026), period-vs-cohort +3 to +9% since v0.6.0 (the E6 computation
    on the committed surface measured +8.06%, above the +3-8% literature
    prose — measurement supersedes prose, governed as a version bump).

The one-sided bounds are VERSION-KEYED in tly.methodology
(VERSION_ONE_SIDED_TERMS): reproducing an archived print selects the
band its version was governed by, never HEAD's. The cohort
best-estimate band applies both one-sided lower bounds and both upper
bounds to the measured level (v0.6.0: +5% / +12% -> ≈381-406B; the
A-16-blessed 381-402B remains the correct v0.5.0 statement). The module
emits COMPUTED values; it does not tune to match prose (RALPH §6).

This budget retires at rung 4 when Monte Carlo intervals replace it
(Part VIII last paragraph) — a methodology version bump.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from tly.guard import assert_decimal
from tly.methodology import METHODOLOGY_VERSION, one_sided_terms_for
from tly.numeric import BILLION

SYMMETRIC_TERMS: dict[str, Decimal] = {
    "population_level_structure_pct": Decimal("1.0"),
    "life_table_level_pct": Decimal("1.5"),
    "banding_interpolation_pct": Decimal("0.5"),
}


def one_sided_terms(version: str | None = None) -> dict[str, tuple[Decimal, Decimal]]:
    """The one-sided bounds for ``version`` (default: HEAD methodology)."""
    raw = one_sided_terms_for(version or METHODOLOGY_VERSION)
    return {name: (Decimal(lo), Decimal(hi)) for name, (lo, hi) in raw.items()}


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


def build_error_budget(s_life_years: Decimal, version: str | None = None) -> ErrorBudget:
    assert_decimal(s_life_years, "s_life_years")
    if s_life_years <= 0:
        raise ValueError("S must be positive")
    return ErrorBudget(
        s_life_years=s_life_years,
        symmetric_pct=quadrature_pct(),
        one_sided=one_sided_terms(version),
    )


def accuracy_block(s_life_years: Decimal, version: str | None = None) -> dict:
    """The print's accuracy block, module-produced end to end (B-uc2-09):
    the Part VIII statement plus a real interval from the symmetric
    quadrature; the one-sided terms ride along, listed never netted. Any
    hand-typed accuracy text in a print is a defect — prints must call
    this."""
    budget = build_error_budget(s_life_years, version)
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
