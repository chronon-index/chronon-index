"""B-uc3-05 / AC-3.2 / invariant P10: correction completeness, forward-only.

The named test runs the real ledger through the parser, proves the ledger
file is append-only in git (existing entry blocks byte-unchanged across
history and into the worktree), and exercises the restatement checker on
synthetic vintage pairs.
"""

from __future__ import annotations

import subprocess
from decimal import Decimal
from pathlib import Path

import pytest

from tly.corrections import (
    LedgerFormatError,
    find_restatements,
    parse_ledger,
)

REPO = Path(__file__).resolve().parent.parent
LEDGER = REPO / "ledger" / "CORRECTIONS.md"

D = Decimal


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(REPO), *args], check=True, capture_output=True, text=True
    ).stdout


def _entry_blocks(text: str) -> dict[str, str]:
    """entry_id -> raw block text, for byte-level history comparison."""
    blocks: dict[str, str] = {}
    current = None
    for line in text.splitlines():
        if line.startswith("## C-"):
            current = line.split(" | ")[0][3:]
            blocks[current] = line
        elif current is not None:
            blocks[current] += "\n" + line
    return {k: v.rstrip() for k, v in blocks.items()}


def test_p10_correction_completeness():
    """Named per RP Part X. Real ledger parses with valid discipline;
    entry blocks are byte-identical across every committed version and
    into the worktree (append-only, forward-applied only)."""
    entries = parse_ledger(LEDGER)
    assert entries, "ledger must contain at least C-0001"
    assert entries[0].entry_id == "C-0001"
    assert "napkin" in entries[0].body or "+2.9" in entries[0].body

    rel = "ledger/CORRECTIONS.md"
    hashes = _git("log", "--reverse", "--pretty=format:%H", "--", rel).splitlines()
    versions = [_entry_blocks(_git("show", f"{h}:{rel}")) for h in hashes]
    versions.append(_entry_blocks(LEDGER.read_text(encoding="utf-8")))
    problems: list[str] = []
    for older, newer in zip(versions, versions[1:]):
        for entry_id, block in older.items():
            if entry_id not in newer:
                problems.append(f"{entry_id}: entry deleted")
            elif newer[entry_id] != block:
                problems.append(f"{entry_id}: entry edited (append-only violated)")
    assert problems == [], "\n".join(problems)


def test_restatement_checker():
    old = {"2026-08-17": D("362.4126"), "2026-08-24": D("362.4130")}
    same_plus_new = dict(old, **{"2026-08-31": D("362.4135")})
    assert find_restatements(old, same_plus_new) == []  # forward fold only

    restated = dict(same_plus_new, **{"2026-08-17": D("362.5000")})
    problems = find_restatements(old, restated)
    assert len(problems) == 1 and "restated" in problems[0]

    dropped = {"2026-08-24": D("362.4130")}
    problems = find_restatements(old, dropped)
    assert len(problems) == 1 and "dropped" in problems[0]


def test_parser_rejects_malformed_ledgers(tmp_path):
    bad = tmp_path / "L.md"
    bad.write_text("## C-1 | 2026-08-17 | scope\n- x\n")  # ID not 4 digits
    with pytest.raises(LedgerFormatError, match="malformed entry header"):
        parse_ledger(bad)

    bad.write_text("## C-0002 | 2026-08-17 | a\n- x\n\n## C-0001 | 2026-08-18 | b\n- y\n")
    with pytest.raises(LedgerFormatError, match="strictly increasing"):
        parse_ledger(bad)

    bad.write_text("## C-0001 | 2026-08-18 | a\n- x\n\n## C-0002 | 2026-08-17 | b\n- y\n")
    with pytest.raises(LedgerFormatError, match="non-decreasing"):
        parse_ledger(bad)
