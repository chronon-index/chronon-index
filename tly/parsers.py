"""Snapshot parsers: WHO GHO life-table ex, OWID population bands, OWID births.

Ported from seed/tly_v0_calc.py (the frozen ground-truth script) at A-12.
Every numeric value is Decimal from the moment it leaves parsing (GHO JSON
via parse_float=Decimal; CSV cells via Decimal(str)) — invariant G1.

All functions read from an on-disk snapshot directory and never touch the
network (snapshot-first rule, RALPH_LOOP §6).
"""

from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from tly import numeric  # noqa: F401  (imports configure the Decimal context)

GHO_EX_FILE = "gho_ex_global_btsx_2019_2021.json"
POPULATION_FILE = "owid_population_5yr_world.csv"
BIRTHS_FILE = "owid_births_deaths_world.csv"
MANIFEST_FILE = "manifest.json"

# GHO abridged age-group codes -> exact-age anchor (start of interval).
GHO_AGE_ANCHORS = {"AGEGROUP_YEARS00-01": 0, "AGEGROUP_YEARS01-04": 1}
for _a in range(5, 85, 5):
    GHO_AGE_ANCHORS[f"AGEGROUP_YEARS{_a:02d}-{_a + 4:02d}"] = _a
GHO_AGE_ANCHORS["AGEGROUP_YEARS85PLUS"] = 85


@dataclass(frozen=True)
class PopulationBand:
    """One population band: label, uniform-within-band midpoint, headcount."""

    label: str
    midpoint: Decimal
    count: Decimal


def read_manifest(snapshot_dir: Path) -> dict:
    return json.loads((snapshot_dir / MANIFEST_FILE).read_text(encoding="utf-8"))


def parse_gho_life_tables(
    snapshot_dir: Path, years: tuple[int, ...]
) -> dict[int, dict[int, Decimal]]:
    """e(x) anchors per year from the GHO ex extract (GLOBAL, both sexes).

    Returns {year: {exact_age_anchor: e}}; raises on unexpected scope or an
    incomplete anchor set — a partial life table must never silently parse.
    """
    gho = json.loads(
        (snapshot_dir / GHO_EX_FILE).read_text(encoding="utf-8"),
        parse_float=Decimal,
    )
    tables: dict[int, dict[int, Decimal]] = {}
    for row in gho["value"]:
        year = int(row["TimeDim"])
        if year not in years:
            continue
        if row["SpatialDim"] != "GLOBAL" or row["Dim1"] != "SEX_BTSX":
            raise ValueError(f"unexpected GHO row scope: {row['SpatialDim']}/{row['Dim1']}")
        age = GHO_AGE_ANCHORS[row["Dim2"]]
        val = row["NumericValue"]
        if not isinstance(val, Decimal):  # ints arrive as int; never float
            val = Decimal(val)
        tables.setdefault(year, {})[age] = val
    for year in years:
        if sorted(tables.get(year, {})) != sorted(GHO_AGE_ANCHORS.values()):
            raise ValueError(f"incomplete GHO life table for {year}")
    return tables


def parse_population_bands(snapshot_dir: Path, year: int) -> list[PopulationBand]:
    """World population by 5-year band (OWID mirror of WPP 2024 estimates).

    Band [lo, hi] of integer ages covers exact ages [lo, hi+1); the
    uniform-within-band midpoint is (lo + hi + 1) / 2. The open-ended band
    has no width; the lo + 2.5 convention is inert because e() is flat
    beyond the last anchor (85).
    """
    pop_text = (snapshot_dir / POPULATION_FILE).read_text(encoding="utf-8")
    rows = list(csv.reader(io.StringIO(pop_text)))
    header, data = rows[0], rows[1:]
    world_row = None
    for r in data:
        if r[1] == "OWID_WRL" and int(r[2]) == year:
            world_row = r
            break
    if world_row is None:
        raise ValueError(f"no OWID_WRL row for {year} in population snapshot")
    bands: list[PopulationBand] = []
    for col, val in zip(header[3:], world_row[3:]):
        # column form: population__sex_all__age_0_4__variant_estimates
        agepart = col.split("__age_")[1].split("__")[0]
        if agepart.endswith("plus"):
            lo = Decimal(agepart[:-4])
            mid = lo + Decimal("2.5")
            label = f"{agepart[:-4]}+"
        else:
            lo_s, hi_s = agepart.split("_")
            lo = Decimal(lo_s)
            mid = (lo + Decimal(hi_s) + 1) / 2
            label = f"{lo_s}-{hi_s}"
        bands.append(PopulationBand(label=label, midpoint=mid, count=Decimal(val)))
    return bands


def parse_births(snapshot_dir: Path, year: int) -> Decimal | None:
    """World births for ``year`` (WPP 2024 estimates via OWID); None if absent."""
    births_text = (snapshot_dir / BIRTHS_FILE).read_text(encoding="utf-8")
    brows = list(csv.reader(io.StringIO(births_text)))
    bheader = brows[0]
    births_col = bheader.index("births__sex_all__age_all__variant_estimates")
    for r in brows[1:]:
        if r[1] == "OWID_WRL" and int(r[2]) == year and r[births_col]:
            return Decimal(r[births_col])
    return None
