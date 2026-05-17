"""DS(k,2) H1 interface-residual checks.

This module is a targeted exact-rational audit for the corrected DS(k,2)
interface residual.  It is finite computational infrastructure only: the
search routines do not claim DS(k,2) exactness.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations_with_replacement, product
import json
import time
from pathlib import Path
from typing import Any, Iterable

from .double_star_depth_projection import (
    DoubleStarLPResult,
    double_star_spec,
    double_star_topology,
    solve_double_star_lp_exact,
    stt_depth_optimum,
    _expanded_full_values,
)
from .hereditary_lp import DEFAULT_TOLERANCE, build_hereditary_lp
from .lp_feasibility import path_between
from .rationals import rational_to_string


DEFAULT_REPORT = Path("reports/dsk2_interface_residual_v0.md")
DEFAULT_CERTIFICATES = Path("certificates/dsk2_interface_residual_examples.json")
IDENTITY_SCHEMA = "dsk2_interface_residual_v0"
VERIFIED_H1_CERTIFICATE_STATUS = (
    "verified_exact_primal_dual_after_floating_basis_reconstruction"
)

Component = tuple[int, ...]
Variable = tuple[Component, int]
WeightExpr = tuple[tuple[str, Fraction], ...]
SymbolicForm = dict[Variable | tuple[str], WeightExpr]


@dataclass(frozen=True)
class IdentityAudit:
    k: int
    connected_subsets: int
    variables: int
    simplex_rows: int
    heredity_rows: int
    identity_holds: bool
    residual_terms: tuple[dict[str, Any], ...]
    left_left_terms: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class SearchCase:
    family: str
    weights: tuple[Fraction, ...]
    stt_optimum: Fraction
    stt_depth_witness: tuple[int, ...]
    h1: DoubleStarLPResult
    dangerous_score: Fraction
    dangerous_profile: tuple[dict[str, Any], ...]

    @property
    def h1_gap(self) -> Fraction:
        return self.h1.optimum - self.stt_optimum

    @property
    def has_gap(self) -> bool:
        return self.h1_gap < 0


def dsk2_labels(k: int) -> dict[int, str]:
    spec = double_star_spec(k, 2)
    labels = {leaf: f"l_{index + 1}" for index, leaf in enumerate(spec.left_leaves)}
    labels[spec.a] = "a"
    labels[spec.b] = "b"
    labels[spec.right_leaves[0]] = "r"
    labels[spec.right_leaves[1]] = "s"
    return labels


def dsk2_weight_symbols(k: int) -> dict[int, str]:
    spec = double_star_spec(k, 2)
    symbols = {leaf: f"u_{index + 1}" for index, leaf in enumerate(spec.left_leaves)}
    symbols[spec.a] = "alpha"
    symbols[spec.b] = "beta"
    symbols[spec.right_leaves[0]] = "w_r"
    symbols[spec.right_leaves[1]] = "w_s"
    return symbols


def run_identity_audits(k_values: Iterable[int] = (1, 2, 3)) -> tuple[IdentityAudit, ...]:
    return tuple(check_interface_identity(k) for k in k_values)


def check_interface_identity(k: int) -> IdentityAudit:
    spec = double_star_spec(k, 2)
    topology = double_star_topology(k, 2)
    lp = build_hereditary_lp(topology, [1] * topology.n, relaxation="h1")
    labels = dsk2_labels(k)
    symbols = dsk2_weight_symbols(k)

    full_objective = _symbolic_h1_objective(k)
    right_objective = _symbolic_right_objective(k)
    residual = _empty_form()
    left_left_terms: list[dict[str, Any]] = []
    residual_terms: list[dict[str, Any]] = []

    _add_expr_to_form(residual, ("constant",), _sum_expr(symbols[leaf] for leaf in spec.left_leaves))

    for leaf_index, leaf in enumerate(spec.left_leaves, start=1):
        y_var = (_component((leaf, spec.a)), leaf)
        alpha_minus_u = _expr_add(_expr("alpha"), _expr(f"u_{leaf_index}", -1))
        _add_expr_to_form(residual, y_var, alpha_minus_u)
        row_terms: list[dict[str, str]] = [
            {
                "name": f"(alpha-u_{leaf_index}) y_{leaf_index}",
                "variable": _format_variable(labels, y_var),
                "coefficient": _format_expr(alpha_minus_u),
            }
        ]
        for right_vertex in (spec.b, *spec.right_leaves):
            right_symbol = symbols[right_vertex]
            eta_var = (_component(path_between(topology, right_vertex, leaf)), leaf)
            p_x_a = _component(path_between(topology, right_vertex, spec.a))
            p_x_l = _component(path_between(topology, right_vertex, leaf))
            eps_positive = (p_x_a, right_vertex)
            eps_negative = (p_x_l, right_vertex)
            _add_expr_to_form(residual, eta_var, _expr(right_symbol))
            _add_expr_to_form(residual, eps_positive, _expr(f"u_{leaf_index}", -1))
            _add_expr_to_form(residual, eps_negative, _expr(f"u_{leaf_index}"))
            row_terms.append(
                {
                    "name": f"{right_symbol} eta_{leaf_index},{labels[right_vertex]}",
                    "variable": _format_variable(labels, eta_var),
                    "coefficient": right_symbol,
                }
            )
            row_terms.append(
                {
                    "name": f"-u_{leaf_index} epsilon_{leaf_index},{labels[right_vertex]}",
                    "positive_variable": _format_variable(labels, eps_positive),
                    "negative_variable": _format_variable(labels, eps_negative),
                    "coefficient": f"-u_{leaf_index}",
                }
            )
        residual_terms.append({"left_leaf": labels[leaf], "terms": row_terms})

    for leaf in spec.left_leaves:
        leaf_symbol = symbols[leaf]
        for other in spec.left_leaves:
            if other == leaf:
                continue
            variable = (_component(path_between(topology, other, leaf)), other)
            _add_expr_to_form(residual, variable, _expr(leaf_symbol))
            left_left_terms.append(
                {
                    "target_left_leaf": labels[leaf],
                    "source_left_leaf": labels[other],
                    "variable": _format_variable(labels, variable),
                    "coefficient": leaf_symbol,
                }
            )

    combined = _form_add(right_objective, residual)
    difference = _form_add(full_objective, combined, scale=-1)
    identity_holds = not difference
    return IdentityAudit(
        k=k,
        connected_subsets=len(lp.connected_subsets),
        variables=len(lp.variables),
        simplex_rows=len(lp.connected_subsets),
        heredity_rows=len(lp.heredity_constraints),
        identity_holds=identity_holds,
        residual_terms=tuple(residual_terms),
        left_left_terms=tuple(left_left_terms),
    )


def search_dsk2_h1_gap(
    max_cases: int = 96,
    integer_bound: int = 2,
    dangerous_high: int = 10,
    tolerance: float = DEFAULT_TOLERANCE,
) -> dict[str, Any]:
    start = time.time()
    cases: list[SearchCase] = []
    failures: list[dict[str, Any]] = []
    seen: set[tuple[Fraction, ...]] = set()
    for family, weights in _candidate_weights(integer_bound, dangerous_high):
        if weights in seen:
            continue
        seen.add(weights)
        if len(cases) >= max_cases:
            break
        try:
            h1 = solve_double_star_lp_exact(2, 2, weights, "h1", tolerance=tolerance)
            stt_value, stt_depth = stt_depth_optimum(2, 2, weights)
        except Exception as exc:  # pragma: no cover - artifact records rare solver failure
            failures.append(
                {
                    "family": family,
                    "weights": _weights_json(2, weights),
                    "error": repr(exc),
                }
            )
            continue
        score, profile = dangerous_pattern_score(h1)
        case = SearchCase(
            family=family,
            weights=weights,
            stt_optimum=stt_value,
            stt_depth_witness=stt_depth,
            h1=h1,
            dangerous_score=score,
            dangerous_profile=profile,
        )
        cases.append(case)
        if case.has_gap:
            break

    identity = run_identity_audits((1, 2, 3))
    representatives = _representative_cases(cases)
    return {
        "schema": IDENTITY_SCHEMA,
        "settings": {
            "topology": "DS(2,2)",
            "weight_order": ["u_1", "u_2", "alpha", "beta", "w_r", "w_s"],
            "integer_bound": integer_bound,
            "dangerous_high": dangerous_high,
            "max_cases": max_cases,
            "cases_run": len(cases),
            "tolerance": tolerance,
        },
        "identity_audits": identity,
        "cases": cases,
        "representative_cases": representatives,
        "solver_failures": failures,
        "runtime_seconds": time.time() - start,
    }


def write_outputs(
    report_path: Path = DEFAULT_REPORT,
    certificate_path: Path = DEFAULT_CERTIFICATES,
    max_cases: int = 96,
    integer_bound: int = 2,
    dangerous_high: int = 10,
) -> dict[str, Any]:
    data = search_dsk2_h1_gap(
        max_cases=max_cases,
        integer_bound=integer_bound,
        dangerous_high=dangerous_high,
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    certificate_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(_render_report(data, certificate_path), encoding="utf-8")
    certificate_path.write_text(
        json.dumps(_certificates_json(data), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    gap_count = sum(1 for case in data["cases"] if case.has_gap)
    return {
        "report": str(report_path),
        "certificates": str(certificate_path),
        "cases": len(data["cases"]),
        "h1_gaps": gap_count,
        "identity_failures": sum(
            1 for audit in data["identity_audits"] if not audit.identity_holds
        ),
        "runtime_seconds": data["runtime_seconds"],
    }


def dangerous_pattern_score(
    h1: DoubleStarLPResult,
) -> tuple[Fraction, tuple[dict[str, Any], ...]]:
    spec = double_star_spec(2, 2)
    labels = dsk2_labels(2)
    values = _expanded_full_values(h1)

    def value(component: Iterable[int], root: int) -> Fraction:
        key = (_component(component), root)
        return values[h1.lp.full_variables.index(key)]

    score = Fraction(0)
    profile: list[dict[str, Any]] = []
    ab_a = value((spec.a, spec.b), spec.a)
    ab_b = value((spec.a, spec.b), spec.b)
    score += abs(ab_a - Fraction(1, 2)) + abs(ab_b - Fraction(1, 2))
    for leaf in spec.left_leaves:
        al_a = value((spec.a, leaf), spec.a)
        al_l = value((spec.a, leaf), leaf)
        lab_b = value((leaf, spec.a, spec.b), spec.b)
        lab_l = value((leaf, spec.a, spec.b), leaf)
        leaf_score = (
            abs(al_a - Fraction(1, 2))
            + abs(al_l - Fraction(1, 2))
            + abs(lab_b)
            + abs(lab_l - Fraction(1, 2))
        )
        score += leaf_score
        profile.append(
            {
                "leaf": labels[leaf],
                "z_ab_a": rational_to_string(ab_a),
                "z_ab_b": rational_to_string(ab_b),
                "z_al_a": rational_to_string(al_a),
                "z_al_l": rational_to_string(al_l),
                "z_lab_b": rational_to_string(lab_b),
                "z_lab_l": rational_to_string(lab_l),
                "leaf_score": rational_to_string(leaf_score),
            }
        )
    return score, tuple(profile)


def interface_values(h1: DoubleStarLPResult) -> tuple[dict[str, Any], ...]:
    spec = double_star_spec(2, 2)
    labels = dsk2_labels(2)
    topology = double_star_topology(2, 2)
    values = _expanded_full_values(h1)

    def value(component: Iterable[int], root: int) -> Fraction:
        key = (_component(component), root)
        return values[h1.lp.full_variables.index(key)]

    rows = []
    for leaf in spec.left_leaves:
        leaf_rows = []
        y = value((spec.a, leaf), leaf)
        for right_vertex in (spec.b, *spec.right_leaves):
            eta = value(path_between(topology, right_vertex, leaf), leaf)
            p_x_a = path_between(topology, right_vertex, spec.a)
            p_x_l = path_between(topology, right_vertex, leaf)
            epsilon = value(p_x_a, right_vertex) - value(p_x_l, right_vertex)
            leaf_rows.append(
                {
                    "x": labels[right_vertex],
                    "eta": rational_to_string(eta),
                    "epsilon": rational_to_string(epsilon),
                    "promotion_slack_y_minus_eta": rational_to_string(y - eta),
                }
            )
        rows.append(
            {
                "leaf": labels[leaf],
                "y": rational_to_string(y),
                "interfaces": leaf_rows,
            }
        )
    return tuple(rows)


def grouped_dual_rows(h1: DoubleStarLPResult) -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = {
        "interface_gap_rows_epsilon": [],
        "promotion_rows_eta_le_y": [],
        "left_left_coarea_rows": [],
        "right_star_defect_rows": [],
        "simplex_rows": [],
        "other_rows": [],
    }
    for active in h1.active_rows:
        row = active["row"]
        group = _classify_row(row)
        groups[group].append(
            {
                "row_index": active["row_index"],
                "value": active["value"],
                "orbit_size": active["orbit_size"],
                "row": row,
            }
        )
    return {
        "counts": {key: len(value) for key, value in groups.items()},
        "nonzero_rows_by_group": groups,
    }


def _candidate_weights(
    integer_bound: int,
    dangerous_high: int,
) -> Iterable[tuple[str, tuple[Fraction, ...]]]:
    # First probe objectives deliberately tilted toward the local interface
    # chamber: heavy left leaves, light centers, and modest right side.
    dangerous: list[tuple[int, int, int, int, int, int]] = []
    for u1 in range(dangerous_high, max(0, dangerous_high - 6), -1):
        for u2 in range(u1, max(0, dangerous_high - 6), -1):
            for alpha in range(0, 3):
                for beta in range(0, 3):
                    for right_sum in range(1, 5):
                        r = max(0, right_sum - 1)
                        s = right_sum - r
                        dangerous.append((u1, u2, alpha, beta, r, s))
    dangerous.sort(key=lambda w: (-(w[0] + w[1] - w[2] - w[3]), w))
    for weights in dangerous:
        yield "dangerous_left_heavy", tuple(Fraction(value) for value in weights)

    values = range(integer_bound + 1)
    left_pairs = combinations_with_replacement(values, 2)
    right_pairs = combinations_with_replacement(values, 2)
    for left in left_pairs:
        for alpha, beta in product(values, repeat=2):
            for right in right_pairs:
                weights = tuple(reversed(left)) + (alpha, beta) + tuple(reversed(right))
                if any(weights):
                    yield "small_integer_canonical", tuple(Fraction(value) for value in weights)


def _representative_cases(cases: list[SearchCase]) -> list[SearchCase]:
    reps: list[SearchCase] = []
    gaps = [case for case in cases if case.has_gap]
    if gaps:
        return [gaps[0]]
    verified = [
        case
        for case in cases
        if case.h1.certificate_status == VERIFIED_H1_CERTIFICATE_STATUS
    ]
    if not verified:
        return []
    dangerous = min(verified, key=lambda case: (case.dangerous_score, case.family, case.weights))
    reps.append(dangerous)
    left_heavy = max(
        verified,
        key=lambda case: (
            case.weights[0] + case.weights[1] - case.weights[2] - case.weights[3],
            -case.dangerous_score,
        ),
    )
    if left_heavy not in reps:
        reps.append(left_heavy)
    balanced = min(
        verified,
        key=lambda case: (
            abs(case.weights[0] - case.weights[1])
            + abs(case.weights[4] - case.weights[5]),
            case.dangerous_score,
        ),
    )
    if balanced not in reps:
        reps.append(balanced)
    for row_group in (
        "interface_gap_rows_epsilon",
        "promotion_rows_eta_le_y",
        "left_left_coarea_rows",
        "right_star_defect_rows",
    ):
        exposing = [
            case
            for case in verified
            if grouped_dual_rows(case.h1)["counts"][row_group] > 0
        ]
        if not exposing:
            continue
        best = max(
            exposing,
            key=lambda case: (
                grouped_dual_rows(case.h1)["counts"][row_group],
                -case.dangerous_score,
            ),
        )
        if best not in reps:
            reps.append(best)
    return reps


def _classify_row(row: dict[str, Any]) -> str:
    kind = row.get("kind")
    if kind in {"simplex_upper", "simplex_lower"}:
        return "simplex_rows"
    if kind != "heredity":
        return "other_rows"
    spec = double_star_spec(2, 2)
    superset = tuple(row.get("superset", ()))
    subset = tuple(row.get("subset", ()))
    root = row.get("root")
    left = set(spec.left_leaves)
    right_star = {spec.a, spec.b, *spec.right_leaves}
    for leaf in spec.left_leaves:
        for right_vertex in (spec.b, *spec.right_leaves):
            if (
                superset == _component(path_between(double_star_topology(2, 2), right_vertex, leaf))
                and subset == _component(path_between(double_star_topology(2, 2), right_vertex, spec.a))
                and root == right_vertex
            ):
                return "interface_gap_rows_epsilon"
            if (
                superset == _component(path_between(double_star_topology(2, 2), right_vertex, leaf))
                and subset == _component((spec.a, leaf))
                and root == leaf
            ):
                return "promotion_rows_eta_le_y"
    vertices = set(superset) | set(subset)
    if vertices.issubset(right_star):
        return "right_star_defect_rows"
    if vertices.issubset(left | {spec.a}) and len(vertices & left) >= 2:
        return "left_left_coarea_rows"
    return "other_rows"


def _symbolic_h1_objective(k: int) -> SymbolicForm:
    spec = double_star_spec(k, 2)
    topology = double_star_topology(k, 2)
    symbols = dsk2_weight_symbols(k)
    form = _empty_form()
    left_index = {leaf: index + 1 for index, leaf in enumerate(spec.left_leaves)}
    for target in topology.vertices:
        for source in topology.vertices:
            if source == target:
                continue
            if target in spec.left_leaves and source == spec.a:
                # The residual identity is stated after the edge-simplex
                # substitution z[{a,l_i},a] = 1 - z[{a,l_i},l_i].
                leaf_weight = _expr(symbols[target])
                y_var = (_component((target, spec.a)), target)
                _add_expr_to_form(form, ("constant",), leaf_weight)
                _add_expr_to_form(form, y_var, _expr(f"u_{left_index[target]}", -1))
                continue
            variable = (_component(path_between(topology, source, target)), source)
            _add_expr_to_form(form, variable, _expr(symbols[target]))
    return form


def _symbolic_right_objective(k: int) -> SymbolicForm:
    spec = double_star_spec(k, 2)
    topology = double_star_topology(k, 2)
    symbols = dsk2_weight_symbols(k)
    right_vertices = (spec.a, spec.b, *spec.right_leaves)
    form = _empty_form()
    collapsed_a_weight = _sum_expr(("alpha", *(symbols[leaf] for leaf in spec.left_leaves)))
    for target in right_vertices:
        target_weight = collapsed_a_weight if target == spec.a else _expr(symbols[target])
        for source in right_vertices:
            if source == target:
                continue
            variable = (_component(path_between(topology, source, target)), source)
            _add_expr_to_form(form, variable, target_weight)
    return form


def _empty_form() -> SymbolicForm:
    return {}


def _expr(symbol: str, coefficient: int | Fraction = 1) -> WeightExpr:
    value = Fraction(coefficient)
    if value == 0:
        return ()
    return ((symbol, value),)


def _sum_expr(symbols: Iterable[str]) -> WeightExpr:
    total: dict[str, Fraction] = {}
    for symbol in symbols:
        total[symbol] = total.get(symbol, Fraction(0)) + 1
    return _normalize_expr(total)


def _expr_add(first: WeightExpr, second: WeightExpr) -> WeightExpr:
    total: dict[str, Fraction] = {}
    for symbol, value in (*first, *second):
        total[symbol] = total.get(symbol, Fraction(0)) + value
    return _normalize_expr(total)


def _expr_scale(expr: WeightExpr, scale: Fraction) -> WeightExpr:
    return _normalize_expr({symbol: value * scale for symbol, value in expr})


def _normalize_expr(raw: dict[str, Fraction]) -> WeightExpr:
    return tuple(sorted((symbol, value) for symbol, value in raw.items() if value))


def _add_expr_to_form(form: SymbolicForm, key: Variable | tuple[str], expr: WeightExpr) -> None:
    if not expr:
        return
    form[key] = _expr_add(form.get(key, ()), expr)
    if not form[key]:
        del form[key]


def _form_add(first: SymbolicForm, second: SymbolicForm, scale: int = 1) -> SymbolicForm:
    result = dict(first)
    for key, expr in second.items():
        _add_expr_to_form(result, key, _expr_scale(expr, Fraction(scale)))
    return result


def _component(vertices: Iterable[int]) -> Component:
    return tuple(sorted(vertices))


def _format_expr(expr: WeightExpr) -> str:
    if not expr:
        return "0"
    parts = []
    for symbol, value in expr:
        if value == 1:
            parts.append(symbol)
        elif value == -1:
            parts.append(f"-{symbol}")
        else:
            parts.append(f"{rational_to_string(value)}*{symbol}")
    return " + ".join(parts).replace("+ -", "- ")


def _format_variable(labels: dict[int, str], variable: Variable) -> str:
    component, root = variable
    inside = ",".join(labels[v] for v in component)
    return f"z[{{{inside}}},{labels[root]}]"


def _weights_json(k: int, weights: tuple[Fraction, ...]) -> dict[str, str]:
    labels = dsk2_weight_symbols(k)
    return {labels[index]: rational_to_string(weights[index]) for index in range(len(weights))}


def _case_json(case: SearchCase, include_certificate: bool = False) -> dict[str, Any]:
    payload = {
        "family": case.family,
        "weights": _weights_json(2, case.weights),
        "stt_optimum": rational_to_string(case.stt_optimum),
        "stt_depth_witness": {
            dsk2_labels(2)[index]: case.stt_depth_witness[index]
            for index in range(len(case.stt_depth_witness))
        },
        "h1_optimum": rational_to_string(case.h1.optimum),
        "h1_gap": rational_to_string(case.h1_gap),
        "h1_certificate_status": case.h1.certificate_status,
        "dangerous_pattern_score": rational_to_string(case.dangerous_score),
        "dangerous_pattern_profile": list(case.dangerous_profile),
        "interface_values": list(interface_values(case.h1)),
    }
    if include_certificate:
        payload["dual_certificate_groups"] = grouped_dual_rows(case.h1)
        payload["active_dual_rows_total"] = len(case.h1.active_rows)
        payload["nonzero_primal_variables"] = _nonzero_primal_json(case.h1)
    return payload


def _nonzero_primal_json(h1: DoubleStarLPResult) -> list[dict[str, Any]]:
    labels = dsk2_labels(2)
    values = _expanded_full_values(h1)
    rows = []
    for index, (component, root) in enumerate(h1.lp.full_variables):
        if values[index]:
            rows.append(
                {
                    "component": [labels[v] for v in component],
                    "root": labels[root],
                    "value": rational_to_string(values[index]),
                }
            )
    return rows


def _audit_json(audit: IdentityAudit) -> dict[str, Any]:
    return {
        "k": audit.k,
        "topology": f"DS({audit.k},2)",
        "connected_subsets": audit.connected_subsets,
        "variables": audit.variables,
        "simplex_rows": audit.simplex_rows,
        "heredity_rows": audit.heredity_rows,
        "identity_holds": audit.identity_holds,
        "residual_terms": list(audit.residual_terms),
        "left_left_terms": list(audit.left_left_terms),
    }


def _certificates_json(data: dict[str, Any]) -> dict[str, Any]:
    cases: list[SearchCase] = data["cases"]
    representatives: list[SearchCase] = data["representative_cases"]
    gap_cases = [case for case in cases if case.has_gap]
    status_counts = Counter(case.h1.certificate_status for case in cases)
    return {
        "schema": data["schema"],
        "settings": data["settings"],
        "summary": {
            "cases": len(cases),
            "h1_gaps": len(gap_cases),
            "h1_certificate_status_counts": dict(sorted(status_counts.items())),
            "best_dangerous_score": (
                rational_to_string(min(case.dangerous_score for case in cases))
                if cases
                else None
            ),
            "runtime_seconds": data["runtime_seconds"],
        },
        "identity_audits": [_audit_json(audit) for audit in data["identity_audits"]],
        "gap_witnesses": [_case_json(case, include_certificate=True) for case in gap_cases],
        "representative_dangerous_chamber_certificates": [
            _case_json(case, include_certificate=True) for case in representatives
        ],
        "all_cases": [_case_json(case) for case in cases],
        "solver_failures": data["solver_failures"],
    }


def _render_report(data: dict[str, Any], certificate_path: Path) -> str:
    cases: list[SearchCase] = data["cases"]
    gap_cases = [case for case in cases if case.has_gap]
    representatives: list[SearchCase] = data["representative_cases"]
    status_counts = Counter(case.h1.certificate_status for case in cases)
    lines: list[str] = []
    lines.append("# DS(k,2) Interface Residual v0")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append("This is a finite exact-rational audit of the corrected DS(k,2) H1 interface residual for `k=1,2,3`, plus a bounded DS(2,2) H1 gap search. It does not claim DS(k,2) exactness.")
    lines.append("")
    lines.append("The checked residual keeps the per-left-leaf, per-right-vertex variables `eta_{i,x}` and `epsilon_{i,x}` for `x in {b,r,s}`. No H2, refined-Z, path monotonicity, or mixed-second-difference rows are used.")
    lines.append("")
    lines.append("## Algebraic Identity")
    lines.append("")
    lines.append("| topology | connected subsets | z variables | simplex rows | heredity rows | identity |")
    lines.append("|---|---:|---:|---:|---:|---|")
    for audit in data["identity_audits"]:
        lines.append(
            f"| DS({audit.k},2) | {audit.connected_subsets} | {audit.variables} | "
            f"{audit.simplex_rows} | {audit.heredity_rows} | {audit.identity_holds} |"
        )
    lines.append("")
    lines.append("The symbolic coefficient check verifies")
    lines.append("")
    lines.append("`H1Obj = RightObj_{alpha+U}(z|_{R*}) + U + sum_i R_i + LeftLeft(z)`")
    lines.append("")
    lines.append("where `LeftLeft(z) = sum_i u_i sum_{j != i} z[P(l_j,l_i),l_j]`. The JSON records every residual and `LeftLeft` term.")
    lines.append("")
    lines.append("## DS(2,2) Search")
    lines.append("")
    if gap_cases:
        first = gap_cases[0]
        lines.append("An exact rational H1 depth gap was found.")
        lines.append(f"- weights: `{_weights_json(2, first.weights)}`")
        lines.append(f"- STT optimum: `{rational_to_string(first.stt_optimum)}`")
        lines.append(f"- H1 optimum: `{rational_to_string(first.h1.optimum)}`")
        lines.append(f"- H1 gap: `{rational_to_string(first.h1_gap)}`")
    else:
        lines.append("No exact rational H1 depth gap was found in the bounded tested DS(2,2) objectives.")
    lines.append("")
    lines.append(f"- Cases run: `{len(cases)}`.")
    lines.append(f"- H1 certificate statuses: `{dict(sorted(status_counts.items()))}`.")
    lines.append(f"- Solver failures: `{len(data['solver_failures'])}`.")
    lines.append(f"- Runtime seconds: `{data['runtime_seconds']:.3f}`.")
    lines.append("")
    lines.append("## Dangerous-Chamber Certificates")
    lines.append("")
    if representatives:
        lines.append(f"Representative exact primal-dual certificates are saved in `{certificate_path}` and grouped by interface gap rows, promotion rows, left-left coarea rows, right-star defect rows, simplex rows, and other H1 rows.")
        lines.append("")
        lines.append("| family | weights | H1 gap | dangerous score | active dual row groups |")
        lines.append("|---|---|---:|---:|---|")
        for case in representatives:
            groups = grouped_dual_rows(case.h1)["counts"]
            lines.append(
                "| {family} | `{weights}` | {gap} | {score} | `{groups}` |".format(
                    family=case.family,
                    weights=_weights_json(2, case.weights),
                    gap=rational_to_string(case.h1_gap),
                    score=rational_to_string(case.dangerous_score),
                    groups=groups,
                )
            )
    else:
        lines.append("No representative certificate was available because no H1 solve produced a verified exact certificate.")
    lines.append("")
    lines.append("## Skeptical Audit")
    lines.append("")
    lines.append("- Finite no-gap results are not evidence of all-weights DS(2,2), DS(k,2), or double-star exactness.")
    lines.append("- The local dangerous pattern is only a chamber heuristic; a simplex optimum can tie to another primal face and miss the displayed half-integral coordinates.")
    lines.append("- The right marginal is not treated as a convex mixture of true right-star states. The residual explicitly keeps `eta` and `epsilon` interface variables.")
    lines.append("- Dual-row grouping is diagnostic, not a symbolic proof generator.")
    return "\n".join(lines) + "\n"


def main_check_identity(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python scripts/check_dsk2_interface_identity.py"
    )
    parser.add_argument("--json", type=Path, default=None)
    args = parser.parse_args(argv)
    audits = run_identity_audits((1, 2, 3))
    payload = {"schema": IDENTITY_SCHEMA, "identity_audits": [_audit_json(audit) for audit in audits]}
    if args.json is not None:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if all(audit.identity_holds for audit in audits) else 1


def main_search(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python scripts/search_dsk2_h1_gap.py")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--certificates", type=Path, default=DEFAULT_CERTIFICATES)
    parser.add_argument("--max-cases", type=int, default=96)
    parser.add_argument("--integer-bound", type=int, default=2)
    parser.add_argument("--dangerous-high", type=int, default=10)
    args = parser.parse_args(argv)
    result = write_outputs(
        report_path=args.report,
        certificate_path=args.certificates,
        max_cases=args.max_cases,
        integer_bound=args.integer_bound,
        dangerous_high=args.dangerous_high,
    )
    print(
        "wrote {report} and {certificates}: cases={cases} h1_gaps={h1_gaps} "
        "identity_failures={identity_failures} runtime_seconds={runtime_seconds:.3f}".format(
            **result
        )
    )
    return 0 if result["identity_failures"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main_search())
