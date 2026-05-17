"""Exact public SKZ-dual utilities for DS(k,1) scouting artifacts.

This module intentionally implements only the public path-dual variables named
in the handoff prompt:

* unordered pair variables R_{ij};
* ordered collinear-triplet variables Q_{ikj};
* capping rows R_{ij} <= Q_{ikj} + Q_{jki};
* frequency rows R_{ki} + sum_j Q_{ikj} <= w_i.

It does not import or encode H1/H2, refined-Z, path monotonicity, ancestry
transitivity, or LCA-separation constraints.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, permutations
from math import gcd
from pathlib import Path
from typing import Any, Iterable


Linear = dict[str, Fraction]


@dataclass(frozen=True)
class PublicConstraint:
    name: str
    family: str
    lhs: Linear
    rhs: Linear
    sense: str = "<="

    def as_le_zero(self) -> Linear:
        row = dict(self.lhs)
        add_scaled(row, self.rhs, Fraction(-1))
        return clean_linear(row)

    def to_json(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "family": self.family,
            "sense": self.sense,
            "lhs": linear_to_json(self.lhs),
            "rhs": linear_to_json(self.rhs),
        }


@dataclass(frozen=True)
class PublicDualModel:
    k: int
    vertices: tuple[str, ...]
    edges: tuple[tuple[str, str], ...]
    weights: dict[str, str]
    r_variables: tuple[str, ...]
    q_variables: tuple[str, ...]
    constraints: tuple[PublicConstraint, ...]

    @property
    def variables(self) -> tuple[str, ...]:
        return self.r_variables + self.q_variables

    def to_json(self) -> dict[str, Any]:
        return {
            "schema": "public_skz_dual_dsk1_v0",
            "k": self.k,
            "vertices": list(self.vertices),
            "edges": [list(edge) for edge in self.edges],
            "weights": dict(self.weights),
            "variable_domains": {
                "nonnegative": list(self.variables),
                "note": (
                    "Only public R/Q variables are generated. Nonnegativity is "
                    "a variable-domain condition, not an additional STT/H1/H2 row."
                ),
            },
            "variables": {
                "R": list(self.r_variables),
                "Q": list(self.q_variables),
            },
            "constraints": [constraint.to_json() for constraint in self.constraints],
            "constraint_counts": count_by_family(self.constraints),
        }


@dataclass(frozen=True)
class AugmentationLP:
    k: int
    parameters: tuple[str, ...]
    variables: tuple[str, ...]
    constraints: tuple[PublicConstraint, ...]
    objective: Linear
    notes: tuple[str, ...]

    def to_json(self) -> dict[str, Any]:
        return {
            "schema": "broot_augmentation_lp_v0",
            "k": self.k,
            "parameters": list(self.parameters),
            "variables": list(self.variables),
            "objective": linear_to_json(self.objective),
            "constraints": [constraint.to_json() for constraint in self.constraints],
            "constraint_counts": count_by_family(self.constraints),
            "notes": list(self.notes),
        }


def frac(value: int | str | Fraction) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


def add_scaled(target: Linear, source: Linear, scale: Fraction) -> None:
    for key, value in source.items():
        target[key] = target.get(key, Fraction(0)) + scale * value
        if target[key] == 0:
            del target[key]


def clean_linear(expr: Linear) -> Linear:
    return {key: value for key, value in expr.items() if value}


def linear_to_json(expr: Linear) -> dict[str, str]:
    return {key: rational_to_string(value) for key, value in sorted(expr.items())}


def rational_to_string(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def parse_rational_text(value: str) -> Fraction:
    return Fraction(value)


def count_by_family(constraints: Iterable[PublicConstraint]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for constraint in constraints:
        counts[constraint.family] = counts.get(constraint.family, 0) + 1
    return dict(sorted(counts.items()))


def dsk1_vertices(k: int) -> tuple[str, ...]:
    if k < 1:
        raise ValueError("k must be positive")
    return tuple([f"l{i}" for i in range(1, k + 1)] + ["a", "b", "r"])


def dsk1_edges(k: int) -> tuple[tuple[str, str], ...]:
    leaves = tuple(f"l{i}" for i in range(1, k + 1))
    return tuple([(leaf, "a") for leaf in leaves] + [("a", "b"), ("b", "r")])


def dsk1_weight_symbols(k: int) -> dict[str, str]:
    weights = {f"l{i}": f"u{i}" for i in range(1, k + 1)}
    weights["a"] = "alpha"
    weights["b"] = "beta"
    weights["r"] = "gamma"
    return weights


def adjacency(vertices: Iterable[str], edges: Iterable[tuple[str, str]]) -> dict[str, tuple[str, ...]]:
    raw: dict[str, list[str]] = {vertex: [] for vertex in vertices}
    for u, v in edges:
        raw[u].append(v)
        raw[v].append(u)
    return {vertex: tuple(sorted(neighbors)) for vertex, neighbors in raw.items()}


def path_between(
    adj: dict[str, tuple[str, ...]], source: str, target: str
) -> tuple[str, ...]:
    if source == target:
        return (source,)
    parent: dict[str, str | None] = {source: None}
    queue: deque[str] = deque([source])
    while queue and target not in parent:
        current = queue.popleft()
        for neighbor in adj[current]:
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)
    if target not in parent:
        raise ValueError("tree is disconnected")
    result = [target]
    while result[-1] != source:
        previous = parent[result[-1]]
        if previous is None:
            raise ValueError("internal path reconstruction failure")
        result.append(previous)
    return tuple(reversed(result))


def vertex_order(vertices: Iterable[str]) -> dict[str, int]:
    return {vertex: index for index, vertex in enumerate(vertices)}


def ordered_pair_key(u: str, v: str, order: dict[str, int]) -> tuple[str, str]:
    if u == v:
        raise ValueError("R endpoints must be distinct")
    return (u, v) if order[u] < order[v] else (v, u)


def r_name(u: str, v: str, order: dict[str, int]) -> str:
    x, y = ordered_pair_key(u, v, order)
    return f"R[{x},{y}]"


def q_name(i: str, k: str, j: str) -> str:
    if len({i, k, j}) != 3:
        raise ValueError("Q indices must be distinct")
    return f"Q[{i},{k},{j}]"


def public_dual_model_for_tree(
    vertices: tuple[str, ...],
    edges: tuple[tuple[str, str], ...],
    weights: dict[str, str],
    k: int,
) -> PublicDualModel:
    order = vertex_order(vertices)
    adj = adjacency(vertices, edges)
    r_variables = tuple(
        r_name(u, v, order) for u, v in combinations(vertices, 2)
    )
    q_set: set[str] = set()
    for i in vertices:
        for j in vertices:
            if i == j:
                continue
            path = path_between(adj, i, j)
            for middle in path[1:-1]:
                q_set.add(q_name(i, middle, j))
    q_variables = tuple(sorted(q_set, key=_variable_sort_key))

    constraints: list[PublicConstraint] = []
    for i, j in combinations(vertices, 2):
        path = path_between(adj, i, j)
        for middle in path[1:-1]:
            lhs = {
                r_name(i, j, order): Fraction(1),
            }
            rhs = {
                q_name(i, middle, j): Fraction(1),
                q_name(j, middle, i): Fraction(1),
            }
            constraints.append(
                PublicConstraint(
                    name=f"cap:{r_name(i, j, order)}@{middle}",
                    family="capping",
                    lhs=lhs,
                    rhs=rhs,
                )
            )

    for i in vertices:
        for middle in vertices:
            if i == middle:
                continue
            lhs: Linear = {r_name(i, middle, order): Fraction(1)}
            for j in vertices:
                if j in (i, middle):
                    continue
                path = path_between(adj, i, j)
                if middle in path[1:-1]:
                    lhs[q_name(i, middle, j)] = lhs.get(
                        q_name(i, middle, j), Fraction(0)
                    ) + Fraction(1)
            constraints.append(
                PublicConstraint(
                    name=f"freq:{i}|{middle}",
                    family="frequency",
                    lhs=lhs,
                    rhs={weights[i]: Fraction(1)},
                )
            )

    return PublicDualModel(
        k=k,
        vertices=vertices,
        edges=edges,
        weights=weights,
        r_variables=r_variables,
        q_variables=q_variables,
        constraints=tuple(constraints),
    )


def generate_public_dual_dsk1(k: int) -> PublicDualModel:
    vertices = dsk1_vertices(k)
    return public_dual_model_for_tree(
        vertices=vertices,
        edges=dsk1_edges(k),
        weights=dsk1_weight_symbols(k),
        k=k,
    )


def star_vertices(k: int) -> tuple[str, ...]:
    return tuple([f"l{i}" for i in range(1, k + 1)] + ["a"])


def star_edges(k: int) -> tuple[tuple[str, str], ...]:
    return tuple((f"l{i}", "a") for i in range(1, k + 1))


def star_weight_symbols(k: int) -> dict[str, str]:
    weights = {f"l{i}": f"u{i}" for i in range(1, k + 1)}
    weights["a"] = "alpha"
    return weights


def generate_public_dual_star(k: int) -> PublicDualModel:
    vertices = star_vertices(k)
    return public_dual_model_for_tree(
        vertices=vertices,
        edges=star_edges(k),
        weights=star_weight_symbols(k),
        k=k,
    )


def star_depth_vectors(k: int) -> tuple[dict[str, int], ...]:
    """Enumerate exact root-depth-0 STT depth vectors for a k-leaf star."""

    leaves = [f"l{i}" for i in range(1, k + 1)]
    seen: dict[tuple[tuple[str, int], ...], dict[str, int]] = {}
    for prefix_len in range(0, k + 1):
        for prefix in permutations(leaves, prefix_len):
            prefix_set = set(prefix)
            depths: dict[str, int] = {}
            for index, leaf in enumerate(prefix):
                depths[leaf] = index
            depths["a"] = prefix_len
            for leaf in leaves:
                if leaf not in prefix_set:
                    depths[leaf] = prefix_len + 1
            seen[tuple(sorted(depths.items()))] = depths
    return tuple(seen[key] for key in sorted(seen))


def dsk1_tree_depth_vectors(k: int) -> tuple[dict[str, int], ...]:
    """Enumerate all recursive STT depth vectors for DS(k,1), root-depth 0."""

    vertices = dsk1_vertices(k)
    adj = adjacency(vertices, dsk1_edges(k))
    seen: dict[tuple[tuple[str, int], ...], dict[str, int]] = {}

    def components_after_removing(component: tuple[str, ...], root: str) -> tuple[tuple[str, ...], ...]:
        remaining = set(component)
        remaining.remove(root)
        comps: list[tuple[str, ...]] = []
        while remaining:
            start = min(remaining)
            stack = [start]
            found: set[str] = set()
            remaining.remove(start)
            while stack:
                current = stack.pop()
                found.add(current)
                for neighbor in adj[current]:
                    if neighbor in remaining:
                        remaining.remove(neighbor)
                        stack.append(neighbor)
            comps.append(tuple(sorted(found, key=vertex_order(vertices).__getitem__)))
        return tuple(comps)

    def rec(component: tuple[str, ...], depth: int) -> Iterable[dict[str, int]]:
        if not component:
            yield {}
            return
        for root in component:
            child_components = components_after_removing(component, root)
            child_options = [tuple(rec(child, depth + 1)) for child in child_components]
            if not child_options:
                yield {root: depth}
                continue
            for product_choice in cartesian_product(child_options):
                depths = {root: depth}
                for child_depths in product_choice:
                    depths.update(child_depths)
                yield depths

    for depths in rec(vertices, 0):
        seen[tuple(sorted(depths.items()))] = depths
    return tuple(seen[key] for key in sorted(seen))


def cartesian_product(groups: list[tuple[dict[str, int], ...]]) -> Iterable[tuple[dict[str, int], ...]]:
    if not groups:
        yield ()
        return
    first, *rest = groups
    for item in first:
        for suffix in cartesian_product(rest):
            yield (item,) + suffix


def depth_cost(depths: dict[str, int]) -> Linear:
    result: Linear = {}
    for vertex, depth in depths.items():
        if depth == 0:
            continue
        if vertex.startswith("l"):
            symbol = f"u{vertex[1:]}"
        elif vertex == "a":
            symbol = "alpha"
        elif vertex == "b":
            symbol = "beta"
        elif vertex == "r":
            symbol = "gamma"
        else:
            raise ValueError(f"unknown vertex {vertex}")
        result[symbol] = result.get(symbol, Fraction(0)) + Fraction(depth)
    return clean_linear(result)


def public_objective_for_model(model: PublicDualModel) -> Linear:
    return {name: Fraction(1) for name in model.r_variables}


def is_star_variable(name: str, k: int) -> bool:
    vertices = set(star_vertices(k))
    indices = variable_indices(name)
    return all(index in vertices for index in indices)


def variable_indices(name: str) -> tuple[str, ...]:
    inside = name[name.index("[") + 1 : name.index("]")]
    return tuple(part.strip() for part in inside.split(","))


def build_broot_augmentation_lp(k: int) -> AugmentationLP:
    model = generate_public_dual_dsk1(k)
    aug_variables = tuple(
        variable for variable in model.variables if not is_star_variable(variable, k)
    )
    aug_set = set(aug_variables)
    constraints: list[PublicConstraint] = []

    for variable in aug_variables:
        constraints.append(
            PublicConstraint(
                name=f"nonneg:{variable}",
                family="nonnegativity",
                lhs={},
                rhs={variable: Fraction(1)},
            )
        )

    for constraint in model.constraints:
        row = constraint.as_le_zero()
        kept = {var: coeff for var, coeff in row.items() if var in aug_set}
        dropped = {
            var: coeff
            for var, coeff in row.items()
            if var not in aug_set and (var.startswith("R[") or var.startswith("Q["))
        }
        if dropped:
            if constraint.family == "frequency":
                # The only star-side frequency consumption retained by the
                # augmentation interface is the leaf/a residual s_i.
                parts = constraint.name.split(":", 1)[1].split("|")
                endpoint, middle = parts[0], parts[1]
                if endpoint.startswith("l") and middle == "a":
                    kept[f"s{endpoint[1:]}"] = kept.get(
                        f"s{endpoint[1:]}", Fraction(0)
                    ) - Fraction(1)
                else:
                    continue
            else:
                continue
        else:
            for symbol, coeff in row.items():
                if not (symbol.startswith("R[") or symbol.startswith("Q[")):
                    kept[symbol] = kept.get(symbol, Fraction(0)) + coeff
        if not kept:
            continue
        constraints.append(
            PublicConstraint(
                name=f"aug:{constraint.name}",
                family=f"augmented_{constraint.family}",
                lhs={var: coeff for var, coeff in kept.items() if coeff > 0},
                rhs={var: -coeff for var, coeff in kept.items() if coeff < 0},
            )
        )

    objective = {
        variable: Fraction(1) for variable in aug_variables if variable.startswith("R[")
    }
    params = tuple([f"u{i}" for i in range(1, k + 1)] + ["alpha", "beta", "gamma"] + [f"s{i}" for i in range(1, k + 1)])
    return AugmentationLP(
        k=k,
        parameters=params,
        variables=aug_variables,
        constraints=tuple(constraints),
        objective=objective,
        notes=(
            "The LP is the public-dual augmentation after an optimal public-dual star certificate on {a,l_i}.",
            "Only the star leaf/a frequency residuals s_i are imported from the star face.",
            "The b vertex keeps its public frequency capacity beta; the target bound is independent of beta.",
        ),
    )


def residual_star_system_cases(k: int) -> tuple[dict[str, Any], ...]:
    """Return exact projected residual systems for star Bellman chambers."""

    model = generate_public_dual_star(k)
    variables = tuple(model.variables)
    objective = public_objective_for_model(model)
    costs = [(depths, depth_cost(depths)) for depths in star_depth_vectors(k)]
    cases: list[dict[str, Any]] = []
    keep = tuple([f"u{i}" for i in range(1, k + 1)] + ["alpha"] + [f"s{i}" for i in range(1, k + 1)])

    for index, (depths, cost) in enumerate(costs):
        inequalities: list[Linear] = []
        for variable in variables:
            inequalities.append({variable: Fraction(-1)})
        inequalities.extend(constraint.as_le_zero() for constraint in model.constraints)
        for other_depths, other_cost in costs:
            if other_depths == depths:
                continue
            row = dict(cost)
            add_scaled(row, other_cost, Fraction(-1))
            inequalities.append(clean_linear(row))
        equality = dict(objective)
        add_scaled(equality, cost, Fraction(-1))
        inequalities.append(equality)
        inequalities.append({key: -value for key, value in equality.items()})
        for i in range(1, k + 1):
            lhs: Linear = {f"s{i}": Fraction(1), f"R[l{i},a]": Fraction(1)}
            for j in range(1, k + 1):
                if i == j:
                    continue
                lhs[f"Q[l{i},a,l{j}]"] = lhs.get(
                    f"Q[l{i},a,l{j}]", Fraction(0)
                ) + Fraction(1)
            lhs[f"u{i}"] = lhs.get(f"u{i}", Fraction(0)) - Fraction(1)
            inequalities.append(clean_linear(lhs))
            inequalities.append({key: -value for key, value in lhs.items()})
        for param in [f"u{i}" for i in range(1, k + 1)] + ["alpha"]:
            inequalities.append({param: Fraction(-1)})

        projected, status = fourier_motzkin_project(
            inequalities,
            eliminate=variables,
            keep=keep,
            max_rows=20000 if k <= 2 else 40000,
        )
        cases.append(
            {
                "case_id": f"star_chamber_{index}",
                "depths": dict(sorted(depths.items())),
                "cost": linear_to_json(cost),
                "projected_residual_inequalities": [
                    linear_to_json(row) for row in projected
                ],
                "projection_status": status,
            }
        )
    return tuple(cases)


def augmentation_projected_cuts(k: int, max_rows: int) -> dict[str, Any]:
    lp = build_broot_augmentation_lp(k)
    inequalities: list[Linear] = [constraint.as_le_zero() for constraint in lp.constraints]
    value_row: Linear = {"t": Fraction(1)}
    add_scaled(value_row, lp.objective, Fraction(-1))
    inequalities.append(clean_linear(value_row))
    keep = tuple(lp.parameters + ("t",))
    projected, status = fourier_motzkin_project(
        inequalities,
        eliminate=lp.variables,
        keep=keep,
        max_rows=max_rows,
    )
    cuts = []
    side_conditions = []
    for row in projected:
        coeff_t = row.get("t", Fraction(0))
        if coeff_t > 0:
            scale = Fraction(1, 1) / coeff_t
            expr = {
                key: -value * scale
                for key, value in row.items()
                if key != "t" and value
            }
            cuts.append(
                {
                    "inequality": f"t <= {format_linear(expr)}",
                    "expression": linear_to_json(expr),
                    "classification": classify_cut(expr, k),
                }
            )
        else:
            side_conditions.append(linear_to_json(row))
    return {
        "lp": lp.to_json(),
        "projection_status": status,
        "cuts": dedupe_cut_dicts(cuts),
        "side_conditions": side_conditions,
    }


def classify_cut(expr: Linear, k: int) -> str:
    s_support = sorted(key for key in expr if key.startswith("s") and expr[key])
    u_support = sorted(key for key in expr if key.startswith("u") and expr[key])
    non_s = sorted(key for key in expr if not key.startswith("s") and expr[key])
    if not expr:
        return "trivial/nonnegativity"
    if len(s_support) == 1 and all(key in {s_support[0], "alpha", "beta", "gamma"} for key in expr):
        return "singleton"
    if not s_support:
        return "global a/r Bellman-like"
    if len(s_support) >= 2:
        return "genuine subset-level"
    if len(u_support) >= 2 or len(non_s) >= 3:
        return "global a/r Bellman-like"
    return "singleton"


def dedupe_cut_dicts(cuts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[tuple[str, str], ...]] = set()
    result: list[dict[str, Any]] = []
    for cut in cuts:
        key = tuple(sorted(cut["expression"].items()))
        if key in seen:
            continue
        seen.add(key)
        result.append(cut)
    result.sort(key=lambda item: (item["classification"], item["inequality"]))
    return result


def format_linear(expr: Linear) -> str:
    if not expr:
        return "0"
    parts = []
    for key, value in sorted(expr.items()):
        if value == 1:
            parts.append(key)
        elif value == -1:
            parts.append(f"-{key}")
        else:
            parts.append(f"{rational_to_string(value)}*{key}")
    text = " + ".join(parts)
    return text.replace("+ -", "- ")


def fourier_motzkin_project(
    inequalities: Iterable[Linear],
    eliminate: Iterable[str],
    keep: Iterable[str],
    max_rows: int = 20000,
) -> tuple[tuple[Linear, ...], str]:
    keep_set = set(keep)
    rows = tuple(normalize_inequality(row) for row in inequalities if row)
    rows = dedupe_rows(rows)
    status = "complete"
    remaining = list(eliminate)
    while remaining:
        variable = choose_elimination_variable(rows, remaining)
        remaining.remove(variable)
        positive: list[Linear] = []
        negative: list[Linear] = []
        zero: list[Linear] = []
        for row in rows:
            coeff = row.get(variable, Fraction(0))
            if coeff > 0:
                positive.append(row)
            elif coeff < 0:
                negative.append(row)
            else:
                zero.append(row)
        next_rows: list[Linear] = [strip_variable(row, variable) for row in zero]
        for upper in positive:
            a_pos = upper[variable]
            upper_rest = strip_variable(upper, variable)
            for lower in negative:
                a_neg = lower[variable]
                lower_rest = strip_variable(lower, variable)
                combined: Linear = {}
                add_scaled(combined, upper_rest, Fraction(1, 1) / a_pos)
                add_scaled(combined, lower_rest, Fraction(-1, 1) / a_neg)
                combined = normalize_inequality(combined)
                if combined:
                    next_rows.append(combined)
                if len(next_rows) > max_rows:
                    status = f"aborted_row_limit_after_eliminating_{variable}"
                    projected = [
                        project_to_keep(row, keep_set)
                        for row in next_rows
                        if only_uses(row, keep_set)
                    ]
                    return dedupe_rows(projected), status
        rows = dedupe_rows(next_rows)
        if len(rows) > max_rows:
            status = f"aborted_row_limit_after_eliminating_{variable}"
            break
    projected = [project_to_keep(row, keep_set) for row in rows if only_uses(row, keep_set)]
    return dedupe_rows(projected), status


def choose_elimination_variable(rows: tuple[Linear, ...], candidates: list[str]) -> str:
    best: tuple[int, int, str] | None = None
    for variable in candidates:
        positive = 0
        negative = 0
        zero = 0
        for row in rows:
            coeff = row.get(variable, Fraction(0))
            if coeff > 0:
                positive += 1
            elif coeff < 0:
                negative += 1
            else:
                zero += 1
        estimate = zero + positive * negative
        touched = positive + negative
        key = (estimate, touched, variable)
        if best is None or key < best:
            best = key
    if best is None:
        raise ValueError("no elimination candidates")
    return best[2]


def only_uses(row: Linear, allowed: set[str]) -> bool:
    return all(key in allowed for key in row)


def project_to_keep(row: Linear, keep: set[str]) -> Linear:
    return {key: value for key, value in row.items() if key in keep and value}


def strip_variable(row: Linear, variable: str) -> Linear:
    return {key: value for key, value in row.items() if key != variable and value}


def dedupe_rows(rows: Iterable[Linear]) -> tuple[Linear, ...]:
    unique: dict[tuple[tuple[str, Fraction], ...], Linear] = {}
    for row in rows:
        normalized = normalize_inequality(row)
        if normalized:
            unique[linear_key(normalized)] = normalized
    return tuple(unique[key] for key in sorted(unique))


def linear_key(row: Linear) -> tuple[tuple[str, Fraction], ...]:
    return tuple(sorted(row.items()))


def normalize_inequality(row: Linear) -> Linear:
    cleaned = clean_linear(row)
    if not cleaned:
        return {}
    denominators = [value.denominator for value in cleaned.values()]
    lcm = 1
    for denominator in denominators:
        lcm = lcm * denominator // gcd(lcm, denominator)
    integers = {key: value.numerator * (lcm // value.denominator) for key, value in cleaned.items()}
    common = 0
    for value in integers.values():
        common = gcd(common, abs(value))
    if common == 0:
        return {}
    return {key: Fraction(value // common, 1) for key, value in integers.items() if value}


def _variable_sort_key(name: str) -> tuple[str, tuple[str, ...]]:
    return (name[0], variable_indices(name))


def matrix_json_from_lp(lp: AugmentationLP) -> dict[str, Any]:
    rows = []
    for constraint in lp.constraints:
        row = constraint.as_le_zero()
        rows.append(
            {
                "name": constraint.name,
                "family": constraint.family,
                "coefficients": linear_to_json(
                    {var: row[var] for var in lp.variables if row.get(var)}
                ),
                "rhs": linear_to_json(
                    {param: -row[param] for param in lp.parameters if row.get(param)}
                ),
            }
        )
    return {
        "variables": list(lp.variables),
        "parameters": list(lp.parameters),
        "objective": linear_to_json(lp.objective),
        "rows": rows,
    }


def solve_square_system(
    equations: list[list[Fraction]], rhs: list[Fraction]
) -> list[Fraction] | None:
    n = len(rhs)
    if any(len(row) != n for row in equations):
        raise ValueError("solve_square_system requires an n by n matrix")
    matrix = [list(row) + [rhs_value] for row, rhs_value in zip(equations, rhs)]
    rank = 0
    for col in range(n):
        pivot = None
        for row in range(rank, n):
            if matrix[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            return None
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][col]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for row in range(n):
            if row == rank:
                continue
            factor = matrix[row][col]
            if factor:
                matrix[row] = [
                    current - factor * base
                    for current, base in zip(matrix[row], matrix[rank])
                ]
        rank += 1
    return [matrix[row][-1] for row in range(n)]


def cone_membership_certificate(
    generators: list[Linear],
    target: Linear,
    variables: tuple[str, ...],
) -> dict[str, Any] | None:
    """Find a small exact conic certificate target=sum lambda_i generator_i."""

    n = len(variables)
    target_vec = [target.get(var, Fraction(0)) for var in variables]
    indexed = list(enumerate(generators))
    for size in range(1, min(n, len(indexed)) + 1):
        for subset in combinations(indexed, size):
            # Pad to a square system by selecting independent coordinate rows.
            cols = [[row.get(var, Fraction(0)) for _, row in subset] for var in variables]
            for coord_subset in combinations(range(n), size):
                square = [[cols[coord][col] for col in range(size)] for coord in coord_subset]
                sub_rhs = [target_vec[coord] for coord in coord_subset]
                solution = solve_square_system(square, sub_rhs)
                if solution is None:
                    continue
                if any(value < 0 for value in solution):
                    continue
                reconstructed = [Fraction(0) for _ in variables]
                for coeff, (_, row) in zip(solution, subset):
                    for idx, var in enumerate(variables):
                        reconstructed[idx] += coeff * row.get(var, Fraction(0))
                if reconstructed == target_vec:
                    return {
                        "rows": [
                            {
                                "index": row_index,
                                "multiplier": rational_to_string(coeff),
                                "row": linear_to_json(row),
                            }
                            for coeff, (row_index, row) in zip(solution, subset)
                            if coeff
                        ]
                    }
    if not target:
        return {"rows": []}
    return None


def chamber_rows_for_depth(
    selected_cost: Linear,
    all_costs: Iterable[Linear],
    parameters: Iterable[str],
) -> list[Linear]:
    rows = [{param: Fraction(-1)} for param in parameters]
    for other in all_costs:
        if other == selected_cost:
            continue
        row = dict(selected_cost)
        add_scaled(row, other, Fraction(-1))
        rows.append(clean_linear(row))
    return rows
