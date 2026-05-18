"""Exact DS(3,2)/DS(4,2) packet-window capacity hardening.

This module stays in the H1 first-hit coordinate system and embeds the
DS(2,2) ``Sigma/Lambda/Gamma/Delta/Omega/Pi`` packet atoms into every two-left
window of DS(k,2).  Floating-point simplex is used only to find candidate LP
bases; checked artifacts store exact rational packet coefficients.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, permutations, product
import json
from pathlib import Path
from typing import Any, Iterable

from scripts.stt_checker.hereditary_lp import DEFAULT_TOLERANCE, _simplex_maximize

from .ds22_h1_depth_polytope import _solve_square_linear_system


Vertex = str
Component = tuple[Vertex, ...]
Variable = tuple[Component, Vertex]
SparseRow = dict[int, Fraction]

FACTORIZATION_SCHEMA = "ds32_ds42_packet_window_factorizations_v0"
GAP_SCHEMA = "ds32_ds42_packet_window_gap_witnesses_v0"

DEFAULT_DS32_FACTORIZATIONS = Path("data/ds32_packet_window_factorizations_ternary.json")
DEFAULT_DS42_FACTORIZATIONS = Path("data/ds42_packet_window_factorizations_binary.json")
DEFAULT_GAP_WITNESSES = Path("data/ds32_ds42_packet_window_gap_witnesses.json")
DEFAULT_REPORT = Path("reports/ds32_ds42_packet_window_capacity_hardening_report.md")


@dataclass(frozen=True)
class K2Topology:
    k: int
    vertices: tuple[Vertex, ...]
    left_leaves: tuple[Vertex, ...]
    right_leaves: tuple[Vertex, ...]
    edges: tuple[tuple[Vertex, Vertex], ...]
    order: dict[Vertex, int]
    adjacency: dict[Vertex, tuple[Vertex, ...]]


@dataclass(frozen=True)
class H1CoordinateSystem:
    topology: K2Topology
    connected_subsets: tuple[Component, ...]
    variables: tuple[Variable, ...]
    variable_index: dict[Variable, int]


@dataclass(frozen=True)
class PacketAtom:
    atom_id: str
    kind: str
    window: tuple[Vertex, Vertex]
    vector: tuple[Fraction, ...]
    parameters: dict[str, Any]


@dataclass(frozen=True)
class TrueDepthCatalog:
    schedule_count: int
    depth_vectors: tuple[tuple[int, ...], ...]

    @property
    def depth_vector_count(self) -> int:
        return len(self.depth_vectors)


@dataclass(frozen=True)
class ExactPacketLPSolution:
    status: int
    message: str
    optimum: Fraction
    coefficients: tuple[Fraction, ...]
    residual: tuple[Fraction, ...]
    dual: tuple[Fraction, ...]
    nonzero_coefficients: int


@dataclass(frozen=True)
class PacketLPModel:
    atoms: tuple[PacketAtom, ...]
    rows: tuple[SparseRow, ...]
    float_matrix: list[list[float]]
    atom_signature_index: dict[tuple[str, tuple[Vertex, Vertex], tuple[Fraction, ...]], int]


def rational_to_string(value: Fraction | int) -> str:
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def parse_fraction(value: Any, field: str = "value") -> Fraction:
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, str):
        try:
            return Fraction(value)
        except ValueError as exc:
            raise ValueError(f"{field}: invalid rational {value!r}") from exc
    raise ValueError(f"{field}: expected rational string")


def ds_k2_topology(k: int) -> K2Topology:
    if k < 2:
        raise ValueError("packet-window DS(k,2) requires k >= 2")
    left_leaves = tuple(f"l{index}" for index in range(1, k + 1))
    right_leaves = ("r", "s")
    vertices = ("a", "b", *right_leaves, *left_leaves)
    edges = (("a", "b"), ("b", "r"), ("b", "s"), *tuple(("a", leaf) for leaf in left_leaves))
    order = {vertex: index for index, vertex in enumerate(vertices)}
    adjacency: dict[Vertex, list[Vertex]] = {vertex: [] for vertex in vertices}
    for source, target in edges:
        adjacency[source].append(target)
        adjacency[target].append(source)
    frozen_adjacency = {
        vertex: tuple(sorted(neighbors, key=order.__getitem__))
        for vertex, neighbors in adjacency.items()
    }
    return K2Topology(
        k=k,
        vertices=vertices,
        left_leaves=left_leaves,
        right_leaves=right_leaves,
        edges=edges,
        order=order,
        adjacency=frozen_adjacency,
    )


def canonical_component(topology: K2Topology, vertices: Iterable[Vertex]) -> Component:
    values = tuple(sorted(vertices, key=topology.order.__getitem__))
    if not values:
        raise ValueError("component must be nonempty")
    if len(set(values)) != len(values):
        raise ValueError(f"component has duplicate vertices: {values}")
    return values


def is_connected(topology: K2Topology, component: Iterable[Vertex]) -> bool:
    values = set(component)
    if not values or not values.issubset(set(topology.vertices)):
        return False
    start = min(values, key=topology.order.__getitem__)
    seen = {start}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for neighbor in topology.adjacency[current]:
            if neighbor in values and neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return seen == values


def connected_components(topology: K2Topology, vertices: Iterable[Vertex]) -> tuple[Component, ...]:
    remaining = set(vertices)
    if not remaining:
        return ()
    components: list[Component] = []
    while remaining:
        start = min(remaining, key=topology.order.__getitem__)
        remaining.remove(start)
        seen = {start}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for neighbor in topology.adjacency[current]:
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    seen.add(neighbor)
                    queue.append(neighbor)
        components.append(canonical_component(topology, seen))
    return tuple(
        sorted(
            components,
            key=lambda item: (len(item), [topology.order[vertex] for vertex in item]),
        )
    )


def connected_components_after_removing(
    topology: K2Topology, root: Vertex, within: Iterable[Vertex]
) -> tuple[Component, ...]:
    available = set(within)
    if root not in available:
        raise ValueError("root is not in component")
    available.remove(root)
    return connected_components(topology, available)


def connected_subsets(topology: K2Topology) -> tuple[Component, ...]:
    result: list[Component] = []
    n = len(topology.vertices)
    for mask in range(1, 1 << n):
        component = tuple(
            topology.vertices[index] for index in range(n) if mask & (1 << index)
        )
        if is_connected(topology, component):
            result.append(component)
    return tuple(
        sorted(result, key=lambda item: (len(item), [topology.order[vertex] for vertex in item]))
    )


def h1_coordinate_system(k: int) -> H1CoordinateSystem:
    topology = ds_k2_topology(k)
    subsets = connected_subsets(topology)
    variables = tuple((component, root) for component in subsets for root in component)
    variable_index = {variable: index for index, variable in enumerate(variables)}
    return H1CoordinateSystem(
        topology=topology,
        connected_subsets=subsets,
        variables=variables,
        variable_index=variable_index,
    )


def path_between(topology: K2Topology, source: Vertex, target: Vertex) -> Component:
    if source not in topology.order or target not in topology.order:
        raise ValueError("unknown path endpoint")
    if source == target:
        return (source,)
    parent: dict[Vertex, Vertex | None] = {source: None}
    queue = deque([source])
    while queue and target not in parent:
        current = queue.popleft()
        for neighbor in topology.adjacency[current]:
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)
    if target not in parent:
        raise ValueError("DS(k,2) topology is disconnected")
    reversed_path = [target]
    while reversed_path[-1] != source:
        previous = parent[reversed_path[-1]]
        if previous is None:
            raise ValueError("internal path reconstruction failure")
        reversed_path.append(previous)
    return canonical_component(topology, reversed(reversed_path))


def true_depth_catalog(topology: K2Topology) -> TrueDepthCatalog:
    schedules = list(_enumerate_component_depths(topology, tuple(topology.vertices), 0))
    depth_vectors = sorted(
        {
            tuple(depths[vertex] for vertex in topology.vertices)
            for depths in schedules
        }
    )
    return TrueDepthCatalog(
        schedule_count=len(schedules),
        depth_vectors=tuple(depth_vectors),
    )


def coordinate_capacity(
    system: H1CoordinateSystem, weights: Iterable[Fraction | int]
) -> tuple[Fraction, ...]:
    topology = system.topology
    weight_tuple = tuple(Fraction(value) for value in weights)
    if len(weight_tuple) != len(topology.vertices):
        raise ValueError("weight vector length must match topology vertices")
    capacity = [Fraction(0) for _ in system.variables]
    for source_index, source in enumerate(topology.vertices):
        for target in topology.vertices:
            if source == target:
                continue
            path = path_between(topology, source, target)
            capacity[system.variable_index[(path, target)]] += weight_tuple[source_index]
    return tuple(capacity)


def true_optimum(
    catalog: TrueDepthCatalog,
    weights: Iterable[Fraction | int],
) -> Fraction:
    weight_tuple = tuple(Fraction(value) for value in weights)
    if all(value.denominator == 1 for value in weight_tuple):
        integer_weights = tuple(value.numerator for value in weight_tuple)
        return Fraction(
            min(
                sum(weight * depth for weight, depth in zip(integer_weights, depth_vector))
                for depth_vector in catalog.depth_vectors
            )
        )
    return min(
        sum(weight * depth for weight, depth in zip(weight_tuple, depth_vector))
        for depth_vector in catalog.depth_vectors
    )


def packet_atoms(system: H1CoordinateSystem) -> tuple[PacketAtom, ...]:
    atoms: list[PacketAtom] = []
    for left_pair in combinations(system.topology.left_leaves, 2):
        atoms.extend(_window_packet_atoms(system, tuple(left_pair)))
    return tuple(atoms)


def packet_lp_model(system: H1CoordinateSystem) -> PacketLPModel:
    atoms = packet_atoms(system)
    atom_signature_index = {
        _atom_signature(atom): index for index, atom in enumerate(atoms)
    }
    if len(atom_signature_index) != len(atoms):
        raise ValueError("packet atom signatures are not unique")
    rows: tuple[SparseRow, ...] = tuple(
        {
            atom_index: atom.vector[coordinate]
            for atom_index, atom in enumerate(atoms)
            if atom.vector[coordinate] != 0
        }
        for coordinate in range(len(system.variables))
    )
    float_matrix = [
        [float(row.get(atom_index, Fraction(0))) for atom_index in range(len(atoms))]
        for row in rows
    ]
    return PacketLPModel(
        atoms=atoms,
        rows=rows,
        float_matrix=float_matrix,
        atom_signature_index=atom_signature_index,
    )


def solve_packet_window_lp(
    model: PacketLPModel,
    capacity: tuple[Fraction, ...],
    *,
    tolerance: float = DEFAULT_TOLERANCE,
) -> ExactPacketLPSolution:
    atom_count = len(model.atoms)
    simplex_result = _simplex_maximize(
        model.float_matrix,
        [float(value) for value in capacity],
        [1.0 for _ in model.atoms],
        tolerance=tolerance,
    )
    if simplex_result.status != 0:
        return ExactPacketLPSolution(
            status=simplex_result.status,
            message=simplex_result.message,
            optimum=Fraction(0),
            coefficients=tuple(Fraction(0) for _ in model.atoms),
            residual=capacity,
            dual=tuple(Fraction(0) for _ in capacity),
            nonzero_coefficients=0,
        )

    max_objective = tuple(Fraction(1) for _ in model.atoms)
    coefficients, dual = _exact_primal_dual_from_basis(
        model.rows,
        capacity,
        max_objective,
        simplex_result.basis,
        simplex_result.nonbasis,
        atom_count,
    )
    residual = _residual_from_rows(model.rows, capacity, coefficients)
    optimum = sum(coefficients)
    _verify_lp_solution(model.rows, capacity, max_objective, coefficients, residual, dual, optimum)
    return ExactPacketLPSolution(
        status=0,
        message="optimal_exact_basis_verified",
        optimum=optimum,
        coefficients=coefficients,
        residual=residual,
        dual=dual,
        nonzero_coefficients=sum(1 for value in coefficients if value != 0),
    )


def automorphism_mappings(topology: K2Topology) -> tuple[dict[Vertex, Vertex], ...]:
    mappings: list[dict[Vertex, Vertex]] = []
    for left_targets in permutations(topology.left_leaves):
        for swap_right in (False, True):
            mapping = {vertex: vertex for vertex in topology.vertices}
            for source, target in zip(topology.left_leaves, left_targets):
                mapping[source] = target
            if swap_right:
                mapping["r"] = "s"
                mapping["s"] = "r"
            mappings.append(mapping)
    return tuple(mappings)


def apply_weight_transform(
    topology: K2Topology,
    weight: tuple[Fraction, ...],
    mapping: dict[Vertex, Vertex],
) -> tuple[Fraction, ...]:
    output = [Fraction(0) for _ in topology.vertices]
    for source_index, source in enumerate(topology.vertices):
        target = mapping[source]
        output[topology.order[target]] = weight[source_index]
    return tuple(output)


def canonical_weight_and_mapping(
    topology: K2Topology,
    weight: tuple[Fraction, ...],
    mappings: tuple[dict[Vertex, Vertex], ...] | None = None,
) -> tuple[tuple[Fraction, ...], dict[Vertex, Vertex]]:
    mappings = automorphism_mappings(topology) if mappings is None else mappings
    candidates = [
        (apply_weight_transform(topology, weight, mapping), mapping)
        for mapping in mappings
    ]
    return min(candidates, key=lambda item: item[0])


def transform_solution_from_canonical(
    system: H1CoordinateSystem,
    model: PacketLPModel,
    canonical_solution: ExactPacketLPSolution,
    mapping: dict[Vertex, Vertex],
    original_capacity: tuple[Fraction, ...],
) -> ExactPacketLPSolution:
    if canonical_solution.status != 0:
        return ExactPacketLPSolution(
            status=canonical_solution.status,
            message=canonical_solution.message,
            optimum=canonical_solution.optimum,
            coefficients=tuple(Fraction(0) for _ in model.atoms),
            residual=original_capacity,
            dual=tuple(Fraction(0) for _ in original_capacity),
            nonzero_coefficients=0,
        )

    coefficients = [Fraction(0) for _ in model.atoms]
    for original_index, atom in enumerate(model.atoms):
        transformed_signature = _transform_atom_signature(system, atom, mapping)
        canonical_index = model.atom_signature_index[transformed_signature]
        coefficients[original_index] = canonical_solution.coefficients[canonical_index]

    dual = [Fraction(0) for _ in system.variables]
    for original_index, variable in enumerate(system.variables):
        transformed_variable = _transform_variable(system, variable, mapping)
        dual[original_index] = canonical_solution.dual[
            system.variable_index[transformed_variable]
        ]

    coefficient_tuple = tuple(coefficients)
    residual = _residual_from_rows(model.rows, original_capacity, coefficient_tuple)
    message = canonical_solution.message
    if any(mapping[vertex] != vertex for vertex in system.topology.vertices):
        message = f"{message}_via_automorphism"
    return ExactPacketLPSolution(
        status=0,
        message=message,
        optimum=sum(coefficient_tuple),
        coefficients=coefficient_tuple,
        residual=residual,
        dual=tuple(dual),
        nonzero_coefficients=sum(1 for value in coefficient_tuple if value != 0),
    )


def build_universe_artifact(
    k: int,
    values: tuple[int, ...],
    *,
    tolerance: float = DEFAULT_TOLERANCE,
    stop_on_gap: bool = False,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    system = h1_coordinate_system(k)
    catalog = true_depth_catalog(system.topology)
    model = packet_lp_model(system)
    mappings = automorphism_mappings(system.topology)

    factorizations: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    solution_cache: dict[tuple[Fraction, ...], ExactPacketLPSolution] = {}
    max_denominator = 1
    zero_optimum_count = 0
    weight_count = 0

    for raw_weight in product(values, repeat=len(system.topology.vertices)):
        if not any(raw_weight):
            continue
        weight_count += 1
        weight = tuple(Fraction(value) for value in raw_weight)
        capacity = coordinate_capacity(system, weight)
        optimum = true_optimum(catalog, weight)
        canonical_weight, mapping = canonical_weight_and_mapping(
            system.topology,
            weight,
            mappings,
        )
        if optimum == 0:
            zero_optimum_count += 1
        if canonical_weight not in solution_cache:
            canonical_capacity = coordinate_capacity(system, canonical_weight)
            canonical_optimum = true_optimum(catalog, canonical_weight)
            if canonical_optimum != optimum:
                raise ValueError("automorphism changed true optimum")
            solution_cache[canonical_weight] = solve_packet_window_lp(
                model,
                canonical_capacity,
                tolerance=tolerance,
            )
        solution = transform_solution_from_canonical(
            system,
            model,
            solution_cache[canonical_weight],
            mapping,
            capacity,
        )
        if solution.status != 0:
            failure = {
                "id": f"w{weight_count:05d}",
                "status": "lp_solver_failure",
                "message": solution.message,
                "weights": weight_json(system.topology, weight),
                "true_optimum": rational_to_string(optimum),
            }
            failures.append(failure)
            if stop_on_gap:
                break
            continue

        if solution.optimum < optimum:
            failure = gap_witness_json(
                system,
                model,
                weight,
                optimum,
                solution,
                witness_id=f"gap_ds{k}2_w{weight_count:05d}",
            )
            failures.append(failure)
            if stop_on_gap:
                break
            continue
        if solution.optimum > optimum:
            raise ValueError(
                f"DS({k},2) packet-window LP exceeded true OPT for "
                f"{raw_weight}: packet={solution.optimum} true={optimum}"
            )

        for coefficient in solution.coefficients:
            max_denominator = max(max_denominator, coefficient.denominator)
        factorizations.append(
            factorization_entry_json(
                system,
                model,
                f"w{weight_count:05d}",
                weight,
                optimum,
                solution,
            )
        )

    artifact = {
        "schema": FACTORIZATION_SCHEMA,
        "topology": topology_json(system.topology),
        "universe": {
            "name": _universe_name(k, values),
            "values": list(values),
            "excludes_all_zero_weight": True,
            "weight_count": weight_count,
        },
        "h1_coordinate_system": coordinate_system_json(system),
        "true_depths": {
            "schedule_count": catalog.schedule_count,
            "depth_vector_count": catalog.depth_vector_count,
        },
        "packet_window": {
            "two_left_window_count": len(tuple(combinations(system.topology.left_leaves, 2))),
            "packet_atom_count": len(model.atoms),
            "packet_kind_counts": kind_counts(model.atoms),
            "packet_atoms": [atom_json(system, atom) for atom in model.atoms],
        },
        "factorization_count": len(factorizations),
        "canonical_lp_solve_count": len(solution_cache),
        "zero_true_optimum_count": zero_optimum_count,
        "max_certificate_denominator": max_denominator,
        "failures": failures,
        "factorizations": factorizations,
        "notes": [
            "Floating-point simplex is used only to locate candidate packet-window LP bases.",
            "Stored packet coefficients are exact rationals and verify coordinatewise against cap_w(S,v).",
            "This finite universe does not prove DS(k,2), DS(2,m), DS(k,m), public Golinsky/SKZ LP exactness, or general STT exactness.",
            "No H2, refined-Z, path-monotonicity, ancestry-transitivity, LCA-separation, or mixed-second-difference rows are used.",
        ],
    }
    return artifact, failures


def build_all_artifacts(
    *,
    tolerance: float = DEFAULT_TOLERANCE,
    stop_on_gap: bool = False,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], str]:
    ds32, ds32_failures = build_universe_artifact(
        3,
        (0, 1, 2),
        tolerance=tolerance,
        stop_on_gap=stop_on_gap,
    )
    ds42, ds42_failures = build_universe_artifact(
        4,
        (0, 1),
        tolerance=tolerance,
        stop_on_gap=stop_on_gap,
    )
    gap_witnesses = {
        "schema": GAP_SCHEMA,
        "status": "gaps_found" if ds32_failures or ds42_failures else "no_gaps_found",
        "required_universes": [
            {
                "topology": "DS(3,2)",
                "values": [0, 1, 2],
                "weight_count": ds32["universe"]["weight_count"],
                "failure_count": len(ds32_failures),
            },
            {
                "topology": "DS(4,2)",
                "values": [0, 1],
                "weight_count": ds42["universe"]["weight_count"],
                "failure_count": len(ds42_failures),
            },
        ],
        "witnesses": ds32_failures + ds42_failures,
        "scope_guard": (
            "A no-gap result here is exact finite packet-window evidence only; "
            "it is not an all-k theorem."
        ),
    }
    report = render_report(ds32, ds42, gap_witnesses)
    return ds32, ds42, gap_witnesses, report


def write_artifacts(
    *,
    ds32_path: Path = DEFAULT_DS32_FACTORIZATIONS,
    ds42_path: Path = DEFAULT_DS42_FACTORIZATIONS,
    gaps_path: Path = DEFAULT_GAP_WITNESSES,
    report_path: Path = DEFAULT_REPORT,
    tolerance: float = DEFAULT_TOLERANCE,
    stop_on_gap: bool = False,
) -> dict[str, Any]:
    ds32, ds32_failures = build_universe_artifact(
        3,
        (0, 1, 2),
        tolerance=tolerance,
        stop_on_gap=stop_on_gap,
    )
    ds32_path.parent.mkdir(parents=True, exist_ok=True)
    ds32_path.write_text(json.dumps(ds32, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    ds32_report = _slim_report_artifact(ds32)
    ds32_factorizations = ds32["factorization_count"]
    ds32_max_denominator = ds32["max_certificate_denominator"]
    del ds32

    ds42, ds42_failures = build_universe_artifact(
        4,
        (0, 1),
        tolerance=tolerance,
        stop_on_gap=stop_on_gap,
    )
    ds42_path.parent.mkdir(parents=True, exist_ok=True)
    ds42_path.write_text(json.dumps(ds42, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    ds42_report = _slim_report_artifact(ds42)
    ds42_factorizations = ds42["factorization_count"]
    ds42_max_denominator = ds42["max_certificate_denominator"]
    del ds42

    gaps = {
        "schema": GAP_SCHEMA,
        "status": "gaps_found" if ds32_failures or ds42_failures else "no_gaps_found",
        "required_universes": [
            {
                "topology": "DS(3,2)",
                "values": [0, 1, 2],
                "weight_count": ds32_report["universe"]["weight_count"],
                "failure_count": len(ds32_failures),
            },
            {
                "topology": "DS(4,2)",
                "values": [0, 1],
                "weight_count": ds42_report["universe"]["weight_count"],
                "failure_count": len(ds42_failures),
            },
        ],
        "witnesses": ds32_failures + ds42_failures,
        "scope_guard": (
            "A no-gap result here is exact finite packet-window evidence only; "
            "it is not an all-k theorem."
        ),
    }
    gaps_path.parent.mkdir(parents=True, exist_ok=True)
    gaps_path.write_text(json.dumps(gaps, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = render_report(ds32_report, ds42_report, gaps)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    return {
        "ds32": str(ds32_path),
        "ds42": str(ds42_path),
        "gaps": str(gaps_path),
        "report": str(report_path),
        "ds32_factorizations": ds32_factorizations,
        "ds42_factorizations": ds42_factorizations,
        "gap_witnesses": len(gaps["witnesses"]),
        "ds32_max_denominator": ds32_max_denominator,
        "ds42_max_denominator": ds42_max_denominator,
    }


def verify_artifact_files(
    ds32_path: Path = DEFAULT_DS32_FACTORIZATIONS,
    ds42_path: Path = DEFAULT_DS42_FACTORIZATIONS,
    gaps_path: Path = DEFAULT_GAP_WITNESSES,
) -> dict[str, Any]:
    with ds32_path.open("r", encoding="utf-8") as handle:
        ds32 = json.load(handle)
    with ds42_path.open("r", encoding="utf-8") as handle:
        ds42 = json.load(handle)
    with gaps_path.open("r", encoding="utf-8") as handle:
        gaps = json.load(handle)
    return verify_artifacts(ds32, ds42, gaps)


def verify_artifacts(
    ds32: dict[str, Any],
    ds42: dict[str, Any],
    gaps: dict[str, Any],
) -> dict[str, Any]:
    ds32_summary = verify_universe_artifact(ds32, expected_k=3, expected_values=(0, 1, 2))
    ds42_summary = verify_universe_artifact(ds42, expected_k=4, expected_values=(0, 1))
    if gaps.get("schema") != GAP_SCHEMA:
        raise ValueError("gap witness schema mismatch")
    expected_status = "no_gaps_found"
    if ds32_summary["failure_count"] or ds42_summary["failure_count"]:
        expected_status = "gaps_found"
    if gaps.get("status") != expected_status:
        raise ValueError("gap witness status mismatch")
    if len(gaps.get("witnesses", [])) != ds32_summary["failure_count"] + ds42_summary["failure_count"]:
        raise ValueError("gap witness count mismatch")
    return {
        "ds32_factorizations": ds32_summary["factorization_count"],
        "ds42_factorizations": ds42_summary["factorization_count"],
        "gap_witnesses": len(gaps.get("witnesses", [])),
        "ds32_max_denominator": ds32_summary["max_denominator"],
        "ds42_max_denominator": ds42_summary["max_denominator"],
    }


def verify_universe_artifact(
    artifact: dict[str, Any],
    *,
    expected_k: int,
    expected_values: tuple[int, ...],
) -> dict[str, Any]:
    if artifact.get("schema") != FACTORIZATION_SCHEMA:
        raise ValueError("factorization schema mismatch")
    if artifact["topology"]["k"] != expected_k:
        raise ValueError("topology k mismatch")
    if tuple(artifact["universe"]["values"]) != expected_values:
        raise ValueError("universe values mismatch")

    system = h1_coordinate_system(expected_k)
    catalog = true_depth_catalog(system.topology)
    model = packet_lp_model(system)
    _verify_coordinate_catalog(system, artifact["h1_coordinate_system"])
    _verify_atom_catalog(system, model.atoms, artifact["packet_window"]["packet_atoms"])

    expected_weights = [
        tuple(Fraction(value) for value in raw_weight)
        for raw_weight in product(expected_values, repeat=len(system.topology.vertices))
        if any(raw_weight)
    ]
    if artifact["universe"]["weight_count"] != len(expected_weights):
        raise ValueError("universe weight count mismatch")
    entries = artifact.get("factorizations", [])
    failures = artifact.get("failures", [])
    if len(entries) + len(failures) != len(expected_weights):
        raise ValueError("factorization/failure count does not cover the universe")

    atom_index_by_id = {atom.atom_id: index for index, atom in enumerate(model.atoms)}
    seen_weights: set[tuple[Fraction, ...]] = set()
    max_denominator = 1
    zero_true_optimum_count = 0
    for entry in entries:
        weight = weight_from_json(system.topology, entry["weights"])
        if weight in seen_weights:
            raise ValueError(f"duplicate factorization weight {weight}")
        seen_weights.add(weight)
        optimum = true_optimum(catalog, weight)
        if optimum == 0:
            zero_true_optimum_count += 1
        if parse_fraction(entry["true_optimum"], "true_optimum") != optimum:
            raise ValueError(f"{entry['id']}: true optimum mismatch")
        if parse_fraction(entry["packet_mass"], "packet_mass") != optimum:
            raise ValueError(f"{entry['id']}: packet mass mismatch")
        coefficients = coefficients_from_entries(
            model.atoms,
            atom_index_by_id,
            entry["nonzero_packet_coefficients"],
            entry["id"],
        )
        for coefficient in coefficients:
            max_denominator = max(max_denominator, coefficient.denominator)
        if sum(coefficients) != optimum:
            raise ValueError(f"{entry['id']}: coefficient mass does not equal true OPT")
        capacity = coordinate_capacity(system, weight)
        residual = _residual_from_rows(model.rows, capacity, coefficients)
        if min(residual, default=Fraction(0)) < 0:
            raise ValueError(f"{entry['id']}: negative residual coordinate")
        if sum(1 for value in residual if value != 0) != entry["residual_nonzero_count"]:
            raise ValueError(f"{entry['id']}: residual nonzero count mismatch")
        if rational_to_string(min(residual, default=Fraction(0))) != entry["minimum_residual_coordinate"]:
            raise ValueError(f"{entry['id']}: residual minimum mismatch")
        if max_denominator > artifact["max_certificate_denominator"]:
            raise ValueError("max denominator metadata is too small")

    failed_weights = {
        weight_from_json(system.topology, entry["weights"])
        for entry in failures
        if "weights" in entry
    }
    if set(expected_weights) != seen_weights | failed_weights:
        raise ValueError("artifact weight set mismatch")
    if zero_true_optimum_count != artifact["zero_true_optimum_count"]:
        raise ValueError("zero true optimum count mismatch")
    if artifact["factorization_count"] != len(entries):
        raise ValueError("factorization_count mismatch")
    if artifact["max_certificate_denominator"] != max_denominator:
        raise ValueError("max denominator mismatch")
    return {
        "factorization_count": len(entries),
        "failure_count": len(failures),
        "max_denominator": max_denominator,
        "zero_true_optimum_count": zero_true_optimum_count,
    }


def factorization_entry_json(
    system: H1CoordinateSystem,
    model: PacketLPModel,
    entry_id: str,
    weight: tuple[Fraction, ...],
    optimum: Fraction,
    solution: ExactPacketLPSolution,
) -> dict[str, Any]:
    if solution.optimum != optimum:
        raise ValueError("factorization entry requires exact packet-window closure")
    residual = _residual_from_rows(
        model.rows,
        coordinate_capacity(system, weight),
        solution.coefficients,
    )
    if min(residual, default=Fraction(0)) < 0:
        raise ValueError("negative residual in factorization entry")
    return {
        "id": entry_id,
        "weights": weight_json(system.topology, weight),
        "support": sum(1 for value in weight if value != 0),
        "true_optimum": rational_to_string(optimum),
        "packet_mass": rational_to_string(sum(solution.coefficients)),
        "packet_window_lp_status": solution.message,
        "nonzero_packet_coefficients": [
            {
                "atom_id": atom.atom_id,
                "kind": atom.kind,
                "window": list(atom.window),
                "coefficient": rational_to_string(solution.coefficients[index]),
            }
            for index, atom in enumerate(model.atoms)
            if solution.coefficients[index] != 0
        ],
        "residual_nonzero_count": sum(1 for value in residual if value != 0),
        "minimum_residual_coordinate": rational_to_string(min(residual, default=Fraction(0))),
    }


def gap_witness_json(
    system: H1CoordinateSystem,
    model: PacketLPModel,
    weight: tuple[Fraction, ...],
    true_opt: Fraction,
    solution: ExactPacketLPSolution,
    *,
    witness_id: str,
) -> dict[str, Any]:
    residual = solution.residual
    binding_terms = [
        term
        for term in nonzero_or_zero_terms(system, residual, zeros_only=True)
        if term["coordinate"] in {
            "a,b|a",
            "a,b|b",
            "b,r|b",
            "b,s|b",
            *{f"a,{leaf}|a" for leaf in system.topology.left_leaves},
        }
    ]
    return {
        "id": witness_id,
        "status": "packet_window_gap",
        "topology": f"DS({system.topology.k},2)",
        "weights": weight_json(system.topology, weight),
        "true_optimum": rational_to_string(true_opt),
        "packet_window_optimum": rational_to_string(solution.optimum),
        "deficit": rational_to_string(true_opt - solution.optimum),
        "binding_or_exhausted_focus_coordinates": binding_terms,
        "nonzero_packet_coefficients": [
            {
                "atom_id": atom.atom_id,
                "kind": atom.kind,
                "window": list(atom.window),
                "coefficient": rational_to_string(solution.coefficients[index]),
            }
            for index, atom in enumerate(model.atoms)
            if solution.coefficients[index] != 0
        ],
        "dual_upper_bound_terms": nonzero_terms(system, solution.dual),
    }


def render_report(
    ds32: dict[str, Any],
    ds42: dict[str, Any],
    gaps: dict[str, Any],
) -> str:
    has_gap = gaps["status"] == "gaps_found"
    result = (
        "Exact rational packet-window gaps were found."
        if has_gap
        else "No packet-window gap was found in either required finite universe."
    )
    lines = [
        "# DS(3,2)/DS(4,2) Packet-Window Capacity Hardening",
        "",
        "## Result",
        "",
        result,
        "",
        "The closure claim here is finite and certificate-backed only for the declared weight universes. It does not prove DS(k,2), DS(2,m), DS(k,m), public Golinsky/SKZ LP exactness, or general STT exactness.",
        "",
        "Packet-window closure is also separate from full H1 exactness: by the prompt-provided implications, a mass-`OPT` packet-window certificate gives `Pkt_{k,2}(w)=OPT_{k,2}(w)` for that tested weight, and then H1 is exact for that weight.",
        "",
        "## Finite Universes",
        "",
        _universe_report_line(ds32),
        _universe_report_line(ds42),
        "",
        "## Construction",
        "",
        "- Coordinates are H1 first-hit variables `z[S,v]` for connected `S` and `v in S`.",
        "- Capacities are exact strict-path coefficients `cap_w(S,v)=sum_{x != v : P(x,v)=S} w_x`.",
        "- True `OPT` values come from exact recursive-search-tree depth-vector enumeration.",
        "- Packet atoms are the DS(2,2) `Sigma/Lambda/Gamma/Delta/Omega/Pi` atoms embedded into every two-left window.",
        "- Floating-point simplex is used only to locate candidate LP bases; stored coefficients are exact rationals and are verified coordinatewise.",
        "",
        "## Scope Guardrails",
        "",
        "This hardening uses only H1 coordinate capacities and embedded DS(2,2) packet atoms. It does not use H2, refined-Z, path-monotonicity, ancestry-transitivity, LCA-separation, or mixed-second-difference rows.",
        "",
        "Raw `Sigma` atoms remain essential certificate bookkeeping inherited from DS(2,2); this report does not promote them to a conceptual all-k theorem.",
        "",
        "## Artifacts",
        "",
        f"- DS(3,2) ternary factorizations: `{DEFAULT_DS32_FACTORIZATIONS}`.",
        f"- DS(4,2) binary factorizations: `{DEFAULT_DS42_FACTORIZATIONS}`.",
        f"- Gap witnesses: `{DEFAULT_GAP_WITNESSES}`.",
        f"- Tests: `tests/test_ds32_ds42_packet_window_capacity.py`.",
        "",
        "## Verification Commands",
        "",
        "```powershell",
        "python -m src.ds22_simplex_augmented_packet_conic --verify",
        "python -m unittest tests.test_ds22_simplex_augmented_packet_conic",
        "python -m src.ds32_ds42_packet_window_capacity --verify",
        "python -m pytest tests/test_ds32_ds42_packet_window_capacity.py",
        "```",
    ]
    if has_gap:
        lines.extend(
            [
                "",
                "## Gap Witnesses",
                "",
                f"`{len(gaps['witnesses'])}` exact packet-window gap witness(es) are stored in `{DEFAULT_GAP_WITNESSES}`.",
                "All-k proof work should stop until these witnesses are analyzed.",
            ]
        )
    else:
        lines.extend(
            [
                "",
                "## Next Proof-Work Prompt",
                "",
                "Try to prove or refute the all-k DS(k,2) packet-window gluing conjecture using only the H1 capacity LP and the embedded DS(2,2) `Sigma/Lambda/Gamma/Delta/Omega/Pi` atoms. Treat the DS(3,2) ternary and DS(4,2) binary certificates as finite evidence, not as theorem proof.",
            ]
        )
    return "\n".join(lines) + "\n"


def _slim_report_artifact(artifact: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in artifact.items()
        if key not in {"factorizations", "h1_coordinate_system"}
    }


def weight_json(topology: K2Topology, weight: Iterable[Fraction | int]) -> dict[str, str]:
    return {
        vertex: rational_to_string(value)
        for vertex, value in zip(topology.vertices, tuple(weight))
    }


def weight_from_json(topology: K2Topology, weights: dict[str, Any]) -> tuple[Fraction, ...]:
    return tuple(parse_fraction(weights[vertex], f"weights.{vertex}") for vertex in topology.vertices)


def variable_key(variable: Variable) -> str:
    component, root = variable
    return f"{component_key(component)}|{root}"


def component_key(component: Component) -> str:
    return ",".join(component)


def topology_json(topology: K2Topology) -> dict[str, Any]:
    return {
        "family": "DS(k,2)",
        "k": topology.k,
        "vertices": list(topology.vertices),
        "left_leaves": list(topology.left_leaves),
        "right_leaves": list(topology.right_leaves),
        "edges": [list(edge) for edge in topology.edges],
    }


def coordinate_system_json(system: H1CoordinateSystem) -> dict[str, Any]:
    return {
        "vertices": list(system.topology.vertices),
        "definition": "H1 coordinates z[S,v] for connected S and v in S",
        "connected_subset_count": len(system.connected_subsets),
        "variable_count": len(system.variables),
        "variables": [
            {
                "index": index,
                "key": variable_key(variable),
                "component": list(variable[0]),
                "root": variable[1],
            }
            for index, variable in enumerate(system.variables)
        ],
    }


def atom_json(system: H1CoordinateSystem, atom: PacketAtom) -> dict[str, Any]:
    return {
        "id": atom.atom_id,
        "kind": atom.kind,
        "window": list(atom.window),
        "parameters": atom.parameters,
        "nonzero_terms": nonzero_terms(system, atom.vector),
    }


def kind_counts(atoms: tuple[PacketAtom, ...]) -> dict[str, int]:
    return dict(Counter(atom.kind for atom in atoms))


def nonzero_terms(
    system: H1CoordinateSystem,
    vector: tuple[Fraction, ...],
) -> list[dict[str, Any]]:
    return [
        {
            "coordinate": variable_key(system.variables[index]),
            "component": list(system.variables[index][0]),
            "root": system.variables[index][1],
            "value": rational_to_string(value),
        }
        for index, value in enumerate(vector)
        if value != 0
    ]


def nonzero_or_zero_terms(
    system: H1CoordinateSystem,
    vector: tuple[Fraction, ...],
    *,
    zeros_only: bool = False,
) -> list[dict[str, Any]]:
    terms: list[dict[str, Any]] = []
    for index, value in enumerate(vector):
        if zeros_only and value != 0:
            continue
        if not zeros_only and value == 0:
            continue
        terms.append(
            {
                "coordinate": variable_key(system.variables[index]),
                "component": list(system.variables[index][0]),
                "root": system.variables[index][1],
                "value": rational_to_string(value),
            }
        )
    return terms


def coefficients_from_entries(
    atoms: tuple[PacketAtom, ...],
    atom_index_by_id: dict[str, int],
    entries: list[dict[str, Any]],
    entry_id: str,
) -> tuple[Fraction, ...]:
    coefficients = [Fraction(0) for _ in atoms]
    seen: set[str] = set()
    for coefficient_entry in entries:
        atom_id = coefficient_entry.get("atom_id")
        if atom_id not in atom_index_by_id:
            raise ValueError(f"{entry_id}: unknown packet atom {atom_id}")
        if atom_id in seen:
            raise ValueError(f"{entry_id}: duplicate coefficient for {atom_id}")
        seen.add(atom_id)
        atom = atoms[atom_index_by_id[atom_id]]
        if coefficient_entry.get("kind") != atom.kind:
            raise ValueError(f"{entry_id}: atom kind mismatch for {atom_id}")
        value = parse_fraction(coefficient_entry.get("coefficient"), f"{entry_id}.{atom_id}")
        if value <= 0:
            raise ValueError(f"{entry_id}: listed packet coefficient must be positive")
        coefficients[atom_index_by_id[atom_id]] = value
    return tuple(coefficients)


def _enumerate_component_depths(
    topology: K2Topology,
    component: Component,
    depth: int,
) -> Iterable[dict[Vertex, int]]:
    component = canonical_component(topology, component)
    for root in component:
        child_components = connected_components_after_removing(topology, root, component)
        child_options = [
            tuple(_enumerate_component_depths(topology, child, depth + 1))
            for child in child_components
        ]
        for children in product(*child_options):
            depths = {root: depth}
            for child in children:
                depths.update(child)
            yield depths


def _window_packet_atoms(
    system: H1CoordinateSystem,
    left_pair: tuple[Vertex, Vertex],
) -> list[PacketAtom]:
    topology = system.topology
    li, lj = left_pair
    window = tuple(sorted(left_pair, key=topology.order.__getitem__))
    window_vertices = {"a", "b", *topology.right_leaves, *window}
    variable_count = len(system.variables)
    atoms: list[PacketAtom] = []

    for component in system.connected_subsets:
        if set(component).issubset(window_vertices):
            vector = _zero_vector(variable_count)
            for root in component:
                _add_term(vector, system, component, root)
            atoms.append(
                PacketAtom(
                    atom_id=_atom_id(window, f"Sigma[{component_key(component)}]"),
                    kind="Sigma",
                    window=window,
                    vector=tuple(vector),
                    parameters={"S": list(component)},
                )
            )

    left_spine = _component(topology, "a", li, lj)
    for ell in window:
        source = _component(topology, "a", ell)
        vector = _sigma_vector(system, left_spine)
        _add_term(vector, system, source, "a")
        _add_term(vector, system, left_spine, "a", -1)
        atoms.append(
            PacketAtom(
                atom_id=_atom_id(window, f"Lambda[{ell}]"),
                kind="Lambda",
                window=window,
                vector=tuple(vector),
                parameters={"ell": ell, "L": list(left_spine), "source": list(source)},
            )
        )

    right_spine = _component(topology, "b", "r", "s")
    for x in topology.right_leaves:
        source = _component(topology, "b", x)
        vector = _sigma_vector(system, right_spine)
        _add_term(vector, system, source, "b")
        _add_term(vector, system, right_spine, "b", -1)
        atoms.append(
            PacketAtom(
                atom_id=_atom_id(window, f"Gamma[{x}]"),
                kind="Gamma",
                window=window,
                vector=tuple(vector),
                parameters={"x": x, "R": list(right_spine), "source": list(source)},
            )
        )

    for ell in window:
        cap = _component(topology, "a", "b", ell)
        for source in (_component(topology, "a", "b"), _component(topology, "a", ell)):
            vector = _sigma_vector(system, cap)
            _add_term(vector, system, source, "a")
            _add_term(vector, system, cap, "a", -1)
            atoms.append(
                PacketAtom(
                    atom_id=_atom_id(window, f"Delta[{ell};P={component_key(source)}]"),
                    kind="Delta",
                    window=window,
                    vector=tuple(vector),
                    parameters={"ell": ell, "D": list(cap), "P": list(source)},
                )
            )

    for x in topology.right_leaves:
        cap = _component(topology, "a", "b", x)
        for source in (_component(topology, "a", "b"), _component(topology, "b", x)):
            vector = _sigma_vector(system, cap)
            _add_term(vector, system, source, "b")
            _add_term(vector, system, cap, "b", -1)
            atoms.append(
                PacketAtom(
                    atom_id=_atom_id(window, f"Omega[{x};Q={component_key(source)}]"),
                    kind="Omega",
                    window=window,
                    vector=tuple(vector),
                    parameters={"x": x, "C": list(cap), "Q": list(source)},
                )
            )

    for x in topology.right_leaves:
        for ell in window:
            cell = _component(topology, "a", "b", x, ell)
            left_sources = (
                _component(topology, "a", "b"),
                _component(topology, "a", ell),
                _component(topology, "a", "b", x),
            )
            right_sources = (
                _component(topology, "a", "b"),
                _component(topology, "b", x),
                _component(topology, "a", "b", ell),
            )
            for left_source in left_sources:
                for right_source in right_sources:
                    vector = _sigma_vector(system, cell)
                    _add_term(vector, system, left_source, "a")
                    _add_term(vector, system, cell, "a", -1)
                    _add_term(vector, system, right_source, "b")
                    _add_term(vector, system, cell, "b", -1)
                    atoms.append(
                        PacketAtom(
                            atom_id=_atom_id(
                                window,
                                (
                                    f"Pi[{x},{ell};P={component_key(left_source)};"
                                    f"Q={component_key(right_source)}]"
                                ),
                            ),
                            kind="Pi",
                            window=window,
                            vector=tuple(vector),
                            parameters={
                                "x": x,
                                "ell": ell,
                                "U": list(cell),
                                "P": list(left_source),
                                "Q": list(right_source),
                            },
                        )
                    )

    return atoms


def _component(topology: K2Topology, *vertices: Vertex) -> Component:
    component = canonical_component(topology, vertices)
    if not is_connected(topology, component):
        raise ValueError(f"not connected: {component}")
    return component


def _atom_id(window: tuple[Vertex, Vertex], local_id: str) -> str:
    return f"W[{window[0]},{window[1]}]::{local_id}"


def _atom_signature(atom: PacketAtom) -> tuple[str, tuple[Vertex, Vertex], tuple[Fraction, ...]]:
    return (atom.kind, atom.window, atom.vector)


def _transform_atom_signature(
    system: H1CoordinateSystem,
    atom: PacketAtom,
    mapping: dict[Vertex, Vertex],
) -> tuple[str, tuple[Vertex, Vertex], tuple[Fraction, ...]]:
    transformed_window = tuple(
        sorted((mapping[vertex] for vertex in atom.window), key=system.topology.order.__getitem__)
    )
    return (
        atom.kind,
        transformed_window,
        _transform_vector(system, atom.vector, mapping),
    )


def _transform_vector(
    system: H1CoordinateSystem,
    vector: tuple[Fraction, ...],
    mapping: dict[Vertex, Vertex],
) -> tuple[Fraction, ...]:
    output = [Fraction(0) for _ in system.variables]
    for index, value in enumerate(vector):
        if value == 0:
            continue
        transformed_variable = _transform_variable(system, system.variables[index], mapping)
        output[system.variable_index[transformed_variable]] += value
    return tuple(output)


def _transform_variable(
    system: H1CoordinateSystem,
    variable: Variable,
    mapping: dict[Vertex, Vertex],
) -> Variable:
    component, root = variable
    return (_transform_component(system.topology, component, mapping), mapping[root])


def _transform_component(
    topology: K2Topology,
    component: Component,
    mapping: dict[Vertex, Vertex],
) -> Component:
    return canonical_component(topology, (mapping[vertex] for vertex in component))


def _zero_vector(length: int) -> list[Fraction]:
    return [Fraction(0) for _ in range(length)]


def _sigma_vector(system: H1CoordinateSystem, component: Component) -> list[Fraction]:
    vector = _zero_vector(len(system.variables))
    for root in component:
        _add_term(vector, system, component, root)
    return vector


def _add_term(
    vector: list[Fraction],
    system: H1CoordinateSystem,
    component: Component,
    root: Vertex,
    coefficient: Fraction | int = 1,
) -> None:
    vector[system.variable_index[(component, root)]] += Fraction(coefficient)


def _residual_from_rows(
    rows: tuple[SparseRow, ...],
    capacity: tuple[Fraction, ...],
    coefficients: tuple[Fraction, ...],
) -> tuple[Fraction, ...]:
    return tuple(
        capacity[row_index]
        - sum(coefficient * coefficients[index] for index, coefficient in row.items())
        for row_index, row in enumerate(rows)
    )


def _exact_primal_dual_from_basis(
    rows: tuple[SparseRow, ...],
    rhs: tuple[Fraction, ...],
    max_objective: tuple[Fraction, ...],
    basis: tuple[int, ...],
    nonbasis: tuple[int, ...],
    variable_count: int,
) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    if -1 in basis:
        raise ValueError("cannot reconstruct exact packet LP with artificial variable in basis")
    row_count = len(rows)
    basis_set = set(basis)
    basic_originals = [index for index in basis if 0 <= index < variable_count]
    nonbasic_slack_rows = [
        index - variable_count
        for index in range(variable_count, variable_count + row_count)
        if index not in basis_set
    ]
    if len(basic_originals) != len(nonbasic_slack_rows):
        raise ValueError(
            "basis shape is not reconstructible: "
            f"{len(basic_originals)} basic originals vs "
            f"{len(nonbasic_slack_rows)} nonbasic slacks"
        )
    matrix = [
        [rows[row].get(variable, Fraction(0)) for variable in basic_originals]
        for row in nonbasic_slack_rows
    ]
    tight_rhs = [rhs[row] for row in nonbasic_slack_rows]
    basic_values = _solve_square_linear_system(matrix, tight_rhs) if basic_originals else []
    coefficients = [Fraction(0) for _ in range(variable_count)]
    for variable, value in zip(basic_originals, basic_values):
        coefficients[variable] = value

    dual_rows = [
        index - variable_count
        for index in nonbasis
        if variable_count <= index < variable_count + row_count
    ]
    dual_system = [
        [rows[row].get(variable, Fraction(0)) for row in dual_rows]
        for variable in basic_originals
    ]
    dual_values = (
        _solve_square_linear_system(
            dual_system,
            [max_objective[variable] for variable in basic_originals],
        )
        if basic_originals
        else []
    )
    dual = [Fraction(0) for _ in range(row_count)]
    for row, value in zip(dual_rows, dual_values):
        dual[row] = value
    return tuple(coefficients), tuple(dual)


def _verify_lp_solution(
    rows: tuple[SparseRow, ...],
    rhs: tuple[Fraction, ...],
    max_objective: tuple[Fraction, ...],
    coefficients: tuple[Fraction, ...],
    residual: tuple[Fraction, ...],
    dual: tuple[Fraction, ...],
    optimum: Fraction,
) -> None:
    if min(coefficients, default=Fraction(0)) < 0:
        raise ValueError("packet LP primal has a negative coefficient")
    if min(residual, default=Fraction(0)) < 0:
        raise ValueError("packet LP primal has a negative residual")
    if min(dual, default=Fraction(0)) < 0:
        raise ValueError("packet LP dual has a negative coordinate price")
    for row, row_rhs in enumerate(rhs):
        lhs = sum(
            rows[row].get(variable, Fraction(0)) * coefficients[variable]
            for variable in range(len(coefficients))
        )
        if row_rhs - lhs != residual[row]:
            raise ValueError("packet LP residual mismatch")
    for variable, coefficient in enumerate(max_objective):
        lhs = sum(rows[row].get(variable, Fraction(0)) * dual[row] for row in range(len(rows)))
        if lhs < coefficient:
            raise ValueError("packet LP dual is not feasible")
    primal_value = sum(max_objective[index] * coefficients[index] for index in range(len(coefficients)))
    dual_value = sum(rhs[row] * dual[row] for row in range(len(rows)))
    if primal_value != optimum or dual_value != optimum:
        raise ValueError(
            f"packet LP strong-duality mismatch: primal={primal_value}, "
            f"dual={dual_value}, optimum={optimum}"
        )


def _verify_coordinate_catalog(system: H1CoordinateSystem, catalog: dict[str, Any]) -> None:
    expected = coordinate_system_json(system)
    for key in ("vertices", "connected_subset_count", "variable_count"):
        if catalog.get(key) != expected[key]:
            raise ValueError(f"H1 coordinate catalog {key} mismatch")
    if catalog.get("variables") != expected["variables"]:
        raise ValueError("H1 coordinate variable catalog mismatch")


def _verify_atom_catalog(
    system: H1CoordinateSystem,
    atoms: tuple[PacketAtom, ...],
    catalog: list[dict[str, Any]],
) -> None:
    catalog_by_id = {entry["id"]: entry for entry in catalog}
    if set(catalog_by_id) != {atom.atom_id for atom in atoms}:
        raise ValueError("packet atom catalog id set mismatch")
    if len(catalog_by_id) != len(catalog):
        raise ValueError("packet atom catalog has duplicate ids")
    index_by_key = {variable_key(variable): index for index, variable in enumerate(system.variables)}
    for atom in atoms:
        entry = catalog_by_id[atom.atom_id]
        if entry.get("kind") != atom.kind:
            raise ValueError(f"packet atom kind mismatch for {atom.atom_id}")
        vector = [Fraction(0) for _ in system.variables]
        for term in entry.get("nonzero_terms", []):
            vector[index_by_key[term["coordinate"]]] = parse_fraction(term["value"], term["coordinate"])
        if tuple(vector) != atom.vector:
            raise ValueError(f"packet atom vector mismatch for {atom.atom_id}")


def _universe_name(k: int, values: tuple[int, ...]) -> str:
    if k == 3 and values == (0, 1, 2):
        return "DS(3,2) full ternary cube {0,1,2}^7 minus zero"
    if k == 4 and values == (0, 1):
        return "DS(4,2) full binary cube {0,1}^8 minus zero"
    return f"DS({k},2) values {values} minus zero"


def _universe_report_line(artifact: dict[str, Any]) -> str:
    topology = artifact["topology"]
    return (
        f"- `DS({topology['k']},2)`: `{artifact['factorization_count']}` "
        f"closed weights in `{artifact['universe']['name']}`; "
        f"true schedules `{artifact['true_depths']['schedule_count']}`, "
        f"deduplicated depth vectors `{artifact['true_depths']['depth_vector_count']}`, "
        f"packet atoms `{artifact['packet_window']['packet_atom_count']}`, "
        f"canonical LP solves `{artifact['canonical_lp_solve_count']}`, "
        f"max denominator `{artifact['max_certificate_denominator']}`, "
        f"failures `{len(artifact['failures'])}`."
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m src.ds32_ds42_packet_window_capacity"
    )
    parser.add_argument("--ds32", type=Path, default=DEFAULT_DS32_FACTORIZATIONS)
    parser.add_argument("--ds42", type=Path, default=DEFAULT_DS42_FACTORIZATIONS)
    parser.add_argument("--gaps", type=Path, default=DEFAULT_GAP_WITNESSES)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--verify", action="store_true", help="verify existing artifacts")
    parser.add_argument("--stop-on-gap", action="store_true")
    parser.add_argument("--tolerance", type=float, default=DEFAULT_TOLERANCE)
    args = parser.parse_args(argv)

    if args.verify:
        summary = verify_artifact_files(args.ds32, args.ds42, args.gaps)
        print(
            "verified ds32/ds42 packet-window capacity artifacts: "
            f"ds32_factorizations={summary['ds32_factorizations']} "
            f"ds42_factorizations={summary['ds42_factorizations']} "
            f"gap_witnesses={summary['gap_witnesses']} "
            f"ds32_max_denominator={summary['ds32_max_denominator']} "
            f"ds42_max_denominator={summary['ds42_max_denominator']}"
        )
        return 0

    result = write_artifacts(
        ds32_path=args.ds32,
        ds42_path=args.ds42,
        gaps_path=args.gaps,
        report_path=args.report,
        tolerance=args.tolerance,
        stop_on_gap=args.stop_on_gap,
    )
    print(
        "wrote ds32/ds42 packet-window capacity artifacts: "
        f"ds32={result['ds32']} "
        f"ds42={result['ds42']} "
        f"gaps={result['gaps']} "
        f"report={result['report']} "
        f"ds32_factorizations={result['ds32_factorizations']} "
        f"ds42_factorizations={result['ds42_factorizations']} "
        f"gap_witnesses={result['gap_witnesses']} "
        f"ds32_max_denominator={result['ds32_max_denominator']} "
        f"ds42_max_denominator={result['ds42_max_denominator']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
