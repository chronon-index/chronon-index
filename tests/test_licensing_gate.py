"""B-uc3-13 / P1 GATE: public prints blocked unless compute sources cleared.

The honest headline test: the CURRENT pipeline is WHO-table-based, so the
commercial gate must BLOCK it today — the gate working correctly, and the
G5 WPP migration made unforgettable.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tly.licensing_gate import (
    CLEARED,
    HUMAN,
    LicensingGateError,
    check_gate,
    parse_table,
    row_for_file,
)
from tly.pipeline import build_settlement_print

REPO = Path(__file__).resolve().parent.parent


def _pipeline_compute_files() -> list[str]:
    """The files the live print actually cites — from its own provenance."""
    p = build_settlement_print("2026-08-17T12:00:00+00:00")
    return [name for snap, files in p.provenance["snapshots"].items() for name in files]


def test_table_parses_with_expected_statuses():
    rows = parse_table()
    assert rows["UN WPP 2024"] == CLEARED
    assert rows["ACLED"] == HUMAN
    assert rows["WHO GHO / GHE"] == "VERIFIED-RESTRICTED"
    assert rows["HMD STMF"] == "CLEARED-CONSTRUCTED-ONLY"
    assert len(rows) >= 13


def test_p1_gate_blocks_current_who_based_commercial_print():
    """THE P1 gate, honestly applied: today's pipeline cites WHO GHO files,
    so a COMMERCIAL print must be blocked — this failing would mean the
    gate stopped guarding the G5 migration."""
    violations = check_gate(_pipeline_compute_files(), commercial=True)
    assert violations, "gate should block the WHO-based pipeline in commercial mode"
    assert any("WHO GHO / GHE" in v and "VERIFIED-RESTRICTED" in v for v in violations)


def test_research_mode_passes_current_pipeline():
    """The v0 research posture: WHO triangulation tolerated, gate open."""
    assert check_gate(_pipeline_compute_files(), commercial=False) == []


def test_wpp_only_compute_path_passes_commercial():
    """The post-G5 world: a print citing only WPP/OWID/WMD files clears
    the commercial gate — the migration target is already gate-legal."""
    files = [
        "WPP2024_PopulationBySingleAgeSex_Medium_1950-2023.csv.gz",
        "WPP2024_Life_Table_Complete_Medium_Both_1950-2023.csv.gz",
        "owid_population_5yr_world.csv",
        "wmd_world_mortality.csv",
    ]
    assert check_gate(files, commercial=True) == []


def test_human_rows_block_even_research():
    table = parse_table()
    table["UN WPP 2024"] = HUMAN  # simulate an unpurchased core license
    files = ["WPP2024_Life_Table_Abridged_Medium_1950-2023.csv.gz"]
    assert check_gate(files, commercial=False, table=table)


def test_unknown_file_fails_closed():
    with pytest.raises(LicensingGateError, match="no licensing classification"):
        row_for_file("mystery_source_dump.csv")


def test_evidence_files_are_not_data_sources():
    assert row_for_file("cc_by_30_igo_deed.html") is None
    assert row_for_file("eurostat_legal_notice.html") is None
    assert row_for_file("fixtures/wpp_pop_single_age_fixture.csv.gz") is None
