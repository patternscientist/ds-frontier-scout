"""Deterministic workload families for the list-update evaluator."""

from __future__ import annotations

import random
from dataclasses import dataclass

from scripts.list_update.adversarial_traces import (
    enumerate_request_traces,
    worst_traces_by_policy,
)
from scripts.list_update.model import RequestTrace, validate_trace


@dataclass(frozen=True)
class TraceCase:
    id: str
    family: str
    n: int
    trace: RequestTrace
    source: str

    def to_json(self) -> dict[str, object]:
        return {
            "id": self.id,
            "family": self.family,
            "n": self.n,
            "trace": list(self.trace),
            "source": self.source,
        }


def suite_names() -> tuple[str, ...]:
    return tuple(sorted(_SUITE_BUILDERS))


def build_suite(name: str) -> tuple[TraceCase, ...]:
    try:
        cases = _SUITE_BUILDERS[name]()
    except KeyError as exc:
        known = ", ".join(suite_names())
        raise ValueError(f"unknown suite {name!r}; known suites: {known}") from exc
    return tuple(_validate_case(case) for case in cases)


def _smoke_suite() -> tuple[TraceCase, ...]:
    return (
        TraceCase("smoke_n2_gap", "smoke", 2, (1, 0), "hand_checked"),
        TraceCase("smoke_n3_mixed", "smoke", 3, (2, 1, 2), "hand_checked"),
        TraceCase("smoke_static_order", "smoke", 3, (0, 1, 2, 0), "hand_checked"),
        TraceCase("smoke_repeated_tail", "repeated_item", 4, (3, 3, 3, 3), "hand_checked"),
        TraceCase("smoke_phase_shift", "phase_shift", 4, (0, 0, 1, 1, 2, 2, 3, 3), "hand_checked"),
    )


def _all_traces_small_suite() -> tuple[TraceCase, ...]:
    cases: list[TraceCase] = []
    for trace in enumerate_request_traces(n=2, max_length=4):
        cases.append(
            TraceCase(
                f"all_n2_len_le_4_{len(cases):03d}",
                "all_traces_small",
                2,
                trace,
                "scripts.list_update.adversarial_traces.enumerate_request_traces",
            )
        )
    for trace in enumerate_request_traces(n=3, max_length=2):
        cases.append(
            TraceCase(
                f"all_n3_len_le_2_{len(cases):03d}",
                "all_traces_small",
                3,
                trace,
                "scripts.list_update.adversarial_traces.enumerate_request_traces",
            )
        )
    return tuple(cases)


def _random_fixed_seed_suite() -> tuple[TraceCase, ...]:
    rng = random.Random(20260517)
    cases: list[TraceCase] = []
    for index in range(8):
        n = 5
        trace = tuple(rng.randrange(n) for _ in range(12))
        cases.append(
            TraceCase(
                f"random_seed_20260517_{index:02d}",
                "random_fixed_seed",
                n,
                trace,
                "random.Random(20260517)",
            )
        )
    return tuple(cases)


def _locality_biased_suite() -> tuple[TraceCase, ...]:
    rng = random.Random(314159)
    cases: list[TraceCase] = []
    for index in range(8):
        n = 5
        current = index % n
        trace: list[int] = []
        for _step in range(15):
            roll = rng.random()
            if roll < 0.65:
                next_item = current
            elif roll < 0.85:
                next_item = (current + 1) % n
            else:
                next_item = rng.randrange(n)
            trace.append(next_item)
            current = next_item
        cases.append(
            TraceCase(
                f"locality_seed_314159_{index:02d}",
                "locality_biased",
                n,
                tuple(trace),
                "random.Random(314159) with repeat/neighbor bias",
            )
        )
    return tuple(cases)


def _repeated_item_suite() -> tuple[TraceCase, ...]:
    cases = [
        TraceCase(f"repeated_item_{item}", "repeated_item", 4, (item,) * 8, "block repeat")
        for item in range(4)
    ]
    cases.append(
        TraceCase(
            "repeated_item_alternating_blocks",
            "repeated_item",
            4,
            (0, 0, 0, 3, 3, 3, 0, 0, 0, 3, 3, 3),
            "alternating repeated blocks",
        )
    )
    return tuple(cases)


def _phase_shift_suite() -> tuple[TraceCase, ...]:
    return (
        TraceCase(
            "phase_shift_ascending_blocks",
            "phase_shift",
            5,
            (0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4),
            "ascending hot item phases",
        ),
        TraceCase(
            "phase_shift_reverse_blocks",
            "phase_shift",
            5,
            (4, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0),
            "descending hot item phases",
        ),
        TraceCase(
            "phase_shift_interleaved",
            "phase_shift",
            5,
            (0, 1, 0, 1, 4, 3, 4, 3, 2, 2, 2, 0, 4, 0, 4),
            "interleaved phase switch",
        ),
    )


def _adversarial_suite() -> tuple[TraceCase, ...]:
    worst = worst_traces_by_policy(
        n=3,
        max_length=4,
        top_k=3,
        policy_names=("mtf", "transpose", "static"),
    )
    seen: set[RequestTrace] = set()
    traces: list[RequestTrace] = []
    for policy_name in sorted(worst):
        for score in worst[policy_name]:
            if score.trace not in seen:
                seen.add(score.trace)
                traces.append(score.trace)
    traces.sort(key=lambda trace: (len(trace), trace))
    return tuple(
        TraceCase(
            f"adversarial_n3_len_le_4_{index:02d}",
            "adversarial_oracle",
            3,
            trace,
            "scripts.list_update.adversarial_traces.worst_traces_by_policy",
        )
        for index, trace in enumerate(traces)
    )


def _milestone1_suite() -> tuple[TraceCase, ...]:
    return (
        _smoke_suite()
        + _all_traces_small_suite()
        + _random_fixed_seed_suite()
        + _locality_biased_suite()
        + _repeated_item_suite()
        + _phase_shift_suite()
        + _adversarial_suite()
    )


def _validate_case(case: TraceCase) -> TraceCase:
    validate_trace(case.trace, case.n, field=f"{case.id}.trace")
    return case


_SUITE_BUILDERS = {
    "smoke": _smoke_suite,
    "all_traces_small": _all_traces_small_suite,
    "random_fixed_seed": _random_fixed_seed_suite,
    "locality_biased": _locality_biased_suite,
    "repeated_item": _repeated_item_suite,
    "phase_shift": _phase_shift_suite,
    "adversarial": _adversarial_suite,
    "milestone1": _milestone1_suite,
}
