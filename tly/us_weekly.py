"""CDC US weekly all-cause deaths (B-uc2-15; ruling B-uc2-02(c)).

SODA dataset ``r8kw-7aab`` — per the 2026-08-20 ruling, the ONLY
still-updating keyless US weekly all-cause feed (muzy-jte6, y5bj-9g5w,
u6jv-9ijr and xkkf-xrst all froze 2025-04-21). It carries NO age
breakdown: US age-specific work runs annual off WPP until a live keyless
age feed reappears.

The feed backfills for ~8 weeks — the newest week prints roughly half of
its final value (observed live 2026-08-24: 20,897 against a ~48k mature
level). The parser therefore CENSORS the immature tail by default; a
mature=False cell is data-in-progress, usable only by code that models
the reporting lag explicitly (the vintage-store/chain-ladder follow-up,
B-uc2-17). Decimal from parse (G1)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pathlib import Path

from tly import numeric  # noqa: F401  (configures the Decimal context)

CENSOR_WEEKS = 8  # NCHS backfill horizon per the B-uc2-02 ruling


@dataclass(frozen=True)
class UsWeekCell:
    week_ending: date
    total_deaths: Decimal | None  # None = not yet reported at pull time
    covid_deaths: Decimal | None
    mature: bool  # False inside the censor window — do not aggregate


class CdcFormatError(ValueError):
    pass


def parse_cdc_weekly(path: Path, censor_weeks: int = CENSOR_WEEKS) -> list[UsWeekCell]:
    """Parse the snapshotted SODA JSON into censored weekly cells.

    Rows must be strictly increasing by end_date (the fetch orders them);
    duplicates or disorder mean a malformed pull and raise."""
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not rows:
        raise CdcFormatError("empty CDC extract")
    cells: list[UsWeekCell] = []
    last: date | None = None
    n = len(rows)
    for i, row in enumerate(rows):
        week = date.fromisoformat(row["end_date"][:10])
        if last is not None and week <= last:
            raise CdcFormatError(f"weeks out of order at {week}")
        last = week

        def dec(field: str) -> Decimal | None:
            v = row.get(field)
            return None if v in (None, "") else Decimal(str(v))

        cells.append(
            UsWeekCell(
                week_ending=week,
                total_deaths=dec("total_deaths"),
                covid_deaths=dec("covid_19_deaths"),
                mature=(n - 1 - i) >= censor_weeks,
            )
        )
    return cells


def mature_series(cells: list[UsWeekCell]) -> list[UsWeekCell]:
    """The aggregation-safe series: mature weeks with reported totals."""
    return [c for c in cells if c.mature and c.total_deaths is not None]


def latest_mature_week(cells: list[UsWeekCell]) -> UsWeekCell:
    series = mature_series(cells)
    if not series:
        raise CdcFormatError("no mature weeks in extract")
    return series[-1]
