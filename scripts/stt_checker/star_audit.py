"""Exact Frontier Note v4 star-obstruction audit utilities."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterable

from .enumerate_stts import enumerate_stts
from .hereditary_lp import (
    RectangleConstraint,
    enumerate_connected_subsets,
    enumerate_h2_rectangle_constraints,
)
from .lp_feasibility import path_between
from .rationals import rational_to_string
from .topology import TreeTopology


DEFAULT_REPORT = Path("reports/stt_v4_star_audit_v0.md")
DEFAULT_EMBEDDING_BRANCH_LENGTHS = (
    (1, 1, 1, 1),
    (2, 1, 1, 1),
    (2, 2, 1, 1),
    (2, 2, 2, 2),
    (3, 2, 1, 1),
)


ZKey = tuple[tuple[int, ...], int]


@dataclass(frozen=True)
class SubdividedStar:
    topology: TreeTopology
    branches: tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class ConstraintFailure:
    family: str
    slack: Fraction
    details: str


@dataclass(frozen=True)
class FeasibilityAudit:
    simplex_count: int
    z_variable_count: int
    h1_count: int
    h2_ordered_count: int
    h2_canonical_nontrivial_count: int
    max_simplex_residual: Fraction
    min_h1_slack: Fraction
    min_h2_ordered_slack: Fraction
    min_h2_canonical_slack: Fraction
    first_failure: ConstraintFailure | None

    @property
    def feasible(self) -> bool:
        return self.first_failure is None


@dataclass(frozen=True)
class DepthDominantAudit:
    depth_vectors: tuple[tuple[int, ...], ...]
    target_depth: tuple[Fraction, ...]
    is_member: bool
    certificate: tuple[tuple[Fraction, tuple[int, ...], tuple[tuple[tuple[int, ...], int], ...]], ...]


@dataclass(frozen=True)
class EmbeddingAudit:
    branch_lengths: tuple[int, ...]
    topology: TreeTopology
    branches: tuple[tuple[int, ...], ...]
    feasibility: FeasibilityAudit
    center_root_mass: Fraction
    negative_masses: tuple[tuple[ZKey, Fraction], ...]


def subdivided_four_star(branch_lengths: Iterable[int]) -> SubdividedStar:
    """Build a subdivided 4-star with center 0 and branches in outward order."""

    lengths = tuple(branch_lengths)
    if len(lengths) != 4 or any(length <= 0 for length in lengths):
        raise ValueError("branch_lengths must contain four positive integers")

    edges: list[list[int]] = []
    branches: list[tuple[int, ...]] = []
    next_vertex = 1
    for length in lengths:
        previous = 0
        branch: list[int] = []
        for _ in range(length):
            vertex = next_vertex
            next_vertex += 1
            branch.append(vertex)
            edges.append([previous, vertex])
            previous = vertex
        branches.append(tuple(branch))

    topology = TreeTopology.from_dict(
        {
            "n": next_vertex,
            "vertices": list(range(next_vertex)),
            "edges": edges,
        }
    )
    return SubdividedStar(topology=topology, branches=tuple(branches))


def star4_instance() -> SubdividedStar:
    return subdivided_four_star((1, 1, 1, 1))


def embedded_z_value(component: Iterable[int], root: int, branches: tuple[tuple[int, ...], ...]) -> Fraction:
    """Return the exact v4 embedded first-hit value for a subdivided star.

    On center-containing connected sets this is the 4-leaf star obstruction,
    with each leaf-root mass assigned to the first vertex on the corresponding
    branch. On connected sets away from the center, the first hit is
    deterministically the vertex nearest the center.
    """

    component_set = set(component)
    if root not in component_set:
        return Fraction(0)

    if 0 not in component_set:
        for branch in branches:
            branch_vertices = [vertex for vertex in branch if vertex in component_set]
            if branch_vertices:
                return Fraction(1 if root == branch_vertices[0] else 0)
        raise ValueError("noncenter connected component is not on a branch")

    active = tuple(
        index
        for index, branch in enumerate(branches)
        if any(vertex in component_set for vertex in branch)
    )
    active_count = len(active)
    center_value = _star_center_value(active_count)
    if root == 0:
        return center_value

    for index in active:
        if root == branches[index][0]:
            return (1 - center_value) / active_count
    return Fraction(0)


def z_assignment(instance: SubdividedStar) -> dict[ZKey, Fraction]:
    values: dict[ZKey, Fraction] = {}
    for component in enumerate_connected_subsets(instance.topology):
        for root in component:
            values[(component, root)] = embedded_z_value(component, root, instance.branches)
    return values


def feasibility_audit(instance: SubdividedStar) -> FeasibilityAudit:
    topology = instance.topology
    connected = enumerate_connected_subsets(topology)
    connected_sets = {component: set(component) for component in connected}
    z_values = z_assignment(instance)

    max_simplex_residual = Fraction(0)
    first_failure: ConstraintFailure | None = None
    for component in connected:
        total = sum(z_values[(component, root)] for root in component)
        residual = abs(total - 1)
        max_simplex_residual = max(max_simplex_residual, residual)
        if residual and first_failure is None:
            first_failure = ConstraintFailure(
                "simplex",
                -residual,
                f"component={component}, total={rational_to_string(total)}",
            )

    h1_count = 0
    min_h1_slack: Fraction | None = None
    for superset in connected:
        superset_set = connected_sets[superset]
        for subset in connected:
            if len(subset) >= len(superset):
                continue
            if not connected_sets[subset].issubset(superset_set):
                continue
            for root in subset:
                h1_count += 1
                slack = z_values[(subset, root)] - z_values[(superset, root)]
                min_h1_slack = slack if min_h1_slack is None else min(min_h1_slack, slack)
                if slack < 0 and first_failure is None:
                    first_failure = ConstraintFailure(
                        "h1_heredity",
                        slack,
                        f"subset={subset}, superset={superset}, root={root}",
                    )

    h2_ordered_count = 0
    min_h2_ordered_slack: Fraction | None = None
    connected_set = set(connected)
    for base in connected:
        base_set = connected_sets[base]
        for extension_a in connected:
            if not base_set.issubset(connected_sets[extension_a]):
                continue
            for extension_b in connected:
                if not base_set.issubset(connected_sets[extension_b]):
                    continue
                union = tuple(sorted(connected_sets[extension_a] | connected_sets[extension_b]))
                if union not in connected_set:
                    continue
                for root in base:
                    h2_ordered_count += 1
                    slack = _h2_slack(z_values, base, extension_a, extension_b, union, root)
                    min_h2_ordered_slack = (
                        slack
                        if min_h2_ordered_slack is None
                        else min(min_h2_ordered_slack, slack)
                    )
                    if slack < 0 and first_failure is None:
                        first_failure = ConstraintFailure(
                            "h2_ordered_rectangle",
                            slack,
                            (
                                f"base={base}, extension_a={extension_a}, "
                                f"extension_b={extension_b}, union={union}, root={root}"
                            ),
                        )

    canonical_rectangles = enumerate_h2_rectangle_constraints(connected)
    min_h2_canonical_slack: Fraction | None = None
    for rectangle in canonical_rectangles:
        slack = _rectangle_slack(z_values, rectangle)
        min_h2_canonical_slack = (
            slack if min_h2_canonical_slack is None else min(min_h2_canonical_slack, slack)
        )
        if slack < 0 and first_failure is None:
            first_failure = ConstraintFailure(
                "h2_canonical_rectangle",
                slack,
                (
                    f"base={rectangle.base}, extension_a={rectangle.extension_a}, "
                    f"extension_b={rectangle.extension_b}, union={rectangle.union}, "
                    f"root={rectangle.root}"
                ),
            )

    return FeasibilityAudit(
        simplex_count=len(connected),
        z_variable_count=len(z_values),
        h1_count=h1_count,
        h2_ordered_count=h2_ordered_count,
        h2_canonical_nontrivial_count=len(canonical_rectangles),
        max_simplex_residual=max_simplex_residual,
        min_h1_slack=min_h1_slack if min_h1_slack is not None else Fraction(0),
        min_h2_ordered_slack=(
            min_h2_ordered_slack if min_h2_ordered_slack is not None else Fraction(0)
        ),
        min_h2_canonical_slack=(
            min_h2_canonical_slack if min_h2_canonical_slack is not None else Fraction(0)
        ),
        first_failure=first_failure,
    )


def mobius_masses(instance: SubdividedStar) -> dict[ZKey, Fraction]:
    topology = instance.topology
    connected = enumerate_connected_subsets(topology)
    connected_sets = {component: set(component) for component in connected}
    z_values = z_assignment(instance)
    masses: dict[ZKey, Fraction] = {}

    for root in topology.vertices:
        containing_root = [component for component in connected if root in component]
        for component in sorted(containing_root, key=lambda item: (-len(item), item)):
            value = z_values[(component, root)]
            component_set = connected_sets[component]
            for superset in containing_root:
                if len(superset) <= len(component):
                    continue
                if component_set.issubset(connected_sets[superset]):
                    value -= masses[(superset, root)]
            masses[(component, root)] = value
    return masses


def negative_masses(instance: SubdividedStar) -> tuple[tuple[ZKey, Fraction], ...]:
    return tuple(
        sorted(
            ((key, value) for key, value in mobius_masses(instance).items() if value < 0),
            key=lambda item: (item[0][0], item[0][1]),
        )
    )


def depth_projection(instance: SubdividedStar) -> tuple[Fraction, ...]:
    topology = instance.topology
    values = z_assignment(instance)
    depths: list[Fraction] = []
    for target in topology.vertices:
        total = Fraction(0)
        for source in topology.vertices:
            if source == target:
                continue
            path = tuple(sorted(path_between(topology, source, target)))
            total += values[(path, source)]
        depths.append(total)
    return tuple(depths)


def depth_dominant_audit(instance: SubdividedStar) -> DepthDominantAudit:
    topology = instance.topology
    target = depth_projection(instance)
    seen: set[tuple[int, ...]] = set()
    depth_vectors: list[tuple[int, ...]] = []
    certificate = ()

    for stt in enumerate_stts(topology, depth_base=0, max_count=100_000):
        vector = tuple(stt.depth[vertex] for vertex in topology.vertices)
        if vector in seen:
            continue
        seen.add(vector)
        depth_vectors.append(vector)
        if not certificate and all(Fraction(vector[index]) <= target[index] for index in range(topology.n)):
            certificate = ((Fraction(1), vector, stt.component_roots),)

    return DepthDominantAudit(
        depth_vectors=tuple(depth_vectors),
        target_depth=target,
        is_member=bool(certificate),
        certificate=certificate,
    )


def embedding_audits(
    branch_length_cases: Iterable[Iterable[int]] = DEFAULT_EMBEDDING_BRANCH_LENGTHS,
) -> tuple[EmbeddingAudit, ...]:
    audits: list[EmbeddingAudit] = []
    for branch_lengths in branch_length_cases:
        lengths = tuple(branch_lengths)
        instance = subdivided_four_star(lengths)
        masses = mobius_masses(instance)
        audits.append(
            EmbeddingAudit(
                branch_lengths=lengths,
                topology=instance.topology,
                branches=instance.branches,
                feasibility=feasibility_audit(instance),
                center_root_mass=masses[((0,), 0)],
                negative_masses=negative_masses(instance),
            )
        )
    return tuple(audits)


def write_report(path: Path = DEFAULT_REPORT) -> dict[str, object]:
    star = star4_instance()
    star_feasibility = feasibility_audit(star)
    star_masses = mobius_masses(star)
    star_negatives = negative_masses(star)
    star_depth = depth_projection(star)
    dominant = depth_dominant_audit(star)
    embeddings = embedding_audits()

    report = _render_report(
        star_feasibility=star_feasibility,
        star_negatives=star_negatives,
        star_center_mass=star_masses[((0,), 0)],
        star_depth=star_depth,
        dominant=dominant,
        embeddings=embeddings,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report, encoding="utf-8")
    return {
        "report": str(path),
        "star_feasible": star_feasibility.feasible,
        "star_center_mass": rational_to_string(star_masses[((0,), 0)]),
        "star_depth": tuple(rational_to_string(value) for value in star_depth),
        "depth_dominant_member": dominant.is_member,
        "embedding_cases": len(embeddings),
    }


def _star_center_value(active_branch_count: int) -> Fraction:
    if active_branch_count == 0:
        return Fraction(1)
    if active_branch_count == 1:
        return Fraction(1, 3)
    return Fraction(0)


def _h2_slack(
    values: dict[ZKey, Fraction],
    base: tuple[int, ...],
    extension_a: tuple[int, ...],
    extension_b: tuple[int, ...],
    union: tuple[int, ...],
    root: int,
) -> Fraction:
    return (
        values[(base, root)]
        - values[(extension_a, root)]
        - values[(extension_b, root)]
        + values[(union, root)]
    )


def _rectangle_slack(values: dict[ZKey, Fraction], rectangle: RectangleConstraint) -> Fraction:
    return _h2_slack(
        values,
        rectangle.base,
        rectangle.extension_a,
        rectangle.extension_b,
        rectangle.union,
        rectangle.root,
    )


def _render_report(
    *,
    star_feasibility: FeasibilityAudit,
    star_negatives: tuple[tuple[ZKey, Fraction], ...],
    star_center_mass: Fraction,
    star_depth: tuple[Fraction, ...],
    dominant: DepthDominantAudit,
    embeddings: tuple[EmbeddingAudit, ...],
) -> str:
    lines: list[str] = []
    lines.append("# STT v4 Star Audit v0")
    lines.append("")
    lines.append("## Definitions Used")
    lines.append("")
    lines.append("- Base tree for the obstruction: center `0` and leaves `1,2,3,4`.")
    lines.append("- Connected-subset first-hit variables are `z[I,r]`, with `r in I`.")
    lines.append("- H1 constraints checked exactly: simplex `sum_{r in I} z[I,r] = 1` and heredity `z[A,r] <= z[S,r]` for connected `S subset A` and `r in S`.")
    lines.append("- H2 extension rectangles checked exactly: `z[S,r] - z[A,r] - z[B,r] + z[A union B,r] >= 0` whenever all four sets are connected, `S subset A`, `S subset B`, and `r in S`.")
    lines.append("- Complete-form masses use the connected-set zeta inversion `z[I,r] = sum_{C superset I} m[C,r]`, over connected supersets containing `r`.")
    lines.append("- Depths use the strict-ancestor/root-depth-0 projection `d_v = sum_{u != v} z[P(u,v),u]`.")
    lines.append("")
    lines.append("## 4-Leaf Star H2 Feasibility")
    lines.append("")
    lines.append(_format_feasibility_table(("4-leaf star", star_feasibility)))
    lines.append("")
    lines.append("All simplex, H1 heredity, and H2 extension rectangle inequalities pass exactly over `Fraction` arithmetic.")
    lines.append("")
    lines.append("## Complete-Mobius Inversion")
    lines.append("")
    lines.append(f"- Center-root mass `m[{{0}},0]`: `{rational_to_string(star_center_mass)}`.")
    lines.append(f"- Negative recovered masses: `{len(star_negatives)}`.")
    for (component, root), value in star_negatives:
        lines.append(f"- `m[{list(component)},{root}] = {rational_to_string(value)}`")
    lines.append("")
    lines.append("There are four additional negative leaf-root masses, so the center-root obstruction is not the only negative recovered mass.")
    lines.append("")
    lines.append("## Depth Projection")
    lines.append("")
    lines.append("- Depth vector `(0,1,2,3,4)`: `" + _format_fraction_tuple(star_depth) + "`.")
    lines.append("- This is `d_0 = 8/3` and `d_i = 11/6` for each leaf `i`.")
    lines.append("")
    lines.append("## STT Dominant Status")
    lines.append("")
    lines.append(f"- Enumerated STT depth vectors on the 4-leaf star: `{len(dominant.depth_vectors)}`.")
    lines.append(f"- Dominant membership: `{'yes' if dominant.is_member else 'no'}`.")
    if dominant.certificate:
        weight, vector, component_roots = dominant.certificate[0]
        lines.append("- Exact convex-combination certificate:")
        lines.append(f"  - weight `{rational_to_string(weight)}` on depth vector `{vector}`.")
        lines.append(f"  - component roots `{_format_component_roots(component_roots)}`.")
        lines.append("")
        lines.append("Thus this exact z-system is a full first-hit-space obstruction, but not a depth-projection obstruction under root-depth-0 dominant convention.")
    else:
        lines.append("- No convex-combination certificate was found by the exact enumerator.")
    lines.append("")
    lines.append("## Degree-4 Embedding Samples")
    lines.append("")
    lines.append(_format_embedding_table(embeddings))
    lines.append("")
    lines.append("The sampled subdivided-star embeddings all satisfy H1/H2 exactly and keep `m[{0},0] = -1/3` as a nonrepresentability witness. These finite samples support the v4 embedding proof, but they are not by themselves a complete proof of the degree-at-least-4 theorem.")
    lines.append("")
    lines.append("## Recommendation")
    lines.append("")
    lines.append("- Promote: the 4-leaf star z-system is exactly H2-feasible and not complete-Mobius representable.")
    lines.append("- Promote with precision: the complete-Mobius obstruction includes `m[{0},0] = -1/3` plus four leaf-root negatives `-1/12`.")
    lines.append("- Weaken or qualify: do not call this example a depth-projection obstruction; its depth vector is already dominated by the integral center-root STT depth vector `(0,1,1,1,1)`.")
    lines.append("- Promote only as computational support: the sampled degree-4 embeddings pass exact H1/H2 checks and preserve a negative center-root mass, but finite samples do not prove the full theorem.")
    lines.append("")
    return "\n".join(lines)


def _format_feasibility_table(row: tuple[str, FeasibilityAudit]) -> str:
    name, audit = row
    headers = (
        "case",
        "simplex",
        "z vars",
        "H1",
        "H2 ordered",
        "H2 canonical",
        "simplex residual",
        "min H1",
        "min H2 ordered",
        "min H2 canonical",
    )
    values = (
        name,
        str(audit.simplex_count),
        str(audit.z_variable_count),
        str(audit.h1_count),
        str(audit.h2_ordered_count),
        str(audit.h2_canonical_nontrivial_count),
        rational_to_string(audit.max_simplex_residual),
        rational_to_string(audit.min_h1_slack),
        rational_to_string(audit.min_h2_ordered_slack),
        rational_to_string(audit.min_h2_canonical_slack),
    )
    return _markdown_table(headers, (values,))


def _format_embedding_table(embeddings: tuple[EmbeddingAudit, ...]) -> str:
    headers = (
        "branch lengths",
        "n",
        "connected",
        "z vars",
        "H1",
        "H2 ordered",
        "H2 canonical",
        "simplex residual",
        "min H1",
        "min H2 ordered",
        "min H2 canonical",
        "center mass",
        "negative masses",
    )
    rows = []
    for embedding in embeddings:
        audit = embedding.feasibility
        rows.append(
            (
                str(list(embedding.branch_lengths)),
                str(embedding.topology.n),
                str(audit.simplex_count),
                str(audit.z_variable_count),
                str(audit.h1_count),
                str(audit.h2_ordered_count),
                str(audit.h2_canonical_nontrivial_count),
                rational_to_string(audit.max_simplex_residual),
                rational_to_string(audit.min_h1_slack),
                rational_to_string(audit.min_h2_ordered_slack),
                rational_to_string(audit.min_h2_canonical_slack),
                rational_to_string(embedding.center_root_mass),
                str(len(embedding.negative_masses)),
            )
        )
    return _markdown_table(headers, tuple(rows))


def _markdown_table(headers: tuple[str, ...], rows: tuple[tuple[str, ...], ...]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def _format_fraction_tuple(values: tuple[Fraction, ...]) -> str:
    return "(" + ", ".join(rational_to_string(value) for value in values) + ")"


def _format_component_roots(
    component_roots: tuple[tuple[tuple[int, ...], int], ...]
) -> str:
    return "[" + ", ".join(f"({list(component)}, {root})" for component, root in component_roots) + "]"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m scripts.stt_checker.star_audit")
    parser.add_argument(
        "--report",
        type=Path,
        default=DEFAULT_REPORT,
        help="path for the markdown report",
    )
    args = parser.parse_args(argv)
    result = write_report(args.report)
    print(
        "wrote {report}: star_feasible={star_feasible} "
        "center_mass={star_center_mass} depth={star_depth} "
        "depth_dominant_member={depth_dominant_member} embedding_cases={embedding_cases}".format(
            **result
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
