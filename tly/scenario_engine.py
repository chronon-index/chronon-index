"""Scenario engine — 20-year index simulations (RP Part V #3/#4 follow-on;
Ben directive 2026-09-04: "what happens to the math when X").

MODEL LAYER: floats permitted (like leecarter/cohort); nothing here can
touch settlement. The engine projects the WORLD index forward from the
committed 2023 structure under a baseline (WPP-medium mortality surface,
documented CBR path) and under shocked variants, and reports the paths
of the numbers a token holder would live with: S(t), supply growth g,
drawdown, recovery.

Mechanics, stated:
- Population projection: N(a+1, t+1) = N(a, t) * (1 - qx(a, t));
  N(0, t+1) = births(t) * (1 - qx(0, t)/2) (half-interval infant risk).
- e(a, t): period life expectancy from the year-t qx column (trapezoid
  person-years, open age 100 closes with qx=1 — same conventions as
  tly.cohort).
- S(t) = sum N(a, t) * e(a, t): the measured-period stock, the quantity
  the settlement series prints.
- Births: baseline CBR ramps linearly 16.327 (2023) -> 14.0 (2045),
  a WPP-medium-like decline (assumption, documented); shocks scale it.
- Shocks compose three levers, exactly the levers reality has:
  mortality (transient qx multipliers by age band and year), longevity
  trend (persistent qx multiplier phased in — breakthroughs lower it,
  systemic decay raises it), fertility (CBR multiplier path).

Token reading: supply mirrors S, so dS/S IS the supply path; a holder's
SHARE never changes (share invariance) — scenarios move the total pie
and hence the per-token time backing. Not modeled: PRICE (no market
exists; trading backtests need a demand model — stated limitation).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SURFACE = (
    REPO_ROOT
    / "data"
    / "snapshots"
    / "2026-08-25"
    / "fixtures"
    / "wpp_world_qx_surface_2010_2100.json"
)
POP_FIX = (
    REPO_ROOT
    / "data"
    / "snapshots"
    / "2026-08-17"
    / "fixtures"
    / "wpp_pop_single_age_fixture.csv.gz"
)
MAX_AGE = 100
BASE_YEAR = 2023
HORIZON = 20
CBR_2023 = 16.327
CBR_2045 = 14.0


def load_inputs() -> tuple[dict[int, list[float]], list[float]]:
    """(qx by year -> list[101], N by single age for 2023)."""
    data = json.loads(SURFACE.read_text(encoding="utf-8"))
    qx = {
        int(y): [float(block[str(a)]) for a in range(MAX_AGE + 1)]
        for y, block in data["years"].items()
    }
    import csv
    import gzip
    import io

    raw = gzip.decompress(POP_FIX.read_bytes()).decode("utf-8")
    pop = [0.0] * (MAX_AGE + 1)
    for r in csv.DictReader(io.StringIO(raw)):
        if r["Location"] == "World" and r["Time"] == str(BASE_YEAR):
            age = min(int(r["AgeGrpStart"]), MAX_AGE)
            pop[age] += float(r["PopTotal"]) * 1000.0
    return qx, pop


def period_e(qx_col: list[float]) -> list[float]:
    """Period e(a) for one year's qx column, trapezoid person-years."""
    e = [0.0] * (MAX_AGE + 1)
    acc_years = 0.0
    for a in range(MAX_AGE, -1, -1):
        q = min(qx_col[a], 1.0)
        # person-years this age per person alive at a: survivors 1, deaths 1/2
        acc_years = (1.0 - q) * (1.0 + acc_years) + q * 0.5
        e[a] = acc_years
    return e


@dataclass(frozen=True)
class Shock:
    """One composable lever-pull.

    mort_mult: {(age_lo, age_hi): multiplier} applied to qx in
        [start, start+duration) — transient (pandemic, war, disaster).
    trend_mult: persistent qx multiplier phased in linearly over
        ramp_years from start (breakthrough < 1, decay > 1), applied to
        ages >= trend_age_lo.
    cbr_mult: CBR multiplier in [start, start+duration) (fertility).
    """

    start: int = BASE_YEAR + 1
    duration: int = 1
    mort_mult: dict[tuple[int, int], float] = field(default_factory=dict)
    trend_mult: float = 1.0
    trend_age_lo: int = 0
    ramp_years: int = 10
    cbr_mult: float = 1.0


