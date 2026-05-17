"""Exact offline optimum for tiny full-cost list-update instances."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache

from .model import (
    ListState,
    RequestTrace,
    access_rank,
    all_list_states,
    free_successors,
    initial_state_for_n,
    validate_n,
    validate_state,
    validate_trace,
)


@dataclass(frozen=True)
class TransitionWitness:
    """One minimum-cost standard transition for a fixed start/request/post state."""

    start_state: ListState
    request: int
    access_state: ListState
    post_state: ListState
    paid_exchange_cost: int
    access_rank: int
    access_cost: int

    @property
    def total_cost(self) -> int:
        return self.paid_exchange_cost + self.access_cost


@dataclass(frozen=True)
class OfflineStep:
    request: int
    state_before: ListState
    access_state: ListState
    paid_exchange_cost: int
    access_rank: int
    access_cost: int
    state_after: ListState

    @property
    def total_cost(self) -> int:
        return self.paid_exchange_cost + self.access_cost


@dataclass(frozen=True)
class OfflineOptimumResult:
    n: int
    trace: RequestTrace
    initial_state: ListState
    cost: int
    final_state: ListState
    steps: tuple[OfflineStep, ...]


def fraction_to_string(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def competitive_ratio(policy_cost: int | Fraction, offline_cost: int | Fraction) -> Fraction:
    offline = Fraction(offline_cost)
    if offline <= 0:
        raise ValueError("offline_cost must be positive")
    return Fraction(policy_cost, 1) / offline


def kendall_tau_distance(start: ListState, target: ListState) -> int:
    """Minimum adjacent swaps needed to transform ``start`` into ``target``."""

    if len(start) != len(target) or set(start) != set(target):
        raise ValueError("states must be permutations of the same items")
    start_position = {item: index for index, item in enumerate(start)}
    encoded_target = [start_position[item] for item in target]
    inversions = 0
    for left in range(len(encoded_target)):
        for right in range(left + 1, len(encoded_target)):
            if encoded_target[left] > encoded_target[right]:
                inversions += 1
    return inversions


def standard_transition_witnesses(
    start_state: ListState,
    request: int,
) -> tuple[TransitionWitness, ...]:
    """Minimum transition witness for each reachable post-access state.

    A transition consists of standard paid adjacent exchanges before the access,
    then the full-cost access, then one free forward move of the accessed item.
    """

    start_state = validate_state(start_state)
    n = len(start_state)
    validate_trace((request,), n, field="request")
    return _standard_transition_witnesses_cached(start_state, request)


@lru_cache(maxsize=None)
def _standard_transition_witnesses_cached(
    start_state: ListState,
    request: int,
) -> tuple[TransitionWitness, ...]:
    n = len(start_state)
    best_by_post: dict[ListState, TransitionWitness] = {}
    for access_state in all_list_states(n):
        paid_cost = kendall_tau_distance(start_state, access_state)
        rank = access_rank(access_state, request)
        cost = rank + 1
        for post_state in free_successors(access_state, request):
            witness = TransitionWitness(
                start_state=start_state,
                request=request,
                access_state=access_state,
                post_state=post_state,
                paid_exchange_cost=paid_cost,
                access_rank=rank,
                access_cost=cost,
            )
            incumbent = best_by_post.get(post_state)
            if incumbent is None or _witness_key(witness) < _witness_key(incumbent):
                best_by_post[post_state] = witness

    return tuple(best_by_post[state] for state in sorted(best_by_post))


def standard_transition_costs(start_state: ListState, request: int) -> dict[ListState, int]:
    return {
        witness.post_state: witness.total_cost
        for witness in standard_transition_witnesses(start_state, request)
    }


def offline_optimum(
    trace: list[int] | tuple[int, ...],
    n: int,
    initial_state: ListState | None = None,
) -> OfflineOptimumResult:
    """Compute exact offline optimum by DP over all list permutations."""

    validate_n(n)
    trace_tuple = validate_trace(trace, n)
    if initial_state is None:
        initial_state = initial_state_for_n(n)
    else:
        initial_state = validate_state(initial_state, n, field="initial_state")

    current: dict[ListState, int] = {initial_state: 0}
    predecessors: list[dict[ListState, tuple[ListState, TransitionWitness]]] = []

    for request in trace_tuple:
        next_costs: dict[ListState, int] = {}
        next_predecessors: dict[ListState, tuple[ListState, TransitionWitness]] = {}
        for state, prefix_cost in current.items():
            for witness in standard_transition_witnesses(state, request):
                candidate_cost = prefix_cost + witness.total_cost
                incumbent = next_costs.get(witness.post_state)
                if incumbent is None or candidate_cost < incumbent:
                    next_costs[witness.post_state] = candidate_cost
                    next_predecessors[witness.post_state] = (state, witness)
                elif candidate_cost == incumbent:
                    previous_state, previous_witness = next_predecessors[witness.post_state]
                    if _predecessor_tie_key(state, witness) < _predecessor_tie_key(
                        previous_state, previous_witness
                    ):
                        next_predecessors[witness.post_state] = (state, witness)
        current = next_costs
        predecessors.append(next_predecessors)

    if not current:
        raise ValueError("offline DP reached no states")

    final_state, best_cost = min(current.items(), key=lambda item: (item[1], item[0]))
    steps_reversed: list[OfflineStep] = []
    cursor = final_state
    for layer in reversed(predecessors):
        previous_state, witness = layer[cursor]
        steps_reversed.append(
            OfflineStep(
                request=witness.request,
                state_before=previous_state,
                access_state=witness.access_state,
                paid_exchange_cost=witness.paid_exchange_cost,
                access_rank=witness.access_rank,
                access_cost=witness.access_cost,
                state_after=witness.post_state,
            )
        )
        cursor = previous_state
    steps = tuple(reversed(steps_reversed))

    return OfflineOptimumResult(
        n=n,
        trace=trace_tuple,
        initial_state=initial_state,
        cost=best_cost,
        final_state=final_state,
        steps=steps,
    )


def _witness_key(witness: TransitionWitness) -> tuple[int, ListState, ListState]:
    return (witness.total_cost, witness.access_state, witness.post_state)


def _predecessor_tie_key(
    previous_state: ListState, witness: TransitionWitness
) -> tuple[ListState, int, ListState, ListState]:
    return (
        previous_state,
        witness.total_cost,
        witness.access_state,
        witness.post_state,
    )
