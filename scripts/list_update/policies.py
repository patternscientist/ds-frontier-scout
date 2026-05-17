"""Exact online policy evaluators for small list-update traces."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, Mapping

from .model import (
    ListState,
    RequestTrace,
    access_cost,
    access_rank,
    free_successors,
    initial_state_for_n,
    move_accessed_to_position,
    validate_n,
    validate_state,
    validate_trace,
)


@dataclass(frozen=True)
class DeterministicPolicy:
    name: str
    transition: Callable[[ListState, int], ListState]


@dataclass(frozen=True)
class RandomizedPolicy:
    name: str
    transition_distribution: Callable[[ListState, int], Mapping[ListState, Fraction]]


@dataclass(frozen=True)
class OnlineStep:
    request: int
    state_before: ListState
    access_rank: int
    access_cost: int
    state_after: ListState


@dataclass(frozen=True)
class DeterministicEvaluation:
    policy_name: str
    n: int
    trace: RequestTrace
    initial_state: ListState
    cost: int
    final_state: ListState
    steps: tuple[OnlineStep, ...]


@dataclass(frozen=True)
class RandomizedStep:
    request: int
    state_distribution_before: tuple[tuple[ListState, Fraction], ...]
    expected_access_cost: Fraction
    state_distribution_after: tuple[tuple[ListState, Fraction], ...]


@dataclass(frozen=True)
class RandomizedEvaluation:
    policy_name: str
    n: int
    trace: RequestTrace
    initial_state: ListState
    expected_cost: Fraction
    final_distribution: tuple[tuple[ListState, Fraction], ...]
    steps: tuple[RandomizedStep, ...]


def mtf_transition(state: ListState, request: int) -> ListState:
    return move_accessed_to_position(state, request, 0)


def transpose_transition(state: ListState, request: int) -> ListState:
    rank = access_rank(state, request)
    return move_accessed_to_position(state, request, max(rank - 1, 0))


def static_transition(state: ListState, request: int) -> ListState:
    access_rank(state, request)
    return state


def half_mtf_half_transpose_distribution(
    state: ListState, request: int
) -> dict[ListState, Fraction]:
    mtf_state = mtf_transition(state, request)
    transpose_state = transpose_transition(state, request)
    return _combine_distribution(
        ((mtf_state, Fraction(1, 2)), (transpose_state, Fraction(1, 2)))
    )


DETERMINISTIC_POLICIES: dict[str, DeterministicPolicy] = {
    "mtf": DeterministicPolicy("mtf", mtf_transition),
    "transpose": DeterministicPolicy("transpose", transpose_transition),
    "static": DeterministicPolicy("static", static_transition),
}

RANDOMIZED_POLICIES: dict[str, RandomizedPolicy] = {
    "half_mtf_half_transpose": RandomizedPolicy(
        "half_mtf_half_transpose",
        half_mtf_half_transpose_distribution,
    )
}


def evaluate_deterministic_policy(
    policy: DeterministicPolicy,
    trace: list[int] | tuple[int, ...],
    n: int,
    initial_state: ListState | None = None,
) -> DeterministicEvaluation:
    validate_n(n)
    trace_tuple = validate_trace(trace, n)
    if initial_state is None:
        state = initial_state_for_n(n)
    else:
        state = validate_state(initial_state, n, field="initial_state")
    start_state = state

    total_cost = 0
    steps: list[OnlineStep] = []
    for request in trace_tuple:
        rank = access_rank(state, request)
        cost = rank + 1
        state_after = policy.transition(state, request)
        state_after = validate_state(state_after, n, field=f"{policy.name} state_after")
        if state_after not in free_successors(state, request):
            raise ValueError(
                f"{policy.name}: transition {state!r} -> {state_after!r} is not a free "
                f"move after requesting {request}"
            )
        steps.append(
            OnlineStep(
                request=request,
                state_before=state,
                access_rank=rank,
                access_cost=cost,
                state_after=state_after,
            )
        )
        total_cost += cost
        state = state_after

    return DeterministicEvaluation(
        policy_name=policy.name,
        n=n,
        trace=trace_tuple,
        initial_state=start_state,
        cost=total_cost,
        final_state=state,
        steps=tuple(steps),
    )


def evaluate_randomized_policy(
    policy: RandomizedPolicy,
    trace: list[int] | tuple[int, ...],
    n: int,
    initial_state: ListState | None = None,
) -> RandomizedEvaluation:
    validate_n(n)
    trace_tuple = validate_trace(trace, n)
    if initial_state is None:
        start_state = initial_state_for_n(n)
    else:
        start_state = validate_state(initial_state, n, field="initial_state")

    distribution: dict[ListState, Fraction] = {start_state: Fraction(1, 1)}
    expected_total = Fraction(0, 1)
    steps: list[RandomizedStep] = []

    for request in trace_tuple:
        before = _sorted_distribution(distribution)
        expected_access = sum(
            probability * access_cost(state, request)
            for state, probability in distribution.items()
        )
        next_distribution: dict[ListState, Fraction] = {}
        for state, state_probability in distribution.items():
            transition_distribution = _validate_transition_distribution(
                policy,
                state,
                request,
                n,
            )
            for state_after, transition_probability in transition_distribution.items():
                next_distribution[state_after] = next_distribution.get(
                    state_after, Fraction(0, 1)
                ) + state_probability * transition_probability
        distribution = {
            state: probability
            for state, probability in next_distribution.items()
            if probability != 0
        }
        expected_total += expected_access
        steps.append(
            RandomizedStep(
                request=request,
                state_distribution_before=before,
                expected_access_cost=expected_access,
                state_distribution_after=_sorted_distribution(distribution),
            )
        )

    return RandomizedEvaluation(
        policy_name=policy.name,
        n=n,
        trace=trace_tuple,
        initial_state=start_state,
        expected_cost=expected_total,
        final_distribution=_sorted_distribution(distribution),
        steps=tuple(steps),
    )


def _combine_distribution(
    weighted_states: tuple[tuple[ListState, Fraction], ...]
) -> dict[ListState, Fraction]:
    combined: dict[ListState, Fraction] = {}
    for state, probability in weighted_states:
        combined[state] = combined.get(state, Fraction(0, 1)) + probability
    return {state: probability for state, probability in combined.items() if probability}


def _validate_transition_distribution(
    policy: RandomizedPolicy,
    state: ListState,
    request: int,
    n: int,
) -> dict[ListState, Fraction]:
    raw_distribution = policy.transition_distribution(state, request)
    distribution: dict[ListState, Fraction] = {}
    for state_after, probability in raw_distribution.items():
        if not isinstance(probability, Fraction):
            raise ValueError(f"{policy.name}: probabilities must be Fraction values")
        if probability < 0:
            raise ValueError(f"{policy.name}: probabilities must be nonnegative")
        state_after = validate_state(state_after, n, field=f"{policy.name} state_after")
        if state_after not in free_successors(state, request):
            raise ValueError(
                f"{policy.name}: transition {state!r} -> {state_after!r} is not a free "
                f"move after requesting {request}"
            )
        distribution[state_after] = distribution.get(state_after, Fraction(0, 1)) + probability
    total_probability = sum(distribution.values(), Fraction(0, 1))
    if total_probability != 1:
        raise ValueError(f"{policy.name}: transition probabilities sum to {total_probability}")
    return {state: probability for state, probability in distribution.items() if probability}


def _sorted_distribution(
    distribution: Mapping[ListState, Fraction]
) -> tuple[tuple[ListState, Fraction], ...]:
    return tuple(sorted(distribution.items(), key=lambda item: item[0]))
