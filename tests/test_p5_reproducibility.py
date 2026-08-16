"""B-uc3-03 / AC-3.1 / invariant P5: identical snapshots → byte-identical output.

The named test runs the full pipeline twice in-process AND twice as fully
separate OS processes with different PYTHONHASHSEED values — so hash
randomization, import order, and any hidden nondeterminism would surface
as a byte diff.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from tly.pipeline import build_settlement_print
from tly.prints import validate_print_dict

REPO = Path(__file__).resolve().parent.parent
EPOCH = "2026-08-17T12:00:00+00:00"


def test_p5_reproducibility():
    """Named per RP Part X. In-process: two builds render byte-identically
    and validate against the print schema."""
    a = build_settlement_print(EPOCH).render()
    b = build_settlement_print(EPOCH).render()
    assert a == b
    validate_print_dict(build_settlement_print(EPOCH).to_json_dict())
    assert '"series_label": "SETTLEMENT"' in a


def _run_pipeline(hashseed: str) -> bytes:
    env = dict(os.environ, PYTHONHASHSEED=hashseed)
    proc = subprocess.run(
        [sys.executable, "-m", "tly.pipeline", EPOCH],
        cwd=REPO,
        env=env,
        capture_output=True,
        check=True,
    )
    return proc.stdout


def test_p5_reproducibility_across_processes():
    """Two cold processes, different hash seeds, byte-identical stdout."""
    out_a = _run_pipeline("0")
    out_b = _run_pipeline("42")
    assert out_a == out_b
    assert out_a.startswith(b"{")
