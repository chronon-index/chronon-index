"""B-uc4-01 / AC-4.6: accuracy statement + interval-or-convention mandatory.

RP Part VI rule 6 as schema: a published S must carry an accuracy block —
either a Decimal interval that actually brackets the value, or an explicit
convention label with a reason.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

from tly.prints import PrintSchemaError, validate_accuracy

D = Decimal
S = D("362412641743.4670")


def test_interval_accuracy_valid():
    validate_accuracy(
        {
            "statement": "S with the RP VIII deterministic budget",
            "uncertainty": {
                "type": "interval",
                "lower": str(S * D("0.98")),
                "upper": str(S * D("1.02")),
            },
        },
        S,
    )


def test_convention_accuracy_valid():
    validate_accuracy(
        {
            "statement": "S, convention-labeled",
            "uncertainty": {"type": "convention", "note": "budget module pending D-03"},
        },
        S,
    )


def test_missing_statement_fails():
    with pytest.raises(PrintSchemaError, match="statement is required"):
        validate_accuracy({"statement": " ", "uncertainty": {"type": "convention", "note": "x"}}, S)


def test_unknown_uncertainty_type_fails():
    with pytest.raises(PrintSchemaError, match="uncertainty.type"):
        validate_accuracy({"statement": "s", "uncertainty": {"type": "approximately"}}, S)


def test_interval_must_bracket_the_published_value():
    with pytest.raises(PrintSchemaError, match="outside its own interval"):
        validate_accuracy(
            {
                "statement": "s",
                "uncertainty": {"type": "interval", "lower": "1", "upper": "2"},
            },
            S,
        )
    with pytest.raises(PrintSchemaError, match="interval inverted"):
        validate_accuracy(
            {
                "statement": "s",
                "uncertainty": {"type": "interval", "lower": "5", "upper": "2"},
            },
            D("3"),
        )


def test_convention_without_reason_fails():
    """The label alone is not honesty — the WHY is mandatory."""
    with pytest.raises(PrintSchemaError, match="must say why"):
        validate_accuracy({"statement": "s", "uncertainty": {"type": "convention", "note": ""}}, S)


def test_pipeline_print_carries_module_produced_interval():
    """B-uc2-09: since D-03, the live pipeline embeds the module-produced
    budget — a real interval, no hand-typed text (the pre-D-03 convention
    label is retired)."""
    from tly.error_budget import accuracy_block
    from tly.pipeline import build_settlement_print

    p = build_settlement_print("2026-08-17T12:00:00+00:00")
    assert p.accuracy == accuracy_block(p.s_life_years)  # byte-equal: module-produced
    assert p.accuracy["uncertainty"]["type"] == "interval"
    assert p.accuracy["produced_by"] == "tly.error_budget.accuracy_block"
