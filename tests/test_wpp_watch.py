"""Q7 watchdog: detector logic pinned on the committed baseline + synthetic futures."""

from __future__ import annotations

from pathlib import Path

from tly.wpp_watch import BASELINE_REVISION, newer_revisions

REPO = Path(__file__).resolve().parent.parent


def test_committed_index_is_quiet():
    text = (REPO / "data/snapshots/2026-08-17/wpp_downloads_index.json").read_text()
    assert "WPP2024" in text  # baseline really present
    assert newer_revisions(text) == []


def test_synthetic_revision_trips():
    text = '{"Folders": ["WPP2024_Foo.csv.gz", "WPP2026_Bar.csv.gz", "WPP2026_Baz.csv.gz"]}'
    assert newer_revisions(text) == [2026]


def test_older_revisions_never_trip():
    assert newer_revisions('{"x": "WPP2022_Old.csv WPP2019_Ancient.csv"}') == []
    assert BASELINE_REVISION == 2024  # bump this constant WITH the methodology, not alone
