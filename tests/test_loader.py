"""B-uc1-02 / AC-1.5: offline-only compute over hash-verified snapshots.

Failure modes required by the AC: (1) mismatched manifest sha256 raises,
(2) missing manifest/file raises — both BEFORE any parsing. Plus the
no-network proof: the entire load+compute path runs with socket creation
disabled.
"""

from __future__ import annotations

import shutil
import socket
from decimal import Decimal
from pathlib import Path

import pytest

from tly.estimator import compute_stock, e_bar, total_population
from tly.loader import load_verified_snapshot
from tly.snapshot import SnapshotIntegrityError

REPO = Path(__file__).resolve().parent.parent
SNAPSHOT = REPO / "data" / "snapshots" / "2026-08-16"


def _copy_snapshot(tmp_path: Path) -> Path:
    dst = tmp_path / "2026-08-16"
    shutil.copytree(SNAPSHOT, dst)
    return dst


def test_load_verified_snapshot_happy_path():
    snap = load_verified_snapshot(SNAPSHOT)
    assert set(snap.tables) == {2019, 2021}
    assert len(snap.bands) == 21
    assert snap.births is not None
    assert len(snap.manifest["files"]) == 6


def test_loader_raises_on_hash_mismatch(tmp_path):
    snap_dir = _copy_snapshot(tmp_path)
    csv_file = snap_dir / "owid_population_5yr_world.csv"
    csv_file.write_text(csv_file.read_text(encoding="utf-8") + "#\n", encoding="utf-8")
    with pytest.raises(SnapshotIntegrityError, match="hash mismatch"):
        load_verified_snapshot(snap_dir)


def test_loader_raises_on_missing_file(tmp_path):
    snap_dir = _copy_snapshot(tmp_path)
    (snap_dir / "gho_ex_global_btsx_2019_2021.json").unlink()
    with pytest.raises(SnapshotIntegrityError, match="missing snapshot file"):
        load_verified_snapshot(snap_dir)


def test_loader_raises_on_missing_manifest(tmp_path):
    snap_dir = _copy_snapshot(tmp_path)
    (snap_dir / "manifest.json").unlink()
    with pytest.raises(SnapshotIntegrityError, match="missing manifest"):
        load_verified_snapshot(snap_dir)


def test_verification_happens_before_parsing(tmp_path):
    """A corrupted-beyond-parsing file must fail on INTEGRITY, not on a
    parse error — proving the hash gate runs first."""
    snap_dir = _copy_snapshot(tmp_path)
    (snap_dir / "gho_ex_global_btsx_2019_2021.json").write_text("not json at all")
    with pytest.raises(SnapshotIntegrityError, match="hash mismatch"):
        load_verified_snapshot(snap_dir)


def test_compute_path_opens_no_socket(monkeypatch):
    """AC-1.5 no-network rule: the full load+compute path succeeds with
    socket creation disabled — any network attempt would crash loudly."""

    def no_socket(*args, **kwargs):
        raise AssertionError("network access attempted during compute")

    monkeypatch.setattr(socket, "socket", no_socket)
    snap = load_verified_snapshot(SNAPSHOT)
    stock = compute_stock(snap.tables[2019], snap.bands, 2019)
    n = total_population(snap.bands)
    assert str(stock.s_billions_4dp) == "362.4126"
    assert str(e_bar(stock, n).quantize(Decimal("0.0001"))) == "44.7880"
