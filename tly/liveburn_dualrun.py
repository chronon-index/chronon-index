"""Live-burn dual run v2 (2026-10-03; v1 corrected by refutation pass 1,
~/coordinator/data/refutations/saeculum-liveburn-20261003-2044-pass1.md).

What pass 1 established, now built in:
- The SIGN of 2026 "excess" is set by the baseline policy, not by 2026
  mortality: the kk-linear 2015-2019 fit extrapolates 9 years from its
  window centre. v2 therefore reports a baseline-sensitivity TABLE
  (methods x windows, plus the same method applied to 2024/2025) instead
  of one number.
- Coverage uses the REPORTING SET per week (countries actually present
  that week), not the static 38-geo panel: 4 geos have no 2026 data at
  all. v1 magnitudes were 17-32% low.
- W27 is NOT a composition artefact: on the identical 26-country set
  W26 is +5,634 and W27 +15,465. W27 is dominated by Germany, where the
  2015 July heat wave drags the fitted slope to -500.7/yr (kk-expected
  12,510 vs its own 2015-19 mean 17,016 vs 2023-25 actuals 17.2-18.1k):
  roughly half baseline artefact, half a real late-June heat spike.

Known proxies, stated: conversion uses the WORLD table e-profile
(9.289 LY/death); pass 1 estimates a Europe-table profile at ~10.26 —
the panel is older than the world, so world-scaling with the world
profile understates the panel's own LY somewhat while the coverage
division assumes panel excess is representative of the world. All 2026
Eurostat cells are flagged provisional ("p"); pass 1 measured net
revisions of -44 deaths across 2,560 cells to date.

ANALYSIS only; settlement untouched until a governed bump.
"""

from __future__ import annotations

import csv
import io
import json
import sys
from decimal import Decimal
from pathlib import Path

from tly.baseline import excess_series, fit_baseline
from tly.estimator import e_interp
from tly.eurostat import parse_eurostat_weekly, weekly_panel_edge
from tly.wpp import ex_anchors, parse_life_table_ex

REPO_ROOT = Path(__file__).resolve().parent.parent
PANEL = REPO_ROOT / "data/snapshots/2026-08-25/eurostat_demo_r_mwk_ts_full.json"
LT_FIX = REPO_ROOT / "data/snapshots/2026-08-17/fixtures/wpp_lt_complete_fixture.csv.gz"
OWID_BD = REPO_ROOT / "data/snapshots/2026-08-16/owid_births_deaths_world.csv"
S_LIVE = Decimal("363511706093.96010")  # the archived 2026-09-28 print

WINDOWS = {
    "fit_2015_2019": ((2015, 2016, 2017, 2018, 2019), False),
    "mean_2015_2019": ((2015, 2016, 2017, 2018, 2019), True),
    "fit_2017_2019": ((2017, 2018, 2019), False),
    "fit_2016_2019": ((2016, 2017, 2018, 2019), False),
    "fit_2015_2018": ((2015, 2016, 2017, 2018), False),
}


def _world_2019() -> Decimal:
    rows = list(csv.reader(io.StringIO(OWID_BD.read_text(encoding="utf-8"))))
    di = rows[0].index("deaths__sex_all__age_all__variant_estimates")
    return next(Decimal(r[di]) for r in rows[1:] if r[1] == "OWID_WRL" and r[2] == "2019" and r[di])


def _conv() -> Decimal:
    lt = parse_life_table_ex(LT_FIX, {2023}, {"World"})
    anchors = ex_anchors(lt, "World", 2023)
    return Decimal("0.7") * e_interp(anchors, Decimal("75.5")) + Decimal("0.3") * e_interp(
        anchors, Decimal("85.5")
    )


