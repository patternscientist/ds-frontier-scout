"""Exact true recursive-search-tree schedules for DS(2,2).

The label order is the one used in the DS(2,2) depth-vector certificate:
``a,b,r,s,li,lj`` with edges ``a-b, b-r, b-s, a-li, a-lj``.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from itertools import product
from typing import Iterable


Vertex = str
Component = tuple[Vertex, ...]

VERTICES: tuple[Vertex, ...] = ("a", "b", "r", "s", "li", "lj")
EDGES: tuple[tuple[Vertex, Vertex], ...] = (
    ("a", "b"),
    ("b", "r"),
    ("b", "s"),
    ("a", "li"),
    ("a", "lj"),
)
ORDER: dict[Vertex, int] = {vertex: index for index, vertex in enumerate(VERTICES)}
ADJACENCY: dict[Vertex, tuple[Vertex, ...]] = {
    vertex: tuple(
        sorted(
            (
                y
                for edge in EDGES
                for x, y in (edge, edge[::-1])
                if x == vertex
            ),
            key=ORDER.__getitem__,
        )
    )
    for vertex in VERTICES
}


@dataclass(frozen=True)
class TrueSchedule:
    """A recursive search-tree schedule on DS(2,2)."""

    schedule_id: str
    component_roots: tuple[tuple[Component, Vertex], ...]
    parent: dict[Vertex, Vertex | None]
    depth: dict[Vertex, int]

    @property
    def depth_vector(self) -> tuple[int, ...]:
        return tuple(self.depth[vertex] for vertex in VERTICES)

    def to_json(self, depth_vector_id: str) -> dict[str, object]:
        return {
            "id": self.schedule_id,
            "depth_vector_id": depth_vector_id,
            "component_roots": [
                {"component": list(component), "root": root}
                for component, root in self.component_roots
            ],
            "parent": {vertex: self.parent[vertex] for vertex in VERTICES},
        }


def canonical_component(vertices: Iterable[Vertex]) -> Component:
    values = tuple(sorted(vertices, key=ORDER.__getitem__))
    if not values:
        raise ValueError("component must be nonempty")
    return values


def is_connected(component: Iterable[Vertex]) -> bool:
    values = set(component)
    if not values or not values.issubset(set(VERTICES)):
        return False
    start = min(values, key=ORDER.__getitem__)
    seen = {start}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for neighbor in ADJACENCY[current]:
            if neighbor in values and neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return seen == values


def connected_components(vertices: Iterable[Vertex]) -> tuple[Component, ...]:
    remaining = set(vertices)
    if not remaining:
        return ()
    components: list[Component] = []
    while remaining:
        start = min(remaining, key=ORDER.__getitem__)
        remaining.remove(start)
        seen = {start}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for neighbor in ADJACENCY[current]:
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    seen.add(neighbor)
                    queue.append(neighbor)
        components.append(canonical_component(seen))
    return tuple(sorted(components, key=lambda item: (len(item), [ORDER[v] for v in item])))


def connected_components_after_removing(
    root: Vertex, within: Iterable[Vertex]
) -> tuple[Component, ...]:
    available = set(within)
    if root not in available:
        raise ValueError("root is not in component")
    available.remove(root)
    return connected_components(available)


def connected_subsets() -> tuple[Component, ...]:
    result: list[Component] = []
    n = len(VERTICES)
    for mask in range(1, 1 << n):
        component = tuple(VERTICES[index] for index in range(n) if mask & (1 << index))
        if is_connected(component):
            result.append(component)
    return tuple(sorted(result, key=lambda item: (len(item), [ORDER[v] for v in item])))


def path_between(source: Vertex, target: Vertex) -> Component:
    if source not in ORDER or target not in ORDER:
        raise ValueError("unknown path endpoint")
    if source == target:
        return (source,)
    parent: dict[Vertex, Vertex | None] = {source: None}
    queue = deque([source])
    while queue and target not in parent:
        current = queue.popleft()
        for neighbor in ADJACENCY[current]:
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)
    if target not in parent:
        raise ValueError("DS(2,2) topology is disconnected")
    reversed_path = [target]
    while reversed_path[-1] != source:
        previous = parent[reversed_path[-1]]
        if previous is None:
            raise ValueError("internal path reconstruction failure")
        reversed_path.append(previous)
    return canonical_component(reversed(reversed_path))


def enumerate_true_schedules() -> tuple[TrueSchedule, ...]:
    schedules: list[TrueSchedule] = []
    for index, raw in enumerate(_enumerate_component(tuple(VERTICES), None, 0)):
        schedules.append(
            TrueSchedule(
                schedule_id=f"T{index:03d}",
                component_roots=raw.component_roots,
                parent=raw.parent,
                depth=raw.depth,
            )
        )
    return tuple(schedules)


def integral_h1_point(schedule: TrueSchedule) -> dict[tuple[Component, Vertex], int]:
    """Return the deterministic H1 point induced by a true schedule."""

    values: dict[tuple[Component, Vertex], int] = {}
    for component in connected_subsets():
        root = min(component, key=lambda vertex: schedule.depth[vertex])
        for vertex in component:
            values[(component, vertex)] = 1 if vertex == root else 0
    return values


@dataclass(frozen=True)
class _PartialSchedule:
    component_roots: tuple[tuple[Component, Vertex], ...]
    parent: dict[Vertex, Vertex | None]
    depth: dict[Vertex, int]


def _enumerate_component(
    component: Component, parent_root: Vertex | None, depth: int
) -> Iterable[_PartialSchedule]:
    component = canonical_component(component)
    for root in component:
        child_components = connected_components_after_removing(root, component)
        child_options = [
            tuple(_enumerate_component(child, root, depth + 1))
            for child in child_components
        ]
        for children in product(*child_options):
            parent = {root: parent_root}
            depths = {root: depth}
            component_roots = [(component, root)]
            for child in children:
                parent.update(child.parent)
                depths.update(child.depth)
                component_roots.extend(child.component_roots)
            yield _PartialSchedule(
                component_roots=tuple(component_roots),
                parent=parent,
                depth=depths,
            )


def main() -> int:
    schedules = enumerate_true_schedules()
    depth_vectors = {schedule.depth_vector for schedule in schedules}
    print(
        "DS(2,2) true schedules: "
        f"schedules={len(schedules)} depth_vectors={len(depth_vectors)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

