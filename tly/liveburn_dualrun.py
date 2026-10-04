"""Live-burn dual run (item 3, 2026-10-03): what weekly prints would do
if the measured excess-death burn fed settlement today.

Everything recomputes from committed snapshots; this module writes the
numbers the activation proposal will cite. ANALYSIS, not pipeline: the
settlement path is untouched until a governed version bump.

Method, stated:
- Panel: Eurostat demo_r_mwk_ts full history (38 geos, committed
  2026-08-25). Per-country kk-linear baseline on 2015-2019; excess =
  observed - expected, per ISO week of 2026, through the >=20-country
  panel edge.
- Conversion: excess x (0.7*e(75.5) + 0.3*e(85.5)) on the LIVE
  settlement table (WPP 2023) — the registered age profile.
- World scaling: divide by the panel's measured coverage share
  (panel 2019 deaths / WPP world 2019 deaths). Measured over measured,
  zero free parameters — the COVID-gate convention.
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


def run(year: int = 2026) -> dict:
    cells = parse_eurostat_weekly(PANEL)
    edge = weekly_panel_edge(cells)
    lt = parse_life_table_ex(LT_FIX, {2023}, {"World"})
    anchors = ex_anchors(lt, "World", 2023)
    conv = Decimal("0.7") * e_interp(anchors, Decimal("75.5")) + Decimal("0.3") * e_interp(
        anchors, Decimal("85.5")
    )

    panel_2019 = sum((c.deaths for c in cells if c.year == 2019), Decimal(0))
    rows = list(csv.reader(io.StringIO(OWID_BD.read_text(encoding="utf-8"))))
    di = rows[0].index("deaths__sex_all__age_all__variant_estimates")
    world_2019 = next(
        Decimal(r[di]) for r in rows[1:] if r[1] == "OWID_WRL" and r[2] == "2019" and r[di]
    )
    coverage = panel_2019 / world_2019

    week_excess: dict[int, Decimal] = {}
    week_countries: dict[int, int] = {}
    for g in sorted({c.iso3 for c in cells}):
        sub = [c for c in cells if c.iso3 == g]
        bl = fit_baseline(sub, g)
        for obs in excess_series(sub, bl, year):
            if obs.period <= edge[1]:
                week_excess[obs.period] = week_excess.get(obs.period, Decimal(0)) + obs.excess
                week_countries[obs.period] = week_countries.get(obs.period, 0) + 1

    weeks = []
    for wk in sorted(week_excess):
        ly = week_excess[wk] * conv / coverage
        weeks.append(
            {
                "week": f"{year}-W{wk:02d}",
                "panel_excess_deaths": str(week_excess[wk].quantize(Decimal("0.1"))),
                "countries": week_countries[wk],
                "world_burn_ly": str(ly.quantize(Decimal("1"))),
                "ppb_of_s": str((ly / S_LIVE * 10**9).quantize(Decimal("0.01"))),
            }
        )
    cum = sum(week_excess.values(), Decimal(0)) * conv / coverage
    cum_no_edge = (
        sum((v for k, v in week_excess.items() if k < edge[1]), Decimal(0)) * conv / coverage
    )
    return {
        "generated": "2026-10-03",
        "panel_edge": f"{edge[0]}-W{edge[1]:02d}",
        "ly_per_excess_death": str(conv.quantize(Decimal("0.0001"))),
        "coverage_share": str(coverage.quantize(Decimal("0.0001"))),
        "noise_amplification": str((1 / coverage).quantize(Decimal("0.1"))),
        "weeks": weeks,
        "cumulative_ppm_of_s": str((cum / S_LIVE * 10**6).quantize(Decimal("0.001"))),
        "cumulative_ppm_excl_edge_week": str(
            (cum_no_edge / S_LIVE * 10**6).quantize(Decimal("0.001"))
        ),
    }


if __name__ == "__main__":
    out = run()
    path = REPO_ROOT / "docs/reports/liveburn_dualrun.json"
    path.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(
        f"written {path.name}: cum {out['cumulative_ppm_of_s']} ppm "
        f"({out['cumulative_ppm_excl_edge_week']} excl edge week)"
    )
    sys.exit(0)
