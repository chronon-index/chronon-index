"""C-uc7-02 / AC-7.1 / invariant P4 / DECISIONS #7: no code path mutates a
FINAL print — and the ONLY sanctioned response to a discovered error is a
ledger entry folded into the NEXT epoch.

P4 has three enforcement layers, each tested here under its named banner:
the fixing (setattr guard), the print (frozen dataclass), and the archive
(same-epoch re-append refused). The final test walks the sanctioned
correction path end to end.
"""

from __future__ import annotations

import dataclasses
from decimal import Decimal

import pytest

from tly.archive import ArchiveImmutabilityError, PrintArchive
from tly.corrections import find_restatements, parse_ledger
from tly.fixings import FINAL, Fixing, FixingImmutabilityError
from tly.prints import WeeklyPrint
from tly.stock import stamp
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SNAP16 = REPO / "data" / "snapshots" / "2026-08-16"

D = Decimal
E1 = "2026-08-10T12:00:00+00:00"
E2 = "2026-08-17T12:00:00+00:00"
HASHES = {"2026-08-16": {"gho_ex_global_btsx_2019_2021.json": "a" * 64}}
URLS = ("https://ghoapi.azureedge.net/api/LIFE_0000000035",)


def _fixing(epoch: str, value: str) -> Fixing:
    return Fixing(
        epoch_utc=epoch,
        value=D(value),
        methodology_version="v0.4.0-reconstruction",
        snapshot_hashes=HASHES,
        source_urls=URLS,
    )


def _print(epoch: str) -> WeeklyPrint:
    return WeeklyPrint(
        epoch_utc=epoch,
        series_label="SETTLEMENT",
        s_life_years=D("362412641743.4670"),
        e_bar_years=D("44.7880"),
        n_persons=D("8091734933"),
        burn_life_years=D("0"),
        coverage={"measured_share": D("0.92")},
        accuracy={
            "statement": "x",
            "uncertainty": {"type": "convention", "note": "x"},
        },
        provenance=stamp([SNAP16]),
    )


def test_p4_immutability(tmp_path):
    """Named per RP Part X: every mutation avenue on a FINAL object raises."""
    # layer 1: FINAL fixing — every attribute, including status itself
    f = _fixing(E2, "362412641743.4670")
    f.finalize()
    for attr, val in (
        ("value", D("1")),
        ("epoch_utc", E1),
        ("status", "DRAFT"),
        ("fixing_hash", "0" * 64),
        ("snapshot_hashes", {}),
    ):
        with pytest.raises(FixingImmutabilityError, match="is FINAL"):
            setattr(f, attr, val)
    assert f.value == D("362412641743.4670")  # untouched after all attempts
    assert f.status == FINAL

    # layer 2: the print object is frozen
    p = _print(E2)
    with pytest.raises(dataclasses.FrozenInstanceError):
        p.s_life_years = D("1")  # type: ignore[misc]

    # layer 3: the archive refuses to re-open a published epoch
    archive = PrintArchive(tmp_path)
    archive.append(_print(E1))
    head = archive.head_hash
    with pytest.raises(ArchiveImmutabilityError, match="FINAL"):
        archive.append(_print(E1))
    assert archive.head_hash == head  # nothing changed
    archive.verify()


def test_corrections_route_forward_only(tmp_path):
    """The sanctioned path for a discovered error on a FINAL epoch:
    (1) the FINAL fixing stays exactly as published;
    (2) a ledger entry records the deviation;
    (3) the NEXT epoch's fixing absorbs the correction;
    (4) the vintage checker confirms nothing was restated."""
    wrong = _fixing(E1, "362412641743.4670")  # published with a (discovered) error
    wrong.finalize()
    error = D("0.0100")  # the discovered overstatement

    ledger = tmp_path / "CORRECTIONS.md"
    ledger.write_text(
        "# Correction ledger — forward-only\n\n"
        "## C-0001 | 2026-08-17 | epoch 2026-08-10 fixing\n"
        "- Published value overstated by 0.0100 life-years (input revision)\n"
        "- Forward treatment: absorbed into the 2026-08-17 epoch\n",
        encoding="utf-8",
    )
    entries = parse_ledger(ledger)
    assert entries[0].scope == "epoch 2026-08-10 fixing"

    corrected_next = _fixing(E2, str(D("362412641743.4671") - error))
    corrected_next.finalize()

    assert wrong.value == D("362412641743.4670")  # (1) first print settled
    old_vintage = {E1: wrong.value}
    new_vintage = {E1: wrong.value, E2: corrected_next.value}
    assert find_restatements(old_vintage, new_vintage) == []  # (4) no restatement
