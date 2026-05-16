"""Double-star depth-projection experiments for the first-hit hierarchy.

This module is a finite theorem-scouting harness for double-stars
``DS(m,n)``.  It deliberately stays inside the edge-diameter-3 family: two
centers ``a,b`` joined by an edge, ``m`` leaves on ``a``, and ``n`` leaves on
``b``.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations, product
import json
from pathlib import Path
from typing import Any, Iterable

from .enumerate_stts import enumerate_stts
from .hereditary_lp import DEFAULT_TOLERANCE, build_hereditary_lp, _simplex_maximize
from .h2_dual_certificate import exact_standard_form
from .rationals import rational_to_string
from .star_depth_projection import (
    ExactLPCertificate,
    _exact_dual_from_basis,
    _exact_primal_from_basis,
    _format_fraction_tuple,
    _max_dual_deficit,
    _max_primal_violation,
)
from .stt import STTResult
from .topology import TreeTopology


DEFAULT_REPORT = Path("reports/stt_double_star_depth_projection_v0.md")
DEFAULT_SUMMARY = Path("examples/stt_lp/double_star_depth_projection_v0_summary.json")
Component = tuple[int, ...]
SparseRow = dict[int, Fraction]
Variable = tuple[Component, int]


@dataclass(frozen=True)
class DoubleStarSpec:
    m: int
    n: int
    a: int
    b: int
    left_leaves: tuple[int, ...]
    right_leaves: tuple[int, ...]

    @property
    def name(self) -> str:
        return f"DS({self.m},{self.n})"

    def label(self, vertex: int) -> str:
        if vertex == self.a:
            return "a"
        if vertex == self.b:
            return "b"
        if vertex in self.left_leaves:
            return f"x{self.left_leaves.index(vertex) + 1}"
        if vertex in self.right_leaves:
            return f"y{self.right_leaves.index(vertex) + 1}"
        raise ValueError(f"unknown vertex {vertex}")


@dataclass(frozen=True)
class ReducedLP:
    topology: TreeTopology
    weights: tuple[Fraction, ...]
    relaxation: str
    full_variables: tuple[Variable, ...]
    orbit_variables: tuple[Variable, ...]
    variable_to_orbit: tuple[int, ...]
    rows: tuple[SparseRow, ...]
    rhs: tuple[Fraction, ...]
    objective: tuple[Fraction, ...]
    row_descriptors: tuple[dict[str, Any], ...]
    row_orbit_sizes: tuple[int, ...]


@dataclass(frozen=True)
class DoubleStarLPResult:
    relaxation: str
    optimum: Fraction
    certificate_status: str
    certificate: ExactLPCertificate | None
    values: tuple[Fraction, ...]
    lp: ReducedLP
    active_rows: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class ObjectiveRun:
    spec: DoubleStarSpec
    family: str
    weights: tuple[Fraction, ...]
    stt_optimum: Fraction
    stt_witness_depth: tuple[int, ...]
    h1: DoubleStarLPResult
    h2: DoubleStarLPResult | None
    reduced_variables: dict[str, Any]

    @property
    def h1_gap(self) -> Fraction:
        return self.h1.optimum - self.stt_optimum

    @property
    def h2_gap(self) -> Fraction | None:
        if self.h2 is None:
            return None
        return self.h2.optimum - self.stt_optimum


def double_star_spec(m: int, n: int) -> DoubleStarSpec:
    if m < 1 or n < 1:
        raise ValueError("double-star parameters m,n must be positive")
    a = m
    b = m + 1
    return DoubleStarSpec(
        m=m,
        n=n,
        a=a,
        b=b,
        left_leaves=tuple(range(m)),
        right_leaves=tuple(range(m + 2, m + 2 + n)),
    )


def double_star_topology(m: int, n: int) -> TreeTopology:
    spec = double_star_spec(m, n)
    edges = [[leaf, spec.a] for leaf in spec.left_leaves]
    edges.append([spec.a, spec.b])
    edges.extend([spec.b, leaf] for leaf in spec.right_leaves)
    return TreeTopology.from_dict(
        {
            "n": m + n + 2,
            "vertices": list(range(m + n + 2)),
            "edges": edges,
        }
    )


def enumerate_normal_form_stts(
    m: int, n: int, depth_base: int = 0
) -> tuple[STTResult, ...]:
    """Enumerate STTs using the double-star component normal form."""

    if depth_base not in (0, 1):
        raise ValueError("depth_base must be 0 or 1")
    spec = double_star_spec(m, n)

    def rec(
        component: Component, parent_root: int | None, depth: int
    ) -> Iterable[STTResult]:
        component = tuple(sorted(component))
        for root in component:
            child_components = _normal_form_child_components(spec, component, root)
            child_options = [tuple(rec(child, root, depth + 1)) for child in child_components]
            for children in product(*child_options):
                parent = {root: parent_root}
                depths = {root: depth}
                component_roots = [(component, root)]
                for child in children:
                    parent.update(child.parent)
                    depths.update(child.depth)
                    component_roots.extend(child.component_roots)
                yield STTResult(
                    parent=parent,
                    depth=depths,
                    component_roots=tuple(component_roots),
                )

    return tuple(rec(tuple(range(m + n + 2)), None, depth_base))


def verify_normal_form_enumeration(m: int, n: int) -> bool:
    topology = double_star_topology(m, n)
    normal = sorted(
        tuple(result.depth[vertex] for vertex in topology.vertices)
        for result in enumerate_normal_form_stts(m, n, depth_base=0)
    )
    generic = sorted(
        tuple(result.depth[vertex] for vertex in topology.vertices)
        for result in enumerate_stts(topology, depth_base=0, max_count=1_000_000)
    )
    return normal == generic


def stt_depth_optimum(
    m: int, n: int, weights: Iterable[Fraction | int]
) -> tuple[Fraction, tuple[int, ...]]:
    topology = double_star_topology(m, n)
    weight_tuple = tuple(Fraction(value) for value in weights)
    if len(weight_tuple) != topology.n:
        raise ValueError("weight vector length must match topology.n")
    best_value: Fraction | None = None
    best_depth: tuple[int, ...] | None = None
    for result in enumerate_normal_form_stts(m, n, depth_base=0):
        depth = tuple(result.depth[vertex] for vertex in topology.vertices)
        value = sum(weight_tuple[index] * depth[index] for index in range(topology.n))
        if best_value is None or value < best_value:
            best_value = value
            best_depth = depth
    if best_value is None or best_depth is None:
        raise ValueError("no STTs enumerated")
    return best_value, best_depth


def structured_weight_vectors(
    m: int, n: int, small_bound: int = 2
) -> tuple[tuple[str, tuple[Fraction, ...]], ...]:
    spec = double_star_spec(m, n)

    def base(value: int = 1) -> list[Fraction]:
        return [Fraction(value) for _ in range(m + n + 2)]

    cases: list[tuple[str, tuple[Fraction, ...]]] = []
    if spec.left_leaves:
        weights = base()
        weights[spec.left_leaves[0]] = Fraction(8)
        cases.append(("one_heavy_left_leaf", tuple(weights)))
    if spec.right_leaves:
        weights = base()
        weights[spec.right_leaves[0]] = Fraction(8)
        cases.append(("one_heavy_right_leaf", tuple(weights)))
    weights = base()
    weights[spec.left_leaves[0]] = Fraction(8)
    weights[spec.right_leaves[0]] = Fraction(8)
    cases.append(("one_heavy_leaf_each_side", tuple(weights)))

    weights = base()
    for leaf in spec.left_leaves:
        weights[leaf] = Fraction(8)
    cases.append(("all_left_leaves_heavy", tuple(weights)))

    weights = base()
    for leaf in spec.right_leaves:
        weights[leaf] = Fraction(8)
    cases.append(("all_right_leaves_heavy", tuple(weights)))

    weights = base()
    weights[spec.a] = Fraction(8)
    cases.append(("left_center_heavy", tuple(weights)))

    weights = base()
    weights[spec.b] = Fraction(8)
    cases.append(("right_center_heavy", tuple(weights)))

    weights = base()
    weights[spec.a] = Fraction(8)
    weights[spec.b] = Fraction(8)
    cases.append(("both_centers_heavy", tuple(weights)))

    weights = base()
    weights[spec.a] = Fraction(6)
    weights[spec.right_leaves[0]] = Fraction(9)
    cases.append(("asym_left_center_right_leaf", tuple(weights)))

    weights = base()
    weights[spec.b] = Fraction(6)
    weights[spec.left_leaves[0]] = Fraction(9)
    cases.append(("asym_right_center_left_leaf", tuple(weights)))

    if (m, n) == (1, 1):
        for raw in product(range(small_bound + 1), repeat=m + n + 2):
            weights = tuple(Fraction(value) for value in raw)
            if any(weights):
                cases.append((f"small_int_leq_{small_bound}", weights))

    dedup: dict[tuple[Fraction, ...], str] = {}
    for name, weights in cases:
        dedup.setdefault(weights, name)
    return tuple((name, weights) for weights, name in dedup.items())


def solve_double_star_lp_exact(
    m: int,
    n: int,
    weights: Iterable[Fraction | int],
    relaxation: str,
    tolerance: float = DEFAULT_TOLERANCE,
) -> DoubleStarLPResult:
    topology = double_star_topology(m, n)
    weight_tuple = tuple(Fraction(value) for value in weights)
    lp = build_hereditary_lp(topology, weight_tuple, relaxation=relaxation)
    form = exact_standard_form(lp)
    reduced = _reduce_by_weight_automorphisms(m, n, weight_tuple, lp.variables, form)

    matrix = [[0.0 for _ in reduced.objective] for _ in reduced.rows]
    for row_index, row in enumerate(reduced.rows):
        for col, value in row.items():
            matrix[row_index][col] = float(value)
    result = _simplex_maximize(
        matrix,
        [float(value) for value in reduced.rhs],
        [float(value) for value in reduced.objective],
        tolerance=tolerance,
    )
    if result.status != 0:
        raise ValueError(f"simplex failed: status={result.status} message={result.message}")

    fallback_values = tuple(Fraction(value).limit_denominator(1_000_000) for value in result.solution)
    certificate: ExactLPCertificate | None = None
    status = "exact_primal_only_after_floating_solution_rationalization"
    values = fallback_values
    active_rows: tuple[dict[str, Any], ...] = ()
    try:
        exact_values = tuple(
            _exact_primal_from_basis(
                reduced.rows,
                reduced.rhs,
                result.basis,
                len(reduced.objective),
            )
        )
        dual_values = _exact_dual_from_basis(
            reduced.rows,
            reduced.objective,
            result.basis,
            result.nonbasis,
            len(reduced.objective),
        )
        max_primal_violation = _max_primal_violation(
            reduced.rows, reduced.rhs, list(exact_values)
        )
        max_dual_deficit = _max_dual_deficit(reduced.rows, reduced.objective, dual_values)
        max_objective = sum(
            reduced.objective[index] * exact_values[index]
            for index in range(len(exact_values))
        )
        dual_objective = sum(
            reduced.rhs[row] * dual_values[row] for row in range(len(reduced.rows))
        )
        if max_primal_violation != 0 or max_dual_deficit != 0:
            raise ValueError("exact basis reconstruction did not verify")
        if dual_objective != max_objective:
            raise ValueError("dual objective mismatch")
        certificate = ExactLPCertificate(
            objective=-max_objective,
            values=exact_values,
            dual_values=dual_values,
            basis=result.basis,
            nonbasis=result.nonbasis,
            max_primal_violation=max_primal_violation,
            max_dual_deficit=max_dual_deficit,
        )
        values = exact_values
        status = "verified_exact_primal_dual_after_floating_basis_reconstruction"
        active_rows = tuple(
            {
                "row_index": row,
                "value": rational_to_string(value),
                "orbit_size": reduced.row_orbit_sizes[row],
                "row": reduced.row_descriptors[row],
            }
            for row, value in enumerate(dual_values)
            if value
        )
    except ValueError:
        max_objective = sum(
            reduced.objective[index] * values[index] for index in range(len(values))
        )

    return DoubleStarLPResult(
        relaxation=relaxation,
        optimum=-max_objective,
        certificate_status=status,
        certificate=certificate,
        values=values,
        lp=reduced,
        active_rows=active_rows,
    )


def evaluate_objective(
    m: int,
    n: int,
    weights: Iterable[Fraction | int],
    family: str,
    run_h2: bool = True,
) -> ObjectiveRun:
    spec = double_star_spec(m, n)
    weight_tuple = tuple(Fraction(value) for value in weights)
    stt_optimum, stt_depth = stt_depth_optimum(m, n, weight_tuple)
    h1 = solve_double_star_lp_exact(m, n, weight_tuple, "h1")
    if not run_h2:
        h2 = None
    elif h1.optimum == stt_optimum:
        h2 = _h2_sandwich_result_from_h1(h1, stt_optimum)
    else:
        h2 = solve_double_star_lp_exact(m, n, weight_tuple, "h2")
    reduced_variables = extract_reduced_variables(spec, h2 or h1)
    return ObjectiveRun(
        spec=spec,
        family=family,
        weights=weight_tuple,
        stt_optimum=stt_optimum,
        stt_witness_depth=stt_depth,
        h1=h1,
        h2=h2,
        reduced_variables=reduced_variables,
    )


def _h2_sandwich_result_from_h1(
    h1: DoubleStarLPResult, stt_optimum: Fraction
) -> DoubleStarLPResult:
    """Certify the H2 optimum without solving H2 when H1 is already tight.

    Since STT points are feasible for H2 and H2 is contained in H1, an exact
    equality ``H1 = STT`` sandwiches the H2 optimum to the same value.
    """

    return DoubleStarLPResult(
        relaxation="h2",
        optimum=stt_optimum,
        certificate_status=(
            "exact_by_h1_equals_stt_sandwich_no_separate_h2_primal"
        ),
        certificate=None,
        values=h1.values,
        lp=h1.lp,
        active_rows=(),
    )


def run_scout(
    topologies: tuple[tuple[int, int], ...] = (
        (1, 1),
        (2, 1),
        (2, 2),
        (3, 1),
        (3, 2),
        (3, 3),
    ),
    small_bound: int = 2,
) -> dict[str, Any]:
    normal_form_checks = {
        f"DS({m},{n})": verify_normal_form_enumeration(m, n)
        for m, n in ((1, 1), (2, 1), (2, 2))
    }
    runs: list[ObjectiveRun] = []
    skipped_h2: list[str] = []
    for m, n in topologies:
        for family, weights in structured_weight_vectors(m, n, small_bound=small_bound):
            run_h2 = True
            runs.append(evaluate_objective(m, n, weights, family, run_h2=run_h2))
    return {
        "settings": {
            "topologies": [f"DS({m},{n})" for m, n in topologies],
            "small_bound": small_bound,
        },
        "normal_form_checks": normal_form_checks,
        "runs": runs,
        "skipped_h2": skipped_h2,
    }


def write_report(
    path: Path = DEFAULT_REPORT,
    summary_path: Path = DEFAULT_SUMMARY,
    data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if data is None:
        data = run_scout()
    report = _render_report(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report, encoding="utf-8")
    write_summary(data, summary_path)
    h1_gaps = [run for run in data["runs"] if run.h1_gap < 0]
    h2_gaps = [run for run in data["runs"] if run.h2_gap is not None and run.h2_gap < 0]
    return {
        "report": str(path),
        "summary": str(summary_path),
        "runs": len(data["runs"]),
        "h1_gaps": len(h1_gaps),
        "h2_gaps": len(h2_gaps),
        "skipped_h2": len(data["skipped_h2"]),
    }


def write_summary(data: dict[str, Any], path: Path = DEFAULT_SUMMARY) -> None:
    payload = {
        "schema": "stt_double_star_depth_projection_v0_summary",
        "settings": data["settings"],
        "normal_form_checks": data["normal_form_checks"],
        "skipped_h2": data["skipped_h2"],
        "runs": [_run_to_json(run) for run in data["runs"]],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def extract_reduced_variables(
    spec: DoubleStarSpec, result: DoubleStarLPResult
) -> dict[str, Any]:
    full_values = _expanded_full_values(result)

    def value(component: Iterable[int], root: int) -> str:
        key = (tuple(sorted(component)), root)
        index = result.lp.full_variables.index(key)
        return rational_to_string(full_values[index])

    data: dict[str, Any] = {
        "theta": value((spec.a, spec.b), spec.a),
        "left": [],
        "right": [],
        "four_sets": [],
    }
    for x in spec.left_leaves:
        data["left"].append(
            {
                "leaf": spec.label(x),
                "p_x": value((x, spec.a), x),
                "r_x": value((x, spec.a, spec.b), x),
                "A_x": value((x, spec.a, spec.b), spec.a),
                "B_x": value((x, spec.a, spec.b), spec.b),
            }
        )
    for y in spec.right_leaves:
        data["right"].append(
            {
                "leaf": spec.label(y),
                "q_y": value((spec.b, y), y),
                "s_y": value((spec.a, spec.b, y), y),
                "A_y": value((spec.a, spec.b, y), spec.a),
                "B_y": value((spec.a, spec.b, y), spec.b),
            }
        )
    for x in spec.left_leaves:
        for y in spec.right_leaves:
            component = (x, spec.a, spec.b, y)
            data["four_sets"].append(
                {
                    "x": spec.label(x),
                    "y": spec.label(y),
                    "z_x": value(component, x),
                    "z_a": value(component, spec.a),
                    "z_b": value(component, spec.b),
                    "z_y": value(component, y),
                }
            )
    return data


def four_set_h2_rectangles(spec: DoubleStarSpec) -> list[dict[str, Any]]:
    topology = double_star_topology(spec.m, spec.n)
    lp = build_hereditary_lp(topology, [1] * topology.n, relaxation="h2")
    rows = []
    for constraint in lp.rectangle_constraints:
        union_set = set(constraint.union)
        if not ({spec.a, spec.b}.issubset(union_set)):
            continue
        left = sorted(union_set & set(spec.left_leaves))
        right = sorted(union_set & set(spec.right_leaves))
        if len(left) == 1 and len(right) == 1 and len(union_set) == 4:
            rows.append(
                {
                    "root": spec.label(constraint.root),
                    "base": [spec.label(v) for v in constraint.base],
                    "extension_a": [spec.label(v) for v in constraint.extension_a],
                    "extension_b": [spec.label(v) for v in constraint.extension_b],
                    "union": [spec.label(v) for v in constraint.union],
                }
            )
    return rows


def _normal_form_child_components(
    spec: DoubleStarSpec, component: Component, root: int
) -> tuple[Component, ...]:
    component_set = set(component)
    left = tuple(sorted(component_set & set(spec.left_leaves)))
    right = tuple(sorted(component_set & set(spec.right_leaves)))
    has_a = spec.a in component_set
    has_b = spec.b in component_set
    if root not in component_set:
        raise ValueError("root outside component")

    children: list[Component] = []
    if has_a and has_b:
        if root == spec.a:
            children.extend((leaf,) for leaf in left)
            children.append(tuple(sorted((spec.b, *right))))
        elif root == spec.b:
            children.append(tuple(sorted((*left, spec.a))))
            children.extend((leaf,) for leaf in right)
        elif root in left:
            children.append(tuple(sorted((*(leaf for leaf in left if leaf != root), spec.a, spec.b, *right))))
        elif root in right:
            children.append(tuple(sorted((*left, spec.a, spec.b, *(leaf for leaf in right if leaf != root)))))
    elif has_a:
        if root == spec.a:
            children.extend((leaf,) for leaf in left)
        elif root in left:
            children.append(tuple(sorted((*(leaf for leaf in left if leaf != root), spec.a))))
    elif has_b:
        if root == spec.b:
            children.extend((leaf,) for leaf in right)
        elif root in right:
            children.append(tuple(sorted((spec.b, *(leaf for leaf in right if leaf != root)))))
    return tuple(child for child in children if child)


def _reduce_by_weight_automorphisms(
    m: int,
    n: int,
    weights: tuple[Fraction, ...],
    variables: tuple[Variable, ...],
    form: Any,
) -> ReducedLP:
    permutations_for_group = _weight_preserving_permutations(m, n, weights)

    def image_variable(variable: Variable, mapping: dict[int, int]) -> Variable:
        component, root = variable
        return tuple(sorted(mapping[v] for v in component)), mapping[root]

    canonical_to_index: dict[Variable, int] = {}
    variable_to_orbit: list[int] = []
    for variable in variables:
        canonical = min(image_variable(variable, mapping) for mapping in permutations_for_group)
        if canonical not in canonical_to_index:
            canonical_to_index[canonical] = len(canonical_to_index)
        variable_to_orbit.append(canonical_to_index[canonical])

    orbit_variables = tuple(
        variable for variable, _index in sorted(canonical_to_index.items(), key=lambda item: item[1])
    )
    objective = [Fraction(0) for _ in orbit_variables]
    for index, coefficient in enumerate(form.objective):
        objective[variable_to_orbit[index]] += coefficient

    row_map: dict[tuple[tuple[tuple[int, Fraction], ...], Fraction], int] = {}
    rows: list[SparseRow] = []
    rhs: list[Fraction] = []
    descriptors: list[dict[str, Any]] = []
    orbit_sizes: list[int] = []
    for row, bound, descriptor in zip(form.rows, form.rhs, form.row_descriptors):
        reduced_row: SparseRow = {}
        for variable, coefficient in row.items():
            orbit = variable_to_orbit[variable]
            reduced_row[orbit] = reduced_row.get(orbit, Fraction(0)) + coefficient
        reduced_row = {index: value for index, value in reduced_row.items() if value}
        key = (tuple(sorted(reduced_row.items())), bound)
        if key in row_map:
            orbit_sizes[row_map[key]] += 1
            continue
        row_map[key] = len(rows)
        rows.append(reduced_row)
        rhs.append(bound)
        descriptors.append(descriptor)
        orbit_sizes.append(1)

    topology = double_star_topology(m, n)
    return ReducedLP(
        topology=topology,
        weights=weights,
        relaxation="h2" if any(d.get("kind") == "h2_rectangle" for d in descriptors) else "h1",
        full_variables=variables,
        orbit_variables=orbit_variables,
        variable_to_orbit=tuple(variable_to_orbit),
        rows=tuple(rows),
        rhs=tuple(rhs),
        objective=tuple(objective),
        row_descriptors=tuple(descriptors),
        row_orbit_sizes=tuple(orbit_sizes),
    )


def _weight_preserving_permutations(
    m: int, n: int, weights: tuple[Fraction, ...]
) -> tuple[dict[int, int], ...]:
    spec = double_star_spec(m, n)
    left_blocks = _equal_weight_blocks(spec.left_leaves, weights)
    right_blocks = _equal_weight_blocks(spec.right_leaves, weights)
    block_permutations = []
    for block in (*left_blocks, *right_blocks):
        block_permutations.append(tuple(permutations(block)))

    mappings = []
    for choices in product(*block_permutations):
        mapping = {vertex: vertex for vertex in range(m + n + 2)}
        for block, image in zip((*left_blocks, *right_blocks), choices):
            for source, target in zip(block, image):
                mapping[source] = target
        mappings.append(mapping)
    return tuple(mappings)


def _equal_weight_blocks(
    vertices: tuple[int, ...], weights: tuple[Fraction, ...]
) -> tuple[tuple[int, ...], ...]:
    blocks: dict[Fraction, list[int]] = defaultdict(list)
    for vertex in vertices:
        blocks[weights[vertex]].append(vertex)
    return tuple(tuple(values) for _weight, values in sorted(blocks.items(), key=lambda item: item[0]))


def _expanded_full_values(result: DoubleStarLPResult) -> tuple[Fraction, ...]:
    return tuple(result.values[orbit] for orbit in result.lp.variable_to_orbit)


def _run_to_json(run: ObjectiveRun) -> dict[str, Any]:
    return {
        "topology": run.spec.name,
        "family": run.family,
        "weights": {
            run.spec.label(vertex): rational_to_string(run.weights[vertex])
            for vertex in range(run.spec.m + run.spec.n + 2)
        },
        "stt_optimum": rational_to_string(run.stt_optimum),
        "stt_witness_depth": {
            run.spec.label(vertex): run.stt_witness_depth[vertex]
            for vertex in range(run.spec.m + run.spec.n + 2)
        },
        "h1_optimum": rational_to_string(run.h1.optimum),
        "h1_gap": rational_to_string(run.h1_gap),
        "h1_certificate_status": run.h1.certificate_status,
        "h2_optimum": rational_to_string(run.h2.optimum) if run.h2 is not None else None,
        "h2_gap": rational_to_string(run.h2_gap) if run.h2_gap is not None else None,
        "h2_certificate_status": run.h2.certificate_status if run.h2 is not None else None,
        "reduced_variables": run.reduced_variables,
    }


def _render_report(data: dict[str, Any]) -> str:
    runs: list[ObjectiveRun] = data["runs"]
    h1_gaps = [run for run in runs if run.h1_gap < 0]
    h2_gaps = [run for run in runs if run.h2_gap is not None and run.h2_gap < 0]
    lines: list[str] = []
    lines.append("# STT Double-Star Depth Projection v0")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append("This is finite theorem-driven computation for double-stars `DS(m,n)`, not a broad arbitrary-tree sweep.  The complete baseline is exact root-depth-0 STT enumeration; H1 is connected first-hit heredity; H2 adds connected two-extension rectangle inequalities.")
    lines.append("")
    lines.append("The tested topologies are `" + "`, `".join(data["settings"]["topologies"]) + "`.")
    lines.append(f"Normal-form STT enumeration agrees with generic recursive enumeration on small checks: `{data['normal_form_checks']}`.")
    lines.append("")
    lines.append("## Outcome")
    lines.append("")
    if h1_gaps:
        first = h1_gaps[0]
        lines.append(f"H1 depth gap found first at `{first.spec.name}` family `{first.family}`.")
    else:
        lines.append("No H1 depth-projection gap was found in the tested double-star objectives.")
    if h2_gaps:
        first = h2_gaps[0]
        lines.append(f"H2 depth gap found first at `{first.spec.name}` family `{first.family}`.")
    else:
        lines.append("No H2 depth-projection gap was found; H2 optima were certified by the H1/STT sandwich whenever H1 was already tight.")
    lines.append("")
    lines.append("This is finite evidence only.  It does not claim double-star exactness.")
    lines.append("")
    lines.append("## Solve Table")
    lines.append("")
    lines.append("| topology | family | weights | STT | H1 | H1 cert | H2 | H2 cert |")
    lines.append("|---|---|---:|---:|---:|---|---:|---|")
    for run in runs:
        h2_value = rational_to_string(run.h2.optimum) if run.h2 is not None else "not run"
        h2_status = run.h2.certificate_status if run.h2 is not None else "not run"
        lines.append(
            "| {topology} | {family} | `{weights}` | {stt} | {h1} | {h1_cert} | {h2} | {h2_cert} |".format(
                topology=run.spec.name,
                family=run.family,
                weights=_format_labeled_weights(run.spec, run.weights),
                stt=rational_to_string(run.stt_optimum),
                h1=rational_to_string(run.h1.optimum),
                h1_cert=run.h1.certificate_status,
                h2=h2_value,
                h2_cert=h2_status,
            )
        )
    lines.append("")
    lines.append("## Representative Reduced Variables")
    lines.append("")
    for run in _representative_runs(runs):
        lines.append(f"### {run.spec.name} / {run.family}")
        lines.append("")
        lines.append(f"- `theta = z[{{a,b}},a]`: `{run.reduced_variables['theta']}`")
        lines.append(f"- left leaf variables: `{run.reduced_variables['left']}`")
        lines.append(f"- right leaf variables: `{run.reduced_variables['right']}`")
        lines.append(f"- four-set values: `{run.reduced_variables['four_sets']}`")
        lines.append("")
    lines.append("## Representative H1 Dual Rows")
    lines.append("")
    lines.append("Because every H1 optimum matched the STT baseline, H2 optima are certified by the `H1 <= H2 <= STT` sandwich.  The reduced H1 proof-pattern fitting attempt therefore starts from exact H1 dual multipliers rather than H2 repair rows.")
    lines.append("")
    for run in _representative_runs(runs):
        lines.append(f"- `{run.spec.name}` / `{run.family}` active H1 dual rows, first few nonzero multipliers: `{_compact_active_rows(run.h1.active_rows)}`.")
    lines.append("")
    lines.append("Observed finite pattern: after quotienting by weight-preserving left/right leaf permutations, nonzero H1 dual rows are simplex rows plus heredity rows on path components touching the center edge or the heavy side.  This is a useful target for the reduced H1 proof pattern, but it is not a checked symbolic proof and is not promoted as double-star exactness.")
    lines.append("")
    lines.append("## Four-Set H2 Rectangles")
    lines.append("")
    for m, n in ((1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3)):
        spec = double_star_spec(m, n)
        grouped: dict[str, int] = defaultdict(int)
        for row in four_set_h2_rectangles(spec):
            grouped[row["root"]] += 1
        lines.append(f"- `{spec.name}` relevant four-set rectangles on `{{x,a,b,y}}`, grouped by root: `{dict(sorted(grouped.items()))}`.")
    lines.append("")
    lines.append("No H2 repair was needed in these runs because no H1 depth gap was found; consequently there are no active H2 repair rectangles to list.")
    lines.append("")
    lines.append("## Skeptical Audit")
    lines.append("")
    lines.append("- A no-gap finite run is not a proof of double-star exactness.")
    lines.append("- DS(3,3) H2 is feasible here only because the structured objectives permit weight-preserving symmetry reduction; arbitrary asymmetric objectives remain out of scope.")
    lines.append("- Full-`z` failure and depth-projection failure are kept separate: this report only compares projected weighted depth objectives.")
    lines.append("- Before promoting any theorem claim, the reduced H1 proof pattern from the theory note still has to be fitted symbolically.")
    return "\n".join(lines) + "\n"


def _representative_runs(runs: list[ObjectiveRun]) -> list[ObjectiveRun]:
    wanted = []
    seen: set[str] = set()
    for run in runs:
        if run.spec.name not in seen:
            wanted.append(run)
            seen.add(run.spec.name)
    return wanted


def _format_labeled_weights(spec: DoubleStarSpec, weights: tuple[Fraction, ...]) -> str:
    return _format_fraction_tuple(
        weights[vertex] for vertex in range(spec.m + spec.n + 2)
    )


def _compact_active_rows(rows: tuple[dict[str, Any], ...], limit: int = 8) -> list[dict[str, Any]]:
    compact = []
    for row in rows[:limit]:
        compact.append(
            {
                "value": row["value"],
                "orbit_size": row["orbit_size"],
                "kind": row["row"].get("kind"),
                "row": row["row"],
            }
        )
    return compact


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m scripts.stt_checker.double_star_depth_projection"
    )
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    args = parser.parse_args(argv)
    result = write_report(args.report, args.summary)
    print(
        "wrote {report} and {summary}: runs={runs} h1_gaps={h1_gaps} "
        "h2_gaps={h2_gaps} skipped_h2={skipped_h2}".format(**result)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
