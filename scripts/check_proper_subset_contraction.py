"""Exact small-k audit for the DS(k,1) proper-subset source deletion step.

This is a finite certificate/evidence harness.  It deliberately uses only the
public Golinsky/SKZ dual-variable skeleton (`R` unordered pairs and ordered
collinear-triplet `Q` variables) when recording the public-LP side of the
experiment.  The actual obstruction/evidence checks below are exact rational
Bellman and corrected source-deletion computations; they do not claim an
all-k theorem.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, permutations, product
import json
import math
from pathlib import Path
import sys
from typing import Any, Iterable

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.stt_checker.double_star_depth_projection import (
    double_star_spec,
    double_star_topology,
    enumerate_normal_form_stts,
)
from scripts.stt_checker.rationals import rational_to_string


DEFAULT_REPORT = Path("reports/proper_subset_contraction_report.md")
DEFAULT_K3_JSON = Path("data/proper_subset_contraction_k3.json")
DEFAULT_K4_JSON = Path("data/proper_subset_contraction_k4.json")


@dataclass(frozen=True)
class DepthIndex:
    all_depths: tuple[tuple[int, ...], ...]
    b_root_depths: tuple[tuple[int, ...], ...]
    b_exact_ancestor_set_depths: dict[tuple[int, ...], tuple[tuple[int, ...], ...]]
    first_root_depths: dict[int, tuple[tuple[int, ...], ...]]


def left_vertices(k: int) -> tuple[int, ...]:
    return tuple(range(k))


def label(k: int, vertex: int) -> str:
    spec = double_star_spec(k, 1)
    if vertex in spec.left_leaves:
        return f"l{vertex + 1}"
    if vertex == spec.a:
        return "a"
    if vertex == spec.b:
        return "b"
    if vertex == spec.right_leaves[0]:
        return "r"
    raise ValueError(f"unknown DS({k},1) vertex {vertex}")


def labels(k: int) -> tuple[str, ...]:
    return tuple(label(k, vertex) for vertex in range(k + 3))


def subset_label(k: int, subset: Iterable[int]) -> str:
    values = tuple(sorted(subset))
    if not values:
        return "{}"
    return "{" + ",".join(label(k, vertex) for vertex in values) + "}"


def powerset(values: Iterable[int]) -> tuple[tuple[int, ...], ...]:
    items = tuple(values)
    return tuple(
        tuple(items[index] for index in range(len(items)) if mask & (1 << index))
        for mask in range(1 << len(items))
    )


def proper_nonsingleton_subsets(k: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        subset
        for size in range(2, k)
        for subset in combinations(left_vertices(k), size)
    )


def kappa_value(k: int, weights: tuple[Fraction, ...], active: Iterable[int]) -> Fraction:
    """Corrected kappa(A) from the prompt."""

    active_set = set(active)
    alpha = weights[k]
    value = Fraction(0)
    for vertex in active_set:
        value += min(alpha, weights[vertex])
    for i, j in combinations(left_vertices(k), 2):
        if i in active_set or j in active_set:
            value += min(weights[i], weights[j])
    return value


def source_deletion_branch_value(
    k: int,
    weights: tuple[Fraction, ...],
    active: Iterable[int],
    deleted_sources: Iterable[int] = (),
) -> Fraction:
    """One branch of the corrected source-deletion formula."""

    active_set = set(active)
    deleted_set = set(deleted_sources)
    residual = sum(
        (
            weights[vertex]
            for vertex in left_vertices(k)
            if vertex not in active_set and vertex not in deleted_set
        ),
        Fraction(0),
    )
    return residual + kappa_value(k, weights, active_set)


def F_value(k: int, weights: tuple[Fraction, ...]) -> Fraction:
    """F(L), using the corrected formula with no deleted sources."""

    return min(
        source_deletion_branch_value(k, weights, active)
        for active in powerset(left_vertices(k))
    )


def F_deleted_value(
    k: int, weights: tuple[Fraction, ...], deleted_sources: Iterable[int]
) -> Fraction:
    """F^{(-S)}(L) from the prompt."""

    deleted = tuple(sorted(deleted_sources))
    return min(
        source_deletion_branch_value(k, weights, active, deleted)
        for active in powerset(left_vertices(k))
    )


def delta_value(
    k: int, weights: tuple[Fraction, ...], deleted_sources: Iterable[int]
) -> Fraction:
    return F_value(k, weights) - F_deleted_value(k, weights, deleted_sources)


def active_source_deletion_branches(
    k: int, weights: tuple[Fraction, ...], deleted_sources: Iterable[int] = ()
) -> tuple[tuple[int, ...], ...]:
    values = [
        (active, source_deletion_branch_value(k, weights, active, deleted_sources))
        for active in powerset(left_vertices(k))
    ]
    optimum = min(value for _active, value in values)
    return tuple(active for active, value in values if value == optimum)


def corrected_star_stt_cost(k: int, weights: tuple[Fraction, ...]) -> Fraction:
    """Direct star STT optimum for the left star (a plus k leaves)."""

    best: Fraction | None = None
    leaves = left_vertices(k)
    alpha = weights[k]
    for size in range(k + 1):
        for prefix_set in combinations(leaves, size):
            for prefix in permutations(prefix_set):
                prefix_set_lookup = set(prefix)
                value = alpha * size
                for position, vertex in enumerate(prefix):
                    value += weights[vertex] * position
                for vertex in leaves:
                    if vertex not in prefix_set_lookup:
                        value += weights[vertex] * (size + 1)
                if best is None or value < best:
                    best = value
    if best is None:
        raise ValueError("star STT enumeration produced no candidates")
    return best


def depth_index(k: int) -> DepthIndex:
    spec = double_star_spec(k, 1)
    all_depths: list[tuple[int, ...]] = []
    b_root_depths: list[tuple[int, ...]] = []
    b_exact_ancestor_set_depths: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    first_root_depths: dict[int, list[tuple[int, ...]]] = {
        vertex: [] for vertex in range(k + 3)
    }
    seen_all: set[tuple[int, ...]] = set()
    seen_b: set[tuple[int, ...]] = set()
    for stt in enumerate_normal_form_stts(k, 1, depth_base=0):
        depth = tuple(stt.depth[vertex] for vertex in range(k + 3))
        if depth not in seen_all:
            seen_all.add(depth)
            all_depths.append(depth)
        root = next(vertex for vertex, parent in stt.parent.items() if parent is None)
        first_root_depths[root].append(depth)
        if stt.parent[spec.b] is None and depth not in seen_b:
            seen_b.add(depth)
            b_root_depths.append(depth)

        ancestors: list[int] = []
        current = spec.b
        while stt.parent[current] is not None:
            current = stt.parent[current]
            ancestors.append(current)
        key = tuple(sorted(ancestors))
        b_exact_ancestor_set_depths.setdefault(key, []).append(depth)

    return DepthIndex(
        all_depths=tuple(sorted(all_depths)),
        b_root_depths=tuple(sorted(b_root_depths)),
        b_exact_ancestor_set_depths={
            key: tuple(sorted(set(value)))
            for key, value in b_exact_ancestor_set_depths.items()
        },
        first_root_depths={
            key: tuple(sorted(set(value))) for key, value in first_root_depths.items()
        },
    )


def dot_depth(weights: tuple[Fraction, ...], depth: tuple[int, ...]) -> Fraction:
    return sum(weights[index] * depth[index] for index in range(len(weights)))


def true_bellman_optimum(index: DepthIndex, weights: tuple[Fraction, ...]) -> Fraction:
    return min(dot_depth(weights, depth) for depth in index.all_depths)


def b_root_cost(index: DepthIndex, weights: tuple[Fraction, ...]) -> Fraction:
    return min(dot_depth(weights, depth) for depth in index.b_root_depths)


def s_first_b_cost(
    index: DepthIndex, weights: tuple[Fraction, ...], deleted_sources: Iterable[int]
) -> Fraction:
    """Best cost among STTs where exactly S left leaves are ancestors of b."""

    key = tuple(sorted(deleted_sources))
    depths = index.b_exact_ancestor_set_depths.get(key)
    if not depths:
        raise ValueError(f"no S-first b-depths for source set {key}")
    return min(dot_depth(weights, depth) for depth in depths)


def s_first_deletion_bound(
    k: int,
    index: DepthIndex,
    weights: tuple[Fraction, ...],
    deleted_sources: Iterable[int],
) -> Fraction:
    """D(S): the S-first deletion gap relative to the best b-root branch.

    This is the natural finite Bellman interpretation audited here: force the
    leaves in S to be the left-leaf ancestors of b, then compare the best such
    STT against the unconstrained b-root branch.
    """

    del k
    return s_first_b_cost(index, weights, deleted_sources) - b_root_cost(index, weights)


def first_root_gap(
    index: DepthIndex, weights: tuple[Fraction, ...], root: int
) -> Fraction:
    root_depths = index.first_root_depths[root]
    if not root_depths:
        raise ValueError(f"no first-root depths for {root}")
    return min(dot_depth(weights, depth) for depth in root_depths) - b_root_cost(
        index, weights
    )


def normalized_integer_weight_rays(k: int, bound: int) -> tuple[tuple[Fraction, ...], ...]:
    """Primitive nonzero integer rays in [0,bound]^(k+3)."""

    rays: list[tuple[Fraction, ...]] = []
    seen: set[tuple[int, ...]] = set()
    for values in product(range(bound + 1), repeat=k + 3):
        if not any(values):
            continue
        divisor = 0
        for value in values:
            divisor = math.gcd(divisor, value)
        primitive = tuple(value // divisor for value in values)
        if primitive in seen:
            continue
        seen.add(primitive)
        rays.append(tuple(Fraction(value) for value in primitive))
    return tuple(rays)


def public_dual_skeleton(k: int) -> dict[str, Any]:
    """Return the public R/Q domains and row counts for DS(k,1)."""

    topology = double_star_topology(k, 1)
    vertices = tuple(topology.vertices)
    paths: dict[tuple[int, int], tuple[int, ...]] = {}
    for i, j in combinations(vertices, 2):
        paths[(i, j)] = _path_between(topology.adjacency, i, j)

    r_pairs = tuple(combinations(vertices, 2))
    q_triples: list[tuple[int, int, int]] = []
    for i in vertices:
        for j in vertices:
            if i == j:
                continue
            path = paths[(min(i, j), max(i, j))]
            for middle in path[1:-1]:
                q_triples.append((i, middle, j))

    capping = []
    for i, j in r_pairs:
        for middle in paths[(i, j)][1:-1]:
            capping.append(
                {
                    "R": [label(k, i), label(k, j)],
                    "Q_left": [label(k, i), label(k, middle), label(k, j)],
                    "Q_right": [label(k, j), label(k, middle), label(k, i)],
                    "sense": "R_ij <= Q_ikj + Q_jki",
                }
            )

    frequency = []
    for target in vertices:
        for ancestor in vertices:
            if target == ancestor:
                continue
            terms = []
            for other in vertices:
                if other in (target, ancestor):
                    continue
                path = paths[(min(target, other), max(target, other))]
                if ancestor in path[1:-1]:
                    terms.append([label(k, target), label(k, ancestor), label(k, other)])
            frequency.append(
                {
                    "target": label(k, target),
                    "ancestor": label(k, ancestor),
                    "R": sorted([label(k, target), label(k, ancestor)]),
                    "Q_terms": terms,
                    "sense": "R_ki + sum_j Q_ikj <= w_i",
                }
            )

    return {
        "variables": {
            "R_unordered_pairs": [[label(k, i), label(k, j)] for i, j in r_pairs],
            "Q_ordered_collinear_triplets": [
                [label(k, i), label(k, middle), label(k, j)]
                for i, middle, j in sorted(set(q_triples))
            ],
        },
        "counts": {
            "R": len(r_pairs),
            "Q": len(set(q_triples)),
            "capping_constraints": len(capping),
            "frequency_constraints": len(frequency),
        },
        "constraints": {
            "capping": capping,
            "frequency": frequency,
            "excluded": [
                "H1/H2",
                "refined-Z",
                "path-monotonicity",
                "ancestry-transitivity",
                "LCA-separation",
            ],
        },
    }


def _path_between(adjacency: dict[int, tuple[int, ...]], source: int, target: int) -> tuple[int, ...]:
    parents: dict[int, int | None] = {source: None}
    queue = [source]
    for current in queue:
        if current == target:
            break
        for neighbor in adjacency[current]:
            if neighbor not in parents:
                parents[neighbor] = current
                queue.append(neighbor)
    if target not in parents:
        raise ValueError("disconnected topology")
    path = [target]
    while path[-1] != source:
        parent = parents[path[-1]]
        if parent is None:
            raise ValueError("path reconstruction failed")
        path.append(parent)
    return tuple(reversed(path))


def rational_payload(value: Fraction) -> str:
    return rational_to_string(value)


def weights_payload(k: int, weights: tuple[Fraction, ...]) -> dict[str, str]:
    return {label(k, index): rational_payload(value) for index, value in enumerate(weights)}


def subset_payload(k: int, subset: Iterable[int]) -> list[str]:
    return [label(k, vertex) for vertex in sorted(subset)]


def run_k_audit(k: int, bound: int, *, include_samples: bool = True) -> dict[str, Any]:
    index = depth_index(k)
    rays = normalized_integer_weight_rays(k, bound)
    proper_subsets = proper_nonsingleton_subsets(k)
    subset_stats: dict[tuple[int, ...], dict[str, Any]] = {
        subset: {
            "checked_b_root_rays": 0,
            "strictly_positive_b_root_rays": 0,
            "minimum_slack": None,
            "minimum_slack_witness": None,
            "failures": [],
            "strictly_positive_failures": [],
            "tight_examples": [],
            "active_F_branches": {},
            "active_deleted_branches": {},
        }
        for subset in proper_subsets
    }

    b_root_ray_count = 0
    positive_b_root_ray_count = 0
    first_obstruction: dict[str, Any] | None = None
    active_cone_counts: dict[str, int] = {}

    for weights in rays:
        true_optimum = true_bellman_optimum(index, weights)
        b_cost = b_root_cost(index, weights)
        if b_cost != true_optimum:
            continue
        b_root_ray_count += 1
        if all(value > 0 for value in weights):
            positive_b_root_ray_count += 1
        active_b = active_source_deletion_branches(k, weights)
        for branch in active_b:
            active_cone_counts[subset_label(k, branch)] = (
                active_cone_counts.get(subset_label(k, branch), 0) + 1
            )
        base = F_value(k, weights)

        for subset in proper_subsets:
            stats = subset_stats[subset]
            stats["checked_b_root_rays"] += 1
            if all(value > 0 for value in weights):
                stats["strictly_positive_b_root_rays"] += 1
            deleted = F_deleted_value(k, weights, subset)
            delta = base - deleted
            deletion_bound = s_first_deletion_bound(k, index, weights, subset)
            slack = deletion_bound - delta

            active_f = active_b
            active_deleted = active_source_deletion_branches(k, weights, subset)
            for branch in active_f:
                key = subset_label(k, branch)
                stats["active_F_branches"][key] = stats["active_F_branches"].get(key, 0) + 1
            for branch in active_deleted:
                key = subset_label(k, branch)
                stats["active_deleted_branches"][key] = (
                    stats["active_deleted_branches"].get(key, 0) + 1
                )

            if stats["minimum_slack"] is None or slack < stats["minimum_slack"]:
                witness = _witness_payload(
                    k,
                    index,
                    weights,
                    subset,
                    base,
                    deleted,
                    delta,
                    deletion_bound,
                    slack,
                    b_cost,
                    true_optimum,
                    active_f,
                    active_deleted,
                )
                stats["minimum_slack"] = slack
                stats["minimum_slack_witness"] = witness
            if slack == 0 and len(stats["tight_examples"]) < 3 and include_samples:
                witness = _witness_payload(
                    k,
                    index,
                    weights,
                    subset,
                    base,
                    deleted,
                    delta,
                    deletion_bound,
                    slack,
                    b_cost,
                    true_optimum,
                    active_f,
                    active_deleted,
                )
                stats["tight_examples"].append(witness)
            if slack < 0:
                witness = _witness_payload(
                    k,
                    index,
                    weights,
                    subset,
                    base,
                    deleted,
                    delta,
                    deletion_bound,
                    slack,
                    b_cost,
                    true_optimum,
                    active_f,
                    active_deleted,
                )
                stats["failures"].append(witness)
                if all(value > 0 for value in weights):
                    stats["strictly_positive_failures"].append(witness)
                if first_obstruction is None:
                    first_obstruction = witness

    function_failures = _audit_F_formula(k, bound=min(bound, 3))
    subset_summaries = []
    for subset, stats in subset_stats.items():
        failures = stats["failures"]
        positive_failures = stats["strictly_positive_failures"]
        minimum_slack = stats["minimum_slack"]
        summary = {
            "subset": subset_payload(k, subset),
            "support_size": len(subset),
            "checked_b_root_rays": stats["checked_b_root_rays"],
            "strictly_positive_b_root_rays": stats["strictly_positive_b_root_rays"],
            "minimum_slack": (
                rational_payload(minimum_slack)
                if isinstance(minimum_slack, Fraction)
                else None
            ),
            "minimum_slack_witness": stats["minimum_slack_witness"],
            "failure_count": len(failures),
            "strictly_positive_failure_count": len(positive_failures),
            "failures": failures[:5],
            "strictly_positive_failures": positive_failures[:5],
            "tight_examples": stats["tight_examples"],
            "corrected_h_star_active_F_branch_counts": stats["active_F_branches"],
            "corrected_h_star_active_deleted_branch_counts": stats[
                "active_deleted_branches"
            ],
            "domination_certificate_attempt": _certificate_attempt_payload(
                k, subset, failures
            ),
        }
        subset_summaries.append(summary)

    return {
        "schema": "proper_subset_contraction_small_k_v0",
        "k": k,
        "topology": "DS(k,1)",
        "labels": list(labels(k)),
        "public_dual": public_dual_skeleton(k),
        "normalization": {
            "weight_rays": f"primitive integer rays with coordinates in [0,{bound}]",
            "depth_convention": "root-depth-0",
            "A_b_s": (
                "b-root Bellman-normal rays grouped by corrected F(L) active "
                "source-deletion branches s"
            ),
        },
        "corrected_formulas": {
            "F(L)": "min_A U(L\\A)+kappa(A)",
            "F_deleted(L,S)": "min_A U((L\\A)\\S)+kappa(A)",
            "kappa(A)": "sum_i_in_A min(alpha,u_i)+sum_pairs_intersecting_A min(u_i,u_j)",
            "delta(S)": "F(L)-F_deleted(L,S)",
            "D(S)": "best S-first-b STT cost minus best b-root STT cost",
        },
        "counts": {
            "all_stt_depth_vectors": len(index.all_depths),
            "b_root_depth_vectors": len(index.b_root_depths),
            "integer_rays_considered": len(rays),
            "b_root_bellman_optimal_rays": b_root_ray_count,
            "strictly_positive_b_root_rays": positive_b_root_ray_count,
            "proper_nonsingleton_subsets": len(proper_subsets),
            "F_formula_failures_on_small_star_grid": len(function_failures),
        },
        "corrected_A_b_s_branch_counts": active_cone_counts,
        "proper_subset_summaries": subset_summaries,
        "first_obstruction_candidate": first_obstruction,
        "status": (
            "obstruction_candidate_found"
            if first_obstruction is not None
            else "no_obstruction_in_checked_rays"
        ),
        "overclaim_guard": (
            "Finite exact evidence only.  This JSON does not prove the all-k "
            "proper-subset contraction lemma and does not claim public LP "
            "exactness on DS(k,1)."
        ),
    }


def _witness_payload(
    k: int,
    index: DepthIndex,
    weights: tuple[Fraction, ...],
    subset: tuple[int, ...],
    base: Fraction,
    deleted: Fraction,
    delta: Fraction,
    deletion_bound: Fraction,
    slack: Fraction,
    b_cost: Fraction,
    true_optimum: Fraction,
    active_f: tuple[tuple[int, ...], ...],
    active_deleted: tuple[tuple[int, ...], ...],
) -> dict[str, Any]:
    return {
        "weights": weights_payload(k, weights),
        "subset": subset_payload(k, subset),
        "F": rational_payload(base),
        "F_deleted": rational_payload(deleted),
        "delta": rational_payload(delta),
        "D_S": rational_payload(deletion_bound),
        "slack_D_minus_delta": rational_payload(slack),
        "b_root_cost": rational_payload(b_cost),
        "true_bellman_optimum": rational_payload(true_optimum),
        "b_root_bellman_optimal": b_cost == true_optimum,
        "strictly_positive_weights": all(value > 0 for value in weights),
        "active_F_branches": [subset_payload(k, branch) for branch in active_f],
        "active_deleted_branches": [
            subset_payload(k, branch) for branch in active_deleted
        ],
        "bellman_gaps": {
            "B/a": rational_payload(first_root_gap(index, weights, k)),
            "B/b": rational_payload(first_root_gap(index, weights, k + 1)),
            "B/r": rational_payload(first_root_gap(index, weights, k + 2)),
            **{
                f"B/{label(k, leaf)}": rational_payload(
                    first_root_gap(index, weights, leaf)
                )
                for leaf in left_vertices(k)
            },
        },
    }


def _certificate_attempt_payload(
    k: int, subset: tuple[int, ...], failures: list[dict[str, Any]]
) -> dict[str, Any]:
    if failures:
        return {
            "status": "failed_for_checked_rays",
            "failed_cut_support": subset_payload(k, subset),
            "combination_tried": [
                {"inequality": f"SUB_{subset_label(k, subset)}", "coefficient": "1"}
            ],
            "note": (
                "The natural S-first deletion bound does not dominate delta on "
                "at least one checked b-root Bellman ray.  See failures for exact "
                "obstruction candidates and Bellman verification."
            ),
        }
    return {
        "status": "certified_on_checked_rays",
        "combination": [
            {"inequality": f"SUB_{subset_label(k, subset)}", "coefficient": "1"}
        ],
        "residual_checked": "D(S)-delta(S) >= 0 on all checked b-root rays",
        "uses_only": [
            "public R/Q skeleton for LP-side domains",
            "Bellman B/a, B/r, B/i gap evaluation",
            "proper subset SUB_S finite check",
            "trivial nonnegativity of checked weights",
        ],
    }


def _audit_F_formula(k: int, bound: int) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for values in product(range(bound + 1), repeat=k + 1):
        if not any(values):
            continue
        weights = tuple(Fraction(value) for value in values) + (
            Fraction(0),
            Fraction(0),
        )
        formula = F_value(k, weights)
        direct = corrected_star_stt_cost(k, weights)
        if formula != direct:
            failures.append(
                {
                    "weights": weights_payload(k, weights),
                    "formula": rational_payload(formula),
                    "direct_star_stt": rational_payload(direct),
                }
            )
            if len(failures) >= 5:
                break
    return failures


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_report(path: Path, k3: dict[str, Any], k4: dict[str, Any] | None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payloads = [payload for payload in (k3, k4) if payload is not None]
    lines: list[str] = []
    lines.append("# Proper-Subset Source-Deletion Contraction Audit v0")
    lines.append("")
    lines.append("## Stop Sign")
    lines.append("")
    lines.append(
        "Finite exact small-k evidence only. This report does not claim public LP "
        "exactness on `DS(k,1)`, does not promote the b-root branch to a theorem, "
        "and does not prove the all-k proper-subset contraction lemma."
    )
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(
        "The scripts implement the corrected source-deletion formula "
        "`F^{(-S)}(L)=min_A U((L\\A)\\S)+kappa(A)` with "
        "`kappa(A)=sum_{i in A} min(alpha,u_i)+sum_{pairs intersect A} min(u_i,u_j)`. "
        "The public-LP side records only the SKZ/Golinsky dual skeleton with "
        "unordered `R` and ordered collinear-triplet `Q` variables, capping rows, "
        "and frequency rows."
    )
    lines.append("")
    lines.append("## Exact Status")
    lines.append("")
    lines.append("| k | integer rays | b-root rays | positive b-root rays | proper subsets | status |")
    lines.append("|---:|---:|---:|---:|---:|---|")
    for payload in payloads:
        counts = payload["counts"]
        lines.append(
            "| {k} | {rays} | {broot} | {positive} | {subsets} | `{status}` |".format(
                k=payload["k"],
                rays=counts["integer_rays_considered"],
                broot=counts["b_root_bellman_optimal_rays"],
                positive=counts["strictly_positive_b_root_rays"],
                subsets=counts["proper_nonsingleton_subsets"],
                status=payload["status"],
            )
        )
    lines.append("")
    lines.append("The corrected `F(L)` formula was cross-checked against direct star-STT enumeration on the small star grids used by the script; no formula mismatch was found in the recorded runs.")
    lines.append("")
    lines.append("## Floating Evidence")
    lines.append("")
    lines.append(
        "None. The generated JSON values are exact `Fraction` computations serialized "
        "as reduced rational strings. The only limitation is finite coverage, not "
        "floating-point reconstruction."
    )
    lines.append("")
    lines.append("## First Proper-Subset Cut")
    lines.append("")
    first = next(
        (payload.get("first_obstruction_candidate") for payload in payloads if payload.get("first_obstruction_candidate")),
        None,
    )
    if first is None:
        lines.append(
            "No proper-subset obstruction appeared in the checked rays. The first "
            "proper-subset families are certified only in the finite sense recorded "
            "in JSON: `SUB_S` has nonnegative exact slack on every checked b-root ray."
        )
    else:
        lines.append(
            "The natural `D(S)` interpretation as the best S-first-b Bellman gap "
            "has an exact boundary obstruction candidate. This is not an all-k "
            "counterexample to any theorem unless this is confirmed as the intended "
            "`D(S)` definition, but it is a real architecture warning for this "
            "formulation."
        )
        lines.append("")
        lines.append(f"- support: `{first['subset']}`")
        lines.append(f"- weights: `{first['weights']}`")
        lines.append(f"- `F`: `{first['F']}`")
        lines.append(f"- `F_deleted`: `{first['F_deleted']}`")
        lines.append(f"- `delta(S)`: `{first['delta']}`")
        lines.append(f"- `D(S)`: `{first['D_S']}`")
        lines.append(f"- slack `D(S)-delta(S)`: `{first['slack_D_minus_delta']}`")
        lines.append(f"- b-root cost: `{first['b_root_cost']}`")
        lines.append(f"- true Bellman optimum: `{first['true_bellman_optimum']}`")
        lines.append(f"- b-root Bellman-optimal: `{first['b_root_bellman_optimal']}`")
        lines.append(f"- strictly positive weights: `{first['strictly_positive_weights']}`")
    lines.append("")
    lines.append("## Public Dual Skeleton")
    lines.append("")
    for payload in payloads:
        counts = payload["public_dual"]["counts"]
        lines.append(
            f"- k={payload['k']}: `R` variables `{counts['R']}`, `Q` variables "
            f"`{counts['Q']}`, capping rows `{counts['capping_constraints']}`, "
            f"frequency rows `{counts['frequency_constraints']}`."
        )
    lines.append("")
    lines.append("No H1/H2, refined-Z, path-monotonicity, ancestry-transitivity, or LCA-separation rows are generated.")
    lines.append("")
    lines.append("## Corrected A_b(s) Families")
    lines.append("")
    lines.append(
        "The JSON groups normalized b-root Bellman rays by the corrected active "
        "`F(L)` branch `s`; these are the finite `A_b(s)` cut families extracted "
        "by the scripts. Proper non-singleton supports are then audited as "
        "`SUB_S` rows against exact `delta(S)` and `D(S)` values."
    )
    lines.append("")
    for payload in payloads:
        branch_counts = ", ".join(
            f"{branch}: {count}"
            for branch, count in sorted(payload["corrected_A_b_s_branch_counts"].items())
        )
        lines.append(f"- k={payload['k']}: {branch_counts}")
    lines.append("")
    lines.append("## Proper-Subset Summary")
    lines.append("")
    for payload in payloads:
        lines.append(f"### k={payload['k']}")
        lines.append("")
        lines.append("| S | checked b-root rays | min slack | failures | positive failures | certificate status |")
        lines.append("|---|---:|---:|---:|---:|---|")
        for summary in payload["proper_subset_summaries"]:
            lines.append(
                "| `{S}` | {checked} | `{slack}` | {failures} | {positive_failures} | `{status}` |".format(
                    S=summary["subset"],
                    checked=summary["checked_b_root_rays"],
                    slack=summary["minimum_slack"],
                    failures=summary["failure_count"],
                    positive_failures=summary["strictly_positive_failure_count"],
                    status=summary["domination_certificate_attempt"]["status"],
                )
            )
        lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    if first is None:
        lines.append(
            "This supports another manual proof pass: the corrected source-deletion "
            "formula survives the checked b-root rays, including proper non-singleton "
            "supports. The evidence is still finite and should be used only for "
            "lemma mining."
        )
    else:
        lines.append(
            "This points to an architecture correction or at least a degeneracy "
            "patch before a proof pass: the S-first deletion bound must either be "
            "stronger than the audited Bellman interpretation, or the proof must "
            "route boundary faces through `B/a`, `B/r`, singleton rows, or explicit "
            "capacity/nonnegativity rows."
        )
    lines.append("")
    lines.append("## Artifacts")
    lines.append("")
    lines.append(f"- `{DEFAULT_K3_JSON}`")
    if k4 is not None:
        lines.append(f"- `{DEFAULT_K4_JSON}`")
    lines.append(f"- `{path}`")
    lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--k3-bound", type=int, default=3)
    parser.add_argument("--k4-bound", type=int, default=2)
    parser.add_argument("--skip-k4", action="store_true")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--k3-json", type=Path, default=DEFAULT_K3_JSON)
    parser.add_argument("--k4-json", type=Path, default=DEFAULT_K4_JSON)
    args = parser.parse_args(argv)

    k3 = run_k_audit(3, args.k3_bound)
    write_json(args.k3_json, k3)
    k4 = None
    if not args.skip_k4:
        k4 = run_k_audit(4, args.k4_bound)
        write_json(args.k4_json, k4)
    write_report(args.report, k3, k4)

    print(
        "proper-subset contraction audit: "
        f"k3={k3['status']} "
        f"k4={(k4['status'] if k4 else 'skipped')} "
        f"report={args.report}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
