"""B-uc2-17: the append-only weekly-feed vintage store."""

from __future__ import annotations

import json
from datetime import date

import pytest

from tly.vintage_store import VintageStore, VintageStoreError


def test_store_ledger_verify_roundtrip(tmp_path):
    store = VintageStore(tmp_path)
    r1 = store.store_pull("eurostat_weekly", date(2026, 8, 25), b'{"a":1}', "https://x")
    assert r1["new"] is True
    # idempotent for identical bytes
    r2 = store.store_pull("eurostat_weekly", date(2026, 8, 25), b'{"a":1}', "https://x")
    assert r2["new"] is False
    assert len(store.ledger("eurostat_weekly")) == 1
    store.verify("eurostat_weekly")


def test_vintages_never_mutate(tmp_path):
    store = VintageStore(tmp_path)
    store.store_pull("cdc_weekly", date(2026, 8, 25), b'{"v":1}', "https://x")
    with pytest.raises(VintageStoreError, match="never mutate"):
        store.store_pull("cdc_weekly", date(2026, 8, 25), b'{"v":2}', "https://x")


def test_verify_catches_tamper_and_strays(tmp_path):
    store = VintageStore(tmp_path)
    store.store_pull("f", date(2026, 8, 25), b"data", "https://x")
    (tmp_path / "f" / "2026-08-25.json").write_bytes(b"tampered")
    with pytest.raises(VintageStoreError, match="mutated"):
        store.verify("f")
    (tmp_path / "f" / "2026-08-25.json").write_bytes(b"data")  # restore
    (tmp_path / "f" / "2026-09-01.json").write_bytes(b"stray")
    with pytest.raises(VintageStoreError, match="unledgered"):
        store.verify("f")


def test_lag_triangle_accumulates_across_pulls(tmp_path):
    """The reason the store exists: the same week's value seen from
    successive pull dates — immature first, mature later."""
    store = VintageStore(tmp_path)
    store.store_pull("cdc", date(2026, 8, 18), json.dumps({"2026-W32": 20000}).encode(), "u")
    store.store_pull(
        "cdc", date(2026, 8, 25), json.dumps({"2026-W32": 39000, "2026-W33": 21000}).encode(), "u"
    )
    store.store_pull(
        "cdc", date(2026, 9, 1), json.dumps({"2026-W32": 47500, "2026-W33": 40000}).encode(), "u"
    )

    tri = store.lag_triangle("cdc", lambda b: json.loads(b))
    w32 = tri["2026-W32"]
    assert [w32[d] for d in sorted(w32)] == [20000, 39000, 47500]  # maturation visible
    assert len(tri["2026-W33"]) == 2  # younger week, fewer observations
