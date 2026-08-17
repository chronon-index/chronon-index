"""C-uc6-02 / AC-6.5: test_simulation_isolation (named) — three walls
between what-if and what-is."""

from __future__ import annotations

import json
from decimal import Decimal

import pytest

from tly.archive import ArchiveImmutabilityError, PrintArchive
from tly.prints import PrintSchemaError, WeeklyPrint
from tly.scenarios import SIMULATION_LABEL, Scenario, run_scenario

D = Decimal
S0 = D("362412641743.4670")

SCENARIO = Scenario(
    name="isolation-check",
    seed=1,
    initial_s=S0,
    epochs=5,
    weekly_growth=D("1.000138"),
)


def test_simulation_isolation(tmp_path):
    """Named per AC-6.5. Wall 1: every rendered lab output carries the
    SIMULATION label. Wall 2: print storage type-rejects lab objects.
    Wall 3: SIMULATION is not a constructible print label, so a simulation
    cannot even be disguised as a print."""
    result = run_scenario(SCENARIO)
    rendered = json.loads(result.render())
    assert rendered["series_label"] == SIMULATION_LABEL  # wall 1

    archive = PrintArchive(tmp_path)
    with pytest.raises(ArchiveImmutabilityError, match="simulations stay in the lab"):
        archive.append(result)  # type: ignore[arg-type]  # wall 2
    assert archive.head_hash == "0" * 64  # nothing was written
    assert list(tmp_path.glob("*.json")) == []

    with pytest.raises(PrintSchemaError, match="series_label"):  # wall 3
        WeeklyPrint(
            epoch_utc="2026-08-17T12:00:00+00:00",
            series_label=SIMULATION_LABEL,
            s_life_years=S0,
            e_bar_years=D("44.7880"),
            n_persons=D("8091734933"),
            burn_life_years=D("0"),
            coverage={"measured_share": D("1")},
            accuracy={
                "statement": "x",
                "uncertainty": {"type": "convention", "note": "x"},
            },
            provenance={"methodology_version": "v", "snapshots": {"s": {}}},
        )


def test_every_lab_render_is_labeled():
    """The label is emitted by render() itself, not by callers — no lab
    output path can forget it."""
    for seed in (1, 2, 3):
        s = Scenario(name=f"s{seed}", seed=seed, initial_s=S0, epochs=2, weekly_growth=D("1.0001"))
        assert json.loads(run_scenario(s).render())["series_label"] == SIMULATION_LABEL
