"""B-uc1-05: WPP single-age population parser tests.

Primary tests run on the committed fixture (World/Japan/Nigeria, 2019+2023,
derived from the manifested 62MB source — provenance in manifest.json).
A slow regression against the full file runs only where it exists.
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from tly.wpp import parse_population_single_age, population_by_age

REPO = Path(__file__).resolve().parent.parent
SNAP = REPO / "data" / "snapshots" / "2026-08-17"
FIXTURE = SNAP / "fixtures" / "wpp_pop_single_age_fixture.csv.gz"
FULL = SNAP / "WPP2024_PopulationBySingleAgeSex_Medium_1950-2023.csv.gz"

GOLDEN_N_PERSONS = Decimal("8091734933.000")  # B-uc1-03 triangulation, exact


def test_fixture_parses_all_cells():
    cells = parse_population_single_age(FIXTURE, {2019, 2023})
    # 3 locations x 2 years x 101 ages x 3 sexes
    assert len(cells) == 3 * 2 * 101 * 3
    assert all(isinstance(c.persons, Decimal) for c in cells)
    assert {c.location for c in cells} == {"World", "Japan", "Nigeria"}
    world = next(c for c in cells if c.location == "World")
    assert world.iso3 is None  # aggregate rows carry no ISO3
    japan = next(c for c in cells if c.location == "Japan")
    assert japan.iso3 == "JPN"


def test_world_2023_total_equals_golden_n():
    """Thousands->persons conversion is exact and sums to golden N."""
    cells = parse_population_single_age(FIXTURE, {2023}, locations={"World"})
    by_age = population_by_age(cells, "World", 2023)
    assert sum(by_age.values()) == GOLDEN_N_PERSONS


def test_population_by_age_complete_and_strict():
    cells = parse_population_single_age(FIXTURE, {2019, 2023})
    ja = population_by_age(cells, "Japan", 2019)
    assert sorted(ja) == list(range(0, 101))
    with pytest.raises(ValueError, match="no population cells"):
        population_by_age(cells, "France", 2023)


def test_male_plus_female_close_to_total():
    """M+F vs Total agrees within the file's 3-dp-of-thousands rounding
    (0.001 thousand = 1 person per component, so <= 1.5 persons per age)."""
    cells = parse_population_single_age(FIXTURE, {2023}, locations={"Nigeria"})
    tot = population_by_age(cells, "Nigeria", 2023, "total")
    male = population_by_age(cells, "Nigeria", 2023, "male")
    fem = population_by_age(cells, "Nigeria", 2023, "female")
    for age in range(101):
        assert abs(male[age] + fem[age] - tot[age]) <= Decimal("1.5")


def test_no_matching_year_raises():
    with pytest.raises(ValueError, match="no rows matched"):
        parse_population_single_age(FIXTURE, {1800})


@pytest.mark.skipif(
    not FULL.exists(), reason="full 62MB snapshot not present (manifest-only in git)"
)
def test_full_file_world_2023_regression():
    cells = parse_population_single_age(FULL, {2023}, locations={"World"})
    by_age = population_by_age(cells, "World", 2023)
    assert sum(by_age.values()) == GOLDEN_N_PERSONS
