"""Exact rational parsing and normalization."""

from __future__ import annotations

from fractions import Fraction
import re
from typing import Any


_RATIONAL_RE = re.compile(r"^-?(0|[1-9][0-9]*)(/([1-9][0-9]*))?$")


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def parse_rational(value: Any, field: str = "value") -> Fraction:
    """Parse an exact rational value.

    Accepted forms are integers, strings like ``"3"`` or ``"-2/5"``, and
    objects ``{"num": int, "den": int}``. Floats are deliberately rejected.
    """

    if isinstance(value, float):
        raise ValueError(f"{field}: floats are not exact rationals")

    if _is_int(value):
        return Fraction(value, 1)

    if isinstance(value, str):
        text = value.strip()
        match = _RATIONAL_RE.match(text)
        if not match:
            raise ValueError(f"{field}: invalid rational string {value!r}")
        if "/" in text:
            num_text, den_text = text.split("/", 1)
            return Fraction(int(num_text), int(den_text))
        return Fraction(int(text), 1)

    if isinstance(value, dict):
        if set(value.keys()) != {"num", "den"}:
            raise ValueError(f"{field}: rational object must have num and den")
        num = value["num"]
        den = value["den"]
        if not _is_int(num) or not _is_int(den):
            raise ValueError(f"{field}: rational object num and den must be integers")
        if den <= 0:
            raise ValueError(f"{field}: rational denominator must be positive")
        return Fraction(num, den)

    raise ValueError(f"{field}: unsupported rational value {value!r}")


def rational_to_string(value: Fraction) -> str:
    """Return a reduced rational as ``a`` or ``a/b``."""

    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def rational_to_object(value: Fraction) -> dict[str, int]:
    """Return a reduced rational JSON object."""

    return {"num": value.numerator, "den": value.denominator}

