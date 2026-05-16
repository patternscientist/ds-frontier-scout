"""Numerical solver for the hereditary first-hit STT relaxation.

The relaxation has variables z_{A,r} for every nonempty connected subset A of
the base tree and every r in A. It is intentionally separate from the
Golinsky-LP proof checker: this module solves a different clean-room LP.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import json
import math
from pathlib import Path
from typing import Any, Iterable

from .enumerate_stts import integer_optimum_by_enumeration
from .lp_feasibility import path_between
from .topology import TreeTopology


DEFAULT_TOLERANCE = 1e-9
SKZ_LONG_STAR_TOPOLOGY = {
    "n": 7,
    "vertices": [0, 1, 2, 3, 4, 5, 6],
    "edges": [[0, 1], [1, 2], [2, 3], [3, 4], [2, 5], [5, 6]],
}
SKZ_LONG_STAR_WEIGHTS = [3, 2, 0, 2, 3, 3, 10]


@dataclass(frozen=True)
class HeredityConstraint:
    superset: tuple[int, ...]
    subset: tuple[int, ...]
    root: int


@dataclass(frozen=True)
class HereditaryLP:
    topology: TreeTopology
    weights: dict[int, Fraction]
    connected_subsets: tuple[tuple[int, ...], ...]
    variables: tuple[tuple[tuple[int, ...], int], ...]
    variable_index: dict[tuple[tuple[int, ...], int], int]
    paths: dict[tuple[int, int], tuple[int, ...]]
    objective_coefficients: tuple[Fraction, ...]
    heredity_constraints: tuple[HeredityConstraint, ...]

    @property
    def simplex_constraint_count(self) -> int:
        return len(self.connected_subsets)


@dataclass(frozen=True)
class HereditaryLPDiagnostics:
    min_variable_value: float
    max_simplex_residual: float
    max_heredity_violation: float
    objective_recomputed: float

    def to_dict(self) -> dict[str, float]:
        return {
            "min_variable_value": self.min_variable_value,
            "max_simplex_residual": self.max_simplex_residual,
            "max_heredity_violation": self.max_heredity_violation,
            "objective_recomputed": self.objective_recomputed,
        }


@dataclass(frozen=True)
class HereditaryLPSolution:
    lp: HereditaryLP
    solver: str
    status: int
    message: str
    objective_value: float
    variable_values: tuple[float, ...]
    tolerance: float
    diagnostics: HereditaryLPDiagnostics

    @property
    def success(self) -> bool:
        return self.status == 0

    def value(self, component: Iterable[int], root: int) -> float:
        key = (tuple(sorted(component)), root)
        return self.variable_values[self.lp.variable_index[key]]

    def summary_dict(self) -> dict[str, Any]:
        return {
            "solver": self.solver,
            "status": self.status,
            "message": self.message,
            "objective_value": self.objective_value,
            "tolerance": self.tolerance,
            "diagnostics": self.diagnostics.to_dict(),
            "connected_subsets": len(self.lp.connected_subsets),
            "z_variables": len(self.lp.variables),
            "simplex_constraints": self.lp.simplex_constraint_count,
            "heredity_inequalities": len(self.lp.heredity_constraints),
        }

    def to_result_json(
        self,
        include_variables: bool = True,
        include_rationalized: bool = True,
    ) -> dict[str, Any]:
        payload = {
            "schema_version": "stt-hereditary-lp-result-v0",
            "relaxation": "clean_room_hereditary_first_hit",
            "result_type": "numerical_lp_solve",
            "topology": {
                "n": self.lp.topology.n,
                "vertices": list(self.lp.topology.vertices),
                "edges": [list(edge) for edge in self.lp.topology.edges],
            },
            "weights": {
                str(vertex): rational_to_string(self.lp.weights[vertex])
                for vertex in self.lp.topology.vertices
            },
            "summary": self.summary_dict(),
            "caveat": "Floating-point simplex output; not an exact rational proof.",
        }
        if include_variables:
            payload["z_variables"] = [
                {
                    "component": list(component),
                    "root": root,
                    "value": self.variable_values[index],
                }
                for index, (component, root) in enumerate(self.lp.variables)
            ]
        if include_rationalized:
            payload["rationalized_certificate"] = rationalize_solution(self).to_dict()
        return payload


@dataclass(frozen=True)
class RationalizedCertificate:
    values: tuple[Fraction, ...]
    exact_objective: Fraction
    min_variable_value: Fraction
    max_simplex_residual: Fraction
    max_heredity_violation: Fraction
    max_rounding_error: float
    feasible: bool
    lp: HereditaryLP

    def to_dict(self) -> dict[str, Any]:
        return {
            "max_rounding_error": self.max_rounding_error,
            "feasible_exactly_after_rationalization": self.feasible,
            "exact_objective": rational_to_string(self.exact_objective),
            "min_variable_value": rational_to_string(self.min_variable_value),
            "max_simplex_residual": rational_to_string(self.max_simplex_residual),
            "max_heredity_violation": rational_to_string(self.max_heredity_violation),
            "nonzero_z_variables": [
                {
                    "component": list(component),
                    "root": root,
                    "value": rational_to_string(self.values[index]),
                }
                for index, (component, root) in enumerate(self.lp.variables)
                if self.values[index] != 0
            ],
        }


@dataclass(frozen=True)
class StandardCaseResult:
    name: str
    topology: TreeTopology
    weights: dict[int, Fraction]
    hereditary_solution: HereditaryLPSolution
    true_optimum: Fraction
    expected: Fraction | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "name": self.name,
            "weights": {
                str(vertex): rational_to_string(self.weights[vertex])
                for vertex in self.topology.vertices
            },
            "true_root_depth_0_optimum": rational_to_string(self.true_optimum),
            "hereditary_objective": self.hereditary_solution.objective_value,
            "diagnostics": self.hereditary_solution.diagnostics.to_dict(),
            "counts": {
                "connected_subsets": len(self.hereditary_solution.lp.connected_subsets),
                "z_variables": len(self.hereditary_solution.lp.variables),
                "simplex_constraints": self.hereditary_solution.lp.simplex_constraint_count,
                "heredity_inequalities": len(
                    self.hereditary_solution.lp.heredity_constraints
                ),
            },
        }
        if self.expected is not None:
            payload["expected"] = rational_to_string(self.expected)
        return payload


def rational_to_string(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def parse_weight_vector(
    topology: TreeTopology, weights: Iterable[int | Fraction]
) -> dict[int, Fraction]:
    values = list(weights)
    if len(values) != topology.n:
        raise ValueError("weight vector length must match topology.n")
    result: dict[int, Fraction] = {}
    for vertex, value in zip(topology.vertices, values):
        weight = value if isinstance(value, Fraction) else Fraction(value)
        if weight < 0:
            raise ValueError("hereditary LP weights must be nonnegative")
        result[vertex] = weight
    return result


def enumerate_connected_subsets(topology: TreeTopology) -> tuple[tuple[int, ...], ...]:
    """Enumerate all nonempty connected vertex subsets in deterministic order."""

    subsets: list[tuple[int, ...]] = []
    vertices = tuple(topology.vertices)
    for mask in range(1, 1 << len(vertices)):
        subset = tuple(vertices[index] for index in range(len(vertices)) if mask & (1 << index))
        if topology.is_connected_subset(subset):
            subsets.append(subset)
    return tuple(sorted(subsets, key=lambda item: (len(item), item)))


def compute_tree_paths(
    topology: TreeTopology,
) -> dict[tuple[int, int], tuple[int, ...]]:
    """Return unique simple paths for all ordered pairs of vertices."""

    return {
        (source, target): path_between(topology, source, target)
        for source in topology.vertices
        for target in topology.vertices
    }


def build_hereditary_lp(
    topology: TreeTopology, weights: dict[int, Fraction] | Iterable[int | Fraction]
) -> HereditaryLP:
    if not isinstance(weights, dict):
        weights = parse_weight_vector(topology, weights)
    else:
        weights = {vertex: Fraction(weights[vertex]) for vertex in topology.vertices}
        if any(value < 0 for value in weights.values()):
            raise ValueError("hereditary LP weights must be nonnegative")

    connected_subsets = enumerate_connected_subsets(topology)
    variables = tuple(
        (component, root) for component in connected_subsets for root in component
    )
    variable_index = {variable: index for index, variable in enumerate(variables)}
    paths = compute_tree_paths(topology)

    objective = [Fraction(0) for _ in variables]
    for v in topology.vertices:
        for u in topology.vertices:
            if u == v:
                continue
            path_component = tuple(sorted(paths[(u, v)]))
            objective[variable_index[(path_component, u)]] += weights[v]

    heredity_constraints: list[HeredityConstraint] = []
    subset_sets = {component: set(component) for component in connected_subsets}
    for superset in connected_subsets:
        superset_set = subset_sets[superset]
        for subset in connected_subsets:
            if len(subset) >= len(superset):
                continue
            if not subset_sets[subset].issubset(superset_set):
                continue
            for root in subset:
                heredity_constraints.append(
                    HeredityConstraint(
                        superset=superset,
                        subset=subset,
                        root=root,
                    )
                )

    return HereditaryLP(
        topology=topology,
        weights=weights,
        connected_subsets=connected_subsets,
        variables=variables,
        variable_index=variable_index,
        paths=paths,
        objective_coefficients=tuple(objective),
        heredity_constraints=tuple(heredity_constraints),
    )


def solve_hereditary_lp(
    topology: TreeTopology,
    weights: dict[int, Fraction] | Iterable[int | Fraction],
    tolerance: float = DEFAULT_TOLERANCE,
) -> HereditaryLPSolution:
    lp = build_hereditary_lp(topology, weights)
    matrix, rhs, maximize_coefficients = _standard_form_for_simplex(lp)
    simplex_result = _simplex_maximize(
        matrix,
        rhs,
        maximize_coefficients,
        tolerance=tolerance,
    )
    objective_value = -simplex_result.objective_value
    diagnostics = compute_diagnostics(lp, simplex_result.solution)
    return HereditaryLPSolution(
        lp=lp,
        solver="pure_python_two_phase_simplex",
        status=simplex_result.status,
        message=simplex_result.message,
        objective_value=objective_value,
        variable_values=tuple(simplex_result.solution),
        tolerance=tolerance,
        diagnostics=diagnostics,
    )


def compute_diagnostics(
    lp: HereditaryLP, variable_values: tuple[float, ...] | list[float]
) -> HereditaryLPDiagnostics:
    values = list(variable_values)
    simplex_residual = 0.0
    for component in lp.connected_subsets:
        total = sum(values[lp.variable_index[(component, root)]] for root in component)
        simplex_residual = max(simplex_residual, abs(total - 1.0))

    heredity_violation = 0.0
    for constraint in lp.heredity_constraints:
        lhs = values[lp.variable_index[(constraint.superset, constraint.root)]]
        rhs = values[lp.variable_index[(constraint.subset, constraint.root)]]
        heredity_violation = max(heredity_violation, lhs - rhs)

    objective = sum(
        float(coefficient) * values[index]
        for index, coefficient in enumerate(lp.objective_coefficients)
    )
    return HereditaryLPDiagnostics(
        min_variable_value=min(values) if values else 0.0,
        max_simplex_residual=simplex_residual,
        max_heredity_violation=max(0.0, heredity_violation),
        objective_recomputed=objective,
    )


def rationalize_solution(
    solution: HereditaryLPSolution,
    max_denominator: int = 1_000_000,
) -> RationalizedCertificate:
    values = tuple(
        Fraction(value).limit_denominator(max_denominator)
        for value in solution.variable_values
    )
    lp = solution.lp
    objective = sum(
        lp.objective_coefficients[index] * values[index]
        for index in range(len(values))
    )
    simplex_residual = Fraction(0)
    for component in lp.connected_subsets:
        total = sum(
            (values[lp.variable_index[(component, root)]] for root in component),
            Fraction(0),
        )
        simplex_residual = max(simplex_residual, abs(total - 1))

    heredity_violation = Fraction(0)
    for constraint in lp.heredity_constraints:
        lhs = values[lp.variable_index[(constraint.superset, constraint.root)]]
        rhs = values[lp.variable_index[(constraint.subset, constraint.root)]]
        heredity_violation = max(heredity_violation, lhs - rhs)

    max_rounding_error = max(
        (
            abs(float(values[index]) - solution.variable_values[index])
            for index in range(len(values))
        ),
        default=0.0,
    )
    min_variable = min(values) if values else Fraction(0)
    max_positive_heredity_violation = max(Fraction(0), heredity_violation)
    return RationalizedCertificate(
        values=values,
        exact_objective=objective,
        min_variable_value=min_variable,
        max_simplex_residual=simplex_residual,
        max_heredity_violation=max_positive_heredity_violation,
        max_rounding_error=max_rounding_error,
        feasible=(
            min_variable >= 0
            and simplex_residual == 0
            and max_positive_heredity_violation == 0
        ),
        lp=lp,
    )


def _standard_form_for_simplex(
    lp: HereditaryLP,
) -> tuple[list[list[float]], list[float], list[float]]:
    variable_count = len(lp.variables)
    matrix: list[list[float]] = []
    rhs: list[float] = []

    for component in lp.connected_subsets:
        row = [0.0] * variable_count
        for root in component:
            row[lp.variable_index[(component, root)]] = 1.0
        matrix.append(row)
        rhs.append(1.0)
        matrix.append([-entry for entry in row])
        rhs.append(-1.0)

    for constraint in lp.heredity_constraints:
        row = [0.0] * variable_count
        row[lp.variable_index[(constraint.superset, constraint.root)]] = 1.0
        row[lp.variable_index[(constraint.subset, constraint.root)]] = -1.0
        matrix.append(row)
        rhs.append(0.0)

    maximize_coefficients = [-float(coefficient) for coefficient in lp.objective_coefficients]
    return matrix, rhs, maximize_coefficients


@dataclass(frozen=True)
class _SimplexResult:
    status: int
    message: str
    objective_value: float
    solution: tuple[float, ...]


def _simplex_maximize(
    matrix: list[list[float]],
    rhs: list[float],
    objective: list[float],
    tolerance: float = DEFAULT_TOLERANCE,
) -> _SimplexResult:
    """Solve max c*x subject to A*x <= b, x >= 0.

    This is a compact two-phase tableau simplex implementation with Bland-style
    tie breaking. It is only intended for the small diagnostic LPs in this repo.
    """

    row_count = len(rhs)
    variable_count = len(objective)
    if row_count != len(matrix):
        raise ValueError("matrix row count must match rhs length")
    if any(len(row) != variable_count for row in matrix):
        raise ValueError("all matrix rows must match objective length")

    basis = [variable_count + row for row in range(row_count)]
    nonbasis = list(range(variable_count)) + [-1]
    tableau = [
        [0.0 for _ in range(variable_count + 2)] for _ in range(row_count + 2)
    ]
    artificial_col = variable_count
    rhs_col = variable_count + 1

    for row in range(row_count):
        for col in range(variable_count):
            tableau[row][col] = matrix[row][col]
        tableau[row][artificial_col] = -1.0
        tableau[row][rhs_col] = rhs[row]
    for col in range(variable_count):
        tableau[row_count][col] = -objective[col]
    tableau[row_count + 1][artificial_col] = 1.0

    def pivot(pivot_row: int, pivot_col: int) -> None:
        pivot_value = tableau[pivot_row][pivot_col]
        if abs(pivot_value) <= tolerance:
            raise ArithmeticError("simplex attempted a numerically zero pivot")
        inverse = 1.0 / pivot_value
        for row in range(row_count + 2):
            if row == pivot_row:
                continue
            for col in range(variable_count + 2):
                if col == pivot_col:
                    continue
                tableau[row][col] -= (
                    tableau[pivot_row][col] * tableau[row][pivot_col] * inverse
                )
        for col in range(variable_count + 2):
            if col != pivot_col:
                tableau[pivot_row][col] *= inverse
        for row in range(row_count + 2):
            if row != pivot_row:
                tableau[row][pivot_col] *= -inverse
        tableau[pivot_row][pivot_col] = inverse
        basis[pivot_row], nonbasis[pivot_col] = (
            nonbasis[pivot_col],
            basis[pivot_row],
        )

    def simplex(phase: int) -> bool:
        objective_row = row_count + 1 if phase == 1 else row_count
        while True:
            entering_col: int | None = None
            for col in range(variable_count + 1):
                if phase == 2 and nonbasis[col] == -1:
                    continue
                if entering_col is None:
                    entering_col = col
                    continue
                candidate = (tableau[objective_row][col], nonbasis[col])
                incumbent = (
                    tableau[objective_row][entering_col],
                    nonbasis[entering_col],
                )
                if candidate < incumbent:
                    entering_col = col
            if entering_col is None or tableau[objective_row][entering_col] >= -tolerance:
                return True

            leaving_row: int | None = None
            for row in range(row_count):
                if tableau[row][entering_col] <= tolerance:
                    continue
                if leaving_row is None:
                    leaving_row = row
                    continue
                candidate_ratio = (
                    tableau[row][rhs_col] / tableau[row][entering_col],
                    basis[row],
                )
                incumbent_ratio = (
                    tableau[leaving_row][rhs_col]
                    / tableau[leaving_row][entering_col],
                    basis[leaving_row],
                )
                if candidate_ratio < incumbent_ratio:
                    leaving_row = row
            if leaving_row is None:
                return False
            pivot(leaving_row, entering_col)

    if row_count:
        most_negative_row = min(range(row_count), key=lambda row: tableau[row][rhs_col])
        if tableau[most_negative_row][rhs_col] < -tolerance:
            pivot(most_negative_row, artificial_col)
            phase_one_bounded = simplex(1)
            phase_one_value = tableau[row_count + 1][rhs_col]
            if not phase_one_bounded or phase_one_value < -tolerance:
                return _SimplexResult(
                    status=2,
                    message="infeasible in simplex phase I",
                    objective_value=math.nan,
                    solution=tuple(math.nan for _ in range(variable_count)),
                )
            if phase_one_value > tolerance:
                return _SimplexResult(
                    status=2,
                    message="infeasible in simplex phase I",
                    objective_value=math.nan,
                    solution=tuple(math.nan for _ in range(variable_count)),
                )
            for row in range(row_count):
                if basis[row] != -1:
                    continue
                pivot_col = None
                for col in range(variable_count):
                    if abs(tableau[row][col]) > tolerance:
                        pivot_col = col
                        break
                if pivot_col is not None:
                    pivot(row, pivot_col)

    if not simplex(2):
        return _SimplexResult(
            status=3,
            message="unbounded in simplex phase II",
            objective_value=math.inf,
            solution=tuple(math.nan for _ in range(variable_count)),
        )

    solution = [0.0 for _ in range(variable_count)]
    for row in range(row_count):
        if 0 <= basis[row] < variable_count:
            solution[basis[row]] = tableau[row][rhs_col]
    return _SimplexResult(
        status=0,
        message="optimal",
        objective_value=tableau[row_count][rhs_col],
        solution=tuple(solution),
    )


def standard_cases(tolerance: float = DEFAULT_TOLERANCE) -> list[StandardCaseResult]:
    cases = [
        (
            "edge_weights_1_1",
            TreeTopology.from_dict(
                {"n": 2, "vertices": [0, 1], "edges": [[0, 1]]}
            ),
            [1, 1],
            Fraction(1),
        ),
        (
            "p3_uniform",
            TreeTopology.from_dict(
                {"n": 3, "vertices": [0, 1, 2], "edges": [[0, 1], [1, 2]]}
            ),
            [1, 1, 1],
            Fraction(2),
        ),
        (
            "p3_endpoint_heavy",
            TreeTopology.from_dict(
                {"n": 3, "vertices": [0, 1, 2], "edges": [[0, 1], [1, 2]]}
            ),
            [2, 0, 3],
            Fraction(2),
        ),
        (
            "p3_good_root_failure_weights_1_4_4",
            TreeTopology.from_dict(
                {"n": 3, "vertices": [0, 1, 2], "edges": [[0, 1], [1, 2]]}
            ),
            [1, 4, 4],
            Fraction(5),
        ),
        (
            "skz_u_7_3_long_star",
            TreeTopology.from_dict(SKZ_LONG_STAR_TOPOLOGY),
            SKZ_LONG_STAR_WEIGHTS,
            Fraction(30),
        ),
    ]

    results: list[StandardCaseResult] = []
    for name, topology, weights_raw, expected in cases:
        weights = parse_weight_vector(topology, weights_raw)
        solution = solve_hereditary_lp(topology, weights, tolerance=tolerance)
        true_optimum, _best_stt, _count = integer_optimum_by_enumeration(
            topology,
            weights,
            depth_base=0,
            max_count=100_000,
        )
        results.append(
            StandardCaseResult(
                name=name,
                topology=topology,
                weights=weights,
                hereditary_solution=solution,
                true_optimum=true_optimum,
                expected=expected,
            )
        )
    return results


def _write_skz_result(path: Path, result: StandardCaseResult) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = result.hereditary_solution.to_result_json(
        include_variables=True,
        include_rationalized=True,
    )
    payload["comparison"] = {
        "true_root_depth_0_stt_optimum": rational_to_string(result.true_optimum),
        "expected_root_depth_0_stt_optimum": (
            rational_to_string(result.expected) if result.expected is not None else None
        ),
        "lp_minus_true_optimum": (
            result.hereditary_solution.objective_value - float(result.true_optimum)
        ),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m scripts.stt_checker.hereditary_lp"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print standard-case results as JSON instead of a compact table",
    )
    parser.add_argument(
        "--write-skz-json",
        type=Path,
        default=None,
        help="write the numerical SKZ solution/result JSON to this path",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=DEFAULT_TOLERANCE,
        help="simplex feasibility/optimality tolerance",
    )
    args = parser.parse_args(argv)

    results = standard_cases(tolerance=args.tolerance)

    if args.write_skz_json is not None:
        skz_result = next(
            result for result in results if result.name == "skz_u_7_3_long_star"
        )
        _write_skz_result(args.write_skz_json, skz_result)

    if args.json:
        print(json.dumps([result.to_dict() for result in results], indent=2, sort_keys=True))
        return 0

    for result in results:
        solution = result.hereditary_solution
        expected_text = (
            f" expected={rational_to_string(result.expected)}"
            if result.expected is not None
            else ""
        )
        print(
            f"{result.name}: status={solution.status} objective="
            f"{solution.objective_value:.12g} true_root_depth_0="
            f"{rational_to_string(result.true_optimum)}{expected_text} "
            f"max_simplex_residual={solution.diagnostics.max_simplex_residual:.3g} "
            f"max_heredity_violation={solution.diagnostics.max_heredity_violation:.3g}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
