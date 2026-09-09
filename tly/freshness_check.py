"""Print-freshness alarm (2026-09-09; born from the external verifier
catching a 5.6-hour-late Monday cron). Exits nonzero — a RED scheduled
run, the in-repo alarm — if the newest archived epoch is not the most
recent Monday once that Monday is comfortably past (grace ends 22:00
UTC Monday; the check itself runs Tuesdays). Idempotent, read-only."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GRACE_END_HOUR = 22  # Monday 22:00 UTC: all three cron slots long past


def expected_epoch(now: datetime) -> str | None:
    """The Monday-12:00 epoch that MUST be archived by ``now`` — or None
    while still inside Monday's grace window."""
    monday = now.date() - timedelta(days=now.weekday())
    epoch = datetime(monday.year, monday.month, monday.day, 12, tzinfo=timezone.utc)
    if now < epoch + timedelta(hours=GRACE_END_HOUR - 12):
        epoch -= timedelta(days=7)  # this week's not yet due; last week's is
    return epoch.isoformat()


def main() -> int:
    now = datetime.now(timezone.utc)
    due = expected_epoch(now)
    chain = json.loads((REPO_ROOT / "archive" / "chain.json").read_text(encoding="utf-8"))
    newest = chain[-1]["epoch_utc"]
    if newest >= due:
        print(f"FRESH: newest archived epoch {newest} covers due epoch {due}")
        return 0
    print(f"STALE PRINT ALARM: due epoch {due} is NOT archived (newest: {newest}).")
    print("The Monday print did not land through any cron slot — dispatch")
    print("weekly-print manually and investigate the runs' timestamps.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
