"""Golden tests for the reconstructed v0 calculator.

Reconstructed 2026-08-16 from DECISIONS.md, RESEARCH_PROGRAM.md and
RALPH_LOOP.md after loss of the original; pending Ben's review.

test_offline_recompute_is_byte_exact is invariant P5 (reproducibility):
identical snapshot hashes -> byte-identical outputs.
"""

import importlib.util
import json
from decimal import Decimal
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CALC_PATH = REPO_ROOT / "seed" / "tly_v0_calc.py"
RESULTS_PATH = REPO_ROOT / "seed" / "results_v0.json"
SNAPSHOT_DIR = REPO_ROOT / "data" / "snapshots" / "2026-08-16"


def _load_calc_module():
    spec = importlib.util.spec_from_file_location("tly_v0_calc", CALC_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_offline_recompute_is_byte_exact():
    """P5: recomputing from the committed snapshot reproduces results_v0.json
    byte for byte."""
    calc = _load_calc_module()
    snapshot = calc.load_snapshot(SNAPSHOT_DIR)
    rendered = calc.render_json(calc.compute(snapshot)).encode("utf-8")
    committed = RESULTS_PATH.read_bytes()
    assert rendered == committed, (
        "offline recompute from the committed snapshot does not byte-match seed/results_v0.json"
    )


def test_ebar_times_n_equals_s():
    """Consistency: E-bar * N == S (2019 table) within Decimal-34 round-off,
    and spend == -N exactly."""
    results = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    a = results["achieved"]
    s = Decimal(a["S_2019_life_years"])
    n = Decimal(a["N_persons"])
    e_bar = Decimal(a["E_bar_years_full"])
    # E-bar was produced by the prec-34 division S/N; multiplying back cannot
    # be bit-exact in general, so assert agreement to 1e-30 relative — far
    # beyond any published precision (published values are quantized to 4 dp).
    rel = abs(e_bar * n - s) / s
    assert rel < Decimal("1e-30"), f"E-bar*N deviates from S by {rel} relative"
    assert Decimal(a["spend_minus_N_life_years"]) == -n
