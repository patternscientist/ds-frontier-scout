"""Complete STT enumeration for small tree topologies."""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from typing import Iterable

from .stt import STTResult
from .topology import TreeTopology


class EnumerationLimitExceeded(ValueError):
    """Raised when complete enumeration exceeds the configured safety cap."""


def enumerate_stts(
    topology: TreeTopology, depth_base: int = 1, max_count: int = 100_000
) -> list[STTResult]:
    if depth_base not in (0, 1):
        raise ValueError("depth_base must be 0 or 1")
    if max_count <= 0:
        raise ValueError("max_count must be positive")

    results: list[STTResult] = []
    for result in _enumerate_component(topology, tuple(topology.vertices), None, depth_base):
        results.append(result)
        if len(results) > max_count:
            raise EnumerationLimitExceeded(
                f"STT enumeration exceeded safety cap {max_count}"
            )
    return results


def weighted_cost(depths: dict[int, int], weights: dict[int, Fraction]) -> Fraction:
    return sum(weights[v] * depths[v] for v in weights)


def integer_optimum_by_enumeration(
    topology: TreeTopology,
    weights: dict[int, Fraction],
    depth_base: int = 1,
    max_count: int = 100_000,
) -> tuple[Fraction, STTResult, int]:
    best_cost: Fraction | None = None
    best_result: STTResult | None = None
    count = 0
    for result in _enumerate_component(topology, tuple(topology.vertices), None, depth_base):
        count += 1
        if count > max_count:
            raise EnumerationLimitExceeded(
                f"STT enumeration exceeded safety cap {max_count}"
            )
        cost = weighted_cost(result.depth, weights)
        if best_cost is None or cost < best_cost:
            best_cost = cost
            best_result = result
    if best_cost is None or best_result is None:
        raise ValueError("no STTs enumerated")
    return best_cost, best_result, count


def _enumerate_component(
    topology: TreeTopology,
    component: tuple[int, ...],
    parent_root: int | None,
    depth: int,
) -> Iterable[STTResult]:
    component = tuple(sorted(component))
    for root in component:
        child_components = topology.connected_components_after_removing(root, component)
        child_option_lists = [
            list(_enumerate_component(topology, child, root, depth + 1))
            for child in child_components
        ]
        for child_options in product(*child_option_lists):
            parent = {root: parent_root}
            depths = {root: depth}
            component_roots = [(component, root)]
            for child_result in child_options:
                parent.update(child_result.parent)
                depths.update(child_result.depth)
                component_roots.extend(child_result.component_roots)
            yield STTResult(
                parent=parent,
                depth=depths,
                component_roots=tuple(component_roots),
            )

