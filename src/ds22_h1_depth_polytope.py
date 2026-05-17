"""Exact DS(2,2) H1 depth-vector inclusion certificate builder.

The proof object generated here is a cell/facet cover, not a sampled objective
test.  It enumerates the vertices of the blocking polyhedron

    { w >= 0 : w dot d(T) >= 1 for every true DS(2,2) schedule T },

and then certifies, for each blocking vertex w, that the H1 relaxation has
minimum weighted depth at least 1.  Since every listed w is a lower facet of
``conv(D_RST) + R_+^V``, these exact dual certificates prove the full upward
hull inclusion for all nonnegative objectives.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import time
from typing import Any, Iterable

from scripts.stt_checker.hereditary_lp import DEFAULT_TOLERANCE, _simplex_maximize

from .ds22_true_schedules import (
    VERTICES,
    Component,
    Vertex,
    connected_subsets,
    enumerate_true_schedules,
    integral_h1_point,
    path_between,
)


CERT_SCHEMA = "ds22_full_objective_depth_inclusion_v0"
DEFAULT_CERTIFICATE = Path("certificates/ds22_depth_inclusion_cert.json")
DEFAULT_REPORT = Path("reports/ds22_full_objective_depth_vector_cert_report.md")
SparseRow = dict[int, Fraction]
Variable = tuple[Component, Vertex]


@dataclass(frozen=True)
class H1System:
    connected_subsets: tuple[Component, ...]
    variables: tuple[Variable, ...]
    variable_index: dict[Variable, int]
    rows: tuple[SparseRow, ...]
    rhs: tuple[Fraction, ...]
    row_descriptors: tuple[dict[str, Any], ...]

    @property
    def simplex_rows(self) -> int:
        return len(self.connected_subsets)

    @property
    def heredity_rows(self) -> int:
        return sum(1 for row in self.row_descriptors if row["kind"] == "heredity")


@dataclass(frozen=True)
class H1DualCertificate:
    weight: tuple[Fraction, ...]
    h1_minimum: Fraction
    dual_max_objective: Fraction
    nonzero_dual_rows: tuple[dict[str, Any], ...]


def rational_to_string(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def rational_vector_json(values: Iterable[Fraction | int]) -> dict[str, str]:
    return {
        vertex: rational_to_string(Fraction(value))
        for vertex, value in zip(VERTICES, values)
    }


def h1_system() -> H1System:
    subsets = connected_subsets()
    variables = tuple((component, root) for component in subsets for root in component)
    variable_index = {variable: index for index, variable in enumerate(variables)}
    rows: list[SparseRow] = []
    rhs: list[Fraction] = []
    descriptors: list[dict[str, Any]] = []

    for component in subsets:
        row = {variable_index[(component, root)]: Fraction(1) for root in component}
        rows.append(row)
        rhs.append(Fraction(1))
        descriptors.append({"kind": "simplex_upper", "component": list(component)})

        rows.append({index: -value for index, value in row.items()})
        rhs.append(Fraction(-1))
        descriptors.append({"kind": "simplex_lower", "component": list(component)})

    subset_sets = {component: set(component) for component in subsets}
    for superset in subsets:
        superset_set = subset_sets[superset]
        for subset in subsets:
            if len(subset) >= len(superset):
                continue
            if not subset_sets[subset].issubset(superset_set):
                continue
            for root in subset:
                rows.append(
                    {
                        variable_index[(superset, root)]: Fraction(1),
                        variable_index[(subset, root)]: Fraction(-1),
                    }
                )
                rhs.append(Fraction(0))
                descriptors.append(
                    {
                        "kind": "heredity",
                        "superset": list(superset),
                        "subset": list(subset),
                        "root": root,
                    }
                )

    return H1System(
        connected_subsets=subsets,
        variables=variables,
        variable_index=variable_index,
        rows=tuple(rows),
        rhs=tuple(rhs),
        row_descriptors=tuple(descriptors),
    )


def depth_objective_coefficients(
    system: H1System, weights: Iterable[Fraction | int]
) -> tuple[Fraction, ...]:
    weight_tuple = tuple(Fraction(value) for value in weights)
    if len(weight_tuple) != len(VERTICES):
        raise ValueError("weight vector length must match DS(2,2) vertex count")
    objective = [Fraction(0) for _ in system.variables]
    for x_index, x in enumerate(VERTICES):
        for y in VERTICES:
            if x == y:
                continue
            path = path_between(x, y)
            objective[system.variable_index[(path, y)]] += weight_tuple[x_index]
    return tuple(objective)


def depth_vector_from_h1_values(
    system: H1System, values: dict[Variable, Fraction] | tuple[Fraction, ...]
) -> tuple[Fraction, ...]:
    if isinstance(values, tuple):
        value_at = lambda variable: values[system.variable_index[variable]]
    else:
        value_at = values.__getitem__
    depth: list[Fraction] = []
    for x in VERTICES:
        total = Fraction(0)
        for y in VERTICES:
            if x != y:
                total += value_at((path_between(x, y), y))
        depth.append(total)
    return tuple(depth)


def true_depth_vectors() -> tuple[tuple[int, ...], ...]:
    return tuple(schedule.depth_vector for schedule in enumerate_true_schedules())


def enumerate_blocking_vertices(
    depth_vectors: Iterable[tuple[int, ...]],
    box_bound: Fraction = Fraction(2),
) -> tuple[tuple[Fraction, ...], ...]:
    """Enumerate blocker vertices exactly by incremental halfspace intersection.

    The artificial box uses upper bound 2.  It is proof-safe here because all
    depth coordinates are nonnegative integers: if a feasible blocker has
    ``w_i > 1``, replacing ``w_i`` by 1 preserves every inequality
    ``w dot d(T) >= 1``.  Thus no genuine blocker vertex lies above 1.
    """

    points = sorted(set(tuple(int(value) for value in point) for point in depth_vectors))
    dimension = len(VERTICES)
    processed: list[tuple[tuple[Fraction, ...], Fraction, tuple[str, Any]]] = []
    vertices: list[tuple[Fraction, ...]] = []

    for index in range(dimension):
        row = [Fraction(0) for _ in range(dimension)]
        row[index] = Fraction(-1)
        processed.append((tuple(row), Fraction(0), ("lower_bound", index)))
    for index in range(dimension):
        row = [Fraction(0) for _ in range(dimension)]
        row[index] = Fraction(1)
        processed.append((tuple(row), box_bound, ("artificial_upper_bound", index)))

    for bits in product((Fraction(0), box_bound), repeat=dimension):
        vertices.append(tuple(bits))

    processed_rows = [row for row, _rhs, _tag in processed]
    active_sets = [
        frozenset(
            index
            for index, (row, rhs, _tag) in enumerate(processed)
            if _dot(row, vertex) == rhs
        )
        for vertex in vertices
    ]
    rank_cache: dict[tuple[int, ...], int] = {}

    def rank_indices(indices: Iterable[int]) -> int:
        key = tuple(sorted(indices))
        if key not in rank_cache:
            rank_cache[key] = _rank_rows([processed_rows[index] for index in key])
        return rank_cache[key]

    constraints = [
        (tuple(Fraction(-value) for value in point), Fraction(-1), ("depth", point))
        for point in points
    ]
    constraints.sort(key=lambda item: (sum(item[2][1]), item[2][1]))

    for row, rhs, tag in constraints:
        new_constraint_index = len(processed)
        values = [_dot(row, vertex) - rhs for vertex in vertices]
        inside = [value <= 0 for value in values]
        if all(inside):
            processed.append((row, rhs, tag))
            processed_rows.append(row)
            active_sets = [
                active | ({new_constraint_index} if value == 0 else frozenset())
                for active, value in zip(active_sets, values)
            ]
            continue

        kept_vertices: list[tuple[Fraction, ...]] = []
        kept_active: list[frozenset[int]] = []
        seen: set[tuple[Fraction, ...]] = set()
        inside_indices: list[int] = []
        outside_indices: list[int] = []

        for index, (vertex, active, is_inside, value) in enumerate(
            zip(vertices, active_sets, inside, values)
        ):
            if is_inside:
                inside_indices.append(index)
                updated = active | (
                    {new_constraint_index} if value == 0 else frozenset()
                )
                kept_vertices.append(vertex)
                kept_active.append(frozenset(updated))
                seen.add(vertex)
            else:
                outside_indices.append(index)

        for outside_index in outside_indices:
            outside_vertex = vertices[outside_index]
            outside_value = values[outside_index]
            outside_active = active_sets[outside_index]
            for inside_index in inside_indices:
                common_active = outside_active & active_sets[inside_index]
                if len(common_active) < dimension - 1:
                    continue
                if rank_indices(common_active) < dimension - 1:
                    continue

                inside_vertex = vertices[inside_index]
                inside_value = values[inside_index]
                if outside_value == inside_value:
                    continue
                parameter = -inside_value / (outside_value - inside_value)
                candidate = tuple(
                    inside_vertex[index]
                    + parameter * (outside_vertex[index] - inside_vertex[index])
                    for index in range(dimension)
                )
                if candidate in seen:
                    continue
                if any(_dot(old_row, candidate) > old_rhs for old_row, old_rhs, _ in processed):
                    continue
                if _dot(row, candidate) != rhs:
                    raise ArithmeticError("halfspace intersection produced a bad vertex")

                candidate_active = set(common_active)
                candidate_active.add(new_constraint_index)
                for old_index, (old_row, old_rhs, _old_tag) in enumerate(processed):
                    if old_index not in candidate_active and _dot(old_row, candidate) == old_rhs:
                        candidate_active.add(old_index)
                kept_vertices.append(candidate)
                kept_active.append(frozenset(candidate_active))
                seen.add(candidate)

        vertices = kept_vertices
        active_sets = kept_active
        processed.append((row, rhs, tag))
        processed_rows.append(row)

    real_vertices = [
        vertex
        for vertex in vertices
        if all(coordinate != box_bound for coordinate in vertex)
    ]
    for vertex in real_vertices:
        if min(vertex) < 0 or max(vertex) > 1:
            raise ValueError("blocker vertex escaped the proof-safe [0,1] bound")
        if min(sum(Fraction(p[i]) * vertex[i] for i in range(dimension)) for p in points) != 1:
            raise ValueError("blocker vertex is not normalized to true minimum 1")
    return tuple(sorted(set(real_vertices)))


def solve_h1_dual_certificate(
    system: H1System,
    weight: tuple[Fraction, ...],
    tolerance: float = DEFAULT_TOLERANCE,
) -> H1DualCertificate:
    objective = depth_objective_coefficients(system, weight)
    max_objective = tuple(-coefficient for coefficient in objective)
    matrix = [
        [float(row.get(index, Fraction(0))) for index in range(len(system.variables))]
        for row in system.rows
    ]
    result = _simplex_maximize(
        matrix,
        [float(value) for value in system.rhs],
        [float(value) for value in max_objective],
        tolerance=tolerance,
    )
    if result.status != 0:
        raise ValueError(f"simplex failed: status={result.status} message={result.message}")

    primal = _exact_primal_from_basis(
        system.rows, system.rhs, result.basis, len(system.variables)
    )
    dual = _exact_dual_from_basis(
        system.rows,
        max_objective,
        result.basis,
        result.nonbasis,
        len(system.variables),
    )
    max_primal_violation = _max_primal_violation(system.rows, system.rhs, primal)
    max_dual_deficit = _max_dual_deficit(system.rows, max_objective, dual)
    if max_primal_violation != 0 or max_dual_deficit != 0:
        raise ValueError(
            "basis reconstruction did not verify exactly: "
            f"primal_violation={max_primal_violation}, "
            f"dual_deficit={max_dual_deficit}"
        )
    max_value = sum(max_objective[index] * primal[index] for index in range(len(primal)))
    dual_value = sum(system.rhs[row] * dual[row] for row in range(len(system.rows)))
    if max_value != dual_value:
        raise ValueError(f"dual objective mismatch: primal={max_value}, dual={dual_value}")

    return H1DualCertificate(
        weight=weight,
        h1_minimum=-max_value,
        dual_max_objective=dual_value,
        nonzero_dual_rows=tuple(
            {
                "row_index": row,
                "value": rational_to_string(value),
                "row": system.row_descriptors[row],
            }
            for row, value in enumerate(dual)
            if value
        ),
    )


def build_certificate(progress: bool = False) -> dict[str, Any]:
    started = time.time()
    system = h1_system()
    schedules = enumerate_true_schedules()
    depth_to_schedules: dict[tuple[int, ...], list[str]] = {}
    for schedule in schedules:
        depth_to_schedules.setdefault(schedule.depth_vector, []).append(schedule.schedule_id)
    depth_vectors = tuple(sorted(depth_to_schedules))

    if progress:
        print(
            "enumerating blocker vertices for "
            f"{len(depth_vectors)} true depth vectors",
            flush=True,
        )
    blocker_vertices = enumerate_blocking_vertices(depth_vectors)
    if progress:
        print(f"blocker_vertices={len(blocker_vertices)}", flush=True)

    depth_id = {depth: f"d{index:03d}" for index, depth in enumerate(depth_vectors)}
    weight_id = {
        weight: f"w{index:04d}" for index, weight in enumerate(blocker_vertices)
    }
    true_depth_json = [
        {
            "id": depth_id[depth],
            "depth": {vertex: depth[index] for index, vertex in enumerate(VERTICES)},
            "schedule_ids": depth_to_schedules[depth],
        }
        for depth in depth_vectors
    ]
    schedule_json = [
        schedule.to_json(depth_id[schedule.depth_vector]) for schedule in schedules
    ]

    blocker_json: list[dict[str, Any]] = []
    dual_json: list[dict[str, Any]] = []
    for index, weight in enumerate(blocker_vertices, start=1):
        if progress and (index == 1 or index % 50 == 0 or index == len(blocker_vertices)):
            print(f"solving H1 dual certificates {index}/{len(blocker_vertices)}", flush=True)
        tight_depths = [
            depth_id[depth]
            for depth in depth_vectors
            if sum(Fraction(depth[i]) * weight[i] for i in range(len(VERTICES))) == 1
        ]
        blocker_json.append(
            {
                "id": weight_id[weight],
                "weights": rational_vector_json(weight),
                "normalization": "min_true_depth_dot_weight_equals_1",
                "tight_depth_vector_ids": tight_depths,
            }
        )
        dual = solve_h1_dual_certificate(system, weight)
        if dual.h1_minimum != 1:
            raise ValueError(
                f"H1 minimum for {weight_id[weight]} is {dual.h1_minimum}, expected 1"
            )
        dual_json.append(
            {
                "weight_id": weight_id[weight],
                "h1_minimum": rational_to_string(dual.h1_minimum),
                "dual_max_objective": rational_to_string(dual.dual_max_objective),
                "dual_original_lower_bound": rational_to_string(-dual.dual_max_objective),
                "nonzero_dual_rows": list(dual.nonzero_dual_rows),
            }
        )

    singleton_integral_point = integral_h1_point(schedules[0])
    singleton_depth = depth_vector_from_h1_values(
        system,
        {key: Fraction(value) for key, value in singleton_integral_point.items()},
    )
    if tuple(int(value) for value in singleton_depth) != schedules[0].depth_vector:
        raise ValueError("integral H1 point sanity check failed")

    runtime = time.time() - started
    return {
        "schema": CERT_SCHEMA,
        "result": "success",
        "result_statement": "certificate-backed DS(2,2) full-objective H1 exactness",
        "topology": {
            "vertices": list(VERTICES),
            "edges": [list(edge) for edge in (
                ("a", "b"),
                ("b", "r"),
                ("b", "s"),
                ("a", "li"),
                ("a", "lj"),
            )],
        },
        "h1_system": {
            "connected_subsets": len(system.connected_subsets),
            "variables": len(system.variables),
            "simplex_rows": system.simplex_rows,
            "heredity_rows": system.heredity_rows,
            "standard_form_rows": len(system.rows),
            "nonnegativity_rows": len(system.variables),
            "rows_used": "H1 simplex/heredity plus variable nonnegativity only",
            "excluded_rows": [
                "H2",
                "refined-Z",
                "path monotonicity",
                "mixed second differences",
                "endpointwise kappa payment",
                "true-right-star-mixture",
            ],
        },
        "true_schedules": {
            "schedule_count": len(schedules),
            "depth_vector_count": len(depth_vectors),
            "depth_vectors": true_depth_json,
            "schedules": schedule_json,
        },
        "cell_cover": {
            "type": "blocking_polyhedron_vertices",
            "blocker_vertex_count": len(blocker_vertices),
            "definition": (
                "Vertices of {w >= 0 : w dot d(T) >= 1 for every true schedule T}; "
                "each vertex is a nonnegative objective cell normal for the lower "
                "facets of conv(D_RST)+R_+^V."
            ),
            "artificial_box_bound": "2",
            "safe_box_reason": (
                "All true depth coordinates are nonnegative integers; any blocker "
                "coordinate above 1 can be decreased to 1 without violating "
                "w dot d(T) >= 1."
            ),
            "blocker_vertices": blocker_json,
        },
        "h1_dual_certificates": dual_json,
        "coordinate_nonnegativity": {
            "status": "covered_by_z_nonnegativity_in_depth_definition",
            "explanation": (
                "The remaining c=0 upward-hull facets are q_x >= 0, and every "
                "H1 depth coordinate is a sum of nonnegative z variables."
            ),
        },
        "runtime_seconds": runtime,
    }


def write_certificate_and_report(
    certificate_path: Path = DEFAULT_CERTIFICATE,
    report_path: Path = DEFAULT_REPORT,
    progress: bool = False,
) -> dict[str, Any]:
    certificate = build_certificate(progress=progress)
    certificate_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    certificate_path.write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    report_path.write_text(
        render_report(certificate, certificate_path, report_path),
        encoding="utf-8",
    )
    return {
        "certificate": str(certificate_path),
        "report": str(report_path),
        "blocker_vertices": certificate["cell_cover"]["blocker_vertex_count"],
        "dual_certificates": len(certificate["h1_dual_certificates"]),
        "runtime_seconds": certificate["runtime_seconds"],
    }


def render_report(
    certificate: dict[str, Any],
    certificate_path: Path = DEFAULT_CERTIFICATE,
    report_path: Path = DEFAULT_REPORT,
) -> str:
    h1 = certificate["h1_system"]
    schedules = certificate["true_schedules"]
    cover = certificate["cell_cover"]
    lines = [
        "# DS(2,2) Full-Objective Depth-Vector Certificate",
        "",
        "## Result",
        "",
        "certificate-backed DS(2,2) full-objective H1 exactness.",
        "",
        "This is only a finite DS(2,2) H1 depth-vector statement. It does not claim DS(k,2), H2, refined-Z, path monotonicity, mixed second differences, endpointwise kappa payment, or any true-right-star-mixture fact.",
        "",
        "## Counts",
        "",
        f"- H1 connected subsets: `{h1['connected_subsets']}`.",
        f"- H1 variables: `{h1['variables']}`.",
        f"- H1 simplex rows: `{h1['simplex_rows']}`.",
        f"- H1 heredity rows: `{h1['heredity_rows']}`.",
        f"- Standard-form rows checked by dual certificates: `{h1['standard_form_rows']}`.",
        f"- True schedules: `{schedules['schedule_count']}`.",
        f"- Deduplicated true depth vectors: `{schedules['depth_vector_count']}`.",
        f"- Blocking-cell facet normals: `{cover['blocker_vertex_count']}`.",
        f"- H1 exact dual certificates: `{len(certificate['h1_dual_certificates'])}`.",
        "",
        "## Exact Inclusion Certificate",
        "",
        "The certificate enumerates the exact vertices of the blocking polyhedron `{w >= 0 : w dot d(T) >= 1 for every true recursive search tree T}`. For every listed nonnegative blocker vertex `w`, the JSON stores an exact H1 dual certificate proving `min_{z in H1} w dot d(z) >= 1`. Since each blocker is normalized so that `min_T w dot d(T) = 1`, every lower facet of `conv(D_RST)+R_+^V` is valid for `D_H1`.",
        "",
        "The coordinate facets `q_x >= 0` are covered directly because every H1 depth coordinate is a sum of nonnegative first-hit variables.",
        "",
        "## Artifacts",
        "",
        f"- Certificate: `{certificate_path}`.",
        f"- Verifier: `src/ds22_depth_inclusion_check.py`.",
        f"- Builder: `src/ds22_h1_depth_polytope.py`.",
        f"- True schedule enumerator: `src/ds22_true_schedules.py`.",
        f"- Report: `{report_path}`.",
        "",
        "## Commands",
        "",
        "```powershell",
        "python -m src.ds22_h1_depth_polytope --progress",
        "python -m src.ds22_depth_inclusion_check certificates/ds22_depth_inclusion_cert.json",
        "python -m unittest tests.test_ds22_depth_inclusion",
        "```",
        "",
        "Expected verifier output:",
        "",
        "```text",
        "verified ds22 depth inclusion certificate: true_schedules=214 depth_vectors=214 blocker_vertices=943 dual_certificates=943 h1_rows=436",
        "```",
        "",
        "## Overclaim-Safe Interpretation",
        "",
        "The certificate proves `D_H1 subset conv(D_RST)+R_{>=0}^V` for the six-vertex DS(2,2) tree only. It is a full-objective nonnegative-weight certificate, not a bounded-weight search, but it should not be promoted to DS(k,2) or arbitrary double-star exactness.",
        "",
        "## Best Next Proof-Work Prompt",
        "",
        "Use the DS(2,2) blocker-vertex dual certificates as a finite atlas. Cluster the 943 nonnegative facet normals by graph automorphism and active H1 heredity rows, then ask for a symbolic proof template that derives the recurring dual patterns using only H1 simplex and heredity rows.",
    ]
    return "\n".join(lines) + "\n"


def _dot(row: tuple[Fraction, ...], vector: tuple[Fraction, ...]) -> Fraction:
    return sum(coefficient * value for coefficient, value in zip(row, vector))


def _rank_rows(rows: Iterable[tuple[Fraction, ...]]) -> int:
    matrix = [list(row) for row in rows if any(row)]
    dimension = len(VERTICES)
    rank = 0
    for column in range(dimension):
        pivot = None
        for row_index in range(rank, len(matrix)):
            if matrix[row_index][column] != 0:
                pivot = row_index
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        for index in range(column, dimension):
            matrix[rank][index] /= pivot_value
        for row_index in range(len(matrix)):
            if row_index == rank:
                continue
            factor = matrix[row_index][column]
            if factor == 0:
                continue
            for index in range(column, dimension):
                matrix[row_index][index] -= factor * matrix[rank][index]
        rank += 1
        if rank == dimension:
            break
    return rank


def _exact_primal_from_basis(
    rows: tuple[SparseRow, ...],
    rhs: tuple[Fraction, ...],
    basis: tuple[int, ...],
    variable_count: int,
) -> list[Fraction]:
    if -1 in basis:
        raise ValueError("cannot reconstruct exact primal with artificial variable in basis")
    row_count = len(rows)
    if len(basis) != row_count:
        raise ValueError("basis length must equal row count")
    basis_set = set(basis)
    basic_originals = [index for index in basis if 0 <= index < variable_count]
    nonbasic_slack_rows = [
        index - variable_count
        for index in range(variable_count, variable_count + row_count)
        if index not in basis_set
    ]
    if len(basic_originals) != len(nonbasic_slack_rows):
        raise ValueError(
            "basis shape is not reconstructible by tight-row shortcut: "
            f"{len(basic_originals)} basic originals vs {len(nonbasic_slack_rows)} nonbasic slacks"
        )
    matrix = [
        [rows[row].get(variable, Fraction(0)) for variable in basic_originals]
        for row in nonbasic_slack_rows
    ]
    tight_rhs = [rhs[row] for row in nonbasic_slack_rows]
    basic_values = _solve_square_linear_system(matrix, tight_rhs)
    values = [Fraction(0) for _ in range(variable_count)]
    for basis_variable, value in zip(basic_originals, basic_values):
        values[basis_variable] = value
    return values


def _exact_dual_from_basis(
    rows: tuple[SparseRow, ...],
    max_objective: tuple[Fraction, ...],
    basis: tuple[int, ...],
    nonbasis: tuple[int, ...],
    variable_count: int,
) -> tuple[Fraction, ...]:
    row_count = len(rows)
    basic_originals = [index for index in basis if 0 <= index < variable_count]
    nonbasic_slack_rows = [
        index - variable_count
        for index in nonbasis
        if variable_count <= index < variable_count + row_count
    ]
    if len(basic_originals) != len(nonbasic_slack_rows):
        raise ValueError(
            "basis shape is not reconstructible by sparse slack shortcut: "
            f"{len(basic_originals)} basic originals vs {len(nonbasic_slack_rows)} nonbasic slacks"
        )
    system = [
        [rows[row].get(variable, Fraction(0)) for row in nonbasic_slack_rows]
        for variable in basic_originals
    ]
    rhs = [max_objective[variable] for variable in basic_originals]
    solved = _solve_square_linear_system(system, rhs) if system else []
    dual = [Fraction(0) for _ in range(row_count)]
    for row, value in zip(nonbasic_slack_rows, solved):
        dual[row] = value
    if min(dual, default=Fraction(0)) < 0:
        raise ValueError("reconstructed dual has a negative multiplier")
    return tuple(dual)


def _max_primal_violation(
    rows: tuple[SparseRow, ...], rhs: tuple[Fraction, ...], values: list[Fraction]
) -> Fraction:
    violation = Fraction(0)
    for row, bound in zip(rows, rhs):
        lhs = sum(coefficient * values[index] for index, coefficient in row.items())
        violation = max(violation, lhs - bound)
    return violation


def _max_dual_deficit(
    rows: tuple[SparseRow, ...],
    max_objective: tuple[Fraction, ...],
    dual_values: tuple[Fraction, ...],
) -> Fraction:
    deficit = Fraction(0)
    for variable, coefficient in enumerate(max_objective):
        lhs = sum(
            rows[row].get(variable, Fraction(0)) * dual_values[row]
            for row in range(len(rows))
        )
        deficit = max(deficit, coefficient - lhs)
    return deficit


def _solve_square_linear_system(
    matrix: list[list[Fraction]], rhs: list[Fraction]
) -> list[Fraction]:
    size = len(rhs)
    if len(matrix) != size or any(len(row) != size for row in matrix):
        raise ValueError("linear system must be square")
    if size == 0:
        return []
    augmented = [list(row) + [rhs[row_index]] for row_index, row in enumerate(matrix)]
    for column in range(size):
        pivot = None
        for row in range(column, size):
            if augmented[row][column] != 0:
                pivot = row
                break
        if pivot is None:
            raise ValueError(f"linear system is singular at column {column}")
        if pivot != column:
            augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        for index in range(column, size + 1):
            augmented[column][index] /= pivot_value
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor == 0:
                continue
            for index in range(column, size + 1):
                augmented[row][index] -= factor * augmented[column][index]
    return [augmented[row][size] for row in range(size)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m src.ds22_h1_depth_polytope")
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args(argv)
    result = write_certificate_and_report(
        certificate_path=args.certificate,
        report_path=args.report,
        progress=args.progress,
    )
    print(
        "wrote {certificate} and {report}: blocker_vertices={blocker_vertices} "
        "dual_certificates={dual_certificates} runtime_seconds={runtime_seconds:.3f}".format(
            **result
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

