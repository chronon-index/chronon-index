"""A-14 unit tests: tly.snapshot — manifest writing, integrity verification.

Network-free: the fetcher is injected for fetch tests, and the integrity
gate is exercised against the real committed 2026-08-16 snapshot.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from tly.snapshot import (
    SnapshotIntegrityError,
    fetch_snapshot,
    fetch_url,
    verify_manifest,
)

REPO = Path(__file__).resolve().parent.parent
COMMITTED_SNAPSHOT = REPO / "data" / "snapshots" / "2026-08-16"


def fake_fetcher(url: str) -> bytes:
    return f"payload-for::{url}".encode()


def test_fetch_snapshot_writes_files_and_manifest(tmp_path):
    sources = {"a.json": "https://example.org/a", "b.csv": "https://example.org/b"}
    manifest = fetch_snapshot(tmp_path / "2026-01-01", sources, fetcher=fake_fetcher, note="test")
    snap = tmp_path / "2026-01-01"
    assert (snap / "a.json").read_bytes() == b"payload-for::https://example.org/a"
    on_disk = json.loads((snap / "manifest.json").read_text(encoding="utf-8"))
    assert on_disk == manifest
    assert manifest["snapshot_date"] == "2026-01-01"
    assert manifest["note"] == "test"
    for name, url in sources.items():
        entry = manifest["files"][name]
        assert entry["source_url"] == url
        assert entry["sha256"] == hashlib.sha256(fake_fetcher(url)).hexdigest()
        assert entry["bytes"] == len(fake_fetcher(url))
        assert entry["retrieved_utc"].endswith("+00:00")  # UTC, per RP Part VI


def test_fetch_then_verify_roundtrip(tmp_path):
    snap = tmp_path / "2026-01-02"
    fetch_snapshot(snap, {"x.bin": "https://example.org/x"}, fetcher=fake_fetcher)
    verified = verify_manifest(snap)
    assert "x.bin" in verified["files"]


def test_verify_committed_snapshot_is_intact():
    """The real 2026-08-16 snapshot must verify — this IS the offline gate."""
    manifest = verify_manifest(COMMITTED_SNAPSHOT)
    assert len(manifest["files"]) == 6


def test_verify_detects_tampering(tmp_path):
    snap = tmp_path / "2026-01-03"
    fetch_snapshot(snap, {"x.bin": "https://example.org/x"}, fetcher=fake_fetcher)
    (snap / "x.bin").write_bytes(b"tampered")
    with pytest.raises(SnapshotIntegrityError, match="hash mismatch for x.bin"):
        verify_manifest(snap)


def test_verify_detects_missing_file(tmp_path):
    snap = tmp_path / "2026-01-04"
    fetch_snapshot(snap, {"x.bin": "https://example.org/x"}, fetcher=fake_fetcher)
    (snap / "x.bin").unlink()
    with pytest.raises(SnapshotIntegrityError, match="missing snapshot file"):
        verify_manifest(snap)


def test_verify_missing_manifest(tmp_path):
    with pytest.raises(SnapshotIntegrityError, match="missing manifest"):
        verify_manifest(tmp_path)


def test_fetch_url_backs_off_and_raises(monkeypatch):
    """No network: point at an unroutable URL scheme failure via mock opener."""
    calls = {"n": 0}
    sleeps: list[float] = []

    def failing_opener(*a, **k):
        calls["n"] += 1
        raise OSError("boom")

    monkeypatch.setattr("urllib.request.urlopen", failing_opener)
    with pytest.raises(RuntimeError, match="fetch failed after 3 attempts"):
        fetch_url("https://example.org/never", attempts=3, sleep=sleeps.append)
    assert calls["n"] == 3
    assert len(sleeps) == 2  # no sleep before the first attempt
    assert sleeps[0] >= 2 and sleeps[1] >= 4  # exponential base + jitter
