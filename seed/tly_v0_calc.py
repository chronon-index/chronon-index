#!/usr/bin/env python3.12
"""tly_v0_calc.py — v0 calculator for S, humanity's total remaining life-years.

Reconstructed 2026-08-16 from DECISIONS.md, RESEARCH_PROGRAM.md and
RALPH_LOOP.md after loss of the original; pending Ben's review.

Estimator E2 (RESEARCH_PROGRAM Part IX):
    S = sum over bands of N_band * e(mid(band))
    - band midpoint by the uniform-within-band assumption
    - e() by piecewise-linear interpolation on the exact-age anchors of the
      abridged life table; flat beyond the last anchor (age 85)

All arithmetic is Decimal (precision 34, ROUND_HALF_EVEN) from the moment
values leave parsing. Floats never touch published numbers (JSON is parsed
with parse_float=Decimal).

Modes:
    --fetch     fetch sources over the network, write a content-hashed
                snapshot + manifest.json, then compute from that snapshot.
    (default)   offline: read the committed snapshot, recompute, write results.

Python 3.12, stdlib only. No secrets; all endpoints keyless.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import random
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from decimal import ROUND_HALF_EVEN, Decimal, getcontext
from pathlib import Path

getcontext().prec = 34
getcontext().rounding = ROUND_HALF_EVEN

REPO_ROOT = Path(__file__).resolve().parent.parent
SNAPSHOTS_ROOT = REPO_ROOT / "data" / "snapshots"
DEFAULT_RESULTS = REPO_ROOT / "seed" / "results_v0.json"

USER_AGENT = (
    "tly-research/0.1 (benjaminpauls.stocks@gmail.com; "
    "open reproducible index research; github: pending)"
)

BILLION = Decimal(10) ** 9
Q4 = Decimal("0.0001")

# ---------------------------------------------------------------------------
# Sources. Few-and-large requests; World Bank API deliberately NOT used
# (WAF-blocked this project on 2026-08-16 — see RALPH_LOOP.md section 6).
# GHO indicator LIFE_0000000035 = "ex - expectation of life at age x",
# verified against https://ghoapi.azureedge.net/api/Indicator on 2026-08-16.
# ---------------------------------------------------------------------------
SOURCES = {
    "gho_ex_global_btsx_2019_2021.json": (
        "https://ghoapi.azureedge.net/api/LIFE_0000000035"
        "?$filter=SpatialDim%20eq%20%27GLOBAL%27%20and%20Dim1%20eq%20%27SEX_BTSX%27"
        "%20and%20(TimeDim%20eq%202019%20or%20TimeDim%20eq%202021)"
    ),
    "gho_lifetable_indicator_list.json": (
        "https://ghoapi.azureedge.net/api/Indicator"
        "?$filter=contains(IndicatorCode,%20%27LIFE_%27)"
    ),
    "owid_population_5yr_world.csv": (
        "https://ourworldindata.org/grapher/population-by-five-year-age-group.csv"
        "?v=1&csvType=filtered&useColumnShortNames=true&country=~OWID_WRL"
    ),
    "owid_population_5yr.metadata.json": (
        "https://ourworldindata.org/grapher/population-by-five-year-age-group.metadata.json"
        "?v=1&csvType=filtered&useColumnShortNames=true&country=~OWID_WRL"
    ),
    "owid_births_deaths_world.csv": (
        "https://ourworldindata.org/grapher/births-and-deaths-projected-to-2100.csv"
        "?v=1&csvType=filtered&useColumnShortNames=true&country=~OWID_WRL"
    ),
    "owid_births_deaths.metadata.json": (
        "https://ourworldindata.org/grapher/births-and-deaths-projected-to-2100.metadata.json"
        "?v=1&csvType=filtered&useColumnShortNames=true&country=~OWID_WRL"
    ),
}

POPULATION_YEAR = 2023
LIFE_TABLE_YEARS = (2019, 2021)

# GHO abridged age-group codes -> exact-age anchor (start of interval).
GHO_AGE_ANCHORS = {"AGEGROUP_YEARS00-01": 0, "AGEGROUP_YEARS01-04": 1}
for _a in range(5, 85, 5):
    GHO_AGE_ANCHORS[f"AGEGROUP_YEARS{_a:02d}-{_a + 4:02d}"] = _a
GHO_AGE_ANCHORS["AGEGROUP_YEARS85PLUS"] = 85

TARGETS_FROM_DECISIONS = {
    "S_2019_billions": "362.4126",
    "S_2021_billions": "348.1905",
    "E_bar_years": "44.7880",
    "N_billions": "8.0917",
    "mint_B_times_e0_billions": "9.6606",
    "spend_minus_N_billions": "-8.0917",
    "drift_billions": "1.0394",
    "g_pct_per_yr": "0.7197",
}


# ---------------------------------------------------------------------------
# Fetch (snapshot-first)
# ---------------------------------------------------------------------------
def _fetch_url(url: str, attempts: int = 4) -> bytes:
    last_err: Exception | None = None
    for attempt in range(attempts):
        if attempt:
            delay = (2**attempt) + random.uniform(0.0, 1.5)  # backoff with jitter
            time.sleep(delay)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=120) as resp:
                return resp.read()
        except (urllib.error.URLError, TimeoutError, OSError) as err:
            last_err = err
            print(f"  attempt {attempt + 1}/{attempts} failed: {err}", file=sys.stderr)
    raise RuntimeError(f"fetch failed after {attempts} attempts: {url}") from last_err


def fetch_snapshot(snapshot_dir: Path) -> Path:
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict = {
        "snapshot_date": snapshot_dir.name,
        "note": (
            "Reconstructed 2026-08-16 from DECISIONS.md, RESEARCH_PROGRAM.md and "
            "RALPH_LOOP.md after loss of the original; pending Ben's review."
        ),
        "network_policy": (
            "User-Agent sent; few-and-large requests; exponential backoff with "
            "jitter; World Bank API not used (WAF-blocked 2026-08-16)."
        ),
        "files": {},
    }
    for name, url in SOURCES.items():
        print(f"FETCH {url}")
        body = _fetch_url(url)
        (snapshot_dir / name).write_bytes(body)
        manifest["files"][name] = {
            "source_url": url,
            "retrieved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "sha256": hashlib.sha256(body).hexdigest(),
            "bytes": len(body),
        }
    (snapshot_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"snapshot written: {snapshot_dir}")
    return snapshot_dir


# ---------------------------------------------------------------------------
# Load (offline; everything Decimal from the moment it leaves parsing)
# ---------------------------------------------------------------------------
def load_snapshot(snapshot_dir: Path) -> dict:
    manifest = json.loads((snapshot_dir / "manifest.json").read_text(encoding="utf-8"))

    # WHO GHO ex — parse_float=Decimal keeps floats out entirely.
    gho = json.loads(
        (snapshot_dir / "gho_ex_global_btsx_2019_2021.json").read_text(encoding="utf-8"),
        parse_float=Decimal,
    )
    tables: dict[int, dict[int, Decimal]] = {}
    for row in gho["value"]:
        year = int(row["TimeDim"])
        if year not in LIFE_TABLE_YEARS:
            continue
        if row["SpatialDim"] != "GLOBAL" or row["Dim1"] != "SEX_BTSX":
            raise ValueError(f"unexpected GHO row scope: {row['SpatialDim']}/{row['Dim1']}")
        age = GHO_AGE_ANCHORS[row["Dim2"]]
        val = row["NumericValue"]
        if not isinstance(val, Decimal):  # ints arrive as int; never float
            val = Decimal(val)
        tables.setdefault(year, {})[age] = val
    for year in LIFE_TABLE_YEARS:
        if sorted(tables.get(year, {})) != sorted(GHO_AGE_ANCHORS.values()):
            raise ValueError(f"incomplete GHO life table for {year}")

    # OWID population by 5-year band, World, both sexes, WPP 2024 estimates.
    pop_text = (snapshot_dir / "owid_population_5yr_world.csv").read_text(encoding="utf-8")
    rows = list(csv.reader(io.StringIO(pop_text)))
    header, data = rows[0], rows[1:]
    world_row = None
    for r in data:
        if r[1] == "OWID_WRL" and int(r[2]) == POPULATION_YEAR:
            world_row = r
            break
    if world_row is None:
        raise ValueError(f"no OWID_WRL row for {POPULATION_YEAR} in population snapshot")
    bands: list[tuple[str, Decimal, Decimal]] = []  # (label, midpoint, N_band)
    for col, val in zip(header[3:], world_row[3:]):
        # column form: population__sex_all__age_0_4__variant_estimates
        agepart = col.split("__age_")[1].split("__")[0]
        if agepart.endswith("plus"):
            lo = Decimal(agepart[:-4])
            # Open-ended band: no width, so uniform-within-band gives no
            # midpoint. Convention: lo + 2.5. Inert here — e() is flat beyond
            # the last anchor (85), so any midpoint >= 85 yields e(85+).
            mid = lo + Decimal("2.5")
            label = f"{agepart[:-4]}+"
        else:
            lo_s, hi_s = agepart.split("_")
            lo = Decimal(lo_s)
            # Band [lo, hi] of integer ages covers exact ages [lo, hi+1);
            # uniform-within-band midpoint = (lo + hi + 1) / 2.
            mid = (lo + Decimal(hi_s) + 1) / 2
            label = f"{lo_s}-{hi_s}"
        bands.append((label, mid, Decimal(val)))

    # OWID births (WPP 2024 estimates), World.
    births_text = (snapshot_dir / "owid_births_deaths_world.csv").read_text(encoding="utf-8")
    brows = list(csv.reader(io.StringIO(births_text)))
    bheader = brows[0]
    births_col = bheader.index("births__sex_all__age_all__variant_estimates")
    births: Decimal | None = None
    for r in brows[1:]:
        if r[1] == "OWID_WRL" and int(r[2]) == POPULATION_YEAR and r[births_col]:
            births = Decimal(r[births_col])
            break

    return {
        "manifest": manifest,
        "tables": tables,
        "bands": bands,
        "births": births,
        "snapshot_dir": snapshot_dir.resolve(),
    }


# ---------------------------------------------------------------------------
# Estimator E2
# ---------------------------------------------------------------------------
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


def compute(snapshot: dict) -> dict:
    tables = snapshot["tables"]
    bands = snapshot["bands"]
    births = snapshot["births"]

    n_total = sum(n for _, _, n in bands)
    s_by_year: dict[int, Decimal] = {}
    band_detail: dict[int, list] = {}
    for year in LIFE_TABLE_YEARS:
        t = tables[year]
        detail = []
        s = Decimal(0)
        for label, mid, n in bands:
            e_mid = e_interp(t, mid)
            term = n * e_mid
            s += term
            detail.append((label, str(mid), str(n), str(e_mid), str(term)))
        s_by_year[year] = s
        band_detail[year] = detail

    s2019, s2021 = s_by_year[2019], s_by_year[2021]
    e_bar = s2019 / n_total
    e0_2019 = tables[2019][0]
    e0_2021 = tables[2021][0]
    mint = births * e0_2019 if births is not None else None
    spend = -n_total

    def dev_pct(achieved: Decimal, target_key: str) -> str:
        target = Decimal(TARGETS_FROM_DECISIONS[target_key])
        return str(((achieved - target) / target * 100).quantize(Q4))

    achieved = {
        "S_2019_life_years": str(s2019),
        "S_2019_billions": str((s2019 / BILLION).quantize(Q4)),
        "S_2021_life_years": str(s2021),
        "S_2021_billions": str((s2021 / BILLION).quantize(Q4)),
        "N_persons": str(n_total),
        "N_billions": str((n_total / BILLION).quantize(Q4)),
        "E_bar_years_full": str(e_bar),
        "E_bar_years": str(e_bar.quantize(Q4)),
        "E_bar_2021_years": str((s2021 / n_total).quantize(Q4)),
        "e0_2019": str(e0_2019),
        "e0_2021": str(e0_2021),
        "births_2023": str(births) if births is not None else None,
        "mint_B_times_e0_life_years": str(mint) if mint is not None else None,
        "mint_B_times_e0_billions": (
            str((mint / BILLION).quantize(Q4)) if mint is not None else None
        ),
        "spend_minus_N_life_years": str(spend),
        "spend_minus_N_billions": str((spend / BILLION).quantize(Q4)),
    }
    deviations = {
        "S_2019_billions_pct": dev_pct(s2019 / BILLION, "S_2019_billions"),
        "S_2021_billions_pct": dev_pct(s2021 / BILLION, "S_2021_billions"),
        "E_bar_years_pct": dev_pct(e_bar, "E_bar_years"),
        "N_billions_pct": dev_pct(n_total / BILLION, "N_billions"),
        "spend_minus_N_billions_pct": dev_pct(spend / BILLION, "spend_minus_N_billions"),
    }
    if mint is not None:
        deviations["mint_B_times_e0_billions_pct"] = dev_pct(
            mint / BILLION, "mint_B_times_e0_billions"
        )

    manifest = snapshot["manifest"]
    return {
        "_note": (
            "Reconstructed 2026-08-16 from DECISIONS.md, RESEARCH_PROGRAM.md and "
            "RALPH_LOOP.md after loss of the original; pending Ben's review."
        ),
        "_method": (
            "Estimator E2 (RESEARCH_PROGRAM Part IX): S = sum over bands of "
            "N_band * e(mid(band)); midpoint by uniform-within-band; e() "
            "piecewise-linear on exact-age anchors of the WHO abridged global "
            "life table; flat beyond age 85. Decimal prec 34 ROUND_HALF_EVEN."
        ),
        "_precision": "Decimal precision 34, ROUND_HALF_EVEN; no floats",
        "snapshot_dir": str(snapshot["snapshot_dir"].relative_to(REPO_ROOT)),
        "sources": {
            name: {
                "source_url": meta["source_url"],
                "retrieved_utc": meta["retrieved_utc"],
                "sha256": meta["sha256"],
            }
            for name, meta in sorted(manifest["files"].items())
        },
        "population_year": POPULATION_YEAR,
        "life_table_years": list(LIFE_TABLE_YEARS),
        "achieved": achieved,
        "not_reproduced": {
            "drift_billions": (
                "NOT REPRODUCED in this pass: requires dE-bar/dt across "
                "successive population/life-table vintages, not fetched here."
            ),
            "g_pct_per_yr": (
                "NOT REPRODUCED in this pass: g depends on the drift term "
                "above; mint and spend alone do not determine it."
            ),
        },
        "targets_from_DECISIONS": TARGETS_FROM_DECISIONS,
        "deviation_pct": deviations,
        "band_detail": {str(y): band_detail[y] for y in LIFE_TABLE_YEARS},
    }


def render_json(results: dict) -> str:
    """Deterministic rendering — byte-identical across runs (invariant P5)."""
    return json.dumps(results, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def latest_snapshot_dir() -> Path:
    dirs = sorted(p for p in SNAPSHOTS_ROOT.iterdir() if p.is_dir())
    if not dirs:
        raise SystemExit(f"no snapshot under {SNAPSHOTS_ROOT}; run with --fetch first")
    return dirs[-1]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fetch", action="store_true", help="fetch sources, write snapshot")
    ap.add_argument("--snapshot-dir", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=DEFAULT_RESULTS)
    args = ap.parse_args(argv)

    if args.fetch:
        snap_dir = args.snapshot_dir or (
            SNAPSHOTS_ROOT / datetime.now(timezone.utc).strftime("%Y-%m-%d")
        )
        fetch_snapshot(snap_dir)
    else:
        snap_dir = args.snapshot_dir or latest_snapshot_dir()

    snapshot = load_snapshot(snap_dir)
    results = compute(snapshot)
    args.out.write_text(render_json(results), encoding="utf-8")

    a = results["achieved"]
    print("TLY v0 calculator — estimator E2 — Decimal(34, ROUND_HALF_EVEN)")
    print(f"snapshot: {results['snapshot_dir']}")
    print("sources (radical verifiability):")
    for name, meta in results["sources"].items():
        print(f"  {name}")
        print(f"    {meta['source_url']}")
        print(f"    sha256 {meta['sha256']}  retrieved {meta['retrieved_utc']}")
    print(f"S  (2019 table) = {a['S_2019_billions']}B life-years "
          f"(target {TARGETS_FROM_DECISIONS['S_2019_billions']}B)")
    print(f"S  (2021 table) = {a['S_2021_billions']}B life-years "
          f"(target {TARGETS_FROM_DECISIONS['S_2021_billions']}B)")
    print(f"E-bar           = {a['E_bar_years']} years "
          f"(target {TARGETS_FROM_DECISIONS['E_bar_years']})")
    print(f"N               = {a['N_billions']}B persons "
          f"(target {TARGETS_FROM_DECISIONS['N_billions']}B)")
    if a["mint_B_times_e0_billions"] is not None:
        print(f"mint B*e(0)     = {a['mint_B_times_e0_billions']}B "
              f"(target {TARGETS_FROM_DECISIONS['mint_B_times_e0_billions']}B)")
    print(f"spend -N        = {a['spend_minus_N_billions']}B "
          f"(target {TARGETS_FROM_DECISIONS['spend_minus_N_billions']}B)")
    print("drift, g        = NOT REPRODUCED in this pass (see results file)")
    print(f"results written: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