@dataclass(frozen=True)
class Scenario:
    key: str
    category: str
    name: str
    shocks: tuple[Shock, ...]
    rationale: str = ""


@dataclass(frozen=True)
class PathResult:
    years: list[int]
    s: list[float]  # S(t), life-years
    n: list[float]
    e_bar: list[float]

    def g_pct(self) -> list[float]:
        return [(self.s[i + 1] / self.s[i] - 1.0) * 100.0 for i in range(len(self.s) - 1)]


def _cbr(year: int) -> float:
    if year >= 2045:
        return CBR_2045
    return CBR_2023 + (CBR_2045 - CBR_2023) * (year - BASE_YEAR) / (2045 - BASE_YEAR)


def project(
    qx: dict[int, list[float]],
    pop0: list[float],
    shocks: tuple[Shock, ...] = (),
    horizon: int = HORIZON,
) -> PathResult:
    """Project S/N/Ē from BASE_YEAR for ``horizon`` years under shocks."""
    pop = list(pop0)
    years, s_path, n_path, ebar_path = [], [], [], []
    for step in range(horizon + 1):
        year = BASE_YEAR + step
        col = list(qx[min(year, 2100)])
        for sh in shocks:
            # persistent trend, phased in
            if year >= sh.start and sh.trend_mult != 1.0:
                phase = min(1.0, (year - sh.start + 1) / max(sh.ramp_years, 1))
                mult = 1.0 + (sh.trend_mult - 1.0) * phase
                for a in range(sh.trend_age_lo, MAX_AGE + 1):
                    col[a] *= mult
            # transient mortality
            if sh.start <= year < sh.start + sh.duration:
                for (lo, hi), m in sh.mort_mult.items():
                    for a in range(lo, min(hi, MAX_AGE) + 1):
                        col[a] *= m
        col = [min(q, 1.0) for q in col]

        e = period_e(col)
        n = sum(pop)
        s = sum(pop[a] * e[a] for a in range(MAX_AGE + 1))
        years.append(year)
        s_path.append(s)
        n_path.append(n)
        ebar_path.append(s / n)

        # advance one year
        cbr = _cbr(year)
        for sh in shocks:
            if sh.start <= year < sh.start + sh.duration:
                cbr *= sh.cbr_mult
        births = n * cbr / 1000.0
        new = [0.0] * (MAX_AGE + 1)
        for a in range(MAX_AGE):
            new[a + 1] = pop[a] * (1.0 - min(col[a], 1.0))
        new[MAX_AGE] += pop[MAX_AGE] * (1.0 - min(col[MAX_AGE], 1.0))  # open group
        new[0] = births * (1.0 - min(col[0], 1.0) / 2.0)
        pop = new
    return PathResult(years=years, s=s_path, n=n_path, e_bar=ebar_path)


@dataclass(frozen=True)
class ScenarioOutcome:
    key: str
    category: str
    name: str
    ds_pct_h: float  # S deviation vs baseline at horizon end, %
    max_drawdown_pct: float  # worst S deviation vs baseline, %
    trough_year: int
    recovery_years: int | None  # years from trough back to baseline; None = never (in horizon)
    worst_g_pct: float  # worst single-year supply growth under scenario
    e_bar_delta_h: float  # Ē deviation at horizon, years


def evaluate(scenario: Scenario, baseline: PathResult, qx, pop0) -> ScenarioOutcome:
    path = project(qx, pop0, scenario.shocks)
    dev = [(path.s[i] / baseline.s[i] - 1.0) * 100.0 for i in range(len(path.s))]
    trough_i = min(range(len(dev)), key=lambda i: dev[i])
    recovery = None
    for i in range(trough_i + 1, len(dev)):
        if dev[i] >= -0.01:
            recovery = path.years[i] - path.years[trough_i]
            break
    g = path.g_pct()
    return ScenarioOutcome(
        key=scenario.key,
        category=scenario.category,
        name=scenario.name,
        ds_pct_h=dev[-1],
        max_drawdown_pct=min(dev),
        trough_year=path.years[trough_i],
        recovery_years=recovery,
        worst_g_pct=min(g) if g else 0.0,
        e_bar_delta_h=path.e_bar[-1] - baseline.e_bar[-1],
    )
