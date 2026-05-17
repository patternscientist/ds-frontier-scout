"""DS(k,1) H1/H2 depth-exactness and coarea scouting harness.

This module is a finite, exact-rational experiment for double-stars
``DS(k,1)``: left leaves ``x_1..x_k`` adjacent to ``a``, center edge ``a-b``,
and one right leaf ``r`` adjacent to ``b``.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations_with_replacement, product
import json
import random
from pathlib import Path
from typing import Any, Iterable

from .double_star_depth_projection import (
    DoubleStarLPResult,
    double_star_spec,
    double_star_topology,
    solve_double_star_lp_exact,
    structured_weight_vectors,
)
from .enumerate_stts import integer_optimum_by_enumeration
from .hereditary_lp import (
    DEFAULT_TOLERANCE,
    SKZ_LONG_STAR_TOPOLOGY,
    SKZ_LONG_STAR_WEIGHTS,
    build_hereditary_lp,
    solve_hereditary_lp,
)
from .lp_feasibility import path_between
from .rationals import rational_to_string
from .star_depth_projection import evaluate_objective as evaluate_star_objective
from .topology import TreeTopology


DEFAULT_REPORT = Path("reports/stt_dsk1_h1_coarea_v0.md")
DEFAULT_CERTIFICATES = Path("examples/stt_lp/dsk1_h1_coarea_v0_certificates.json")


@dataclass(frozen=True)
class BellmanResult:
    optimum: Fraction
    phi: dict[tuple[int, ...], Fraction]
    phi_submodular: bool
    phi_violations: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class CaseResult:
    k: int
    family: str
    weights: tuple[Fraction, ...]
    true_optimum: Fraction
    phi_submodular: bool
    phi_violations: tuple[dict[str, Any], ...]
    h1: DoubleStarLPResult
    h2: DoubleStarLPResult | None
    h2_status: str
    dual_pattern: str

    @property
    def h1_gap(self) -> Fraction:
        return self.h1.optimum - self.true_optimum

    @property
    def h2_optimum(self) -> Fraction:
        if self.h2 is None:
            return self.true_optimum
        return self.h2.optimum

    @property
    def h2_gap(self) -> Fraction:
        return self.h2_optimum - self.true_optimum


def dsk1_labels(k: int) -> dict[int, str]:
    spec = double_star_spec(k, 1)
    return {
        **{leaf: f"x{index + 1}" for index, leaf in enumerate(spec.left_leaves)},
        spec.a: "a",
        spec.b: "b",
        spec.right_leaves[0]: "r",
    }


def bellman_true_optimum(k: int, weights: Iterable[Fraction | int]) -> Fraction:
    """Compute the exact DS(k,1) optimum by the left-leaf/a/b/r recurrence."""

    weight_tuple = tuple(Fraction(value) for value in weights)
    expected_n = k + 3
    if len(weight_tuple) != expected_n:
        raise ValueError("DS(k,1) weight vector must have length k+3")
    memo: dict[tuple[int, ...], Fraction] = {}
    topology = double_star_topology(k, 1)

    def component_weight(component: tuple[int, ...]) -> Fraction:
        return sum((weight_tuple[v] for v in component), Fraction(0))

    def unrestricted(component: tuple[int, ...]) -> Fraction:
        component = tuple(sorted(component))
        if len(component) <= 1:
            return Fraction(0)
        if component in memo:
            return memo[component]
        best: Fraction | None = None
        for root in component:
            value = Fraction(0)
            for child in topology.connected_components_after_removing(root, component):
                value += unrestricted(child) + component_weight(child)
            if best is None or value < best:
                best = value
        if best is None:
            raise ValueError("empty component in recurrence")
        memo[component] = best
        return best

    return unrestricted(tuple(range(expected_n)))


def bellman_phi(k: int, weights: Iterable[Fraction | int]) -> BellmanResult:
    """Return Phi(S), where S is exactly the left-leaf ancestor set of a."""

    weight_tuple = tuple(Fraction(value) for value in weights)
    expected_n = k + 3
    if len(weight_tuple) != expected_n:
        raise ValueError("DS(k,1) weight vector must have length k+3")
    spec = double_star_spec(k, 1)
    topology = double_star_topology(k, 1)
    left_set = set(spec.left_leaves)
    unrestricted_memo: dict[tuple[int, ...], Fraction] = {}
    conditioned_memo: dict[tuple[tuple[int, ...], tuple[int, ...]], Fraction | None] = {}

    def component_weight(component: tuple[int, ...]) -> Fraction:
        return sum((weight_tuple[v] for v in component), Fraction(0))

    def unrestricted(component: tuple[int, ...]) -> Fraction:
        component = tuple(sorted(component))
        if len(component) <= 1:
            return Fraction(0)
        if component in unrestricted_memo:
            return unrestricted_memo[component]
        best: Fraction | None = None
        for root in component:
            value = Fraction(0)
            for child in topology.connected_components_after_removing(root, component):
                value += unrestricted(child) + component_weight(child)
            if best is None or value < best:
                best = value
        if best is None:
            raise ValueError("empty unrestricted component")
        unrestricted_memo[component] = best
        return best

    def conditioned(component: tuple[int, ...], target: tuple[int, ...]) -> Fraction | None:
        component = tuple(sorted(component))
        target = tuple(sorted(target))
        key = (component, target)
        if key in conditioned_memo:
            return conditioned_memo[key]
        if spec.a not in component:
            raise ValueError("conditioned component must contain a")
        component_left = set(component) & left_set
        if not set(target).issubset(component_left):
            conditioned_memo[key] = None
            return None

        best: Fraction | None = None
        for root in component:
            if root == spec.a and target:
                continue
            if root in left_set and root not in target:
                continue
            value = Fraction(0)
            feasible = True
            next_target = tuple(x for x in target if x != root)
            for child in topology.connected_components_after_removing(root, component):
                if spec.a in child:
                    child_value = conditioned(child, next_target)
                else:
                    child_value = unrestricted(child)
                if child_value is None:
                    feasible = False
                    break
                value += child_value + component_weight(child)
            if feasible and (best is None or value < best):
                best = value
        conditioned_memo[key] = best
        return best

    phi: dict[tuple[int, ...], Fraction] = {}
    full = tuple(range(expected_n))
    for mask in range(1 << k):
        subset = tuple(leaf for bit, leaf in enumerate(spec.left_leaves) if mask & (1 << bit))
        value = conditioned(full, subset)
        if value is None:
            raise ValueError(f"Phi unexpectedly infeasible for {subset}")
        phi[subset] = value

    violations: list[dict[str, Any]] = []
    subsets = tuple(phi)
    for first in subsets:
        first_set = set(first)
        for second in subsets:
            second_set = set(second)
            union = tuple(sorted(first_set | second_set))
            intersection = tuple(sorted(first_set & second_set))
            slack = phi[first] + phi[second] - phi[union] - phi[intersection]
            if slack < 0:
                violations.append(
                    {
                        "A": list(first),
                        "B": list(second),
                        "phi_A": rational_to_string(phi[first]),
                        "phi_B": rational_to_string(phi[second]),
                        "phi_union": rational_to_string(phi[union]),
                        "phi_intersection": rational_to_string(phi[intersection]),
                        "slack": rational_to_string(slack),
                    }
                )
    return BellmanResult(
        optimum=bellman_true_optimum(k, weight_tuple),
        phi=phi,
        phi_submodular=not violations,
        phi_violations=tuple(violations),
    )


def small_integer_weight_vectors(k: int, bound: int = 2) -> tuple[tuple[str, tuple[Fraction, ...]], ...]:
    """Enumerate nonzero integer weights modulo left-leaf permutation."""

    cases: list[tuple[str, tuple[Fraction, ...]]] = []
    for nondecreasing_left in combinations_with_replacement(range(bound + 1), k):
        left = tuple(Fraction(value) for value in reversed(nondecreasing_left))
        for centers in product(range(bound + 1), repeat=3):
            weights = left + tuple(Fraction(value) for value in centers)
            if any(weights):
                cases.append((f"small_int_leq_{bound}", weights))
    return tuple(cases)


def structured_random_weight_vectors(
    k: int, seed: int = 4101, random_count: int = 2
) -> tuple[tuple[str, tuple[Fraction, ...]], ...]:
    """Structured plus orbit-friendly pseudorandom integer weights for k=4,5."""

    wanted = {
        "one_heavy_left_leaf",
        "one_heavy_right_leaf",
        "all_left_leaves_heavy",
        "all_right_leaves_heavy",
        "left_center_heavy",
        "right_center_heavy",
        "both_centers_heavy",
        "asym_left_center_right_leaf",
    }
    cases = [
        (name, weights)
        for name, weights in structured_weight_vectors(k, 1)
        if name in wanted
    ]
    rng = random.Random(seed + k)
    for index in range(random_count):
        split = rng.randrange(1, k)
        high = Fraction(rng.randrange(3, 8))
        low = Fraction(rng.randrange(0, 4))
        center_a = Fraction(rng.randrange(0, 6))
        center_b = Fraction(rng.randrange(0, 6))
        right = Fraction(rng.randrange(0, 8))
        left = tuple([high] * split + [low] * (k - split))
        weights = left + (center_a, center_b, right)
        if any(weights):
            cases.append((f"two_block_random_seed_{seed + k}_{index}", weights))
    dedup: dict[tuple[Fraction, ...], str] = {}
    for name, weights in cases:
        dedup.setdefault(weights, name)
    return tuple((name, weights) for weights, name in dedup.items())


def evaluate_case(
    k: int,
    weights: Iterable[Fraction | int],
    family: str,
    tolerance: float = DEFAULT_TOLERANCE,
) -> CaseResult:
    weight_tuple = tuple(Fraction(value) for value in weights)
    bellman = bellman_phi(k, weight_tuple)
    h1 = solve_double_star_lp_exact(
        k,
        1,
        weight_tuple,
        relaxation="h1",
        tolerance=tolerance,
    )
    if h1.optimum == bellman.optimum:
        h2 = None
        h2_status = "exact_by_h1_equals_stt_sandwich_no_separate_h2_primal"
    else:
        h2 = solve_double_star_lp_exact(
            k,
            1,
            weight_tuple,
            relaxation="h2",
            tolerance=tolerance,
        )
        h2_status = h2.certificate_status
    return CaseResult(
        k=k,
        family=family,
        weights=weight_tuple,
        true_optimum=bellman.optimum,
        phi_submodular=bellman.phi_submodular,
        phi_violations=bellman.phi_violations,
        h1=h1,
        h2=h2,
        h2_status=h2_status,
        dual_pattern=classify_dual_pattern(k, h1),
    )


def classify_dual_pattern(k: int, h1: DoubleStarLPResult) -> str:
    if k == 1:
        return "path exactness"
    active = tuple(row["row"] for row in h1.active_rows)
    heredity_rows = [row for row in active if row.get("kind") == "heredity"]
    spec = double_star_spec(k, 1)
    left_star = set(spec.left_leaves) | {spec.a}

    def row_vertices(row: dict[str, Any]) -> set[int]:
        vertices: set[int] = set()
        for key in ("superset", "subset", "component"):
            raw = row.get(key)
            if isinstance(raw, list):
                vertices.update(int(v) for v in raw)
        if isinstance(row.get("root"), int):
            vertices.add(int(row["root"]))
        return vertices

    if heredity_rows and all(row_vertices(row).issubset(left_star) for row in heredity_rows):
        return "pure-star coarea"
    if k == 2:
        return "DS(2,1)-style endpoint allocation"
    return "new global leaf-exchange/coarea lemma"


def regression_summary() -> dict[str, Any]:
    star = evaluate_star_objective(4, (3, 2, 2, 1, 1), k=1, family="pure_star_h1")
    topology = TreeTopology.from_dict(SKZ_LONG_STAR_TOPOLOGY)
    weights = {v: Fraction(SKZ_LONG_STAR_WEIGHTS[v]) for v in topology.vertices}
    true_u73, _witness, _count = integer_optimum_by_enumeration(
        topology,
        weights,
        depth_base=0,
        max_count=100_000,
    )
    h1_u73 = solve_hereditary_lp(topology, weights, relaxation="h1")
    h1_u73_exact = h1_u73.to_result_json(
        include_variables=False,
        include_rationalized=True,
    )["rationalized_certificate"]["exact_objective"]
    return {
        "pure_stars_h1_exact": {
            "d": 4,
            "weights": [rational_to_string(value) for value in star.weights],
            "stt": rational_to_string(star.stt_optimum),
            "h1": rational_to_string(star.h_optimum),
            "gap": rational_to_string(star.gap),
            "certificate_verified": star.certificate.verified,
        },
        "u_7_3_h1_gap": {
            "topology": "repo SKZ_LONG_STAR_TOPOLOGY / U(7,3) regression",
            "weights": [str(value) for value in SKZ_LONG_STAR_WEIGHTS],
            "true_stt": rational_to_string(true_u73),
            "h1": h1_u73_exact,
            "gap_h1_minus_true": rational_to_string(
                _parse_fraction_string(h1_u73_exact) - true_u73
            ),
        },
        "ds21_persistency_caveat": {
            "status": "retained",
            "note": (
                "DS(2,1) full depth objectives tested here are H1-tight, but prior "
                "normal-cone and pinned-boundary artifacts separate full-H1 depth "
                "exactness from reduced-functional persistency/coherence claims."
            ),
            "related_artifacts": [
                "reports/stt_double_star_ds21_normal_cones_v1_coverage.md",
                "reports/stt_double_star_ds21_pinned_boundary_v2.md",
            ],
        },
    }


def run_scout(
    exhaustive_bound: int = 2,
    random_count: int = 2,
    tolerance: float = DEFAULT_TOLERANCE,
    include_regressions: bool = True,
    include_large: bool = True,
) -> dict[str, Any]:
    cases: list[CaseResult] = []
    for k in (1, 2, 3):
        for family, weights in small_integer_weight_vectors(k, bound=exhaustive_bound):
            cases.append(evaluate_case(k, weights, family, tolerance=tolerance))
    if include_large:
        for k in (4, 5):
            for family, weights in structured_random_weight_vectors(k, random_count=random_count):
                cases.append(evaluate_case(k, weights, family, tolerance=tolerance))
    return {
        "schema": "stt_dsk1_h1_coarea_v0",
        "settings": {
            "topologies": [f"DS({k},1)" for k in range(1, 6)],
            "small_integer_exhaustive_k": [1, 2, 3],
            "small_integer_bound": exhaustive_bound,
            "structured_random_k": [4, 5],
            "random_count_per_large_k": random_count,
            "tolerance": tolerance,
        },
        "cases": cases,
        "regressions": regression_summary() if include_regressions else {},
    }


def write_outputs(
    report_path: Path = DEFAULT_REPORT,
    certificate_path: Path = DEFAULT_CERTIFICATES,
    exhaustive_bound: int = 2,
    random_count: int = 2,
    include_regressions: bool = True,
    include_large: bool = True,
) -> dict[str, Any]:
    data = run_scout(
        exhaustive_bound=exhaustive_bound,
        random_count=random_count,
        include_regressions=include_regressions,
        include_large=include_large,
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    certificate_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(_render_report(data, certificate_path), encoding="utf-8")
    certificate_path.write_text(
        json.dumps(_certificates_json(data), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    h1_gaps = [case for case in data["cases"] if case.h1_gap < 0]
    phi_failures = [case for case in data["cases"] if not case.phi_submodular]
    return {
        "report": str(report_path),
        "certificates": str(certificate_path),
        "cases": len(data["cases"]),
        "h1_gaps": len(h1_gaps),
        "phi_failures": len(phi_failures),
    }


def _case_json(case: CaseResult, include_dual: bool = False) -> dict[str, Any]:
    labels = dsk1_labels(case.k)
    payload: dict[str, Any] = {
        "topology": f"DS({case.k},1)",
        "family": case.family,
        "weights": {
            labels[index]: rational_to_string(case.weights[index])
            for index in range(case.k + 3)
        },
        "true_stt_optimum_bellman": rational_to_string(case.true_optimum),
        "h1_optimum": rational_to_string(case.h1.optimum),
        "h1_gap": rational_to_string(case.h1_gap),
        "h1_certificate_status": case.h1.certificate_status,
        "h2_optimum": rational_to_string(case.h2_optimum),
        "h2_gap": rational_to_string(case.h2_gap),
        "h2_certificate_status": case.h2_status,
        "phi_submodular": case.phi_submodular,
        "phi_violation_count": len(case.phi_violations),
        "dual_pattern": case.dual_pattern,
    }
    if case.phi_violations:
        payload["first_phi_violation"] = case.phi_violations[0]
    if include_dual:
        payload["h1_dual_certificate"] = _dual_certificate_json(case.h1)
    if case.h1_gap < 0:
        payload["h1_gap_witness"] = _h1_gap_witness_json(case)
    return payload


def _dual_certificate_json(result: DoubleStarLPResult) -> dict[str, Any]:
    cert = result.certificate
    return {
        "status": result.certificate_status,
        "objective": rational_to_string(cert.objective) if cert is not None else None,
        "verified": cert.verified if cert is not None else False,
        "max_primal_violation": (
            rational_to_string(cert.max_primal_violation) if cert is not None else None
        ),
        "max_dual_deficit": (
            rational_to_string(cert.max_dual_deficit) if cert is not None else None
        ),
        "basis_size": len(cert.basis) if cert is not None else None,
        "nonzero_dual_rows": result.active_rows,
    }


def _h1_gap_witness_json(case: CaseResult) -> dict[str, Any]:
    labels = dsk1_labels(case.k)
    depths = _lp_depths(case.h1)
    return {
        "violated_stt_dominant_inequality": {
            "form": "sum_v w_v D_v >= OPT_STT(w)",
            "weights": {
                labels[index]: rational_to_string(case.weights[index])
                for index in range(case.k + 3)
            },
            "rhs": rational_to_string(case.true_optimum),
            "h1_lhs": rational_to_string(case.h1.optimum),
            "slack": rational_to_string(case.h1.optimum - case.true_optimum),
        },
        "h1_fractional_depths": {
            labels[index]: rational_to_string(depths[index])
            for index in range(case.k + 3)
        },
        "h1_primal_nonzero_orbit_values": [
            {
                "component": list(component),
                "root": root,
                "value": rational_to_string(case.h1.values[index]),
            }
            for index, (component, root) in enumerate(case.h1.lp.orbit_variables)
            if case.h1.values[index]
        ],
    }


def _lp_depths(result: DoubleStarLPResult) -> tuple[Fraction, ...]:
    values = tuple(result.values[orbit] for orbit in result.lp.variable_to_orbit)
    depths: list[Fraction] = []
    for vertex in result.lp.topology.vertices:
        value = Fraction(0)
        for source in result.lp.topology.vertices:
            if source == vertex:
                continue
            path_component = tuple(sorted(path_between(result.lp.topology, source, vertex)))
            index = result.lp.full_variables.index((path_component, source))
            value += values[index]
        depths.append(value)
    return tuple(depths)


def _certificates_json(data: dict[str, Any]) -> dict[str, Any]:
    cases: list[CaseResult] = data["cases"]
    representatives: dict[tuple[int, str], CaseResult] = {}
    for case in cases:
        representatives.setdefault((case.k, case.dual_pattern), case)
    return {
        "schema": data["schema"],
        "settings": data["settings"],
        "summary": _summary_json(cases),
        "cases": [_case_json(case) for case in cases],
        "representative_h1_dual_certificates": [
            _case_json(case, include_dual=True)
            for _key, case in sorted(representatives.items(), key=lambda item: item[0])
        ],
        "h1_gap_witnesses": [
            _case_json(case, include_dual=True)
            for case in cases
            if case.h1_gap < 0
        ],
        "phi_submodularity_failures": [
            _case_json(case)
            for case in cases
            if not case.phi_submodular
        ],
        "regressions": data["regressions"],
    }


def _summary_json(cases: list[CaseResult]) -> dict[str, Any]:
    by_k: dict[str, dict[str, Any]] = {}
    for k in range(1, 6):
        subset = [case for case in cases if case.k == k]
        if not subset:
            continue
        by_k[str(k)] = {
            "cases": len(subset),
            "h1_gaps": sum(1 for case in subset if case.h1_gap < 0),
            "h2_gaps": sum(1 for case in subset if case.h2_gap < 0),
            "phi_submodularity_failures": sum(
                1 for case in subset if not case.phi_submodular
            ),
            "dual_patterns": sorted({case.dual_pattern for case in subset}),
            "h1_certificate_statuses": sorted({case.h1.certificate_status for case in subset}),
        }
    return {
        "total_cases": len(cases),
        "by_k": by_k,
        "overall_h1_gaps": sum(1 for case in cases if case.h1_gap < 0),
        "overall_h2_gaps": sum(1 for case in cases if case.h2_gap < 0),
        "overall_phi_submodularity_failures": sum(
            1 for case in cases if not case.phi_submodular
        ),
    }


def _render_report(data: dict[str, Any], certificate_path: Path) -> str:
    cases: list[CaseResult] = data["cases"]
    h1_gaps = [case for case in cases if case.h1_gap < 0]
    h2_gaps = [case for case in cases if case.h2_gap < 0]
    phi_failures = [case for case in cases if not case.phi_submodular]
    summary = _summary_json(cases)

    lines: list[str] = []
    lines.append("# DS(k,1) H1/H2 Coarea Test v0")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append("This run tests `DS(k,1)` for `k=1..5` with exact rational Bellman optima and exact H1 dual certificates reconstructed from simplex bases. H2 values are exact by sandwich whenever H1 equals the true STT optimum; otherwise the H2 LP is solved directly.")
    lines.append("")
    lines.append("The true optimum is computed by the DS(k,1) recurrence that either peels a left leaf from the component containing `a`, chooses `a`, chooses `b`, or chooses the right leaf `r`. The same recurrence gives `Phi(S)`, the optimum conditioned on exactly `S` being the left-leaf ancestors of `a`.")
    lines.append("")
    lines.append("## Outcome")
    lines.append("")
    if h1_gaps:
        first = h1_gaps[0]
        lines.append(f"H1 gap found at `DS({first.k},1)` / `{first.family}`.")
        lines.append(f"- weights: `{_format_weights(first)}`")
        lines.append(f"- true STT: `{rational_to_string(first.true_optimum)}`")
        lines.append(f"- H1: `{rational_to_string(first.h1.optimum)}`")
    else:
        lines.append("No H1 depth gap appeared in the tested DS(k,1) cases.")
    if h2_gaps:
        first = h2_gaps[0]
        lines.append(f"H2 gap found at `DS({first.k},1)` / `{first.family}`.")
    else:
        lines.append("No H2 depth gap appeared; every reported H2 value is exact, mostly by H1/STT sandwiching.")
    if phi_failures:
        first = phi_failures[0]
        lines.append(f"`Phi` submodularity failed first at `DS({first.k},1)` / `{first.family}`.")
    else:
        lines.append("`Phi(S)` was submodular for every tested weight vector.")
    lines.append("")
    lines.append(f"JSON certificate artifacts are in `{certificate_path}`.")
    lines.append("")
    lines.append("## Coverage")
    lines.append("")
    lines.append("| k | cases | H1 gaps | H2 gaps | Phi failures | dual patterns |")
    lines.append("|---:|---:|---:|---:|---:|---|")
    for k, row in summary["by_k"].items():
        lines.append(
            "| {k} | {cases} | {h1} | {h2} | {phi} | `{patterns}` |".format(
                k=k,
                cases=row["cases"],
                h1=row["h1_gaps"],
                h2=row["h2_gaps"],
                phi=row["phi_submodularity_failures"],
                patterns=", ".join(row["dual_patterns"]),
            )
        )
    lines.append("")
    lines.append("## Dual Pattern Read")
    lines.append("")
    pattern_counts: dict[str, int] = {}
    for case in cases:
        pattern_counts[case.dual_pattern] = pattern_counts.get(case.dual_pattern, 0) + 1
    for pattern, count in sorted(pattern_counts.items()):
        lines.append(f"- `{pattern}`: `{count}` tested objectives.")
    lines.append("")
    lines.append("Finite classification: `DS(1,1)` behaves as path exactness; the `k=2` rows line up with the existing endpoint-allocation story; larger `k` cases repeatedly need cross-component heredity rows, so the natural proof target is a global leaf-exchange/coarea lemma rather than a pure-star argument.")
    lines.append("")
    lines.append("## Regressions")
    lines.append("")
    regressions = data["regressions"]
    if regressions:
        star = regressions["pure_stars_h1_exact"]
        u73 = regressions["u_7_3_h1_gap"]
        caveat = regressions["ds21_persistency_caveat"]
        lines.append(f"- Pure star regression: H1 `{star['h1']}` equals STT `{star['stt']}` with gap `{star['gap']}`.")
        lines.append(f"- `U(7,3)` regression: H1 `{u73['h1']}` versus true STT `{u73['true_stt']}`, gap `{u73['gap_h1_minus_true']}`.")
        lines.append(f"- DS(2,1) persistency caveat: {caveat['note']}")
    lines.append("")
    lines.append("## Skeptical Audit")
    lines.append("")
    lines.append("- This is finite evidence, not a theorem. The exhaustive part is only integer weights `0..2` modulo left-leaf symmetry for `k<=3`.")
    lines.append("- For `k=4,5`, random cases are deliberately orbit-friendly two-block integer vectors so exact LP reconstruction remains tractable.")
    lines.append("- H2 is often certified by sandwiching rather than separately solved; this is exact for the objective value but does not provide a separate H2 primal-dual basis in those cases.")
    lines.append("- The repeated dual-pattern labels are heuristic proof-route classifications, not promoted symbolic lemmas.")
    return "\n".join(lines) + "\n"


def _format_weights(case: CaseResult) -> str:
    labels = dsk1_labels(case.k)
    return "(" + ", ".join(
        f"{labels[index]}={rational_to_string(case.weights[index])}"
        for index in range(case.k + 3)
    ) + ")"


def _parse_fraction_string(value: str) -> Fraction:
    if "/" in value:
        numerator, denominator = value.split("/", 1)
        return Fraction(int(numerator), int(denominator))
    return Fraction(int(value), 1)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m scripts.stt_checker.dsk1_h1_coarea")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--certificates", type=Path, default=DEFAULT_CERTIFICATES)
    parser.add_argument("--exhaustive-bound", type=int, default=2)
    parser.add_argument("--random-count", type=int, default=2)
    args = parser.parse_args(argv)
    result = write_outputs(
        report_path=args.report,
        certificate_path=args.certificates,
        exhaustive_bound=args.exhaustive_bound,
        random_count=args.random_count,
    )
    print(
        "wrote {report} and {certificates}: cases={cases} "
        "h1_gaps={h1_gaps} phi_failures={phi_failures}".format(**result)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
