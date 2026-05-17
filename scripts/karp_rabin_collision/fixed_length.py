"""Fixed-length exact Karp-Rabin collision detector.

The routines here are deliberately finite and exact.  Fingerprints are used
only to form candidate buckets; true substring inequality is checked directly
before any witness is returned.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Sequence


StringInput = Sequence[int] | str


@dataclass(frozen=True, order=True)
class CollisionWitness:
    """A checkable same-length false fingerprint equality."""

    length: int
    i: int
    j: int
    hash_value: int

    def as_tuple(self) -> tuple[int, int, int]:
        return (self.length, self.i, self.j)

    def to_dict(self) -> dict[str, int]:
        return {
            "length": self.length,
            "i": self.i,
            "j": self.j,
            "hash": self.hash_value,
        }


@dataclass(frozen=True)
class FixedLengthScan:
    """Audit information for one fixed-length scan."""

    length: int
    checked_same_hash_pairs: int
    bucket_count: int
    max_bucket_size: int
    witness: CollisionWitness | None

    @property
    def has_collision(self) -> bool:
        return self.witness is not None

    def to_dict(self) -> dict[str, object]:
        return {
            "length": self.length,
            "has_collision": self.has_collision,
            "witness": None if self.witness is None else self.witness.to_dict(),
            "checked_same_hash_pairs": self.checked_same_hash_pairs,
            "bucket_count": self.bucket_count,
            "max_bucket_size": self.max_bucket_size,
        }


def normalize_symbols(value: StringInput) -> tuple[int, ...]:
    """Normalize an integer string or ASCII string to integer symbols."""

    if isinstance(value, str):
        try:
            value.encode("ascii")
        except UnicodeEncodeError as exc:
            raise ValueError("S must be ASCII when provided as a str") from exc
        return tuple(ord(character) for character in value)

    symbols: list[int] = []
    try:
        iterator = iter(value)
    except TypeError as exc:
        raise ValueError("S must be an integer sequence or ASCII str") from exc

    for index, symbol in enumerate(iterator):
        if isinstance(symbol, bool) or not isinstance(symbol, int):
            raise ValueError(f"S[{index}] must be an integer symbol")
        if symbol < 0:
            raise ValueError(f"S[{index}] must be nonnegative")
        symbols.append(symbol)
    return tuple(symbols)


def validate_base_modulus(base: int, modulus: int) -> None:
    if isinstance(base, bool) or not isinstance(base, int):
        raise ValueError("base must be an integer")
    if base < 1:
        raise ValueError("base must be positive")
    if isinstance(modulus, bool) or not isinstance(modulus, int):
        raise ValueError("modulus must be an integer")
    if not is_prime(modulus):
        raise ValueError("modulus must be prime")


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value == 2:
        return True
    if value % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def prefix_hashes(
    value: StringInput,
    base: int,
    modulus: int,
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    """Return normalized symbols, prefix hashes, and powers of ``base`` mod p."""

    symbols = normalize_symbols(value)
    validate_base_modulus(base, modulus)
    prefix = [0] * (len(symbols) + 1)
    powers = [1] * (len(symbols) + 1)
    base_mod = base % modulus
    for index, symbol in enumerate(symbols):
        prefix[index + 1] = (prefix[index] * base_mod + symbol) % modulus
        powers[index + 1] = (powers[index] * base_mod) % modulus
    return symbols, tuple(prefix), tuple(powers)


def substring_hash(
    prefix: Sequence[int],
    powers: Sequence[int],
    start: int,
    length: int,
    modulus: int,
) -> int:
    return (prefix[start + length] - prefix[start] * powers[length]) % modulus


def fixed_length_hashes(
    value: StringInput,
    base: int,
    modulus: int,
    length: int,
) -> tuple[int, ...]:
    symbols, prefix, powers = prefix_hashes(value, base, modulus)
    _validate_length(length, len(symbols))
    return tuple(
        substring_hash(prefix, powers, start, length, modulus)
        for start in range(len(symbols) - length + 1)
    )


def scan_fixed_length(
    value: StringInput,
    base: int,
    modulus: int,
    length: int,
) -> FixedLengthScan:
    """Group one length by fingerprint and return the first real collision."""

    symbols, prefix, powers = prefix_hashes(value, base, modulus)
    return scan_fixed_length_precomputed(symbols, prefix, powers, modulus, length)


def scan_fixed_length_precomputed(
    symbols: Sequence[int],
    prefix: Sequence[int],
    powers: Sequence[int],
    modulus: int,
    length: int,
) -> FixedLengthScan:
    """Fixed-length scan using already computed prefix hashes and powers."""

    symbols = tuple(symbols)
    _validate_length(length, len(symbols))
    hashes = tuple(
        substring_hash(prefix, powers, start, length, modulus)
        for start in range(len(symbols) - length + 1)
    )
    buckets: dict[int, list[int]] = defaultdict(list)
    for start, hash_value in enumerate(hashes):
        buckets[hash_value].append(start)

    max_bucket_size = max((len(starts) for starts in buckets.values()), default=0)
    checked_same_hash_pairs = 0
    for i, hash_value in enumerate(hashes):
        left = symbols[i : i + length]
        for j in buckets[hash_value]:
            if j <= i:
                continue
            checked_same_hash_pairs += 1
            if left != symbols[j : j + length]:
                return FixedLengthScan(
                    length=length,
                    checked_same_hash_pairs=checked_same_hash_pairs,
                    bucket_count=len(buckets),
                    max_bucket_size=max_bucket_size,
                    witness=CollisionWitness(length, i, j, hash_value),
                )

    return FixedLengthScan(
        length=length,
        checked_same_hash_pairs=checked_same_hash_pairs,
        bucket_count=len(buckets),
        max_bucket_size=max_bucket_size,
        witness=None,
    )


def find_fixed_length_collision(
    value: StringInput,
    base: int,
    modulus: int,
    length: int,
) -> CollisionWitness | None:
    return scan_fixed_length(value, base, modulus, length).witness


def brute_force_fixed_length_collision(
    value: StringInput,
    base: int,
    modulus: int,
    length: int,
) -> CollisionWitness | None:
    """Independent direct pair enumeration for tests and audits."""

    symbols = normalize_symbols(value)
    validate_base_modulus(base, modulus)
    _validate_length(length, len(symbols))
    for i in range(len(symbols) - length + 1):
        left = symbols[i : i + length]
        left_hash = naive_substring_hash(symbols, base, modulus, i, length)
        for j in range(i + 1, len(symbols) - length + 1):
            right_hash = naive_substring_hash(symbols, base, modulus, j, length)
            if left_hash == right_hash and left != symbols[j : j + length]:
                return CollisionWitness(length, i, j, left_hash)
    return None


def naive_substring_hash(
    symbols: Sequence[int],
    base: int,
    modulus: int,
    start: int,
    length: int,
) -> int:
    value = 0
    for symbol in symbols[start : start + length]:
        value = (value * base + symbol) % modulus
    return value


def _validate_length(length: int, n: int) -> None:
    if isinstance(length, bool) or not isinstance(length, int):
        raise ValueError("length must be an integer")
    if length < 1:
        raise ValueError("length zero is excluded")
    if length > n:
        raise ValueError("length must be at most len(S)")
