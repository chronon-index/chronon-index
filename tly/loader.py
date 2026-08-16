"""Verified offline snapshot loading (SPEC#1 AC-1.5; RALPH_LOOP §6).

The ONE sanctioned way to get data into the compute path: hash-verify the
snapshot manifest first, then parse. A missing manifest, missing file, or
sha256 mismatch raises :class:`~tly.snapshot.SnapshotIntegrityError` before
a single value is parsed — no number can be computed from data that does
not match what was fetched and recorded.

Compute is offline by construction: nothing below this layer imports
urllib or opens a socket (enforced by test_compute_path_opens_no_socket).
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from tly.parsers import (
    PopulationBand,
    parse_births,
    parse_gho_life_tables,
    parse_population_bands,
)
from tly.snapshot import verify_manifest


@dataclass(frozen=True)
class VerifiedSnapshot:
    """Parsed, hash-verified inputs for one v0-shaped computation."""

    snapshot_dir: Path
    manifest: dict
    tables: dict[int, dict[int, Decimal]]
    bands: list[PopulationBand]
    births: Decimal | None


def load_verified_snapshot(
    snapshot_dir: Path,
    life_table_years: tuple[int, ...] = (2019, 2021),
    population_year: int = 2023,
) -> VerifiedSnapshot:
    """Verify integrity, then parse. Raises SnapshotIntegrityError first."""
    manifest = verify_manifest(snapshot_dir)
    return VerifiedSnapshot(
        snapshot_dir=snapshot_dir.resolve(),
        manifest=manifest,
        tables=parse_gho_life_tables(snapshot_dir, life_table_years),
        bands=parse_population_bands(snapshot_dir, population_year),
        births=parse_births(snapshot_dir, population_year),
    )
