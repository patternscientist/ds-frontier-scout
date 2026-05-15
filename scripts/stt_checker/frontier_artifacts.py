"""Build the reproducible STT v0 frontier artifact.

This script summarizes exact combinatorial data produced by the v0 checker.
It intentionally does not implement or test any LP feasibility constraints.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from .enumerate_stts import EnumerationLimitExceeded, integer_optimum_by_enumeration
from .rationals import rational_to_string
from .topology import TreeTopology
from .topology_generation import DEFAULT_MAX_N, generate_unlabeled_tree_topologies


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = REPO_ROOT / "data" / "stt_frontier"
DEFAULT_REPORT_PATH = REPO_ROOT / "reports" / "stt_v0_frontier_artifact.md"


@dataclass(frozen=True)
class ArtifactPaths:
    json_path: Path
    csv_path: Path
    report_path: Path


def build_frontier_artifact(
    max_n: int = DEFAULT_MAX_N,
    max_enumeration: int = 100_000,
    data_dir: Path = DEFAULT_DATA_DIR,
    report_path: Path = DEFAULT_REPORT_PATH,
) -> ArtifactPaths:
    """Generate frontier JSON, CSV, and Markdown report files."""

    if max_n <= 0:
        raise ValueError("max_n must be positive")
    if max_n > DEFAULT_MAX_N:
        raise ValueError(f"max_n above {DEFAULT_MAX_N} is intentionally unsupported")
    if max_enumeration <= 0:
        raise ValueError("max_enumeration must be positive")

    data_dir.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    records = [
        _record_for_topology(item["topology"], item["canonical_form"], max_enumeration)
        for item in generate_unlabeled_tree_topologies(max_n)
    ]

    json_path = data_dir / f"topologies_n_leq_{max_n}.json"
    csv_path = data_dir / f"topology_summary_n_leq_{max_n}.csv"
    payload = {
        "schema_version": "stt-frontier-artifact-v0",
        "max_n": max_n,
        "max_enumeration": max_enumeration,
        "lp_feasibility_checked": False,
        "lp_note": "No Golinsky LP constraints are implemented or checked in this artifact.",
        "topologies": records,
    }
    json_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    _write_csv(csv_path, records)
    report_path.write_text(
        _render_report(records, max_n, max_enumeration), encoding="utf-8"
    )
    return ArtifactPaths(json_path=json_path, csv_path=csv_path, report_path=report_path)


def _record_for_topology(
    topology: TreeTopology, canonical_form: str, max_enumeration: int
) -> dict[str, Any]:
    degree_sequence = sorted(topology.degrees.values(), reverse=True)
    labels = sorted(topology.derived_subclass_labels())
    uniform_weights = {v: Fraction(1, topology.n) for v in topology.vertices}
    leaf_vertices = [
        v for v in topology.vertices if topology.degrees[v] <= 1 or topology.n == 1
    ]
    leaf_weight = Fraction(1, len(leaf_vertices))
    leaf_heavy_weights = {
        v: leaf_weight if v in leaf_vertices else Fraction(0, 1)
        for v in topology.vertices
    }

    enumeration: dict[str, Any] = {
        "max_enumeration": max_enumeration,
        "completed": False,
        "stt_count": None,
        "exceeded_cap": False,
    }
    uniform: dict[str, Any] = {"normalization": "sum_1", "optimum": None}
    leaf_heavy: dict[str, Any] = {
        "normalization": "sum_1",
        "support": leaf_vertices,
        "weights": {str(v): rational_to_string(leaf_heavy_weights[v]) for v in topology.vertices},
        "optimum": None,
    }

    try:
        uniform_optimum, _uniform_best, stt_count = integer_optimum_by_enumeration(
            topology, uniform_weights, max_count=max_enumeration
        )
        leaf_optimum, _leaf_best, leaf_count = integer_optimum_by_enumeration(
            topology, leaf_heavy_weights, max_count=max_enumeration
        )
        if leaf_count != stt_count:
            raise ValueError("internal error: repeated enumeration counts differ")
        enumeration.update({"completed": True, "stt_count": stt_count})
        uniform["optimum"] = rational_to_string(uniform_optimum)
        leaf_heavy["optimum"] = rational_to_string(leaf_optimum)
    except EnumerationLimitExceeded as exc:
        enumeration.update({"exceeded_cap": True, "message": str(exc)})

    return {
        "n": topology.n,
        "canonical_form": canonical_form,
        "canonical_id": f"n{topology.n}:{canonical_form}",
        "vertices": list(topology.vertices),
        "edges": [list(edge) for edge in topology.edges],
        "degree_sequence": degree_sequence,
        "derived_labels": labels,
        "edge_diameter": topology.diameter_edges,
        "edge_diameter_at_most_3": topology.diameter_edges <= 3,
        "edge_diameter_equals_3": topology.diameter_edges == 3,
        "enumeration": enumeration,
        "uniform_weights": {
            "normalization": "sum_1",
            "weights": {str(v): rational_to_string(uniform_weights[v]) for v in topology.vertices},
            "optimum": uniform["optimum"],
        },
        "leaf_heavy_weights": leaf_heavy,
    }


def _write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    fieldnames = [
        "n",
        "canonical_form",
        "edges",
        "degree_sequence",
        "derived_labels",
        "edge_diameter",
        "stt_count",
        "enumeration_completed",
        "uniform_optimum",
        "leaf_heavy_optimum",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(
                {
                    "n": record["n"],
                    "canonical_form": record["canonical_form"],
                    "edges": json.dumps(record["edges"], separators=(",", ":")),
                    "degree_sequence": " ".join(map(str, record["degree_sequence"])),
                    "derived_labels": " ".join(record["derived_labels"]),
                    "edge_diameter": record["edge_diameter"],
                    "stt_count": record["enumeration"]["stt_count"],
                    "enumeration_completed": record["enumeration"]["completed"],
                    "uniform_optimum": record["uniform_weights"]["optimum"],
                    "leaf_heavy_optimum": record["leaf_heavy_weights"]["optimum"],
                }
            )


def _render_report(
    records: list[dict[str, Any]], max_n: int, max_enumeration: int
) -> str:
    shapes_by_n = Counter(record["n"] for record in records)
    diameters_by_n: dict[int, Counter[int]] = defaultdict(Counter)
    for record in records:
        diameters_by_n[record["n"]][record["edge_diameter"]] += 1

    ed3_records = [record for record in records if record["edge_diameter"] == 3]
    edge_leq3 = sum(1 for record in records if record["edge_diameter"] <= 3)
    enumerated = sum(1 for record in records if record["enumeration"]["completed"])
    capped = len(records) - enumerated

    lines: list[str] = []
    lines.extend(
        [
            "# STT v0 Frontier Artifact",
            "",
            f"Generated for unlabeled tree topologies with `n <= {max_n}`.",
            "",
            "## Purpose And Scope",
            "",
            "This artifact is a reproducible small-instance summary for the exact "
            "combinatorial STT checker scaffold v0. It generates tree topologies, "
            "deduplicates them up to isomorphism, derives checker-supported labels, "
            "enumerates valid recursive STTs when below the configured cap, and "
            "computes exact integer optima for simple rational vertex-frequency "
            "objectives.",
            "",
            "**No LP feasibility is checked here.** This artifact does not implement, "
            "guess, or validate Golinsky LP constraints, LP variable domains, root "
            "rounding, or integrality-gap claims.",
            "",
            "## Method",
            "",
            "- Labeled trees are generated from Prufer codes on vertices `0..n-1`.",
            "- Isomorphic duplicates are removed using an AHU-style canonical string: "
            "find the tree center or centers, compute sorted rooted subtree strings, "
            "and keep the lexicographically smallest center-rooted form.",
            "- Derived labels use the existing checker: `path`, `star`, and exact "
            "`edge-diameter-k` under the line-graph edge-distance convention.",
            f"- Complete STT enumeration uses the checker cap `{max_enumeration}`. "
            "If a topology exceeds that cap, the record says so instead of failing "
            "the artifact build.",
            "",
            "## Output Files",
            "",
            f"- `data/stt_frontier/topologies_n_leq_{max_n}.json`",
            f"- `data/stt_frontier/topology_summary_n_leq_{max_n}.csv`",
            "- `reports/stt_v0_frontier_artifact.md`",
            "",
            "## Unlabeled Tree Shapes By n",
            "",
            "| n | shapes |",
            "|---:|---:|",
        ]
    )
    for n in range(1, max_n + 1):
        lines.append(f"| {n} | {shapes_by_n[n]} |")

    all_diameters = sorted({record["edge_diameter"] for record in records})
    header = "| n | " + " | ".join(f"edge-diameter-{d}" for d in all_diameters) + " |"
    separator = "|---:|" + "|".join("---:" for _ in all_diameters) + "|"
    lines.extend(
        [
            "",
            "## Edge-Diameter Class Counts By n",
            "",
            header,
            separator,
        ]
    )
    for n in range(1, max_n + 1):
        row = [str(diameters_by_n[n][diameter]) for diameter in all_diameters]
        lines.append(f"| {n} | " + " | ".join(row) + " |")

    lines.extend(
        [
            "",
            "## Edge-Diameter-3 Topologies",
            "",
            "| n | degree sequence | edges | STT count | uniform optimum |",
            "|---:|---|---|---:|---:|",
        ]
    )
    for record in ed3_records:
        stt_count = record["enumeration"]["stt_count"]
        count_text = str(stt_count) if stt_count is not None else "exceeded cap"
        lines.append(
            "| {n} | {degrees} | `{edges}` | {count} | {optimum} |".format(
                n=record["n"],
                degrees=" ".join(map(str, record["degree_sequence"])),
                edges=json.dumps(record["edges"], separators=(",", ":")),
                count=count_text,
                optimum=record["uniform_weights"]["optimum"] or "not enumerated",
            )
        )

    lines.extend(
        [
            "",
            "## Checker-Only Observations",
            "",
            f"- The generator found `{len(records)}` unlabeled tree shapes for "
            f"`n <= {max_n}`.",
            f"- `{edge_leq3}` of these shapes have checker-derived edge diameter at "
            "most 3.",
            f"- `{len(ed3_records)}` shapes have checker-derived edge diameter exactly 3.",
            f"- Complete STT enumeration finished for `{enumerated}` shapes and exceeded "
            f"the configured cap for `{capped}` shapes.",
            "- Uniform and leaf-heavy objective values in the machine-readable files "
            "are exact integer optima only when `enumeration.completed` is true.",
            "",
            "These observations are only statements about the exact checker output. "
            "They do not imply any LP integrality, LP feasibility, or theorem-level "
            "claim.",
            "",
            "## Next Targets For The LP Phase",
            "",
            "- Specify a versioned machine-readable Golinsky STT LP constraint set.",
            "- Define exact variable domains and absent-variable defaults for all LP "
            "variable families.",
            "- Add exact LP feasibility checking only after the constraint set is fixed.",
            "- Compare future LP depth projections against the enumerated STT depth "
            "vectors for the edge-diameter-3 records listed above.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m scripts.stt_checker.frontier_artifacts"
    )
    parser.add_argument("--max-n", type=int, default=DEFAULT_MAX_N)
    parser.add_argument("--max-enumeration", type=int, default=100_000)
    args = parser.parse_args(argv)
    paths = build_frontier_artifact(
        max_n=args.max_n,
        max_enumeration=args.max_enumeration,
    )
    print(f"Wrote {paths.json_path}")
    print(f"Wrote {paths.csv_path}")
    print(f"Wrote {paths.report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
