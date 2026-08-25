"""End-to-end settlement pipeline (SPEC#3 AC-3.1; B-uc3-03).

One callable path from committed snapshots to a rendered print — the unit
of reproducibility. ``python -m tly.pipeline <epoch>`` prints the rendered
JSON to stdout, which is how the P5 test diffs two fully separate
processes byte for byte.

v0-equivalent inputs: 2026-08-16 snapshot (WHO 2019 table × WPP2024
population) for S/Ē/N; WMD (DEU+ALB, 2021) for the P7 coverage block;
burn 0 pending the live shock mesh.
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
from tly.prints import WeeklyPrint
from tly.stock import stamp
from tly.wmd import parse_wmd

REPO_ROOT = Path(__file__).resolve().parent.parent
SNAP16 = REPO_ROOT / "data" / "snapshots" / "2026-08-16"
SNAP17 = REPO_ROOT / "data" / "snapshots" / "2026-08-17"
WMD_CSV = SNAP17 / "wmd_world_mortality.csv"

COVERAGE_COUNTRIES = ("ALB", "DEU")
COVERAGE_YEAR = 2021


def build_settlement_print(epoch_utc: str, methodology_version: str | None = None) -> WeeklyPrint:
    """``methodology_version`` selects the GOVERNED parameter set for
    version-keyed terms (outsider-sim reproduces archived epochs under
    the version that produced them); None = HEAD."""
    snap = load_verified_snapshot(SNAP16)
    stock = compute_stock(snap.tables[2019], snap.bands, 2019)
    n = total_population(snap.bands)

    cells = parse_wmd(WMD_CSV, countries=set(COVERAGE_COUNTRIES))
    records = [
        coverage_metadata(cells, fit_baseline(cells, iso3), COVERAGE_YEAR)
        for iso3 in COVERAGE_COUNTRIES
    ]

    return WeeklyPrint(
        epoch_utc=epoch_utc,
        series_label="SETTLEMENT",
        s_life_years=stock.s_life_years,
        e_bar_years=e_bar(stock, n),
        n_persons=n,
        burn_life_years=Decimal(0),
        coverage=coverage_block(records),
        accuracy=accuracy_block(stock.s_life_years, methodology_version),
        provenance=stamp([SNAP16, SNAP17]),
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
