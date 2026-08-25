"""B-uc4-07 / AC-4.5: stale-print CI integration — a missing source flips
the status flag within the same epoch, walked through the real ladder."""

from __future__ import annotations

from tly.failure_ladder import CARRY, DEFER, HEALTHY, STALE, SourceState, evaluate_ladder

FEEDS = ("eurostat_weekly", "cdc_weekly", "wpp_structure")


def _states(down: dict[str, int] | None = None) -> list[SourceState]:
    down = down or {}
    return [
        SourceState(
            name=f,
            available=f not in down,
            last_vintage="2026-08-25" if f not in down else "2026-08-18",
            epochs_carried=max(0, down.get(f, 0) - 1) if f in down else 0,
        )
        for f in FEEDS
    ]


def test_missing_source_flips_status_same_epoch():
    """The AC: healthy one epoch; a source goes down; THE SAME epoch's
    decision already carries the flipped flag — no grace epoch."""
    healthy = evaluate_ladder(_states())
    assert healthy.action == HEALTHY
    outage = evaluate_ladder(_states(down={"eurostat_weekly": 1}))
    assert outage.action == CARRY  # flipped immediately
    assert outage.status_block()["sources"]["eurostat_weekly"]["state"] == CARRY
    assert outage.status_block()["sources"]["eurostat_weekly"]["vintage"] == "2026-08-18"
    assert outage.publish_print and outage.publish_fixing  # carry, not stop


def test_full_ladder_walk_carry_stale_defer():
    """Consecutive epochs of the same outage walk every rung in order,
    and recovery snaps back to HEALTHY."""
    seen = []
    for carried in (1, 2, 3, 4, 5):
        d = evaluate_ladder(_states(down={"cdc_weekly": carried}))
        seen.append(d.action)
    assert seen == [CARRY, CARRY, STALE, STALE, DEFER]
    deferred = evaluate_ladder(_states(down={"cdc_weekly": 5}))
    assert deferred.publish_print and not deferred.publish_fixing
    assert deferred.status_block()["fixing"] == "DEFERRED"
    recovered = evaluate_ladder(_states())
    assert recovered.action == HEALTHY and recovered.publish_fixing
