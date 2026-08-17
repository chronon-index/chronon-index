"""E-02: OTS workflow — real-client orchestration tested via a stub client
fixture; the no-client path is honest, never faked."""

from __future__ import annotations

import os
import stat
from pathlib import Path

import pytest

from tly.timestamping import (
    STALE,
    STAMPED,
    UNSTAMPED,
    StampStore,
    TimestampError,
    ots_client,
)

DIGEST = "a" * 64
OTHER = "b" * 64


def _install_stub_ots(tmp_path: Path, monkeypatch) -> Path:
    """A local fixture standing in for the opentimestamps client: takes
    `stamp <file>` and writes `<file>.ots` — letting the tests exercise OUR
    orchestration without faking any cryptography in the module itself."""
    stub = tmp_path / "bin" / "ots"
    stub.parent.mkdir()
    stub.write_text('#!/bin/sh\n[ "$1" = "stamp" ] || exit 2\ncp "$2" "$2.ots"\n')
    stub.chmod(stub.stat().st_mode | stat.S_IEXEC)
    monkeypatch.setenv("PATH", f"{stub.parent}{os.pathsep}{os.environ['PATH']}")
    return stub


def test_record_and_status(tmp_path):
    store = StampStore(tmp_path / "stamps")
    assert store.status("epoch-1").state == UNSTAMPED
    store.record_target("epoch-1", DIGEST)
    s = store.status("epoch-1")
    assert s.state == UNSTAMPED and s.digest == DIGEST  # recorded, unproven


def test_recorded_digest_cannot_change(tmp_path):
    store = StampStore(tmp_path)
    store.record_target("epoch-1", DIGEST)
    store.record_target("epoch-1", DIGEST)  # idempotent re-record is fine
    with pytest.raises(TimestampError, match="never an overwrite"):
        store.record_target("epoch-1", OTHER)


def test_stamp_via_stub_client(tmp_path, monkeypatch):
    _install_stub_ots(tmp_path, monkeypatch)
    assert ots_client() is not None
    store = StampStore(tmp_path / "stamps")
    store.record_target("epoch-1", DIGEST)
    s = store.stamp("epoch-1")
    assert s.state == STAMPED
    assert s.proof_path is not None and s.proof_path.is_file()


def test_no_client_is_honest_not_fake(tmp_path, monkeypatch):
    monkeypatch.setenv("PATH", str(tmp_path / "empty"))  # no ots anywhere
    store = StampStore(tmp_path / "stamps")
    store.record_target("epoch-1", DIGEST)
    with pytest.raises(TimestampError, match="never faked"):
        store.stamp("epoch-1")
    assert store.status("epoch-1").state == UNSTAMPED  # still honest


def test_stale_stamp_surfaces(tmp_path):
    store = StampStore(tmp_path)
    store.record_target("epoch-1", DIGEST)
    assert store.status("epoch-1", live_digest=DIGEST).state == UNSTAMPED
    assert store.status("epoch-1", live_digest=OTHER).state == STALE


def test_archive_head_is_a_stampable_target(tmp_path):
    """The intended integration: the archive head hash records cleanly."""
    from tly.archive import PrintArchive

    archive = PrintArchive(tmp_path / "archive")
    store = StampStore(tmp_path / "stamps")
    path = store.record_target("genesis-head", archive.head_hash)
    assert path.read_text().strip() == "0" * 64
