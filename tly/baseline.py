"""Baseline expected deaths + coverage metadata (SPEC#2; B-uc2-04).

Method (registered as the v0.2.0 ``baseline`` policy): for each country and
each period-of-year (week or month), fit a straight line through the
2015-2019 observations and extrapolate — Karlinsky & Kobak's own published
baseline for the World Mortality Dataset. Excess = observed − expected.

Least squares is closed-form in Decimal: with years x centered on their
mean, slope = Σ(x−x̄)y / Σ(x−x̄)² — exact arithmetic except the final
divisions (prec 34).

Coverage metadata (invariant P7): per country and target year, which
periods are MEASURED (observation exists) vs IMPUTED (no observation) —
published on every print, never hidden.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from tly.wmd import DeathsCell, country_series

FIT_YEARS = (2015, 2016, 2017, 2018, 2019)


@dataclass(frozen=True)
class PeriodFit:
    """Per-period linear fit: expected(year) = intercept + slope·(year−x̄)."""

    period: int
    x_bar: Decimal
    intercept: Decimal  # mean deaths over fit years
    slope: Decimal

    def expected(self, year: int) -> Decimal:
        return self.intercept + self.slope * (Decimal(year) - self.x_bar)


@dataclass(frozen=True)
class CountryBaseline:
    iso3: str
    time_unit: str
    fits: dict[int, PeriodFit]  # period -> fit

    def expected(self, year: int, period: int) -> Decimal:
        if period not in self.fits:
            raise ValueError(f"no baseline fit for {self.iso3} period {period}")
        return self.fits[period].expected(year)


def fit_baseline(
    cells: list[DeathsCell], iso3: str, fit_years: tuple[int, ...] = FIT_YEARS
) -> CountryBaseline:
    """Fit the per-period linear baseline from ``fit_years`` observations.

    Periods missing any fit year are excluded (week 53 exists only in some
    years) — an incomplete fit would silently bias the baseline low or
    high, so those periods become IMPUTED in coverage terms.
    """
    series = country_series(cells, iso3)
    time_unit = series[0].time_unit
    by_period: dict[int, dict[int, Decimal]] = {}
    for c in series:
        if c.year in fit_years:
            by_period.setdefault(c.time, {})[c.year] = c.deaths
    n = Decimal(len(fit_years))
    x_bar = sum((Decimal(y) for y in fit_years), Decimal(0)) / n
    sxx = sum(((Decimal(y) - x_bar) ** 2 for y in fit_years), Decimal(0))
    fits: dict[int, PeriodFit] = {}
    for period, obs in by_period.items():
        if set(obs) != set(fit_years):
            continue  # incomplete fit window -> no baseline for this period
        ys = [obs[y] for y in fit_years]
        intercept = sum(ys, Decimal(0)) / n
        sxy = sum(((Decimal(y) - x_bar) * obs[y] for y in fit_years), Decimal(0))
        fits[period] = PeriodFit(period=period, x_bar=x_bar, intercept=intercept, slope=sxy / sxx)
    if not fits:
        raise ValueError(f"no complete fit periods for {iso3} over {fit_years}")
    return CountryBaseline(iso3=iso3, time_unit=time_unit, fits=fits)


@dataclass(frozen=True)
class ExcessObservation:
    iso3: str
    year: int
    period: int
    observed: Decimal
    expected: Decimal

    @property
    def excess(self) -> Decimal:
        return self.observed - self.expected


def excess_series(
    cells: list[DeathsCell], baseline: CountryBaseline, year: int
) -> list[ExcessObservation]:
    """Observed−expected for every measured period of ``year`` that has a
    baseline fit. Unmeasured or unfit periods are simply absent here — they
    appear in :func:`coverage_metadata` as imputed instead."""
    series = [c for c in country_series(cells, baseline.iso3) if c.year == year]
    return [
        ExcessObservation(
            iso3=baseline.iso3,
            year=year,
            period=c.time,
            observed=c.deaths,
            expected=baseline.expected(year, c.time),
        )
        for c in series
        if c.time in baseline.fits
    ]


@dataclass(frozen=True)
class CoverageRecord:
    """P7 coverage honesty for one (country, year): measured vs imputed."""

    iso3: str
    year: int
    time_unit: str
    measured_periods: tuple[int, ...]
    imputed_periods: tuple[int, ...]  # no observation OR no baseline fit

    @property
    def measured_share(self) -> Decimal:
        total = len(self.measured_periods) + len(self.imputed_periods)
        return Decimal(len(self.measured_periods)) / Decimal(total)


def coverage_metadata(
    cells: list[DeathsCell], baseline: CountryBaseline, year: int
) -> CoverageRecord:
    total_periods = range(1, 13) if baseline.time_unit == "monthly" else range(1, 53)
    observed = {c.time for c in country_series(cells, baseline.iso3) if c.year == year}
    measured = tuple(p for p in total_periods if p in observed and p in baseline.fits)
    imputed = tuple(p for p in total_periods if p not in measured)
    return CoverageRecord(
        iso3=baseline.iso3,
        year=year,
        time_unit=baseline.time_unit,
        measured_periods=measured,
        imputed_periods=imputed,
    )


def coverage_block(records: list[CoverageRecord]) -> dict:
    """The print's P7 coverage block from per-country records.

    measured_share is the plain ratio of measured periods to total periods
    across all listed countries (equal period weighting — a versioned
    upgrade to population weighting would need a methodology bump);
    by_country carries each country's own share for full honesty.
    """
    if not records:
        raise ValueError("coverage_block needs at least one CoverageRecord")
    measured = sum(len(r.measured_periods) for r in records)
    total = sum(len(r.measured_periods) + len(r.imputed_periods) for r in records)
    return {
        "measured_share": Decimal(measured) / Decimal(total),
        "by_country": {r.iso3: r.measured_share for r in sorted(records, key=lambda r: r.iso3)},
        "period_universe": {r.iso3: r.time_unit for r in sorted(records, key=lambda r: r.iso3)},
    }
