"""The stale-print alarm's date logic, pinned."""

from __future__ import annotations

from datetime import datetime, timezone

from tly.freshness_check import expected_epoch, main


def _dt(s):
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)


def test_grace_window_and_due_transitions():
    # Monday morning before grace ends: LAST week's epoch is what's due
    assert expected_epoch(_dt("2026-09-07T13:00:00")) == "2026-08-31T12:00:00+00:00"
    # Monday 22:00 UTC: this week's becomes due
    assert expected_epoch(_dt("2026-09-07T22:00:00")) == "2026-09-07T12:00:00+00:00"
    # Tuesday (when the workflow runs): this week's due
    assert expected_epoch(_dt("2026-09-08T06:00:00")) == "2026-09-07T12:00:00+00:00"
    # Sunday: last Monday due
    assert expected_epoch(_dt("2026-09-13T23:00:00")) == "2026-09-07T12:00:00+00:00"


def test_alarm_is_green_on_the_real_archive_right_now():
    """Whenever the suite runs, the committed archive must satisfy the
    alarm — a red here IS the stale-print signal, in CI, on every push."""
    assert main() == 0
