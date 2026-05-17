"""Exact DS(1,1) b-root public-dual envelope audit.

This script reconstructs the public-only DS(1,1) residual envelope from the
R/Q constraints in the handoff prompt.  The named 12-envelope source
certificate is not present in this checkout; when that certificate cannot be
loaded, the script reports that fact explicitly and audits the two exact star
Bellman chambers that are reconstructible from first principles.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
from typing import Any

from public_dual_dsk1_common import (
    add_scaled,
    augmentation_projected_cuts,
    chamber_rows_for_depth,
    clean_linear,
    cone_membership_certificate,
    depth_cost,
    dsk1_tree_depth_vectors,
    format_linear,
    linear_to_json,
    rational_to_string,
    star_depth_vectors,
)


PARAMETERS = ("u1", "alpha", "beta", "gamma")


def substitute_ds11_case(row: dict[str, Fraction], residual_case: str) -> dict[str, Fraction]:
    """Substitute t=alpha+u1+gamma and the exact DS(1,1) star residual."""

    result = dict(row)
    coeff_t = result.pop("t", Fraction(0))
    if coeff_t:
        result["alpha"] = result.get("alpha", Fraction(0)) + coeff_t
        result["u1"] = result.get("u1", Fraction(0)) + coeff_t
        result["gamma"] = result.get("gamma", Fraction(0)) + coeff_t
    coeff_s = result.pop("s1", Fraction(0))
    if coeff_s:
        if residual_case == "center_root_star":
            pass
        elif residual_case == "leaf_root_star":
            result["u1"] = result.get("u1", Fraction(0)) + coeff_s
            result["alpha"] = result.get("alpha", Fraction(0)) - coeff_s
        else:
            raise ValueError(f"unknown residual case {residual_case}")
    return clean_linear(result)


def selected_broot_depth(star_depth: dict[str, int]) -> dict[str, int]:
    return {
        "l1": star_depth["l1"] + 1,
        "a": star_depth["a"] + 1,
        "b": 0,
        "r": 1,
    }


def small_integer_counterexample(
    chamber_rows: list[dict[str, Fraction]],
    target_row: dict[str, Fraction],
    bound: int = 8,
) -> dict[str, str] | None:
    """Find a tiny exact nonnegative integer point violating target_row <= 0."""

    for total in range(1, 4 * bound + 1):
        for u1 in range(bound + 1):
            for alpha in range(bound + 1):
                for beta in range(bound + 1):
                    gamma = total - u1 - alpha - beta
                    if gamma < 0 or gamma > bound:
                        continue
                    point = {
                        "u1": Fraction(u1),
                        "alpha": Fraction(alpha),
                        "beta": Fraction(beta),
                        "gamma": Fraction(gamma),
                    }
                    if any(eval_linear(row, point) > 0 for row in chamber_rows):
                        continue
                    if eval_linear(target_row, point) > 0:
                        return {
                            key: rational_to_string(value)
                            for key, value in point.items()
                        }
    return None


def eval_linear(row: dict[str, Fraction], point: dict[str, Fraction]) -> Fraction:
    return sum((coeff * point.get(key, Fraction(0)) for key, coeff in row.items()), Fraction(0))


def cut_rows_from_projection(projection: dict[str, Any]) -> list[dict[str, Fraction]]:
    rows = []
    for cut in projection["cuts"]:
        row = {"t": Fraction(1)}
        for key, text_value in cut["expression"].items():
            row[key] = row.get(key, Fraction(0)) - Fraction(text_value)
        rows.append(clean_linear(row))
    for side in projection["side_conditions"]:
        rows.append({key: Fraction(value) for key, value in side.items()})
    return rows


def run_audit() -> dict[str, Any]:
    projection = augmentation_projected_cuts(1, max_rows=250000)
    all_tree_costs = [depth_cost(depths) for depths in dsk1_tree_depth_vectors(1)]
    star_cases = []
    for star_depth in star_depth_vectors(1):
        if star_depth["a"] == 0:
            residual_case = "center_root_star"
            residual_formula = {"s1": "0"}
        else:
            residual_case = "leaf_root_star"
            residual_formula = {"s1": "u1 - alpha"}
        selected_depth = selected_broot_depth(star_depth)
        selected_cost = depth_cost(selected_depth)
        chamber_rows = chamber_rows_for_depth(selected_cost, all_tree_costs, PARAMETERS)
        checked = []
        failures = []
        for index, row in enumerate(cut_rows_from_projection(projection)):
            substituted = substitute_ds11_case(row, residual_case)
            certificate = cone_membership_certificate(chamber_rows, substituted, PARAMETERS)
            counterexample = None
            status = "verified_by_exact_conic_certificate"
            if certificate is None:
                counterexample = small_integer_counterexample(chamber_rows, substituted)
                status = "failed_with_small_exact_counterexample" if counterexample else "missing_conic_certificate"
                failures.append(
                    {
                        "index": index,
                        "row_after_substitution": linear_to_json(substituted),
                        "counterexample": counterexample,
                    }
                )
            checked.append(
                {
                    "index": index,
                    "raw_row": linear_to_json(row),
                    "after_substitution": linear_to_json(substituted),
                    "status": status,
                    "certificate": certificate,
                    "counterexample": counterexample,
                }
            )
        star_cases.append(
            {
                "case": residual_case,
                "star_depth": star_depth,
                "broot_depth": selected_depth,
                "broot_cost": linear_to_json(selected_cost),
                "target": "alpha + u1 + gamma",
                "residual_formula": residual_formula,
                "chamber_rows": [linear_to_json(row) for row in chamber_rows],
                "checked_rows": checked,
                "failures": failures,
                "verified": not failures,
            }
        )
    source_paths = [
        Path("public_lp_bridge_augmented_flow_audit_report_2026_05_17.md"),
        Path("b_root_star_deficit_cut_domination_audit_pass_2026_05_17.md"),
        Path("public_lp_bridge_step_back_2026_05_17.md"),
    ]
    return {
        "schema": "ds11_broot_envelope_exact_audit_v0",
        "source_certificate_status": {
            "named_12_envelope_certificate_loaded": False,
            "missing_paths": [str(path) for path in source_paths if not path.exists()],
            "interpretation": (
                "No claimed 12-envelope certificate file was available. The audit "
                "therefore checks the reconstructed public-only DS(1,1) envelope "
                "rows produced by Fourier-Motzkin projection of A_b(s)."
            ),
        },
        "augmentation_projection_status": projection["projection_status"],
        "augmentation_cut_count": len(projection["cuts"]),
        "augmentation_side_condition_count": len(projection["side_conditions"]),
        "cases": star_cases,
        "verified": projection["projection_status"] == "complete"
        and all(case["verified"] for case in star_cases),
    }


def format_report(data: dict[str, Any]) -> str:
    lines = [
        "# DS(1,1) b-root Envelope Hardening",
        "",
        f"Source 12-envelope certificate loaded: `{data['source_certificate_status']['named_12_envelope_certificate_loaded']}`.",
        f"Projection status: `{data['augmentation_projection_status']}`.",
        f"Cut rows: `{data['augmentation_cut_count']}`; side rows: `{data['augmentation_side_condition_count']}`.",
        f"Overall reconstructed-envelope verdict: `{'verified' if data['verified'] else 'not verified'}`.",
        "",
    ]
    for case in data["cases"]:
        lines.append(f"## {case['case']}")
        lines.append("")
        lines.append(f"- b-root depth: `{case['broot_depth']}`")
        lines.append(f"- b-root full cost: `{case['broot_cost']}`")
        lines.append(f"- augmentation target: `{case['target']}`")
        lines.append(f"- residual formula: `{case['residual_formula']}`")
        lines.append(f"- verified: `{case['verified']}`")
        lines.append("")
        lines.append("| row | after substitution | status |")
        lines.append("| --- | --- | --- |")
        for checked in case["checked_rows"]:
            row_text = format_linear(
                {key: Fraction(value) for key, value in checked["after_substitution"].items()}
            )
            lines.append(f"| {checked['index']} | `{row_text} <= 0` | `{checked['status']}` |")
        lines.append("")
        if case["failures"]:
            lines.append("Failures or missing inequalities:")
            for failure in case["failures"]:
                lines.append(
                    f"- row `{failure['index']}`: `{failure['row_after_substitution']}`, "
                    f"counterexample `{failure['counterexample']}`"
                )
            lines.append("")
    lines.append("No H1/H2/refined-Z/path-monotonicity/ancestry-transitivity/LCA-separation rows were used.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    data = run_audit()
    data_path = Path("data/ds11_broot_envelope_audit.json")
    report_path = Path("reports/ds11_broot_envelope_audit.md")
    data_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_path.write_text(format_report(data), encoding="utf-8")
    print(f"wrote {data_path}")
    print(f"wrote {report_path}")
    print(f"verified: {data['verified']}")


if __name__ == "__main__":
    main()
