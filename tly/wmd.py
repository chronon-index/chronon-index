"""World Mortality Dataset parser (SPEC#2; RP Part II D3; B-uc2-03a).

Karlinsky & Kobak's compilation of national all-cause deaths — weekly or
monthly per country, MIT-licensed, keyless via GitHub raw (G6-compliant).
The automated-feed candidate for the nowcast while HMD STMF sits behind a
login (see B-uc2-02).

Values are Decimal from parse (G1). The dataset carries NO age structure —
age-at-death distributions must come from elsewhere before the burn term
can price WMD excess deaths in life-years (B-uc2-05's concern, not here).
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from tly import numeric  # noqa: F401  (configures the Decimal context)

TIME_UNITS = ("weekly", "monthly")


@dataclass(frozen=True)
class DeathsCell:
    """One country-period all-cause deaths observation."""

    iso3: str
    country: str
    year: int
    time: int  # week number (weekly) or month number (monthly)
    time_unit: str
    deaths: Decimal


def parse_wmd(
    path: Path,
    countries: set[str] | None = None,
    years: set[int] | None = None,
) -> list[DeathsCell]:
    """Parse world_mortality.csv → DeathsCells, optionally filtered.

    Rejects unknown time units and malformed periods rather than guessing:
    a nowcast fed by silently misparsed periods is worse than a crash.
    """
    cells: list[DeathsCell] = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if countries is not None and row["iso3c"] not in countries:
                continue
            year = int(row["year"])
            if years is not None and year not in years:
                continue
            unit = row["time_unit"]
            if unit not in TIME_UNITS:
                raise ValueError(f"unknown time_unit {unit!r} for {row['iso3c']} {year}")
            time = int(row["time"])
            if unit == "weekly" and not 1 <= time <= 53:
                raise ValueError(f"week {time} out of range for {row['iso3c']} {year}")
            if unit == "monthly" and not 1 <= time <= 12:
                raise ValueError(f"month {time} out of range for {row['iso3c']} {year}")
            cells.append(
                DeathsCell(
                    iso3=row["iso3c"],
                    country=row["country_name"],
                    year=year,
                    time=time,
                    time_unit=unit,
                    deaths=Decimal(row["deaths"]),
                )
            )
    if not cells:
        raise ValueError(f"no rows matched filters in {path.name}")
    return cells


def country_series(cells: list[DeathsCell], iso3: str) -> list[DeathsCell]:
    """One country's observations, chronologically sorted; single-unit."""
    series = sorted((c for c in cells if c.iso3 == iso3), key=lambda c: (c.year, c.time))
    if not series:
        raise ValueError(f"no observations for {iso3}")
    units = {c.time_unit for c in series}
    if len(units) != 1:
        raise ValueError(f"{iso3} mixes time units {sorted(units)} — handle explicitly")
    return series


def latest_observation(cells: list[DeathsCell], iso3: str) -> DeathsCell:
    return country_series(cells, iso3)[-1]


def coverage(cells: list[DeathsCell]) -> dict[str, tuple[int, int]]:
    """{iso3: (latest_year, latest_period)} — the staleness map that the
    P7 coverage-honesty invariant will publish per print."""
    out: dict[str, tuple[int, int]] = {}
    for c in cells:
        key = (c.year, c.time)
        if c.iso3 not in out or key > out[c.iso3]:
            out[c.iso3] = key
    return out
