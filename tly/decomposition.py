"""Decomposition engine (SPEC#1; RP Part IX E4/E5).

Two views of ΔS between epochs, kept strictly distinct:

1. ``exact_decomposition`` — the algebraic identity
       ΔS = Ē_t·ΔN + N_t·ΔĒ + ΔN·ΔĒ
   Algebraically exact; in Decimal the Ē = S/N divisions round at prec 34,
   so the closure term is not literally zero but ULP-noise (observed
   ~1e-23 life-years on world-scale values, relative ~1e-33). Tests bound
   it below 1e-15 life-years — 18 orders below a single second of life.
   This is bookkeeping, not modeling.

2. ``identity_decomposition`` — the E4/E5 economic form
       ΔS = mint(B·e(0)) + spend(−N) + drift(N·ΔĒ) − burn + residual
   whose terms are CONVENTIONS (per-epoch flows). The residual — deaths'
   expectancy mismatch, migration, cross terms, convention slack — is
   computed and EXPOSED on every result, never absorbed into a term.
   Hiding a residual inside drift would be tuning (RALPH_LOOP §6).

The v0 drift convention was lost with the original METHODOLOGY; proposing
and validating one is B-uc1-12's task. This module only provides the
machinery that makes any convention's residual visible.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from tly.guard import assert_decimal
from tly.stock import LocationStock


@dataclass(frozen=True)
class ExactDecomposition:
    """ΔS = population_term + revision_term + cross_term, exactly."""

    location: str
    year_start: int
    year_end: int
    ds: Decimal
    population_term: Decimal  # Ē_t · ΔN
    revision_term: Decimal  # N_t · ΔĒ
    cross_term: Decimal  # ΔN · ΔĒ

    @property
    def closure(self) -> Decimal:
        """Zero up to prec-34 division ULP; bounded (<1e-15) in tests."""
        return self.ds - (self.population_term + self.revision_term + self.cross_term)


def exact_decomposition(start: LocationStock, end: LocationStock) -> ExactDecomposition:
    if start.location != end.location or start.sex != end.sex:
        raise ValueError("decomposition requires one location and one sex")
    dn = end.n_persons - start.n_persons
    de = end.e_bar - start.e_bar
    return ExactDecomposition(
        location=start.location,
        year_start=start.year,
        year_end=end.year,
        ds=end.s_life_years - start.s_life_years,
        population_term=start.e_bar * dn,
        revision_term=start.n_persons * de,
        cross_term=dn * de,
    )


@dataclass(frozen=True)
class IdentityDecomposition:
    """E4/E5 economic form with the residual exposed, never netted."""

    location: str
    year_start: int
    year_end: int
    ds: Decimal
    mint: Decimal  # B · e(0)
    spend: Decimal  # −N_t
    drift: Decimal  # N_t · ΔĒ (revision term under the chosen convention)
    burn: Decimal  # excess-death life-years (0 outside shock epochs)

    @property
    def residual(self) -> Decimal:
        """ΔS minus the sum of the convention terms. Published, not hidden."""
        return self.ds - (self.mint + self.spend + self.drift - self.burn)


def identity_decomposition(
    start: LocationStock,
    end: LocationStock,
    *,
    births: Decimal,
    e0: Decimal,
    burn: Decimal = Decimal(0),
) -> IdentityDecomposition:
    """E5 discrete accounting over one epoch pair.

    ``births`` is the epoch's birth count; ``e0`` the newborn expectancy
    under the chosen table convention; ``burn`` the excess-death
    life-years. drift here is N_t·ΔĒ; the residual carries everything the
    conventions do not.
    """
    if start.location != end.location or start.sex != end.sex:
        raise ValueError("decomposition requires one location and one sex")
    assert_decimal(births, "births")
    assert_decimal(e0, "e0")
    assert_decimal(burn, "burn")
    return IdentityDecomposition(
        location=start.location,
        year_start=start.year,
        year_end=end.year,
        ds=end.s_life_years - start.s_life_years,
        mint=births * e0,
        spend=-start.n_persons,
        drift=start.n_persons * (end.e_bar - start.e_bar),
        burn=burn,
    )
