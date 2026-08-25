"""ONS England & Wales weekly deaths (B-uc2-18; ruling B-uc2-02(c)).

Keyless: the ONS beta API (api.beta.ons.gov.uk) and its CSV downloads
need no account or token. Dataset ``weekly-deaths-age-sex`` — one
edition per calendar year, versioned as revisions land; verified live
2026-08-25 (2026 edition v20, weeks 1-25; 2025 edition v45, 52 weeks).

SCOPE, stated: this is **England & Wales**, not the UK. Scotland (NRS)
and Northern Ireland (NISRA) publish separately and are NOT covered by
this adapter — no silent scope inflation. There is also no national
total row in the v4 CSV: the E&W total is England (E92000001) + Wales
(W92000004), computed here with both halves required.

Two bases, opposite maturity: REGISTRATIONS are complete when published
(registration lag folds deaths into later weeks but a published week
does not restate), while OCCURRENCES backfill as late registrations
arrive — occurrence cells are revision-prone and callers must choose
the basis explicitly; aggregation defaults to registrations.

Decimal from parse (G1); malformed pulls raise, never coerce.
"""

from __future__ import annotations

import csv
import gzip
import io
import json
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from tly import numeric  # noqa: F401  (configures the Decimal context)
from tly.snapshot import fetch_url

GEO_ENGLAND = "E92000001"
GEO_WALES = "W92000004"
REGISTRATIONS = "registrations"
OCCURRENCES = "occurrences"
API_BASE = "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-age-sex"


class OnsFormatError(ValueError):
    pass


@dataclass(frozen=True)
class OnsWeekCell:
    year: int
    week: int
    geography: str  # administrative-geography code
    sex: str  # all | female | male
    age_group: str  # 'all-ages' or an ONS band like '85-89'
    basis: str  # registrations | occurrences
    deaths: Decimal


def parse_ons_weekly(path: Path) -> list[OnsWeekCell]:
    """Parse a v4 CSV (plain or .gz) into cells. Raises on unknown sex or
    basis values, non-integer counts, or malformed week labels."""
    raw = path.read_bytes()
    if path.suffix == ".gz":
        raw = gzip.decompress(raw)
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8")))
    cells: list[OnsWeekCell] = []
    for row in reader:
        week_label = row["week-number"]
        if not week_label.startswith("week-"):
            raise OnsFormatError(f"malformed week label {week_label!r}")
        sex = row["sex"]
        if sex not in ("all", "female", "male"):
            raise OnsFormatError(f"unknown sex {sex!r}")
        basis = row["registration-or-occurrence"]
        if basis not in (REGISTRATIONS, OCCURRENCES):
            raise OnsFormatError(f"unknown basis {basis!r}")
        count = row["v4_0"]
        if not count.isdigit():
            raise OnsFormatError(f"non-integer count {count!r}")
        cells.append(
            OnsWeekCell(
                year=int(row["calendar-years"]),
                week=int(week_label[5:]),
                geography=row["administrative-geography"],
                sex=sex,
                age_group=row["age-groups"],
                basis=basis,
                deaths=Decimal(count),
            )
        )
    if not cells:
        raise OnsFormatError("empty ONS extract")
    return cells


def ew_weekly_totals(
    cells: list[OnsWeekCell], basis: str = REGISTRATIONS
) -> dict[tuple[int, int], Decimal]:
    """{(year, week): England+Wales all-sex all-age deaths}. A week
    missing either national half raises — no silent partial totals."""
    halves: dict[tuple[int, int], dict[str, Decimal]] = {}
    for c in cells:
        if (
            c.basis == basis
            and c.sex == "all"
            and c.age_group == "all-ages"
            and c.geography in (GEO_ENGLAND, GEO_WALES)
        ):
            halves.setdefault((c.year, c.week), {})[c.geography] = c.deaths
    totals: dict[tuple[int, int], Decimal] = {}
    for key in sorted(halves):
        pair = halves[key]
        if set(pair) != {GEO_ENGLAND, GEO_WALES}:
            raise OnsFormatError(
                f"{key[0]}-W{key[1]:02d}: missing national half "
                f"{sorted({GEO_ENGLAND, GEO_WALES} - set(pair))} — "
                "refusing a partial England+Wales total"
            )
        totals[key] = pair[GEO_ENGLAND] + pair[GEO_WALES]
    return totals


def latest_csv_url(year: int) -> str:
    """Resolve the current year-edition's newest CSV download URL via the
    keyless API (editions revise weekly; the URL is version-pinned)."""
    editions = json.loads(fetch_url(f"{API_BASE}/editions").decode("utf-8"))
    for item in editions.get("items", []):
        if item.get("edition") == str(year):
            version_href = item["links"]["latest_version"]["href"]
            version = json.loads(fetch_url(version_href).decode("utf-8"))
            return version["downloads"]["csv"]["href"]
    raise OnsFormatError(f"no ONS weekly-deaths edition for {year}")
