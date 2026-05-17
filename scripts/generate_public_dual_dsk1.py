"""Generate the public SKZ-dual model for DS(k,1).

The generator emits only R/Q variables plus public capping and frequency rows.
It deliberately excludes H1/H2/refined-Z/path-monotonicity/ancestry
transitivity/LCA-separation constraints.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from public_dual_dsk1_common import generate_public_dual_dsk1


EXPECTED_DS11 = {
    "r_variables": {
        "R[l1,a]",
        "R[l1,b]",
        "R[l1,r]",
        "R[a,b]",
        "R[a,r]",
        "R[b,r]",
    },
    "q_variables": {
        "Q[a,b,r]",
        "Q[b,a,l1]",
        "Q[l1,a,b]",
        "Q[l1,a,r]",
        "Q[l1,b,r]",
        "Q[r,a,l1]",
        "Q[r,b,a]",
        "Q[r,b,l1]",
    },
    "counts": {"capping": 4, "frequency": 12},
    "capping_names": {
        "cap:R[l1,b]@a",
        "cap:R[l1,r]@a",
        "cap:R[l1,r]@b",
        "cap:R[a,r]@b",
    },
    "frequency_names": {
        "freq:l1|a",
        "freq:l1|b",
        "freq:l1|r",
        "freq:a|l1",
        "freq:a|b",
        "freq:a|r",
        "freq:b|l1",
        "freq:b|a",
        "freq:b|r",
        "freq:r|l1",
        "freq:r|a",
        "freq:r|b",
    },
}


def run_self_test() -> dict[str, object]:
    model = generate_public_dual_dsk1(1)
    counts = model.to_json()["constraint_counts"]
    capping_names = {
        constraint.name for constraint in model.constraints if constraint.family == "capping"
    }
    frequency_names = {
        constraint.name for constraint in model.constraints if constraint.family == "frequency"
    }
    checks = {
        "r_variables_match_embedded_ds11_witness_shape": set(model.r_variables)
        == EXPECTED_DS11["r_variables"],
        "q_variables_match_embedded_ds11_witness_shape": set(model.q_variables)
        == EXPECTED_DS11["q_variables"],
        "constraint_counts_match_embedded_ds11_witness_shape": counts
        == EXPECTED_DS11["counts"],
        "capping_names_match_embedded_ds11_witness_shape": capping_names
        == EXPECTED_DS11["capping_names"],
        "frequency_names_match_embedded_ds11_witness_shape": frequency_names
        == EXPECTED_DS11["frequency_names"],
        "external_check_ds11_public_dual_witness_py_present": Path(
            "check_ds11_public_dual_witness.py"
        ).exists()
        or Path("scripts/check_ds11_public_dual_witness.py").exists(),
    }
    return {
        "self_test_schema": "public_dual_dsk1_self_test_v0",
        "passed": all(value for key, value in checks.items() if not key.startswith("external_")),
        "checks": checks,
        "note": (
            "The external witness checker named in the handoff is absent in this "
            "checkout, so the self-test compares against the embedded DS(1,1) "
            "public R/Q row shape."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, required=True)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional JSON output path. Defaults to data/public_dual_dsk1_k{k}.json.",
    )
    args = parser.parse_args()

    model = generate_public_dual_dsk1(args.k)
    payload = model.to_json()
    if args.self_test:
        payload["self_test"] = run_self_test()
        if not payload["self_test"]["passed"]:
            raise SystemExit(json.dumps(payload["self_test"], indent=2, sort_keys=True))

    output = args.output or Path("data") / f"public_dual_dsk1_k{args.k}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"wrote {output}")
    print(
        "counts:",
        json.dumps(payload["constraint_counts"], sort_keys=True),
        "variables:",
        len(model.variables),
    )
    if args.self_test:
        print("self-test: passed")


if __name__ == "__main__":
    main()
