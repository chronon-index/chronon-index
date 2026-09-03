"""S-03/S-06: deposit curation + digest generation, guarded."""

from __future__ import annotations

from pathlib import Path

from tly.digest import build_digest
from tly.zenodo_deposit import EXCLUDED_PREFIXES, deposit_members

REPO = Path(__file__).resolve().parent.parent


def test_deposit_curation_excludes_licensed_material_on_the_real_repo():
    members = deposit_members()
    names = [p.name for p in members]
    assert any(n.startswith("2026-") for n in names)  # archive prints in
    assert "chain.json" in names and "CORRECTIONS.md" in names
    for n in names:
        assert not n.startswith(EXCLUDED_PREFIXES), f"license-excluded file staged: {n}"
    # the exclusion BITES: WHO files exist in the repo but not the deposit
    who_in_repo = list((REPO / "data").rglob("gho_*"))
    assert who_in_repo, "expected WHO files in the repo (they are committed inputs)"
    assert not any(str(p).startswith(str(REPO / "data")) for p in members)


def test_deposit_tarball_deterministic(tmp_path):
    from tly.zenodo_deposit import build_tarball

    a = build_tarball(tmp_path / "a.tar.gz")
    b = build_tarball(tmp_path / "b.tar.gz")
    assert a == b  # mtime=0, sorted members — byte-stable


def test_digest_renders_august_from_the_archive():
    d = build_digest("2026-08")
    assert "362.4126B" in d  # both August epochs printed the same S
    assert "2026-08-17" in d and "2026-08-24" in d and "2026-08-31" in d
    assert "✅" in d  # OTS stamped
    assert "never restated" in d


def test_digest_empty_month_is_honest():
    assert "No epochs were printed" in build_digest("2019-01")
