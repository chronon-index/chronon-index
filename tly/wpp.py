"""WPP 2024 bulk-CSV parsers (SPEC#1; source of record per SPEC#0 G5).

Streams the gzipped CSV_FILES surfaces (population by single age × sex ×
country) into Decimal structures. File units are THOUSANDS of persons with
3 decimals; values are converted to exact person counts (× 1000 in Decimal
— exact, no rounding). Every value is Decimal from parse (G1).

Large source files are not in git (manifest records them, in_git:false);
committed fixtures derived from them keep the tests runnable everywhere.
"""

from __future__ import annotations

import csv
import gzip
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from tly import numeric  # noqa: F401  (configures the Decimal context)

THOUSAND = Decimal(1000)

SEX_COLUMNS = {"total": "PopTotal", "male": "PopMale", "female": "PopFemale"}


@dataclass(frozen=True)
class PopulationCell:
    """One (location, sex, single-age) population count, in persons."""

    loc_id: int
    iso3: str | None
    location: str
    year: int
    sex: str  # "total" | "male" | "female"
    age: int  # 0..100; 100 is the open-ended 100+ group
    persons: Decimal


def parse_population_single_age(
    path: Path,
    years: set[int],
    locations: set[str] | None = None,
    loc_types: set[str] | None = None,
) -> list[PopulationCell]:
    """Stream a WPP PopulationBySingleAgeSex CSV.gz into PopulationCells.

    ``locations`` filters on the Location name column (None = all rows —
    only sensible on fixtures; the full file has 4.1M rows). Each input row
    fans out into three cells (total/male/female).
    """
    cells: list[PopulationCell] = []
    year_strs = {str(y) for y in years}
    with gzip.open(path, "rt", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if row["Time"] not in year_strs:
                continue
            if locations is not None and row["Location"] not in locations:
                continue
            if loc_types is not None and row["LocTypeName"] not in loc_types:
                continue
            loc_id = int(row["LocID"])
            iso3 = row["ISO3_code"] or None
            location = row["Location"]
            year = int(row["Time"])
            age = int(row["AgeGrpStart"])
            for sex, col in SEX_COLUMNS.items():
                cells.append(
                    PopulationCell(
                        loc_id=loc_id,
                        iso3=iso3,
                        location=location,
                        year=year,
                        sex=sex,
                        age=age,
                        persons=Decimal(row[col]) * THOUSAND,
                    )
                )
    if not cells:
        raise ValueError(f"no rows matched years={sorted(years)} in {path.name}")
    return cells


def population_by_age(
    cells: list[PopulationCell], location: str, year: int, sex: str = "total"
) -> dict[int, Decimal]:
    """{single_age: persons} for one location/year/sex; raises if absent."""
    out = {
        c.age: c.persons
        for c in cells
        if c.location == location and c.year == year and c.sex == sex
    }
    if not out:
        raise ValueError(f"no population cells for {location}/{year}/{sex}")
    if sorted(out) != list(range(0, 101)):
        raise ValueError(f"incomplete single-age set for {location}/{year}/{sex}: {len(out)} ages")
    return out


ABRIDGED_ANCHOR_AGES = (0, 1, *range(5, 101, 5))  # 22 anchors: 0,1,5,...,100
COMPLETE_ANCHOR_AGES = tuple(range(0, 101))  # 101 single ages


@dataclass(frozen=True)
class LifeTableCell:
    """One (location, sex, exact-age) life-table e(x) value, in years."""

    loc_id: int
    iso3: str | None
    location: str
    year: int
    sex: str  # "total" | "male" | "female"
    age: int
    ex: Decimal


_WPP_SEX = {"Total": "total", "Male": "male", "Female": "female"}


def parse_life_table_ex(
    path: Path,
    years: set[int],
    locations: set[str] | None = None,
    loc_types: set[str] | None = None,
) -> list[LifeTableCell]:
    """Stream a WPP Life_Table CSV.gz (abridged or complete) into e(x) cells.

    Works for both surfaces: they share columns; only the AgeGrpStart set
    differs (validated in :func:`ex_anchors`, not here).
    """
    cells: list[LifeTableCell] = []
    year_strs = {str(y) for y in years}
    with gzip.open(path, "rt", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if row["Time"] not in year_strs:
                continue
            if locations is not None and row["Location"] not in locations:
                continue
            if loc_types is not None and row["LocTypeName"] not in loc_types:
                continue
            cells.append(
                LifeTableCell(
                    loc_id=int(row["LocID"]),
                    iso3=row["ISO3_code"] or None,
                    location=row["Location"],
                    year=int(row["Time"]),
                    sex=_WPP_SEX[row["Sex"]],
                    age=int(row["AgeGrpStart"]),
                    ex=Decimal(row["ex"]),
                )
            )
    if not cells:
        raise ValueError(f"no rows matched years={sorted(years)} in {path.name}")
    return cells


def ex_anchors(
    cells: list[LifeTableCell], location: str, year: int, sex: str = "total"
) -> dict[int, Decimal]:
    """{exact_age: e(x)} for one location/year/sex.

    Accepts exactly the abridged (22-anchor) or complete (101-anchor) age
    set; anything else — a partial table — raises rather than parsing.
    """
    out = {c.age: c.ex for c in cells if c.location == location and c.year == year and c.sex == sex}
    if not out:
        raise ValueError(f"no life-table cells for {location}/{year}/{sex}")
    ages = tuple(sorted(out))
    if ages not in (ABRIDGED_ANCHOR_AGES, COMPLETE_ANCHOR_AGES):
        raise ValueError(f"unexpected anchor set for {location}/{year}/{sex}: {len(ages)} ages")
    return out
