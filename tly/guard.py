"""Float quarantine (SPEC#1 AC-1.3; SPEC#0 G1).

Published-path code must be Decimal end to end. Python already refuses
mixed Decimal/float arithmetic, but two leaks remain: an all-float pipeline
never touches a Decimal and so never trips, and ``Decimal(0.1)`` silently
launders binary error into a Decimal. This module closes both: every
published-path entry point calls :func:`assert_no_floats` on its inputs, so
a float anywhere in the structure raises before any arithmetic happens.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Mapping, Sequence
from decimal import Decimal


class FloatContaminationError(TypeError):
    """A float reached a published-value code path."""


def assert_no_floats(obj: object, path: str = "$") -> None:
    """Recursively reject floats in scalars, mappings, sequences, dataclasses.

    ``path`` names the offending location in the raised error so a failure
    inside a nested structure is diagnosable.
    """
    if isinstance(obj, float):
        raise FloatContaminationError(
            f"float at {path}: {obj!r} — published paths are Decimal-only (G1)"
        )
    if isinstance(obj, (str, bytes, bool, int, Decimal)) or obj is None:
        return
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        for f in dataclasses.fields(obj):
            assert_no_floats(getattr(obj, f.name), f"{path}.{f.name}")
        return
    if isinstance(obj, Mapping):
        for k, v in obj.items():
            assert_no_floats(k, f"{path}[key {k!r}]")
            assert_no_floats(v, f"{path}[{k!r}]")
        return
    if isinstance(obj, Sequence):
        for i, v in enumerate(obj):
            assert_no_floats(v, f"{path}[{i}]")
        return
    if isinstance(obj, (set, frozenset)):
        for v in obj:
            assert_no_floats(v, f"{path}{{...}}")
        return
    # Unknown container-ish objects: reject rather than silently pass a
    # structure we cannot inspect (fail closed on the published path).
    raise FloatContaminationError(f"uninspectable object at {path}: {type(obj).__name__}")


def assert_decimal(value: object, name: str) -> Decimal:
    """Require an actual Decimal (bool/int/float all rejected). Returns it."""
    if not isinstance(value, Decimal):
        raise FloatContaminationError(
            f"{name} must be Decimal, got {type(value).__name__}: {value!r}"
        )
    return value
