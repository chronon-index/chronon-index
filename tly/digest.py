"""Monthly digest (S-06): the human-readable state of the series,
generated from committed artifacts only — archive chain, stamps,
vintage ledgers, correction ledger. Written to
``docs/reports/digests/<YYYY-MM>.md`` by a monthly workflow and
published on the site build like every other report. No number in a
digest is typed by hand.
"""

from __future__ import annotations

import json
import sys
from decimal import Decimal
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
B = Decimal(10) ** 9


def build_digest(month: str, repo_root: Path = REPO_ROOT) -> str:
    """``month`` = 'YYYY-MM'. Digest of every epoch printed in it."""
    chain = json.loads((repo_root / "archive" / "chain.json").read_text(encoding="utf-8"))
    in_month = [ln for ln in chain if ln["epoch_utc"][:7] == month]
    lines = [
        f"# SAECULUM digest — {month}",
        "",
        "*Generated from committed artifacts by `tly.digest`; every number",
        "recomputes from the public archive.*",
        "",
    ]
    if not in_month:
        lines += ["No epochs were printed in this month."]
        return "\n".join(lines) + "\n"

    prev_s = None
    # previous epoch before the month, for the first delta
    idx = chain.index(in_month[0])
    if idx > 0:
        prev = json.loads(
            (repo_root / "archive" / chain[idx - 1]["file"]).read_text(encoding="utf-8")
        )
        prev_s = Decimal(prev["s_life_years"])

    rows = []
    first = last = None
    for ln in in_month:
        rec = json.loads((repo_root / "archive" / ln["file"]).read_text(encoding="utf-8"))
        s = Decimal(rec["s_life_years"])
        d = "" if prev_s is None else f"{((s / prev_s - 1) * 100):+.4f}%"
        stamped = (repo_root / "stamps" / f"{ln['epoch_utc'][:10]}.ots").is_file()
        rows.append(
            f"| {ln['epoch_utc'][:10]} | {(s / B):.4f}B | "
            f"{Decimal(rec['e_bar_years']):.4f} | {d} | "
            f"{rec['provenance']['methodology_version']} | {'✅' if stamped else '⏳'} |"
        )
        prev_s = s
        last = rec
        first = first or rec

    lines += [
        f"**{len(in_month)} epoch(s) printed.** S moved "
        f"{(Decimal(first['s_life_years']) / B):.4f}B → "
        f"{(Decimal(last['s_life_years']) / B):.4f}B; "
        f"Ē ended at {Decimal(last['e_bar_years']):.4f} years.",
        "",
        "| epoch | S | Ē | ΔS | methodology | OTS |",
        "|---|---|---|---|---|---|",
        *rows,
        "",
        "## Vintage pulls",
        "",
    ]
    vroot = repo_root / "data" / "vintages"
    if vroot.is_dir():
        for feed in sorted(p.name for p in vroot.iterdir() if p.is_dir()):
            ledger = vroot / feed / "ledger.jsonl"
            pulls = (
                [json.loads(row) for row in ledger.read_text(encoding="utf-8").splitlines() if row]
                if ledger.is_file()
                else []
            )
            in_m = [p for p in pulls if p["pull_date"][:7] == month]
            lines.append(f"- `{feed}`: {len(in_m)} pull(s) this month, {len(pulls)} total")
    corrections = (repo_root / "ledger" / "CORRECTIONS.md").read_text(encoding="utf-8")
    n_corr = corrections.count(f"| {month}-")
    lines += [
        "",
        "## Corrections",
        "",
        f"{n_corr} correction(s) entered this month (forward-only ledger; "
        "archived prints are never restated).",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    import time

    month = argv[0] if argv else time.strftime("%Y-%m", time.gmtime())
    out = REPO_ROOT / "docs" / "reports" / "digests" / f"{month}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_digest(month), encoding="utf-8")
    print(f"digest written: {out.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
