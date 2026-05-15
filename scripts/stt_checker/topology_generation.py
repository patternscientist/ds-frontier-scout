"""Small tree topology generation and canonicalization utilities.

The frontier artifact only needs tiny trees, so this module deliberately uses
plain Prufer-code generation and an AHU-style tree canonical form instead of a
graph-isomorphism dependency.
"""

from __future__ import annotations

from itertools import product
from typing import Iterable

from .topology import TreeTopology


DEFAULT_MAX_N = 7


def decode_prufer_code(code: Iterable[int], n: int) -> list[tuple[int, int]]:
    """Decode a Prufer code into a sorted edge list on vertices ``0..n-1``."""

    code_tuple = tuple(code)
    if n <= 0:
        raise ValueError("n must be positive")
    if n == 1:
        if code_tuple:
            raise ValueError("Prufer code for n=1 must be empty")
        return []
    if len(code_tuple) != n - 2:
        raise ValueError("Prufer code length must be n - 2")
    if any(v < 0 or v >= n for v in code_tuple):
        raise ValueError("Prufer code contains vertex outside 0..n-1")

    degree = [1] * n
    for vertex in code_tuple:
        degree[vertex] += 1

    edges: list[tuple[int, int]] = []
    leaves = {vertex for vertex, value in enumerate(degree) if value == 1}
    for vertex in code_tuple:
        leaf = min(leaves)
        leaves.remove(leaf)
        edges.append(tuple(sorted((leaf, vertex))))
        degree[leaf] -= 1
        degree[vertex] -= 1
        if degree[vertex] == 1:
            leaves.add(vertex)

    a, b = sorted(leaves)
    edges.append((a, b))
    return sorted(edges)


def tree_canonical_form(topology: TreeTopology) -> str:
    """Return an isomorphism-invariant AHU-style canonical form for a tree."""

    centers = _tree_centers(topology)
    rooted_forms = [_rooted_canonical_form(topology, center, None) for center in centers]
    return min(rooted_forms)


def generate_labeled_tree_topologies(n: int) -> Iterable[TreeTopology]:
    """Generate all labeled trees on ``n`` vertices via Prufer codes."""

    if n <= 0:
        raise ValueError("n must be positive")
    if n > DEFAULT_MAX_N:
        raise ValueError(
            f"refusing labeled Prufer generation above n={DEFAULT_MAX_N} by default"
        )
    vertices = list(range(n))
    if n == 1:
        yield TreeTopology.from_dict({"n": 1, "vertices": vertices, "edges": []})
        return
    for code in product(vertices, repeat=n - 2):
        yield TreeTopology.from_dict(
            {
                "n": n,
                "vertices": vertices,
                "edges": [list(edge) for edge in decode_prufer_code(code, n)],
            }
        )


def generate_unlabeled_tree_topologies(max_n: int = DEFAULT_MAX_N) -> list[dict[str, object]]:
    """Generate one representative for each unlabeled tree shape up to ``max_n``.

    The representative is whichever labeled Prufer tree first realizes a
    canonical form. Its vertices are therefore always ``0..n-1``.
    """

    if max_n <= 0:
        raise ValueError("max_n must be positive")
    if max_n > DEFAULT_MAX_N:
        raise ValueError(f"max_n above {DEFAULT_MAX_N} is intentionally unsupported")

    representatives: list[dict[str, object]] = []
    for n in range(1, max_n + 1):
        by_form: dict[str, TreeTopology] = {}
        for topology in generate_labeled_tree_topologies(n):
            canonical = tree_canonical_form(topology)
            by_form.setdefault(canonical, topology)
        for canonical in sorted(by_form):
            topology = by_form[canonical]
            representatives.append(
                {
                    "n": n,
                    "canonical_form": canonical,
                    "topology": topology,
                    "edges": topology.edges,
                    "degree_sequence": tuple(
                        sorted(topology.degrees.values(), reverse=True)
                    ),
                    "derived_labels": tuple(sorted(topology.derived_subclass_labels())),
                    "edge_diameter": topology.diameter_edges,
                }
            )
    return representatives


def _tree_centers(topology: TreeTopology) -> tuple[int, ...]:
    if topology.n <= 2:
        return topology.vertices

    degree = dict(topology.degrees)
    leaves = [vertex for vertex in topology.vertices if degree[vertex] <= 1]
    remaining = topology.n
    while remaining > 2:
        remaining -= len(leaves)
        next_leaves: list[int] = []
        for leaf in leaves:
            degree[leaf] = 0
            for neighbor in topology.adjacency[leaf]:
                if degree[neighbor] > 1:
                    degree[neighbor] -= 1
                    if degree[neighbor] == 1:
                        next_leaves.append(neighbor)
        leaves = sorted(next_leaves)
    return tuple(sorted(vertex for vertex in topology.vertices if degree[vertex] > 0))


def _rooted_canonical_form(
    topology: TreeTopology, vertex: int, parent: int | None
) -> str:
    child_forms = [
        _rooted_canonical_form(topology, child, vertex)
        for child in topology.adjacency[vertex]
        if child != parent
    ]
    return "(" + "".join(sorted(child_forms)) + ")"
