"""Recursive STT validation and derived parent/depth maps."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .topology import TreeTopology


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


@dataclass(frozen=True)
class STTResult:
    parent: dict[int, int | None]
    depth: dict[int, int]
    component_roots: tuple[tuple[tuple[int, ...], int], ...]

    def to_normalized_component_roots(self) -> list[dict[str, Any]]:
        return [
            {"component": list(component), "root": root}
            for component, root in self.component_roots
        ]


def validate_stt(
    topology: TreeTopology, stt_data: dict[str, Any], depth_base: int = 1
) -> STTResult:
    if depth_base not in (0, 1):
        raise ValueError("cost.depth_base: must be 0 or 1")
    if not isinstance(stt_data, dict):
        raise ValueError("stt: must be an object")
    raw_entries = stt_data.get("component_roots", [])
    if not isinstance(raw_entries, list):
        raise ValueError("stt.component_roots: must be a list")

    vertex_set = set(topology.vertices)
    entries: dict[tuple[int, ...], int] = {}
    for index, entry in enumerate(raw_entries):
        if not isinstance(entry, dict):
            raise ValueError(f"stt.component_roots[{index}]: must be an object")
        component = entry.get("component")
        root = entry.get("root")
        if not isinstance(component, list) or any(not _is_int(v) for v in component):
            raise ValueError(f"stt.component_roots[{index}].component: must be integers")
        if not component:
            raise ValueError(f"stt.component_roots[{index}].component: must be nonempty")
        if len(component) != len(set(component)):
            raise ValueError(f"stt.component_roots[{index}].component: duplicate vertex")
        component_tuple = tuple(sorted(component))
        component_set = set(component_tuple)
        if not component_set.issubset(vertex_set):
            raise ValueError(f"stt.component_roots[{index}].component: invalid vertex")
        if not topology.is_connected_subset(component_set):
            raise ValueError(f"stt.component_roots[{index}].component: not connected")
        if not _is_int(root):
            raise ValueError(f"stt.component_roots[{index}].root: must be an integer")
        if root not in component_set:
            raise ValueError(f"stt.component_roots[{index}].root: outside component")
        if component_tuple in entries:
            raise ValueError(f"stt.component_roots[{index}].component: duplicate component")
        entries[component_tuple] = root

    parent: dict[int, int | None] = {}
    depth: dict[int, int] = {}
    reached: set[tuple[int, ...]] = set()
    normalized: list[tuple[tuple[int, ...], int]] = []

    def recurse(component: tuple[int, ...], parent_root: int | None, current_depth: int) -> None:
        key = tuple(sorted(component))
        if len(key) == 1:
            root = key[0]
            if key in entries:
                if entries[key] != root:
                    raise ValueError("stt: singleton component root mismatch")
                reached.add(key)
            parent[root] = parent_root
            depth[root] = current_depth
            normalized.append((key, root))
            return

        if key not in entries:
            raise ValueError(f"stt: missing root for non-singleton component {list(key)}")
        root = entries[key]
        reached.add(key)
        parent[root] = parent_root
        depth[root] = current_depth
        normalized.append((key, root))
        for child in topology.connected_components_after_removing(root, key):
            recurse(child, root, current_depth + 1)

    recurse(tuple(topology.vertices), None, depth_base)

    unreached = set(entries) - reached
    if unreached:
        formatted = [list(component) for component in sorted(unreached)]
        raise ValueError(f"stt: declared component was never reached: {formatted}")
    if set(parent) != set(topology.vertices) or set(depth) != set(topology.vertices):
        raise ValueError("stt: recursion did not assign every vertex")

    return STTResult(parent=parent, depth=depth, component_roots=tuple(normalized))


def validate_parent_array(
    topology: TreeTopology, parent: dict[int, int | None], raw_parent: Any
) -> None:
    """Validate optional derived ``stt_parent`` data against the recursive STT."""

    if raw_parent is None:
        return
    if topology.vertices != tuple(range(topology.n)):
        raise ValueError("stt_parent: array form requires vertices 0..n-1")
    if not isinstance(raw_parent, list) or len(raw_parent) != topology.n:
        raise ValueError("stt_parent: must be a list of length n")
    for vertex, claimed in enumerate(raw_parent):
        expected = parent[vertex]
        if claimed is None:
            if expected is not None:
                raise ValueError(f"stt_parent[{vertex}]: expected {expected}, got null")
        elif not _is_int(claimed) or claimed != expected:
            raise ValueError(f"stt_parent[{vertex}]: expected {expected}, got {claimed!r}")

