"""Tree topology validation and derived invariants."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Any, Iterable


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


@dataclass(frozen=True)
class TreeTopology:
    n: int
    vertices: tuple[int, ...]
    edges: tuple[tuple[int, int], ...]
    adjacency: dict[int, tuple[int, ...]]
    degrees: dict[int, int]
    distances: dict[int, dict[int, int]]
    diameter_edges: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TreeTopology":
        if not isinstance(data, dict):
            raise ValueError("topology: must be an object")
        n = data.get("n")
        if not _is_int(n) or n <= 0:
            raise ValueError("topology.n: must be a positive integer")

        if "vertices" in data:
            raw_vertices = data["vertices"]
            if not isinstance(raw_vertices, list):
                raise ValueError("topology.vertices: must be a list")
            if any(not _is_int(v) for v in raw_vertices):
                raise ValueError("topology.vertices: all vertices must be integers")
            if len(raw_vertices) != n or len(set(raw_vertices)) != n:
                raise ValueError("topology.vertices: must contain n distinct integers")
            vertices = tuple(sorted(raw_vertices))
        else:
            vertices = tuple(range(n))

        vertex_set = set(vertices)
        raw_edges = data.get("edges")
        if not isinstance(raw_edges, list):
            raise ValueError("topology.edges: must be a list")

        edges_set: set[tuple[int, int]] = set()
        for index, edge in enumerate(raw_edges):
            if (
                not isinstance(edge, list)
                or len(edge) != 2
                or not _is_int(edge[0])
                or not _is_int(edge[1])
            ):
                raise ValueError(f"topology.edges[{index}]: must be a pair of integers")
            a, b = edge
            if a == b:
                raise ValueError(f"topology.edges[{index}]: loop edge is not allowed")
            if a not in vertex_set or b not in vertex_set:
                raise ValueError(f"topology.edges[{index}]: endpoint outside vertex set")
            normalized = tuple(sorted((a, b)))
            if normalized in edges_set:
                raise ValueError(f"topology.edges[{index}]: duplicate edge {normalized}")
            edges_set.add(normalized)

        if len(edges_set) != n - 1:
            raise ValueError("topology.edges: a tree on n vertices must have n - 1 edges")

        adjacency_mut = {v: [] for v in vertices}
        for a, b in sorted(edges_set):
            adjacency_mut[a].append(b)
            adjacency_mut[b].append(a)
        adjacency = {v: tuple(sorted(neighbors)) for v, neighbors in adjacency_mut.items()}

        if not _is_connected(vertices, adjacency):
            raise ValueError("topology: graph is not connected")

        distances = _all_pairs_distances(vertices, adjacency)
        diameter = 0
        for source in vertices:
            if distances[source]:
                diameter = max(diameter, max(distances[source].values()))

        return cls(
            n=n,
            vertices=vertices,
            edges=tuple(sorted(edges_set)),
            adjacency=adjacency,
            degrees={v: len(adjacency[v]) for v in vertices},
            distances=distances,
            diameter_edges=diameter,
        )

    def validate_declared_labels(self, declared: Iterable[str]) -> None:
        derived = self.derived_subclass_labels()
        for label in declared:
            if label == "almost-star":
                continue
            if label in {"path", "star"} or label.startswith("edge-diameter-"):
                if label not in derived:
                    raise ValueError(
                        f"topology.declared_subclass_labels: declared {label!r} "
                        f"but derived labels are {sorted(derived)}"
                    )

    def derived_subclass_labels(self) -> set[str]:
        labels = {f"edge-diameter-{self.diameter_edges}"}
        if max(self.degrees.values(), default=0) <= 2:
            labels.add("path")
        if self.n == 1 or max(self.degrees.values(), default=0) == self.n - 1:
            labels.add("star")
        return labels

    def connected_components_after_removing(
        self, root: int, within: Iterable[int] | None = None
    ) -> list[tuple[int, ...]]:
        if within is None:
            available = set(self.vertices)
        else:
            available = set(within)
        if root not in available:
            raise ValueError("root is not inside component")
        available.remove(root)
        return self.connected_components(available)

    def connected_components(self, subset: Iterable[int]) -> list[tuple[int, ...]]:
        remaining = set(subset)
        if not remaining:
            return []
        if not remaining.issubset(set(self.vertices)):
            raise ValueError("component subset contains invalid vertices")
        components: list[tuple[int, ...]] = []
        while remaining:
            start = min(remaining)
            queue = deque([start])
            seen = {start}
            remaining.remove(start)
            while queue:
                current = queue.popleft()
                for neighbor in self.adjacency[current]:
                    if neighbor in remaining:
                        remaining.remove(neighbor)
                        seen.add(neighbor)
                        queue.append(neighbor)
            components.append(tuple(sorted(seen)))
        return sorted(components)

    def is_connected_subset(self, subset: Iterable[int]) -> bool:
        values = set(subset)
        if not values or not values.issubset(set(self.vertices)):
            return False
        return len(self.connected_components(values)) == 1

    def to_normalized_dict(self, declared: Iterable[str] = ()) -> dict[str, Any]:
        return {
            "n": self.n,
            "vertices": list(self.vertices),
            "edges": [list(edge) for edge in self.edges],
            "declared_subclass_labels": sorted(declared),
            "derived_subclass_labels": sorted(self.derived_subclass_labels()),
            "diameter_edges": self.diameter_edges,
            "degrees": {str(v): self.degrees[v] for v in self.vertices},
        }


def declared_labels_from_topology_dict(data: dict[str, Any]) -> list[str]:
    raw = data.get("declared_subclass_labels", data.get("subclass_labels", []))
    if raw is None:
        return []
    if not isinstance(raw, list) or any(not isinstance(label, str) for label in raw):
        raise ValueError("topology.declared_subclass_labels: must be a list of strings")
    return list(raw)


def _is_connected(vertices: tuple[int, ...], adjacency: dict[int, tuple[int, ...]]) -> bool:
    if not vertices:
        return False
    start = vertices[0]
    queue = deque([start])
    seen = {start}
    while queue:
        current = queue.popleft()
        for neighbor in adjacency[current]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return len(seen) == len(vertices)


def _all_pairs_distances(
    vertices: tuple[int, ...], adjacency: dict[int, tuple[int, ...]]
) -> dict[int, dict[int, int]]:
    distances: dict[int, dict[int, int]] = {}
    for source in vertices:
        queue = deque([source])
        dist = {source: 0}
        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current]:
                if neighbor not in dist:
                    dist[neighbor] = dist[current] + 1
                    queue.append(neighbor)
        distances[source] = dist
    return distances

