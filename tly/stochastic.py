"""P3 stochastic S (S-04; RP Part IV P3; RP Part VIII rung 4 candidate).

MODEL LAYER (floats): interval fans on S(t) from a Lee-Carter fit on the
committed 2010-2023 World qx surface, plus a jump overlay calibrated on
the historical shock set the program names (1918, WWII, HIV, COVID).

Construction, stated:
1. Fit LC on log qx (World, ages 0-100, 2010-2023 measured years).
2. Diffusion: kt is a random walk with drift; simulate paths with the
   fit's sigma (deterministic seeded LCG — reproducible everywhere,
   no numpy, no platform RNG drift).
3. Jumps: a Poisson overlay of mortality-shock years. Calibration
   honesty: four events in ~107 years (1918 flu, WWII, HIV plateau,
   COVID) -> arrival ~ 0.037/yr; severity = a one-to-three-year qx
   multiplier drawn from the event set's observed range (COVID ~1.15x
   world, 1918 ~2x, WWII ~1.3x sustained, HIV ~1.05x long) — a 4-point
   empirical distribution, resampled, never smoothed into a fitted tail
   we have no data for.
4. Each simulated qx surface -> S(t) via the scenario engine's
   projection (same population mechanics, same CBR baseline).

Output: percentile fan for S(t) over a horizon. The interval-coverage
BACKTEST (the P3 acceptance gate) fits on 2010-2018 only and asks
whether measured 2019-2023 S fell inside the fan — with COVID in the
window, this is a real test, not a formality.

This is INFORMATIONAL model content. It does not replace the
deterministic error budget until a governed version bump adopts it
(RP Part VIII's own retirement clause).
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass

from tly.leecarter import lee_carter
from tly.scenario_engine import MAX_AGE, SURFACE, load_inputs, project

MEASURED_YEARS = tuple(range(2010, 2024))
JUMP_RATE = 4.0 / 107.0  # four world shocks in 1918-2024
# (name, qx multiplier, duration years) — the observed set, resampled as-is
JUMP_SET = (
    ("1918-class", 2.0, 1),
    ("wwii-class", 1.3, 3),
    ("hiv-class", 1.05, 8),
    ("covid-class", 1.15, 2),
)


class _LCG:
    """Deterministic 64-bit LCG — same stream on every platform."""

    def __init__(self, seed: int):
        self.s = seed & 0xFFFFFFFFFFFFFFFF

    def u(self) -> float:
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
        return (self.s >> 11) / float(1 << 53)

    def normal(self) -> float:
        u1 = max(self.u(), 1e-12)
        return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * self.u())


def _fit_world(last_year: int):
    """LC fit on the World surface + JUMP-ROBUST diffusion parameters.

    lee_carter takes {age: {year: log mx}}. The fit's own drift/sigma
    over 2010-2023 are contaminated by COVID (the exact years the JUMP
    overlay models), so using them for the diffusion would double-count
    shock risk. Separation, documented: kt innovations more than 2.5
    robust-sigma (MAD-based) from the median are classified as jump
    years and EXCLUDED; drift/sigma re-estimated on the rest. Returns
    (fit, diff_drift, diff_sigma, jump_years).
    """
    data = json.loads(SURFACE.read_text(encoding="utf-8"))
    years = [y for y in MEASURED_YEARS if y <= last_year]
    log_mx = {
        a: {y: math.log(max(float(data["years"][str(y)][str(a)]), 1e-10)) for y in years}
        for a in range(MAX_AGE + 1)
    }
    fit = lee_carter(log_mx)
    innov = [fit.kt[i + 1] - fit.kt[i] for i in range(len(fit.kt) - 1)]
    med = sorted(innov)[len(innov) // 2]
    mad = sorted(abs(x - med) for x in innov)[len(innov) // 2]
    robust_sigma = 1.4826 * mad if mad > 0 else (fit.sigma or 1e-6)
    kept = [x for x in innov if abs(x - med) <= 2.5 * robust_sigma]
    jumps = [years[i + 1] for i, x in enumerate(innov) if abs(x - med) > 2.5 * robust_sigma]
    drift = sum(kept) / len(kept)
    var = sum((x - drift) ** 2 for x in kept) / max(len(kept) - 1, 1)
    return fit, drift, math.sqrt(var), jumps


@dataclass(frozen=True)
class Fan:
    years: list[int]
    p5: list[float]
    p25: list[float]
    p50: list[float]
    p75: list[float]
    p95: list[float]
    n_paths: int


def simulate_fan(
    horizon: int = 20,
    n_paths: int = 500,
    seed: int = 20260904,
    last_fit_year: int = 2023,
    with_jumps: bool = True,
) -> Fan:
    """Percentile fan for S over ``horizon`` years from the fit's end."""
    fit, drift, sigma, _jumps = _fit_world(last_fit_year)
    qx_base, pop0 = load_inputs()
    rng = _LCG(seed)
    bbar = sum(fit.bx) / len(fit.bx)
    paths: list[list[float]] = []
    for _ in range(n_paths):
        # diffusion path for kt (jump-robust parameters)
        kt = fit.kt[-1]
        mults: list[float] = []
        jump_left, jump_mult = 0, 1.0
        for _h in range(horizon + 1):
            kt = kt + drift + sigma * rng.normal()
            # qx multiplier vs the CENTRAL forecast at the same horizon:
            # exp(bbar * (kt - kt_central)) — age-average bx, scalar
            # (bx variation is second-order for S)
            central = fit.kt[-1] + drift * (_h + 1)
            m = math.exp(bbar * (kt - central))
            if with_jumps:
                if jump_left > 0:
                    m *= jump_mult
                    jump_left -= 1
                elif rng.u() < JUMP_RATE:
                    _name, jm, jd = JUMP_SET[int(rng.u() * len(JUMP_SET)) % len(JUMP_SET)]
                    jump_mult, jump_left = jm, jd
                    m *= jm
                    jump_left -= 1
            mults.append(m)
        # build a shocked surface: year-t column scaled by mults[t]
        qx_path = {
            y: [
                min(1.0, q * mults[min(max(y - 2023 - 1, 0), horizon)])
                for q in qx_base[min(y, 2100)]
            ]
            if y > 2023
            else qx_base[min(y, 2100)]
            for y in range(2023, 2023 + horizon + 1)
        }
        res = project(qx_path, pop0, (), horizon)
        paths.append(res.s)
    years = list(range(2023, 2023 + horizon + 1))
    fan_cols = list(zip(*paths))

    def pct(col, p):
        s = sorted(col)
        return s[min(len(s) - 1, int(p * len(s)))]

    return Fan(
        years=years,
        p5=[pct(c, 0.05) for c in fan_cols],
        p25=[pct(c, 0.25) for c in fan_cols],
        p50=[pct(c, 0.50) for c in fan_cols],
        p75=[pct(c, 0.75) for c in fan_cols],
        p95=[pct(c, 0.95) for c in fan_cols],
        n_paths=n_paths,
    )


