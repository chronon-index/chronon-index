"""Estimator E2 (RP Part IX): S = Σ over bands of N_band × e(mid(band)).

Ported from seed/tly_v0_calc.py (frozen ground truth) at A-13. The package
golden test (tests/test_package_golden.py) proves this module reproduces
seed/results_v0.json to 4 decimal places on the committed snapshot — the
anchor every refactor must keep green (RALPH_LOOP §5 Phase A).

Interpolation policy, versioned per AC-1.4: "linear-on-anchors, flat-tail".
Changing it requires a methodology version bump.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from tly.numeric import BILLION, Q4
from tly.parsers import PopulationBand

INTERPOLATION_POLICY = "linear-on-anchors, flat-tail"


def e_interp(table: dict[int, Decimal], age: Decimal) -> Decimal:
    """Piecewise-linear e() on exact-age anchors; flat beyond the last anchor."""
    anchors = sorted(table)
    if age >= anchors[-1]:
        return table[anchors[-1]]
    if age < anchors[0]:
        raise ValueError(f"age {age} below first anchor")
    for lo, hi in zip(anchors, anchors[1:]):
        if Decimal(lo) <= age <= Decimal(hi):
            frac = (age - Decimal(lo)) / (Decimal(hi) - Decimal(lo))
            return table[lo] + (table[hi] - table[lo]) * frac
    raise AssertionError("unreachable")


@dataclass(frozen=True)
class BandTerm:
    """One band's contribution to S: N_band × e(mid(band))."""

    label: str
    midpoint: Decimal
    count: Decimal
    e_mid: Decimal
    term: Decimal


@dataclass(frozen=True)
class StockResult:
    """S for one life-table year, with the full per-band decomposition."""

    year: int
    s_life_years: Decimal
    band_terms: tuple[BandTerm, ...]

    @property
    def s_billions_4dp(self) -> Decimal:
        return (self.s_life_years / BILLION).quantize(Q4)


def compute_stock(table: dict[int, Decimal], bands: list[PopulationBand], year: int) -> StockResult:
    """E2 over one life table and one population structure."""
    terms: list[BandTerm] = []
    s = Decimal(0)
    for band in bands:
        e_mid = e_interp(table, band.midpoint)
        term = band.count * e_mid
        s += term
        terms.append(
            BandTerm(
                label=band.label,
                midpoint=band.midpoint,
                count=band.count,
                e_mid=e_mid,
                term=term,
            )
        )
    return StockResult(year=year, s_life_years=s, band_terms=tuple(terms))


def total_population(bands: list[PopulationBand]) -> Decimal:
    return sum((b.count for b in bands), Decimal(0))


def e_bar(stock: StockResult, n_total: Decimal) -> Decimal:
    """Mean remaining expectancy per living person: Ē = S / N."""
    return stock.s_life_years / n_total


def mint(births: Decimal, e0: Decimal) -> Decimal:
    """Identity mint term B × e(0) (RP Part IX E4/E5)."""
    return births * e0
