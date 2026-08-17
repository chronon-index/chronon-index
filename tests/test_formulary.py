"""D-05: the formulary cross-reference — E1-E12 mapped to real homes."""

from __future__ import annotations

import importlib
import inspect

from tly.formulary import FORMULARY, implemented, pending


def test_formulary_is_complete_e1_to_e12():
    assert [e.number for e in FORMULARY] == [f"E{i}" for i in range(1, 13)]
    assert all(e.statement.strip() for e in FORMULARY)


def test_every_home_imports_and_cites_its_equation():
    """The cross-reference: each implemented equation's home module exists
    AND its source mentions the equation number — the code knows which
    equation it embodies."""
    for eq in implemented():
        module = importlib.import_module(eq.home)
        source = inspect.getsource(module)
        assert eq.number in source, f"{eq.home} never mentions {eq.number}"


def test_pending_entries_name_their_phase():
    """Unimplemented equations are honest: each names the phase/task that
    delivers it, and none quietly claims a home."""
    pend = pending()
    assert {e.number for e in pend} == {"E3", "E6", "E7"}
    for e in pend:
        assert e.pending and any(marker in e.pending for marker in ("P2", "METHODOLOGY")), e.number


def test_no_orphan_equation_homes():
    """Every home is inside the tly package — the formulary maps to THIS
    codebase, not to aspirations."""
    for eq in implemented():
        assert eq.home.startswith("tly."), eq.number
