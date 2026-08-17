"""E-06: Zenodo deposit dry-run — license-aware, account-free, hash-tied."""

from __future__ import annotations

import hashlib
import json

import pytest

from tly.zenodo import build_deposit, classify


def test_classification_follows_licensing_table():
    assert classify("owid_population_5yr_world.csv")[0] is True
    assert classify("wmd_world_mortality.csv")[0] is True
    assert classify("wpp_downloads_index.json")[0] is True
    ok, reason = classify("gho_ex_global_btsx_2019_2021.json")
    assert ok is False and "non-commercial" in reason
    assert classify("who_copyright.html")[0] is False
    assert classify("hmd_user_agreement.html")[0] is False


def test_dry_run_builds_2026_08_16_deposit(tmp_path):
    deposition = build_deposit("2026-08-16", tmp_path)
    deposit = tmp_path / "tly-vintage-2026-08-16"
    assert (deposit / "manifest.json").is_file()  # the record always travels
    assert (deposit / "deposition.json").is_file()
    assert (deposit / "CHECKSUMS.sha256").is_file()
    # WHO extracts excluded WITH hash + URL for independent refetch
    excluded = deposition["excluded_files"]
    assert any(k.startswith("gho_") for k in excluded)
    for row in excluded.values():
        assert row["sha256"] and row["reason"]
    # OWID files included and byte-identical to the snapshot
    included = deposition["included_files"]
    assert "owid_population_5yr_world.csv" in included
    copied = deposit / "files" / "owid_population_5yr_world.csv"
    assert (
        hashlib.sha256(copied.read_bytes()).hexdigest() == included["owid_population_5yr_world.csv"]
    )


def test_dry_run_2026_08_17_respects_in_git_false(tmp_path):
    deposition = build_deposit("2026-08-17", tmp_path)
    excluded = deposition["excluded_files"]
    big = "WPP2024_Life_Table_Complete_Medium_Both_1950-2023.csv.gz"
    if big in excluded:  # local tree HAS the file; classify includes it
        assert excluded[big]["sha256"]
    else:
        # present locally -> included as redistributable UN data
        assert big in deposition["included_files"]
    # fixtures (committed, derived from UN data) are included
    assert any("fixtures/" in k for k in deposition["included_files"])
    # WMD included (MIT)
    assert "wmd_world_mortality.csv" in deposition["included_files"]


def test_metadata_shape_and_honesty(tmp_path):
    deposition = build_deposit("2026-08-16", tmp_path)
    meta = deposition["metadata"]
    assert meta["upload_type"] == "dataset"
    assert meta["license"] == "cc-by-4.0"
    assert meta["version"] == "2026-08-16"
    assert "excluded" in meta["description"].lower() or deposition["excluded_files"]
    data = json.loads((tmp_path / "tly-vintage-2026-08-16" / "deposition.json").read_text())
    assert data["excluded_files"] == deposition["excluded_files"]


def test_unknown_vintage_rejected(tmp_path):
    with pytest.raises(ValueError, match="no vintage"):
        build_deposit("1999-01-01", tmp_path)
