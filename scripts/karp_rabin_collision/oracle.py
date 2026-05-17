"""Exact all-length oracle for fixed-prime Karp-Rabin collisions."""

from __future__ import annotations

from dataclasses import dataclass

from .fixed_length import (
    CollisionWitness,
    StringInput,
    brute_force_fixed_length_collision,
    naive_substring_hash,
    normalize_symbols,
    prefix_hashes,
    scan_fixed_length_precomputed,
    validate_base_modulus,
)


@dataclass(frozen=True)
class OracleResult:
    """Result object matching the finite oracle spec."""

    has_collision: bool
    witness: CollisionWitness | None
    checked_lengths: int
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "has_collision": self.has_collision,
            "witness": None if self.witness is None else self.witness.to_dict(),
            "checked_lengths": self.checked_lengths,
            "notes": list(self.notes),
        }


def all_length_oracle(value: StringInput, base: int, modulus: int) -> OracleResult:
    """Return the first all-length collision witness, if one exists.

    Lengths are checked in increasing order, and starts are checked
    lexicographically within a fixed length.  ``checked_lengths`` records the
    number of lengths inspected before returning; for a no instance this is
    exactly ``len(S)``.
    """

    symbols, prefix, powers = prefix_hashes(value, base, modulus)
    if not symbols:
        return OracleResult(
            has_collision=False,
            witness=None,
            checked_lengths=0,
            notes=("empty string has no positive lengths",),
        )

    for length in range(1, len(symbols) + 1):
        scan = scan_fixed_length_precomputed(symbols, prefix, powers, modulus, length)
        if scan.witness is not None:
            return OracleResult(True, scan.witness, length)
    return OracleResult(False, None, len(symbols))


def find_collision(
    value: StringInput,
    base: int,
    modulus: int,
) -> CollisionWitness | None:
    return all_length_oracle(value, base, modulus).witness


def brute_force_oracle(value: StringInput, base: int, modulus: int) -> OracleResult:
    """Independent all-length pair enumeration for tests."""

    symbols = normalize_symbols(value)
    validate_base_modulus(base, modulus)
    if not symbols:
        return OracleResult(
            has_collision=False,
            witness=None,
            checked_lengths=0,
            notes=("empty string has no positive lengths",),
        )
    for length in range(1, len(symbols) + 1):
        witness = brute_force_fixed_length_collision(symbols, base, modulus, length)
        if witness is not None:
            return OracleResult(True, witness, length)
    return OracleResult(False, None, len(symbols))


def verify_witness(
    value: StringInput,
    base: int,
    modulus: int,
    witness: CollisionWitness,
) -> bool:
    """Check witness bounds, hash equality, and true substring inequality."""

    symbols = normalize_symbols(value)
    validate_base_modulus(base, modulus)
    length = witness.length
    if length < 1:
        return False
    if witness.i == witness.j:
        return False
    if witness.i < 0 or witness.j < 0:
        return False
    if witness.i > len(symbols) - length or witness.j > len(symbols) - length:
        return False
    left = symbols[witness.i : witness.i + length]
    right = symbols[witness.j : witness.j + length]
    if left == right:
        return False
    left_hash = naive_substring_hash(symbols, base, modulus, witness.i, length)
    right_hash = naive_substring_hash(symbols, base, modulus, witness.j, length)
    return left_hash == right_hash == witness.hash_value


def collision_lengths(value: StringInput, base: int, modulus: int) -> tuple[int, ...]:
    """Return every length at which at least one real collision exists."""

    symbols, prefix, powers = prefix_hashes(value, base, modulus)
    lengths: list[int] = []
    for length in range(1, len(symbols) + 1):
        scan = scan_fixed_length_precomputed(symbols, prefix, powers, modulus, length)
        if scan.witness is not None:
            lengths.append(length)
    return tuple(lengths)
