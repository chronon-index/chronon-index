"""COVID replay on TRUE real-time vintages (C-uc6-07; SPEC#6 AC-6.2;
RP Part IV P4).

The no-hindsight constraint is real, not simulated: each vintage is the
World Mortality Dataset exactly as a given git commit published it
(2021-01-14, 2021-06-29, 2021-12-31, 2022-06-29 — snapshotted with
commit shas and dual hashes). An analyst on those dates had exactly
those bytes, nothing more.

LIMITATIONS, stated:
- Panel = Albania + Germany, the settlement print's coverage panel —
  a two-country replay of the pipeline's own machinery, not a world
  estimate.
- Our OWN vintage store only begins 2026-08-25; future shocks replay
  natively from ``data/vintages``. For 2020 the WMD git history is the
  only true as-of source we have (keyless, G6-compliant).
- Baseline fitting is no-hindsight INCLUDING its fit years: the
  2021-01-14 vintage carries no 2015 data for Germany, so that
  vintage's baseline fits on 2016-2019 — the same kk-linear form on
  the years actually available (>= MIN_FIT_YEARS required), exactly
  what a real-time analyst could have done. Reporting units also shift
  under replay (Albania was weekly in Jan 2021, monthly later): excess
  SUMS are comparable across vintages, period counts are not.

The replay measures: per vintage and country, the 2020 excess-death
estimate computable from that vintage alone, versus the final figure
from the committed 2026-08-17 snapshot — the real-time error the P4
first-print-settles rule accepts in exchange for never restating.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from tly import numeric  # noqa: F401
from tly.baseline import FIT_YEARS, excess_series, fit_baseline
from tly.wmd import DeathsCell, parse_wmd

REPO_ROOT = Path(__file__).resolve().parent.parent
VINTAGE_FIXTURE = (
    REPO_ROOT / "data" / "snapshots" / "2026-08-25" / "fixtures" / "wmd_vintages_alb_deu.json"
)
FINAL_WMD = REPO_ROOT / "data" / "snapshots" / "2026-08-17" / "wmd_world_mortality.csv"
PANEL = ("ALB", "DEU")
MIN_FIT_YEARS = 4
ISO3_TO_NAME = {"ALB": "Albania", "DEU": "Germany"}


@dataclass(frozen=True)
class ReplayPoint:
    vintage: str  # 'final' or the vintage date
    iso3: str
    fit_years: tuple[int, ...]
    time_unit: str
    periods_2020: int
    excess_2020: Decimal

    def error_vs(self, final: "ReplayPoint") -> tuple[Decimal, Decimal]:
        """(absolute error, percent of final)."""
        err = self.excess_2020 - final.excess_2020
        return err, (err / final.excess_2020 * 100)


def load_vintage_cells(fixture: dict, vintage: str, iso3: str) -> list[DeathsCell]:
    rows = fixture[vintage]["countries"][iso3]
    return [
        DeathsCell(
            iso3=iso3,
            country=ISO3_TO_NAME[iso3],
            year=year,
            time=time,
            time_unit=unit,
            deaths=Decimal(deaths),
        )
        for year, time, unit, deaths in rows
    ]


def replay_point(cells: list[DeathsCell], vintage: str, iso3: str) -> ReplayPoint:
    """The 2020 excess estimate computable from ``cells`` alone."""
    available = tuple(y for y in FIT_YEARS if any(c.year == y for c in cells if c.iso3 == iso3))
    if len(available) < MIN_FIT_YEARS:
        raise ValueError(
            f"{vintage}/{iso3}: only {len(available)} fit years available — "
            f"below the {MIN_FIT_YEARS}-year floor, refusing a baseline"
        )
    baseline = fit_baseline(cells, iso3, fit_years=available)
    obs = excess_series(cells, baseline, 2020)
    unit = next(c.time_unit for c in cells if c.iso3 == iso3 and c.year == 2020)
    return ReplayPoint(
        vintage=vintage,
        iso3=iso3,
        fit_years=available,
        time_unit=unit,
        periods_2020=len(obs),
        excess_2020=sum((o.excess for o in obs), Decimal(0)),
    )


def run_replay() -> dict[str, dict[str, ReplayPoint]]:
    """{iso3: {vintage-or-'final': ReplayPoint}} over all true vintages."""
    fixture = json.loads(VINTAGE_FIXTURE.read_text(encoding="utf-8"))
    final_cells = parse_wmd(FINAL_WMD, countries=set(PANEL))
    out: dict[str, dict[str, ReplayPoint]] = {}
    for iso3 in PANEL:
        out[iso3] = {"final": replay_point(final_cells, "final", iso3)}
        for vintage in sorted(fixture):
            cells = load_vintage_cells(fixture, vintage, iso3)
            out[iso3][vintage] = replay_point(cells, vintage, iso3)
    return out
