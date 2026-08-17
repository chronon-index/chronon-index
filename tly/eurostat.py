"""Eurostat weekly-deaths feed (SPEC#2; RP Part II D3; B-uc2-14).

THE live nowcast source: ``demo_r_mwk_ts`` (total weekly deaths by
country) is keyless, CLEARED (EU CC BY 4.0 — docs/LICENSING.md), and
current to within ~2 weeks (2026-W31 in the 2026-08-17 snapshot, probed
live). This is what closes the staleness gap WMD left (its CSV ends
2024-12) without touching the login-walled STMF.

Output is the same DeathsCell shape the WMD parser produces, so the
kk-linear baseline, excess series, and P7 coverage machinery work
unchanged on this feed. Eurostat's ISO-2 geo codes are mapped to ISO3;
aggregate geos (EU27_2020 …) are skipped explicitly, never summed into
country series. Decimal from parse (G1).
"""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

from tly.wmd import DeathsCell

# Eurostat ISO-2 (incl. EL/UK quirks) -> ISO3. Aggregates intentionally absent.
GEO_TO_ISO3: dict[str, str] = {
    "BE": "BEL",
    "BG": "BGR",
    "CZ": "CZE",
    "DK": "DNK",
    "DE": "DEU",
    "EE": "EST",
    "IE": "IRL",
    "EL": "GRC",
    "ES": "ESP",
    "FR": "FRA",
    "HR": "HRV",
    "IT": "ITA",
    "CY": "CYP",
    "LV": "LVA",
    "LT": "LTU",
    "LU": "LUX",
    "HU": "HUN",
    "MT": "MLT",
    "NL": "NLD",
    "AT": "AUT",
    "PL": "POL",
    "PT": "PRT",
    "RO": "ROU",
    "SI": "SVN",
    "SK": "SVK",
    "FI": "FIN",
    "SE": "SWE",
    "IS": "ISL",
    "LI": "LIE",
    "NO": "NOR",
    "CH": "CHE",
    "UK": "GBR",
    "ME": "MNE",
    "MK": "MKD",
    "AL": "ALB",
    "RS": "SRB",
    "TR": "TUR",
    "AD": "AND",
    "AM": "ARM",
    "GE": "GEO",
    "AZ": "AZE",
    "UA": "UKR",
    "MD": "MDA",
    "XK": "XKX",
}


class EurostatFormatError(ValueError):
    pass


def parse_eurostat_weekly(path: Path, countries: set[str] | None = None) -> list[DeathsCell]:
    """Decode the JSON-stat cube into DeathsCells (weekly, ISO3-keyed).

    JSON-stat linearizes the cube row-major over ``id``-ordered dimensions;
    absent keys are missing observations (reporting lag) — they simply do
    not become cells, and the P7 coverage layer surfaces the gap.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    dims = data["id"]
    sizes = data["size"]
    if "geo" not in dims or "time" not in dims:
        raise EurostatFormatError("cube lacks geo/time dimensions")

    indices: dict[str, dict[str, int]] = {
        d: data["dimension"][d]["category"]["index"] for d in dims
    }
    labels = data["dimension"]["geo"]["category"]["label"]
    geo_list = sorted(indices["geo"], key=indices["geo"].__getitem__)
    time_list = sorted(indices["time"], key=indices["time"].__getitem__)

    # linear index strides, row-major over dims order
    strides: dict[str, int] = {}
    acc = 1
    for d in reversed(dims):
        strides[d] = acc
        acc *= sizes[dims.index(d)]

    fixed_offset = 0
    for d in dims:
        if d in ("geo", "time"):
            continue
        if sizes[dims.index(d)] != 1:
            raise EurostatFormatError(f"expected singleton dimension {d}")
        # singleton index 0 contributes nothing

    values = data["value"]
    cells: list[DeathsCell] = []
    for geo in geo_list:
        iso3 = GEO_TO_ISO3.get(geo)
        if iso3 is None:
            continue  # aggregates (EU27_2020 …) and unmapped codes: skipped
        if countries is not None and iso3 not in countries:
            continue
        g_off = fixed_offset + indices["geo"][geo] * strides["geo"]
        for week in time_list:
            key = str(g_off + indices["time"][week] * strides["time"])
            if key not in values:
                continue  # reporting lag — absent, not zero
            year_s, week_s = week.split("-W")
            cells.append(
                DeathsCell(
                    iso3=iso3,
                    country=labels.get(geo, geo),
                    year=int(year_s),
                    time=int(week_s),
                    time_unit="weekly",
                    deaths=Decimal(str(values[key])),
                )
            )
    if not cells:
        raise EurostatFormatError("no observations decoded")
    return cells


def latest_week(cells: list[DeathsCell]) -> tuple[int, int]:
    return max((c.year, c.time) for c in cells)
