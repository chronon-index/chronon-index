"""Static site generator (RP Part VII/XI; E-01). Files only.

Renders committed repo artifacts into a plain HTML tree. No server, no
JavaScript, no external assets — the publication surface stays as dumb as
the API (the attack surface is the repo and the data). The markdown
treatment is deliberately minimal and total: headers, fenced code, and
paragraphs; everything else renders as-written inside escaped text, so the
site can never silently mangle a governance document — what you read on
the page is byte-derived from what is in git.

Building is a pure function of the input files: identical inputs yield a
byte-identical tree (tested).
"""

from __future__ import annotations

import html
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# page name -> (title, source file relative to repo root)
PAGES: dict[str, tuple[str, str]] = {
    "index": ("TLY — humanity's remaining time, measured", "README.md"),
    "methodology": ("Methodology v0", "METHODOLOGY_v0.md"),
    "data-licenses": ("Data & licenses", "docs/LICENSING.md"),
    "changelog": ("Methodology changelog", "docs/METHODOLOGY_CHANGELOG.md"),
    "correction-ledger": ("Correction ledger", "ledger/CORRECTIONS.md"),
    "governance": ("Methodology change process", "docs/METHODOLOGY_CHANGE_PROCESS.md"),
    "reproduce": ("Reproduce a fixing", "docs/REPRODUCE_FIXING.md"),
    "glossary": ("Glossary", "docs/GLOSSARY.md"),
    "faq": ("FAQ", "docs/FAQ.md"),
    "api-reference": ("API reference", "docs/API_REFERENCE.md"),
}

_SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
body {{ max-width: 46rem; margin: 2rem auto; padding: 0 1rem;
       font: 16px/1.6 system-ui, sans-serif; color: #222; }}
pre {{ background: #f6f6f6; padding: .8rem; overflow-x: auto; }}
nav {{ font-size: .9rem; margin-bottom: 2rem; }}
h1, h2, h3 {{ line-height: 1.25; }}
</style>
</head>
<body>
<nav>{nav}</nav>
{body}
</body>
</html>
"""


def _render_markdown(text: str) -> str:
    """Minimal, total, deterministic: headers, code fences, paragraphs.
    All content is HTML-escaped — the generator cannot inject or mangle."""
    out: list[str] = []
    in_fence = False
    paragraph: list[str] = []

    def flush() -> None:
        if paragraph:
            out.append("<p>" + html.escape("\n".join(paragraph)) + "</p>")
            paragraph.clear()

    for line in text.splitlines():
        if line.startswith("```"):
            flush()
            out.append("<pre>" if not in_fence else "</pre>")
            in_fence = not in_fence
            continue
        if in_fence:
            out.append(html.escape(line))
            continue
        if line.startswith("#"):
            flush()
            level = min(len(line) - len(line.lstrip("#")), 6)
            out.append(f"<h{level}>{html.escape(line.lstrip('#').strip())}</h{level}>")
        elif not line.strip():
            flush()
        else:
            paragraph.append(line)
    flush()
    if in_fence:
        out.append("</pre>")  # unterminated fence still yields valid HTML
    return "\n".join(out)


def _vintage_archive_markdown(repo_root: Path) -> str:
    """Synthesize the vintage-archive page from the committed manifests —
    the page IS the manifest record, restated; nothing is invented."""
    import json

    lines = [
        "# Vintage archive",
        "",
        "Every dated snapshot generation, from the committed manifests.",
        "Vintages are immutable: upstream revisions create NEW vintages",
        "beside the old (first print settles; RP Part VI).",
        "",
    ]
    root = repo_root / "data" / "snapshots"
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        mf = d / "manifest.json"
        if not mf.is_file():
            continue
        manifest = json.loads(mf.read_text(encoding="utf-8"))
        files = manifest.get("files", {})
        committed = sum(1 for r in files.values() if r.get("in_git") is not False)
        lines.append(f"## Vintage {d.name}")
        lines.append("")
        lines.append(
            f"{len(files)} manifested files ({committed} committed, "
            f"{len(files) - committed} manifest-only large files)."
        )
        lines.append("")
        lines.append("```")
        for name, row in sorted(files.items()):
            lines.append(f"{row.get('sha256', '?')[:16]}…  {name}")
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


def build_site(out_dir: Path, repo_root: Path = REPO_ROOT) -> dict[str, str]:
    """Render every registered page + the synthesized vintage archive."""
    site = out_dir / "site"
    site.mkdir(parents=True, exist_ok=True)
    all_names = list(PAGES) + ["vintage-archive"]
    titles = {name: PAGES[name][0] for name in PAGES}
    titles["vintage-archive"] = "Vintage archive"
    nav = " · ".join(f'<a href="{name}.html">{html.escape(titles[name])}</a>' for name in all_names)
    written: dict[str, str] = {}
    for name, (title, source_rel) in PAGES.items():
        source = repo_root / source_rel
        body = _render_markdown(source.read_text(encoding="utf-8"))
        page = _SHELL.format(title=html.escape(title), nav=nav, body=body)
        (site / f"{name}.html").write_text(page, encoding="utf-8")
        written[name] = f"site/{name}.html"
    body = _render_markdown(_vintage_archive_markdown(repo_root))
    page = _SHELL.format(title="Vintage archive", nav=nav, body=body)
    (site / "vintage-archive.html").write_text(page, encoding="utf-8")
    written["vintage-archive"] = "site/vintage-archive.html"
    return written
