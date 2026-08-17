"""C-uc7-06 / AC-7.5: the outsider doc exists, its commands actually run,
and it names every load-bearing mechanism."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOC = REPO / "docs" / "REPRODUCE_FIXING.md"


def test_doc_names_every_mechanism():
    doc = DOC.read_text(encoding="utf-8")
    for needed in (
        "python -m tly.pipeline",
        "test_manifest_schema",
        "test_snapshot_immutability",
        "test_p5_reproducibility",
        "settle_from_archive",
        "fixing_hash",
        "manifest.json",
        "in_git",
        "48 hours",
        "CORRECTIONS.md",
        "never rewritten",
    ):
        assert needed in doc, f"outsider doc missing: {needed}"


def test_doc_step_6_code_actually_runs(tmp_path):
    """The doc's step-6 snippet, executed verbatim-in-spirit as an
    outsider would: it must produce a 64-hex fixing hash."""
    code = f"""
from pathlib import Path
from tly.archive import PrintArchive
from tly.fixings import settle_from_archive
from tly.pipeline import build_settlement_print

archive = PrintArchive(Path(r"{tmp_path}"))
archive.append(build_settlement_print("2026-08-17T12:00:00+00:00"))
fixing = settle_from_archive(
    archive, "2026-08-17T12:00:00+00:00", Path("data/snapshots")
)
print(fixing.fixing_hash)
"""
    proc = subprocess.run(
        [sys.executable, "-c", code], cwd=REPO, capture_output=True, text=True, check=True
    )
    digest = proc.stdout.strip()
    assert len(digest) == 64 and all(c in "0123456789abcdef" for c in digest)


def test_doc_honest_about_current_state():
    doc = DOC.read_text(encoding="utf-8")
    assert "not yet" in doc  # the A-17 / no-official-prints caveat is stated
    assert "does not prove" in doc  # the epistemics section exists
