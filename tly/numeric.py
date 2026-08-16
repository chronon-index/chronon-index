"""Numeric standards (SPEC#0 G1; RALPH_LOOP §6; RP Part I M5).

Decimal precision 34, ROUND_HALF_EVEN, for everything supply- or
index-adjacent. Floats never touch published numbers: parse JSON with
``parse_float=decimal.Decimal`` and CSV cells with ``Decimal(str)`` so no
value ever transits a float. Importing this module configures the process
default context; call :func:`configure` explicitly in long-lived processes
that may have altered it.
"""

from __future__ import annotations

from decimal import ROUND_HALF_EVEN, Decimal, getcontext

PRECISION = 34
ROUNDING = ROUND_HALF_EVEN

BILLION = Decimal(10) ** 9
Q4 = Decimal("0.0001")  # published 4-dp quantum


def configure() -> None:
    """Set the process-default Decimal context to the project standard."""
    ctx = getcontext()
    ctx.prec = PRECISION
    ctx.rounding = ROUNDING


configure()
