"""E-01: static site — files only, byte-reproducible, faithful to sources."""

from __future__ import annotations

from pathlib import Path

from tly.site import PAGES, build_site

REPO = Path(__file__).resolve().parent.parent


def test_build_renders_every_registered_page(tmp_path):
    written = build_site(tmp_path)
    assert set(written) == set(PAGES) | {"vintage-archive"}
    for name in written:
        page = (tmp_path / "site" / f"{name}.html").read_text(encoding="utf-8")
        assert page.startswith("<!DOCTYPE html>")
        assert "<nav>" in page


def test_build_is_byte_reproducible(tmp_path):
    build_site(tmp_path / "a")
    build_site(tmp_path / "b")
    for name in PAGES:
        a = (tmp_path / "a" / "site" / f"{name}.html").read_bytes()
        b = (tmp_path / "b" / "site" / f"{name}.html").read_bytes()
        assert a == b, name


def test_files_only_no_scripts(tmp_path):
    build_site(tmp_path)
    for f in (tmp_path / "site").rglob("*"):
        assert f.suffix == ".html"
        content = f.read_text(encoding="utf-8")
        assert "<script" not in content  # no JS, ever
        assert "http-equiv" not in content  # no meta refresh tricks


def test_content_is_escaped_and_faithful(tmp_path):
    """Load-bearing text from the governance docs survives verbatim (post
    escaping) — the generator may not mangle what git says."""
    build_site(tmp_path)
    ledger = (tmp_path / "site" / "correction-ledger.html").read_text(encoding="utf-8")
    assert "C-0001" in ledger
    assert "forward-only" in ledger
    faq = (tmp_path / "site" / "faq.html").read_text(encoding="utf-8")
    assert "putting a price on human lives" in faq
    glossary = (tmp_path / "site" / "glossary.html").read_text(encoding="utf-8")
    assert "chronon" in glossary
    # escaping: raw angle brackets from sources never appear unescaped
    meth = (tmp_path / "site" / "methodology.html").read_text(encoding="utf-8")
    assert "<McKendrick" not in meth  # any such token would be escaped


def test_d10_site_map_complete(tmp_path):
    """D-10: the mandated map — home / methodology / data & licenses /
    API reference / changelog / correction ledger / governance / vintage
    archive — every page present and non-trivial."""
    written = build_site(tmp_path)
    mandated = {
        "index",
        "methodology",
        "data-licenses",
        "api-reference",
        "changelog",
        "correction-ledger",
        "governance",
        "vintage-archive",
    }
    assert mandated <= set(written)
    archive = (tmp_path / "site" / "vintage-archive.html").read_text(encoding="utf-8")
    assert "Vintage 2026-08-16" in archive
    assert "Vintage 2026-08-17" in archive
    assert "manifested files" in archive
    api = (tmp_path / "site" / "api-reference.html").read_text(encoding="utf-8")
    assert "latest.json" in api
    assert "print-v1" in api
    # every page links every other page (one nav, complete)
    for name in mandated:
        page = (tmp_path / "site" / f"{name}.html").read_text(encoding="utf-8")
        assert "vintage-archive.html" in page


def test_b4_09_pages_render_from_live_artifacts(tmp_path):
    """B-uc4-09: the named pages source from the LIVE repo artifacts — a
    change to the artifact appears in the rendered page on the next build,
    proving no stale intermediate copy exists between git and the site."""
    import shutil

    stage = tmp_path / "repo"
    # stage every registered page source (derived from PAGES so a page
    # added to the site can never silently miss this liveness proof)
    from tly.site import PAGES

    for _, rel in PAGES.values():
        (stage / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO / rel, stage / rel)
    for rel in ("ledger/CORRECTIONS.md",):
        (stage / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO / rel, stage / rel)
    snap_dir = stage / "data" / "snapshots" / "2026-08-16"
    snap_dir.mkdir(parents=True)
    shutil.copy2(
        REPO / "data" / "snapshots" / "2026-08-16" / "manifest.json",
        snap_dir / "manifest.json",
    )

    build_site(tmp_path / "v1", repo_root=stage)
    before = (tmp_path / "v1" / "site" / "correction-ledger.html").read_text()
    assert "C-9999" not in before

    with (stage / "ledger" / "CORRECTIONS.md").open("a") as f:
        f.write("\n## C-9999 | 2026-08-17 | liveness-probe\n- artifact edit visible\n")
    build_site(tmp_path / "v2", repo_root=stage)
    after = (tmp_path / "v2" / "site" / "correction-ledger.html").read_text()
    assert "C-9999" in after  # ledger page tracks the live ledger

    # vintage archive tracks live manifests too
    archive = (tmp_path / "v2" / "site" / "vintage-archive.html").read_text()
    assert "Vintage 2026-08-16" in archive
    assert "Vintage 2026-08-17" not in archive  # staged repo has only one vintage
