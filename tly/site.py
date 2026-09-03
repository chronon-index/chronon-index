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
    "index": ("SAECULUM — humanity's remaining time, measured", "README.md"),
    "methodology": ("Methodology v0", "METHODOLOGY_v0.md"),
    "data-licenses": ("Data & licenses", "docs/LICENSING.md"),
    "changelog": ("Methodology changelog", "docs/METHODOLOGY_CHANGELOG.md"),
    "correction-ledger": ("Correction ledger", "ledger/CORRECTIONS.md"),
    "governance": ("Methodology change process", "docs/METHODOLOGY_CHANGE_PROCESS.md"),
    "reproduce": ("Reproduce a fixing", "docs/REPRODUCE_FIXING.md"),
    "glossary": ("Glossary", "docs/GLOSSARY.md"),
    "faq": ("FAQ", "docs/FAQ.md"),
    "api-reference": ("API reference", "docs/API_REFERENCE.md"),
    "proposal-g5": (
        "OPEN PROPOSAL: G5 source of record",
        "docs/proposals/2026-09-03-G5-source-of-record.md",
    ),
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
blockquote {{ margin: 1rem 0; padding: .4rem 1rem; border-left: 4px solid #999;
              background: #f9f9f4; }}
table {{ border-collapse: collapse; margin: 1rem 0; display: block;
         overflow-x: auto; }}
th, td {{ border: 1px solid #ccc; padding: .3rem .6rem; text-align: left; }}
code {{ background: #f2f2f2; padding: 0 .25rem; }}
pre code {{ background: none; padding: 0; }}
</style>
</head>
<body>
<nav>{nav}</nav>
{body}
</body>
</html>
"""


def _inline(text: str) -> str:
    """Escape, then render the three inline forms the governance docs use:
    `code`, **bold**, [text](http…). Escape-first means nothing an author
    writes can inject markup; unmatched syntax renders as-written."""
    import re

    s = html.escape(text)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(
        r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
        r'<a href="\2">\1</a>',
        s,
    )
    return s


def _table(rows: list[str]) -> str:
    def cells(line: str) -> list[str]:
        return [c.strip() for c in line.strip().strip("|").split("|")]

    head = cells(rows[0])
    body = [cells(r) for r in rows[2:]]  # rows[1] is the |---| separator
    out = ["<table>", "<tr>" + "".join(f"<th>{_inline(c)}</th>" for c in head) + "</tr>"]
    for r in body:
        out.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>")
    out.append("</table>")
    return "\n".join(out)


def _is_table_start(lines: list[str], i: int) -> bool:
    if not lines[i].lstrip().startswith("|") or i + 1 >= len(lines):
        return False
    sep = lines[i + 1].strip()
    return sep.startswith("|") and set(sep) <= set("|-: ")


def _render_markdown(text: str) -> str:
    """Minimal, total, deterministic rendering of the forms the governance
    docs actually use: headings, fences, paragraphs, blockquotes, tables,
    bullet lists, and the three inline forms (bold / code / links). All
    content is escaped before any markup is added — the generator cannot
    inject, and anything outside these forms renders as-written."""
    out: list[str] = []
    in_fence = False
    paragraph: list[str] = []

    def flush() -> None:
        if paragraph:
            out.append("<p>" + _inline("\n".join(paragraph)) + "</p>")
            paragraph.clear()

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            flush()
            out.append("<pre>" if not in_fence else "</pre>")
            in_fence = not in_fence
            i += 1
            continue
        if in_fence:
            out.append(html.escape(line))
            i += 1
            continue
        if line.startswith("#"):
            flush()
            level = min(len(line) - len(line.lstrip("#")), 6)
            out.append(f"<h{level}>{_inline(line.lstrip('#').strip())}</h{level}>")
            i += 1
        elif line.startswith(">"):
            flush()
            quoted: list[str] = []
            while i < len(lines) and lines[i].startswith(">"):
                quoted.append(lines[i].lstrip(">").lstrip())
                i += 1
            inner = _render_markdown("\n".join(quoted))
            out.append(f"<blockquote>\n{inner}\n</blockquote>")
        elif _is_table_start(lines, i):
            flush()
            rows: list[str] = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append(_table(rows))
        elif line.lstrip().startswith("- "):
            flush()
            out.append("<ul>")
            while i < len(lines) and lines[i].lstrip().startswith("- "):
                item = [lines[i].lstrip()[2:]]
                i += 1
                # continuation lines (indented, not a new bullet/blank)
                while (
                    i < len(lines)
                    and lines[i].startswith("  ")
                    and not lines[i].lstrip().startswith("- ")
                ):
                    item.append(lines[i].strip())
                    i += 1
                out.append(f"<li>{_inline(' '.join(item))}</li>")
            out.append("</ul>")
        elif not line.strip():
            flush()
            i += 1
        else:
            paragraph.append(line)
            i += 1
    flush()
    if in_fence:
        out.append("</pre>")  # unterminated fence still yields valid HTML
    return "\n".join(out)


def _dashboard_markdown(repo_root: Path) -> str:
    """S-08: the index dashboard, synthesized STATICALLY from the committed
    archive at build time (print.yml rebuilds weekly) — settlement surfaces
    stay JavaScript-free. The price panel is honest: no market exists."""
    import json
    from decimal import Decimal

    chain = json.loads((repo_root / "archive" / "chain.json").read_text(encoding="utf-8"))
    rows = []
    prev_s = None
    latest = None
    B = Decimal(10) ** 9
    for link in chain:
        rec = json.loads((repo_root / "archive" / link["file"]).read_text(encoding="utf-8"))
        s = Decimal(rec["s_life_years"])
        g = "" if prev_s is None else f"{((s / prev_s - 1) * 100):+.4f}%"
        rows.append(
            f"| {rec['epoch_utc'][:10]} | {(s / B):.4f}B | "
            f"{Decimal(rec['e_bar_years']):.4f} | {int(Decimal(rec['n_persons'])):,} | {g} | "
            f"{rec['provenance']['methodology_version']} |"
        )
        prev_s = s
        latest = rec
    s = Decimal(latest["s_life_years"])
    lines = [
        "# The index",
        "",
        f"**S = {(s / B):.4f} billion life-years** — humanity's total remaining",
        f"time as of epoch {latest['epoch_utc'][:10]} (measured-period,",
        "settlement series). Average remaining time per living person:",
        f"**{Decimal(latest['e_bar_years']):.2f} years** across",
        f"{int(Decimal(latest['n_persons'])):,} people.",
        "",
        "One token = one life-year; supply mirrors S, so a holder's SHARE of",
        "humanity's remaining time never changes — only the size of the pie",
        "does. Every number below recomputes from public artifacts",
        "([reproduce it](reproduce.html)).",
        "",
        "## Price",
        "",
        "**No market exists yet.** The index is live and settling weekly; the",
        "token has not launched (counsel, entity and audits come first — the",
        "process is public in the repo). When a market exists, this panel",
        "shows the traded price of one life-year. The vision anchor: at",
        "burger parity ($6 per 15 minutes), one life-year is $210,384.",
        "",
        "## Weekly prints (from the immutable archive)",
        "",
        "| epoch | S | E-bar | N | dS | methodology |",
        "|---|---|---|---|---|---|",
        *rows,
        "",
        "Prints are FINAL when archived (first-print-settles): corrections",
        "are forward-only via the public [correction ledger](correction-ledger.html).",
        "Each record hash is Bitcoin-timestamped (stamps/ in the repo).",
        "",
        "## Your own time",
        "",
        "The [personal page](me.html) estimates YOUR remaining time from an",
        "in-depth questionnaire — computed entirely in your browser (nothing",
        "you enter ever leaves it), with the math explained line by line.",
    ]
    return "\n".join(lines)


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
    all_names = ["dashboard"] + list(PAGES) + ["vintage-archive", "me"]
    titles = {name: PAGES[name][0] for name in PAGES}
    titles["dashboard"] = "The index"
    titles["vintage-archive"] = "Vintage archive"
    titles["me"] = "Your time"
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
    body = _render_markdown(_dashboard_markdown(repo_root))
    page = _SHELL.format(title="The index — SAECULUM", nav=nav, body=body)
    (site / "dashboard.html").write_text(page, encoding="utf-8")
    written["dashboard"] = "site/dashboard.html"
    from tly.personal_page import build_personal_page

    (site / "me.html").write_text(build_personal_page(repo_root, nav), encoding="utf-8")
    written["me"] = "site/me.html"
    return written


def not_found_page() -> str:
    """The 404 page (served BY STATUS 404 on Cloudflare Pages — its
    presence is what makes nonexistent paths say no; without it every
    path returns the home page at 200, which for the API means a
    fabricated print date looks like a success. Found live by the
    2026-09-03 deploy verification)."""
    body = (
        "<h1>404 — no such artifact</h1>\n"
        "<p>Nothing exists at this path. Prints that were never made do "
        "not resolve — <em>first print settles</em> also means absence "
        "is an answer.</p>\n"
        "<p>Everything that exists is enumerated, with hashes, in "
        '<a href="/api/v1/index.json">api/v1/index.json</a>; the pages '
        'are linked from the <a href="/">home page</a>.</p>'
    )
    return _SHELL.format(title="404 — not found", nav='<a href="/">home</a>', body=body)
