"""Exact targeted coverage for the DS(2,1) pinned boundary cells.

This module is deliberately narrower than the v0/v1 normal-cone audits in
``ds21_normal_cones``.  It enumerates only the remaining A-pinned and B-pinned
endpoint/cross-kink cells from the current frontier note, reconstructs rational
cell and normal-cone witnesses, and classifies any exposed optimum against
coherent reduced witnesses and deterministic STT equality witnesses.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
from typing import Any, Iterable

from .double_star_coupling_functional import ReducedCouplingLP, build_reduced_coupling_lp
from .double_star_depth_projection import stt_depth_optimum
from .hereditary_lp import DEFAULT_TOLERANCE
from .rationals import rational_to_string
from .ds21_normal_cones import (
    ExactFeasibilityResult,
    ExactOptimizationResult,
    LinearForm,
    SparseRow,
    WeightVector,
    _active_rows,
    _add_forms,
    _arrangement_summary,
    _coherence_rows,
    _constant_form,
    _form_minus,
    _format_tuple,
    _objective_coefficient_matrix,
    _optimal_face_feasibility,
    _positive_optimum,
    _scale_form,
    _solve_exact_max_lp,
    _structural_classification,
    _var_form,
    _values_json,
    _weights_json,
)


DEFAULT_REPORT = Path("reports/stt_double_star_ds21_pinned_boundary_v2.md")
DEFAULT_CERTIFICATES = Path(
    "examples/stt_lp/ds21_pinned_boundary_v2_certificates.json"
)


@dataclass(frozen=True)
class PinnedBoundaryCell:
    cell_id: str
    family: str
    facet_states: tuple[tuple[str, str], ...]
    psi_active: tuple[int, ...]
    gamma_lower_active: tuple[tuple[int, ...], tuple[int, ...]]

    @property
    def active_rows(self) -> tuple[int, ...]:
        return tuple(sorted(self.psi_active + self.gamma_lower_active[0] + self.gamma_lower_active[1]))

    @property
    def active_facets(self) -> tuple[str, ...]:
        return tuple(name for name, state in self.facet_states if state == "eq")

    def state(self, facet: str) -> str:
        for name, state in self.facet_states:
            if name == facet:
                return state
        raise KeyError(facet)


@dataclass(frozen=True)
class PinnedBoundaryCertificate:
    cell: PinnedBoundaryCell
    cell_feasibility: ExactOptimizationResult
    active_rows: tuple[int, ...]
    zero_variables: tuple[int, ...]
    normal_cone: ExactOptimizationResult
    sample_values: tuple[Fraction, ...] = ()
    normal_weights: WeightVector | None = None
    reduced_objective: Fraction | None = None
    stt_optimum: Fraction | None = None
    stt_depth_witness: tuple[int, ...] = ()
    coherent_witness: ExactFeasibilityResult | None = None

    @property
    def outcome(self) -> str:
        if not self.cell_feasibility.feasible:
            return "empty_pinned_cell"
        if not _positive_optimum(self.cell_feasibility):
            return "no_pinned_relative_interior"
        if not self.normal_cone.feasible or not _positive_optimum(self.normal_cone):
            return "normal_cone_infeasible_for_pinned_slope"
        if self.reduced_objective is not None and self.stt_optimum is not None:
            if self.reduced_objective < self.stt_optimum:
                return "rational_reduced_counterexample"
        if self.coherent_witness is not None and self.coherent_witness.feasible:
            return "coherent_reduced_equality_witness"
        if self.reduced_objective is not None and self.stt_optimum is not None:
            if self.reduced_objective == self.stt_optimum:
                return "deterministic_stt_equality_witness"
        return "unresolved_pinned_cell"


def run_pinned_boundary_coverage(
    tolerance: float = DEFAULT_TOLERANCE,
    max_unresolved: int = 64,
    cell_limit: int | None = None,
) -> dict[str, Any]:
    lp = build_reduced_coupling_lp(2, 1, (1, 1, 1, 1, 1))
    objective_by_weight = _objective_coefficient_matrix()
    all_cells = tuple(_pinned_boundary_cells())
    cells = all_cells[:cell_limit] if cell_limit is not None else all_cells
    certificates: list[PinnedBoundaryCertificate] = []
    unresolved: list[dict[str, Any]] = []
    outcome_counts: dict[str, int] = {}

    for cell in cells:
        cell_feasibility = _pinned_boundary_cell_feasibility(lp, cell, tolerance)
        if not cell_feasibility.feasible or not _positive_optimum(cell_feasibility):
            cert = PinnedBoundaryCertificate(
                cell=cell,
                cell_feasibility=cell_feasibility,
                active_rows=cell.active_rows,
                zero_variables=(),
                normal_cone=ExactOptimizationResult(
                    feasible=False,
                    status="not_run_no_pinned_relative_interior",
                ),
            )
            certificates.append(cert)
            outcome_counts[cert.outcome] = outcome_counts.get(cert.outcome, 0) + 1
            continue

        sample = cell_feasibility.values[:-1]
        active_rows = _active_rows(lp, sample)
        zero_variables = tuple(index for index, value in enumerate(sample) if value == 0)
        normal_cone = _pinned_normal_cone_feasibility(
            lp=lp,
            family=cell.family,
            active_rows=active_rows,
            zero_variables=zero_variables,
            objective_by_weight=objective_by_weight,
            tolerance=tolerance,
        )

        normal_weights: WeightVector | None = None
        reduced_objective: Fraction | None = None
        stt_value: Fraction | None = None
        stt_depth: tuple[int, ...] = ()
        coherent: ExactFeasibilityResult | None = None
        if normal_cone.feasible and _positive_optimum(normal_cone):
            normal_weights = tuple(normal_cone.values[:5])  # type: ignore[assignment]
            solved_lp = build_reduced_coupling_lp(2, 1, normal_weights)
            reduced_objective = solved_lp.objective_constant + sum(
                solved_lp.objective[index] * sample[index]
                for index in range(len(sample))
            )
            stt_value, stt_depth = stt_depth_optimum(2, 1, normal_weights)
            coherent = _optimal_face_feasibility(
                lp=solved_lp,
                optimum=reduced_objective,
                extra_rows=_coherence_rows(solved_lp),
                tolerance=tolerance,
            )

        cert = PinnedBoundaryCertificate(
            cell=cell,
            cell_feasibility=cell_feasibility,
            active_rows=active_rows,
            zero_variables=zero_variables,
            normal_cone=normal_cone,
            sample_values=sample,
            normal_weights=normal_weights,
            reduced_objective=reduced_objective,
            stt_optimum=stt_value,
            stt_depth_witness=stt_depth,
            coherent_witness=coherent,
        )
        certificates.append(cert)
        outcome_counts[cert.outcome] = outcome_counts.get(cert.outcome, 0) + 1
        if cert.outcome == "rational_reduced_counterexample":
            break
        if cert.outcome == "unresolved_pinned_cell":
            unresolved.append(_unresolved_pinned_cell_json(lp, cert))
            if len(unresolved) >= max_unresolved:
                break

    return {
        "schema": "stt_ds21_pinned_boundary_v2",
        "settings": {
            "mode": "targeted_pinned_endpoint_cross_kink_coverage",
            "weight_order": ["u1", "u2", "alpha", "beta", "v"],
            "weight_cone": (
                "sum weights = 1, u1 >= u2 >= 0, alpha >= 0, beta >= 0, v >= 0; "
                "A-pinned adds u2 > v and beta <= u2-v; "
                "B-pinned adds u1 > v and beta <= u1-v"
            ),
            "families": {
                "A-pinned": [
                    "p1=p2",
                    "a1<a2",
                    "b1=c1>b2",
                    "a2<S",
                    "at least one of a1=0, b1=1-theta, b2=c2, c1=T",
                ],
                "B-pinned": [
                    "p1=p2",
                    "a1>a2",
                    "b2=c2>b1",
                    "a1<S",
                    "at least one of a2=0, b2=1-theta, b1=c1, c2=T",
                ],
            },
            "profile_convention": {
                "a_i": "A_left[x_i]",
                "b_i": "1-r_i-A_left[x_i]",
                "c_i": "1-p_i-A_left[x_i]",
                "S": "A_right[y1]",
                "T": "1-s_y-A_right[y1]",
            },
            "pinned_cells_considered": len(cells),
            "full_pinned_cell_count": len(all_cells),
            "max_unresolved": max_unresolved,
            "tolerance": tolerance,
        },
        "arrangement": _arrangement_summary(lp),
        "lp": lp,
        "pinned_boundary_certificates": tuple(certificates),
        "pinned_boundary_outcomes": outcome_counts,
        "unresolved": unresolved,
    }


def write_pinned_boundary_outputs(
    report_path: Path = DEFAULT_REPORT,
    certificate_path: Path = DEFAULT_CERTIFICATES,
) -> dict[str, Any]:
    data = run_pinned_boundary_coverage()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    certificate_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(_render_pinned_report(data, certificate_path), encoding="utf-8")
    certificate_path.write_text(
        json.dumps(_pinned_certificates_json(data), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "report": str(report_path),
        "certificates": str(certificate_path),
        "cells": len(data["pinned_boundary_certificates"]),
        "outcomes": data["pinned_boundary_outcomes"],
        "unresolved": len(data["unresolved"]),
    }


def _pinned_boundary_cells() -> Iterable[PinnedBoundaryCell]:
    psi_options = tuple(
        tuple(row for bit, row in enumerate((25, 26, 27, 28)) if mask & (1 << bit))
        for mask in range(16)
    )
    gamma_x1_lower = ((29,), (32,), (29, 32))
    gamma_x2_lower = ((36,), (39,), (36, 39))
    counter = 1
    for family in ("A-pinned", "B-pinned"):
        for facet_states in _facet_state_splits(family):
            for psi in psi_options:
                for lower_1 in gamma_x1_lower:
                    for lower_2 in gamma_x2_lower:
                        yield PinnedBoundaryCell(
                            cell_id=f"pinned-boundary-cell-{counter:05d}",
                            family=family,
                            facet_states=facet_states,
                            psi_active=psi,
                            gamma_lower_active=(lower_1, lower_2),
                        )
                        counter += 1


def _facet_state_splits(family: str) -> Iterable[tuple[tuple[str, str], ...]]:
    if family == "A-pinned":
        names = ("a1_zero", "b1_endpoint", "b2_c2", "c1_T")
    elif family == "B-pinned":
        names = ("a2_zero", "b2_endpoint", "b1_c1", "c2_T")
    else:
        raise ValueError(f"unknown pinned family {family}")

    binary_options = (("eq", "inactive"),) * 3
    c_t_options = ("eq", "lt", "gt")
    for states in product(*binary_options, c_t_options):
        facet_states = tuple(zip(names, states, strict=True))
        if any(state == "eq" for _name, state in facet_states):
            yield facet_states


def _pinned_boundary_cell_feasibility(
    lp: ReducedCouplingLP,
    cell: PinnedBoundaryCell,
    tolerance: float,
) -> ExactOptimizationResult:
    margin = len(lp.variables)
    variable_count = margin + 1
    rows: list[SparseRow] = [dict(row) for row in lp.rows]
    rhs: list[Fraction] = list(lp.rhs)
    rows.extend({index: Fraction(-1)} for index in range(len(lp.variables)))
    rhs.extend(Fraction(0) for _ in lp.variables)

    def add_leq(row: SparseRow, bound: Fraction) -> None:
        rows.append({index: value for index, value in row.items() if value})
        rhs.append(bound)

    def add_eq(row: SparseRow, bound: Fraction) -> None:
        add_leq(row, bound)
        add_leq({index: -value for index, value in row.items()}, -bound)

    def add_eq_form(form: LinearForm) -> None:
        constant, row = form
        add_eq(row, -constant)

    def add_margin_leq_form(form: LinearForm) -> None:
        constant, row = form
        with_margin = dict(row)
        with_margin[margin] = with_margin.get(margin, Fraction(0)) + 1
        add_leq(with_margin, -constant)

    forms = _profile_forms(lp)
    add_eq_form(_form_minus(forms["p1"], forms["p2"]))

    if cell.family == "A-pinned":
        add_eq_form(_form_minus(forms["r1"], forms["p1"]))
        add_margin_leq_form(_form_minus(forms["a1"], forms["a2"]))
        add_margin_leq_form(_form_minus(forms["b2"], forms["b1"]))
        add_margin_leq_form(_form_minus(forms["a2"], forms["S"]))
        _apply_facet_state(cell, "a1_zero", forms["a1"], add_eq_form, add_margin_leq_form)
        _apply_facet_state(
            cell,
            "b1_endpoint",
            _form_minus(forms["b1"], forms["one_minus_theta"]),
            add_eq_form,
            add_margin_leq_form,
        )
        _apply_facet_state(
            cell,
            "b2_c2",
            _form_minus(forms["r2"], forms["p2"]),
            add_eq_form,
            add_margin_leq_form,
        )
        _apply_c_t_state(
            cell,
            "c1_T",
            _form_minus(forms["c1"], forms["T"]),
            add_eq_form,
            add_margin_leq_form,
        )
    elif cell.family == "B-pinned":
        add_eq_form(_form_minus(forms["r2"], forms["p2"]))
        add_margin_leq_form(_form_minus(forms["a2"], forms["a1"]))
        add_margin_leq_form(_form_minus(forms["b1"], forms["b2"]))
        add_margin_leq_form(_form_minus(forms["a1"], forms["S"]))
        _apply_facet_state(cell, "a2_zero", forms["a2"], add_eq_form, add_margin_leq_form)
        _apply_facet_state(
            cell,
            "b2_endpoint",
            _form_minus(forms["b2"], forms["one_minus_theta"]),
            add_eq_form,
            add_margin_leq_form,
        )
        _apply_facet_state(
            cell,
            "b1_c1",
            _form_minus(forms["r1"], forms["p1"]),
            add_eq_form,
            add_margin_leq_form,
        )
        _apply_c_t_state(
            cell,
            "c2_T",
            _form_minus(forms["c2"], forms["T"]),
            add_eq_form,
            add_margin_leq_form,
        )
    else:
        raise ValueError(f"unknown pinned family {cell.family}")

    kink_rows = set(range(25, 33)) | set(range(36, 40))
    active = set(cell.active_rows)
    for row_index in sorted(kink_rows):
        row = lp.rows[row_index]
        bound = lp.rhs[row_index]
        if row_index in active:
            add_eq(row, bound)
        else:
            constant, sparse = Fraction(0), row
            with_margin = dict(sparse)
            with_margin[margin] = with_margin.get(margin, Fraction(0)) + 1
            add_leq(with_margin, bound - constant)

    add_leq({margin: Fraction(1)}, Fraction(1))
    objective = tuple(Fraction(0) for _ in range(margin)) + (Fraction(1),)
    return _solve_exact_max_lp(tuple(rows), tuple(rhs), objective, variable_count, tolerance)


def _pinned_normal_cone_feasibility(
    lp: ReducedCouplingLP,
    family: str,
    active_rows: tuple[int, ...],
    zero_variables: tuple[int, ...],
    objective_by_weight: tuple[tuple[Fraction, ...], ...],
    tolerance: float,
) -> ExactOptimizationResult:
    weight_count = 5
    lambda_offset = weight_count
    mu_offset = lambda_offset + len(active_rows)
    margin = mu_offset + len(zero_variables)
    total = margin + 1
    rows: list[SparseRow] = []
    rhs: list[Fraction] = []

    def add_leq(row: SparseRow, bound: Fraction) -> None:
        rows.append({index: value for index, value in row.items() if value})
        rhs.append(bound)

    def add_eq(row: SparseRow, bound: Fraction) -> None:
        add_leq(row, bound)
        add_leq({index: -value for index, value in row.items()}, -bound)

    add_eq({index: Fraction(1) for index in range(weight_count)}, Fraction(1))
    add_leq({1: Fraction(1), 0: Fraction(-1)}, Fraction(0))
    if family == "A-pinned":
        add_leq({4: Fraction(1), 1: Fraction(-1), margin: Fraction(1)}, Fraction(0))
        add_leq({3: Fraction(1), 4: Fraction(1), 1: Fraction(-1)}, Fraction(0))
    elif family == "B-pinned":
        add_leq({4: Fraction(1), 0: Fraction(-1), margin: Fraction(1)}, Fraction(0))
        add_leq({3: Fraction(1), 4: Fraction(1), 0: Fraction(-1)}, Fraction(0))
    else:
        raise ValueError(f"unknown pinned family {family}")
    add_leq({margin: Fraction(1)}, Fraction(1))

    zero_to_mu = {var: pos for pos, var in enumerate(zero_variables)}
    for primal_var in range(len(lp.variables)):
        stationarity: SparseRow = {}
        for weight_index in range(weight_count):
            coeff = objective_by_weight[primal_var][weight_index]
            if coeff:
                stationarity[weight_index] = stationarity.get(weight_index, Fraction(0)) + coeff
        for active_pos, row_index in enumerate(active_rows):
            coeff = lp.rows[row_index].get(primal_var, Fraction(0))
            if coeff:
                stationarity[lambda_offset + active_pos] = (
                    stationarity.get(lambda_offset + active_pos, Fraction(0)) + coeff
                )
        if primal_var in zero_to_mu:
            stationarity[mu_offset + zero_to_mu[primal_var]] = (
                stationarity.get(mu_offset + zero_to_mu[primal_var], Fraction(0)) - 1
            )
        add_eq(stationarity, Fraction(0))

    objective = tuple(Fraction(0) for _ in range(margin)) + (Fraction(1),)
    return _solve_exact_max_lp(tuple(rows), tuple(rhs), objective, total, tolerance)


def _profile_forms(lp: ReducedCouplingLP) -> dict[str, LinearForm]:
    p1 = _var_form(lp, ("p", 0))
    p2 = _var_form(lp, ("p", 1))
    r1 = _var_form(lp, ("r", 0))
    r2 = _var_form(lp, ("r", 1))
    a1 = _var_form(lp, ("A_left", 0))
    a2 = _var_form(lp, ("A_left", 1))
    theta = _var_form(lp, ("theta",))
    s = _var_form(lp, ("s", 4))
    s_right = _var_form(lp, ("A_right", 4))
    one = _constant_form(Fraction(1))
    b1 = _add_forms(one, _scale_form(r1, -1), _scale_form(a1, -1))
    b2 = _add_forms(one, _scale_form(r2, -1), _scale_form(a2, -1))
    c1 = _add_forms(one, _scale_form(p1, -1), _scale_form(a1, -1))
    c2 = _add_forms(one, _scale_form(p2, -1), _scale_form(a2, -1))
    t_right = _add_forms(one, _scale_form(s, -1), _scale_form(s_right, -1))
    return {
        "theta": theta,
        "one_minus_theta": _add_forms(one, _scale_form(theta, -1)),
        "p1": p1,
        "p2": p2,
        "r1": r1,
        "r2": r2,
        "a1": a1,
        "a2": a2,
        "b1": b1,
        "b2": b2,
        "c1": c1,
        "c2": c2,
        "S": s_right,
        "T": t_right,
    }


def _apply_facet_state(
    cell: PinnedBoundaryCell,
    facet: str,
    form: LinearForm,
    add_eq_form: Any,
    add_margin_leq_form: Any,
) -> None:
    state = cell.state(facet)
    if state == "eq":
        add_eq_form(form)
    elif state == "inactive":
        if facet.endswith("_zero"):
            add_margin_leq_form(_scale_form(form, -1))
        else:
            add_margin_leq_form(form)
    else:
        raise ValueError(f"unexpected state {state} for {facet}")


def _apply_c_t_state(
    cell: PinnedBoundaryCell,
    facet: str,
    c_minus_t: LinearForm,
    add_eq_form: Any,
    add_margin_leq_form: Any,
) -> None:
    state = cell.state(facet)
    if state == "eq":
        add_eq_form(c_minus_t)
    elif state == "lt":
        add_margin_leq_form(c_minus_t)
    elif state == "gt":
        add_margin_leq_form(_scale_form(c_minus_t, -1))
    else:
        raise ValueError(f"unexpected state {state} for {facet}")


def _render_pinned_report(data: dict[str, Any], certificate_path: Path) -> str:
    certs: tuple[PinnedBoundaryCertificate, ...] = data["pinned_boundary_certificates"]
    outcomes = data["pinned_boundary_outcomes"]
    counterexamples = [
        cert for cert in certs if cert.outcome == "rational_reduced_counterexample"
    ]
    unresolved = [cert for cert in certs if cert.outcome == "unresolved_pinned_cell"]
    nonempty = [
        cert
        for cert in certs
        if cert.outcome not in {"empty_pinned_cell", "no_pinned_relative_interior"}
    ]
    tied_count = (
        outcomes.get("coherent_reduced_equality_witness", 0)
        + outcomes.get("deterministic_stt_equality_witness", 0)
    )

    lines: list[str] = []
    lines.append("# DS(2,1) Pinned Boundary Coverage v2")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append("This is a targeted exact rational coverage run for only the remaining A-pinned and B-pinned endpoint/cross-kink cells.  It does not use an unconstrained weight-grid scan as evidence.")
    lines.append("")
    lines.append("The run imposes the pinned equations and strict profile inequalities, splits the listed endpoint/cross-kink facets, and tests the relevant normal cones under the requested slope restrictions.")
    lines.append("")
    lines.append("## Outcome")
    lines.append("")
    if counterexamples:
        first = counterexamples[0]
        lines.append("A rational reduced counterexample was produced.")
        lines.append(f"- Cell: `{first.cell.cell_id}` / `{first.cell.family}`")
        lines.append(f"- Active facets: `{', '.join(first.cell.active_facets)}`")
        lines.append(f"- Weights `(u1,u2,alpha,beta,v)`: `{_format_tuple(first.normal_weights or ())}`")
        lines.append(f"- Reduced optimum: `{rational_to_string(first.reduced_objective)}`")
        lines.append(f"- Deterministic STT optimum: `{rational_to_string(first.stt_optimum)}`")
    elif unresolved:
        lines.append("No rational reduced counterexample was produced, but exact active pinned cells remain unresolved.")
        lines.append(f"- Unresolved cells recorded: `{len(unresolved)}`.")
        lines.append(f"- Cells tied by coherent or deterministic witnesses: `{tied_count}`.")
    else:
        lines.append("No bad exposed pinned endpoint/cross-kink cell remains: every targeted cell is empty/no-relative-interior, has no pinned-slope normal cone, or is tied by a coherent reduced or deterministic STT witness.")
    lines.append("")
    lines.append(f"Coverage certificates written to `{certificate_path}`.")
    lines.append(f"Outcome counts: `{outcomes}`.")
    lines.append("")
    lines.append("## Coverage Summary")
    lines.append("")
    lines.append(f"- Pinned cells considered: `{data['settings']['pinned_cells_considered']}`.")
    lines.append(f"- Nonempty cells with normal-cone work recorded: `{len(nonempty)}`.")
    lines.append("- Coherent-reduced and deterministic-STT-only witnesses are separated in the JSON via `witness_class`.")
    lines.append("")
    lines.append("## Unresolved Cells")
    lines.append("")
    if unresolved:
        lines.append("| cell | family | active facets | active rows | zero vars | normal cone |")
        lines.append("|---|---|---|---:|---:|---|")
        for cert in unresolved[: data["settings"]["max_unresolved"]]:
            lines.append(
                "| {cell} | {family} | `{facets}` | `{rows}` | `{zeros}` | {normal} |".format(
                    cell=cert.cell.cell_id,
                    family=cert.cell.family,
                    facets=",".join(cert.cell.active_facets),
                    rows=",".join(str(row) for row in cert.active_rows),
                    zeros=",".join(str(var) for var in cert.zero_variables),
                    normal=cert.normal_cone.status,
                )
            )
    else:
        lines.append("No unresolved pinned cells remain.")
    lines.append("")
    lines.append("## Skeptical Audit")
    lines.append("")
    lines.append("- This v2 artifact covers only the frontier-listed pinned endpoint/cross-kink families, not the full DS(2,1) arrangement.")
    lines.append("- Strict profile and slope restrictions are represented by exact positive-margin LPs with normalized objective scale.")
    lines.append("- Normal-cone witnesses, reduced objectives, STT comparisons, and coherent-face checks are reconstructed and reported as rational data.")
    lines.append("- Infeasible normal cones are reported per exact active cell; promoted cells require either a rational counterexample or an explicit equality-witness classification.")
    return "\n".join(lines) + "\n"


def _pinned_certificates_json(data: dict[str, Any]) -> dict[str, Any]:
    lp: ReducedCouplingLP = data["lp"]
    return {
        "schema": data["schema"],
        "settings": data["settings"],
        "arrangement": data["arrangement"],
        "pinned_boundary_outcomes": data["pinned_boundary_outcomes"],
        "pinned_boundary_cells": [
            _pinned_cell_json(lp, cert) for cert in data["pinned_boundary_certificates"]
        ],
        "unresolved": data["unresolved"],
    }


def _pinned_cell_json(lp: ReducedCouplingLP, cert: PinnedBoundaryCertificate) -> dict[str, Any]:
    return {
        "cell_id": cert.cell.cell_id,
        "family": cert.cell.family,
        "outcome": cert.outcome,
        "facet_states": dict(cert.cell.facet_states),
        "active_facets": list(cert.cell.active_facets),
        "kink_cell": {
            "psi_active": list(cert.cell.psi_active),
            "gamma_lower_active": [list(rows) for rows in cert.cell.gamma_lower_active],
        },
        "cell_margin_status": {
            "status": cert.cell_feasibility.status,
            "margin": (
                rational_to_string(cert.cell_feasibility.optimum)
                if cert.cell_feasibility.optimum is not None
                else None
            ),
            "max_violation": (
                rational_to_string(cert.cell_feasibility.max_violation)
                if cert.cell_feasibility.max_violation is not None
                else None
            ),
        },
        "normal_cone_status": {
            "status": cert.normal_cone.status,
            "margin": (
                rational_to_string(cert.normal_cone.optimum)
                if cert.normal_cone.optimum is not None
                else None
            ),
            "max_violation": (
                rational_to_string(cert.normal_cone.max_violation)
                if cert.normal_cone.max_violation is not None
                else None
            ),
        },
        "normal_cone_weights": (
            _weights_json(cert.normal_weights) if cert.normal_weights is not None else None
        ),
        "reduced_objective": (
            rational_to_string(cert.reduced_objective)
            if cert.reduced_objective is not None
            else None
        ),
        "stt_optimum": (
            rational_to_string(cert.stt_optimum)
            if cert.stt_optimum is not None
            else None
        ),
        "stt_depth_witness": list(cert.stt_depth_witness),
        "witness_class": _pinned_witness_class(cert),
        "active_rows": [
            {"row_index": row, "descriptor": lp.row_descriptors[row]}
            for row in cert.active_rows
        ],
        "zero_variables": [
            {"var_index": index, "label": list(lp.variables[index])}
            for index in cert.zero_variables
        ],
        "sample_reduced_variables": (
            _values_json(lp, cert.sample_values) if cert.sample_values else None
        ),
        "structural_classification": (
            _structural_classification(lp, cert.sample_values)
            if cert.sample_values
            else None
        ),
        "coherent_witness_status": (
            {
                "status": cert.coherent_witness.status,
                "max_violation": (
                    rational_to_string(cert.coherent_witness.max_violation)
                    if cert.coherent_witness.max_violation is not None
                    else None
                ),
            }
            if cert.coherent_witness is not None
            else None
        ),
    }


def _pinned_witness_class(cert: PinnedBoundaryCertificate) -> str:
    if cert.coherent_witness is not None and cert.coherent_witness.feasible:
        return "coherent-reduced"
    if (
        cert.reduced_objective is not None
        and cert.stt_optimum is not None
        and cert.reduced_objective == cert.stt_optimum
    ):
        return "deterministic-STT-only"
    return "none"


def _unresolved_pinned_cell_json(
    lp: ReducedCouplingLP,
    cert: PinnedBoundaryCertificate,
) -> dict[str, Any]:
    return {
        "cell_id": cert.cell.cell_id,
        "family": cert.cell.family,
        "failed_reason": cert.outcome,
        "facet_states": dict(cert.cell.facet_states),
        "active_facets": list(cert.cell.active_facets),
        "active_rows": [
            {"row_index": row, "descriptor": lp.row_descriptors[row]}
            for row in cert.active_rows
        ],
        "zero_variables": [
            {"var_index": index, "label": list(lp.variables[index])}
            for index in cert.zero_variables
        ],
        "normal_cone_status": cert.normal_cone.status,
        "normal_cone_margin": (
            rational_to_string(cert.normal_cone.optimum)
            if cert.normal_cone.optimum is not None
            else None
        ),
        "normal_cone_weights": (
            _weights_json(cert.normal_weights) if cert.normal_weights is not None else None
        ),
        "reduced_objective": (
            rational_to_string(cert.reduced_objective)
            if cert.reduced_objective is not None
            else None
        ),
        "stt_optimum": (
            rational_to_string(cert.stt_optimum)
            if cert.stt_optimum is not None
            else None
        ),
        "structural_classification": (
            _structural_classification(lp, cert.sample_values)
            if cert.sample_values
            else None
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m scripts.stt_checker.ds21_pinned_boundary"
    )
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--certificates", type=Path, default=DEFAULT_CERTIFICATES)
    args = parser.parse_args(argv)
    result = write_pinned_boundary_outputs(args.report, args.certificates)
    print(
        "wrote {report} and {certificates}: cells={cells} "
        "outcomes={outcomes} unresolved={unresolved}".format(**result)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
