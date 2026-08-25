"""B-uc4-06: the OTS publish gate — proof exists + matches, else blocked."""

from __future__ import annotations

import json

from tly.ots_gate import REPO_ROOT, chain_targets, gate

DIGEST_A = "a" * 64
DIGEST_B = "b" * 64


def _archive(tmp_path, record_hash=DIGEST_A):
    root = tmp_path / "archive"
    root.mkdir()
    (root / "chain.json").write_text(
        json.dumps([{"file": "2026-01-05.json", "record_hash": record_hash}])
    )
    return root


def test_missing_target_blocks(tmp_path):
    problems = gate(_archive(tmp_path), tmp_path / "stamps")
    assert len(problems) == 1 and "no recorded stamp target" in problems[0]


def test_digest_mismatch_blocks(tmp_path):
    archive = _archive(tmp_path)
    stamps = tmp_path / "stamps"
    stamps.mkdir()
    (stamps / "2026-01-05.hash").write_text(DIGEST_B + "\n")
    (stamps / "2026-01-05.ots").write_bytes(b"proof")
    assert any("!= chain record_hash" in p for p in gate(archive, stamps))


def test_missing_proof_blocks(tmp_path):
    archive = _archive(tmp_path)
    stamps = tmp_path / "stamps"
    stamps.mkdir()
    (stamps / "2026-01-05.hash").write_text(DIGEST_A + "\n")
    assert any("no .ots proof" in p for p in gate(archive, stamps))


def test_stamped_and_matching_passes(tmp_path):
    archive = _archive(tmp_path)
    stamps = tmp_path / "stamps"
    stamps.mkdir()
    (stamps / "2026-01-05.hash").write_text(DIGEST_A + "\n")
    (stamps / "2026-01-05.ots").write_bytes(b"proof")
    assert gate(archive, stamps) == []


def test_real_archive_is_fully_stamped():
    """The committed repo passes its own publish gate: every chain link
    has a matching .hash + real .ots proof under stamps/."""
    assert gate(REPO_ROOT / "archive", REPO_ROOT / "stamps") == []
    assert len(chain_targets(REPO_ROOT / "archive")) >= 2
