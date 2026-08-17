"""Status / stale-print failure ladder (SPEC#4 AC-4.5; RP Part XII; E-04).

The Monday print's response to upstream failure is a LADDER, not a switch:

- rung 0 — HEALTHY: all sources fresh; normal print.
- rung 1 — CARRY: a source is down this epoch; carry its last vintage
  forward, name the carried vintage in the status block, publish. The
  carry rule keeps a transient outage from silencing the index.
- rung 2 — STALE: a source has been carried beyond ``carry_limit``
  consecutive epochs; the print still publishes but carries the STALE
  flag prominently — consumers see exactly which input has gone quiet.
- rung 3 — DEFER: carried beyond ``defer_limit``: publishing a settlement
  fixing on data this old would be invention, so THE FIXING IS DEFERRED —
  a DEFERRED record is published in its place (visible, dated), and the
  next epoch tries again. Deferral never blocks the next epoch's attempt
  (the same non-blocking philosophy as the dispute window).

The ladder is pure decision logic — no clocks, no network; epochs_carried
is supplied by the caller's bookkeeping, so every rung is unit-testable.
"""

from __future__ import annotations

from dataclasses import dataclass

HEALTHY = "HEALTHY"
CARRY = "CARRY"
STALE = "STALE"
DEFER = "DEFER"

CARRY_LIMIT = 2  # epochs a source may be carried before the STALE flag
DEFER_LIMIT = 4  # epochs carried after which the fixing defers


@dataclass(frozen=True)
class SourceState:
    name: str
    available: bool  # did this epoch's fetch succeed?
    last_vintage: str  # vintage date the freshest data comes from
    epochs_carried: int  # consecutive epochs carried BEFORE this one


@dataclass(frozen=True)
class LadderDecision:
    rung: int
    action: str  # HEALTHY | CARRY | STALE | DEFER
    publish_print: bool
    publish_fixing: bool
    source_status: dict[str, dict]

    def status_block(self) -> dict:
        """The print's status block — what consumers see."""
        return {
            "ladder_rung": self.rung,
            "action": self.action,
            "fixing": "published" if self.publish_fixing else "DEFERRED",
            "sources": self.source_status,
        }


def evaluate_ladder(
    states: list[SourceState],
    carry_limit: int = CARRY_LIMIT,
    defer_limit: int = DEFER_LIMIT,
) -> LadderDecision:
    if not states:
        raise ValueError("a print has at least one source")
    if not 0 < carry_limit < defer_limit:
        raise ValueError("need 0 < carry_limit < defer_limit")

    source_status: dict[str, dict] = {}
    worst_carried = 0
    for s in states:
        carried_now = s.epochs_carried + (0 if s.available else 1)
        entry: dict = {"vintage": s.last_vintage}
        if s.available and s.epochs_carried == 0:
            entry["state"] = HEALTHY
        elif carried_now <= carry_limit:
            entry["state"] = CARRY
            entry["epochs_carried"] = carried_now
        elif carried_now <= defer_limit:
            entry["state"] = STALE
            entry["epochs_carried"] = carried_now
        else:
            entry["state"] = DEFER
            entry["epochs_carried"] = carried_now
        source_status[s.name] = entry
        if not s.available or s.epochs_carried > 0:
            worst_carried = max(worst_carried, carried_now)

    if worst_carried == 0:
        return LadderDecision(0, HEALTHY, True, True, source_status)
    if worst_carried <= carry_limit:
        return LadderDecision(1, CARRY, True, True, source_status)
    if worst_carried <= defer_limit:
        return LadderDecision(2, STALE, True, True, source_status)
    return LadderDecision(3, DEFER, True, False, source_status)
