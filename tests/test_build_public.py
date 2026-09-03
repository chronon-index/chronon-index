"""E-08: the committed site/ tree is exactly what the builder produces —
the deployed surface can never drift from the committed artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tly.api import API_ROOT
from tly.build_public import build_public

REPO = Path(__file__).resolve().parent.parent


def _tree_hashes(root: Path) -> dict[str, str]:
    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in root.rglob("*")
        if p.is_file()
    }


def test_committed_site_matches_fresh_build(tmp_path):
    committed = _tree_hashes(REPO / "site")
    # build into a copy of the repo layout? build_public writes in place —
    # compare against a rebuild in a scratch clone of the inputs instead:
    # the builder is deterministic, so building twice in place and hashing
    # before/after would destroy evidence on failure. Hash, rebuild, hash.
    build_public(REPO)
    rebuilt = _tree_hashes(REPO / "site")
    assert committed == rebuilt, (
        "committed site/ differs from a fresh build — run "
        "`python -m tly.build_public` and commit the result"
    )


def test_api_serves_archived_bytes_verbatim():
    chain = json.loads((REPO / "archive" / "chain.json").read_text(encoding="utf-8"))
    root = (REPO / "site").joinpath(*API_ROOT)
    for link in chain:
        archived = (REPO / "archive" / link["file"]).read_bytes()
        date = link["epoch_utc"][:10]
        assert (root / "prints" / f"{date}.json").read_bytes() == archived
    assert (root / "latest.json").read_bytes() == (
        REPO / "archive" / chain[-1]["file"]
    ).read_bytes()


def test_headers_file_present_with_cors_on_api():
    text = (REPO / "site" / "_headers").read_text(encoding="utf-8")
    assert "/api/*" in text and "Access-Control-Allow-Origin: *" in text
    assert "X-Content-Type-Options: nosniff" in text