@dataclass(frozen=True)
class CoverageResult:
    fit_through: int
    tested_years: list[int]
    observed_s: list[float]
    inside_90: list[bool]
    coverage: float


def measured_world_s(year: int) -> float:
    """Measured-period S for ``year`` from the committed surface + the
    2023 population structure held fixed (structure-constant S, the same
    convention the backfill uses for vintage comparisons)."""
    qx_base, pop0 = load_inputs()
    from tly.scenario_engine import period_e

    e = period_e(qx_base[year])
    return sum(pop0[a] * e[a] for a in range(MAX_AGE + 1))


def coverage_backtest(fit_through: int = 2018, n_paths: int = 500) -> CoverageResult:
    """THE P3 GATE: fit only on data through ``fit_through``, fan forward,
    and check whether measured S (structure-constant) fell inside the
    90% interval — 2019-2023 includes COVID, so this is a genuine test."""
    fit, drift, sigma, _jumps = _fit_world(fit_through)
    qx_base, pop0 = load_inputs()
    from tly.scenario_engine import period_e

    rng = _LCG(20260904)
    horizon = 2023 - fit_through
    bbar = sum(fit.bx) / len(fit.bx)
    sims: list[list[float]] = []  # per path, S at each tested year
    for _ in range(n_paths):
        kt = fit.kt[-1]
        row = []
        jump_left, jump_mult = 0, 1.0
        for h in range(1, horizon + 1):
            kt = kt + drift + sigma * rng.normal()
            central = fit.kt[-1] + drift * h
            m = math.exp(bbar * (kt - central))
            if jump_left > 0:
                m *= jump_mult
                jump_left -= 1
            elif rng.u() < JUMP_RATE:
                _n, jm, jd = JUMP_SET[int(rng.u() * len(JUMP_SET)) % len(JUMP_SET)]
                jump_mult, jump_left = jm, jd - 1
                m *= jm
            # S under fitted central qx for that year scaled by m,
            # holding 2023 structure (same convention as the observation)
            col = [min(1.0, math.exp(lm) * m) for lm in fit.log_mx_hat(central)]
            e = period_e(col)
            row.append(sum(pop0[a] * e[a] for a in range(MAX_AGE + 1)))
        sims.append(row)
    tested = list(range(fit_through + 1, 2024))
    observed = [measured_world_s(y) for y in tested]
    inside = []
    for i, _y in enumerate(tested):
        col = sorted(s[i] for s in sims)
        lo, hi = col[int(0.05 * len(col))], col[min(len(col) - 1, int(0.95 * len(col)))]
        inside.append(lo <= observed[i] <= hi)
    return CoverageResult(
        fit_through=fit_through,
        tested_years=tested,
        observed_s=observed,
        inside_90=inside,
        coverage=sum(inside) / len(inside),
    )
