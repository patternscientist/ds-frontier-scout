"""Exact rational normal-cone scan for the reduced DS(2,1) functional.

The reduced double-star coupling functional is represented by the exact
extended LP in :mod:`double_star_coupling_functional`.  This module keeps the
normal-cone audit rational: floating simplex is used only to find a basis, and
all saved witnesses are reconstructed and checked over ``Fraction``.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
from math import comb
from pathlib import Path
from typing import Any, Iterable

from .double_star_coupling_functional import (
    ReducedCouplingLP,
    build_reduced_coupling_lp,
    solve_reduced_coupling_lp_exact,
)
from .double_star_depth_projection import stt_depth_optimum
from .hereditary_lp import DEFAULT_TOLERANCE, _simplex_maximize
from .rationals import rational_to_string
from .star_depth_projection import (
    _exact_primal_from_basis,
    _max_primal_violation,
)


DEFAULT_REPORT = Path("reports/stt_double_star_ds21_normal_cones_v0.md")
DEFAULT_CERTIFICATES = Path(
    "examples/stt_lp/ds21_normal_cones_v0_certificates.json"
)

WeightVector = tuple[Fraction, Fraction, Fraction, Fraction, Fraction]
SparseRow = dict[int, Fraction]


@dataclass(frozen=True)
class ExactFeasibilityResult:
    feasible: bool
    values: tuple[Fraction, ...] = ()
    max_violation: Fraction | None = None
    status: str = "not_run"


@dataclass(frozen=True)
class ExactOptimizationResult:
    feasible: bool
    optimum: Fraction | None = None
    values: tuple[Fraction, ...] = ()
    max_violation: Fraction | None = None
    status: str = "not_run"


@dataclass(frozen=True)
class FaceCertificate:
    face_id: str
    sample_weights: WeightVector
    sample_objective: Fraction
    stt_optimum: Fraction
    stt_depth_witness: tuple[int, ...]
    active_rows: tuple[int, ...]
    zero_variables: tuple[int, ...]
    normal_cone: ExactFeasibilityResult
    coherent_witness: ExactFeasibilityResult
    incoherent_margin: Fraction
    incoherent_kind: str
    sample_values: tuple[Fraction, ...]

    @property
    def outcome(self) -> str:
        if self.sample_objective < self.stt_optimum:
            return "reduced_lb_h1_counterexample"
        if self.coherent_witness.feasible or self.sample_objective == self.stt_optimum:
            return "exposed_incoherent_face_tied_with_coherent_deterministic_witness"
        return "unresolved_exposed_incoherent_face"


def run_scan(
    grid_bound: int = 3,
    tolerance: float = DEFAULT_TOLERANCE,
) -> dict[str, Any]:
    lp = build_reduced_coupling_lp(2, 1, (1, 1, 1, 1, 1))
    objective_by_weight = _objective_coefficient_matrix()
    arrangement = _arrangement_summary(lp)
    candidates: dict[tuple[tuple[int, ...], tuple[int, ...]], FaceCertificate] = {}
    unresolved: list[dict[str, Any]] = []

    for weights in _weight_grid(grid_bound):
        solved_lp, optimum, values, certificate, status, _active = (
            solve_reduced_coupling_lp_exact(2, 1, weights, tolerance=tolerance)
        )
        if status.startswith("verified_exact"):
            exact_values = values
        elif certificate is not None and certificate.verified:
            exact_values = certificate.values
        else:
            unresolved.append(
                {
                    "kind": "unverified_sample_basis",
                    "weights": _weights_json(weights),
                    "solver_status": status,
                }
            )
            continue
        active_rows = _active_rows(solved_lp, exact_values)
        zero_variables = tuple(
            index for index, value in enumerate(exact_values) if value == 0
        )
        key = (active_rows, zero_variables)
        if key in candidates:
            continue
        incoherent = _incoherent_margin(solved_lp, exact_values)
        if incoherent[0] >= 0:
            continue
        normal_cone = _normal_cone_feasibility(
            lp=lp,
            active_rows=active_rows,
            zero_variables=zero_variables,
            objective_by_weight=objective_by_weight,
            tolerance=tolerance,
        )
        if not normal_cone.feasible:
            unresolved.append(
                {
                    "kind": "normal_cone_lp_unverified_or_infeasible",
                    "weights": _weights_json(weights),
                    "active_rows": active_rows,
                    "zero_variables": zero_variables,
                    "status": normal_cone.status,
                }
            )
            continue
        stt_value, stt_depth = stt_depth_optimum(2, 1, weights)
        coherent = _optimal_face_feasibility(
            lp=solved_lp,
            optimum=optimum,
            extra_rows=_coherence_rows(solved_lp),
            tolerance=tolerance,
        )
        face_id = f"ds21-face-{len(candidates) + 1:04d}"
        candidates[key] = FaceCertificate(
            face_id=face_id,
            sample_weights=weights,
            sample_objective=optimum,
            stt_optimum=stt_value,
            stt_depth_witness=stt_depth,
            active_rows=active_rows,
            zero_variables=zero_variables,
            normal_cone=normal_cone,
            coherent_witness=coherent,
            incoherent_margin=incoherent[0],
            incoherent_kind=incoherent[1],
            sample_values=exact_values,
        )

    face_certificates = tuple(candidates.values())
    return {
        "schema": "stt_ds21_normal_cones_v0",
        "settings": {
            "grid_bound": grid_bound,
            "weight_order": ["u1", "u2", "alpha", "beta", "v"],
            "weight_cone": "u1 >= u2 >= 0, alpha >= 0, beta >= 0, v >= 0",
            "tolerance": tolerance,
        },
        "arrangement": arrangement,
        "lp": lp,
        "certificates": face_certificates,
        "unresolved": unresolved,
    }


def write_outputs(
    report_path: Path = DEFAULT_REPORT,
    certificate_path: Path = DEFAULT_CERTIFICATES,
    grid_bound: int = 3,
) -> dict[str, Any]:
    data = run_scan(grid_bound=grid_bound)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    certificate_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(_render_report(data, certificate_path), encoding="utf-8")
    certificate_path.write_text(
        json.dumps(_certificates_json(data), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    outcomes: dict[str, int] = {}
    for cert in data["certificates"]:
        outcomes[cert.outcome] = outcomes.get(cert.outcome, 0) + 1
    return {
        "report": str(report_path),
        "certificates": str(certificate_path),
        "faces": len(data["certificates"]),
        "outcomes": outcomes,
        "unresolved": len(data["unresolved"]) + len(data["arrangement"]["unresolved"]),
    }


def _objective_coefficient_matrix() -> tuple[tuple[Fraction, ...], ...]:
    """Return objective coefficients as linear forms in (u1,u2,alpha,beta,v)."""

    unit_weights = (
        (1, 0, 0, 0, 0),
        (0, 1, 0, 0, 0),
        (0, 0, 1, 0, 0),
        (0, 0, 0, 1, 0),
        (0, 0, 0, 0, 1),
    )
    columns: list[tuple[Fraction, ...]] = []
    for weights in unit_weights:
        lp = build_reduced_coupling_lp(2, 1, weights)
        columns.append(lp.objective)
    return tuple(tuple(column[index] for column in columns) for index in range(len(columns[0])))


def _weight_grid(bound: int) -> Iterable[WeightVector]:
    for u1, u2, alpha, beta, v in product(range(bound + 1), repeat=5):
        if not any((u1, u2, alpha, beta, v)):
            continue
        if u1 < u2:
            continue
        yield (
            Fraction(u1),
            Fraction(u2),
            Fraction(alpha),
            Fraction(beta),
            Fraction(v),
        )


def _active_rows(lp: ReducedCouplingLP, values: tuple[Fraction, ...]) -> tuple[int, ...]:
    active = []
    for row_index, (row, bound) in enumerate(zip(lp.rows, lp.rhs)):
        lhs = sum(row.get(col, Fraction(0)) * values[col] for col in row)
        if lhs == bound:
            active.append(row_index)
    return tuple(active)


def _profile_values(lp: ReducedCouplingLP, values: tuple[Fraction, ...]) -> dict[str, Fraction]:
    idx = lp.variable_index
    a1 = values[idx[("A_left", 0)]]
    a2 = values[idx[("A_left", 1)]]
    b1 = 1 - values[idx[("r", 0)]] - values[idx[("A_left", 0)]]
    b2 = 1 - values[idx[("r", 1)]] - values[idx[("A_left", 1)]]
    s_a = values[idx[("A_right", 4)]]
    s_b = 1 - values[idx[("s", 4)]] - values[idx[("A_right", 4)]]
    return {"a1": a1, "a2": a2, "b1": b1, "b2": b2, "S": s_a, "T": s_b}


def _incoherent_margin(
    lp: ReducedCouplingLP, values: tuple[Fraction, ...]
) -> tuple[Fraction, str]:
    profile = _profile_values(lp, values)
    margins = (
        (profile["a1"] - profile["a2"], "a1_minus_a2"),
        (profile["b1"] - profile["b2"], "b1_minus_b2"),
    )
    return min(margins, key=lambda item: item[0])


def _coherence_rows(lp: ReducedCouplingLP) -> tuple[tuple[SparseRow, Fraction, str], ...]:
    idx = lp.variable_index
    # Rows are in <= form.  a1 >= a2 becomes A2-A1 <= 0.
    row_a = {idx[("A_left", 1)]: Fraction(1), idx[("A_left", 0)]: Fraction(-1)}
    # b1 >= b2, with b_i = 1-r_i-A_i, becomes r1+A1-r2-A2 <= 0.
    row_b = {
        idx[("r", 0)]: Fraction(1),
        idx[("A_left", 0)]: Fraction(1),
        idx[("r", 1)]: Fraction(-1),
        idx[("A_left", 1)]: Fraction(-1),
    }
    return ((row_a, Fraction(0), "a1_ge_a2"), (row_b, Fraction(0), "b1_ge_b2"))


def _face_feasibility(
    lp: ReducedCouplingLP,
    active_rows: tuple[int, ...],
    zero_variables: tuple[int, ...],
    extra_rows: tuple[tuple[SparseRow, Fraction, str], ...] = (),
    tolerance: float = DEFAULT_TOLERANCE,
) -> ExactFeasibilityResult:
    rows: list[SparseRow] = list(lp.rows)
    rhs: list[Fraction] = list(lp.rhs)
    for row_index in active_rows:
        rows.append(lp.rows[row_index])
        rhs.append(lp.rhs[row_index])
        rows.append({col: -value for col, value in lp.rows[row_index].items()})
        rhs.append(-lp.rhs[row_index])
    for var_index in zero_variables:
        rows.append({var_index: Fraction(1)})
        rhs.append(Fraction(0))
    for row, bound, _name in extra_rows:
        rows.append(row)
        rhs.append(bound)
    return _exact_feasible(tuple(rows), tuple(rhs), len(lp.variables), tolerance)


def _optimal_face_feasibility(
    lp: ReducedCouplingLP,
    optimum: Fraction,
    extra_rows: tuple[tuple[SparseRow, Fraction, str], ...] = (),
    tolerance: float = DEFAULT_TOLERANCE,
) -> ExactFeasibilityResult:
    rows: list[SparseRow] = list(lp.rows)
    rhs: list[Fraction] = list(lp.rhs)
    objective_bound = optimum - lp.objective_constant
    objective_row = {
        index: coefficient
        for index, coefficient in enumerate(lp.objective)
        if coefficient
    }
    rows.append(objective_row)
    rhs.append(objective_bound)
    rows.append({index: -value for index, value in objective_row.items()})
    rhs.append(-objective_bound)
    for row, bound, _name in extra_rows:
        rows.append(row)
        rhs.append(bound)
    return _exact_feasible(tuple(rows), tuple(rhs), len(lp.variables), tolerance)


def _normal_cone_feasibility(
    lp: ReducedCouplingLP,
    active_rows: tuple[int, ...],
    zero_variables: tuple[int, ...],
    objective_by_weight: tuple[tuple[Fraction, ...], ...],
    tolerance: float = DEFAULT_TOLERANCE,
) -> ExactFeasibilityResult:
    # Variables: five weights, active row multipliers, zero-variable multipliers.
    weight_count = 5
    lambda_offset = weight_count
    mu_offset = lambda_offset + len(active_rows)
    total = mu_offset + len(zero_variables)
    rows: list[SparseRow] = []
    rhs: list[Fraction] = []

    # u2 - u1 <= 0.
    rows.append({1: Fraction(1), 0: Fraction(-1)})
    rhs.append(Fraction(0))

    # Normalize away the zero normal vector: sum weights + sum multipliers = 1.
    norm = {index: Fraction(1) for index in range(total)}
    rows.append(norm)
    rhs.append(Fraction(1))
    rows.append({index: -value for index, value in norm.items()})
    rhs.append(Fraction(-1))

    zero_to_mu = {var: pos for pos, var in enumerate(zero_variables)}
    for primal_var in range(len(lp.variables)):
        # KKT stationarity for minimization:
        # c(w) + A_I^T lambda - mu = 0.
        row: SparseRow = {}
        for weight_index in range(weight_count):
            coeff = objective_by_weight[primal_var][weight_index]
            if coeff:
                row[weight_index] = row.get(weight_index, Fraction(0)) + coeff
        for active_pos, row_index in enumerate(active_rows):
            coeff = lp.rows[row_index].get(primal_var, Fraction(0))
            if coeff:
                row[lambda_offset + active_pos] = (
                    row.get(lambda_offset + active_pos, Fraction(0)) + coeff
                )
        if primal_var in zero_to_mu:
            row[mu_offset + zero_to_mu[primal_var]] = (
                row.get(mu_offset + zero_to_mu[primal_var], Fraction(0)) - 1
            )
        rows.append(row)
        rhs.append(Fraction(0))
        rows.append({index: -value for index, value in row.items()})
        rhs.append(Fraction(0))
    return _exact_feasible(tuple(rows), tuple(rhs), total, tolerance)


def _exact_feasible(
    rows: tuple[SparseRow, ...],
    rhs: tuple[Fraction, ...],
    variable_count: int,
    tolerance: float,
) -> ExactFeasibilityResult:
    result = _solve_exact_lp(rows, rhs, (Fraction(0),) * variable_count, tolerance)
    return ExactFeasibilityResult(
        feasible=result.feasible,
        values=result.values,
        max_violation=result.max_violation,
        status=result.status,
    )


def _solve_exact_lp(
    rows: tuple[SparseRow, ...],
    rhs: tuple[Fraction, ...],
    objective: tuple[Fraction, ...],
    tolerance: float = DEFAULT_TOLERANCE,
) -> ExactOptimizationResult:
    matrix = [[0.0 for _ in range(len(objective))] for _ in rows]
    for row_index, row in enumerate(rows):
        for col, value in row.items():
            matrix[row_index][col] = float(value)
    result = _simplex_maximize(
        matrix,
        [float(value) for value in rhs],
        [-float(value) for value in objective],
        tolerance=tolerance,
    )
    if result.status != 0:
        return ExactOptimizationResult(False, status=result.message)
    try:
        values = tuple(_exact_primal_from_basis(rows, rhs, result.basis, len(objective)))
    except ValueError as exc:
        rationalized = tuple(
            Fraction(value).limit_denominator(1_000_000)
            for value in result.solution
        )
        violation = _max_primal_violation(rows, rhs, list(rationalized))
        if violation == 0:
            optimum = sum(objective[index] * rationalized[index] for index in range(len(objective)))
            return ExactOptimizationResult(
                True,
                optimum=optimum,
                values=rationalized,
                max_violation=violation,
                status="verified_exact_after_solution_rationalization",
            )
        return ExactOptimizationResult(
            False,
            max_violation=violation,
            status=f"basis_reconstruction_failed: {exc}",
        )
    violation = _max_primal_violation(rows, rhs, list(values))
    if violation != 0:
        return ExactOptimizationResult(
            False,
            values=values,
            max_violation=violation,
            status="exact_basis_primal_violation",
        )
    optimum = sum(objective[index] * values[index] for index in range(len(objective)))
    return ExactOptimizationResult(
        True,
        optimum=optimum,
        values=values,
        max_violation=violation,
        status="verified_exact_primal_from_basis",
    )


def _arrangement_summary(lp: ReducedCouplingLP) -> dict[str, Any]:
    named_hyperplanes = [
        "p1=p2",
        "A_left[xi]=A_right[y1] for i=1,2",
        "B_left[xi]=B_right[y1] for i=1,2",
        "r_i=p_i",
        "A_left[xi]=0",
        "A_left[xi]=theta",
        "B_left[xi]=0",
        "B_left[xi]=1-theta",
        "same-side Psi endpoint caps/sum kinks",
        "cross Gamma E=max(...) facets",
        "cross Gamma endpoint caps/sum kinks",
    ]
    inequality_count = len(lp.rows) + len(lp.variables)
    rank_dimension = len(lp.variables)
    naive_basis_count = comb(inequality_count, rank_dimension)
    return {
        "backend": "exact reduced LB_H1 extended LP",
        "variable_count": len(lp.variables),
        "row_count_without_nonnegativity": len(lp.rows),
        "nonnegativity_facets": len(lp.variables),
        "total_halfspaces_for_naive_basis_enumeration": inequality_count,
        "naive_basis_patterns": str(naive_basis_count),
        "prompt_hyperplanes_represented": named_hyperplanes,
        "unresolved": [
            {
                "kind": "full_arrangement_face_enumeration_not_attempted",
                "reason": (
                    "Naive exact basis enumeration would require C("
                    f"{inequality_count},{rank_dimension})={naive_basis_count} "
                    "patterns before rank pruning; this run certifies only exposed "
                    "faces discovered by deterministic rational weight-grid solves."
                ),
            }
        ],
    }


def _render_report(data: dict[str, Any], certificate_path: Path) -> str:
    certs: tuple[FaceCertificate, ...] = data["certificates"]
    outcomes: dict[str, int] = {}
    for cert in certs:
        outcomes[cert.outcome] = outcomes.get(cert.outcome, 0) + 1
    counterexamples = [cert for cert in certs if cert.outcome == "reduced_lb_h1_counterexample"]
    unresolved = list(data["unresolved"]) + list(data["arrangement"]["unresolved"])

    lines: list[str] = []
    lines.append("# DS(2,1) Reduced Normal-Cone Scan v0")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append("This audit uses the repository's exact reduced `LB_H1` extended LP for `DS(2,1)`.  The same-side `Psi` and cross `Gamma` terms are represented by rational endpoint-allocation variables and linear facets, not by sampled nonlinear surrogates.")
    lines.append("")
    lines.append("The projected profile used for the coherence test is `a_i = A_left[x_i]` and `b_i = 1-r_i-A_left[x_i]`, with right split `S = A_right[y1]` and `T = 1-s_y-A_right[y1]`.  These are the center-orientation masses in the existing reduced LP.")
    lines.append("")
    lines.append("## Outcome")
    lines.append("")
    if counterexamples:
        first = counterexamples[0]
        lines.append("A reduced `LB_H1 < OPT_DS` counterexample was found.")
        lines.append(f"- Face: `{first.face_id}`")
        lines.append(f"- Weights `(u1,u2,alpha,beta,v)`: `{_format_tuple(first.sample_weights)}`")
        lines.append(f"- Reduced optimum: `{rational_to_string(first.sample_objective)}`")
        lines.append(f"- Deterministic STT optimum: `{rational_to_string(first.stt_optimum)}`")
    else:
        lines.append("No reduced `LB_H1 < OPT_DS` counterexample was found among the exposed incoherent faces discovered by the deterministic grid scan.")
    lines.append("")
    lines.append(f"Exposed incoherent face certificates written to `{certificate_path}`.")
    lines.append(f"Outcome counts: `{outcomes}`.")
    lines.append("")
    lines.append("## Exact Arrangement Data")
    lines.append("")
    arr = data["arrangement"]
    lines.append(f"- Backend variables: `{arr['variable_count']}`.")
    lines.append(f"- Feasibility rows before nonnegativity: `{arr['row_count_without_nonnegativity']}`.")
    lines.append(f"- Total halfspaces with nonnegativity: `{arr['total_halfspaces_for_naive_basis_enumeration']}`.")
    lines.append(f"- Naive basis patterns: `{arr['naive_basis_patterns']}`.")
    lines.append("- Included hyperplanes/facets: `" + "`, `".join(arr["prompt_hyperplanes_represented"]) + "`.")
    lines.append("")
    lines.append("## Face Table")
    lines.append("")
    if certs:
        lines.append("| face | weights | margin | incoherence | reduced | STT | normal cone | coherent witness | outcome |")
        lines.append("|---|---:|---:|---|---:|---:|---|---|---|")
        for cert in certs:
            lines.append(
                "| {face} | `{weights}` | {margin} | {kind} | {reduced} | {stt} | {normal} | {coh} | {outcome} |".format(
                    face=cert.face_id,
                    weights=_format_tuple(cert.sample_weights),
                    margin=rational_to_string(cert.incoherent_margin),
                    kind=cert.incoherent_kind,
                    reduced=rational_to_string(cert.sample_objective),
                    stt=rational_to_string(cert.stt_optimum),
                    normal=cert.normal_cone.status,
                    coh=cert.coherent_witness.status if cert.coherent_witness.feasible else "none",
                    outcome=cert.outcome,
                )
            )
    else:
        lines.append("No incoherent exposed faces were discovered by the deterministic grid scan.")
    lines.append("")
    lines.append("## Unresolved")
    lines.append("")
    if unresolved:
        for item in unresolved:
            lines.append(f"- `{item['kind']}`: `{item.get('reason', item)}`")
    else:
        lines.append("No unresolved discovered-face normal-cone LPs remain.")
    lines.append("")
    lines.append("## Skeptical Audit")
    lines.append("")
    lines.append("- This is not yet a proof of all arrangement faces: full active-face enumeration is explicitly unresolved above.")
    lines.append("- Reduced `LB_H1` outcomes are kept separate from full H1/H2 depth-projection outcomes.")
    lines.append("- Every saved discovered-face witness is rational and rechecked against the exact LP rows.")
    lines.append("- The deterministic STT comparison uses normal-form `DS(2,1)` STT enumeration, not a reduced surrogate.")
    return "\n".join(lines) + "\n"


def _certificates_json(data: dict[str, Any]) -> dict[str, Any]:
    lp: ReducedCouplingLP = data["lp"]
    return {
        "schema": data["schema"],
        "settings": data["settings"],
        "arrangement": data["arrangement"],
        "faces": [_face_json(lp, cert) for cert in data["certificates"]],
        "unresolved": data["unresolved"],
    }


def _face_json(lp: ReducedCouplingLP, cert: FaceCertificate) -> dict[str, Any]:
    normal_weights = cert.normal_cone.values[:5] if cert.normal_cone.values else ()
    coherent_values = cert.coherent_witness.values
    return {
        "face_id": cert.face_id,
        "outcome": cert.outcome,
        "sample_weights": _weights_json(cert.sample_weights),
        "normal_cone_weights": _weights_json(normal_weights) if normal_weights else None,
        "sample_reduced_objective": rational_to_string(cert.sample_objective),
        "stt_optimum": rational_to_string(cert.stt_optimum),
        "stt_depth_witness": list(cert.stt_depth_witness),
        "incoherent_margin": rational_to_string(cert.incoherent_margin),
        "incoherent_kind": cert.incoherent_kind,
        "active_rows": [
            {"row_index": row, "descriptor": lp.row_descriptors[row]}
            for row in cert.active_rows
        ],
        "zero_variables": [
            {"var_index": index, "label": list(lp.variables[index])}
            for index in cert.zero_variables
        ],
        "sample_reduced_variables": _values_json(lp, cert.sample_values),
        "coherent_witness_variables": (
            _values_json(lp, coherent_values) if cert.coherent_witness.feasible else None
        ),
        "normal_cone_status": {
            "status": cert.normal_cone.status,
            "max_violation": (
                rational_to_string(cert.normal_cone.max_violation)
                if cert.normal_cone.max_violation is not None
                else None
            ),
        },
        "coherent_witness_status": {
            "status": cert.coherent_witness.status,
            "max_violation": (
                rational_to_string(cert.coherent_witness.max_violation)
                if cert.coherent_witness.max_violation is not None
                else None
            ),
        },
    }


def _values_json(lp: ReducedCouplingLP, values: tuple[Fraction, ...]) -> dict[str, Any]:
    profile = _profile_values(lp, values)
    return {
        "profile": {key: rational_to_string(value) for key, value in profile.items()},
        "extended": {
            _label_text(label): rational_to_string(values[index])
            for index, label in enumerate(lp.variables)
            if values[index] != 0 or label[0] in {"theta", "p", "r", "q", "s", "A_left", "A_right"}
        },
    }


def _weights_json(weights: Iterable[Fraction]) -> dict[str, str]:
    keys = ("u1", "u2", "alpha", "beta", "v")
    return {
        key: rational_to_string(value)
        for key, value in zip(keys, tuple(weights))
    }


def _format_tuple(values: Iterable[Fraction]) -> str:
    return "(" + ", ".join(rational_to_string(value) for value in values) + ")"


def _label_text(label: tuple[Any, ...]) -> str:
    return "[" + ",".join(str(part) for part in label) + "]"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m scripts.stt_checker.ds21_normal_cones"
    )
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--certificates", type=Path, default=DEFAULT_CERTIFICATES)
    parser.add_argument("--grid-bound", type=int, default=3)
    args = parser.parse_args(argv)
    result = write_outputs(args.report, args.certificates, args.grid_bound)
    print(
        "wrote {report} and {certificates}: faces={faces} "
        "outcomes={outcomes} unresolved={unresolved}".format(**result)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
