"""Model constants for the list-update exact evaluator.

This scaffold uses the full-cost standard list-update model:

* a list state is a permutation of item labels ``0..n-1``;
* accessing an item in 0-based rank ``r`` costs ``r + 1``;
* immediately after access, the accessed item may move to any earlier list
  position for free, including moving to the front or staying put;
* the offline optimum may use the standard unit-cost adjacent paid exchanges.

There are no alternate paid-exchange variants in this package. The DP
canonicalizes paid exchanges as rearrangements before an access; paid
rearrangements after an access can be charged before the next access.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import permutations
from typing import Iterable


MAX_EXACT_N = 5
FULL_COST_MODEL_NAME = "full_cost_standard_free_after_access"

ListState = tuple[int, ...]
RequestTrace = tuple[int, ...]


def validate_n(n: int) -> None:
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError("n must be an integer")
    if n < 1:
        raise ValueError("n must be positive")
    if n > MAX_EXACT_N:
        raise ValueError(f"exact scaffold supports n <= {MAX_EXACT_N}")


def initial_state_for_n(n: int) -> ListState:
    validate_n(n)
    return tuple(range(n))


@lru_cache(maxsize=None)
def all_list_states(n: int) -> tuple[ListState, ...]:
    validate_n(n)
    return tuple(permutations(range(n)))


def validate_state(state: Iterable[int], n: int | None = None, field: str = "state") -> ListState:
    state_tuple = tuple(state)
    if n is None:
        n = len(state_tuple)
    validate_n(n)
    if len(state_tuple) != n:
        raise ValueError(f"{field}: expected length {n}, got {len(state_tuple)}")
    expected = set(range(n))
    if set(state_tuple) != expected:
        raise ValueError(f"{field}: expected a permutation of 0..{n - 1}")
    return state_tuple


def validate_trace(trace: Iterable[int], n: int, field: str = "trace") -> RequestTrace:
    validate_n(n)
    result = tuple(trace)
    for index, item in enumerate(result):
        if not isinstance(item, int) or isinstance(item, bool) or item < 0 or item >= n:
            raise ValueError(f"{field}[{index}]: expected an item in 0..{n - 1}")
    return result


def access_rank(state: ListState, item: int) -> int:
    if item not in state:
        raise ValueError(f"item {item!r} is not in state {state!r}")
    return state.index(item)


def access_cost(state: ListState, item: int) -> int:
    return access_rank(state, item) + 1


def move_accessed_to_position(state: ListState, item: int, target_index: int) -> ListState:
    """Move ``item`` forward after access, preserving all other relative order."""

    rank = access_rank(state, item)
    if target_index < 0 or target_index > rank:
        raise ValueError(
            "free move target must be between the front and the accessed item's rank"
        )
    without_item = [candidate for candidate in state if candidate != item]
    return tuple(without_item[:target_index] + [item] + without_item[target_index:])


def free_successors(state: ListState, item: int) -> tuple[ListState, ...]:
    """All states reachable by a free forward move of the accessed item."""

    state = validate_state(state)
    return _free_successors_cached(state, item)


@lru_cache(maxsize=None)
def _free_successors_cached(state: ListState, item: int) -> tuple[ListState, ...]:
    rank = access_rank(state, item)
    return tuple(move_accessed_to_position(state, item, target) for target in range(rank + 1))
