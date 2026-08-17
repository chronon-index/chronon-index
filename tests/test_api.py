"""B-uc4-02 / AC-4.4: static JSON API — committed files only, self-verifying."""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

import pytest

from tly.api import assert_static_only, build_api, load_latest_s, verify_api
from tly.prints import WeeklyPrint, validate_print_dict
from tly.stock import LocationStock, stamp

REPO = Path(__file__).resolve().parent.parent
SNAP16 = REPO / "data" / "snapshots" / "2026-08-16"

D = Decimal


def _print(epoch: str, s: str) -> WeeklyPrint:
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


PRINTS = [
    _print("2026-08-03T12:00:00+00:00", "362412000000.0001"),
    _print("2026-08-10T12:00:00+00:00", "362412500000.0002"),
    _print("2026-08-17T12:00:00+00:00", "362413000000.0003"),
]

COUNTRIES = [
    LocationStock("Japan", "JPN", 2023, "total", D("4803100000"), D("124370947")),
    LocationStock("Nigeria", "NGA", 2023, "total", D("9604100000"), D("227882950")),
]


def test_build_layout_and_latest(tmp_path):
    build_api(PRINTS, tmp_path, country_stocks=COUNTRIES)
    root = tmp_path / "api" / "v1"
    assert (root / "latest.json").is_file()
    assert (root / "prints" / "2026-08-03.json").is_file()
    assert (root / "prints" / "2026-08-17.json").is_file()
    assert (root / "countries.json").is_file()
    assert load_latest_s(tmp_path) == D("362413000000.0003")  # newest epoch wins
    # every per-epoch artifact passes the consumer print schema
    for f in (root / "prints").glob("*.json"):
        validate_print_dict(json.loads(f.read_text()))
    countries = json.loads((root / "countries.json").read_text())
    assert countries["Japan"]["iso3"] == "JPN"


def test_index_self_describes_integrity(tmp_path):
    build_api(PRINTS, tmp_path)
    verify_api(tmp_path)  # hashes match
    # tamper -> verify fails
    victim = tmp_path / "api" / "v1" / "latest.json"
    victim.write_text(victim.read_text().replace("362413", "999999"))
    with pytest.raises(ValueError, match="sha256 mismatch"):
        verify_api(tmp_path)


def test_undescribed_artifact_detected(tmp_path):
    build_api(PRINTS, tmp_path)
    (tmp_path / "api" / "v1" / "rogue.json").write_text("{}")
    with pytest.raises(ValueError, match="not in index"):
        verify_api(tmp_path)


def test_static_only_gate(tmp_path):
    build_api(PRINTS, tmp_path)
    assert_static_only(tmp_path)  # clean build passes
    (tmp_path / "api" / "v1" / "server.py").write_text("print('hi')")
    with pytest.raises(ValueError, match="non-JSON artifact"):
        assert_static_only(tmp_path)


def test_build_is_deterministic(tmp_path):
    a_dir, b_dir = tmp_path / "a", tmp_path / "b"
    build_api(PRINTS, a_dir, country_stocks=COUNTRIES)
    build_api(PRINTS, b_dir, country_stocks=COUNTRIES)
    a_files = sorted((a_dir / "api" / "v1").rglob("*.json"))
    b_files = sorted((b_dir / "api" / "v1").rglob("*.json"))
    assert [p.name for p in a_files] == [p.name for p in b_files]
    for pa, pb in zip(a_files, b_files):
        assert pa.read_bytes() == pb.read_bytes()


def test_build_rejects_bad_inputs(tmp_path):
    with pytest.raises(ValueError, match="zero prints"):
        build_api([], tmp_path)
    with pytest.raises(ValueError, match="duplicate epochs"):
        build_api([PRINTS[0], PRINTS[0]], tmp_path)
