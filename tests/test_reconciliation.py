"""B-uc1-09 / AC-1.1 / invariant P3: Σ per-country dS == global dS, exactly.

The engine invariant runs on the committed fixture universe. The full
all-countries run (62MB pop + 200MB life tables) is a skipif test that also
MEASURES the WPP data-level World-vs-Σcountries gap — a data fact recorded
with a documented rounding bound, kept strictly separate from the exact
engine invariant.
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from tly.stock import aggregate_stocks, compute_location_stock, reconcile_delta
from tly.wpp import (
    ex_anchors,
    parse_life_table_ex,
    parse_population_single_age,
    population_by_age,
)

REPO = Path(__file__).resolve().parent.parent
SNAP17 = REPO / "data" / "snapshots" / "2026-08-17"
POP_FIX = SNAP17 / "fixtures" / "wpp_pop_single_age_fixture.csv.gz"
LT_FIX = SNAP17 / "fixtures" / "wpp_lt_complete_fixture.csv.gz"
POP_FULL = SNAP17 / "WPP2024_PopulationBySingleAgeSex_Medium_1950-2023.csv.gz"
LT_FULL = SNAP17 / "WPP2024_Life_Table_Complete_Medium_Both_1950-2023.csv.gz"


def _country_stocks(pop_path, lt_path, year, locations=None, loc_types=None):
    pop = parse_population_single_age(pop_path, {year}, locations, loc_types)
    lt = parse_life_table_ex(lt_path, {year}, locations, loc_types)
    locs = sorted({c.location for c in pop})
    return [
        compute_location_stock(
            population_by_age(pop, loc, year),
            ex_anchors(lt, loc, year),
            location=loc,
            year=year,
            sex="total",
        )
        for loc in locs
    ]


def test_p3_reconciliation():
    """Named per RP Part X: per-country deltas sum to the global delta,
    exactly, in Decimal — fixture universe {Japan, Nigeria}, 2019→2023."""
    countries = {"Japan", "Nigeria"}
    start = _country_stocks(POP_FIX, LT_FIX, 2019, locations=countries)
    end = _country_stocks(POP_FIX, LT_FIX, 2023, locations=countries)
    per_location, global_delta = reconcile_delta(start, end)
    assert per_location == global_delta  # exact Decimal equality, no tolerance


def test_reconcile_rejects_universe_mismatch():
    start = _country_stocks(POP_FIX, LT_FIX, 2019, locations={"Japan", "Nigeria"})
    end = _country_stocks(POP_FIX, LT_FIX, 2023, locations={"Japan"})
    with pytest.raises(ValueError, match="location universes differ"):
        reconcile_delta(start, end)


def test_aggregate_rejects_mixed_epochs():
    a = _country_stocks(POP_FIX, LT_FIX, 2019, locations={"Japan"})
    b = _country_stocks(POP_FIX, LT_FIX, 2023, locations={"Nigeria"})
    with pytest.raises(ValueError, match="mixed year/sex"):
        aggregate_stocks(a + b)


@pytest.mark.skipif(
    not (POP_FULL.exists() and LT_FULL.exists()),
    reason="full WPP snapshots not present (manifest-only in git)",
)
def test_p3_full_universe_and_wpp_world_gap():
    """All Country/Area locations, 2022→2023: the engine invariant holds
    exactly at full scale; separately, the DATA-level gap between
    WPP's published World aggregate and Σ countries is measured and
    bounded by file rounding (±0.5 person per cell ⇒ conservatively
    < 100,000 persons over ~236 countries × 101 ages)."""
    start = _country_stocks(POP_FULL, LT_FULL, 2022, loc_types={"Country/Area"})
    end = _country_stocks(POP_FULL, LT_FULL, 2023, loc_types={"Country/Area"})
    assert len(end) >= 200  # sanity: a real all-countries universe
    per_location, global_delta = reconcile_delta(start, end)
    assert per_location == global_delta  # P3 at full scale, exact

    world = _country_stocks(POP_FULL, LT_FULL, 2023, locations={"World"})[0]
    sigma = aggregate_stocks(end, name="SUM_OF_COUNTRIES")
    n_gap = abs(sigma.n_persons - world.n_persons)
    assert n_gap < Decimal(100_000), f"WPP World vs Σcountries N gap {n_gap} persons"
