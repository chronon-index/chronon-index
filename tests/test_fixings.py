"""C-uc7-01 / AC-7.6: fixing schema + DRAFT→FINAL lifecycle."""

from __future__ import annotations

from decimal import Decimal

import pytest

from tly.fixings import (
    DRAFT,
    FINAL,
    Fixing,
    FixingImmutabilityError,
    FixingValidationError,
)

D = Decimal
EPOCH = "2026-08-17T12:00:00+00:00"
HASHES = {"2026-08-16": {"gho_ex_global_btsx_2019_2021.json": "a" * 64}}
URLS = ("https://ghoapi.azureedge.net/api/LIFE_0000000035",)


def _draft(**over) -> Fixing:
    kwargs = dict(
        epoch_utc=EPOCH,
        value=D("362412641743.4670"),
        methodology_version="v0.4.0-reconstruction",
        snapshot_hashes=HASHES,
        source_urls=URLS,
    )
    kwargs.update(over)
    return Fixing(**kwargs)


def test_lifecycle_draft_to_final():
    f = _draft()
    assert f.status == DRAFT
    assert f.fixing_hash is None
    f.value = D("362412641743.4671")  # drafts may still be corrected
    h = f.finalize()
    assert f.status == FINAL
    assert f.fixing_hash == h and len(h) == 64
    with pytest.raises(FixingImmutabilityError, match="already FINAL"):
        f.finalize()


def test_incomplete_provenance_cannot_exist():
    """AC-7.6: incomplete provenance fails at construction, not later."""
    with pytest.raises(FixingValidationError, match="at least one snapshot"):
        _draft(snapshot_hashes={})
    with pytest.raises(FixingValidationError, match="at least one snapshot"):
        _draft(snapshot_hashes={"2026-08-16": {}})
    with pytest.raises(FixingValidationError, match="bad sha256"):
        _draft(snapshot_hashes={"2026-08-16": {"f.json": "short"}})
    with pytest.raises(FixingValidationError, match="source_urls"):
        _draft(source_urls=())
    with pytest.raises(FixingValidationError, match="http"):
        _draft(source_urls=("ftp://example.org/data",))
    with pytest.raises(FixingValidationError, match="methodology_version"):
        _draft(methodology_version="  ")
    with pytest.raises(FixingValidationError, match="Decimal"):
        _draft(value=362412641743.467)
    with pytest.raises(FixingValidationError, match="negative"):
        _draft(value=D("-1"))


def test_render_covers_all_provenance():
    import json

    f = _draft()
    data = json.loads(f.render())
    assert set(data) == {
        "epoch_utc",
        "value",
        "methodology_version",
        "snapshot_hashes",
        "source_urls",
        "status",
    }
    assert data["snapshot_hashes"] == HASHES


def test_hash_binds_to_content():
    a, b = _draft(), _draft(value=D("999"))
    ha, hb = a.finalize(), b.finalize()
    assert ha != hb  # different content, different fixing hash
    c = _draft()
    assert c.finalize() == ha  # identical content, identical hash
