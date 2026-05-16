"""Exact H2 certificate reconstruction and verification utilities.

The H2 solver itself is numerical.  This module rebuilds the same standard
form over ``Fraction`` and checks proof objects derived from the saved simplex
basis.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import json
from pathlib import Path
from typing import Any

from .hereditary_lp import (
    SKZ_LONG_STAR_TOPOLOGY,
    SKZ_LONG_STAR_WEIGHTS,
    HereditaryLP,
    RectangleConstraint,
    build_hereditary_lp,
    rational_to_string,
)
from .rationals import parse_rational
from .topology import TreeTopology


DUAL_CERT_SCHEMA = "stt-h2-primal-dual-cert-v0"
FIXED_D_SCHEMA = "stt-h2-fixed-depth-cert-v0"
DEFAULT_H2_RESULT = Path("examples/stt_lp/skz_long_star_7_h2_result.json")
DEFAULT_DUAL_CERT = Path("examples/stt_lp/skz_long_star_7_h2_dual_certificate.json")
DEFAULT_FIXED_D_RESULT = Path("examples/stt_lp/skz_long_star_7_h2_fixed_d_result.json")
SKZ_FRACTIONAL_DEPTH_VECTOR = (
    Fraction(2),
    Fraction(2),
    Fraction(9, 2),
    Fraction(2),
    Fraction(2),
    Fraction(3, 2),
    Fraction(1, 2),
)


SparseRow = dict[int, Fraction]


@dataclass(frozen=True)
class ExactStandardForm:
    rows: tuple[SparseRow, ...]
    rhs: tuple[Fraction, ...]
    objective: tuple[Fraction, ...]
    row_descriptors: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class CertificateVerification:
    primal_objective: Fraction
    dual_max_objective: Fraction
    original_min_lower_bound: Fraction
    max_dual_deficit: Fraction
    matching_objective: bool


@dataclass(frozen=True)
class FixedDepthCheck:
    depth_objective: Fraction
    lower_bound: Fraction
    farkas_rhs: Fraction
    feasible: bool


def exact_standard_form(lp: HereditaryLP) -> ExactStandardForm:
    """Return exact ``max c*x`` form: ``A*x <= b, x >= 0``."""

    rows: list[SparseRow] = []
    rhs: list[Fraction] = []
    descriptors: list[dict[str, Any]] = []

    for component in lp.connected_subsets:
        row = {lp.variable_index[(component, root)]: Fraction(1) for root in component}
        rows.append(row)
        rhs.append(Fraction(1))
        descriptors.append({"kind": "simplex_upper", "component": list(component)})

        rows.append({index: -value for index, value in row.items()})
        rhs.append(Fraction(-1))
        descriptors.append({"kind": "simplex_lower", "component": list(component)})

    for constraint in lp.heredity_constraints:
        rows.append(
            {
                lp.variable_index[(constraint.superset, constraint.root)]: Fraction(1),
                lp.variable_index[(constraint.subset, constraint.root)]: Fraction(-1),
            }
        )
        rhs.append(Fraction(0))
        descriptors.append(
            {
                "kind": "heredity",
                "superset": list(constraint.superset),
                "subset": list(constraint.subset),
                "root": constraint.root,
            }
        )

    for constraint in lp.rectangle_constraints:
        row: SparseRow = {}
        for variable, coefficient in (
            ((constraint.base, constraint.root), Fraction(-1)),
            ((constraint.extension_a, constraint.root), Fraction(1)),
            ((constraint.extension_b, constraint.root), Fraction(1)),
            ((constraint.union, constraint.root), Fraction(-1)),
        ):
            index = lp.variable_index[variable]
            row[index] = row.get(index, Fraction(0)) + coefficient
        rows.append({index: value for index, value in row.items() if value})
        rhs.append(Fraction(0))
        descriptors.append(
            {
                "kind": "h2_rectangle",
                "base": list(constraint.base),
                "extension_a": list(constraint.extension_a),
                "extension_b": list(constraint.extension_b),
                "union": list(constraint.union),
                "root": constraint.root,
            }
        )

    return ExactStandardForm(
        rows=tuple(rows),
        rhs=tuple(rhs),
        objective=tuple(-coefficient for coefficient in lp.objective_coefficients),
        row_descriptors=tuple(descriptors),
    )


def audit_h2_rectangle_enumeration(lp: HereditaryLP) -> dict[str, Any]:
    """Audit that H2 keeps exactly the nontrivial rectangle rows.

    The audit enumerates ordered candidate triples ``(S,A,B)``.  Rows whose
    simplified expression is zero are tautologies; rows with two terms are H1
    heredity duplicates.  The remaining rows are canonicalized by sorting the
    symmetric ``A,B`` pair and must match ``lp.rectangle_constraints`` exactly.
    """

    connected = lp.connected_subsets
    connected_set = set(connected)
    subset_sets = {component: set(component) for component in connected}
    actual = {
        (
            constraint.base,
            constraint.extension_a,
            constraint.extension_b,
            constraint.union,
            constraint.root,
        )
        for constraint in lp.rectangle_constraints
    }

    category_counts: Counter[str] = Counter()
    nontrivial_ordered: list[
        tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...], tuple[int, ...], int]
    ] = []

    for base in connected:
        base_set = subset_sets[base]
        for extension_a in connected:
            if not base_set.issubset(subset_sets[extension_a]):
                continue
            for extension_b in connected:
                if not base_set.issubset(subset_sets[extension_b]):
                    continue
                union = tuple(sorted(subset_sets[extension_a] | subset_sets[extension_b]))
                if union not in connected_set:
                    continue
                for root in base:
                    coefficients: Counter[tuple[tuple[int, ...], int]] = Counter()
                    for key, coefficient in (
                        ((base, root), 1),
                        ((extension_a, root), -1),
                        ((extension_b, root), -1),
                        ((union, root), 1),
                    ):
                        coefficients[key] += coefficient
                    reduced = {key: value for key, value in coefficients.items() if value}

                    if not reduced:
                        category_counts["tautology"] += 1
                        continue

                    if len(reduced) == 2 and sorted(reduced.values()) == [-1, 1]:
                        plus_set = next(key[0] for key, value in reduced.items() if value == 1)
                        minus_set = next(key[0] for key, value in reduced.items() if value == -1)
                        if subset_sets[plus_set].issubset(subset_sets[minus_set]):
                            category_counts["h1_duplicate"] += 1
                            continue

                    category_counts["nontrivial_ordered"] += 1
                    first, second = sorted((extension_a, extension_b))
                    nontrivial_ordered.append((base, first, second, union, root))

    canonical = set(nontrivial_ordered)
    missing = sorted(canonical - actual)
    extra = sorted(actual - canonical)
    return {
        "connected_subsets": len(lp.connected_subsets),
        "z_variables": len(lp.variables),
        "ordered_candidates": sum(category_counts.values()),
        "tautologies": category_counts["tautology"],
        "h1_duplicates": category_counts["h1_duplicate"],
        "nontrivial_ordered": category_counts["nontrivial_ordered"],
        "symmetric_or_exact_duplicates": len(nontrivial_ordered) - len(canonical),
        "canonical_nontrivial": len(canonical),
        "implemented_rectangles": len(actual),
        "missing_nontrivial_rows": len(missing),
        "extra_rows": len(extra),
        "missing_examples": [_rectangle_key_to_dict(item) for item in missing[:5]],
        "extra_examples": [_rectangle_key_to_dict(item) for item in extra[:5]],
        "passes": not missing and not extra,
    }


def reconstruct_certificate_from_result(result_path: Path) -> dict[str, Any]:
    data = _load_json(result_path)
    topology = TreeTopology.from_dict(data["topology"])
    weights = [parse_rational(data["weights"][str(vertex)], f"weights.{vertex}") for vertex in topology.vertices]
    lp = build_hereditary_lp(topology, weights, relaxation="h2")
    form = exact_standard_form(lp)
    basis_data = data.get("solver_basis_data")
    if not isinstance(basis_data, dict):
        raise ValueError("solver_basis_data: missing object")

    variable_count = len(lp.variables)
    row_count = len(form.rows)
    if basis_data.get("original_variable_count") != variable_count:
        raise ValueError("basis original_variable_count does not match rebuilt LP")
    if basis_data.get("inequality_row_count") != row_count:
        raise ValueError("basis inequality_row_count does not match rebuilt LP")

    basis = _parse_int_list(basis_data.get("basis_variable_indices"), "basis_variable_indices")
    nonbasis = _parse_int_list(
        basis_data.get("nonbasis_variable_indices"), "nonbasis_variable_indices"
    )
    _check_basis_partition(basis, nonbasis, variable_count, row_count)

    basic_originals = [index for index in basis if 0 <= index < variable_count]
    nonbasic_slack_rows = [
        index - variable_count
        for index in nonbasis
        if variable_count <= index < variable_count + row_count
    ]
    if len(basic_originals) != len(nonbasic_slack_rows):
        raise ValueError(
            "basis shape is not reconstructible by the sparse slack shortcut: "
            f"{len(basic_originals)} basic originals vs "
            f"{len(nonbasic_slack_rows)} nonbasic slacks"
        )

    system = [
        [form.rows[row].get(variable, Fraction(0)) for row in nonbasic_slack_rows]
        for variable in basic_originals
    ]
    rhs = [form.objective[variable] for variable in basic_originals]
    nonbasic_dual_values = _solve_square_linear_system(system, rhs)

    dual_values = [Fraction(0) for _ in range(row_count)]
    for row, value in zip(nonbasic_slack_rows, nonbasic_dual_values):
        dual_values[row] = value

    primal_values = _primal_values_from_result(data, lp)
    primal_objective = _check_primal(lp, primal_values)
    verification = _check_dual(form, dual_values, primal_objective)
    if not verification.matching_objective:
        raise ValueError("reconstructed dual does not match primal objective")

    nonzero_dual_rows = [
        {
            "row_index": row,
            "value": rational_to_string(value),
            "row": form.row_descriptors[row],
        }
        for row, value in enumerate(dual_values)
        if value
    ]

    return {
        "schema_version": DUAL_CERT_SCHEMA,
        "certificate_id": "skz_long_star_7_h2_exact_primal_dual",
        "relaxation": "h2",
        "topology": data["topology"],
        "weights": data["weights"],
        "objective_convention": {
            "primal": "minimize original weighted depth objective over H2",
            "dual": "dual for max -objective subject to Ax <= b, x >= 0",
        },
        "standard_form": {
            "original_variable_count": variable_count,
            "inequality_row_count": row_count,
            "simplex_equalities_as_two_inequalities": True,
        },
        "primal": {
            "objective": rational_to_string(primal_objective),
            "nonzero_z_variables": _nonzero_primal_entries(lp, primal_values),
        },
        "dual": {
            "max_negated_objective": rational_to_string(verification.dual_max_objective),
            "original_min_lower_bound": rational_to_string(
                verification.original_min_lower_bound
            ),
            "nonzero_rows": nonzero_dual_rows,
        },
        "basis_reconstruction": {
            "source_result_json": str(result_path),
            "basic_original_variables": basic_originals,
            "nonbasic_original_variables": [
                index for index in nonbasis if 0 <= index < variable_count
            ],
            "nonbasic_slack_rows": nonbasic_slack_rows,
            "nonzero_dual_rows": len(nonzero_dual_rows),
        },
        "verified": {
            "primal_feasible": True,
            "dual_feasible": True,
            "weak_duality_matches": True,
            "h2_optimum": rational_to_string(primal_objective),
        },
    }


def verify_certificate_file(path: Path) -> CertificateVerification:
    return verify_certificate(_load_json(path))


def verify_certificate(data: dict[str, Any]) -> CertificateVerification:
    if data.get("schema_version") != DUAL_CERT_SCHEMA:
        raise ValueError(
            f"schema_version: expected {DUAL_CERT_SCHEMA!r}, got {data.get('schema_version')!r}"
        )
    if data.get("relaxation") != "h2":
        raise ValueError("relaxation: expected 'h2'")
    topology = TreeTopology.from_dict(data["topology"])
    weights = [parse_rational(data["weights"][str(vertex)], f"weights.{vertex}") for vertex in topology.vertices]
    lp = build_hereditary_lp(topology, weights, relaxation="h2")
    form = exact_standard_form(lp)

    standard_form = data.get("standard_form", {})
    if standard_form.get("original_variable_count") != len(lp.variables):
        raise ValueError("standard_form.original_variable_count mismatch")
    if standard_form.get("inequality_row_count") != len(form.rows):
        raise ValueError("standard_form.inequality_row_count mismatch")

    primal_values = _parse_primal_values(data.get("primal"), lp)
    primal_objective = _check_primal(lp, primal_values)
    claimed_primal = parse_rational(data["primal"].get("objective"), "primal.objective")
    if claimed_primal != primal_objective:
        raise ValueError(
            "primal.objective: claimed "
            f"{rational_to_string(claimed_primal)}, computed "
            f"{rational_to_string(primal_objective)}"
        )

    dual_values = _parse_dual_values(data.get("dual"), form)
    verification = _check_dual(form, dual_values, primal_objective)
    claimed_dual = parse_rational(
        data["dual"].get("max_negated_objective"), "dual.max_negated_objective"
    )
    if claimed_dual != verification.dual_max_objective:
        raise ValueError(
            "dual.max_negated_objective: claimed "
            f"{rational_to_string(claimed_dual)}, computed "
            f"{rational_to_string(verification.dual_max_objective)}"
        )
    claimed_lower = parse_rational(
        data["dual"].get("original_min_lower_bound"), "dual.original_min_lower_bound"
    )
    if claimed_lower != verification.original_min_lower_bound:
        raise ValueError("dual.original_min_lower_bound does not match max dual objective")
    if not verification.matching_objective:
        raise ValueError("primal objective and dual lower bound do not match")
    return verification


def fixed_depth_certificate(
    dual_certificate_path: Path,
    depth_vector: tuple[Fraction, ...] = SKZ_FRACTIONAL_DEPTH_VECTOR,
    run_numerical: bool = False,
) -> dict[str, Any]:
    cert = _load_json(dual_certificate_path)
    verification = verify_certificate(cert)
    topology = TreeTopology.from_dict(cert["topology"])
    if len(depth_vector) != topology.n:
        raise ValueError("depth vector length must match topology.n")
    weights = {
        vertex: parse_rational(cert["weights"][str(vertex)], f"weights.{vertex}")
        for vertex in topology.vertices
    }
    lp = build_hereditary_lp(topology, weights, relaxation="h2")
    form = exact_standard_form(lp)
    dual_values = _parse_dual_values(cert["dual"], form)
    check = check_fixed_depth_infeasibility(lp, form, dual_values, depth_vector)

    numerical: dict[str, Any] | None = None
    if run_numerical:
        numerical = _run_fixed_depth_simplex(lp, depth_vector)

    return {
        "schema_version": FIXED_D_SCHEMA,
        "certificate_id": "skz_long_star_7_h2_fixed_depth_infeasible",
        "topology": cert["topology"],
        "weights": cert["weights"],
        "depth_vector": {
            str(vertex): rational_to_string(depth_vector[index])
            for index, vertex in enumerate(topology.vertices)
        },
        "exact_certificate": {
            "type": "dual_bound_plus_fixed_depth_objective_contradiction",
            "h2_lower_bound": rational_to_string(verification.original_min_lower_bound),
            "fixed_depth_objective": rational_to_string(check.depth_objective),
            "farkas_rhs": rational_to_string(check.farkas_rhs),
            "feasible": check.feasible,
            "explanation": (
                "The H2 dual gives objective >= 30, while the fixed depth vector "
                "forces the same objective to 59/2."
            ),
        },
        "numerical_simplex": numerical,
    }


def check_fixed_depth_infeasibility(
    lp: HereditaryLP,
    form: ExactStandardForm,
    dual_values: list[Fraction],
    depth_vector: tuple[Fraction, ...],
) -> FixedDepthCheck:
    if len(depth_vector) != lp.topology.n:
        raise ValueError("depth vector length must match topology.n")
    depth_objective = sum(
        lp.weights[vertex] * depth_vector[index]
        for index, vertex in enumerate(lp.topology.vertices)
    )
    lower_bound = -sum(form.rhs[row] * dual_values[row] for row in range(len(form.rows)))

    reduced_min = None
    for variable in range(len(lp.variables)):
        value = lp.objective_coefficients[variable] + sum(
            form.rows[row].get(variable, Fraction(0)) * dual_values[row]
            for row in range(len(form.rows))
        )
        reduced_min = value if reduced_min is None else min(reduced_min, value)
    if reduced_min is None or reduced_min < 0:
        raise ValueError("fixed-depth Farkas reduced-cost vector is not nonnegative")

    farkas_rhs = sum(form.rhs[row] * dual_values[row] for row in range(len(form.rows)))
    farkas_rhs += depth_objective
    return FixedDepthCheck(
        depth_objective=depth_objective,
        lower_bound=lower_bound,
        farkas_rhs=farkas_rhs,
        feasible=not (farkas_rhs < 0),
    )


def _run_fixed_depth_simplex(
    lp: HereditaryLP, depth_vector: tuple[Fraction, ...]
) -> dict[str, Any]:
    from .hereditary_lp import _simplex_maximize, _standard_form_for_simplex

    matrix, rhs, _objective = _standard_form_for_simplex(lp)
    for index, vertex in enumerate(lp.topology.vertices):
        row = [0.0] * len(lp.variables)
        for source in lp.topology.vertices:
            if source == vertex:
                continue
            component = tuple(sorted(lp.paths[(source, vertex)]))
            row[lp.variable_index[(component, source)]] += 1.0
        matrix.append(row)
        rhs.append(float(depth_vector[index]))
        matrix.append([-entry for entry in row])
        rhs.append(-float(depth_vector[index]))
    result = _simplex_maximize(matrix, rhs, [0.0] * len(lp.variables))
    return {
        "status": result.status,
        "message": result.message,
        "augmented_inequality_rows": len(matrix),
    }


def _check_primal(lp: HereditaryLP, values: list[Fraction]) -> Fraction:
    if len(values) != len(lp.variables):
        raise ValueError("primal dimension mismatch")
    if min(values, default=Fraction(0)) < 0:
        raise ValueError("primal contains negative z values")
    for component in lp.connected_subsets:
        total = sum(values[lp.variable_index[(component, root)]] for root in component)
        if total != 1:
            raise ValueError(f"simplex constraint failed for component {component}: {total}")
    for constraint in lp.heredity_constraints:
        lhs = values[lp.variable_index[(constraint.superset, constraint.root)]]
        rhs = values[lp.variable_index[(constraint.subset, constraint.root)]]
        if lhs > rhs:
            raise ValueError(f"heredity constraint failed: {constraint}")
    for constraint in lp.rectangle_constraints:
        expression = (
            values[lp.variable_index[(constraint.base, constraint.root)]]
            - values[lp.variable_index[(constraint.extension_a, constraint.root)]]
            - values[lp.variable_index[(constraint.extension_b, constraint.root)]]
            + values[lp.variable_index[(constraint.union, constraint.root)]]
        )
        if expression < 0:
            raise ValueError(f"H2 rectangle constraint failed: {constraint}")
    return sum(
        lp.objective_coefficients[index] * values[index]
        for index in range(len(lp.variables))
    )


def _check_dual(
    form: ExactStandardForm,
    values: list[Fraction],
    primal_objective: Fraction,
) -> CertificateVerification:
    if len(values) != len(form.rows):
        raise ValueError("dual dimension mismatch")
    if min(values, default=Fraction(0)) < 0:
        raise ValueError("dual contains negative row multipliers")
    max_deficit = Fraction(0)
    for variable in range(len(form.objective)):
        lhs = sum(
            form.rows[row].get(variable, Fraction(0)) * values[row]
            for row in range(len(form.rows))
        )
        deficit = form.objective[variable] - lhs
        if deficit > max_deficit:
            max_deficit = deficit
    if max_deficit > 0:
        raise ValueError(f"dual feasibility failed with deficit {max_deficit}")
    dual_objective = sum(form.rhs[row] * values[row] for row in range(len(form.rows)))
    lower_bound = -dual_objective
    return CertificateVerification(
        primal_objective=primal_objective,
        dual_max_objective=dual_objective,
        original_min_lower_bound=lower_bound,
        max_dual_deficit=max_deficit,
        matching_objective=lower_bound == primal_objective,
    )


def _primal_values_from_result(data: dict[str, Any], lp: HereditaryLP) -> list[Fraction]:
    values = [Fraction(0) for _ in lp.variables]
    certificate = data.get("rationalized_certificate", {})
    entries = certificate.get("nonzero_z_variables")
    if not isinstance(entries, list):
        raise ValueError("rationalized_certificate.nonzero_z_variables missing")
    for entry in entries:
        component = tuple(entry["component"])
        root = entry["root"]
        index = lp.variable_index[(component, root)]
        values[index] = parse_rational(entry["value"], "nonzero_z_variables.value")
    return values


def _parse_primal_values(raw: Any, lp: HereditaryLP) -> list[Fraction]:
    if not isinstance(raw, dict):
        raise ValueError("primal: missing object")
    values = [Fraction(0) for _ in lp.variables]
    entries = raw.get("nonzero_z_variables")
    if not isinstance(entries, list):
        raise ValueError("primal.nonzero_z_variables: must be a list")
    seen: set[int] = set()
    for entry in entries:
        component = tuple(entry["component"])
        root = entry["root"]
        index = lp.variable_index[(component, root)]
        if index in seen:
            raise ValueError("primal.nonzero_z_variables: duplicate variable")
        seen.add(index)
        values[index] = parse_rational(entry["value"], "primal.nonzero_z_variables.value")
    return values


def _parse_dual_values(raw: Any, form: ExactStandardForm) -> list[Fraction]:
    if not isinstance(raw, dict):
        raise ValueError("dual: missing object")
    values = [Fraction(0) for _ in form.rows]
    entries = raw.get("nonzero_rows")
    if not isinstance(entries, list):
        raise ValueError("dual.nonzero_rows: must be a list")
    seen: set[int] = set()
    for entry in entries:
        row = entry.get("row_index")
        if not isinstance(row, int) or isinstance(row, bool):
            raise ValueError("dual.nonzero_rows.row_index: must be an integer")
        if row < 0 or row >= len(form.rows):
            raise ValueError("dual.nonzero_rows.row_index: out of range")
        if row in seen:
            raise ValueError("dual.nonzero_rows: duplicate row")
        seen.add(row)
        if entry.get("row") != form.row_descriptors[row]:
            raise ValueError(f"dual.nonzero_rows[{row}].row descriptor mismatch")
        value = parse_rational(entry.get("value"), "dual.nonzero_rows.value")
        if value == 0:
            raise ValueError("dual.nonzero_rows.value: zero rows must be omitted")
        values[row] = value
    return values


def _nonzero_primal_entries(lp: HereditaryLP, values: list[Fraction]) -> list[dict[str, Any]]:
    return [
        {
            "component": list(component),
            "root": root,
            "value": rational_to_string(values[index]),
        }
        for index, (component, root) in enumerate(lp.variables)
        if values[index]
    ]


def _solve_square_linear_system(
    matrix: list[list[Fraction]], rhs: list[Fraction]
) -> list[Fraction]:
    size = len(rhs)
    if len(matrix) != size or any(len(row) != size for row in matrix):
        raise ValueError("linear system must be square")
    augmented = [list(row) + [rhs[row_index]] for row_index, row in enumerate(matrix)]
    for column in range(size):
        pivot = None
        for row in range(column, size):
            if augmented[row][column] != 0:
                pivot = row
                break
        if pivot is None:
            raise ValueError(f"basis reconstruction system is singular at column {column}")
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


def _check_basis_partition(
    basis: list[int], nonbasis: list[int], variable_count: int, row_count: int
) -> None:
    expected = set(range(variable_count + row_count)) | {-1}
    actual = set(basis) | set(nonbasis)
    if len(basis) != row_count:
        raise ValueError("basis length must equal inequality row count")
    if len(set(basis)) != len(basis):
        raise ValueError("basis contains duplicate indices")
    if len(set(nonbasis)) != len(nonbasis):
        raise ValueError("nonbasis contains duplicate indices")
    if set(basis) & set(nonbasis):
        raise ValueError("basis and nonbasis overlap")
    if actual != expected:
        raise ValueError("basis/nonbasis partition does not cover all variables")


def _parse_int_list(raw: Any, field: str) -> list[int]:
    if not isinstance(raw, list):
        raise ValueError(f"{field}: must be a list")
    result: list[int] = []
    for index, value in enumerate(raw):
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(f"{field}[{index}]: must be an integer")
        result.append(value)
    return result


def _rectangle_key_to_dict(
    key: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...], tuple[int, ...], int]
) -> dict[str, Any]:
    base, extension_a, extension_b, union, root = key
    return {
        "base": list(base),
        "extension_a": list(extension_a),
        "extension_b": list(extension_b),
        "union": list(union),
        "root": root,
    }


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top-level JSON value must be an object")
    return data


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _skz_h2_lp() -> HereditaryLP:
    return build_hereditary_lp(
        TreeTopology.from_dict(SKZ_LONG_STAR_TOPOLOGY),
        SKZ_LONG_STAR_WEIGHTS,
        relaxation="h2",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m scripts.stt_checker.h2_dual_certificate"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser("audit-rectangles")
    audit_parser.add_argument("--output", type=Path)

    reconstruct_parser = subparsers.add_parser("reconstruct")
    reconstruct_parser.add_argument("--result-json", type=Path, default=DEFAULT_H2_RESULT)
    reconstruct_parser.add_argument("--certificate", type=Path, default=DEFAULT_DUAL_CERT)

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("certificate", type=Path, nargs="?", default=DEFAULT_DUAL_CERT)

    fixed_parser = subparsers.add_parser("fixed-d")
    fixed_parser.add_argument("--certificate", type=Path, default=DEFAULT_DUAL_CERT)
    fixed_parser.add_argument("--output", type=Path, default=DEFAULT_FIXED_D_RESULT)
    fixed_parser.add_argument(
        "--run-numerical",
        action="store_true",
        help="also run the slow numerical simplex feasibility test",
    )

    args = parser.parse_args(argv)

    if args.command == "audit-rectangles":
        audit = audit_h2_rectangle_enumeration(_skz_h2_lp())
        if args.output is not None:
            _write_json(args.output, audit)
        print(json.dumps(audit, indent=2, sort_keys=True))
        return 0 if audit["passes"] else 1

    if args.command == "reconstruct":
        certificate = reconstruct_certificate_from_result(args.result_json)
        verify_certificate(certificate)
        _write_json(args.certificate, certificate)
        print(
            "wrote "
            f"{args.certificate} with primal objective "
            f"{certificate['primal']['objective']} and dual lower bound "
            f"{certificate['dual']['original_min_lower_bound']}"
        )
        return 0

    if args.command == "verify":
        verification = verify_certificate_file(args.certificate)
        print(
            "verified H2 certificate: primal="
            f"{rational_to_string(verification.primal_objective)} "
            "dual_max="
            f"{rational_to_string(verification.dual_max_objective)} "
            "lower_bound="
            f"{rational_to_string(verification.original_min_lower_bound)}"
        )
        return 0

    if args.command == "fixed-d":
        result = fixed_depth_certificate(
            args.certificate,
            run_numerical=args.run_numerical,
        )
        _write_json(args.output, result)
        exact = result["exact_certificate"]
        print(
            "fixed-D feasible="
            f"{exact['feasible']} fixed_objective={exact['fixed_depth_objective']} "
            f"h2_lower_bound={exact['h2_lower_bound']} "
            f"farkas_rhs={exact['farkas_rhs']}"
        )
        if result["numerical_simplex"] is not None:
            numerical = result["numerical_simplex"]
            print(
                "numerical_simplex status="
                f"{numerical['status']} message={numerical['message']}"
            )
        return 0 if not exact["feasible"] else 1

    raise AssertionError(f"unhandled command {args.command!r}")


if __name__ == "__main__":
    raise SystemExit(main())
