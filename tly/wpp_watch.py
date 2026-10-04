"""WPP revision watchdog (RP Part V Q7; built 2026-10-03).

The UN's biennial World Population Prospects revision will restate our
source-of-record level. The machinery for absorbing it exists (new
vintage snapshot, dual-run, governed version bump — the G5 playbook);
this watchdog makes sure the revision is NOTICED the week it lands,
never discovered mid-print.

Mechanism: fetch the live WPP downloads index and scan for any revision
tag newer than the one our committed baseline carries (WPP2024). A hit
exits nonzero — a RED scheduled run is the alarm, same pattern as the
stale-print check. Network failure is reported but exits 0 (an outage
is not a revision; the weekly cadence retries).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_URL = "https://population.un.org/wpp/assets/downloads.json"
BASELINE_REVISION = 2024  # our source of record (G5, methodology v0.7.0)


def newer_revisions(index_text: str, baseline: int = BASELINE_REVISION) -> list[int]:
    """Revision years in the index strictly newer than the baseline."""
    years = {int(m) for m in re.findall(r"WPP(20\d\d)", index_text)}
    return sorted(y for y in years if y > baseline)


def main() -> int:
    try:
        from tly.snapshot import fetch_url

        text = fetch_url(INDEX_URL).decode("utf-8")
    except Exception as err:  # noqa: BLE001 — outage is not a revision
        print(f"fetch failed ({err}) — cannot check this week; not an alarm")
        return 0
    json.loads(text)  # malformed index should fail loudly below, not silently
    found = newer_revisions(text)
    if not found:
        print(f"no revision newer than WPP{BASELINE_REVISION} in the live index")
        return 0
    print(f"WPP REVISION ALARM: WPP{found[-1]} is live in the UN downloads index.")
    print("Playbook (the G5 pattern, docs/proposals/2026-09-03-G5-source-of-record.md):")
    print(" 1. snapshot the new files into a dated vintage (hash-manifested),")
    print(" 2. dual-run old vs new tables, publish the level delta,")
    print(" 3. governed version bump; archived prints stand (P4).")
    print("Until the bump, prints continue on the committed WPP2024 vintage —")
    print("frozen inputs mean nothing drifts silently.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
