"""Extract corrected A_b(s) finite cut data for DS(k,1).

The extraction is intentionally small-k and exact-rational.  It reuses the
corrected source-deletion/Bellman machinery from
`check_proper_subset_contraction.py`, writes the requested JSON artifact, and
prints a compact status line suitable for shell runs.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.check_proper_subset_contraction import (
    DEFAULT_K3_JSON,
    DEFAULT_K4_JSON,
    run_k_audit,
    write_json,
)


def default_output(k: int) -> Path:
    if k == 3:
        return DEFAULT_K3_JSON
    if k == 4:
        return DEFAULT_K4_JSON
    return Path(f"data/proper_subset_contraction_k{k}.json")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--k", type=int, choices=(3, 4), default=3)
    parser.add_argument(
        "--bound",
        type=int,
        default=None,
        help="primitive integer coordinate bound; defaults to 3 for k=3 and 2 for k=4",
    )
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args(argv)

    bound = args.bound if args.bound is not None else (3 if args.k == 3 else 2)
    output = args.output if args.output is not None else default_output(args.k)
    payload = run_k_audit(args.k, bound)
    write_json(output, payload)
    counts = payload["counts"]
    print(
        "corrected A_b(s) extraction: "
        f"k={args.k} bound={bound} "
        f"b_root_rays={counts['b_root_bellman_optimal_rays']} "
        f"proper_subsets={counts['proper_nonsingleton_subsets']} "
        f"status={payload['status']} output={output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
