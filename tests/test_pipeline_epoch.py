"""B-uc4-04: current-epoch derivation — injectable, deterministic tests."""

from datetime import datetime, timezone

from tly.pipeline import current_epoch


def test_current_epoch_midweek():
    now = datetime(2026, 8, 20, 9, 0, tzinfo=timezone.utc)  # a Thursday
    assert current_epoch(now) == "2026-08-17T12:00:00+00:00"


def test_current_epoch_monday_before_and_after_noon():
    before = datetime(2026, 8, 17, 11, 59, tzinfo=timezone.utc)
    after = datetime(2026, 8, 17, 12, 0, tzinfo=timezone.utc)
    assert current_epoch(before) == "2026-08-10T12:00:00+00:00"
    assert current_epoch(after) == "2026-08-17T12:00:00+00:00"


def test_current_epoch_validates_against_print_schema():
    from tly.prints import validate_epoch

    now = datetime(2026, 12, 31, 23, 59, tzinfo=timezone.utc)
    validate_epoch(current_epoch(now))
