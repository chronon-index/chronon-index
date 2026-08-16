"""Correction ledger (SPEC#3 AC-3.2; RP Part X P10; DECISIONS #7).

Parses ledger/CORRECTIONS.md — the forward-only record of every deviation.
Two enforcement pieces:

- Ledger discipline: entries ``## C-NNNN | <iso-date> | <scope>`` with
  strictly increasing IDs and non-decreasing dates; the file is append-only
  (history checks live in the P10 test).
- Restatement checker: DECISIONS #7 says no historical value is EVER
  restated — corrections fold into the NEXT epoch. Between two vintages of
  a published series, any change to an epoch present in both is a
  violation, ledger entry or not; genuinely new epochs are fine. A
  correction ledger licenses the forward fold, never the rewrite.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pathlib import Path

HEADER_RE = re.compile(r"^## (C-\d{4}) \| (\d{4}-\d{2}-\d{2}) \| (.+)$")


class LedgerFormatError(ValueError):
    """ledger/CORRECTIONS.md violates the ledger format."""


@dataclass(frozen=True)
class CorrectionEntry:
    entry_id: str
    entry_date: date
    scope: str
    body: str


def parse_ledger(path: Path) -> list[CorrectionEntry]:
    """Parse and validate the ledger: increasing IDs, non-decreasing dates."""
    entries: list[CorrectionEntry] = []
    current: tuple[str, date, str] | None = None
    body: list[str] = []

    def flush() -> None:
        if current is not None:
            entries.append(
                CorrectionEntry(
                    entry_id=current[0],
                    entry_date=current[1],
                    scope=current[2],
                    body="\n".join(body).strip(),
                )
            )

    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            if current is not None:
                body.append(line)
            continue
        if in_fence:
            if current is not None:
                body.append(line)
            continue
        if line.startswith("## "):
            m = HEADER_RE.match(line)
            if not m:
                raise LedgerFormatError(f"malformed entry header: {line!r}")
            flush()
            current = (m.group(1), date.fromisoformat(m.group(2)), m.group(3).strip())
            body = []
        elif current is not None:
            body.append(line)
    flush()

    ids = [int(e.entry_id[2:]) for e in entries]
    if ids != sorted(ids) or len(set(ids)) != len(ids):
        raise LedgerFormatError(f"entry IDs must be strictly increasing: {ids}")
    dates = [e.entry_date for e in entries]
    if dates != sorted(dates):
        raise LedgerFormatError("entry dates must be non-decreasing")
    return entries


def find_restatements(
    old_vintage: dict[str, Decimal], new_vintage: dict[str, Decimal]
) -> list[str]:
    """Epochs whose published value CHANGED between vintages — always
    violations (DECISIONS #7). Epochs only in the new vintage are the
    forward fold and are fine; epochs dropped from the new vintage are
    also violations (published history may not vanish)."""
    problems: list[str] = []
    for epoch in sorted(old_vintage):
        if epoch not in new_vintage:
            problems.append(f"{epoch}: published epoch dropped from newer vintage")
        elif new_vintage[epoch] != old_vintage[epoch]:
            problems.append(
                f"{epoch}: restated {old_vintage[epoch]} -> {new_vintage[epoch]} "
                "(first print settles; corrections are forward-only)"
            )
    return problems
