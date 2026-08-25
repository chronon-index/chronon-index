"""Lee-Carter vintage backtest harness (C-uc6-04; RP Part IV P2 gate; D-02).

PROTOCOL ADAPTATION, stated openly: RP prescribes "fit through 1990,
project to 2020" — on HMD series reaching back to the 1950s. The keyless
Eurostat registry data (ruling B-uc2-02(c)) BEGINS in 1990, so the
adapted protocol preserves the structure rather than the exact dates:
fit 1990–2005 (16 years), project 2006–2024 (19 years out-of-sample,
containing the COVID structural break — precisely what makes the
backtest honest). Cairns et al. (2009)'s protocol refinements remain
reading-gated (R2) and may supersede this harness via version bump.

Jump-off bias correction (Lee-Carter's standard fix): projections are
anchored at the LAST OBSERVED log-rates, not the fitted ones —
log m̂(x, T+h) = log m(x, T) + b(x)·(k̂(T+h) − k(T)). Both anchored and
unanchored paths are computed so the correction's effect is measured,
not asserted.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from tly.leecarter import LeeCarterFit, lee_carter, log_mx_matrix
from tly.lifetables import kannisto_close, life_table, raw_rates


@dataclass(frozen=True)
class BacktestResult:
    geo: str
    fit_years: tuple[int, int]
    test_years: tuple[int, ...]
    realized_e0: dict[int, float]
    projected_e0: dict[int, float]  # jump-off corrected (anchored)
    projected_e0_unanchored: dict[int, float]

    @property
    def bias(self) -> float:
        """Mean signed error, projected − realized (anchored path)."""
        return sum(self.projected_e0[y] - self.realized_e0[y] for y in self.test_years) / len(
            self.test_years
        )

    @property
    def mae(self) -> float:
        return sum(abs(self.projected_e0[y] - self.realized_e0[y]) for y in self.test_years) / len(
            self.test_years
        )

    def bias_over(self, years: tuple[int, ...]) -> float:
        return sum(self.projected_e0[y] - self.realized_e0[y] for y in years) / len(years)


def _e0_from_log_mx(log_mx: list[float], ages: tuple[int, ...]) -> float:
    mx = {a: math.exp(v) for a, v in zip(ages, log_mx)}
    return life_table(mx)[0]["ex"]


def backtest(
    magec_path: Path,
    pjan_path: Path,
    geo: str,
    fit_start: int = 1990,
    fit_end: int = 2005,
    test_end: int = 2024,
) -> BacktestResult:
    fit_grid = log_mx_matrix(magec_path, pjan_path, geo, range(fit_start, fit_end + 1))
    fit: LeeCarterFit = lee_carter(fit_grid)
    test_years = tuple(range(fit_end + 1, test_end + 1))

    # jump-off anchor: the last OBSERVED graduated log-rates
    last_raw = raw_rates(magec_path, pjan_path, geo, fit_end)
    last_grad = kannisto_close(last_raw.mx, last_raw.dx_weights)
    anchor = [math.log(last_grad[a]) for a in fit.ages]

    k_path = fit.forecast_kt(len(test_years))
    k_last = fit.kt[-1]

    projected: dict[int, float] = {}
    unanchored: dict[int, float] = {}
    for h, year in enumerate(test_years):
        shifted = [a0 + b * (k_path[h] - k_last) for a0, b in zip(anchor, fit.bx)]
        projected[year] = _e0_from_log_mx(shifted, fit.ages)
        unanchored[year] = _e0_from_log_mx(fit.log_mx_hat(k_path[h]), fit.ages)

    realized: dict[int, float] = {}
    for year in test_years:
        raw = raw_rates(magec_path, pjan_path, geo, year)
        grad = kannisto_close(raw.mx, raw.dx_weights)
        realized[year] = life_table({a: grad[a] for a in fit.ages})[0]["ex"]

    return BacktestResult(
        geo=geo,
        fit_years=(fit_start, fit_end),
        test_years=test_years,
        realized_e0=realized,
        projected_e0=projected,
        projected_e0_unanchored=unanchored,
    )
