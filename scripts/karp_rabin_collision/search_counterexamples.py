"""Finite searches for false Karp-Rabin all-length reductions."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from itertools import product
from typing import Iterable

from .fixed_length import CollisionWitness, find_fixed_length_collision
from .oracle import all_length_oracle, collision_lengths, verify_witness


SAVED_COUNTEREXAMPLES: dict[str, dict[str, object]] = {
    "powers_of_two_gap": {
        "S": [0, 1, 0, 1],
        "base": 2,
        "modulus": 3,
        "restricted_lengths": [1, 2, 4],
        "missed_witness": {"length": 3, "i": 0, "j": 1, "hash": 2},
    },
    "restricted_prefix_gap": {
        "S": [0, 1, 0, 1],
        "base": 2,
        "modulus": 3,
        "restricted_lengths": [1, 2],
        "missed_witness": {"length": 3, "i": 0, "j": 1, "hash": 2},
    },
    "minimal_length_structure_gap": {
        "S": [0, 1, 0, 1],
        "base": 2,
        "modulus": 3,
        "restricted_lengths": [1, 2],
        "missed_witness": {"length": 3, "i": 0, "j": 1, "hash": 2},
        "structure_checks": {
            "minimal_collision_length": 3,
            "proper_divisors_checked": [1],
            "halving_lengths_checked": [1, 2],
        },
    },
}


@dataclass(frozen=True)
class SearchOutcome:
    kind: str
    found: bool
    bounds: dict[str, object]
    example: dict[str, object] | None
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "kind": self.kind,
            "found": self.found,
            "bounds": self.bounds,
            "example": self.example,
            "notes": list(self.notes),
        }


def powers_of_two_upto(n: int) -> tuple[int, ...]:
    powers: list[int] = []
    value = 1
    while value <= n:
        powers.append(value)
        value *= 2
    return tuple(powers)


def find_powers_of_two_gap(
    *,
    alphabet_size: int = 2,
    max_n: int = 6,
    base: int | None = None,
    moduli: Iterable[int] = (3, 5, 7),
) -> SearchOutcome:
    """Find an instance clean on power-of-two lengths but colliding elsewhere."""

    resolved_base = alphabet_size if base is None else base
    moduli_tuple = tuple(moduli)
    bounds = _bounds("powers_of_two_gap", alphabet_size, max_n, resolved_base, moduli_tuple)
    for symbols, modulus in _instances(alphabet_size, max_n, moduli_tuple):
        restricted = powers_of_two_upto(len(symbols))
        if _has_collision_in_lengths(symbols, resolved_base, modulus, restricted):
            continue
        missed = _first_collision_outside(symbols, resolved_base, modulus, restricted)
        if missed is not None:
            return SearchOutcome(
                kind="powers_of_two_gap",
                found=True,
                bounds=bounds,
                example=_example(symbols, resolved_base, modulus, restricted, missed),
                notes=(
                    "minimal only in the stated increasing-n, lexicographic search order",
                    "no theorem claim",
                ),
            )
    return _none_found("powers_of_two_gap", bounds)


def find_restricted_length_gap(
    restricted_lengths: Iterable[int],
    *,
    alphabet_size: int = 2,
    max_n: int = 6,
    base: int | None = None,
    moduli: Iterable[int] = (3, 5, 7),
) -> SearchOutcome:
    """Find an instance where a chosen finite length set misses a collision."""

    resolved_base = alphabet_size if base is None else base
    moduli_tuple = tuple(moduli)
    requested = tuple(sorted(set(restricted_lengths)))
    bounds = _bounds(
        "restricted_length_gap",
        alphabet_size,
        max_n,
        resolved_base,
        moduli_tuple,
        restricted_lengths=requested,
    )
    for symbols, modulus in _instances(alphabet_size, max_n, moduli_tuple):
        checked = tuple(length for length in requested if 1 <= length <= len(symbols))
        if _has_collision_in_lengths(symbols, resolved_base, modulus, checked):
            continue
        missed = _first_collision_outside(symbols, resolved_base, modulus, checked)
        if missed is not None:
            return SearchOutcome(
                kind="restricted_length_gap",
                found=True,
                bounds=bounds,
                example=_example(symbols, resolved_base, modulus, checked, missed),
                notes=(
                    "the restricted set is an input to this finite search",
                    "no theorem claim",
                ),
            )
    return _none_found("restricted_length_gap", bounds)


def find_minimal_length_structure_gap(
    *,
    alphabet_size: int = 2,
    max_n: int = 6,
    base: int | None = None,
    moduli: Iterable[int] = (3, 5, 7),
    min_length: int = 3,
) -> SearchOutcome:
    """Find a minimal collision length with no divisor/halving witness below it."""

    resolved_base = alphabet_size if base is None else base
    moduli_tuple = tuple(moduli)
    bounds = _bounds(
        "minimal_length_structure_gap",
        alphabet_size,
        max_n,
        resolved_base,
        moduli_tuple,
        min_length=min_length,
    )
    for symbols, modulus in _instances(alphabet_size, max_n, moduli_tuple):
        result = all_length_oracle(symbols, resolved_base, modulus)
        witness = result.witness
        if witness is None or witness.length < min_length:
            continue
        if _is_power_of_two(witness.length):
            continue
        divisors = tuple(
            length for length in range(1, witness.length) if witness.length % length == 0
        )
        halves = tuple(sorted({witness.length // 2, (witness.length + 1) // 2}))
        check_lengths = tuple(
            length for length in sorted(set(divisors + halves)) if 1 <= length < witness.length
        )
        if _has_collision_in_lengths(symbols, resolved_base, modulus, check_lengths):
            continue
        example = _example(symbols, resolved_base, modulus, check_lengths, witness)
        example["structure_checks"] = {
            "minimal_collision_length": witness.length,
            "proper_divisors_checked": list(divisors),
            "halving_lengths_checked": list(halves),
        }
        return SearchOutcome(
            kind="minimal_length_structure_gap",
            found=True,
            bounds=bounds,
            example=example,
            notes=(
                "minimality is certified by the all-length oracle up to this witness",
                "no theorem claim",
            ),
        )
    return _none_found("minimal_length_structure_gap", bounds)


def run_default_searches(
    *,
    alphabet_size: int = 2,
    max_n: int = 6,
    base: int | None = None,
    moduli: Iterable[int] = (3, 5, 7),
    restricted_lengths: Iterable[int] = (1, 2),
) -> dict[str, SearchOutcome]:
    return {
        "powers_of_two_gap": find_powers_of_two_gap(
            alphabet_size=alphabet_size,
            max_n=max_n,
            base=base,
            moduli=moduli,
        ),
        "restricted_length_gap": find_restricted_length_gap(
            restricted_lengths,
            alphabet_size=alphabet_size,
            max_n=max_n,
            base=base,
            moduli=moduli,
        ),
        "minimal_length_structure_gap": find_minimal_length_structure_gap(
            alphabet_size=alphabet_size,
            max_n=max_n,
            base=base,
            moduli=moduli,
        ),
    }


def validate_saved_counterexamples() -> dict[str, bool]:
    return {
        name: _validate_saved_record(record)
        for name, record in SAVED_COUNTEREXAMPLES.items()
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m scripts.karp_rabin_collision.search_counterexamples"
    )
    parser.add_argument("--alphabet-size", type=int, default=2)
    parser.add_argument("--max-n", type=int, default=6)
    parser.add_argument("--base", type=int, default=None)
    parser.add_argument("--moduli", default="3,5,7")
    parser.add_argument("--restricted-lengths", default="1,2")
    args = parser.parse_args(argv)

    moduli = tuple(_parse_csv_ints(args.moduli))
    restricted_lengths = tuple(_parse_csv_ints(args.restricted_lengths))
    outcomes = run_default_searches(
        alphabet_size=args.alphabet_size,
        max_n=args.max_n,
        base=args.base,
        moduli=moduli,
        restricted_lengths=restricted_lengths,
    )
    print(
        json.dumps(
            {name: outcome.to_dict() for name, outcome in outcomes.items()},
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _instances(
    alphabet_size: int,
    max_n: int,
    moduli: tuple[int, ...],
) -> Iterable[tuple[tuple[int, ...], int]]:
    if alphabet_size < 1:
        raise ValueError("alphabet_size must be positive")
    if max_n < 0:
        raise ValueError("max_n must be nonnegative")
    for n in range(1, max_n + 1):
        for symbols in product(range(alphabet_size), repeat=n):
            for modulus in moduli:
                yield tuple(symbols), modulus


def _has_collision_in_lengths(
    symbols: tuple[int, ...],
    base: int,
    modulus: int,
    lengths: Iterable[int],
) -> bool:
    return any(
        find_fixed_length_collision(symbols, base, modulus, length) is not None
        for length in lengths
        if 1 <= length <= len(symbols)
    )


def _first_collision_outside(
    symbols: tuple[int, ...],
    base: int,
    modulus: int,
    excluded_lengths: Iterable[int],
) -> CollisionWitness | None:
    excluded = set(excluded_lengths)
    for length in range(1, len(symbols) + 1):
        if length in excluded:
            continue
        witness = find_fixed_length_collision(symbols, base, modulus, length)
        if witness is not None:
            return witness
    return None


def _example(
    symbols: tuple[int, ...],
    base: int,
    modulus: int,
    restricted_lengths: Iterable[int],
    witness: CollisionWitness,
) -> dict[str, object]:
    return {
        "S": list(symbols),
        "base": base,
        "modulus": modulus,
        "restricted_lengths": list(restricted_lengths),
        "collision_lengths": list(collision_lengths(symbols, base, modulus)),
        "missed_witness": witness.to_dict(),
    }


def _bounds(
    kind: str,
    alphabet_size: int,
    max_n: int,
    base: int,
    moduli: tuple[int, ...],
    **extra: object,
) -> dict[str, object]:
    bounds: dict[str, object] = {
        "kind": kind,
        "alphabet_size": alphabet_size,
        "max_n": max_n,
        "base": base,
        "moduli": list(moduli),
        "string_order": "increasing n, lexicographic symbols, listed modulus order",
    }
    bounds.update(extra)
    return bounds


def _none_found(kind: str, bounds: dict[str, object]) -> SearchOutcome:
    return SearchOutcome(
        kind=kind,
        found=False,
        bounds=bounds,
        example=None,
        notes=("none found within the finite bounds above", "no theorem claim"),
    )


def _validate_saved_record(record: dict[str, object]) -> bool:
    symbols = tuple(record["S"])  # type: ignore[arg-type]
    base = int(record["base"])
    modulus = int(record["modulus"])
    raw = record["missed_witness"]  # type: ignore[assignment]
    if not isinstance(raw, dict):
        return False
    witness = CollisionWitness(
        length=int(raw["length"]),
        i=int(raw["i"]),
        j=int(raw["j"]),
        hash_value=int(raw["hash"]),
    )
    if not verify_witness(symbols, base, modulus, witness):
        return False
    restricted = tuple(int(length) for length in record["restricted_lengths"])  # type: ignore[arg-type]
    return not _has_collision_in_lengths(symbols, base, modulus, restricted)


def _parse_csv_ints(value: str) -> tuple[int, ...]:
    if not value.strip():
        return ()
    return tuple(int(part.strip()) for part in value.split(","))


def _is_power_of_two(value: int) -> bool:
    return value > 0 and value & (value - 1) == 0


if __name__ == "__main__":
    raise SystemExit(main())
