"""Fixed-shift exact Karp-Rabin collision explorer.

This module studies pairs of equal-length substrings whose starts differ by a
fixed positive offset ``d``.  It is finite proof-scouting infrastructure only:
fingerprints identify zero events, and direct substring comparison filters the
events that are true deterministic collision witnesses.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from itertools import product
from pathlib import Path

from .fixed_length import (
    CollisionWitness,
    StringInput,
    normalize_symbols,
    prefix_hashes,
    substring_hash,
    validate_base_modulus,
)
from .oracle import OracleResult, all_length_oracle, collision_lengths, verify_witness


@dataclass(frozen=True)
class ShiftDelta:
    """One value of Delta_{i,d}(length)."""

    d: int
    i: int
    length: int
    left_hash: int
    right_hash: int
    delta: int

    @property
    def j(self) -> int:
        return self.i + self.d

    def to_dict(self) -> dict[str, int]:
        return {
            "d": self.d,
            "i": self.i,
            "j": self.j,
            "length": self.length,
            "left_hash": self.left_hash,
            "right_hash": self.right_hash,
            "delta": self.delta,
        }


@dataclass(frozen=True)
class ShiftZeroEvent:
    """A same-hash event for the fixed pair of starts ``i`` and ``i+d``."""

    d: int
    i: int
    length: int
    hash_value: int

    @property
    def j(self) -> int:
        return self.i + self.d

    def as_witness(self) -> CollisionWitness:
        return CollisionWitness(
            length=self.length,
            i=self.i,
            j=self.j,
            hash_value=self.hash_value,
        )

    def to_dict(self) -> dict[str, int]:
        return {
            "d": self.d,
            "i": self.i,
            "j": self.j,
            "length": self.length,
            "hash": self.hash_value,
        }


@dataclass(frozen=True)
class FixedShiftOracleComparison:
    """Audit record comparing fixed-shift enumeration with the all-length oracle."""

    oracle: OracleResult
    first_fixed_shift_witness: CollisionWitness | None
    zero_event_count: int
    true_collision_count: int

    @property
    def agrees(self) -> bool:
        return self.oracle.witness == self.first_fixed_shift_witness

    def to_dict(self) -> dict[str, object]:
        return {
            "agrees": self.agrees,
            "oracle": self.oracle.to_dict(),
            "first_fixed_shift_witness": (
                None
                if self.first_fixed_shift_witness is None
                else self.first_fixed_shift_witness.to_dict()
            ),
            "zero_event_count": self.zero_event_count,
            "true_collision_count": self.true_collision_count,
        }


@dataclass(frozen=True)
class ShiftBatchingSearchOutcome:
    """Result of a finite search for a false fixed-shift batching rule."""

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


EventGroups = Mapping[int, tuple[ShiftZeroEvent, ...]]
Selector = Callable[[EventGroups, int], tuple[ShiftZeroEvent, ...]]


SAVED_FIXED_SHIFT_COUNTEREXAMPLES: dict[str, dict[str, object]] = {}


def fixed_shift_deltas(
    value: StringInput,
    base: int,
    modulus: int,
    d: int,
) -> tuple[ShiftDelta, ...]:
    """Compute Delta_{i,d}(length) for every valid ``i`` and ``length``.

    The canonical enumeration order is increasing length, then increasing
    start ``i`` for the requested fixed shift.
    """

    symbols, prefix, powers = prefix_hashes(value, base, modulus)
    _validate_shift(d, len(symbols))
    records: list[ShiftDelta] = []
    for length in range(1, len(symbols) - d + 1):
        for i in range(len(symbols) - d - length + 1):
            left_hash = substring_hash(prefix, powers, i, length, modulus)
            right_hash = substring_hash(prefix, powers, i + d, length, modulus)
            records.append(
                ShiftDelta(
                    d=d,
                    i=i,
                    length=length,
                    left_hash=left_hash,
                    right_hash=right_hash,
                    delta=(left_hash - right_hash) % modulus,
                )
            )
    return tuple(records)


def fixed_shift_delta_value(
    value: StringInput,
    base: int,
    modulus: int,
    i: int,
    d: int,
    length: int,
) -> int:
    """Return one Delta_{i,d}(length) value after checking bounds."""

    symbols, prefix, powers = prefix_hashes(value, base, modulus)
    _validate_event_bounds(i, d, length, len(symbols))
    left_hash = substring_hash(prefix, powers, i, length, modulus)
    right_hash = substring_hash(prefix, powers, i + d, length, modulus)
    return (left_hash - right_hash) % modulus


def enumerate_zero_events(
    value: StringInput,
    base: int,
    modulus: int,
    d: int,
) -> tuple[ShiftZeroEvent, ...]:
    """Enumerate all zero events for one positive shift ``d``."""

    return tuple(
        ShiftZeroEvent(
            d=record.d,
            i=record.i,
            length=record.length,
            hash_value=record.left_hash,
        )
        for record in fixed_shift_deltas(value, base, modulus, d)
        if record.delta == 0
    )


def all_zero_events(
    value: StringInput,
    base: int,
    modulus: int,
) -> tuple[ShiftZeroEvent, ...]:
    """Enumerate zero events for every positive shift."""

    symbols, prefix, powers = prefix_hashes(value, base, modulus)
    events: list[ShiftZeroEvent] = []
    for d in range(1, len(symbols)):
        events.extend(
            _enumerate_zero_events_precomputed(symbols, prefix, powers, modulus, d)
        )
    return tuple(sorted(events, key=_oracle_event_key))


def group_zero_events_by_shift(
    value: StringInput,
    base: int,
    modulus: int,
) -> dict[int, tuple[ShiftZeroEvent, ...]]:
    """Return ``{d: zero events}`` for every shift with at least one zero."""

    symbols, prefix, powers = prefix_hashes(value, base, modulus)
    groups: dict[int, tuple[ShiftZeroEvent, ...]] = {}
    for d in range(1, len(symbols)):
        events = _enumerate_zero_events_precomputed(symbols, prefix, powers, modulus, d)
        if events:
            groups[d] = events
    return groups


def filter_true_substring_inequality(
    value: StringInput,
    zero_events: Iterable[ShiftZeroEvent],
) -> tuple[ShiftZeroEvent, ...]:
    """Keep only zero events whose two substrings are truly unequal."""

    symbols = normalize_symbols(value)
    true_events = [
        event for event in zero_events if _is_true_collision_event(symbols, event)
    ]
    return tuple(sorted(true_events, key=_oracle_event_key))


def true_collision_witnesses_by_shift(
    value: StringInput,
    base: int,
    modulus: int,
) -> tuple[CollisionWitness, ...]:
    """Return every true fixed-shift collision witness in oracle order."""

    return tuple(
        event.as_witness()
        for event in filter_true_substring_inequality(
            value,
            all_zero_events(value, base, modulus),
        )
    )


def compare_fixed_shift_enumeration_to_oracle(
    value: StringInput,
    base: int,
    modulus: int,
) -> FixedShiftOracleComparison:
    """Compare exhaustive fixed-shift enumeration with the all-length oracle."""

    zero_events = all_zero_events(value, base, modulus)
    true_events = filter_true_substring_inequality(value, zero_events)
    first_witness = None if not true_events else true_events[0].as_witness()
    return FixedShiftOracleComparison(
        oracle=all_length_oracle(value, base, modulus),
        first_fixed_shift_witness=first_witness,
        zero_event_count=len(zero_events),
        true_collision_count=len(true_events),
    )


def select_first_last_zero_events_by_shift(
    groups: EventGroups,
    n: int,
) -> tuple[ShiftZeroEvent, ...]:
    """Select only the first and last zero event of each shift."""

    del n
    selected: list[ShiftZeroEvent] = []
    for events in groups.values():
        if not events:
            continue
        ordered = tuple(sorted(events, key=_oracle_event_key))
        selected.append(ordered[0])
        if ordered[-1] != ordered[0]:
            selected.append(ordered[-1])
    return tuple(sorted(selected, key=_oracle_event_key))


def select_minimal_zero_length_events_by_shift(
    groups: EventGroups,
    n: int,
) -> tuple[ShiftZeroEvent, ...]:
    """Select all zero events with the minimum zero length for each shift."""

    del n
    selected: list[ShiftZeroEvent] = []
    for events in groups.values():
        if not events:
            continue
        min_length = min(event.length for event in events)
        selected.extend(event for event in events if event.length == min_length)
    return tuple(sorted(selected, key=_oracle_event_key))


def select_length_set_events(
    groups: EventGroups,
    allowed_lengths: Iterable[int],
) -> tuple[ShiftZeroEvent, ...]:
    """Select zero events whose length is in a fixed global length set."""

    allowed = set(allowed_lengths)
    return tuple(
        sorted(
            (
                event
                for events in groups.values()
                for event in events
                if event.length in allowed
            ),
            key=_oracle_event_key,
        )
    )


def arithmetic_progression_lengths(n: int, start: int, step: int) -> tuple[int, ...]:
    """Return positive lengths ``start + k * step`` up to ``n``."""

    if start < 1:
        raise ValueError("start must be positive")
    if step < 1:
        raise ValueError("step must be positive")
    return tuple(range(start, n + 1, step))


def powers_of_two_upto(n: int) -> tuple[int, ...]:
    powers: list[int] = []
    value = 1
    while value <= n:
        powers.append(value)
        value *= 2
    return tuple(powers)


def divisors_upto(n: int) -> tuple[int, ...]:
    if n < 1:
        return ()
    return tuple(length for length in range(1, n + 1) if n % length == 0)


def divisor_power_lengths(n: int) -> tuple[int, ...]:
    """Tempting global divisor/power-of-two length set for a string of length n."""

    return tuple(sorted(set(divisors_upto(n)) | set(powers_of_two_upto(n))))


def find_first_last_zero_gap(
    *,
    alphabet_size: int = 3,
    max_n: int = 6,
    base: int | None = None,
    moduli: Iterable[int] = (2, 3, 5, 7),
) -> ShiftBatchingSearchOutcome:
    """Find an instance missed by first/last zero checks per shift."""

    return _find_selector_gap(
        kind="first_last_zero_per_shift_gap",
        selector=select_first_last_zero_events_by_shift,
        alphabet_size=alphabet_size,
        max_n=max_n,
        base=base,
        moduli=moduli,
        rule={"selector": "first and last zero event in each shift, ordered by (length,i,j)"},
    )


def find_minimal_zero_length_gap(
    *,
    alphabet_size: int = 3,
    max_n: int = 6,
    base: int | None = None,
    moduli: Iterable[int] = (2, 3, 5, 7),
) -> ShiftBatchingSearchOutcome:
    """Find an instance missed by checking only minimal zero lengths per shift."""

    return _find_selector_gap(
        kind="minimal_zero_length_per_shift_gap",
        selector=select_minimal_zero_length_events_by_shift,
        alphabet_size=alphabet_size,
        max_n=max_n,
        base=base,
        moduli=moduli,
        rule={"selector": "all zero events with the minimum zero length in each shift"},
    )


def find_arithmetic_progression_gap(
    *,
    progressions: Iterable[tuple[int, int]] = (
        (1, 2),
        (2, 2),
        (1, 3),
        (2, 3),
        (3, 3),
    ),
    alphabet_size: int = 3,
    max_n: int = 6,
    base: int | None = None,
    moduli: Iterable[int] = (2, 3, 5, 7),
) -> ShiftBatchingSearchOutcome:
    """Find an instance missed by one candidate arithmetic progression."""

    resolved_base = alphabet_size if base is None else base
    moduli_tuple = tuple(moduli)
    progressions_tuple = tuple(progressions)
    if not progressions_tuple:
        return _none_found(
            "arithmetic_progression_length_gap",
            _bounds(
                "arithmetic_progression_length_gap",
                alphabet_size,
                max_n,
                resolved_base,
                moduli_tuple,
                progressions=[],
            ),
        )
    best: ShiftBatchingSearchOutcome | None = None
    for start, step in progressions_tuple:
        selector = _length_set_selector_factory(
            lambda n, start=start, step=step: arithmetic_progression_lengths(
                n,
                start,
                step,
            )
        )
        outcome = _find_selector_gap(
            kind="arithmetic_progression_length_gap",
            selector=selector,
            alphabet_size=alphabet_size,
            max_n=max_n,
            base=resolved_base,
            moduli=moduli_tuple,
            rule={
                "selector": "zero events whose length lies in one arithmetic progression",
                "start": start,
                "step": step,
            },
            extra_bounds={"progressions": [list(item) for item in progressions_tuple]},
        )
        if outcome.found:
            return outcome
        if best is None:
            best = outcome
    assert best is not None
    return _none_found(
        "arithmetic_progression_length_gap",
        _bounds(
            "arithmetic_progression_length_gap",
            alphabet_size,
            max_n,
            resolved_base,
            moduli_tuple,
            progressions=[list(item) for item in progressions_tuple],
        ),
    )


def find_divisor_power_length_gap(
    *,
    alphabet_size: int = 3,
    max_n: int = 6,
    base: int | None = None,
    moduli: Iterable[int] = (2, 3, 5, 7),
) -> ShiftBatchingSearchOutcome:
    """Find an instance missed by global divisor/power-of-two length checks."""

    return _find_selector_gap(
        kind="divisor_power_length_gap",
        selector=_length_set_selector_factory(divisor_power_lengths),
        alphabet_size=alphabet_size,
        max_n=max_n,
        base=base,
        moduli=moduli,
        rule={
            "selector": (
                "zero events whose length is a divisor of n or a power of two "
                "at most n"
            )
        },
    )


def run_default_shift_searches(
    *,
    alphabet_size: int = 3,
    max_n: int = 6,
    base: int | None = None,
    moduli: Iterable[int] = (2, 3, 5, 7),
    progressions: Iterable[tuple[int, int]] = (
        (1, 2),
        (2, 2),
        (1, 3),
        (2, 3),
        (3, 3),
    ),
) -> dict[str, ShiftBatchingSearchOutcome]:
    """Run the default finite fixed-shift counterexample searches."""

    return {
        "first_last_zero_per_shift_gap": find_first_last_zero_gap(
            alphabet_size=alphabet_size,
            max_n=max_n,
            base=base,
            moduli=moduli,
        ),
        "minimal_zero_length_per_shift_gap": find_minimal_zero_length_gap(
            alphabet_size=alphabet_size,
            max_n=max_n,
            base=base,
            moduli=moduli,
        ),
        "arithmetic_progression_length_gap": find_arithmetic_progression_gap(
            progressions=progressions,
            alphabet_size=alphabet_size,
            max_n=max_n,
            base=base,
            moduli=moduli,
        ),
        "divisor_power_length_gap": find_divisor_power_length_gap(
            alphabet_size=alphabet_size,
            max_n=max_n,
            base=base,
            moduli=moduli,
        ),
    }


def validate_counterexample_record(record: Mapping[str, object]) -> bool:
    """Validate one saved fixed-shift counterexample record."""

    example = record.get("example")
    if not isinstance(example, Mapping):
        return False
    try:
        symbols = tuple(example.get("S", ()))
        base = int(example.get("base", 0))
        modulus = int(example.get("modulus", 0))
        validate_base_modulus(base, modulus)
    except (TypeError, ValueError):
        return False

    raw_witness = example.get("missed_witness")
    if not isinstance(raw_witness, Mapping):
        return False
    try:
        witness = CollisionWitness(
            length=int(raw_witness.get("length", 0)),
            i=int(raw_witness.get("i", -1)),
            j=int(raw_witness.get("j", -1)),
            hash_value=int(raw_witness.get("hash", -1)),
        )
        if not verify_witness(symbols, base, modulus, witness):
            return False

        groups = group_zero_events_by_shift(symbols, base, modulus)
        if _event_from_witness(witness) not in {
            event for events in groups.values() for event in events
        }:
            return False

        selected = _selected_events_from_record(example)
        selected_true = filter_true_substring_inequality(symbols, selected)
    except (TypeError, ValueError):
        return False
    return len(selected_true) == 0


def validate_saved_fixed_shift_counterexamples(
    records: Mapping[str, object] | None = None,
) -> dict[str, bool]:
    """Validate saved records from memory or a decoded JSON artifact."""

    if records is None:
        records = SAVED_FIXED_SHIFT_COUNTEREXAMPLES
    if isinstance(records.get("outcomes"), Mapping):
        records = records["outcomes"]  # type: ignore[assignment]
    return {
        name: validate_counterexample_record(record)
        for name, record in records.items()
        if isinstance(record, Mapping)
    }


def load_counterexample_json(path: str | Path) -> dict[str, object]:
    with Path(path).open(encoding="utf-8") as handle:
        loaded = json.load(handle)
    if not isinstance(loaded, dict):
        raise ValueError("counterexample JSON must decode to an object")
    return loaded


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m scripts.karp_rabin_collision.fixed_shift"
    )
    parser.add_argument("--alphabet-size", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=6)
    parser.add_argument("--base", type=int, default=None)
    parser.add_argument("--moduli", default="2,3,5,7")
    parser.add_argument(
        "--progressions",
        default="1:2,2:2,1:3,2:3,3:3",
        help="comma-separated start:step pairs",
    )
    parser.add_argument("--output", default=None)
    args = parser.parse_args(argv)

    moduli = tuple(_parse_csv_ints(args.moduli))
    progressions = tuple(_parse_progressions(args.progressions))
    outcomes = run_default_shift_searches(
        alphabet_size=args.alphabet_size,
        max_n=args.max_n,
        base=args.base,
        moduli=moduli,
        progressions=progressions,
    )
    payload = {
        "metadata": {
            "description": (
                "Finite fixed-shift batching counterexamples for deterministic "
                "fixed-base, fixed-prime Karp-Rabin collisions."
            ),
            "no_theorem_claim": True,
            "search_order": "increasing n, lexicographic symbols, listed modulus order",
        },
        "outcomes": {name: outcome.to_dict() for name, outcome in outcomes.items()},
    }
    encoded = json.dumps(payload, indent=2, sort_keys=True)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(encoded + "\n", encoding="utf-8")
    else:
        print(encoded)
    return 0


def _enumerate_zero_events_precomputed(
    symbols: Sequence[int],
    prefix: Sequence[int],
    powers: Sequence[int],
    modulus: int,
    d: int,
) -> tuple[ShiftZeroEvent, ...]:
    _validate_shift(d, len(symbols))
    events: list[ShiftZeroEvent] = []
    for length in range(1, len(symbols) - d + 1):
        for i in range(len(symbols) - d - length + 1):
            left_hash = substring_hash(prefix, powers, i, length, modulus)
            right_hash = substring_hash(prefix, powers, i + d, length, modulus)
            if left_hash == right_hash:
                events.append(
                    ShiftZeroEvent(
                        d=d,
                        i=i,
                        length=length,
                        hash_value=left_hash,
                    )
                )
    return tuple(sorted(events, key=_oracle_event_key))


def _find_selector_gap(
    *,
    kind: str,
    selector: Selector,
    alphabet_size: int,
    max_n: int,
    base: int | None,
    moduli: Iterable[int],
    rule: dict[str, object],
    extra_bounds: dict[str, object] | None = None,
) -> ShiftBatchingSearchOutcome:
    resolved_base = alphabet_size if base is None else base
    moduli_tuple = tuple(moduli)
    bounds = _bounds(kind, alphabet_size, max_n, resolved_base, moduli_tuple)
    if extra_bounds:
        bounds.update(extra_bounds)

    for symbols, modulus in _instances(alphabet_size, max_n, moduli_tuple):
        groups = group_zero_events_by_shift(symbols, resolved_base, modulus)
        if not groups:
            continue
        all_events = tuple(event for events in groups.values() for event in events)
        true_events = filter_true_substring_inequality(symbols, all_events)
        if not true_events:
            continue
        selected = selector(groups, len(symbols))
        selected_true = filter_true_substring_inequality(symbols, selected)
        if selected_true:
            continue
        missed = true_events[0]
        example = _example(
            symbols=symbols,
            base=resolved_base,
            modulus=modulus,
            rule=rule,
            selected=selected,
            missed=missed,
        )
        return ShiftBatchingSearchOutcome(
            kind=kind,
            found=True,
            bounds=bounds,
            example=example,
            notes=(
                "minimal only in the stated increasing-n, lexicographic search order",
                "selected zero events contain no true collision witness",
                "no theorem claim",
            ),
        )
    return _none_found(kind, bounds)


def _example(
    *,
    symbols: tuple[int, ...],
    base: int,
    modulus: int,
    rule: dict[str, object],
    selected: Iterable[ShiftZeroEvent],
    missed: ShiftZeroEvent,
) -> dict[str, object]:
    groups = group_zero_events_by_shift(symbols, base, modulus)
    selected_tuple = tuple(sorted(selected, key=_oracle_event_key))
    return {
        "S": list(symbols),
        "base": base,
        "modulus": modulus,
        "rule": rule,
        "collision_lengths": list(collision_lengths(symbols, base, modulus)),
        "missed_event": missed.to_dict(),
        "missed_witness": missed.as_witness().to_dict(),
        "selected_zero_events": [event.to_dict() for event in selected_tuple],
        "selected_true_collision_events": [
            event.to_dict()
            for event in filter_true_substring_inequality(symbols, selected_tuple)
        ],
        "zero_events_by_shift": {
            str(d): [event.to_dict() for event in events]
            for d, events in sorted(groups.items())
        },
    }


def _length_set_selector_factory(
    length_factory: Callable[[int], Iterable[int]],
) -> Selector:
    def selector(groups: EventGroups, n: int) -> tuple[ShiftZeroEvent, ...]:
        return select_length_set_events(groups, length_factory(n))

    return selector


def _selected_events_from_record(example: Mapping[str, object]) -> tuple[ShiftZeroEvent, ...]:
    raw_events = example.get("selected_zero_events")
    if not isinstance(raw_events, Sequence):
        return ()
    events = []
    for raw in raw_events:
        if not isinstance(raw, Mapping):
            return ()
        events.append(
            ShiftZeroEvent(
                d=int(raw.get("d", 0)),
                i=int(raw.get("i", -1)),
                length=int(raw.get("length", 0)),
                hash_value=int(raw.get("hash", -1)),
            )
        )
    return tuple(events)


def _event_from_witness(witness: CollisionWitness) -> ShiftZeroEvent:
    return ShiftZeroEvent(
        d=witness.j - witness.i,
        i=witness.i,
        length=witness.length,
        hash_value=witness.hash_value,
    )


def _is_true_collision_event(
    symbols: Sequence[int],
    event: ShiftZeroEvent,
) -> bool:
    _validate_event_bounds(event.i, event.d, event.length, len(symbols))
    left = tuple(symbols[event.i : event.i + event.length])
    right_start = event.i + event.d
    right = tuple(symbols[right_start : right_start + event.length])
    return left != right


def _oracle_event_key(event: ShiftZeroEvent) -> tuple[int, int, int]:
    return (event.length, event.i, event.j)


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


def _none_found(
    kind: str,
    bounds: dict[str, object],
) -> ShiftBatchingSearchOutcome:
    return ShiftBatchingSearchOutcome(
        kind=kind,
        found=False,
        bounds=bounds,
        example=None,
        notes=("none found within the finite bounds above", "no theorem claim"),
    )


def _validate_shift(d: int, n: int) -> None:
    if isinstance(d, bool) or not isinstance(d, int):
        raise ValueError("d must be an integer")
    if d < 1:
        raise ValueError("d must be positive")
    if d >= n:
        raise ValueError("d must be less than len(S)")


def _validate_event_bounds(i: int, d: int, length: int, n: int) -> None:
    _validate_shift(d, n)
    if isinstance(i, bool) or not isinstance(i, int):
        raise ValueError("i must be an integer")
    if isinstance(length, bool) or not isinstance(length, int):
        raise ValueError("length must be an integer")
    if i < 0:
        raise ValueError("i must be nonnegative")
    if length < 1:
        raise ValueError("length zero is excluded")
    if i + d + length > n:
        raise ValueError("i, d, and length exceed len(S)")


def _parse_csv_ints(value: str) -> tuple[int, ...]:
    if not value.strip():
        return ()
    return tuple(int(part.strip()) for part in value.split(","))


def _parse_progressions(value: str) -> tuple[tuple[int, int], ...]:
    if not value.strip():
        return ()
    progressions: list[tuple[int, int]] = []
    for raw in value.split(","):
        start, step = raw.split(":", 1)
        progressions.append((int(start), int(step)))
    return tuple(progressions)


if __name__ == "__main__":
    raise SystemExit(main())
