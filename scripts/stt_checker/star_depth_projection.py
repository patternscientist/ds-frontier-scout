"""Star-specific first-hit hierarchy depth-projection experiments.

This module is intentionally computational infrastructure, not a theorem
claim.  It builds exact rational LP models for d-leaf stars, solves them with
the repo's small floating-point simplex, and then reconstructs exact primal
and dual certificates from the reported basis whenever possible.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
import json
from pathlib import Path
from typing import Any, Iterable

from .enumerate_stts import enumerate_stts
from .hereditary_lp import DEFAULT_TOLERANCE, _simplex_maximize
from .lp_feasibility import path_between
from .rationals import rational_to_string
from .star_audit import (
    depth_projection as audited_star4_depth_projection,
    feasibility_audit as audited_star4_feasibility_audit,
    negative_masses as audited_star4_negative_masses,
    star4_instance,
)
from .topology import TreeTopology


DEFAULT_REPORT = Path("reports/stt_star_depth_projection_v0.md")

Component = tuple[int, ...]
Variable = tuple[Component, int]
SparseRow = dict[int, Fraction]


@dataclass(frozen=True)
class StarSTTShape:
    prefix: tuple[int, ...]
    depth_vector: tuple[int, ...]
    component_roots: tuple[tuple[Component, int], ...]


@dataclass(frozen=True)
class HierarchyConstraint:
    order: int
    base: Component
    extensions: tuple[Component, ...]
    root: int
    coefficients: tuple[tuple[Variable, Fraction], ...]


@dataclass(frozen=True)
class StarHierarchyLP:
    d: int
    k: int | str
    topology: TreeTopology
    connected_subsets: tuple[Component, ...]
    variables: tuple[Variable, ...]
    variable_index: dict[Variable, int]
    objective_coefficients: tuple[Fraction, ...]
    hierarchy_constraints: tuple[HierarchyConstraint, ...]
    rows: tuple[SparseRow, ...]
    rhs: tuple[Fraction, ...]
    row_descriptors: tuple[dict[str, Any], ...]
    symmetric: bool = False
    symmetric_variable_labels: tuple[str, ...] = ()


@dataclass(frozen=True)
class ExactLPCertificate:
    objective: Fraction
    values: tuple[Fraction, ...]
    dual_values: tuple[Fraction, ...]
    basis: tuple[int, ...]
    nonbasis: tuple[int, ...]
    max_primal_violation: Fraction
    max_dual_deficit: Fraction

    @property
    def verified(self) -> bool:
        return self.max_primal_violation == 0 and self.max_dual_deficit == 0


@dataclass(frozen=True)
class ObjectiveResult:
    d: int
    k: int | str
    weights: tuple[Fraction, ...]
    family: str
    stt_optimum: Fraction
    h_optimum: Fraction
    gap: Fraction
    stt_witness: tuple[int, ...]
    certificate: ExactLPCertificate
    symmetric: bool = False

    @property
    def has_gap(self) -> bool:
        return self.gap < 0


@lru_cache(maxsize=None)
def star_topology(d: int) -> TreeTopology:
    if d < 1:
        raise ValueError("star leaf count d must be positive")
    return TreeTopology.from_dict(
        {
            "n": d + 1,
            "vertices": list(range(d + 1)),
            "edges": [[0, leaf] for leaf in range(1, d + 1)],
        }
    )


@lru_cache(maxsize=None)
def star_connected_subsets(d: int) -> tuple[Component, ...]:
    leaves = tuple(range(1, d + 1))
    connected: list[Component] = [(0,), *[(leaf,) for leaf in leaves]]
    for size in range(1, d + 1):
        for subset in combinations(leaves, size):
            connected.append((0, *subset))
    return tuple(sorted(connected, key=lambda item: (len(item), item)))


@lru_cache(maxsize=None)
def structural_star_stts(d: int) -> tuple[StarSTTShape, ...]:
    """Enumerate star STTs as an ordered leaf prefix followed by the center."""

    leaves = tuple(range(1, d + 1))
    shapes: list[StarSTTShape] = []
    for prefix_length in range(d + 1):
        for prefix in _permutations_of_length(leaves, prefix_length):
            depths = [0 for _ in range(d + 1)]
            component_roots: list[tuple[Component, int]] = []
            remaining = set(range(d + 1))
            for depth, leaf in enumerate(prefix):
                component = tuple(sorted(remaining))
                component_roots.append((component, leaf))
                depths[leaf] = depth
                remaining.remove(leaf)
            center_depth = prefix_length
            component_roots.append((tuple(sorted(remaining)), 0))
            depths[0] = center_depth
            remaining.remove(0)
            for leaf in sorted(remaining):
                component_roots.append(((leaf,), leaf))
                depths[leaf] = center_depth + 1
            shapes.append(
                StarSTTShape(
                    prefix=prefix,
                    depth_vector=tuple(depths),
                    component_roots=tuple(component_roots),
                )
            )
    return tuple(shapes)


def verify_structural_stts(d: int) -> bool:
    topology = star_topology(d)
    structural = Counter(shape.depth_vector for shape in structural_star_stts(d))
    generic = Counter(
        tuple(result.depth[vertex] for vertex in topology.vertices)
        for result in enumerate_stts(topology, depth_base=0, max_count=1_000_000)
    )
    return structural == generic


def stt_depth_optimum(
    d: int, weights: Iterable[Fraction | int]
) -> tuple[Fraction, tuple[int, ...]]:
    weight_tuple = tuple(Fraction(value) for value in weights)
    if len(weight_tuple) != d + 1:
        raise ValueError("weight vector length must be d+1")
    best_value: Fraction | None = None
    best_vector: tuple[int, ...] | None = None
    for shape in structural_star_stts(d):
        value = sum(weight_tuple[index] * shape.depth_vector[index] for index in range(d + 1))
        if best_value is None or value < best_value:
            best_value = value
            best_vector = shape.depth_vector
    if best_value is None or best_vector is None:
        raise ValueError("no star STTs enumerated")
    return best_value, best_vector


def build_star_hierarchy_lp(
    d: int,
    weights: Iterable[Fraction | int],
    k: int | str = 2,
) -> StarHierarchyLP:
    if k != "infty" and (not isinstance(k, int) or k < 1):
        raise ValueError("k must be a positive integer or 'infty'")
    if k == "infty":
        raise ValueError("use STT enumeration for the complete/infty baseline")

    topology = star_topology(d)
    connected = star_connected_subsets(d)
    variables = tuple((component, root) for component in connected for root in component)
    variable_index = {variable: index for index, variable in enumerate(variables)}
    objective = _depth_objective_coefficients(topology, variables, variable_index, weights)
    constraints = enumerate_union_difference_constraints(connected, max_order=k)
    rows, rhs, descriptors = _standard_rows(
        connected,
        variables,
        variable_index,
        constraints,
    )
    return StarHierarchyLP(
        d=d,
        k=k,
        topology=topology,
        connected_subsets=connected,
        variables=variables,
        variable_index=variable_index,
        objective_coefficients=objective,
        hierarchy_constraints=constraints,
        rows=rows,
        rhs=rhs,
        row_descriptors=descriptors,
    )


def build_symmetric_star_hierarchy_lp(
    d: int,
    center_weight: Fraction | int,
    leaf_weight: Fraction | int,
    k: int = 2,
) -> StarHierarchyLP:
    """Build the leaf-symmetrized LP for symmetric star objectives.

    Variables are ``c_s`` for the center root on a center-containing set with
    ``s`` leaves, and ``l_s`` for a leaf root in such a set.  Singleton leaf
    first-hit values are constants equal to 1 and are substituted away.
    """

    if k < 1:
        raise ValueError("k must be positive")
    labels = tuple([f"c_{s}" for s in range(d + 1)] + [f"l_{s}" for s in range(1, d + 1)])
    label_index = {label: index for index, label in enumerate(labels)}
    variable_count = len(labels)
    variables: tuple[Variable, ...] = tuple(((index,), index) for index in range(variable_count))

    rows: list[SparseRow] = []
    rhs: list[Fraction] = []
    descriptors: list[dict[str, Any]] = []

    def add_row(row: SparseRow, bound: Fraction, descriptor: dict[str, Any]) -> None:
        clean = {index: value for index, value in row.items() if value}
        key = (tuple(sorted(clean.items())), bound)
        if key in seen_rows:
            return
        seen_rows.add(key)
        rows.append(clean)
        rhs.append(bound)
        descriptors.append(descriptor)

    seen_rows: set[tuple[tuple[tuple[int, Fraction], ...], Fraction]] = set()

    # Singleton center and every nonempty center-containing orbit have simplex
    # equalities.  c_0 = 1; c_s + s*l_s = 1.
    for sign in (Fraction(1), Fraction(-1)):
        add_row({label_index["c_0"]: sign}, sign, {"kind": "simplex", "orbit": "center_singleton", "sign": int(sign)})
    for s in range(1, d + 1):
        row = {label_index[f"c_{s}"]: Fraction(1), label_index[f"l_{s}"]: Fraction(s)}
        add_row(row, Fraction(1), {"kind": "simplex", "s": s, "sign": 1})
        add_row({index: -value for index, value in row.items()}, Fraction(-1), {"kind": "simplex", "s": s, "sign": -1})

    # H1 and Hk rows, generated directly in orbit variables.
    for root_type in ("center", "leaf", "singleton_leaf"):
        min_base = 0 if root_type in {"center", "singleton_leaf"} else 1
        for base_size in range(min_base, d + 1):
            if root_type == "singleton_leaf" and base_size != 0:
                continue
            if root_type == "leaf" and base_size == 0:
                continue
            for sup_size in range(max(base_size + 1, 1), d + 1):
                coeffs = _symmetric_term(root_type, base_size, d)
                _merge_coeffs(coeffs, _symmetric_term(root_type, sup_size, d), Fraction(-1))
                row, bound = _sym_coeffs_to_row(coeffs, label_index)
                add_row(
                    {index: -value for index, value in row.items()},
                    -bound,
                    {"kind": "h1", "root_type": root_type, "base_size": base_size, "sup_size": sup_size},
                )

    for order in range(2, k + 1):
        for root_type in ("center", "leaf", "singleton_leaf"):
            min_base = 0 if root_type in {"center", "singleton_leaf"} else 1
            for base_size in range(min_base, d + 1):
                if root_type == "singleton_leaf" and base_size != 0:
                    continue
                if root_type == "leaf" and base_size == 0:
                    continue
                pattern_base_size = 1 if root_type == "singleton_leaf" else base_size
                patterns = _union_size_patterns(d, pattern_base_size, order)
                for pattern in patterns:
                    coeffs: dict[str | None, Fraction] = {}
                    for mask, union_size in pattern.items():
                        sign = Fraction(-1 if _popcount(mask) % 2 else 1)
                        term_size = 0 if root_type == "singleton_leaf" and mask == 0 else union_size
                        _merge_coeffs(coeffs, _symmetric_term(root_type, term_size, d), sign)
                    row, bound = _sym_coeffs_to_row(coeffs, label_index)
                    if not row and bound >= 0:
                        continue
                    add_row(
                        {index: -value for index, value in row.items()},
                        -bound,
                        {
                            "kind": f"h{order}",
                            "root_type": root_type,
                            "base_size": base_size,
                            "union_sizes": {str(mask): size for mask, size in pattern.items()},
                        },
                    )

    weights = [Fraction(center_weight)] + [Fraction(leaf_weight)] * d
    full = build_star_hierarchy_lp(d, weights, k=1)
    full_objective = full.objective_coefficients
    objective = [Fraction(0) for _ in labels]
    constant = Fraction(0)
    for index, ((component, root), coefficient) in enumerate(zip(full.variables, full_objective)):
        label = _symmetric_label_for_variable(component, root)
        if label is None:
            constant += coefficient
        else:
            objective[label_index[label]] += coefficient
    if constant:
        raise ValueError("symmetric objective unexpectedly has a constant term")

    return StarHierarchyLP(
        d=d,
        k=k,
        topology=star_topology(d),
        connected_subsets=(),
        variables=variables,
        variable_index={variable: index for index, variable in enumerate(variables)},
        objective_coefficients=tuple(objective),
        hierarchy_constraints=(),
        rows=tuple(rows),
        rhs=tuple(rhs),
        row_descriptors=tuple(descriptors),
        symmetric=True,
        symmetric_variable_labels=labels,
    )


@lru_cache(maxsize=None)
def enumerate_union_difference_constraints(
    connected_subsets: tuple[Component, ...],
    max_order: int,
) -> tuple[HierarchyConstraint, ...]:
    connected_set = set(connected_subsets)
    subset_sets = {component: set(component) for component in connected_subsets}
    constraints: list[HierarchyConstraint] = []
    seen: set[tuple[int, int, tuple[tuple[Variable, Fraction], ...]]] = set()

    for base in connected_subsets:
        base_set = subset_sets[base]
        supersets = [
            component
            for component in connected_subsets
            if base_set.issubset(subset_sets[component]) and component != base
        ]
        for order in range(1, max_order + 1):
            for extensions in combinations(supersets, order):
                union_cache: dict[int, Component] = {0: base}
                valid = True
                for mask in range(1, 1 << order):
                    union_set = set(base_set)
                    for index, extension in enumerate(extensions):
                        if mask & (1 << index):
                            union_set.update(subset_sets[extension])
                    union = tuple(sorted(union_set))
                    if union not in connected_set:
                        valid = False
                        break
                    union_cache[mask] = union
                if not valid:
                    continue
                for root in base:
                    coeffs: dict[Variable, Fraction] = {}
                    for mask, union in union_cache.items():
                        sign = Fraction(-1 if _popcount(mask) % 2 else 1)
                        key = (union, root)
                        coeffs[key] = coeffs.get(key, Fraction(0)) + sign
                    coeff_tuple = tuple(sorted((key, value) for key, value in coeffs.items() if value))
                    if not coeff_tuple:
                        continue
                    unique_key = (order, root, coeff_tuple)
                    if unique_key in seen:
                        continue
                    seen.add(unique_key)
                    constraints.append(
                        HierarchyConstraint(
                            order=order,
                            base=base,
                            extensions=tuple(sorted(extensions)),
                            root=root,
                            coefficients=coeff_tuple,
                        )
                    )
    return tuple(constraints)


def solve_star_lp_exact(lp: StarHierarchyLP, tolerance: float = DEFAULT_TOLERANCE) -> ExactLPCertificate:
    matrix = [[0.0 for _ in lp.objective_coefficients] for _ in lp.rows]
    for row_index, row in enumerate(lp.rows):
        for col, value in row.items():
            matrix[row_index][col] = float(value)
    rhs = [float(value) for value in lp.rhs]
    maximize = [-float(value) for value in lp.objective_coefficients]
    result = _simplex_maximize(matrix, rhs, maximize, tolerance=tolerance)
    if result.status != 0:
        raise ValueError(f"simplex failed: status={result.status} message={result.message}")

    values = _exact_primal_from_basis(lp.rows, lp.rhs, result.basis, len(lp.objective_coefficients))
    dual_values = _exact_dual_from_basis(
        lp.rows,
        tuple(-value for value in lp.objective_coefficients),
        result.basis,
        result.nonbasis,
        len(lp.objective_coefficients),
    )
    objective = sum(lp.objective_coefficients[index] * values[index] for index in range(len(values)))
    max_primal_violation = _max_primal_violation(lp.rows, lp.rhs, values)
    max_dual_deficit = _max_dual_deficit(lp.rows, tuple(-value for value in lp.objective_coefficients), dual_values)
    if max_primal_violation != 0 or max_dual_deficit != 0:
        raise ValueError(
            "basis reconstruction did not verify exactly: "
            f"primal_violation={max_primal_violation}, dual_deficit={max_dual_deficit}"
        )
    dual_objective = sum(lp.rhs[row] * dual_values[row] for row in range(len(lp.rows)))
    if -dual_objective != objective:
        raise ValueError(
            f"dual objective mismatch: primal={objective}, lower={-dual_objective}"
        )
    return ExactLPCertificate(
        objective=objective,
        values=tuple(values),
        dual_values=tuple(dual_values),
        basis=result.basis,
        nonbasis=result.nonbasis,
        max_primal_violation=max_primal_violation,
        max_dual_deficit=max_dual_deficit,
    )


def evaluate_objective(
    d: int,
    weights: Iterable[Fraction | int],
    k: int,
    family: str,
    symmetric: bool = False,
) -> ObjectiveResult:
    weight_tuple = tuple(Fraction(value) for value in weights)
    stt_value, stt_vector = stt_depth_optimum(d, weight_tuple)
    if symmetric:
        if len(set(weight_tuple[1:])) != 1:
            raise ValueError("symmetric LP requires equal leaf weights")
        lp = build_symmetric_star_hierarchy_lp(d, weight_tuple[0], weight_tuple[1], k=k)
    else:
        lp = build_star_hierarchy_lp(d, weight_tuple, k=k)
    certificate = solve_star_lp_exact(lp)
    return ObjectiveResult(
        d=d,
        k=k,
        weights=weight_tuple,
        family=family,
        stt_optimum=stt_value,
        h_optimum=certificate.objective,
        gap=certificate.objective - stt_value,
        stt_witness=stt_vector,
        certificate=certificate,
        symmetric=symmetric,
    )


def structured_weight_vectors(d: int, small_bound: int = 3) -> tuple[tuple[str, tuple[Fraction, ...]], ...]:
    cases: list[tuple[str, tuple[Fraction, ...]]] = []
    cases.append(("center_heavy", tuple([Fraction(10)] + [Fraction(1)] * d)))
    cases.append(("symmetric_leaf_weights", tuple([Fraction(0)] + [Fraction(1)] * d)))
    for heavy_count in range(1, min(4, d) + 1):
        weights = [Fraction(1)] + [Fraction(1)] * d
        for leaf in range(1, heavy_count + 1):
            weights[leaf] = Fraction(8)
        cases.append((f"{heavy_count}_leaf_heavy", tuple(weights)))
    for heavy_count in range(0, d + 1):
        weights = [Fraction(1)] + [Fraction(3 if leaf <= heavy_count else 1) for leaf in range(1, d + 1)]
        cases.append((f"convex_heavy_count_{heavy_count}", tuple(weights)))
    for leaf_weights in _nondecreasing_tuples(d, small_bound):
        for center_weight in range(small_bound + 1):
            weights = (Fraction(center_weight),) + tuple(Fraction(value) for value in leaf_weights)
            if any(weights):
                cases.append((f"small_int_leq_{small_bound}", weights))
    dedup: dict[tuple[Fraction, ...], str] = {}
    for name, weights in cases:
        dedup.setdefault(weights, name)
    return tuple((name, weights) for weights, name in dedup.items())


def run_scout(
    full_d_max: int = 4,
    symmetric_d_max: int = 8,
    small_bound: int = 2,
) -> dict[str, Any]:
    structural_checks = {str(d): verify_structural_stts(d) for d in range(1, 6)}
    full_results: list[ObjectiveResult] = []
    for d in range(1, full_d_max + 1):
        for _name, weights in structured_weight_vectors(d, small_bound=small_bound):
            full_results.append(evaluate_objective(d, weights, 2, _name))

    h3_h4_results: list[ObjectiveResult] = []
    for d in range(1, min(5, full_d_max) + 1):
        probes = [
            ("center_heavy", tuple([Fraction(10)] + [Fraction(1)] * d)),
            ("symmetric_leaf_weights", tuple([Fraction(0)] + [Fraction(1)] * d)),
        ]
        if d >= 2:
            probes.append(("two_leaf_heavy", tuple([Fraction(1), Fraction(8), Fraction(8)] + [Fraction(1)] * (d - 2))))
        for k in (3, 4):
            for name, weights in probes:
                h3_h4_results.append(evaluate_objective(d, weights, k, name))

    symmetric_results: list[ObjectiveResult] = []
    for d in range(1, symmetric_d_max + 1):
        for center_weight, leaf_weight in ((0, 1), (1, 1), (4, 1), (10, 1), (1, 4)):
            weights = tuple([Fraction(center_weight)] + [Fraction(leaf_weight)] * d)
            full_check = False
            result = evaluate_objective(d, weights, 2, f"symmetric_{center_weight}_{leaf_weight}", symmetric=True)
            if d <= min(6, full_d_max):
                full_result = evaluate_objective(d, weights, 2, f"full_symmetric_{center_weight}_{leaf_weight}")
                full_check = full_result.h_optimum == result.h_optimum
            symmetric_results.append(result)
            if d <= min(6, full_d_max) and not full_check:
                raise ValueError(f"symmetric/full mismatch for d={d}, weights={weights}")

    all_results = full_results + h3_h4_results + symmetric_results
    gaps = [result for result in all_results if result.has_gap]
    return {
        "settings": {
            "full_d_max": full_d_max,
            "symmetric_d_max": symmetric_d_max,
            "small_bound": small_bound,
        },
        "structural_checks": structural_checks,
        "full_results": full_results,
        "h3_h4_results": h3_h4_results,
        "symmetric_results": symmetric_results,
        "gaps": gaps,
        "star4_regression": _star4_regression_summary(),
    }


def write_report(path: Path = DEFAULT_REPORT) -> dict[str, Any]:
    data = run_scout()
    report = _render_report(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report, encoding="utf-8")
    return {
        "report": str(path),
        "full_objectives": len(data["full_results"]),
        "h3_h4_objectives": len(data["h3_h4_results"]),
        "symmetric_objectives": len(data["symmetric_results"]),
        "gaps": len(data["gaps"]),
    }


def _depth_objective_coefficients(
    topology: TreeTopology,
    variables: tuple[Variable, ...],
    variable_index: dict[Variable, int],
    weights: Iterable[Fraction | int],
) -> tuple[Fraction, ...]:
    weight_tuple = tuple(Fraction(value) for value in weights)
    if len(weight_tuple) != topology.n:
        raise ValueError("weight vector length must match topology.n")
    objective = [Fraction(0) for _ in variables]
    for target in topology.vertices:
        for source in topology.vertices:
            if source == target:
                continue
            component = tuple(sorted(path_between(topology, source, target)))
            objective[variable_index[(component, source)]] += weight_tuple[target]
    return tuple(objective)


def _standard_rows(
    connected: tuple[Component, ...],
    variables: tuple[Variable, ...],
    variable_index: dict[Variable, int],
    constraints: tuple[HierarchyConstraint, ...],
) -> tuple[tuple[SparseRow, ...], tuple[Fraction, ...], tuple[dict[str, Any], ...]]:
    rows: list[SparseRow] = []
    rhs: list[Fraction] = []
    descriptors: list[dict[str, Any]] = []

    for component in connected:
        row = {variable_index[(component, root)]: Fraction(1) for root in component}
        rows.append(row)
        rhs.append(Fraction(1))
        descriptors.append({"kind": "simplex_upper", "component": list(component)})
        rows.append({index: -value for index, value in row.items()})
        rhs.append(Fraction(-1))
        descriptors.append({"kind": "simplex_lower", "component": list(component)})

    for constraint in constraints:
        row: SparseRow = {}
        for variable, coefficient in constraint.coefficients:
            row[variable_index[variable]] = row.get(variable_index[variable], Fraction(0)) - coefficient
        rows.append({index: value for index, value in row.items() if value})
        rhs.append(Fraction(0))
        descriptors.append(
            {
                "kind": f"h{constraint.order}",
                "base": list(constraint.base),
                "extensions": [list(extension) for extension in constraint.extensions],
                "root": constraint.root,
            }
        )

    return tuple(rows), tuple(rhs), tuple(descriptors)


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
    basic_originals = [index for index in basis if 0 <= index < variable_count]
    nonbasic_slack_rows = [
        index - variable_count
        for index in range(variable_count, variable_count + row_count)
        if index not in set(basis)
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
            "basis shape is not reconstructible by the sparse slack shortcut: "
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
        lhs = sum(rows[row].get(variable, Fraction(0)) * dual_values[row] for row in range(len(rows)))
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


def _permutations_of_length(items: tuple[int, ...], length: int) -> Iterable[tuple[int, ...]]:
    if length == 0:
        yield ()
        return
    for index, item in enumerate(items):
        rest = items[:index] + items[index + 1 :]
        for suffix in _permutations_of_length(rest, length - 1):
            yield (item, *suffix)


def _popcount(mask: int) -> int:
    return mask.bit_count()


def _nondecreasing_tuples(length: int, max_value: int) -> Iterable[tuple[int, ...]]:
    if length == 0:
        yield ()
        return
    for first in range(max_value + 1):
        for suffix in _nondecreasing_tuples(length - 1, max_value):
            if not suffix or first <= suffix[0]:
                yield (first, *suffix)


def _symmetric_label_for_variable(component: Component, root: int) -> str | None:
    if len(component) == 1 and component[0] != 0:
        return None
    if 0 not in component:
        raise ValueError("unexpected noncenter nonsingleton connected set")
    s = len(component) - 1
    if root == 0:
        return f"c_{s}"
    return f"l_{s}"


def _symmetric_term(root_type: str, size: int, d: int) -> dict[str | None, Fraction]:
    if size < 0 or size > d:
        raise ValueError("invalid orbit size")
    if root_type == "singleton_leaf" and size == 0:
        return {None: Fraction(1)}
    if root_type == "singleton_leaf":
        return {f"l_{size}": Fraction(1)}
    if root_type == "leaf" and size == 0:
        raise ValueError("leaf root cannot live in size-0 center set")
    if root_type == "leaf" and size == 1:
        # This may be either the singleton leaf base or a center+one-leaf set.
        # The caller uses this term for center-containing supersets, except
        # base singleton constants are handled by passing size=0 nowhere.
        return {"l_1": Fraction(1)}
    if root_type == "leaf":
        return {f"l_{size}": Fraction(1)}
    return {f"c_{size}": Fraction(1)}


def _merge_coeffs(
    target: dict[str | None, Fraction],
    source: dict[str | None, Fraction],
    scale: Fraction,
) -> None:
    for key, value in source.items():
        target[key] = target.get(key, Fraction(0)) + scale * value


def _sym_coeffs_to_row(
    coeffs: dict[str | None, Fraction], label_index: dict[str, int]
) -> tuple[SparseRow, Fraction]:
    row: SparseRow = {}
    constant = coeffs.get(None, Fraction(0))
    for label, value in coeffs.items():
        if label is None or value == 0:
            continue
        row[label_index[label]] = row.get(label_index[label], Fraction(0)) + value
    return row, -constant


@lru_cache(maxsize=None)
def _union_size_patterns(d: int, base_size: int, order: int) -> tuple[dict[int, int], ...]:
    """All possible union-size maps for ``order`` supersets of a base orbit."""

    capacity = d - base_size
    patterns: set[tuple[tuple[int, int], ...]] = set()
    boxes = tuple(range(1, 1 << order))

    def rec(box_index: int, remaining: int, counts: dict[int, int]) -> None:
        if box_index == len(boxes):
            for unused in range(remaining + 1):
                del unused
                union_sizes = {0: base_size}
                for mask in boxes:
                    size = base_size
                    for atom, count in counts.items():
                        if atom & mask:
                            size += count
                    union_sizes[mask] = size
                # Every chosen extension should be a proper superset for the
                # order-k generator; lower-order consequences are generated
                # separately.
                singleton_masks = [1 << index for index in range(order)]
                if all(union_sizes[mask] > base_size for mask in singleton_masks):
                    patterns.add(tuple(sorted(union_sizes.items())))
            return
        atom = boxes[box_index]
        for count in range(remaining + 1):
            if count:
                counts[atom] = count
            elif atom in counts:
                del counts[atom]
            rec(box_index + 1, remaining - count, counts)
        counts.pop(atom, None)

    rec(0, capacity, {})
    return tuple(dict(items) for items in sorted(patterns))


def _star4_regression_summary() -> dict[str, Any]:
    star = star4_instance()
    audit = audited_star4_feasibility_audit(star)
    negatives = audited_star4_negative_masses(star)
    depth = audited_star4_depth_projection(star)
    return {
        "h2_feasible": audit.feasible,
        "negative_masses": len(negatives),
        "center_mass": rational_to_string(negatives[0][1]) if negatives else "0",
        "depth": tuple(rational_to_string(value) for value in depth),
        "dominated_by_center_root": all(value >= target for value, target in zip(depth, (0, 1, 1, 1, 1))),
    }


def _format_fraction_tuple(values: Iterable[Fraction]) -> str:
    return "(" + ", ".join(rational_to_string(value) for value in values) + ")"


def _summarize_results(results: list[ObjectiveResult]) -> tuple[str, str]:
    if not results:
        return "none", "none"
    min_gap = min(result.gap for result in results)
    witness = next(result for result in results if result.gap == min_gap)
    return (
        f"{len(results)} objectives; smallest H-STT gap `{rational_to_string(min_gap)}`",
        (
            f"d={witness.d}, H{witness.k}, family={witness.family}, "
            f"weights={_format_fraction_tuple(witness.weights)}, "
            f"H={rational_to_string(witness.h_optimum)}, "
            f"STT={rational_to_string(witness.stt_optimum)}"
        ),
    )


def _render_report(data: dict[str, Any]) -> str:
    full_summary, full_witness = _summarize_results(data["full_results"])
    h34_summary, h34_witness = _summarize_results(data["h3_h4_results"])
    sym_summary, sym_witness = _summarize_results(data["symmetric_results"])
    gaps: list[ObjectiveResult] = data["gaps"]
    star4 = data["star4_regression"]

    lines: list[str] = []
    settings = data["settings"]
    lines.append("# STT Star Depth Projection v0")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append("This report tests whether the connected first-hit H2 failure on the 4-leaf star is only a full-`z` phenomenon or also appears after projecting to root-depth-0 STT depth vectors.  It is finite exact computation plus theorem scouting, not an all-stars proof.")
    lines.append("")
    lines.append("## Exact Model Definitions")
    lines.append("")
    lines.append("- The `d`-leaf star has center `0`, leaves `1..d`, and edges `{0,i}`.")
    lines.append("- Connected sets are exactly the singletons and the sets `{0} union S` with nonempty `S subseteq {1..d}`.")
    lines.append("- Variables are first-hit values `z[I,r]` for connected `I` and `r in I`.")
    lines.append("- H1 is simplex plus heredity.  Hk adds all union finite-difference inequalities through order `k`: `sum_B (-1)^|B| z[union_{i in B} A_i,r] >= 0`.")
    lines.append("- Depth projection uses `D_v = sum_{u != v} z[P(u,v),u]` with root-depth-0 convention.")
    lines.append("- The complete/`H_infty` baseline is exact STT enumeration.  On a star, an STT is an ordered prefix of leaves, followed by the center, then the remaining leaves as children.")
    lines.append("")
    lines.append("## Ranges Tested")
    lines.append("")
    lines.append(f"- Structural STT enumeration checked against generic recursive enumeration for `d=1..5`: `{data['structural_checks']}`.")
    lines.append(f"- Full H2 LP objectives: {full_summary}.")
    lines.append(f"- Full H3/H4 probe objectives: {h34_summary}.")
    lines.append(f"- Symmetric H2 objectives: {sym_summary}.")
    lines.append(f"- Full objective families include center-heavy, one/two/three/four-heavy leaves, symmetric leaf weights, convex heavy-count patterns, and all small integer weights up to `{settings['small_bound']}` modulo leaf symmetry through `d={settings['full_d_max']}`.")
    lines.append(f"- Symmetric objectives use `(center, leaf)` weights `(0,1)`, `(1,1)`, `(4,1)`, `(10,1)`, and `(1,4)` through `d={settings['symmetric_d_max']}`.")
    lines.append("")
    lines.append("## Full vs Symmetric Reduction")
    lines.append("")
    lines.append(f"For symmetric weights and `d<={min(6, settings['full_d_max'])}`, the orbit-variable H2 LP was compared against the full H2 LP.  All compared optima matched exactly.  The reduced variables are `c_s` for the center root on a center-containing set with `s` leaves and `l_s` for a leaf root in such a set; singleton leaf first-hit values are constants equal to `1`.")
    lines.append("")
    lines.append("## Depth-Projection Gap Search")
    lines.append("")
    if gaps:
        lines.append(f"Gap found: `{len(gaps)}` separating objectives.")
        first = gaps[0]
        lines.append(f"- Smallest recorded witness: `d={first.d}`, `H{first.k}`, family `{first.family}`.")
        lines.append(f"- Weights: `{_format_fraction_tuple(first.weights)}`.")
        lines.append(f"- H optimum `{rational_to_string(first.h_optimum)}` versus STT optimum `{rational_to_string(first.stt_optimum)}`.")
        lines.append(f"- STT witness vector: `{first.stt_witness}`.")
        lines.append("- The LP certificate includes exact primal values and exact dual multipliers reconstructed from the simplex basis.")
    else:
        lines.append("No depth-projection gap was found in the tested range.")
        lines.append(f"- Tightest full H2 case: {full_witness}.")
        lines.append(f"- Tightest H3/H4 probe case: {h34_witness}.")
        lines.append(f"- Tightest symmetric H2 case: {sym_witness}.")
        lines.append("- For every reported objective, an exact primal/dual certificate was reconstructed from the LP basis with zero primal violation, zero dual deficit, and matching objective value.")
    lines.append("")
    lines.append("## 4-Leaf z-Obstruction Regression")
    lines.append("")
    lines.append(f"- Audited 4-leaf obstruction H2-feasible in full `z`-space: `{star4['h2_feasible']}`.")
    lines.append(f"- Complete Mobius negative masses: `{star4['negative_masses']}`, including center mass `{star4['center_mass']}`.")
    lines.append(f"- Depth vector: `{star4['depth']}`.")
    lines.append(f"- Dominated by center-root STT vector `(0,1,1,1,1)`: `{star4['dominated_by_center_root']}`.")
    lines.append("")
    lines.append("## Candidate Theorem Statements")
    lines.append("")
    lines.append("1. Conservative candidate: For every fixed nonnegative weight vector tested here, the H2 depth optimum on a star equals the exact STT optimum.  This is only a finite computational statement.")
    lines.append("2. Structural candidate: The leaf-symmetrized H2 constraints may already imply the lower envelope of ordered-prefix STT depth vectors for symmetric weights on all stars.")
    lines.append("3. Strong candidate to audit: H2 has exact depth projection on all stars, even though H2 is not exact in full first-hit `z`-space.")
    lines.append("")
    lines.append("## Skeptical Audit")
    lines.append("")
    lines.append("- The tests do not prove all-star exactness; they only rule out witnesses in the enumerated objective families and sizes.")
    lines.append("- A nonsymmetric separating weight vector with larger support or larger coefficients could still exist.")
    lines.append("- H3/H4 were only probed where the full finite-difference generator was computationally modest.")
    lines.append("- The 4-leaf full-`z` obstruction remains real; the evidence here says it does not project to a depth obstruction.")
    lines.append("- Before promotion, the symmetric reduction should be independently reviewed and a hand-checkable dual pattern should be extracted from the exact multipliers.")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m scripts.stt_checker.star_depth_projection")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args(argv)
    result = write_report(args.report)
    print(
        "wrote {report}: full_objectives={full_objectives} "
        "h3_h4_objectives={h3_h4_objectives} "
        "symmetric_objectives={symmetric_objectives} gaps={gaps}".format(**result)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
