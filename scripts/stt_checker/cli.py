"""Command-line interface for the STT checker scaffold."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .certificates import check_file, load_json
from .enumerate_stts import enumerate_stts, integer_optimum_by_enumeration
from .rationals import rational_to_string
from .topology import TreeTopology
from .certificates import _parse_weights


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m scripts.stt_checker.cli")
    parser.add_argument("--max-enumeration", type=int, default=100_000)
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check", help="check a JSON certificate")
    check_parser.add_argument("certificate")
    check_parser.add_argument(
        "--normalized-json",
        action="store_true",
        help="print the normalized certificate JSON after a successful check",
    )

    enum_parser = subparsers.add_parser(
        "enumerate", help="enumerate STTs for a certificate topology"
    )
    enum_parser.add_argument("certificate")
    enum_parser.add_argument("--depth-base", type=int, default=None)

    topo_parser = subparsers.add_parser(
        "enumerate-topology", help="enumerate STTs for a topology JSON object"
    )
    topo_parser.add_argument("topology")
    topo_parser.add_argument("--depth-base", type=int, default=1)

    args = parser.parse_args(argv)
    try:
        if args.command == "check":
            result = check_file(args.certificate, max_enumeration=args.max_enumeration)
            print(
                f"PASS {args.certificate}: weighted_cost="
                f"{rational_to_string(result.weighted_cost)}"
            )
            if args.normalized_json:
                print(result.normalized_json(), end="")
            return 0

        if args.command == "enumerate":
            data = load_json(args.certificate)
            topology = TreeTopology.from_dict(data["topology"])
            depth_base = args.depth_base
            if depth_base is None:
                depth_base = data.get("cost", {}).get("depth_base", 1)
            count = len(
                enumerate_stts(
                    topology, depth_base=depth_base, max_count=args.max_enumeration
                )
            )
            print(f"STT count: {count}")
            if "weights" in data:
                weights = _parse_weights(data["weights"], topology)
                optimum, _best_stt, opt_count = integer_optimum_by_enumeration(
                    topology,
                    weights,
                    depth_base=depth_base,
                    max_count=args.max_enumeration,
                )
                print(f"Integer optimum: {rational_to_string(optimum)}")
                print(f"Enumerated for optimum: {opt_count}")
            return 0

        if args.command == "enumerate-topology":
            with Path(args.topology).open("r", encoding="utf-8") as handle:
                raw = json.load(handle)
            topology_data = raw.get("topology", raw) if isinstance(raw, dict) else raw
            topology = TreeTopology.from_dict(topology_data)
            count = len(
                enumerate_stts(
                    topology,
                    depth_base=args.depth_base,
                    max_count=args.max_enumeration,
                )
            )
            print(f"STT count: {count}")
            return 0
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    parser.error("unreachable command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

