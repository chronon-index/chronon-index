"""B-uc4-08: append-only print archive with hash chain — mutation raises."""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

import pytest

from tly.archive import (
    GENESIS_HASH,
    ArchiveChainError,
    ArchiveImmutabilityError,
    PrintArchive,
)
from tly.prints import WeeklyPrint
from tly.stock import stamp

REPO = Path(__file__).resolve().parent.parent
SNAP16 = REPO / "data" / "snapshots" / "2026-08-16"

D = Decimal
E1, E2, E3 = (
    "2026-08-03T12:00:00+00:00",
    "2026-08-10T12:00:00+00:00",
    "2026-08-17T12:00:00+00:00",
)


def _print(epoch: str, s: str = "362412641743.4670") -> WeeklyPrint:
    return WeeklyPrint(
        epoch_utc=epoch,
        series_label="SETTLEMENT",
        s_life_years=D(s),
        e_bar_years=D("44.7880"),
        n_persons=D("8091734933"),
        burn_life_years=D("0"),
        coverage={"measured_share": D("0.92")},
        accuracy={
            "statement": "test accuracy statement",
            "uncertainty": {"type": "convention", "note": "test fixture"},
        },
        provenance=stamp([SNAP16]),
    )


def test_append_chain_and_verify(tmp_path):
    a = PrintArchive(tmp_path)
    assert a.head_hash == GENESIS_HASH
    h1 = a.append(_print(E1))
    h2 = a.append(_print(E2))
    h3 = a.append(_print(E3))
    assert len({h1, h2, h3}) == 3
    chain = a.verify()
    assert [c["epoch_utc"] for c in chain] == [E1, E2, E3]
    assert chain[1]["prev_hash"] == h1  # each record commits to history
    assert a.head_hash == h3


def test_duplicate_epoch_raises(tmp_path):
    a = PrintArchive(tmp_path)
    a.append(_print(E1))
    with pytest.raises(ArchiveImmutabilityError, match="already archived"):
        a.append(_print(E1, s="999999999999.0000"))  # even with different data


def test_out_of_order_epoch_raises(tmp_path):
    a = PrintArchive(tmp_path)
    a.append(_print(E2))
    with pytest.raises(ArchiveImmutabilityError, match="not after archive head"):
        a.append(_print(E1))


def test_edited_record_breaks_chain(tmp_path):
    a = PrintArchive(tmp_path)
    a.append(_print(E1))
    a.append(_print(E2))
    victim = tmp_path / "2026-08-03.json"
    victim.write_text(victim.read_text().replace("362412", "999999"))
    with pytest.raises(ArchiveChainError, match="history was edited"):
        a.verify()


def test_tampered_chain_metadata_detected(tmp_path):
    a = PrintArchive(tmp_path)
    a.append(_print(E1))
    a.append(_print(E2))
    chain = json.loads((tmp_path / "chain.json").read_text())
    chain[1]["prev_hash"] = "f" * 64
    (tmp_path / "chain.json").write_text(json.dumps(chain))
    with pytest.raises(ArchiveChainError, match="prev_hash broken"):
        a.verify()


def test_unchained_record_detected(tmp_path):
    a = PrintArchive(tmp_path)
    a.append(_print(E1))
    (tmp_path / "2026-08-10.json").write_text(_print(E2).render())
    with pytest.raises(ArchiveChainError, match="unchained record files"):
        a.verify()
