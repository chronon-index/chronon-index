"""E-04 / AC-4.5: each ladder rung simulated — down → carry → stale → defer."""

from __future__ import annotations

import pytest

from tly.failure_ladder import (
    CARRY,
    DEFER,
    HEALTHY,
    STALE,
    LadderDecision,
    SourceState,
    evaluate_ladder,
)


def _src(name="wpp", available=True, carried=0, vintage="2026-08-17"):
    return SourceState(name=name, available=available, last_vintage=vintage, epochs_carried=carried)


def test_rung0_healthy():
    d = evaluate_ladder([_src(), _src(name="wmd")])
    assert (d.rung, d.action) == (0, HEALTHY)
    assert d.publish_print and d.publish_fixing
    assert d.status_block()["fixing"] == "published"


def test_rung1_source_down_carry_rule():
    """A fresh outage: carry the source's last vintage, keep publishing."""
    d = evaluate_ladder([_src(), _src(name="wmd", available=False, vintage="2026-08-10")])
    assert (d.rung, d.action) == (1, CARRY)
    assert d.publish_print and d.publish_fixing
    wmd = d.status_block()["sources"]["wmd"]
    assert wmd["state"] == CARRY
    assert wmd["vintage"] == "2026-08-10"  # the carried vintage is NAMED
    assert wmd["epochs_carried"] == 1


def test_rung2_stale_flag():
    """Carried past carry_limit: publish with the STALE flag prominent."""
    d = evaluate_ladder([_src(), _src(name="wmd", available=False, carried=2)])
    assert (d.rung, d.action) == (2, STALE)
    assert d.publish_print and d.publish_fixing  # still publishes, flagged
    assert d.status_block()["sources"]["wmd"]["state"] == STALE


def test_rung3_deferred_fixing():
    """Carried past defer_limit: the print appears but THE FIXING DEFERS —
    settling on invented-fresh data is worse than settling late."""
    d = evaluate_ladder([_src(), _src(name="wmd", available=False, carried=4)])
    assert (d.rung, d.action) == (3, DEFER)
    assert d.publish_print  # the status is still published, visibly
    assert not d.publish_fixing
    assert d.status_block()["fixing"] == "DEFERRED"


def test_recovery_resets_the_ladder():
    """The source comes back after a stale stretch: healthy again — the
    ladder is about CURRENT data age, not held grudges."""
    d = evaluate_ladder([_src(), _src(name="wmd", available=True, carried=0)])
    assert d.rung == 0


def test_worst_source_governs():
    """One healthy + one stale + one freshly-down: the worst rung wins."""
    d = evaluate_ladder(
        [
            _src(),
            _src(name="wmd", available=False, carried=3),  # stale (4 <= defer_limit)
            _src(name="gho", available=False, carried=0),  # fresh carry
        ]
    )
    assert (d.rung, d.action) == (2, STALE)
    assert d.status_block()["sources"]["gho"]["state"] == CARRY


def test_ladder_input_discipline():
    with pytest.raises(ValueError, match="at least one source"):
        evaluate_ladder([])
    with pytest.raises(ValueError, match="carry_limit"):
        evaluate_ladder([_src()], carry_limit=3, defer_limit=3)


def test_decision_is_data_not_behavior():
    """The ladder returns a decision object; it performs no IO — the
    runbook's actions attach to it, deterministically testable."""
    d = evaluate_ladder([_src()])
    assert isinstance(d, LadderDecision)
    assert set(d.status_block()) == {"ladder_rung", "action", "fixing", "sources"}