def _weekly_excess(cells, geos, edge_wk, years, mean_only, target_year):
    """{week: (excess_sum, reporter_set)} under one baseline policy."""
    out: dict[int, Decimal] = {}
    reporters: dict[int, set] = {}
    for g in geos:
        sub = [c for c in cells if c.iso3 == g]
        if mean_only:
            by_p: dict[int, dict[int, Decimal]] = {}
            for c in sub:
                if c.year in years:
                    by_p.setdefault(c.time, {})[c.year] = c.deaths
            for c in sub:
                if (
                    c.year == target_year
                    and c.time <= edge_wk
                    and set(by_p.get(c.time, {})) == set(years)
                ):
                    exp = sum(by_p[c.time].values()) / len(years)
                    out[c.time] = out.get(c.time, Decimal(0)) + (c.deaths - exp)
                    reporters.setdefault(c.time, set()).add(g)
        else:
            try:
                bl = fit_baseline(sub, g, fit_years=tuple(years))
            except (ValueError, IndexError):
                continue
            for obs in excess_series(sub, bl, target_year):
                if obs.period <= edge_wk:
                    out[obs.period] = out.get(obs.period, Decimal(0)) + obs.excess
                    reporters.setdefault(obs.period, set()).add(g)
    return out, reporters


def run(year: int = 2026) -> dict:
    cells = parse_eurostat_weekly(PANEL)
    edge = weekly_panel_edge(cells)
    geos = sorted({c.iso3 for c in cells})
    conv = _conv()
    world = _world_2019()
    d2019 = {
        g: sum((c.deaths for c in cells if c.iso3 == g and c.year == 2019), Decimal(0))
        for g in geos
    }

    def ppm(week_excess: dict[int, Decimal], reporters: dict[int, set], drop_edge=False) -> str:
        total = Decimal(0)
        for wk, ex in week_excess.items():
            if drop_edge and wk == edge[1]:
                continue
            cov = sum((d2019[g] for g in reporters[wk]), Decimal(0)) / world
            total += ex * conv / cov
        return str((total / S_LIVE * 10**6).quantize(Decimal("0.01")))

    sensitivity = {}
    for name, (years, mean_only) in WINDOWS.items():
        we, rep = _weekly_excess(cells, geos, edge[1], years, mean_only, year)
        sensitivity[name] = {"cum_ppm": ppm(we, rep), "cum_ppm_excl_edge": ppm(we, rep, True)}
    same_method_prior = {}
    for y in (2024, 2025):
        we, rep = _weekly_excess(cells, geos, 52, (2015, 2016, 2017, 2018, 2019), False, y)
        same_method_prior[str(y)] = ppm(we, rep)

    we, rep = _weekly_excess(cells, geos, edge[1], (2015, 2016, 2017, 2018, 2019), False, year)
    weeks = []
    for wk in sorted(we):
        cov = sum((d2019[g] for g in rep[wk]), Decimal(0)) / world
        ly = we[wk] * conv / cov
        weeks.append(
            {
                "week": f"{year}-W{wk:02d}",
                "panel_excess_deaths": str(we[wk].quantize(Decimal("0.1"))),
                "reporters": len(rep[wk]),
                "reporting_set_coverage": str((cov * 100).quantize(Decimal("0.01"))),
                "world_burn_ly": str(ly.quantize(Decimal("1"))),
                "ppb_of_s": str((ly / S_LIVE * 10**9).quantize(Decimal("0.01"))),
            }
        )
    neg = sum(1 for w in weeks if Decimal(w["ppb_of_s"]) < 0)
    return {
        "generated": "2026-10-03",
        "version": 2,
        "corrected_by": "refutation pass 1 (saeculum-liveburn-20261003-2044-pass1)",
        "panel_edge": f"{edge[0]}-W{edge[1]:02d}",
        "ly_per_excess_death_world_table": str(conv.quantize(Decimal("0.0001"))),
        "europe_profile_proxy_note": "pass-1 estimate ~10.26 on a Europe table; world table used, proxy stated",
        "weeks": weeks,
        "negative_weeks": neg,
        "baseline_sensitivity_cum_ppm": sensitivity,
        "same_method_prior_years_cum_ppm": same_method_prior,
        "provisional_flag_note": "all 2026 cells Eurostat 'p'; pass 1 measured net revisions of -44 deaths on 2,560 cells",
    }


if __name__ == "__main__":
    out = run()
    path = REPO_ROOT / "docs/reports/liveburn_dualrun.json"
    path.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    cur = out["baseline_sensitivity_cum_ppm"]["fit_2015_2019"]
    print(
        f"v2 written: current-policy cum {cur['cum_ppm']} ppm "
        f"({cur['cum_ppm_excl_edge']} excl edge); sensitivity range across windows: "
        + ", ".join(f"{k}={v['cum_ppm']}" for k, v in out["baseline_sensitivity_cum_ppm"].items())
    )
    sys.exit(0)
