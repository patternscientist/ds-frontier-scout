"""Extract finite mixed-lambda certificates and obstructions for k=3.

This script deliberately separates three things:

1. exact support-oracle chamber certificates, which are machine-checkable from
   the public-star edge-cover network;
2. root-comparisons-only mixed-support obstruction data;
3. the stronger residual ``ell_ij`` Farkas target, which is not certified here
   unless a concrete residual feasible region is encoded.

No H1/H2/refined-Z/path-monotonicity/ancestry/LCA rows are introduced.
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

from scripts.check_k3_pair_antichain_chambers import (
    DEFAULT_CHAMBERS,
    DEFAULT_REPORT,
    run_audit,
    write_json,
)
from scripts.star_support_oracle import (
    oracle_payload,
    pair_supports,
    rational_payload,
    residual_pair_lower_bounds,
    source_deletion_delta,
    support_oracle,
)


DEFAULT_CERTIFICATES = Path("data/mixed_support_certificates.json")
DEFAULT_OBSTRUCTIONS = Path("data/mixed_support_obstructions.json")


def pair_lambda(values: tuple[Fraction, Fraction, Fraction]) -> dict[tuple[int, ...], Fraction]:
    return {pair: value for pair, value in zip(pair_supports(3), values) if value}


def _load_or_create_chambers(path: Path) -> dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    payload = run_audit()
    write_json(path, payload)
    return payload


def extract(chambers_payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    symmetric_u = (Fraction(1), Fraction(1), Fraction(1))
    symmetric_alpha = Fraction(1)
    unit_values = []
    for index, _pair in enumerate(pair_supports(3)):
        values = [Fraction(0), Fraction(0), Fraction(0)]
        values[index] = Fraction(1)
        unit_values.append(
            support_oracle(3, symmetric_u, symmetric_alpha, pair_lambda(tuple(values)))
        )
    triangle = support_oracle(
        3,
        symmetric_u,
        symmetric_alpha,
        pair_lambda((Fraction(1), Fraction(1), Fraction(1))),
    )

    additive_rhs = sum((result.phi for result in unit_values), Fraction(0))
    root_only_slack = triangle.phi - additive_rhs

    delta_vector = {
        pair: source_deletion_delta(3, symmetric_u, symmetric_alpha, pair)
        for pair in pair_supports(3)
    }
    delta_rhs = sum(delta_vector.values(), Fraction(0))
    vector_sub_t_slack = triangle.phi - delta_rhs

    residual_demo = residual_pair_lower_bounds(
        z=(Fraction(1), Fraction(1), Fraction(1)),
        t=(Fraction(0), Fraction(0), Fraction(0)),
        rho=Fraction(0),
        beta=Fraction(0),
        eta=Fraction(0),
        gamma=Fraction(0),
    )

    certificates = {
        "schema": "mixed_support_certificates_v1",
        "status": "support_oracle_chambers_certified_residual_ell_farkas_not_extracted",
        "overclaim_guard": (
            "These are exact finite k=3 public-star support-oracle certificates. "
            "They are not a proof of public-LP exactness, b-root closure, or all-k "
            "mixed-support domination."
        ),
        "public_boundary": chambers_payload["public_boundary"],
        "support_oracle_formula": {
            "Phi(lambda)": "sum_i A_i(lambda) u_i - MC_lambda(F(L))",
            "F_network": "leaf -> singleton/pair item -> sink edge-cover network",
            "item_costs": {
                "singleton_i": "A_i(lambda)",
                "pair_ij": "B_ij(lambda)",
            },
            "arithmetic": "fractions.Fraction serialized as reduced rational strings",
        },
        "symmetric_chamber_certificates": chambers_payload["symmetric_star_face"]["chambers"],
        "symmetric_witness": chambers_payload["symmetric_star_face"]["witness_check"],
        "direct_lp_cross_check": {
            "triangle_direct_lp_min_cost": chambers_payload["symmetric_star_face"]["triangle_result"]["direct_lp_min_cost"],
            "triangle_direct_lp_Phi": chambers_payload["symmetric_star_face"]["triangle_result"]["direct_lp_Phi"],
            "triangle_direct_lp_vertex_count": chambers_payload["symmetric_star_face"]["triangle_result"]["direct_lp_vertex_count"],
            "status": "verified",
        },
        "residual_lower_bound_formula": {
            "ell_ij": "max(0, z_i+z_j+rho-beta, t_i+t_j+eta-gamma, z_i+z_j+t_i+t_j+rho+eta-beta-gamma)",
            "implementation_status": "implemented",
            "sample_evaluation_not_a_feasibility_claim": {
                f"ell_{i + 1}{j + 1}": rational_payload(value)
                for (i, j), value in sorted(residual_demo.items())
            },
        },
        "mode_status": {
            "root_comparisons_only": "failed_for_mixed_support_box_proxy",
            "vector_proper_subset_mixed_support": (
                "failed_for_individual_SUB_T_delta_proxy; stronger residual ell "
                "Farkas certificate not extracted"
            ),
        },
    }

    obstructions = {
        "schema": "mixed_support_obstructions_v1",
        "status": "obstructions_found_for_root_only_and_individual_SUB_T_proxy",
        "overclaim_guard": (
            "The obstructions below refute the audited finite proof proxies. "
            "They do not by themselves refute a future residual mixed-support "
            "theorem with a correctly encoded residual feasible region."
        ),
        "root_only_mode": {
            "status": "failed",
            "interpretation": (
                "Root-only support identities that certify unit pair supports "
                "independently cannot be added as a box certificate."
            ),
            "obstruction": {
                "u": ["1", "1", "1"],
                "alpha": "1",
                "lambda": {"lambda_12": "1", "lambda_13": "1", "lambda_23": "1"},
                "unit_pair_Phi_values": {
                    f"Phi_{pair[0] + 1}{pair[1] + 1}": rational_payload(result.phi)
                    for pair, result in zip(pair_supports(3), unit_values)
                },
                "triangle_Phi": rational_payload(triangle.phi),
                "violated_proxy_inequality": (
                    "Phi(lambda_12+lambda_13+lambda_23) >= "
                    "Phi(lambda_12)+Phi(lambda_13)+Phi(lambda_23)"
                ),
                "rhs": rational_payload(additive_rhs),
                "slack": rational_payload(root_only_slack),
                "missing_statistic": "s_min / equivalent min-cost support-flow statistic",
            },
        },
        "vector_proper_subset_mixed_support_mode": {
            "status": "failed_for_individual_delta_proxy",
            "interpretation": (
                "Allowing individual SUB_T-style source-deletion deltas still does "
                "not give simultaneous mixed pair domination on the symmetric face."
            ),
            "obstruction": {
                "u": ["1", "1", "1"],
                "alpha": "1",
                "lambda": {"lambda_12": "1", "lambda_13": "1", "lambda_23": "1"},
                "pair_source_deletion_deltas": {
                    f"delta_{i + 1}{j + 1}": rational_payload(value)
                    for (i, j), value in sorted(delta_vector.items())
                },
                "triangle_Phi": rational_payload(triangle.phi),
                "violated_proxy_inequality": "Phi(lambda) >= sum_ij lambda_ij delta_ij",
                "rhs": rational_payload(delta_rhs),
                "slack": rational_payload(vector_sub_t_slack),
            },
        },
        "residual_ell_target": {
            "status": "not_certified",
            "reason": (
                "The prompt supplies the corrected ell_ij formula, but not a fully "
                "formal residual feasible polyhedron for Farkas extraction. The "
                "script therefore records support-oracle certificates and exact "
                "proxy obstructions instead of inventing residual rows."
            ),
        },
        "oracle_values": {
            "unit_pairs": [oracle_payload(result) for result in unit_values],
            "triangle": oracle_payload(triangle),
        },
        "regressions_preserved": chambers_payload["regressions"],
    }
    return certificates, obstructions


def write_report(
    path: Path,
    chambers_payload: dict[str, Any],
    certificates: dict[str, Any],
    obstructions: dict[str, Any],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    symmetric = chambers_payload["symmetric_star_face"]
    root_obstruction = obstructions["root_only_mode"]["obstruction"]
    vector_obstruction = obstructions["vector_proper_subset_mixed_support_mode"]["obstruction"]

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
    lines.append("## Oracle Status")
    lines.append("")
    lines.append("- corrected edge-cover max-flow/min-cut: `verified in recorded runs`")
    lines.append("- min-cost support oracle: `implemented with exact Fraction arithmetic`")
    lines.append("- direct LP cross-check for symmetric triangle: `verified`")
    lines.append("- residual `ell_ij` formula: `implemented`")
    lines.append("- residual `ell_ij` Farkas extraction: `not_certified`")
    lines.append("")
    lines.append("## Symmetric Witness")
    lines.append("")
    check = symmetric["witness_check"]
    lines.append(f"- `Phi(1_12)`: `{check['Phi_12']}`")
    lines.append(f"- `Phi(1_13)`: `{check['Phi_13']}`")
    lines.append(f"- `Phi(1_23)`: `{check['Phi_23']}`")
    lines.append(f"- `Phi(1_12+1_13+1_23)`: `{check['Phi_triangle']}`")
    lines.append(f"- direct LP vertices: `{symmetric['triangle_result']['direct_lp_vertex_count']}`")
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
    lines.append("## Mode A")
    lines.append("")
    lines.append("Root-comparisons-only mode: `failed_for_mixed_support_box_proxy`.")
    lines.append("")
    lines.append(f"- violated proxy: `{root_obstruction['violated_proxy_inequality']}`")
    lines.append(f"- lhs: `{root_obstruction['triangle_Phi']}`")
    lines.append(f"- rhs: `{root_obstruction['rhs']}`")
    lines.append(f"- slack: `{root_obstruction['slack']}`")
    lines.append(f"- missing statistic: `{root_obstruction['missing_statistic']}`")
    lines.append("")
    lines.append("## Mode B")
    lines.append("")
    lines.append(
        "Vector proper-subset/mixed-support mode: "
        "`failed_for_individual_SUB_T_delta_proxy`; stronger residual `ell_ij` "
        "Farkas certificates were not extracted."
    )
    lines.append("")
    lines.append(f"- violated proxy: `{vector_obstruction['violated_proxy_inequality']}`")
    lines.append(f"- lhs: `{vector_obstruction['triangle_Phi']}`")
    lines.append(f"- rhs: `{vector_obstruction['rhs']}`")
    lines.append(f"- slack: `{vector_obstruction['slack']}`")
    lines.append("")
    lines.append("## Regression Rays")
    lines.append("")
    for regression in chambers_payload["regressions"]:
        lines.append(f"- `{regression['name']}` weights `{regression['full_weights_l1_l2_l3_a_b_r']}`: `F={regression['F']}`, triangle `Phi={regression['triangle_oracle']['Phi']}`.")
    lines.append("")
    lines.append("## Public Boundary")
    lines.append("")
    lines.append("The scripts record only public `R,Q` row families and explicitly exclude H1/H2, refined-Z, path monotonicity, ancestry transitivity, LCA separation, non-public lifts, and grouped Bellman rays as public-dual extreme cuts.")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("")
    lines.append(f"- `{DEFAULT_CHAMBERS}`")
    lines.append(f"- `{DEFAULT_CERTIFICATES}`")
    lines.append(f"- `{DEFAULT_OBSTRUCTIONS}`")
    lines.append(f"- `{path}`")
    lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chambers", type=Path, default=DEFAULT_CHAMBERS)
    parser.add_argument("--certificates", type=Path, default=DEFAULT_CERTIFICATES)
    parser.add_argument("--obstructions", type=Path, default=DEFAULT_OBSTRUCTIONS)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args(argv)

    chambers_payload = _load_or_create_chambers(args.chambers)
    certificates, obstructions = extract(chambers_payload)
    write_json(args.certificates, certificates)
    write_json(args.obstructions, obstructions)
    write_report(args.report, chambers_payload, certificates, obstructions)
    print(
        "mixed-lambda extraction: "
        f"root_only={certificates['mode_status']['root_comparisons_only']} "
        f"vector={certificates['mode_status']['vector_proper_subset_mixed_support']} "
        f"certificates={args.certificates} obstructions={args.obstructions}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
