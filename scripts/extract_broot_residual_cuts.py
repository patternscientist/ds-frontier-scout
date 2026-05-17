"""Extract exact public-dual residual systems and b-root augmentation cuts.

For k=2 the script attempts full Fourier-Motzkin cut extraction.  For k=3 it
uses the same exact procedure but records an explicit fallback to exact
primal/dual matrices if projection exceeds the row limit.  No floating-point
claim is reported as exact.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
from typing import Any

from public_dual_dsk1_common import (
    add_scaled,
    augmentation_projected_cuts,
    build_broot_augmentation_lp,
    chamber_rows_for_depth,
    clean_linear,
    cone_membership_certificate,
    depth_cost,
    dsk1_tree_depth_vectors,
    format_linear,
    linear_to_json,
    matrix_json_from_lp,
    rational_to_string,
    residual_star_system_cases,
    star_depth_vectors,
)


def target_expr(k: int) -> dict[str, Fraction]:
    row = {"alpha": Fraction(1), "gamma": Fraction(1)}
    for i in range(1, k + 1):
        row[f"u{i}"] = Fraction(1)
    return row


def selected_broot_depth(k: int, star_depth: dict[str, int]) -> dict[str, int]:
    depths = {f"l{i}": star_depth[f"l{i}"] + 1 for i in range(1, k + 1)}
    depths["a"] = star_depth["a"] + 1
    depths["b"] = 0
    depths["r"] = 1
    return depths


def cut_domination_audit(k: int, extraction: dict[str, Any]) -> dict[str, Any]:
    if extraction["projection_status"] != "complete":
        return {
            "status": "not_attempted_projection_incomplete",
            "reason": extraction["projection_status"],
            "verified_cut_dominations": 0,
            "missing_cut_dominations": 0,
        }

    params = tuple([f"u{i}" for i in range(1, k + 1)] + ["alpha", "beta", "gamma"] + [f"s{i}" for i in range(1, k + 1)])
    tree_costs = [depth_cost(depths) for depths in dsk1_tree_depth_vectors(k)]
    star_depths = list(star_depth_vectors(k))
    residual_cases = extraction["star_residual_cases"]
    cuts = extraction["augmentation"]["cuts"]
    audits = []
    verified = 0
    missing = 0
    # Keep this intentionally bounded: it is a certificate audit for extracted
    # cuts, not an all-k theorem prover.
    for case_index, star_depth in enumerate(star_depths):
        if case_index >= len(residual_cases):
            continue
        residual_rows = [
            {key: Fraction(value) for key, value in row.items()}
            for row in residual_cases[case_index]["projected_residual_inequalities"]
        ]
        selected_cost = depth_cost(selected_broot_depth(k, star_depth))
        chamber_rows = chamber_rows_for_depth(
            selected_cost,
            tree_costs,
            tuple([f"u{i}" for i in range(1, k + 1)] + ["alpha", "beta", "gamma"]),
        )
        generators = residual_rows + chamber_rows
        case_audit = {
            "case_id": residual_cases[case_index]["case_id"],
            "star_depth": star_depth,
            "checked_cuts": [],
        }
        for cut_index, cut in enumerate(cuts):
            expr = {key: Fraction(value) for key, value in cut["expression"].items()}
            row = dict(target_expr(k))
            add_scaled(row, expr, Fraction(-1))
            row = clean_linear(row)
            cert = cone_membership_certificate(generators, row, params)
            if cert is None:
                missing += 1
                status = "missing_exact_domination_certificate"
            else:
                verified += 1
                status = "verified_by_exact_conic_certificate"
            case_audit["checked_cuts"].append(
                {
                    "cut_index": cut_index,
                    "classification": cut["classification"],
                    "target_minus_cut": linear_to_json(row),
                    "status": status,
                    "certificate": cert,
                }
            )
        audits.append(case_audit)
    return {
        "status": "complete_for_extracted_cuts" if missing == 0 else "incomplete_for_extracted_cuts",
        "verified_cut_dominations": verified,
        "missing_cut_dominations": missing,
        "cases": audits,
        "interpretation": (
            "A missing domination certificate is not by itself a counterexample "
            "to the residual-selection theorem; it is an obstruction to this "
            "strong per-cut domination proof attempt."
        ),
    }


def run(k: int, max_rows: int | None = None) -> dict[str, Any]:
    row_limit = max_rows or (200000 if k <= 2 else 120000)
    star_cases = residual_star_system_cases(k)
    augmentation = augmentation_projected_cuts(k, max_rows=row_limit)
    lp = build_broot_augmentation_lp(k)
    extraction = {
        "schema": "broot_residual_cuts_v0",
        "k": k,
        "public_only_constraint_boundary": (
            "Uses only R/Q variables, capping rows, frequency rows, and nonnegative "
            "variable domains. It does not use H1/H2/refined-Z/path-monotonicity/"
            "ancestry-transitivity/LCA-separation constraints."
        ),
        "star_residual_cases": list(star_cases),
        "augmentation": augmentation,
        "projection_status": augmentation["projection_status"],
        "exact_matrix_fallback": matrix_json_from_lp(lp),
    }
    extraction["residual_selection_audit"] = cut_domination_audit(k, extraction)
    return extraction


def write_report() -> None:
    paths = [Path("data/broot_residual_cuts_k2.json"), Path("data/broot_residual_cuts_k3.json")]
    loaded = []
    for path in paths:
        if path.exists():
            loaded.append(json.loads(path.read_text(encoding="utf-8")))
    lines = [
        "# b-root Residual Cut Extraction Report",
        "",
        "## 1. Summary verdict",
        "",
    ]
    if not loaded:
        lines.append("No k=2 or k=3 extraction JSON is present yet.")
    else:
        for data in loaded:
            cuts = data["augmentation"]["cuts"]
            genuine = [
                cut for cut in cuts if cut["classification"] == "genuine subset-level"
            ]
            lines.append(
                f"- k={data['k']}: projection `{data['projection_status']}`, "
                f"cuts `{len(cuts)}`, genuine subset-level cuts `{len(genuine)}`, "
                f"residual-selection audit `{data['residual_selection_audit']['status']}`."
            )
    lines.extend(
        [
            "",
            "## 2. Exact commands run and outputs",
            "",
            "- `python scripts/check_ds11_broot_envelope.py` writes `data/ds11_broot_envelope_audit.json` and `reports/ds11_broot_envelope_audit.md`.",
            "- `python scripts/generate_public_dual_dsk1.py --k 1 --self-test` writes `data/public_dual_dsk1_k1.json`.",
            "- `python scripts/extract_broot_residual_cuts.py --k 2` writes `data/broot_residual_cuts_k2.json`.",
            "- `python scripts/extract_broot_residual_cuts.py --k 3` writes `data/broot_residual_cuts_k3.json`.",
            "",
            "## 3. DS(1,1) envelope hardening result",
            "",
        ]
    )
    ds11 = Path("data/ds11_broot_envelope_audit.json")
    if ds11.exists():
        audit = json.loads(ds11.read_text(encoding="utf-8"))
        lines.append(
            f"Reconstructed-envelope verdict: `{audit['verified']}`; "
            f"source 12-envelope certificate loaded: "
            f"`{audit['source_certificate_status']['named_12_envelope_certificate_loaded']}`."
        )
    else:
        lines.append("DS(1,1) audit has not been run yet.")
    lines.extend(
        [
            "",
            "## 4. Public-dual model generator audit",
            "",
        ]
    )
    model_path = Path("data/public_dual_dsk1_k1.json")
    if model_path.exists():
        model = json.loads(model_path.read_text(encoding="utf-8"))
        lines.append(
            f"DS(1,1) model counts: `{model['constraint_counts']}`; "
            f"self-test passed: `{model.get('self_test', {}).get('passed')}`."
        )
        for extra_k in (2, 3):
            extra_path = Path("data") / f"public_dual_dsk1_k{extra_k}.json"
            if extra_path.exists():
                extra = json.loads(extra_path.read_text(encoding="utf-8"))
                lines.append(
                    f"DS({extra_k},1) model counts: `{extra['constraint_counts']}`; "
                    f"variables `{len(extra['variables']['R']) + len(extra['variables']['Q'])}`."
                )
    else:
        lines.append("Public-dual generator self-test has not been run yet.")
    for data in loaded:
        k = data["k"]
        lines.extend(
            [
                "",
                f"## {5 if k == 2 else 6}. k={k} residual-cut families",
                "",
                f"- Star residual cases: `{len(data['star_residual_cases'])}`.",
                f"- Augmentation projection status: `{data['projection_status']}`.",
                f"- Extracted cuts: `{len(data['augmentation']['cuts'])}`.",
            ]
        )
        counts: dict[str, int] = {}
        for cut in data["augmentation"]["cuts"]:
            counts[cut["classification"]] = counts.get(cut["classification"], 0) + 1
        lines.append(f"- Classification counts: `{dict(sorted(counts.items()))}`.")
        for cut in data["augmentation"]["cuts"][:20]:
            lines.append(
                f"  - `{cut['classification']}`: `{cut['inequality']}`"
            )
        if len(data["augmentation"]["cuts"]) > 20:
            lines.append("  - additional cuts are in the JSON artifact.")
    lines.extend(
        [
            "",
            "## 7. First genuine subset-level obstruction/cut family",
            "",
        ]
    )
    first_genuine = None
    for data in loaded:
        for cut in data["augmentation"]["cuts"]:
            if cut["classification"] == "genuine subset-level":
                first_genuine = (data["k"], cut)
                break
        if first_genuine:
            break
    if first_genuine:
        lines.append(
            f"First extracted genuine subset-level cut appears at k={first_genuine[0]}: "
            f"`{first_genuine[1]['inequality']}`."
        )
    else:
        lines.append("No genuine subset-level residual cut was extracted for the completed k<=3 projections.")
    lines.extend(
        [
            "",
            "## 8. Exact certificate/counterexample artifacts produced",
            "",
            "- `data/ds11_broot_envelope_audit.json`",
            "- `data/public_dual_dsk1_k1.json`",
            "- `data/broot_residual_cuts_k2.json`",
            "- `data/broot_residual_cuts_k3.json`",
            "- exact matrix fallback sections inside each `broot_residual_cuts_k*.json`",
            "",
            "## 9. Recommended next manual proof prompt",
            "",
            "Use the first non-singleton extracted cut, or the exact matrix fallback if k=3 projection aborted, as the next manual proof target. Prove or refute that the cut is dominated on every b-root Bellman chamber by the projected public-dual star residual system. Treat missing per-cut domination certificates as proof obligations, not theorem counterexamples.",
            "",
            "## 10. Explicit overclaim checklist",
            "",
            "- Does not claim public LP exactness on DS(k,1).",
            "- Does not claim the b-root residual-selection theorem for arbitrary k.",
            "- Does not treat k=2,3 evidence as an all-k theorem.",
            "- Does not use H1/H2/refined-Z/path-monotonicity/ancestry-transitivity/LCA-separation constraints.",
            "- Does not present floating-point output as exact.",
            "",
        ]
    )
    report = Path("reports/broot_residual_cut_extraction_report.md")
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, required=True, choices=(2, 3))
    parser.add_argument("--max-rows", type=int, default=None)
    args = parser.parse_args()
    data = run(args.k, args.max_rows)
    output = Path("data") / f"broot_residual_cuts_k{args.k}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_report()
    print(f"wrote {output}")
    print("projection:", data["projection_status"])
    print("cuts:", len(data["augmentation"]["cuts"]))
    print("residual-selection audit:", data["residual_selection_audit"]["status"])


if __name__ == "__main__":
    main()
