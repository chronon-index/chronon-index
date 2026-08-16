"""E1 stock engine (SPEC#1; RP Part IX E1): S = Σ N(a,s,c) × e(mid(a),s,c).

Computes S and Ē per location (and for any sex with a matching life table)
from single-age population cells and life-table e(x) anchors. The single-age
population value at age a counts persons aged [a, a+1); under the registered
uniform-within-band midpoint policy its expectancy is evaluated at a+0.5 via
the registered "linear-on-anchors, flat-tail" interpolation — one policy,
every resolution (5-year bands in v0, single ages here).

Every result is stamped with the methodology version, the policy strings,
and the snapshot manifest hashes it was computed from (AC-1.4; RP Part VI).
Decimal end to end; entry points run the float quarantine (G1).
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from tly.estimator import e_interp
from tly.guard import assert_no_floats
from tly.methodology import output_metadata
from tly.numeric import BILLION, Q4
from tly.snapshot import verify_manifest

HALF = Decimal("0.5")


@dataclass(frozen=True)
class LocationStock:
    """S and Ē for one (location, sex, year)."""

    location: str
    iso3: str | None
    year: int
    sex: str
    s_life_years: Decimal
    n_persons: Decimal

    @property
    def e_bar(self) -> Decimal:
        return self.s_life_years / self.n_persons

    @property
    def s_billions_4dp(self) -> Decimal:
        return (self.s_life_years / BILLION).quantize(Q4)


def compute_location_stock(
    pop_by_age: dict[int, Decimal],
    ex_anchors: dict[int, Decimal],
    *,
    location: str,
    year: int,
    sex: str,
    iso3: str | None = None,
) -> LocationStock:
    """E1 for one location: Σ over single ages of N(a) × e(a + 0.5).

    ``pop_by_age`` must be the complete single-age set 0..100 (upstream
    parsers enforce this); ``ex_anchors`` may be abridged (22) or complete
    (101) — the registered interpolation policy covers both.
    """
    assert_no_floats(pop_by_age, "pop_by_age")
    assert_no_floats(ex_anchors, "ex_anchors")
    s = Decimal(0)
    n = Decimal(0)
    for age, persons in pop_by_age.items():
        s += persons * e_interp(ex_anchors, Decimal(age) + HALF)
        n += persons
    return LocationStock(
        location=location, iso3=iso3, year=year, sex=sex, s_life_years=s, n_persons=n
    )


@dataclass(frozen=True)
class StockReport:
    """A stamped multi-location stock computation (SPEC#1 output shape)."""

    year: int
    sex: str
    stocks: tuple[LocationStock, ...]
    metadata: dict

    def by_location(self) -> dict[str, LocationStock]:
        return {s.location: s for s in self.stocks}


def stamp(snapshot_dirs: list[Path]) -> dict:
    """Metadata block: methodology version + policies + manifest hashes.

    Manifests are re-verified here (hash gate) so a stamp can never cite a
    snapshot that no longer matches its own manifest.
    """
    meta = output_metadata()
    meta["snapshots"] = {
        d.name: {
            name: entry["sha256"]
            for name, entry in verify_manifest(d, require_all=False)["files"].items()
        }
        for d in snapshot_dirs
    }
    return meta


def build_report(
    stocks: list[LocationStock], *, year: int, sex: str, snapshot_dirs: list[Path]
) -> StockReport:
    if not stocks:
        raise ValueError("no location stocks to report")
    if any(s.year != year or s.sex != sex for s in stocks):
        raise ValueError("mixed year/sex in one report")
    return StockReport(year=year, sex=sex, stocks=tuple(stocks), metadata=stamp(snapshot_dirs))
