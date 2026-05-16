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


DEFAULT_REPORT = Path("reports/stt_double_star_ds21_normal_cones_v1_coverage.md")
DEFAULT_CERTIFICATES = Path(
    "examples/stt_lp/ds21_normal_cones_v1_coverage_certificates.json"
)
V0_CERTIFICATES = Path("examples/stt_lp/ds21_normal_cones_v0_certificates.json")

WeightVector = tuple[Fraction, Fraction, Fraction, Fraction, Fraction]
SparseRow = dict[int, Fraction]
LinearForm = tuple[Fraction, SparseRow]


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


@dataclass(frozen=True)
class KinkCell:
    cell_id: str
    psi_active: tuple[int, ...]
    gamma_lower_active: tuple[tuple[int, ...], tuple[int, ...]]
    gamma_allocation_active: tuple[tuple[int, ...], tuple[int, ...]]
    c1_t_orientation: str
    c2_t_orientation: str

    @property
    def active_rows(self) -> tuple[int, ...]:
        return tuple(
            sorted(
                self.psi_active
                + self.gamma_lower_active[0]
                + self.gamma_lower_active[1]
                + self.gamma_allocation_active[0]
                + self.gamma_allocation_active[1]
            )
        )


@dataclass(frozen=True)
class KinkCellCertificate:
    cell: KinkCell
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
            return "empty_strict_heavy_cell"
        if not _positive_optimum(self.cell_feasibility):
            return "no_strict_interior"
        if not self.normal_cone.feasible or not _positive_optimum(self.normal_cone):
            return "normal_cone_infeasible_for_strict_heavy_weights"
        if self.reduced_objective is not None and self.stt_optimum is not None:
            if self.reduced_objective < self.stt_optimum:
                return "rational_reduced_counterexample"
            if self.reduced_objective == self.stt_optimum:
                return "deterministic_stt_equality_witness"
        if self.coherent_witness is not None and self.coherent_witness.feasible:
            return "coherent_reduced_equality_witness"
        return "unresolved_strict_heavy_cell"


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


