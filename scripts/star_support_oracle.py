"""Exact public-star support oracle for the DS(k,1) public-LP bridge.

This module implements the corrected public-star edge-cover network described
in the mixed-support audit prompt.  It uses only the public star certificate
items:

* singleton items ``s_i = R_{ia}`` with capacity ``min(alpha, u_i)``;
* pair items ``e_ij = R_{ij}`` with capacity ``min(u_i, u_j)``.

Leaves send flow to incident singleton/pair items, and items send flow to the
sink.  The max-flow value is the corrected ``F(L)`` min-cut value.  For
nonnegative support multipliers ``lambda_T``, item costs are

``cost(s_i)=A_i(lambda)``, ``cost(e_ij)=B_ij(lambda)``.

The support oracle is

``Phi(lambda)=sum_i A_i(lambda) u_i - MC_lambda(F(L))``.

The code is intentionally finite/exact.  It does not claim public-LP exactness
or an all-k theorem from the k=3 chamber data.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import sys
from typing import Any, Iterable, Mapping, Sequence

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.stt_checker.rationals import parse_rational, rational_to_string


Pair = tuple[int, int]
Support = tuple[int, ...]


@dataclass(frozen=True)
class EdgeCoverItem:
    """A public-star edge-cover item."""

    name: str
    kind: str
    support: Support
    capacity: Fraction


@dataclass(frozen=True)
class MinCostFlowResult:
    value: Fraction
    cost: Fraction
    item_flow: dict[str, Fraction]
    augmentations: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class SupportOracleResult:
    k: int
    u: tuple[Fraction, ...]
    alpha: Fraction
    lambdas: dict[Support, Fraction]
    A: tuple[Fraction, ...]
    B: dict[Pair, Fraction]
    F: Fraction
    min_cut_F: Fraction
    max_flow_F: Fraction
    min_cost: Fraction
    phi: Fraction
    item_flow: dict[str, Fraction]
    direct_lp_min_cost: Fraction | None = None
    direct_lp_phi: Fraction | None = None
    direct_lp_vertex_count: int | None = None


def left_vertices(k: int) -> tuple[int, ...]:
    return tuple(range(k))


def pair_supports(k: int) -> tuple[Pair, ...]:
    return tuple(combinations(left_vertices(k), 2))


def singleton_name(i: int) -> str:
    return f"s{i + 1}"


def pair_name(i: int, j: int) -> str:
    a, b = sorted((i, j))
    return f"e{a + 1}{b + 1}"


def support_label(support: Support) -> str:
    return "{" + ",".join(f"l{i + 1}" for i in support) + "}"


def parse_fraction_list(text: str, expected: int, field: str) -> tuple[Fraction, ...]:
    values = tuple(parse_rational(part.strip(), f"{field}[{index}]") for index, part in enumerate(text.split(",")))
    if len(values) != expected:
        raise ValueError(f"{field}: expected {expected} comma-separated rationals")
    return values


def parse_pair_lambdas(k: int, text: str) -> dict[Support, Fraction]:
    values = parse_fraction_list(text, len(pair_supports(k)), "lambda")
    return {pair: value for pair, value in zip(pair_supports(k), values) if value}


def rational_payload(value: Fraction) -> str:
    return rational_to_string(value)


def edge_cover_items(k: int, u: Sequence[Fraction], alpha: Fraction) -> tuple[EdgeCoverItem, ...]:
    if len(u) != k:
        raise ValueError("u length must equal k")
    items: list[EdgeCoverItem] = []
    for i in left_vertices(k):
        items.append(
            EdgeCoverItem(
                name=singleton_name(i),
                kind="singleton",
                support=(i,),
                capacity=min(alpha, u[i]),
            )
        )
    for i, j in pair_supports(k):
        items.append(
            EdgeCoverItem(
                name=pair_name(i, j),
                kind="pair",
                support=(i, j),
                capacity=min(u[i], u[j]),
            )
        )
    return tuple(items)


def powerset(values: Iterable[int]) -> tuple[tuple[int, ...], ...]:
    items = tuple(values)
    return tuple(
        tuple(items[index] for index in range(len(items)) if mask & (1 << index))
        for mask in range(1 << len(items))
    )


def min_cut_F_value(
    k: int, u: Sequence[Fraction], alpha: Fraction
) -> tuple[Fraction, tuple[tuple[int, ...], ...]]:
    """Return the corrected ``F(L)`` min-cut value and active cuts."""

    items = edge_cover_items(k, u, alpha)
    values: list[tuple[tuple[int, ...], Fraction]] = []
    for active in powerset(left_vertices(k)):
        active_set = set(active)
        residual = sum((u[i] for i in left_vertices(k) if i not in active_set), Fraction(0))
        crossing_items = sum(
            (item.capacity for item in items if active_set.intersection(item.support)),
            Fraction(0),
        )
        values.append((active, residual + crossing_items))
    optimum = min(value for _active, value in values)
    return optimum, tuple(active for active, value in values if value == optimum)


def source_deletion_F_value(
    k: int,
    u: Sequence[Fraction],
    alpha: Fraction,
    deleted_sources: Iterable[int],
) -> Fraction:
    """Corrected source-deletion formula from the previous audit."""

    deleted = set(deleted_sources)
    items = edge_cover_items(k, u, alpha)
    best: Fraction | None = None
    for active in powerset(left_vertices(k)):
        active_set = set(active)
        residual = sum(
            (
                u[i]
                for i in left_vertices(k)
                if i not in active_set and i not in deleted
            ),
            Fraction(0),
        )
        crossing_items = sum(
            (item.capacity for item in items if active_set.intersection(item.support)),
            Fraction(0),
        )
        value = residual + crossing_items
        if best is None or value < best:
            best = value
    if best is None:
        raise ValueError("empty source-deletion branch set")
    return best


def source_deletion_delta(
    k: int,
    u: Sequence[Fraction],
    alpha: Fraction,
    deleted_sources: Iterable[int],
) -> Fraction:
    F, _active = min_cut_F_value(k, u, alpha)
    return F - source_deletion_F_value(k, u, alpha, deleted_sources)


def support_coefficients(
    k: int, lambdas: Mapping[Support, Fraction]
) -> tuple[tuple[Fraction, ...], dict[Pair, Fraction]]:
    A = [Fraction(0) for _ in left_vertices(k)]
    B = {pair: Fraction(0) for pair in pair_supports(k)}
    for raw_support, value in lambdas.items():
        support = tuple(sorted(raw_support))
        if value < 0:
            raise ValueError("support multipliers must be nonnegative")
        for i in support:
            if i < 0 or i >= k:
                raise ValueError(f"support index out of range: {support}")
            A[i] += value
        for i, j in pair_supports(k):
            if i in support and j in support:
                B[(i, j)] += value
    return tuple(A), B


def item_costs_from_lambdas(
    k: int, lambdas: Mapping[Support, Fraction]
) -> tuple[tuple[Fraction, ...], dict[Pair, Fraction], dict[str, Fraction]]:
    A, B = support_coefficients(k, lambdas)
    costs: dict[str, Fraction] = {}
    for i in left_vertices(k):
        costs[singleton_name(i)] = A[i]
    for i, j in pair_supports(k):
        costs[pair_name(i, j)] = B[(i, j)]
    return A, B, costs


class _ResidualEdge:
    __slots__ = ("to", "rev", "cap", "cost", "initial_cap", "label")

    def __init__(
        self,
        to: int,
        rev: int,
        cap: Fraction,
        cost: Fraction,
        label: str | None = None,
    ) -> None:
        self.to = to
        self.rev = rev
        self.cap = cap
        self.cost = cost
        self.initial_cap = cap
        self.label = label


class _ResidualNetwork:
    def __init__(self, node_count: int) -> None:
        self.graph: list[list[_ResidualEdge]] = [[] for _ in range(node_count)]
        self.labeled_edges: list[_ResidualEdge] = []

    def add_edge(
        self,
        source: int,
        target: int,
        capacity: Fraction,
        cost: Fraction = Fraction(0),
        label: str | None = None,
    ) -> None:
        forward = _ResidualEdge(target, len(self.graph[target]), capacity, cost, label)
        reverse = _ResidualEdge(source, len(self.graph[source]), Fraction(0), -cost)
        self.graph[source].append(forward)
        self.graph[target].append(reverse)
        if label is not None:
            self.labeled_edges.append(forward)


def min_cost_flow_value(
    k: int,
    u: Sequence[Fraction],
    alpha: Fraction,
    item_costs: Mapping[str, Fraction],
    target_value: Fraction | None = None,
) -> MinCostFlowResult:
    """Solve the edge-cover min-cost flow exactly by shortest augmenting paths."""

    items = edge_cover_items(k, u, alpha)
    total_leaf_supply = sum(u, Fraction(0))
    total_item_capacity = sum((item.capacity for item in items), Fraction(0))
    infinite_capacity = total_leaf_supply + total_item_capacity + Fraction(1)

    source = 0
    leaf_offset = 1
    item_offset = leaf_offset + k
    sink = item_offset + len(items)
    network = _ResidualNetwork(sink + 1)

    for i in left_vertices(k):
        network.add_edge(source, leaf_offset + i, u[i])

    item_index = {item.name: item_offset + index for index, item in enumerate(items)}
    for item in items:
        for i in item.support:
            network.add_edge(leaf_offset + i, item_index[item.name], infinite_capacity)
        network.add_edge(
            item_index[item.name],
            sink,
            item.capacity,
            item_costs.get(item.name, Fraction(0)),
            label=item.name,
        )

    flow = Fraction(0)
    cost = Fraction(0)
    augmentations: list[dict[str, Any]] = []
    node_count = sink + 1

    while target_value is None or flow < target_value:
        dist: list[Fraction | None] = [None for _ in range(node_count)]
        parent: list[tuple[int, int] | None] = [None for _ in range(node_count)]
        dist[source] = Fraction(0)
        changed = True
        for _ in range(node_count - 1):
            if not changed:
                break
            changed = False
            for node, edges in enumerate(network.graph):
                if dist[node] is None:
                    continue
                for edge_index, edge in enumerate(edges):
                    if edge.cap <= 0:
                        continue
                    candidate = dist[node] + edge.cost
                    if dist[edge.to] is None or candidate < dist[edge.to]:
                        dist[edge.to] = candidate
                        parent[edge.to] = (node, edge_index)
                        changed = True
        if parent[sink] is None:
            break

        path: list[tuple[int, int]] = []
        current = sink
        bottleneck: Fraction | None = None
        while current != source:
            step = parent[current]
            if step is None:
                raise RuntimeError("broken residual parent chain")
            previous, edge_index = step
            edge = network.graph[previous][edge_index]
            path.append((previous, edge_index))
            bottleneck = edge.cap if bottleneck is None else min(bottleneck, edge.cap)
            current = previous
        if bottleneck is None:
            raise RuntimeError("empty augmenting path")
        if target_value is not None:
            bottleneck = min(bottleneck, target_value - flow)
        if bottleneck <= 0:
            break

        for previous, edge_index in path:
            edge = network.graph[previous][edge_index]
            reverse = network.graph[edge.to][edge.rev]
            edge.cap -= bottleneck
            reverse.cap += bottleneck

        flow += bottleneck
        path_cost = dist[sink]
        if path_cost is None:
            raise RuntimeError("missing path distance")
        cost += bottleneck * path_cost
        augmentations.append(
            {
                "amount": rational_payload(bottleneck),
                "path_cost": rational_payload(path_cost),
            }
        )

    if target_value is not None and flow != target_value:
        raise ValueError(
            f"target flow {rational_payload(target_value)} is infeasible; reached {rational_payload(flow)}"
        )

    item_flow = {
        edge.label: edge.initial_cap - edge.cap
        for edge in network.labeled_edges
        if edge.label is not None
    }
    return MinCostFlowResult(flow, cost, item_flow, tuple(augmentations))


def max_flow_value(k: int, u: Sequence[Fraction], alpha: Fraction) -> Fraction:
    zero_costs = {item.name: Fraction(0) for item in edge_cover_items(k, u, alpha)}
    return min_cost_flow_value(k, u, alpha, zero_costs).value


def support_oracle(
    k: int,
    u: Sequence[Fraction],
    alpha: Fraction,
    lambdas: Mapping[Support, Fraction],
    *,
    direct_lp_check: bool = False,
) -> SupportOracleResult:
    u_tuple = tuple(Fraction(value) for value in u)
    alpha = Fraction(alpha)
    A, B, item_costs = item_costs_from_lambdas(k, lambdas)
    min_cut_F, _active_cuts = min_cut_F_value(k, u_tuple, alpha)
    max_flow_F = max_flow_value(k, u_tuple, alpha)
    if min_cut_F != max_flow_F:
        raise ValueError(
            "edge-cover max-flow/min-cut mismatch: "
            f"min_cut={rational_payload(min_cut_F)} max_flow={rational_payload(max_flow_F)}"
        )
    flow = min_cost_flow_value(k, u_tuple, alpha, item_costs, target_value=min_cut_F)
    total_Au = sum((A[i] * u_tuple[i] for i in left_vertices(k)), Fraction(0))
    phi = total_Au - flow.cost

    direct_cost: Fraction | None = None
    direct_phi: Fraction | None = None
    vertex_count: int | None = None
    if direct_lp_check:
        vertices = direct_lp_vertices(k, u_tuple, alpha)
        if not vertices:
            raise ValueError("direct LP vertex enumeration produced no vertices")
        direct_cost = min(_vertex_cost(vertex, item_costs) for vertex in vertices)
        direct_phi = total_Au - direct_cost
        vertex_count = len(vertices)
        if direct_cost != flow.cost:
            raise ValueError(
                "min-cost flow/direct-LP mismatch: "
                f"mcf={rational_payload(flow.cost)} direct={rational_payload(direct_cost)}"
            )

    return SupportOracleResult(
        k=k,
        u=u_tuple,
        alpha=alpha,
        lambdas={tuple(sorted(support)): Fraction(value) for support, value in lambdas.items() if value},
        A=A,
        B=B,
        F=min_cut_F,
        min_cut_F=min_cut_F,
        max_flow_F=max_flow_F,
        min_cost=flow.cost,
        phi=phi,
        item_flow=flow.item_flow,
        direct_lp_min_cost=direct_cost,
        direct_lp_phi=direct_phi,
        direct_lp_vertex_count=vertex_count,
    )


def direct_lp_vertices(
    k: int, u: Sequence[Fraction], alpha: Fraction
) -> tuple[dict[str, Any], ...]:
    """Enumerate vertices of the max-flow face as an independent k<=3 LP check."""

    if k > 3:
        raise ValueError("direct LP vertex enumeration is intentionally limited to k <= 3")
    u_tuple = tuple(Fraction(value) for value in u)
    F, _active = min_cut_F_value(k, u_tuple, Fraction(alpha))
    items = edge_cover_items(k, u_tuple, Fraction(alpha))
    item_by_name = {item.name: item for item in items}
    arcs: list[tuple[int, str]] = []
    for item in items:
        for leaf in item.support:
            arcs.append((leaf, item.name))

    n = len(arcs)
    if F == 0:
        zero = tuple(Fraction(0) for _ in range(n))
        return (_vertex_payload(arcs, zero),)

    total_eq = ([Fraction(1) for _ in range(n)], F, {"kind": "total_flow_equals_F"})
    capacity_inequalities: list[tuple[list[Fraction], Fraction, dict[str, Any]]] = []
    active_pool: list[tuple[list[Fraction], Fraction, dict[str, Any]]] = []
    for leaf in left_vertices(k):
        row = [Fraction(1) if arc_leaf == leaf else Fraction(0) for arc_leaf, _item in arcs]
        entry = (row, u_tuple[leaf], {"kind": "leaf_capacity", "leaf": leaf + 1})
        capacity_inequalities.append(entry)
        active_pool.append(entry)
    for item in items:
        row = [Fraction(1) if arc_item == item.name else Fraction(0) for _leaf, arc_item in arcs]
        entry = (row, item.capacity, {"kind": "item_capacity", "item": item.name})
        capacity_inequalities.append(entry)
        active_pool.append(entry)
    for index, (leaf, item_name) in enumerate(arcs):
        row = [Fraction(0) for _ in range(n)]
        row[index] = Fraction(1)
        active_pool.append((row, Fraction(0), {"kind": "nonnegativity", "arc": [leaf + 1, item_name]}))

    vertices: dict[tuple[Fraction, ...], dict[str, Any]] = {}
    for active_indices in combinations(range(len(active_pool)), n - 1):
        equations = [total_eq]
        equations.extend(active_pool[index] for index in active_indices)
        solution = _solve_square([row for row, _rhs, _desc in equations], [rhs for _row, rhs, _desc in equations])
        if solution is None:
            continue
        if any(value < 0 for value in solution):
            continue
        if sum(solution) != F:
            continue
        feasible = True
        for row, rhs, _desc in capacity_inequalities:
            lhs = sum(row[index] * solution[index] for index in range(n))
            if lhs > rhs:
                feasible = False
                break
        if not feasible:
            continue
        payload = _vertex_payload(arcs, solution)
        tight = [
            desc
            for row, rhs, desc in capacity_inequalities
            if sum(row[index] * solution[index] for index in range(n)) == rhs
        ]
        tight.extend(
            {"kind": "nonnegativity", "arc": [leaf + 1, item_name]}
            for value, (leaf, item_name) in zip(solution, arcs)
            if value == 0
        )
        payload["tight_constraints"] = tight
        for item in items:
            payload["item_capacities"][item.name] = rational_payload(item.capacity)
        for item_name in tuple(payload["item_flow"]):
            if item_name not in item_by_name:
                raise RuntimeError(f"unknown item in vertex payload: {item_name}")
        vertices[solution] = payload
    return tuple(vertices[key] for key in sorted(vertices))


def _vertex_payload(arcs: Sequence[tuple[int, str]], solution: Sequence[Fraction]) -> dict[str, Any]:
    item_flow: dict[str, Fraction] = {}
    leaf_flow: dict[int, Fraction] = {}
    arc_flow: list[dict[str, Any]] = []
    for value, (leaf, item_name) in zip(solution, arcs):
        item_flow[item_name] = item_flow.get(item_name, Fraction(0)) + value
        leaf_flow[leaf] = leaf_flow.get(leaf, Fraction(0)) + value
        if value:
            arc_flow.append(
                {
                    "leaf": f"l{leaf + 1}",
                    "item": item_name,
                    "flow": rational_payload(value),
                }
            )
    return {
        "arc_solution": tuple(solution),
        "arc_flow": arc_flow,
        "item_flow": item_flow,
        "leaf_flow": leaf_flow,
        "item_capacities": {},
    }


def _vertex_cost(vertex: Mapping[str, Any], item_costs: Mapping[str, Fraction]) -> Fraction:
    return sum(
        (Fraction(flow) * item_costs.get(item_name, Fraction(0)) for item_name, flow in vertex["item_flow"].items()),
        Fraction(0),
    )


def pair_lambda_cost_coefficients(
    k: int, item_flow: Mapping[str, Fraction]
) -> dict[Pair, Fraction]:
    """Return coefficients of the item-flow cost under pair multipliers."""

    coefficients = {pair: Fraction(0) for pair in pair_supports(k)}
    for i, j in pair_supports(k):
        coefficients[(i, j)] += item_flow.get(singleton_name(i), Fraction(0))
        coefficients[(i, j)] += item_flow.get(singleton_name(j), Fraction(0))
        coefficients[(i, j)] += item_flow.get(pair_name(i, j), Fraction(0))
    return coefficients


def total_Au_pair_coefficients(k: int, u: Sequence[Fraction]) -> dict[Pair, Fraction]:
    return {(i, j): Fraction(u[i]) + Fraction(u[j]) for i, j in pair_supports(k)}


def k3_pair_chambers(
    u: Sequence[Fraction], alpha: Fraction
) -> tuple[dict[str, Any], ...]:
    """Enumerate the k=3 pair-multiplier chamber fan for a fixed star face."""

    k = 3
    vertices = direct_lp_vertices(k, u, alpha)
    pairs = pair_supports(k)
    cost_forms: dict[tuple[Fraction, ...], list[dict[str, Any]]] = {}
    for vertex_index, vertex in enumerate(vertices):
        coefficients = pair_lambda_cost_coefficients(k, vertex["item_flow"])
        key = tuple(coefficients[pair] for pair in pairs)
        cost_forms.setdefault(key, []).append(
            {
                "vertex_index": vertex_index,
                "item_flow": {
                    item: rational_payload(value)
                    for item, value in sorted(vertex["item_flow"].items())
                    if value
                },
            }
        )

    total_coefficients = total_Au_pair_coefficients(k, u)
    chambers: list[dict[str, Any]] = []
    keys = tuple(sorted(cost_forms))
    for key in keys:
        witness = _active_form_witness(key, keys)
        if witness is None:
            continue
        phi_coefficients = tuple(total_coefficients[pair] - key[index] for index, pair in enumerate(pairs))
        inequalities = []
        for other in keys:
            if other == key:
                continue
            diff = tuple(other[index] - key[index] for index in range(len(pairs)))
            if any(diff):
                inequalities.append(
                    {
                        "coefficients": _pair_vector_payload(pairs, diff),
                        "sense": ">= 0",
                        "meaning": "this min-cost form is no more expensive than a competing form",
                    }
                )
        chambers.append(
            {
                "min_cost_coefficients": _pair_vector_payload(pairs, key),
                "phi_coefficients": _pair_vector_payload(pairs, phi_coefficients),
                "region": {
                    "lambda_nonnegative": True,
                    "homogeneous_normalization": "lambda_12 + lambda_13 + lambda_23 = 1 for witnesses only",
                    "inequalities": inequalities,
                    "witness_lambda": _pair_vector_payload(pairs, witness),
                },
                "supporting_vertices": cost_forms[key],
            }
        )
    return tuple(chambers)


def _active_form_witness(
    key: tuple[Fraction, ...], all_keys: Sequence[tuple[Fraction, ...]]
) -> tuple[Fraction, ...] | None:
    dimension = len(key)
    constraints: list[tuple[Fraction, ...]] = []
    for index in range(dimension):
        row = [Fraction(0) for _ in range(dimension)]
        row[index] = Fraction(1)
        constraints.append(tuple(row))
    for other in all_keys:
        diff = tuple(other[index] - key[index] for index in range(dimension))
        if any(diff):
            constraints.append(diff)

    barycenter = tuple(Fraction(1, dimension) for _ in range(dimension))
    if _satisfies_cone_constraints(barycenter, constraints):
        return barycenter

    sum_row = tuple(Fraction(1) for _ in range(dimension))
    for first, second in combinations(range(len(constraints)), dimension - 1):
        matrix = [list(sum_row), list(constraints[first]), list(constraints[second])]
        rhs = [Fraction(1), Fraction(0), Fraction(0)]
        candidate = _solve_square(matrix, rhs)
        if candidate is None:
            continue
        candidate_tuple = tuple(candidate)
        if _satisfies_cone_constraints(candidate_tuple, constraints):
            return candidate_tuple
    return None


def _satisfies_cone_constraints(
    point: Sequence[Fraction], constraints: Sequence[Sequence[Fraction]]
) -> bool:
    if sum(point) != 1:
        return False
    return all(
        sum(row[index] * point[index] for index in range(len(point))) >= 0
        for row in constraints
    )


def _pair_vector_payload(pairs: Sequence[Pair], values: Sequence[Fraction]) -> dict[str, str]:
    return {
        f"lambda_{i + 1}{j + 1}": rational_payload(values[index])
        for index, (i, j) in enumerate(pairs)
    }


def _solve_square(
    rows: Sequence[Sequence[Fraction]], rhs: Sequence[Fraction]
) -> tuple[Fraction, ...] | None:
    n = len(rhs)
    if len(rows) != n or any(len(row) != n for row in rows):
        raise ValueError("square solve requires an n by n matrix")
    matrix = [[Fraction(value) for value in row] + [Fraction(rhs[row_index])] for row_index, row in enumerate(rows)]
    for column in range(n):
        pivot = None
        for row in range(column, n):
            if matrix[row][column] != 0:
                pivot = row
                break
        if pivot is None:
            return None
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        pivot_value = matrix[column][column]
        matrix[column] = [value / pivot_value for value in matrix[column]]
        for row in range(n):
            if row == column:
                continue
            factor = matrix[row][column]
            if factor == 0:
                continue
            matrix[row] = [
                matrix[row][col] - factor * matrix[column][col]
                for col in range(n + 1)
            ]
    return tuple(matrix[row][-1] for row in range(n))


def residual_pair_lower_bounds(
    z: Sequence[Fraction],
    t: Sequence[Fraction],
    rho: Fraction,
    beta: Fraction,
    eta: Fraction,
    gamma: Fraction,
) -> dict[Pair, Fraction]:
    """Corrected k=3 residual pair lower bounds ``ell_ij``."""

    if len(z) != 3 or len(t) != 3:
        raise ValueError("residual pair lower bounds are implemented for k=3")
    z_tuple = tuple(Fraction(value) for value in z)
    t_tuple = tuple(Fraction(value) for value in t)
    rho = Fraction(rho)
    beta = Fraction(beta)
    eta = Fraction(eta)
    gamma = Fraction(gamma)
    result: dict[Pair, Fraction] = {}
    for i, j in pair_supports(3):
        z_sum = z_tuple[i] + z_tuple[j]
        t_sum = t_tuple[i] + t_tuple[j]
        result[(i, j)] = max(
            Fraction(0),
            z_sum + rho - beta,
            t_sum + eta - gamma,
            z_sum + t_sum + rho + eta - beta - gamma,
        )
    return result


def oracle_payload(result: SupportOracleResult) -> dict[str, Any]:
    return {
        "k": result.k,
        "u": [rational_payload(value) for value in result.u],
        "alpha": rational_payload(result.alpha),
        "lambda": {
            support_label(support): rational_payload(value)
            for support, value in sorted(result.lambdas.items())
        },
        "A": [rational_payload(value) for value in result.A],
        "B": {
            f"{i + 1}{j + 1}": rational_payload(value)
            for (i, j), value in sorted(result.B.items())
        },
        "F": rational_payload(result.F),
        "min_cut_F": rational_payload(result.min_cut_F),
        "max_flow_F": rational_payload(result.max_flow_F),
        "min_cost": rational_payload(result.min_cost),
        "Phi": rational_payload(result.phi),
        "item_flow": {
            item: rational_payload(value)
            for item, value in sorted(result.item_flow.items())
            if value
        },
        "direct_lp_min_cost": rational_payload(result.direct_lp_min_cost)
        if result.direct_lp_min_cost is not None
        else None,
        "direct_lp_Phi": rational_payload(result.direct_lp_phi)
        if result.direct_lp_phi is not None
        else None,
        "direct_lp_vertex_count": result.direct_lp_vertex_count,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--u", default="1,1,1", help="comma-separated leaf weights")
    parser.add_argument("--alpha", default="1", help="center weight")
    parser.add_argument(
        "--pair-lambda",
        default="1,1,1",
        help="comma-separated multipliers for pairs 12,13,23 when k=3",
    )
    parser.add_argument("--direct-lp-check", action="store_true")
    args = parser.parse_args(argv)

    u = parse_fraction_list(args.u, args.k, "u")
    alpha = parse_rational(args.alpha, "alpha")
    lambdas = parse_pair_lambdas(args.k, args.pair_lambda)
    result = support_oracle(
        args.k,
        u,
        alpha,
        lambdas,
        direct_lp_check=args.direct_lp_check,
    )
    print(json.dumps(oracle_payload(result), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
