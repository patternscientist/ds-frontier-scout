"""Reduced H1 global-coupling functional tests on double-stars.

This module tests the proof-route functional
``LB_H1(theta,p,q,r,s)`` directly.  It is intentionally narrower than the
full first-hit H1/H2 depth-projection harness: the variables are only the
reduced double-star data plus the auxiliary variables needed to express the
same-side and cross-side endpoint allocation LPs.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
from typing import Any, Iterable

from .double_star_depth_projection import (
    DoubleStarLPResult,
    DoubleStarSpec,
    double_star_spec,
    evaluate_objective as evaluate_full_objective,
    stt_depth_optimum,
    structured_weight_vectors,
)
from .hereditary_lp import DEFAULT_TOLERANCE, _simplex_maximize
from .rationals import rational_to_string
from .star_depth_projection import (
    ExactLPCertificate,
    _exact_dual_from_basis,
    _exact_primal_from_basis,
    _max_dual_deficit,
    _max_primal_violation,
)


DEFAULT_REPORT = Path("reports/stt_double_star_coupling_functional_v0.md")
DEFAULT_SUMMARY = Path(
    "examples/stt_lp/double_star_coupling_functional_v0_summary.json"
)

SparseRow = dict[int, Fraction]
VariableLabel = tuple[Any, ...]


@dataclass(frozen=True)
class Interval:
    lower_terms: tuple[tuple[Fraction, VariableLabel | None], ...]
    upper_terms: tuple[tuple[Fraction, VariableLabel | None], ...]


@dataclass(frozen=True)
class ReducedCouplingLP:
    spec: DoubleStarSpec
    weights: tuple[Fraction, ...]
    variables: tuple[VariableLabel, ...]
    variable_index: dict[VariableLabel, int]
    rows: tuple[SparseRow, ...]
    rhs: tuple[Fraction, ...]
    row_descriptors: tuple[dict[str, Any], ...]
    objective: tuple[Fraction, ...]
    objective_constant: Fraction


@dataclass(frozen=True)
class ReducedCouplingResult:
    spec: DoubleStarSpec
    family: str
    weights: tuple[Fraction, ...]
    stt_optimum: Fraction
    reduced_optimum: Fraction
    certificate_status: str
    certificate: ExactLPCertificate | None
    values: tuple[Fraction, ...]
    lp: ReducedCouplingLP
    active_rows: tuple[dict[str, Any], ...]
    full_h1: DoubleStarLPResult
    full_h2: DoubleStarLPResult | None

    @property
    def reduced_gap(self) -> Fraction:
        return self.reduced_optimum - self.stt_optimum

    @property
    def full_h1_gap(self) -> Fraction:
        return self.full_h1.optimum - self.stt_optimum

    @property
    def full_h2_gap(self) -> Fraction | None:
        if self.full_h2 is None:
            return None
        return self.full_h2.optimum - self.stt_optimum


def left_interval(
    theta: Fraction,
    p_x: Fraction,
    r_x: Fraction,
) -> tuple[Fraction, Fraction]:
    """Return the exact interval ``I_x`` from the reduced functional."""

    return (
        max(Fraction(0), theta - r_x),
        min(Fraction(1) - p_x, theta, Fraction(1) - r_x),
    )


def right_interval(
    theta: Fraction,
    q_y: Fraction,
    s_y: Fraction,
) -> tuple[Fraction, Fraction]:
    """Return the exact interval ``J_y`` from the reduced functional."""

    return (
        max(Fraction(0), q_y - s_y, theta - s_y),
        min(theta, Fraction(1) - s_y),
    )


def gamma_allocation_value(
    w_x: Fraction | int,
    w_y: Fraction | int,
    e_value: Fraction | int,
    r_x: Fraction | int,
    s_y: Fraction | int,
) -> tuple[Fraction, Fraction, Fraction]:
    """Solve the two-variable endpoint allocation LP exactly.

    Returns ``(cost, V_x, V_y)`` for
    ``min w_y V_x + w_x V_y`` with the endpoint caps in the prompt.
    """

    wx = Fraction(w_x)
    wy = Fraction(w_y)
    required = Fraction(e_value)
    r = Fraction(r_x)
    s = Fraction(s_y)
    if required < 0 or r < 0 or s < 0:
        raise ValueError("Gamma inputs must be nonnegative")
    if required > r + s:
        raise ValueError("Gamma allocation is infeasible")
    if wy <= wx:
        vx = min(r, required)
        vy = required - vx
    else:
        vy = min(s, required)
        vx = required - vy
    return wy * vx + wx * vy, vx, vy


def build_reduced_coupling_lp(
    m: int,
    n: int,
    weights: Iterable[Fraction | int],
) -> ReducedCouplingLP:
    spec = double_star_spec(m, n)
    weight_tuple = tuple(Fraction(value) for value in weights)
    if len(weight_tuple) != m + n + 2:
        raise ValueError("weight vector length must match DS(m,n)")
    if any(weight < 0 for weight in weight_tuple):
        raise ValueError("weights must be nonnegative")

    variables: list[VariableLabel] = []
    variable_index: dict[VariableLabel, int] = {}
    rows: list[SparseRow] = []
    rhs: list[Fraction] = []
    descriptors: list[dict[str, Any]] = []
    objective: list[Fraction] = []

    def var(label: VariableLabel) -> int:
        if label not in variable_index:
            variable_index[label] = len(variables)
            variables.append(label)
            objective.append(Fraction(0))
        return variable_index[label]

    def add_to_objective(label: VariableLabel, coefficient: Fraction) -> None:
        objective[var(label)] += coefficient

    def add_row(
        coefficients: dict[VariableLabel, Fraction],
        bound: Fraction,
        descriptor: dict[str, Any],
    ) -> None:
        row: SparseRow = {}
        for label, coefficient in coefficients.items():
            if coefficient == 0:
                continue
            index = var(label)
            row[index] = row.get(index, Fraction(0)) + coefficient
        row = {index: coefficient for index, coefficient in row.items() if coefficient}
        rows.append(row)
        rhs.append(bound)
        descriptors.append(descriptor)

    def leq_var(label: VariableLabel, bound: Fraction, kind: str) -> None:
        add_row({label: Fraction(1)}, bound, {"kind": kind, "var": _label_json(label)})

    def leq_expr(
        lhs: dict[VariableLabel, Fraction],
        bound: Fraction,
        kind: str,
        **extra: Any,
    ) -> None:
        descriptor = {"kind": kind, **extra}
        add_row(lhs, bound, descriptor)

    theta = ("theta",)
    var(theta)
    leq_var(theta, Fraction(1), "upper_unit")

    for x in spec.left_leaves:
        p = ("p", x)
        r = ("r", x)
        a_left = ("A_left", x)
        for label in (p, r, a_left):
            var(label)
            leq_var(label, Fraction(1), "upper_unit")
        leq_expr({r: Fraction(1), p: Fraction(-1)}, Fraction(0), "reduced_h1_r_le_p", x=spec.label(x))
        # I_x lower bounds: A_x >= 0 is handled by nonnegativity; A_x >= theta-r_x.
        leq_expr(
            {theta: Fraction(1), r: Fraction(-1), a_left: Fraction(-1)},
            Fraction(0),
            "left_interval_lower_theta_minus_r",
            x=spec.label(x),
        )
        # I_x upper bounds.
        leq_expr({a_left: Fraction(1), p: Fraction(1)}, Fraction(1), "left_interval_upper_one_minus_p", x=spec.label(x))
        leq_expr({a_left: Fraction(1), theta: Fraction(-1)}, Fraction(0), "left_interval_upper_theta", x=spec.label(x))
        leq_expr({a_left: Fraction(1), r: Fraction(1)}, Fraction(1), "left_interval_upper_one_minus_r", x=spec.label(x))

    for y in spec.right_leaves:
        q = ("q", y)
        s = ("s", y)
        a_right = ("A_right", y)
        for label in (q, s, a_right):
            var(label)
            leq_var(label, Fraction(1), "upper_unit")
        leq_expr({s: Fraction(1), q: Fraction(-1)}, Fraction(0), "reduced_h1_s_le_q", y=spec.label(y))
        # J_y lower bounds: A_y >= 0 is handled by nonnegativity.
        leq_expr({q: Fraction(1), s: Fraction(-1), a_right: Fraction(-1)}, Fraction(0), "right_interval_lower_q_minus_s", y=spec.label(y))
        leq_expr({theta: Fraction(1), s: Fraction(-1), a_right: Fraction(-1)}, Fraction(0), "right_interval_lower_theta_minus_s", y=spec.label(y))
        # J_y upper bounds.
        leq_expr({a_right: Fraction(1), theta: Fraction(-1)}, Fraction(0), "right_interval_upper_theta", y=spec.label(y))
        leq_expr({a_right: Fraction(1), s: Fraction(1)}, Fraction(1), "right_interval_upper_one_minus_s", y=spec.label(y))

    alpha = weight_tuple[spec.a]
    beta = weight_tuple[spec.b]
    objective_constant = alpha
    objective_constant += sum(weight_tuple[x] for x in spec.left_leaves)
    objective_constant += sum(weight_tuple[y] for y in spec.right_leaves)
    objective_constant += sum(weight_tuple[x] for x in spec.left_leaves)

    add_to_objective(theta, beta - alpha)
    for x in spec.left_leaves:
        wx = weight_tuple[x]
        add_to_objective(("p", x), alpha - wx)
        add_to_objective(("r", x), beta - wx)
        add_to_objective(("A_left", x), -wx)
    for y in spec.right_leaves:
        wy = weight_tuple[y]
        add_to_objective(("q", y), beta - wy)
        add_to_objective(("s", y), alpha)
        add_to_objective(("A_right", y), wy)

    for left_i, left_j in combinations(spec.left_leaves, 2):
        _add_same_side_pair(
            spec,
            side="left",
            first=left_i,
            second=left_j,
            mass_label=lambda vertex: ("p", vertex),
            first_objective_weight=weight_tuple[left_j],
            second_objective_weight=weight_tuple[left_i],
            add_row=add_row,
            add_to_objective=add_to_objective,
        )

    for right_i, right_j in combinations(spec.right_leaves, 2):
        _add_same_side_pair(
            spec,
            side="right",
            first=right_i,
            second=right_j,
            mass_label=lambda vertex: ("q", vertex),
            first_objective_weight=weight_tuple[right_j],
            second_objective_weight=weight_tuple[right_i],
            add_row=add_row,
            add_to_objective=add_to_objective,
        )

    for x in spec.left_leaves:
        for y in spec.right_leaves:
            e = ("E", x, y)
            vx = ("Vx", x, y)
            vy = ("Vy", x, y)
            for label in (e, vx, vy):
                var(label)
            leq_expr({("r", x): Fraction(1), e: Fraction(-1)}, Fraction(0), "cross_e_ge_r", x=spec.label(x), y=spec.label(y))
            leq_expr({("s", y): Fraction(1), e: Fraction(-1)}, Fraction(0), "cross_e_ge_s", x=spec.label(x), y=spec.label(y))
            leq_expr(
                {
                    ("r", x): Fraction(1),
                    ("A_left", x): Fraction(1),
                    ("A_right", y): Fraction(-1),
                    e: Fraction(-1),
                },
                Fraction(0),
                "cross_e_ge_r_plus_ax_minus_ay",
                x=spec.label(x),
                y=spec.label(y),
            )
            leq_expr(
                {
                    ("s", y): Fraction(1),
                    ("A_left", x): Fraction(-1),
                    ("A_right", y): Fraction(1),
                    e: Fraction(-1),
                },
                Fraction(0),
                "cross_e_ge_s_minus_ax_plus_ay",
                x=spec.label(x),
                y=spec.label(y),
            )
            leq_expr({vx: Fraction(1), ("r", x): Fraction(-1)}, Fraction(0), "gamma_vx_le_r", x=spec.label(x), y=spec.label(y))
            leq_expr({vy: Fraction(1), ("s", y): Fraction(-1)}, Fraction(0), "gamma_vy_le_s", x=spec.label(x), y=spec.label(y))
            leq_expr({e: Fraction(1), vx: Fraction(-1), vy: Fraction(-1)}, Fraction(0), "gamma_vsum_ge_e", x=spec.label(x), y=spec.label(y))
            add_to_objective(vx, weight_tuple[y])
            add_to_objective(vy, weight_tuple[x])

    return ReducedCouplingLP(
        spec=spec,
        weights=weight_tuple,
        variables=tuple(variables),
        variable_index=variable_index,
        rows=tuple(rows),
        rhs=tuple(rhs),
        row_descriptors=tuple(descriptors),
        objective=tuple(objective),
        objective_constant=objective_constant,
    )


def solve_reduced_coupling_lp_exact(
    m: int,
    n: int,
    weights: Iterable[Fraction | int],
    tolerance: float = DEFAULT_TOLERANCE,
) -> tuple[ReducedCouplingLP, Fraction, tuple[Fraction, ...], ExactLPCertificate | None, str, tuple[dict[str, Any], ...]]:
    lp = build_reduced_coupling_lp(m, n, weights)
    matrix = [[0.0 for _ in lp.objective] for _ in lp.rows]
    for row_index, row in enumerate(lp.rows):
        for col, value in row.items():
            matrix[row_index][col] = float(value)
    result = _simplex_maximize(
        matrix,
        [float(value) for value in lp.rhs],
        [-float(value) for value in lp.objective],
        tolerance=tolerance,
    )
    if result.status != 0:
        raise ValueError(f"simplex failed: status={result.status} message={result.message}")

    fallback_values = tuple(
        Fraction(value).limit_denominator(1_000_000) for value in result.solution
    )
    fallback_objective = lp.objective_constant + sum(
        lp.objective[index] * fallback_values[index]
        for index in range(len(fallback_values))
    )
    certificate: ExactLPCertificate | None = None
    status = "exact_primal_only_after_floating_solution_rationalization"
    values = fallback_values
    active_rows: tuple[dict[str, Any], ...] = ()
    try:
        exact_values = tuple(
            _exact_primal_from_basis(lp.rows, lp.rhs, result.basis, len(lp.objective))
        )
        max_objective = tuple(-coefficient for coefficient in lp.objective)
        dual_values = _exact_dual_from_basis(
            lp.rows,
            max_objective,
            result.basis,
            result.nonbasis,
            len(lp.objective),
        )
        max_primal_violation = _max_primal_violation(lp.rows, lp.rhs, list(exact_values))
        max_dual_deficit = _max_dual_deficit(lp.rows, max_objective, dual_values)
        max_value = sum(
            max_objective[index] * exact_values[index]
            for index in range(len(exact_values))
        )
        dual_objective = sum(
            lp.rhs[row] * dual_values[row] for row in range(len(lp.rows))
        )
        if max_primal_violation != 0 or max_dual_deficit != 0:
            raise ValueError("exact basis reconstruction did not verify")
        if dual_objective != max_value:
            raise ValueError("dual objective mismatch")
        exact_objective = lp.objective_constant - max_value
        certificate = ExactLPCertificate(
            objective=exact_objective,
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
                "row": lp.row_descriptors[row],
            }
            for row, value in enumerate(dual_values)
            if value
        )
        return lp, exact_objective, values, certificate, status, active_rows
    except ValueError:
        return lp, fallback_objective, values, certificate, status, active_rows


def evaluate_reduced_objective(
    m: int,
    n: int,
    weights: Iterable[Fraction | int],
    family: str,
) -> ReducedCouplingResult:
    weight_tuple = tuple(Fraction(value) for value in weights)
    stt_optimum, _depth = stt_depth_optimum(m, n, weight_tuple)
    lp, reduced_optimum, values, certificate, status, active_rows = (
        solve_reduced_coupling_lp_exact(m, n, weight_tuple)
    )
    full = evaluate_full_objective(m, n, weight_tuple, family, run_h2=True)
    return ReducedCouplingResult(
        spec=lp.spec,
        family=family,
        weights=weight_tuple,
        stt_optimum=stt_optimum,
        reduced_optimum=reduced_optimum,
        certificate_status=status,
        certificate=certificate,
        values=values,
        lp=lp,
        active_rows=active_rows,
        full_h1=full.h1,
        full_h2=full.h2,
    )


def run_scout(
    topologies: tuple[tuple[int, int], ...] = (
        (1, 1),
        (2, 1),
        (2, 2),
        (3, 1),
        (3, 2),
    ),
    small_bound: int = 2,
) -> dict[str, Any]:
    runs: list[ReducedCouplingResult] = []
    for m, n in topologies:
        for family, weights in structured_weight_vectors(m, n, small_bound=small_bound):
            runs.append(evaluate_reduced_objective(m, n, weights, family))
    return {
        "settings": {
            "topologies": [f"DS({m},{n})" for m, n in topologies],
            "small_bound": small_bound,
        },
        "runs": runs,
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
    reduced_gaps = [run for run in data["runs"] if run.reduced_gap < 0]
    full_h1_gaps = [run for run in data["runs"] if run.full_h1_gap < 0]
    full_h2_gaps = [
        run for run in data["runs"] if run.full_h2_gap is not None and run.full_h2_gap < 0
    ]
    return {
        "report": str(path),
        "summary": str(summary_path),
        "runs": len(data["runs"]),
        "reduced_gaps": len(reduced_gaps),
        "full_h1_gaps": len(full_h1_gaps),
        "full_h2_gaps": len(full_h2_gaps),
    }


def write_summary(data: dict[str, Any], path: Path = DEFAULT_SUMMARY) -> None:
    payload = {
        "schema": "stt_double_star_coupling_functional_v0_summary",
        "settings": data["settings"],
        "runs": [_run_to_json(run) for run in data["runs"]],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _add_same_side_pair(
    spec: DoubleStarSpec,
    side: str,
    first: int,
    second: int,
    mass_label: Any,
    first_objective_weight: Fraction,
    second_objective_weight: Fraction,
    add_row: Any,
    add_to_objective: Any,
) -> None:
    first_endpoint = ("Psi", side, first, second, first)
    second_endpoint = ("Psi", side, first, second, second)
    first_mass = mass_label(first)
    second_mass = mass_label(second)
    add_row(
        {first_endpoint: Fraction(1), first_mass: Fraction(-1)},
        Fraction(0),
        {
            "kind": "psi_first_endpoint_cap",
            "side": side,
            "first": spec.label(first),
            "second": spec.label(second),
        },
    )
    add_row(
        {second_endpoint: Fraction(1), second_mass: Fraction(-1)},
        Fraction(0),
        {
            "kind": "psi_second_endpoint_cap",
            "side": side,
            "first": spec.label(first),
            "second": spec.label(second),
        },
    )
    add_row(
        {first_mass: Fraction(1), first_endpoint: Fraction(-1), second_endpoint: Fraction(-1)},
        Fraction(0),
        {
            "kind": "psi_sum_ge_first_mass",
            "side": side,
            "first": spec.label(first),
            "second": spec.label(second),
        },
    )
    add_row(
        {second_mass: Fraction(1), first_endpoint: Fraction(-1), second_endpoint: Fraction(-1)},
        Fraction(0),
        {
            "kind": "psi_sum_ge_second_mass",
            "side": side,
            "first": spec.label(first),
            "second": spec.label(second),
        },
    )
    add_to_objective(first_endpoint, first_objective_weight)
    add_to_objective(second_endpoint, second_objective_weight)


def _run_to_json(run: ReducedCouplingResult) -> dict[str, Any]:
    return {
        "topology": run.spec.name,
        "family": run.family,
        "weights": {
            run.spec.label(vertex): rational_to_string(run.weights[vertex])
            for vertex in range(run.spec.m + run.spec.n + 2)
        },
        "stt_optimum": rational_to_string(run.stt_optimum),
        "reduced_lb_h1_minimum": rational_to_string(run.reduced_optimum),
        "reduced_gap": rational_to_string(run.reduced_gap),
        "reduced_certificate_status": run.certificate_status,
        "full_h1_optimum": rational_to_string(run.full_h1.optimum),
        "full_h1_gap": rational_to_string(run.full_h1_gap),
        "full_h1_certificate_status": run.full_h1.certificate_status,
        "full_h2_optimum": rational_to_string(run.full_h2.optimum) if run.full_h2 is not None else None,
        "full_h2_gap": rational_to_string(run.full_h2_gap) if run.full_h2_gap is not None else None,
        "full_h2_certificate_status": run.full_h2.certificate_status if run.full_h2 is not None else None,
        "reduced_variables": _reduced_values_json(run),
    }


def _render_report(data: dict[str, Any]) -> str:
    runs: list[ReducedCouplingResult] = data["runs"]
    reduced_gaps = [run for run in runs if run.reduced_gap < 0]
    full_h1_gaps = [run for run in runs if run.full_h1_gap < 0]
    full_h2_gaps = [
        run for run in runs if run.full_h2_gap is not None and run.full_h2_gap < 0
    ]
    first_gap = reduced_gaps[0] if reduced_gaps else None

    lines: list[str] = []
    lines.append("# STT Double-Star Coupling Functional v0")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append("This is a targeted proof-route test of the reduced global coupling functional `LB_H1(theta,p,q,r,s)` on double-stars. It is not a broad almost-star sweep and it does not test H3/H4.")
    lines.append("")
    lines.append("The tested topologies are `" + "`, `".join(data["settings"]["topologies"]) + "`. Structured nonnegative weights reuse the previous double-star families, including all small integer weights through the configured bound on `DS(1,1)`.")
    lines.append("")
    lines.append("## Outcome")
    lines.append("")
    if first_gap is None:
        lines.append("No reduced `LB_H1 < STT` counterexample was found in the tested cases.")
    else:
        lines.append("The reduced global coupling inequality fails in the tested domain.")
        lines.append("")
        lines.append(f"- Smallest recorded topology/family: `{first_gap.spec.name}` / `{first_gap.family}`.")
        lines.append(f"- Weights: `{_format_labeled_weights(first_gap)}`.")
        lines.append(f"- Reduced `LB_H1` minimum: `{rational_to_string(first_gap.reduced_optimum)}`.")
        lines.append(f"- Exact STT optimum: `{rational_to_string(first_gap.stt_optimum)}`.")
        lines.append(f"- Gap `LB_H1 - STT`: `{rational_to_string(first_gap.reduced_gap)}`.")
        lines.append(f"- Reduced variables: `{_reduced_values_json(first_gap)}`.")
        lines.append("")
        lines.append("This refutes the current reduced coupling proof route. It does not by itself refute full H1 depth-projection exactness.")
    if full_h1_gaps:
        run = full_h1_gaps[0]
        lines.append("")
        lines.append(f"Full H1 also has a depth-projection gap first recorded at `{run.spec.name}` / `{run.family}` with H1 `{rational_to_string(run.full_h1.optimum)}` versus STT `{rational_to_string(run.stt_optimum)}`.")
    else:
        lines.append("")
        lines.append("No full H1 depth-projection gap appeared in the same tested cases.")
    if full_h2_gaps:
        run = full_h2_gaps[0]
        lines.append(f"Full H2 also has a depth-projection gap first recorded at `{run.spec.name}` / `{run.family}`.")
    else:
        lines.append("No full H2 depth-projection gap appeared; when H1 matched STT, H2 was certified by sandwiching.")
    lines.append("")
    lines.append("## Solve Table")
    lines.append("")
    lines.append("| topology | family | weights | STT | reduced LB_H1 min | gap | full H1 | full H2 |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|")
    for run in runs:
        h2_text = rational_to_string(run.full_h2.optimum) if run.full_h2 is not None else "not run"
        lines.append(
            "| {topology} | {family} | `{weights}` | {stt} | {reduced} | {gap} | {h1} | {h2} |".format(
                topology=run.spec.name,
                family=run.family,
                weights=_format_labeled_weights(run),
                stt=rational_to_string(run.stt_optimum),
                reduced=rational_to_string(run.reduced_optimum),
                gap=rational_to_string(run.reduced_gap),
                h1=rational_to_string(run.full_h1.optimum),
                h2=h2_text,
            )
        )
    lines.append("")
    lines.append("## Reduced LP Encoding")
    lines.append("")
    lines.append("- Variables are `theta`, `p_x`, `q_y`, `r_x`, `s_y`, interval variables `A_left[x]`, `A_right[y]`, same-side endpoint variables for `Psi`, and cross-side `E_xy`, `Vx_xy`, `Vy_xy` variables for `Gamma`.")
    lines.append("- The interval constraints encode exactly `I_x = [max(0, theta-r_x), min(1-p_x, theta, 1-r_x)]` and `J_y = [max(0, q_y-s_y, theta-s_y), min(theta, 1-s_y)]`; nonnegativity is supplied by the standard LP form.")
    lines.append("- `Gamma` is represented by endpoint allocation constraints `0 <= Vx <= r_x`, `0 <= Vy <= s_y`, `Vx + Vy >= E`, with `E` lower-bounding the four expressions in the prompt.")
    lines.append("")
    if first_gap is None:
        lines.append("## Candidate Proof Pattern")
        lines.append("")
        for run in _representative_runs(runs):
            lines.append(f"- `{run.spec.name}` / `{run.family}` active reduced dual rows, first few nonzero multipliers: `{_compact_active_rows(run.active_rows)}`.")
        lines.append("")
        lines.append("Finite pattern: the reduced duals use interval upper/lower rows together with the `Gamma` endpoint caps and same-side `Psi` sum rows. This is only a candidate symbolic pattern, not a promoted proof.")
        lines.append("")
    lines.append("## Skeptical Audit")
    lines.append("")
    lines.append("- A reduced-functional counterexample only attacks this global coupling lemma route, not full H1 exactness.")
    lines.append("- A no-gap finite run would still not prove the inequality for all reduced H1-feasible data.")
    lines.append("- The reduced feasible region is exactly the one encoded here; any stronger formalization should be added as explicit constraints and rerun.")
    lines.append("- The full H1/H2 comparisons are depth-projection checks from the previous machinery and are kept separate from the reduced-functional result.")
    return "\n".join(lines) + "\n"


def _reduced_values_json(run: ReducedCouplingResult) -> dict[str, Any]:
    values = {
        _label_text(label): rational_to_string(run.values[index])
        for index, label in enumerate(run.lp.variables)
        if run.values[index] != 0 or label[0] in {"theta", "p", "q", "r", "s", "A_left", "A_right"}
    }
    return values


def _representative_runs(runs: list[ReducedCouplingResult]) -> list[ReducedCouplingResult]:
    representatives = []
    seen: set[str] = set()
    for run in runs:
        if run.spec.name in seen:
            continue
        representatives.append(run)
        seen.add(run.spec.name)
    return representatives


def _compact_active_rows(rows: tuple[dict[str, Any], ...], limit: int = 8) -> list[dict[str, Any]]:
    return rows[:limit]


def _format_labeled_weights(run: ReducedCouplingResult) -> str:
    return "(" + ", ".join(
        f"{run.spec.label(vertex)}={rational_to_string(run.weights[vertex])}"
        for vertex in range(run.spec.m + run.spec.n + 2)
    ) + ")"


def _label_text(label: VariableLabel) -> str:
    return "[" + ",".join(str(part) for part in label) + "]"


def _label_json(label: VariableLabel) -> list[Any]:
    return list(label)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m scripts.stt_checker.double_star_coupling_functional"
    )
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    args = parser.parse_args(argv)
    result = write_report(args.report, args.summary)
    print(
        "wrote {report} and {summary}: runs={runs} reduced_gaps={reduced_gaps} "
        "full_h1_gaps={full_h1_gaps} full_h2_gaps={full_h2_gaps}".format(**result)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
