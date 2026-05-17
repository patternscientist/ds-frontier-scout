"""Baseline list-update policies under the candidate policy interface."""

from __future__ import annotations

from collections import Counter

from scripts.list_update.model import ListState, RequestTrace, access_rank

from .policy_api import PolicySpec


def move_to_front(state: ListState, request: int, history: RequestTrace) -> int:
    return 0


def transpose(state: ListState, request: int, history: RequestTrace) -> int:
    return max(access_rank(state, request) - 1, 0)


def frequency_count(state: ListState, request: int, history: RequestTrace) -> int:
    """Move the request ahead of items with strictly smaller post-access count."""

    counts = Counter(history)
    counts[request] += 1
    rank = access_rank(state, request)
    request_count = counts[request]
    for index, item in enumerate(state[:rank]):
        if counts[item] < request_count:
            return index
    return rank


def static_safe(state: ListState, request: int, history: RequestTrace) -> int:
    return access_rank(state, request)


BASELINE_POLICIES: dict[str, PolicySpec] = {
    "move_to_front": PolicySpec("move_to_front", move_to_front),
    "transpose": PolicySpec("transpose", transpose),
    "frequency_count": PolicySpec("frequency_count", frequency_count),
    "static_safe": PolicySpec("static_safe", static_safe),
}


def get_baseline_policies(names: list[str] | tuple[str, ...] | None = None) -> dict[str, PolicySpec]:
    if names is None:
        return dict(BASELINE_POLICIES)

    selected: dict[str, PolicySpec] = {}
    for name in names:
        if name not in BASELINE_POLICIES:
            known = ", ".join(sorted(BASELINE_POLICIES))
            raise ValueError(f"unknown baseline {name!r}; known baselines: {known}")
        selected[name] = BASELINE_POLICIES[name]
    return selected
