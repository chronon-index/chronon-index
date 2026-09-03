"""End-to-end settlement pipeline (SPEC#3 AC-3.1; B-uc3-03).

One callable path from committed snapshots to a rendered print — the unit
of reproducibility. ``python -m tly.pipeline <epoch>`` prints the rendered
JSON to stdout, which is how the P5 test diffs two fully separate
processes byte for byte.

Inputs are VERSION-KEYED (the outsider-sim reproduces archived epochs
under the version that produced them):
- v0.7.0+ (G5, signed off 2026-09-04): WPP 2024 complete life table ×
  single-age population, World 2023, single-age estimator — from the
  committed 2026-08-17 fixtures (CC BY 3.0 IGO; attribution in
  provenance).
- pre-v0.7.0: WHO GHO 2019 banded table × WPP2024 banded population
  (the 2026-08-16 snapshot) — kept so history keeps reproducing.
WMD (DEU+ALB, 2021) supplies the P7 coverage block on both paths; burn
0 pending the live shock mesh.
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from tly.baseline import coverage_block, coverage_metadata, fit_baseline
from tly.error_budget import accuracy_block
from tly.estimator import compute_stock, e_bar, total_population
from tly.loader import load_verified_snapshot
from tly.methodology import METHODOLOGY_VERSION
from tly.prints import WeeklyPrint
from tly.stock import compute_location_stock, stamp
from tly.wmd import parse_wmd
from tly.wpp import (
    ex_anchors,
    parse_life_table_ex,
    parse_population_single_age,
    population_by_age,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
SNAP16 = REPO_ROOT / "data" / "snapshots" / "2026-08-16"
SNAP17 = REPO_ROOT / "data" / "snapshots" / "2026-08-17"
WMD_CSV = SNAP17 / "wmd_world_mortality.csv"
WPP_POP_FIX = SNAP17 / "fixtures" / "wpp_pop_single_age_fixture.csv.gz"
WPP_LT_FIX = SNAP17 / "fixtures" / "wpp_lt_complete_fixture.csv.gz"
STRUCTURE_YEAR = 2023  # WPP path structure year (G5)

COVERAGE_COUNTRIES = ("ALB", "DEU")
COVERAGE_YEAR = 2021

# versions whose settlement S was computed on the WHO-banded path
_PRE_G5_VERSIONS = frozenset(
    {
        "v0.1.0-reconstruction",
        "v0.2.0-reconstruction",
        "v0.3.0-reconstruction",
        "v0.4.0-reconstruction",
        "v0.5.0-reconstruction",
        "v0.6.0-reconstruction",
    }
)

WPP_ATTRIBUTION = (
    "United Nations, Department of Economic and Social Affairs, Population "
    "Division (2024). World Population Prospects 2024. Licensed under "
    "CC BY 3.0 IGO."
)


def _stock_who_banded() -> tuple[Decimal, Decimal, Decimal]:
    snap = load_verified_snapshot(SNAP16)
    stock = compute_stock(snap.tables[2019], snap.bands, 2019)
    n = total_population(snap.bands)
    return stock.s_life_years, e_bar(stock, n), n


def _stock_wpp_single_age() -> tuple[Decimal, Decimal, Decimal]:
    pop = parse_population_single_age(WPP_POP_FIX, {STRUCTURE_YEAR}, {"World"})
    lt = parse_life_table_ex(WPP_LT_FIX, {STRUCTURE_YEAR}, {"World"})
    world = compute_location_stock(
        population_by_age(pop, "World", STRUCTURE_YEAR),
        ex_anchors(lt, "World", STRUCTURE_YEAR),
        location="World",
        year=STRUCTURE_YEAR,
        sex="total",
    )
    return world.s_life_years, world.e_bar, world.n_persons


def build_settlement_print(epoch_utc: str, methodology_version: str | None = None) -> WeeklyPrint:
    """``methodology_version`` selects the GOVERNED computation for that
    version — both the parameter set AND the source-of-record path
    (outsider-sim reproduces archived epochs under the version that
    produced them); None = HEAD."""
    version = methodology_version or METHODOLOGY_VERSION
    if version in _PRE_G5_VERSIONS:
        s, ebar, n = _stock_who_banded()
    else:
        s, ebar, n = _stock_wpp_single_age()

    cells = parse_wmd(WMD_CSV, countries=set(COVERAGE_COUNTRIES))
    records = [
        coverage_metadata(cells, fit_baseline(cells, iso3), COVERAGE_YEAR)
        for iso3 in COVERAGE_COUNTRIES
    ]

    if version in _PRE_G5_VERSIONS:
        provenance = stamp([SNAP16, SNAP17])  # pre-G5: cite-everything, as archived
    else:
        provenance = stamp(
            [SNAP17],
            consumed={
                SNAP17.name: [
                    "fixtures/wpp_pop_single_age_fixture.csv.gz",
                    "fixtures/wpp_lt_complete_fixture.csv.gz",
                    "wmd_world_mortality.csv",
                ]
            },
        )
        provenance["attribution"] = WPP_ATTRIBUTION
    return WeeklyPrint(
        epoch_utc=epoch_utc,
        series_label="SETTLEMENT",
        s_life_years=s,
        e_bar_years=ebar,
        n_persons=n,
        burn_life_years=Decimal(0),
        coverage=coverage_block(records),
        accuracy=accuracy_block(s, methodology_version),
        provenance=provenance,
    )


def current_epoch(now: datetime | None = None) -> str:
    """The most recent Monday-12:00-UTC epoch at ``now`` (UTC). Injectable
    for tests; the CI weekly job is the only caller that omits ``now``."""
    if now is None:
        now = datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    now = now.astimezone(timezone.utc)
    days_back = now.weekday()  # Monday=0
    candidate = (now - timedelta(days=days_back)).replace(
        hour=12, minute=0, second=0, microsecond=0
    )
    if candidate > now:  # it is Monday but before noon UTC
        candidate -= timedelta(days=7)
    return candidate.isoformat()


def main(argv: list[str]) -> int:
    if argv == ["--current-epoch"]:
        sys.stdout.write(build_settlement_print(current_epoch()).render())
        return 0
    if len(argv) != 1:
        print("usage: python -m tly.pipeline <epoch-utc>|--current-epoch", file=sys.stderr)
        return 2
    sys.stdout.write(build_settlement_print(argv[0]).render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
