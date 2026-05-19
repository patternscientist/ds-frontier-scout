"""Verify the DS(k,1) v5 leaf-local cap certificate.

This script checks:
1. The corrected min-choice fan generators for g1,g2,g3.
2. The primitive-ray/four-cap Farkas identities in Frontier Note v5.

It is intentionally small and dependency-light; it uses sympy only for exact expansion.
"""
from __future__ import annotations

import itertools
from math import gcd
from typing import Iterable

import sympy as sp

beta, gamma, u = sp.symbols("beta gamma u")
B, s, R, y, x, b0, X, r0 = sp.symbols("B s R y x b0 X r0")

h1 = x + b0 - s
h2 = X + r0 - R
h3 = x + b0 - y
h4 = X + r0 - x - b0 + B
h5 = X + r0 - B - R + b0
h6 = y - x
h7 = x - X
h8 = X + r0 - x

NS = dict(
    B=B, s=s, R=R, y=y, x=x, b0=b0, X=X, r0=r0,
    h1=h1, h2=h2, h3=h3, h4=h4, h5=h5, h6=h6, h7=h7, h8=h8,
)

RAYS = {
    "e_beta": (1, 0, 0),
    "e_gamma": (0, 1, 0),
    "e_u": (0, 0, 1),
    "p": (1, 1, 1),
    "q": (0, 1, 1),
    "r": (1, 0, 1),
    "t": (2, 0, 1),
}

CERT_TABLE = {
    "e_beta": ["x", "x", "(s-b0)+h3", "(s-b0)+h3"],
    "e_gamma": ["X", "X", "X", "h3+(R-r0)+h4"],
    "e_u": ["2*h6+h1+h7+h2", "h6+h7+h5", "h6+h7+h5", "b0+r0"],
    "p": ["h1+h2", "h1+h2", "h3+h2", "2*h3+h4"],
    "q": ["h6+h1+h2", "h5", "h5", "h3+h8"],
    "r": ["h6+h1+h7+h2", "h7+h5", "h7+h5", "r0+h3"],
    "t": ["h1+h7+h2", "h1+h7+h2", "h3+h7+h2", "2*h3+h7+h4"],
}

EXPECTED_FAN = {
    ("0", "0", "0"): {"e_gamma", "e_beta", "p"},
    ("0", "0", "gamma-u"): {"e_beta", "t", "p"},
    ("0", "beta-u", "0"): {"e_gamma", "q", "p"},
    ("0", "beta-u", "gamma-u"): {"q", "p"},
    ("0", "L-2u", "0"): {"q", "p"},
    ("0", "L-2u", "gamma-u"): {"q", "r", "t", "p"},
    ("L-u", "beta-u", "0"): {"q"},
    ("L-u", "beta-u", "gamma-u"): {"q"},
    ("L-u", "L-2u", "0"): {"q"},
    ("L-u", "L-2u", "gamma-u"): {"e_u", "q", "r"},
}


def min_exprs(be: int, ga: int, uu: int) -> tuple[int, int, int]:
    L = be + ga
    mB = min(0, L - uu)
    ms = min(0, be - uu, L - 2 * uu)
    mR = min(0, ga - uu)
    return (mB - ms, be + mR - mB, L - (be + mR))


def phi(be: int, ga: int, uu: int, region: int) -> sp.Expr:
    L = be + ga
    g1, g2, g3 = min_exprs(be, ga, uu)
    base = be * x + ga * X + uu * (b0 + r0 - s - R) - L * y
    if region == 0:
        return sp.expand(base + (g1 + g2 + g3) * y)
    if region == 1:
        return sp.expand(base + g1 * (s - B) + (g2 + g3) * y)
    if region == 2:
        return sp.expand(base + g1 * (s - B) + g2 * s + g3 * y)
    if region == 3:
        return sp.expand(base + g1 * (s - B) + g2 * s + g3 * (R + B))
    raise ValueError(region)


def normalize(v: Iterable[int]) -> tuple[int, int, int]:
    vals = [int(a) for a in v]
    g = 0
    for a in vals:
        g = gcd(g, abs(a))
    vals = [a // g for a in vals]
    for a in vals:
        if a:
            if a < 0:
                vals = [-b for b in vals]
            break
    return tuple(vals)  # type: ignore[return-value]


def cross(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def dot(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    return sum(i * j for i, j in zip(a, b))


def inequalities(choice: tuple[str, str, str]) -> list[tuple[int, int, int]]:
    mB, ms, mR = choice
    rows = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    rows.append((1, 1, -1) if mB == "0" else (-1, -1, 1))
    if ms == "0":
        rows += [(1, 0, -1), (1, 1, -2)]
    elif ms == "beta-u":
        rows += [(-1, 0, 1), (0, 1, -1)]
    elif ms == "L-2u":
        rows += [(-1, -1, 2), (0, -1, 1)]
    else:
        raise ValueError(ms)
    rows.append((0, 1, -1) if mR == "0" else (0, -1, 1))
    return rows


def cone_rays(choice: tuple[str, str, str]) -> set[str]:
    rows = inequalities(choice)
    found: set[tuple[int, int, int]] = set()
    for a, b in itertools.combinations(rows, 2):
        c = cross(a, b)
        for v in (c, tuple(-z for z in c)):
            if v == (0, 0, 0):
                continue
            if all(dot(row, v) >= 0 for row in rows):
                found.add(normalize(v))
    reverse = {v: k for k, v in RAYS.items()}
    return {reverse[v] for v in found if v in reverse}


def check_fan() -> None:
    actual = {}
    for choice in itertools.product(("0", "L-u"), ("0", "beta-u", "L-2u"), ("0", "gamma-u")):
        rays = cone_rays(choice)
        if rays:
            actual[choice] = rays
    assert actual == EXPECTED_FAN, f"fan mismatch\nactual={actual}\nexpected={EXPECTED_FAN}"


def check_certificates() -> None:
    for ray_name, (be, ga, uu) in RAYS.items():
        for region, rhs_text in enumerate(CERT_TABLE[ray_name]):
            lhs = phi(be, ga, uu, region)
            rhs = eval(rhs_text, {}, NS)
            diff = sp.expand(lhs - rhs)
            assert diff == 0, (ray_name, region, lhs, rhs, diff)


def main() -> None:
    check_fan()
    check_certificates()
    print("ok: corrected fan and primitive-ray certificates verified")


if __name__ == "__main__":
    main()
