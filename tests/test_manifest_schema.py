"""B-uc3-01 / AC-3.3: the manifest schema gate, run over the REAL tree.

test_real_snapshots_fully_manifested is the CI gate itself: it validates
every committed snapshot directory. The synthetic tests prove each failure
mode fires.
"""

from __future__ import annotations

import json
from pathlib import Path

from tly.manifest_schema import validate_all_snapshots, validate_snapshot_dir

REPO = Path(__file__).resolve().parent.parent
SNAPSHOTS = REPO / "data" / "snapshots"


def test_real_snapshots_fully_manifested():
    """THE gate: every file in every committed snapshot has a complete,
    hash-matching manifest row. Violations list prints in full on failure."""
    problems = validate_all_snapshots(SNAPSHOTS)
    assert problems == [], "\n".join(problems)


def _write_manifest(d: Path, files: dict) -> None:
    (d / "manifest.json").write_text(
        json.dumps({"snapshot_date": d.name, "files": files}) + "\n", encoding="utf-8"
    )


def _sha_bytes(body: bytes) -> dict:
    import hashlib

    return {"sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def test_unmanifested_file_fails(tmp_path):
    d = tmp_path / "2026-01-01"
    d.mkdir()
    _write_manifest(d, {})
    (d / "orphan.csv").write_bytes(b"data")
    problems = validate_snapshot_dir(d)
    assert any("NO manifest row" in p for p in problems)


def test_missing_provenance_fields_fail(tmp_path):
    d = tmp_path / "2026-01-02"
    d.mkdir()
    body = b"data"
    _write_manifest(
        d,
        {
            "a.csv": _sha_bytes(body),  # neither source_url nor derived_from
            "b.csv": {**_sha_bytes(body), "source_url": "https://x"},  # no retrieved_utc
            "c.csv": {**_sha_bytes(body), "derived_from": "a.csv"},  # no sha/derivation
        },
    )
    for name in ("a.csv", "b.csv", "c.csv"):
        (d / name).write_bytes(body)
    problems = validate_snapshot_dir(d)
    assert any("neither source_url nor derived_from" in p for p in problems)
    assert any("missing retrieved_utc" in p for p in problems)
    assert any("missing derived_from_sha256" in p for p in problems)


def test_hash_and_size_mismatch_fail(tmp_path):
    d = tmp_path / "2026-01-03"
    d.mkdir()
    row = {**_sha_bytes(b"original"), "source_url": "https://x", "retrieved_utc": "t"}
    _write_manifest(d, {"a.csv": row})
    (d / "a.csv").write_bytes(b"tampered!")
    problems = validate_snapshot_dir(d)
    assert any("sha256 mismatch" in p for p in problems)
    assert any("size mismatch" in p for p in problems)


def test_absent_file_needs_in_git_false(tmp_path):
    d = tmp_path / "2026-01-04"
    d.mkdir()
    row = {**_sha_bytes(b"big"), "source_url": "https://x", "retrieved_utc": "t"}
    _write_manifest(d, {"big.gz": row})
    problems = validate_snapshot_dir(d)
    assert any("not marked in_git:false" in p for p in problems)
    row["in_git"] = False
    _write_manifest(d, {"big.gz": row})
    assert validate_snapshot_dir(d) == []


def test_derived_parent_hash_must_match(tmp_path):
    d = tmp_path / "2026-01-05"
    d.mkdir()
    parent = {**_sha_bytes(b"parent"), "source_url": "https://x", "retrieved_utc": "t"}
    child_body = b"child"
    child = {
        **_sha_bytes(child_body),
        "derived_from": "p.csv",
        "derived_from_sha256": "WRONG",
        "derivation": "subset",
    }
    _write_manifest(d, {"p.csv": parent, "c.csv": child})
    (d / "p.csv").write_bytes(b"parent")
    (d / "c.csv").write_bytes(child_body)
    problems = validate_snapshot_dir(d)
    assert any("derived_from_sha256 does not match parent" in p for p in problems)
