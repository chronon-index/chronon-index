"""C-uc7-04 / AC-7.4: a filed dispute alters nothing and delays nothing."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from tly.archive import PrintArchive
from tly.disputes import DisputeFormatError, DisputeLog, DisputeWindowClosed
from tly.fixings import FINAL, settle_from_archive
from tly.pipeline import build_settlement_print

REPO = Path(__file__).resolve().parent.parent
SNAPSHOTS = REPO / "data" / "snapshots"
E1 = "2026-08-17T12:00:00+00:00"
E2 = "2026-08-24T12:00:00+00:00"

D = Decimal


def test_dispute_alters_nothing_and_delays_nothing(tmp_path):
    """The named property: after a dispute is filed against a FINAL fixing,
    the fixing is bit-identical AND the next epoch publishes on schedule."""
    archive = PrintArchive(tmp_path / "archive")
    archive.append(build_settlement_print(E1))
    fixing = settle_from_archive(archive, E1, SNAPSHOTS)
    rendered_before = fixing.render()

    log = DisputeLog(tmp_path / "disputes")
    record = log.file_dispute(
        fixing_hash=fixing.fixing_hash,
        epoch_utc=E1,
        filed_utc="2026-08-18T09:00:00+00:00",  # 21h after epoch: in window
        claimant="external-recomputer-7",
        claim="my recomputation differs in the 12th decimal",
    )
    assert "log-only" in record["effect"]

    # alters nothing: the fixing is bit-identical
    assert fixing.status == FINAL
    assert fixing.render() == rendered_before
    assert settle_from_archive(archive, E1, SNAPSHOTS).fixing_hash == fixing.fixing_hash

    # delays nothing: the next epoch appends and settles on schedule
    archive.append(build_settlement_print(E2))
    next_fixing = settle_from_archive(archive, E2, SNAPSHOTS)
    assert next_fixing.status == FINAL
    assert log.disputes()[0]["claimant"] == "external-recomputer-7"


def test_window_boundaries(tmp_path):
    log = DisputeLog(tmp_path)
    ok = dict(fixing_hash="a" * 64, epoch_utc=E1, claimant="c", claim="x")
    log.file_dispute(**ok, filed_utc="2026-08-19T12:00:00+00:00")  # exactly 48h: in
    with pytest.raises(DisputeWindowClosed, match="window closed"):
        log.file_dispute(**ok, filed_utc="2026-08-19T12:00:01+00:00")  # 48h+1s
    with pytest.raises(DisputeFormatError, match="precede"):
        log.file_dispute(**ok, filed_utc="2026-08-17T11:59:59+00:00")


def test_log_is_append_only_jsonl(tmp_path):
    log = DisputeLog(tmp_path)
    base = dict(fixing_hash="a" * 64, epoch_utc=E1, claimant="c")
    log.file_dispute(**base, claim="first", filed_utc="2026-08-17T13:00:00+00:00")
    first = log.path.read_text()
    log.file_dispute(**base, claim="second", filed_utc="2026-08-17T14:00:00+00:00")
    assert log.path.read_text().startswith(first)  # strictly extends
    assert [d["claim"] for d in log.disputes()] == ["first", "second"]


def test_filing_discipline(tmp_path):
    log = DisputeLog(tmp_path)
    with pytest.raises(DisputeFormatError, match="sha256"):
        log.file_dispute(
            fixing_hash="xyz",
            epoch_utc=E1,
            claimant="c",
            claim="x",
            filed_utc="2026-08-17T13:00:00+00:00",
        )
    with pytest.raises(DisputeFormatError, match="required"):
        log.file_dispute(
            fixing_hash="a" * 64,
            epoch_utc=E1,
            claimant=" ",
            claim="x",
            filed_utc="2026-08-17T13:00:00+00:00",
        )
    with pytest.raises(DisputeFormatError, match="timezone-aware"):
        log.file_dispute(
            fixing_hash="a" * 64,
            epoch_utc=E1,
            claimant="c",
            claim="x",
            filed_utc="2026-08-17T13:00:00",
        )
