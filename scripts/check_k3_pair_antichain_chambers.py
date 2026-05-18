"""Enumerate the k=3 pair-antichain support chambers for the public-star oracle.

The chamber fan is finite for fixed star weights ``(u_1,u_2,u_3, alpha)``.
This script records the first audit chamber, centered on the symmetric
regression witness from the prompt.  It also records exact oracle values for
the prompt-provided boundary and positive-interior scalar-regression rays.

Finite k=3 output is not promoted to an all-k theorem.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import sys
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.star_support_oracle import (
    k3_pair_chambers,
    min_cut_F_value,
    oracle_payload,
    pair_supports,
    rational_payload,
    source_deletion_delta,
    support_oracle,
)


DEFAULT_CHAMBERS = Path("data/k3_pair_antichain_chambers.json")
DEFAULT_REPORT = Path("reports/mixed_support_oracle_report.md")


def pair_lambda(values: tuple[Fraction, Fraction, Fraction]) -> dict[tuple[int, ...], Fraction]:
    return {pair: value for pair, value in zip(pair_supports(3), values) if value}


def run_audit() -> dict[str, Any]:
    symmetric_u = (Fraction(1), Fraction(1), Fraction(1))
    symmetric_alpha = Fraction(1)
    chambers = k3_pair_chambers(symmetric_u, symmetric_alpha)

    unit_results = {}
    for index, pair in enumerate(pair_supports(3)):
        values = [Fraction(0), Fraction(0), Fraction(0)]
        values[index] = Fraction(1)
        unit_results[f"lambda_{pair[0] + 1}{pair[1] + 1}"] = oracle_payload(
            support_oracle(3, symmetric_u, symmetric_alpha, pair_lambda(tuple(values)))
        )
    triangle = oracle_payload(
        support_oracle(
            3,
            symmetric_u,
            symmetric_alpha,
            pair_lambda((Fraction(1), Fraction(1), Fraction(1))),
            direct_lp_check=True,
        )
    )

    regressions = [
        {
            "name": "existing_boundary_ray",
            "full_weights_l1_l2_l3_a_b_r": ["0", "1", "1", "0", "1", "0"],
            "u": (Fraction(0), Fraction(1), Fraction(1)),
            "alpha": Fraction(0),
            "lambda": (Fraction(1), Fraction(1), Fraction(1)),
        },
        {
            "name": "prompt_positive_interior_scalar_counterexample",
            "full_weights_l1_l2_l3_a_b_r": ["1/2", "19/2", "20/3", "1/3", "5", "5"],
            "u": (Fraction(1, 2), Fraction(19, 2), Fraction(20, 3)),
            "alpha": Fraction(1, 3),
            "lambda": (Fraction(1), Fraction(1), Fraction(1)),
        },
    ]
    regression_payloads = []
    for regression in regressions:
        F, active_cuts = min_cut_F_value(3, regression["u"], regression["alpha"])
        deltas = {
            f"delta_{i + 1}{j + 1}": rational_payload(
                source_deletion_delta(3, regression["u"], regression["alpha"], (i, j))
            )
            for i, j in pair_supports(3)
        }
        regression_payloads.append(
            {
                "name": regression["name"],
                "full_weights_l1_l2_l3_a_b_r": regression["full_weights_l1_l2_l3_a_b_r"],
                "star_weights": {
                    "u": [rational_payload(value) for value in regression["u"]],
                    "alpha": rational_payload(regression["alpha"]),
                },
                "F": rational_payload(F),
                "active_min_cuts": [[f"l{i + 1}" for i in cut] for cut in active_cuts],
                "pair_source_deletion_deltas": deltas,
                "triangle_oracle": oracle_payload(
                    support_oracle(
                        3,
                        regression["u"],
                        regression["alpha"],
                        pair_lambda(regression["lambda"]),
                    )
                ),
            }
        )

    return {
        "schema": "k3_pair_antichain_chambers_v1",
        "overclaim_guard": (
            "Finite k=3 exact chamber data only. This does not prove public-LP "
            "exactness, b-root closure, or an all-k mixed-support theorem."
        ),
        "public_boundary": {
            "allowed_rows": [
                "unordered R_ij variables",
                "ordered collinear-triplet Q_ikj variables",
                "capping rows R_ij <= Q_ikj + Q_jki",
                "frequency rows R_xv + sum_y Q_xvy <= w_x",
            ],
            "forbidden_rows": [
                "H1",
                "H2",
                "refined-Z",
                "path monotonicity",
                "ancestry transitivity",
                "LCA separation",
                "non-public internal lifts",
                "grouped Bellman rays as public-dual extreme cuts",
            ],
        },
        "symmetric_star_face": {
            "u": ["1", "1", "1"],
            "alpha": "1",
            "unit_pair_results": unit_results,
            "triangle_result": triangle,
            "witness_check": {
                "Phi_12": unit_results["lambda_12"]["Phi"],
                "Phi_13": unit_results["lambda_13"]["Phi"],
                "Phi_23": unit_results["lambda_23"]["Phi"],
                "Phi_triangle": triangle["Phi"],
                "expected": {
                    "Phi_12": "2",
                    "Phi_13": "2",
                    "Phi_23": "2",
                    "Phi_triangle": "3",
                },
                "status": "verified" if (
                    unit_results["lambda_12"]["Phi"] == "2"
                    and unit_results["lambda_13"]["Phi"] == "2"
                    and unit_results["lambda_23"]["Phi"] == "2"
                    and triangle["Phi"] == "3"
                ) else "failed",
            },
            "chambers": chambers,
            "chamber_count": len(chambers),
        },
        "regressions": regression_payloads,
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_report(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    symmetric = payload["symmetric_star_face"]
    lines: list[str] = []
    lines.append("# Mixed-Support Public-Star Oracle Audit")
    lines.append("")
    lines.append("## Stop Sign")
    lines.append("")
    lines.append(
        "This is an exact finite k=3 audit of the public-star support oracle. "
        "It does not claim public-LP exactness on `DS(k,1)`, does not close the "
        "b-root branch, and does not promote k=3 chamber data to an all-k theorem."
    )
    lines.append("")
    lines.append("## Oracle")
    lines.append("")
    lines.append(
        "The corrected edge-cover network has leaf supplies `u_i`, singleton "
        "items of capacity `min(alpha,u_i)`, and pair items of capacity "
        "`min(u_i,u_j)`. Its exact max-flow value matches the corrected min-cut "
        "formula for `F(L)` in the recorded checks."
    )
    lines.append("")
    lines.append("For nonnegative support multipliers, the script computes")
    lines.append("")
    lines.append("```text")
    lines.append("Phi(lambda)=sum_i A_i(lambda)u_i - MC_lambda(F(L)).")
    lines.append("```")
    lines.append("")
    lines.append("## Symmetric Witness")
    lines.append("")
    check = symmetric["witness_check"]
    lines.append(f"- `Phi(1_12)`: `{check['Phi_12']}`")
    lines.append(f"- `Phi(1_13)`: `{check['Phi_13']}`")
    lines.append(f"- `Phi(1_23)`: `{check['Phi_23']}`")
    lines.append(f"- `Phi(1_12+1_13+1_23)`: `{check['Phi_triangle']}`")
    lines.append(f"- status: `{check['status']}`")
    lines.append(f"- direct LP cross-check vertices: `{symmetric['triangle_result']['direct_lp_vertex_count']}`")
    lines.append("")
    lines.append("## Chamber Fan")
    lines.append("")
    lines.append(f"The symmetric k=3 pair-antichain fan has `{symmetric['chamber_count']}` active min-cost forms.")
    lines.append("")
    lines.append("| chamber | min-cost coefficients `(12,13,23)` | Phi coefficients `(12,13,23)` | witness lambda |")
    lines.append("|---:|---:|---:|---:|")
    for index, chamber in enumerate(symmetric["chambers"], start=1):
        mc = chamber["min_cost_coefficients"]
        phi = chamber["phi_coefficients"]
        witness = chamber["region"]["witness_lambda"]
        lines.append(
            "| {index} | `({mc12},{mc13},{mc23})` | `({p12},{p13},{p23})` | `({w12},{w13},{w23})` |".format(
                index=index,
                mc12=mc["lambda_12"],
                mc13=mc["lambda_13"],
                mc23=mc["lambda_23"],
                p12=phi["lambda_12"],
                p13=phi["lambda_13"],
                p23=phi["lambda_23"],
                w12=witness["lambda_12"],
                w13=witness["lambda_13"],
                w23=witness["lambda_23"],
            )
        )
    lines.append("")
    lines.append("## Regression Rays")
    lines.append("")
    for regression in payload["regressions"]:
        lines.append(f"- `{regression['name']}` weights `{regression['full_weights_l1_l2_l3_a_b_r']}`: `F={regression['F']}`, triangle `Phi={regression['triangle_oracle']['Phi']}`.")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("")
    lines.append(f"- `{DEFAULT_CHAMBERS}`")
    lines.append("- `data/mixed_support_certificates.json`")
    lines.append("- `data/mixed_support_obstructions.json`")
    lines.append(f"- `{path}`")
    lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_CHAMBERS)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args(argv)
    payload = run_audit()
    write_json(args.output, payload)
    write_report(args.report, payload)
    print(
        "k3 pair-antichain chambers: "
        f"chambers={payload['symmetric_star_face']['chamber_count']} "
        f"witness={payload['symmetric_star_face']['witness_check']['status']} "
        f"output={args.output} report={args.report}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