def run_coverage(
    tolerance: float = DEFAULT_TOLERANCE,
    max_unresolved: int = 64,
) -> dict[str, Any]:
    lp = build_reduced_coupling_lp(2, 1, (1, 1, 1, 1, 1))
    objective_by_weight = _objective_coefficient_matrix()
    cells = tuple(_strict_heavy_kink_cells())
    certificates: list[KinkCellCertificate] = []
    unresolved: list[dict[str, Any]] = []
    outcome_counts: dict[str, int] = {}

    for cell in cells:
        cell_feasibility = _strict_heavy_cell_feasibility(
            lp=lp,
            cell=cell,
            tolerance=tolerance,
        )
        if not cell_feasibility.feasible or not _positive_optimum(cell_feasibility):
            outcome = (
                "empty_strict_heavy_cell"
                if not cell_feasibility.feasible
                else "no_strict_interior"
            )
            certificates.append(
                KinkCellCertificate(
                    cell=cell,
                    cell_feasibility=cell_feasibility,
                    active_rows=cell.active_rows,
                    zero_variables=(),
                    normal_cone=ExactOptimizationResult(
                        feasible=False,
                        status="not_run_no_strict_cell_interior",
                    ),
                )
            )
            outcome_counts[outcome] = outcome_counts.get(outcome, 0) + 1
            continue

        sample = cell_feasibility.values[:-1]
        active_rows = _active_rows(lp, sample)
        zero_variables = tuple(index for index, value in enumerate(sample) if value == 0)
        normal_cone = _strict_heavy_normal_cone_feasibility(
            lp=lp,
            active_rows=active_rows,
            zero_variables=zero_variables,
            objective_by_weight=objective_by_weight,
            tolerance=tolerance,
        )

        normal_weights: WeightVector | None = None
        reduced_objective: Fraction | None = None
        stt_value: Fraction | None = None
        stt_depth: tuple[int, ...] = ()
        coherent = None
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

        cert = KinkCellCertificate(
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
        outcome_counts[cert.outcome] = outcome_counts.get(cert.outcome, 0) + 1
        certificates.append(cert)
        if cert.outcome == "rational_reduced_counterexample":
            break
        if cert.outcome == "unresolved_strict_heavy_cell":
            unresolved.append(_unresolved_cell_json(lp, cert))
            if len(unresolved) >= max_unresolved:
                break

    return {
        "schema": "stt_ds21_normal_cones_v1_coverage",
        "settings": {
            "mode": "strict_heavy_smooth_kink_coverage",
            "weight_order": ["u1", "u2", "alpha", "beta", "v"],
            "weight_cone": "sum weights = 1, u1 > u2 >= 0, u1 > v >= 0, alpha >= 0, beta >= 0",
            "strict_family": [
                "p1=p2",
                "a1=S",
                "a1>a2",
                "b_i>c_i, encoded as p_i>r_i for i=1,2",
                "c_i away from T by the enumerated c_i<T / c_i>T cells",
            ],
            "profile_convention": {
                "a_i": "A_left[x_i]",
                "b_i": "1-r_i-A_left[x_i]",
                "c_i": "1-p_i-A_left[x_i]",
                "S": "A_right[y1]",
                "T": "1-s_y-A_right[y1]",
            },
            "kink_cells_considered": len(cells),
            "max_unresolved": max_unresolved,
            "tolerance": tolerance,
        },
        "arrangement": _arrangement_summary(lp),
        "lp": lp,
        "coverage_certificates": tuple(certificates),
        "coverage_outcomes": outcome_counts,
        "unresolved": unresolved,
        "v0_scan": run_scan(grid_bound=3, tolerance=tolerance),
    }


def write_outputs(
    report_path: Path = DEFAULT_REPORT,
    certificate_path: Path = DEFAULT_CERTIFICATES,
    grid_bound: int = 3,
) -> dict[str, Any]:
    data = run_coverage()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    certificate_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(_render_report(data, certificate_path), encoding="utf-8")
    certificate_path.write_text(
        json.dumps(_certificates_json(data), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    V0_CERTIFICATES.parent.mkdir(parents=True, exist_ok=True)
    V0_CERTIFICATES.write_text(
        json.dumps(_v0_certificates_json(data["v0_scan"]), indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    outcomes: dict[str, int] = {}
    for cert in data["coverage_certificates"]:
        outcomes[cert.outcome] = outcomes.get(cert.outcome, 0) + 1
    return {
        "report": str(report_path),
        "certificates": str(certificate_path),
        "v0_certificates": str(V0_CERTIFICATES),
        "faces": len(data["coverage_certificates"]),
        "outcomes": outcomes,
        "unresolved": len(data["unresolved"]),
    }


def write_v0_outputs(
    report_path: Path = Path("reports/stt_double_star_ds21_normal_cones_v0.md"),
    certificate_path: Path = V0_CERTIFICATES,
    grid_bound: int = 3,
) -> dict[str, Any]:
    data = run_scan(grid_bound=grid_bound)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    certificate_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(_render_v0_report(data, certificate_path), encoding="utf-8")
    certificate_path.write_text(
        json.dumps(_v0_certificates_json(data), indent=2, sort_keys=True) + "\n",
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


def _positive_optimum(result: ExactOptimizationResult) -> bool:
    return result.feasible and result.optimum is not None and result.optimum > 0


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
    theta = values[idx[("theta",)]]
    p1 = values[idx[("p", 0)]]
    p2 = values[idx[("p", 1)]]
    r1 = values[idx[("r", 0)]]
    r2 = values[idx[("r", 1)]]
    q = values[idx[("q", 4)]]
    s = values[idx[("s", 4)]]
    a1 = values[idx[("A_left", 0)]]
    a2 = values[idx[("A_left", 1)]]
    b1 = 1 - r1 - a1
    b2 = 1 - r2 - a2
    c1 = 1 - p1 - a1
    c2 = 1 - p2 - a2
    s_a = values[idx[("A_right", 4)]]
    s_b = 1 - s - s_a
    return {
        "theta": theta,
        "p1": p1,
        "p2": p2,
        "r1": r1,
        "r2": r2,
        "q": q,
        "s": s,
        "a1": a1,
        "a2": a2,
        "b1": b1,
        "b2": b2,
        "c1": c1,
        "c2": c2,
        "S": s_a,
        "T": s_b,
    }


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


def _constant_form(value: Fraction) -> LinearForm:
    return value, {}


def _var_form(lp: ReducedCouplingLP, label: tuple[Any, ...]) -> LinearForm:
    return Fraction(0), {lp.variable_index[label]: Fraction(1)}


def _scale_form(form: LinearForm, scale: Fraction | int) -> LinearForm:
    factor = Fraction(scale)
    constant, row = form
    return constant * factor, {index: value * factor for index, value in row.items()}


def _add_forms(*forms: LinearForm) -> LinearForm:
    constant = Fraction(0)
    row: SparseRow = {}
    for form_constant, form_row in forms:
        constant += form_constant
        for index, value in form_row.items():
            row[index] = row.get(index, Fraction(0)) + value
    return constant, {index: value for index, value in row.items() if value}


def _form_minus(left: LinearForm, right: LinearForm) -> LinearForm:
    return _add_forms(left, _scale_form(right, -1))


def _strict_heavy_kink_cells() -> Iterable[KinkCell]:
    psi_options = tuple(
        tuple(row for bit, row in enumerate((25, 26, 27, 28)) if mask & (1 << bit))
        for mask in range(16)
    )
    # In the strict-heavy family a1=S, so x1 has duplicate Gamma lower rows:
    # rows 29 and 31 are both E>=r1, while rows 30 and 32 are both E>=s.
    gamma_x1_lower = ((29, 31), (30, 32), (29, 30, 31, 32))
    # Since a1=S>a2, x2's rows 38 and 37 are strictly dominated by rows 36
    # and 39 respectively.  The only smooth lower cells are therefore these.
    gamma_x2_lower = ((36,), (39,), (36, 39))
    gamma_x1_alloc = ((),)
    gamma_x2_alloc = ((),)
    orientations = ("lt", "gt")
    counter = 1
    for psi in psi_options:
        for lower_1 in gamma_x1_lower:
            for lower_2 in gamma_x2_lower:
                for alloc_1 in gamma_x1_alloc:
                    for alloc_2 in gamma_x2_alloc:
                        for c1_t in orientations:
                            for c2_t in orientations:
                                yield KinkCell(
                                    cell_id=f"strict-heavy-cell-{counter:05d}",
                                    psi_active=psi,
                                    gamma_lower_active=(lower_1, lower_2),
                                    gamma_allocation_active=(alloc_1, alloc_2),
                                    c1_t_orientation=c1_t,
                                    c2_t_orientation=c2_t,
                                )
                                counter += 1


def _strict_heavy_cell_feasibility(
    lp: ReducedCouplingLP,
    cell: KinkCell,
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

    def add_margin_leq(row: SparseRow, bound: Fraction) -> None:
        with_margin = dict(row)
        with_margin[margin] = with_margin.get(margin, Fraction(0)) + 1
        add_leq(with_margin, bound)

    p1 = _var_form(lp, ("p", 0))
    p2 = _var_form(lp, ("p", 1))
    r1 = _var_form(lp, ("r", 0))
    r2 = _var_form(lp, ("r", 1))
    a1 = _var_form(lp, ("A_left", 0))
    a2 = _var_form(lp, ("A_left", 1))
    s_right = _var_form(lp, ("A_right", 4))
    s = _var_form(lp, ("s", 4))
    c1 = _add_forms(_constant_form(Fraction(1)), _scale_form(p1, -1), _scale_form(a1, -1))
    c2 = _add_forms(_constant_form(Fraction(1)), _scale_form(p2, -1), _scale_form(a2, -1))
    t_right = _add_forms(_constant_form(Fraction(1)), _scale_form(s, -1), _scale_form(s_right, -1))

    add_eq(_form_minus(p1, p2)[1], -_form_minus(p1, p2)[0])
    add_eq(_form_minus(a1, s_right)[1], -_form_minus(a1, s_right)[0])
    add_margin_leq(_form_minus(a2, a1)[1], -_form_minus(a2, a1)[0])
    add_margin_leq(_form_minus(r1, p1)[1], -_form_minus(r1, p1)[0])
    add_margin_leq(_form_minus(r2, p2)[1], -_form_minus(r2, p2)[0])

    for form, orientation in ((c1, cell.c1_t_orientation), (c2, cell.c2_t_orientation)):
        diff = _form_minus(form, t_right)
        if orientation == "lt":
            # c_i < T.
            add_margin_leq(diff[1], -diff[0])
        else:
            # c_i > T.
            reverse = _form_minus(t_right, form)
            add_margin_leq(reverse[1], -reverse[0])

    kink_rows = set(range(25, 33)) | set(range(36, 40))
    active = set(cell.active_rows)
    for row_index in sorted(kink_rows):
        row = lp.rows[row_index]
        bound = lp.rhs[row_index]
        if row_index in active:
            add_eq(row, bound)
        else:
            add_margin_leq(row, bound)

    add_leq({margin: Fraction(1)}, Fraction(1))
    objective = tuple(Fraction(0) for _ in range(margin)) + (Fraction(1),)
    return _solve_exact_max_lp(tuple(rows), tuple(rhs), objective, variable_count, tolerance)


def _strict_heavy_normal_cone_feasibility(
    lp: ReducedCouplingLP,
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

    # Normalize the objective scale and require the strict-heavy inequalities
    # with a positive margin in that scale.
    add_eq({index: Fraction(1) for index in range(weight_count)}, Fraction(1))
    add_leq({1: Fraction(1), 0: Fraction(-1), margin: Fraction(1)}, Fraction(0))
    add_leq({4: Fraction(1), 0: Fraction(-1), margin: Fraction(1)}, Fraction(0))
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


def _solve_exact_max_lp(
    rows: tuple[SparseRow, ...],
    rhs: tuple[Fraction, ...],
    objective: tuple[Fraction, ...],
    variable_count: int,
    tolerance: float = DEFAULT_TOLERANCE,
) -> ExactOptimizationResult:
    matrix = [[0.0 for _ in range(variable_count)] for _ in rows]
    for row_index, row in enumerate(rows):
        for col, value in row.items():
            matrix[row_index][col] = float(value)
    result = _simplex_maximize(
        matrix,
        [float(value) for value in rhs],
        [float(value) for value in objective],
        tolerance=tolerance,
    )
    if result.status != 0:
        return ExactOptimizationResult(False, status=result.message)
    try:
        values = tuple(_exact_primal_from_basis(rows, rhs, result.basis, variable_count))
    except ValueError as exc:
        rationalized = tuple(
            Fraction(value).limit_denominator(1_000_000)
            for value in result.solution
        )
        violation = _max_primal_violation(rows, rhs, list(rationalized))
        if violation == 0:
            optimum = sum(objective[index] * rationalized[index] for index in range(variable_count))
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
    optimum = sum(objective[index] * values[index] for index in range(variable_count))
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
    certs: tuple[KinkCellCertificate, ...] = data["coverage_certificates"]
    outcomes = data["coverage_outcomes"]
    counterexamples = [
        cert for cert in certs if cert.outcome == "rational_reduced_counterexample"
    ]
    unresolved = [
        cert for cert in certs if cert.outcome == "unresolved_strict_heavy_cell"
    ]
    nonempty = [
        cert
        for cert in certs
        if cert.outcome != "empty_strict_heavy_cell"
        and cert.outcome != "no_strict_interior"
    ]
    infeasible_count = outcomes.get("normal_cone_infeasible_for_strict_heavy_weights", 0)
    tied_count = (
        outcomes.get("deterministic_stt_equality_witness", 0)
        + outcomes.get("coherent_reduced_equality_witness", 0)
    )

    lines: list[str] = []
    lines.append("# DS(2,1) Strict-Heavy Normal-Cone Coverage v1")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append("This v1 run is a coverage certificate for the remaining smooth strict-heavy kink family, not another unconstrained weight-grid scan.  It uses the exact reduced `LB_H1` extended LP and enumerates the relevant `Psi/Gamma` kink cells after imposing `p1=p2`, `a1=S`, `a1>a2`, `b_i>c_i`, and the split cells `c_i<T` / `c_i>T`.")
    lines.append("")
    lines.append("The profile convention is `a_i=A_left[x_i]`, `b_i=1-r_i-A_left[x_i]`, `c_i=1-p_i-A_left[x_i]`, `S=A_right[y1]`, and `T=1-s_y-A_right[y1]`.  Thus `b_i>c_i` is the smooth condition `p_i>r_i` already visible in the reduced LP.")
    lines.append("")
    lines.append("## Outcome")
    lines.append("")
    if counterexamples:
        first = counterexamples[0]
        lines.append("A rational reduced counterexample was found in the strict-heavy coverage run.")
        lines.append(f"- Cell: `{first.cell.cell_id}`")
        lines.append(f"- Weights `(u1,u2,alpha,beta,v)`: `{_format_tuple(first.normal_weights or ())}`")
        lines.append(f"- Reduced optimum: `{rational_to_string(first.reduced_objective)}`")
        lines.append(f"- Deterministic STT optimum: `{rational_to_string(first.stt_optimum)}`")
    elif unresolved:
        lines.append("No rational reduced counterexample was produced, but some strict-heavy cells remain unresolved for theorem-chat extraction.")
        lines.append(f"- Unresolved cells recorded: `{len(unresolved)}`.")
        lines.append(f"- Normal-cone infeasible cells: `{infeasible_count}`.")
        lines.append(f"- Cells tied by coherent or deterministic witnesses: `{tied_count}`.")
    else:
        lines.append("No bad exposed strict-heavy smooth cell remains in this exact coverage run: every strict cell either has no strict-heavy normal cone or is tied by a coherent reduced witness or deterministic STT equality.")
    lines.append("")
    lines.append(f"Coverage certificates written to `{certificate_path}`.")
    lines.append(f"Outcome counts: `{outcomes}`.")
    lines.append("")
    lines.append("## Coverage Summary")
    lines.append("")
    lines.append(f"- Kink cells considered after strict-heavy pruning: `{data['settings']['kink_cells_considered']}`.")
    lines.append(f"- Nonempty strict cells with normal-cone work recorded: `{len(nonempty)}`.")
    lines.append(f"- V0 discovered grid faces retained with structural classifications: `{len(data['v0_scan']['certificates'])}`.")
    lines.append("")
    lines.append("## Unresolved Strict-Heavy Cells")
    lines.append("")
    if unresolved:
        lines.append("| cell | c1/T | c2/T | active rows | zero vars | normal cone | reason |")
        lines.append("|---|---|---|---:|---:|---|---|")
        for cert in unresolved[: data["settings"]["max_unresolved"]]:
            lines.append(
                "| {cell} | {c1} | {c2} | `{rows}` | `{zeros}` | {normal} | {reason} |".format(
                    cell=cert.cell.cell_id,
                    c1=cert.cell.c1_t_orientation,
                    c2=cert.cell.c2_t_orientation,
                    rows=",".join(str(row) for row in cert.active_rows),
                    zeros=",".join(str(var) for var in cert.zero_variables),
                    normal=cert.normal_cone.status,
                    reason=cert.outcome,
                )
            )
    else:
        lines.append("No unresolved strict-heavy cells remain.")
    lines.append("")
    lines.append("## Skeptical Audit")
    lines.append("")
    lines.append("- This certificate targets the named smooth strict-heavy blocker only; it does not claim full 61-halfspace arrangement enumeration.")
    lines.append("- Strictness is modeled by exact positive interior margins under normalized objective scale, not by floating tolerances.")
    lines.append("- The v0 deterministic grid scan is retained only as context and now carries structural classifications for each discovered face.")
    lines.append("- Coherent-reduced witnesses and deterministic-STT-only ties are reported separately in the JSON.")
    return "\n".join(lines) + "\n"


def _render_v0_report(data: dict[str, Any], certificate_path: Path) -> str:
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
        "coverage_outcomes": data["coverage_outcomes"],
        "strict_heavy_cells": [
            _coverage_cell_json(lp, cert) for cert in data["coverage_certificates"]
        ],
        "unresolved": data["unresolved"],
        "v0_discovered_faces": [
            _face_json(data["v0_scan"]["lp"], cert)
            for cert in data["v0_scan"]["certificates"]
        ],
    }


def _v0_certificates_json(data: dict[str, Any]) -> dict[str, Any]:
    lp: ReducedCouplingLP = data["lp"]
    return {
        "schema": data["schema"],
        "settings": data["settings"],
        "arrangement": data["arrangement"],
        "faces": [_face_json(lp, cert) for cert in data["certificates"]],
        "unresolved": data["unresolved"],
    }


def _coverage_cell_json(lp: ReducedCouplingLP, cert: KinkCellCertificate) -> dict[str, Any]:
    return {
        "cell_id": cert.cell.cell_id,
        "outcome": cert.outcome,
        "kink_cell": {
            "psi_active": list(cert.cell.psi_active),
            "gamma_lower_active": [list(rows) for rows in cert.cell.gamma_lower_active],
            "gamma_allocation_active": [
                list(rows) for rows in cert.cell.gamma_allocation_active
            ],
            "c1_t_orientation": cert.cell.c1_t_orientation,
            "c2_t_orientation": cert.cell.c2_t_orientation,
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
        "witness_class": _witness_class(cert),
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


def _witness_class(cert: KinkCellCertificate | FaceCertificate) -> str:
    coherent = getattr(cert, "coherent_witness", None)
    if coherent is not None and coherent.feasible:
        return "coherent-reduced"
    reduced_objective = getattr(cert, "reduced_objective", None)
    if reduced_objective is None:
        reduced_objective = getattr(cert, "sample_objective", None)
    stt_optimum = getattr(cert, "stt_optimum", None)
    if reduced_objective is not None and stt_optimum is not None and reduced_objective == stt_optimum:
        return "deterministic-STT-only"
    return "none"


def _structural_classification(
    lp: ReducedCouplingLP,
    values: tuple[Fraction, ...],
) -> dict[str, Any]:
    profile = _profile_values(lp, values)

    def diff(left: str, right: str) -> dict[str, str]:
        value = profile[left] - profile[right]
        return {"value": rational_to_string(value), "sign": _sign_label(value)}

    return {
        "theta": rational_to_string(profile["theta"]),
        "p1_minus_p2": diff("p1", "p2"),
        "a1_minus_a2": diff("a1", "a2"),
        "b1_minus_b2": diff("b1", "b2"),
        "a1_minus_S": diff("a1", "S"),
        "a2_minus_S": diff("a2", "S"),
        "c1_minus_T": diff("c1", "T"),
        "c2_minus_T": diff("c2", "T"),
        "b1_minus_c1": diff("b1", "c1"),
        "b2_minus_c2": diff("b2", "c2"),
    }


def _sign_label(value: Fraction) -> str:
    if value < 0:
        return "negative"
    if value > 0:
        return "positive"
    return "zero"


def _unresolved_cell_json(lp: ReducedCouplingLP, cert: KinkCellCertificate) -> dict[str, Any]:
    return {
        "cell_id": cert.cell.cell_id,
        "failed_reason": cert.outcome,
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
        "structural_classification": (
            _structural_classification(lp, cert.sample_values)
            if cert.sample_values
            else None
        ),
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
        "structural_classification": _structural_classification(lp, cert.sample_values),
        "witness_class": _witness_class(cert),
        "witness_is_coherent_reduced": cert.coherent_witness.feasible,
        "witness_is_deterministic_stt_only": (
            (not cert.coherent_witness.feasible)
            and cert.sample_objective == cert.stt_optimum
        ),
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
