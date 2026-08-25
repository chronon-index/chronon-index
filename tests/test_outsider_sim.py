"""C-uc7-07: the outsider simulation, guarded by the suite."""

from __future__ import annotations

from tly.outsider_sim import main


def test_outsider_sim_passes_on_the_real_archive():
    """Every archived epoch must reproduce (values exact, stamp
    history-consistent, citations resolving) — run in-process exactly as
    the CI job runs it."""
    assert main() == 0
