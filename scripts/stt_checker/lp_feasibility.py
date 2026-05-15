"""Exact rational feasibility checking for ``golinsky_stt_lp_v0``.

This module checks supplied primal points only. It deliberately does not solve
LPs, round roots, check integrality gaps, or test depth-space projections.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from fractions import Fraction
import json
from pathlib import Path
from typing import Any, Iterable

from .rationals import parse_rational, rational_to_string
from .stt import STTResult, validate_stt
from .topology import TreeTopology, declared_labels_from_topology_dict


SUPPORTED_LP_SCHEMA_VERSION = "stt-lp-cert-v0"
SUPPORTED_RELAXATION = "golinsky_stt_lp"
SUPPORTED_RELAXATION_VERSION = "golinsky_stt_lp_v0"
UNSUPPORTED_LP_PROOF_FIELDS = ("root_rounding", "integrality_gap")


@dataclass(frozen=True)
class VariableDomains:
    D: tuple[int, ...]
    X: tuple[tuple[int, int], ...]
    Z: tuple[tuple[int, int, int], ...]


@dataclass(frozen=True)
class LPAssignment:
    D: dict[int, Fraction]
    X: dict[tuple[int, int], Fraction]
    Z: dict[tuple[int, int, int], Fraction]


@dataclass(frozen=True)
class ConstraintViolation:
    family: str
    indices: dict[str, int | str]
    lhs: Fraction
    rhs: Fraction
    sense: str
    slack: Fraction

    def to_dict(self) -> dict[str, Any]:
        return {
            "family": self.family,
            "indices": dict(self.indices),
            "lhs": rational_to_string(self.lhs),
            "rhs": rational_to_string(self.rhs),
            "sense": self.sense,
            "slack": rational_to_string(self.slack),
        }

    def format(self) -> str:
        index_text = ", ".join(f"{key}={value}" for key, value in self.indices.items())
        return (
            f"{self.family}({index_text}): "
            f"{rational_to_string(self.lhs)} {self.sense} {rational_to_string(self.rhs)} "
            f"failed; slack={rational_to_string(self.slack)}"
        )


@dataclass(frozen=True)
class ObjectiveCheck:
    frequency: dict[int, Fraction]
    claimed_value: Fraction | None
    computed_value: Fraction
    frequency_sum: Fraction
    search_cost_value: Fraction

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "frequency": {
                str(vertex): rational_to_string(self.frequency[vertex])
                for vertex in sorted(self.frequency)
            },
            "computed_depth_objective_value": rational_to_string(self.computed_value),
            "frequency_sum": rational_to_string(self.frequency_sum),
            "search_cost_value": rational_to_string(self.search_cost_value),
        }
        if self.claimed_value is not None:
            payload["claimed_value"] = rational_to_string(self.claimed_value)
        return payload


@dataclass(frozen=True)
class LPFeasibilityCheck:
    certificate_id: str
    topology: TreeTopology
    domains: VariableDomains
    assignment: LPAssignment
    violations: tuple[ConstraintViolation, ...]
    objective: ObjectiveCheck | None
    normalized: dict[str, Any]

    @property
    def feasible(self) -> bool:
        return not self.violations

    def normalized_json(self) -> str:
        return json.dumps(self.normalized, indent=2, sort_keys=True) + "\n"


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("certificate: top-level JSON value must be an object")
    return data


def check_lp_file(path: str | Path) -> LPFeasibilityCheck:
    return check_lp_certificate(load_json(path))


def generate_variable_domains(topology: TreeTopology) -> VariableDomains:
    """Generate dense ``golinsky_stt_lp_v0`` variable domains."""

    D = tuple(topology.vertices)
    X = tuple((i, j) for i in topology.vertices for j in topology.vertices if i != j)
    z_values: list[tuple[int, int, int]] = []
    for i in topology.vertices:
        for j in topology.vertices:
            if i >= j:
                continue
            path = path_between(topology, i, j)
            for k in path[1:-1]:
                z_values.append((k, i, j))
    return VariableDomains(D=D, X=X, Z=tuple(z_values))


def path_between(topology: TreeTopology, source: int, target: int) -> tuple[int, ...]:
    """Return the unique simple base-tree path from ``source`` to ``target``."""

    if source not in topology.adjacency or target not in topology.adjacency:
        raise ValueError("path endpoints must be topology vertices")
    if source == target:
        return (source,)
    parent: dict[int, int | None] = {source: None}
    queue = deque([source])
    while queue and target not in parent:
        current = queue.popleft()
        for neighbor in topology.adjacency[current]:
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)
    if target not in parent:
        raise ValueError("topology is disconnected")
    reversed_path = [target]
    while reversed_path[-1] != source:
        previous = parent[reversed_path[-1]]
        if previous is None:
            raise ValueError("internal path reconstruction failure")
        reversed_path.append(previous)
    return tuple(reversed(reversed_path))


def parse_dense_assignment(raw: Any, domains: VariableDomains) -> LPAssignment:
    """Parse and validate dense proof-mode variables."""

    if not isinstance(raw, dict):
        raise ValueError("lp_solution: must be an object")
    if "variables" in raw:
        extra_solution_fields = set(raw) - {"variables"}
        if extra_solution_fields:
            raise ValueError(
                "lp_solution: unsupported fields "
                f"{sorted(extra_solution_fields)}"
            )
        raw_variables = raw["variables"]
    else:
        raw_variables = raw
    if not isinstance(raw_variables, dict):
        raise ValueError("lp_solution.variables: must be an object")

    allowed_sections = {"D", "X", "Z"}
    extra_sections = set(raw_variables) - allowed_sections
    if extra_sections:
        raise ValueError(f"lp_solution.variables: unknown sections {sorted(extra_sections)}")
    missing_sections = allowed_sections - set(raw_variables)
    if missing_sections:
        raise ValueError(f"lp_solution.variables: missing sections {sorted(missing_sections)}")

    D = _parse_D_entries(raw_variables["D"], set(domains.D))
    X = _parse_X_entries(raw_variables["X"], set(domains.X))
    Z = _parse_Z_entries(raw_variables["Z"], set(domains.Z))

    _require_exact_keys("D", set(D), set(domains.D), _format_D_key)
    _require_exact_keys("X", set(X), set(domains.X), _format_X_key)
    _require_exact_keys("Z", set(Z), set(domains.Z), _format_Z_key)
    return LPAssignment(D=D, X=X, Z=Z)


def check_constraints(
    topology: TreeTopology, domains: VariableDomains, assignment: LPAssignment
) -> tuple[ConstraintViolation, ...]:
    """Evaluate all vanilla primal constraints exactly."""

    violations: list[ConstraintViolation] = []

    for i in domains.D:
        _append_ge_violation(
            violations,
            "nonnegativity",
            {"variable": f"D_{i}", "i": i},
            assignment.D[i],
            Fraction(0),
        )
    for i, j in domains.X:
        _append_ge_violation(
            violations,
            "nonnegativity",
            {"variable": f"X_{i}_{j}", "i": i, "j": j},
            assignment.X[(i, j)],
            Fraction(0),
        )
    for k, i, j in domains.Z:
        _append_ge_violation(
            violations,
            "nonnegativity",
            {"variable": f"Z_{k}_{i}_{j}", "k": k, "i": i, "j": j},
            assignment.Z[(k, i, j)],
            Fraction(0),
        )

    z_by_endpoints: dict[tuple[int, int], list[int]] = {}
    for k, i, j in domains.Z:
        z_by_endpoints.setdefault((i, j), []).append(k)

    for i in topology.vertices:
        for j in topology.vertices:
            if i >= j:
                continue
            lhs = assignment.X[(i, j)] + assignment.X[(j, i)]
            for k in z_by_endpoints.get((i, j), []):
                lhs += assignment.Z[(k, i, j)]
            _append_ge_violation(
                violations,
                "ancestry",
                {"i": i, "j": j},
                lhs,
                Fraction(1),
            )

    for k, i, j in domains.Z:
        z_value = assignment.Z[(k, i, j)]
        _append_le_violation(
            violations,
            "loose_lca",
            {"k": k, "i": i, "j": j, "endpoint": i},
            z_value,
            assignment.X[(k, i)],
        )
        _append_le_violation(
            violations,
            "loose_lca",
            {"k": k, "i": i, "j": j, "endpoint": j},
            z_value,
            assignment.X[(k, j)],
        )

    for i in topology.vertices:
        rhs = sum(
            (assignment.X[(j, i)] for j in topology.vertices if j != i),
            Fraction(0),
        )
        _append_ge_violation(
            violations,
            "depth",
            {"i": i},
            assignment.D[i],
            rhs,
        )

    return tuple(violations)


def check_lp_certificate(data: dict[str, Any]) -> LPFeasibilityCheck:
    """Validate a proof-mode LP certificate and check primal feasibility."""

    if data.get("schema_version") != SUPPORTED_LP_SCHEMA_VERSION:
        raise ValueError(
            f"schema_version: expected {SUPPORTED_LP_SCHEMA_VERSION!r}, got "
            f"{data.get('schema_version')!r}"
        )
    if data.get("mode") != "proof":
        raise ValueError("mode: only 'proof' is supported for LP certificates")
    present_unsupported = [name for name in UNSUPPORTED_LP_PROOF_FIELDS if name in data]
    if present_unsupported:
        raise ValueError(
            "proof mode does not support LP-derived fields yet: "
            + ", ".join(present_unsupported)
        )
    if data.get("relaxation") != SUPPORTED_RELAXATION:
        raise ValueError(
            f"relaxation: expected {SUPPORTED_RELAXATION!r}, got "
            f"{data.get('relaxation')!r}"
        )
    if data.get("relaxation_version") != SUPPORTED_RELAXATION_VERSION:
        raise ValueError(
            f"relaxation_version: expected {SUPPORTED_RELAXATION_VERSION!r}, got "
            f"{data.get('relaxation_version')!r}"
        )

    certificate_id = data.get("certificate_id", "")
    if not isinstance(certificate_id, str) or not certificate_id:
        raise ValueError("certificate_id: must be a nonempty string")

    topology_data = data.get("topology")
    if not isinstance(topology_data, dict):
        raise ValueError("topology: missing object")
    declared_labels = declared_labels_from_topology_dict(topology_data)
    topology = TreeTopology.from_dict(topology_data)
    topology.validate_declared_labels(declared_labels)

    domains = generate_variable_domains(topology)
    assignment = parse_dense_assignment(data.get("lp_solution"), domains)
    violations = check_constraints(topology, domains, assignment)

    objective = None
    if "objective" in data:
        objective = check_objective(data["objective"], topology, assignment)

    normalized = {
        "schema_version": SUPPORTED_LP_SCHEMA_VERSION,
        "certificate_id": certificate_id,
        "mode": "proof",
        "relaxation": SUPPORTED_RELAXATION,
        "relaxation_version": SUPPORTED_RELAXATION_VERSION,
        "topology": topology.to_normalized_dict(declared_labels),
        "variable_domains": {
            "D_count": len(domains.D),
            "X_count": len(domains.X),
            "Z_count": len(domains.Z),
            "X": "ordered_pairs_i_j_i_ne_j",
            "Z": "triples_k_i_j_with_i_lt_j_and_k_strictly_between_i_j",
            "encoding": "dense_array_entries_required_in_proof_mode",
        },
        "lp_solution": normalized_assignment(assignment, domains),
        "feasible": not violations,
        "violations": [violation.to_dict() for violation in violations],
    }
    if objective is not None:
        normalized["objective"] = objective.to_dict()

    if violations:
        formatted = "\n".join(f"- {violation.format()}" for violation in violations)
        raise ValueError(
            f"LP feasibility failed with {len(violations)} violation(s):\n{formatted}"
        )

    return LPFeasibilityCheck(
        certificate_id=certificate_id,
        topology=topology,
        domains=domains,
        assignment=assignment,
        violations=violations,
        objective=objective,
        normalized=normalized,
    )


def check_objective(
    raw: Any, topology: TreeTopology, assignment: LPAssignment
) -> ObjectiveCheck:
    if not isinstance(raw, dict):
        raise ValueError("objective: must be an object")
    allowed = {"frequency", "value"}
    extra = set(raw) - allowed
    if extra:
        raise ValueError(f"objective: unsupported fields {sorted(extra)}")
    frequency_raw = raw.get("frequency")
    if not isinstance(frequency_raw, dict):
        raise ValueError("objective.frequency: must be an object")

    expected_keys = {str(vertex) for vertex in topology.vertices}
    if set(frequency_raw) != expected_keys:
        missing = expected_keys - set(frequency_raw)
        extra_keys = set(frequency_raw) - expected_keys
        details = []
        if missing:
            details.append(f"missing {sorted(missing)}")
        if extra_keys:
            details.append(f"extra {sorted(extra_keys)}")
        raise ValueError("objective.frequency: keys must match topology vertices (" + ", ".join(details) + ")")

    frequency: dict[int, Fraction] = {}
    for vertex in topology.vertices:
        value = parse_rational(frequency_raw[str(vertex)], f"objective.frequency.{vertex}")
        if value < 0:
            raise ValueError(f"objective.frequency.{vertex}: must be nonnegative")
        frequency[vertex] = value

    computed = sum(
        (frequency[vertex] * assignment.D[vertex] for vertex in topology.vertices),
        Fraction(0),
    )
    claimed = None
    if "value" in raw:
        claimed = parse_rational(raw["value"], "objective.value")
        if claimed != computed:
            raise ValueError(
                "objective.value: claimed "
                f"{rational_to_string(claimed)}, computed {rational_to_string(computed)}"
            )
    frequency_sum = sum(frequency.values(), Fraction(0))
    return ObjectiveCheck(
        frequency=frequency,
        claimed_value=claimed,
        computed_value=computed,
        frequency_sum=frequency_sum,
        search_cost_value=computed + frequency_sum,
    )


def normalized_assignment(
    assignment: LPAssignment, domains: VariableDomains
) -> dict[str, list[dict[str, Any]]]:
    return {
        "D": [
            {"i": i, "value": rational_to_string(assignment.D[i])}
            for i in domains.D
        ],
        "X": [
            {"i": i, "j": j, "value": rational_to_string(assignment.X[(i, j)])}
            for i, j in domains.X
        ],
        "Z": [
            {
                "k": k,
                "i": i,
                "j": j,
                "value": rational_to_string(assignment.Z[(k, i, j)]),
            }
            for k, i, j in domains.Z
        ],
    }


def stt_induced_assignment(topology: TreeTopology, stt: STTResult) -> LPAssignment:
    """Construct the exact STT-induced ``(D,X,Z)`` point.

    ``D`` uses LP strict-ancestor depth. If ``stt.depth`` is in the checker's
    root-depth-1 convention, this is exactly ``stt.depth[i] - 1``.
    """

    domains = generate_variable_domains(topology)
    ancestors = _strict_ancestor_sets(topology.vertices, stt.parent)
    D = {vertex: Fraction(len(ancestors[vertex]), 1) for vertex in topology.vertices}
    X = {
        (i, j): Fraction(1 if i in ancestors[j] else 0, 1)
        for i, j in domains.X
    }
    Z: dict[tuple[int, int, int], Fraction] = {}
    for k, i, j in domains.Z:
        lca = _lowest_common_ancestor(i, j, ancestors, stt.parent)
        Z[(k, i, j)] = Fraction(1 if k == lca else 0, 1)
    return LPAssignment(D=D, X=X, Z=Z)


def stt_certificate_to_lp_certificate(
    stt_certificate: dict[str, Any], certificate_id: str | None = None
) -> dict[str, Any]:
    """Build a proof-mode LP certificate from a valid combinatorial STT certificate."""

    topology_data = stt_certificate.get("topology")
    if not isinstance(topology_data, dict):
        raise ValueError("topology: missing object")
    declared_labels = declared_labels_from_topology_dict(topology_data)
    topology = TreeTopology.from_dict(topology_data)
    topology.validate_declared_labels(declared_labels)
    stt = validate_stt(topology, stt_certificate.get("stt"), depth_base=1)
    domains = generate_variable_domains(topology)
    assignment = stt_induced_assignment(topology, stt)
    result_id = certificate_id
    if result_id is None:
        source_id = stt_certificate.get("certificate_id", "stt-certificate")
        result_id = f"{source_id}-induced-lp"

    objective: dict[str, Any] | None = None
    weights = stt_certificate.get("weights")
    if isinstance(weights, dict) and weights.get("type") == "vertex_frequency":
        values = weights.get("values")
        if isinstance(values, dict) and set(values) == {str(v) for v in topology.vertices}:
            frequency = {str(v): values[str(v)] for v in topology.vertices}
            computed = sum(
                parse_rational(frequency[str(v)], f"weights.values.{v}") * assignment.D[v]
                for v in topology.vertices
            )
            objective = {
                "frequency": {
                    str(v): rational_to_string(
                        parse_rational(frequency[str(v)], f"weights.values.{v}")
                    )
                    for v in topology.vertices
                },
                "value": rational_to_string(computed),
            }

    payload: dict[str, Any] = {
        "schema_version": SUPPORTED_LP_SCHEMA_VERSION,
        "certificate_id": result_id,
        "mode": "proof",
        "relaxation": SUPPORTED_RELAXATION,
        "relaxation_version": SUPPORTED_RELAXATION_VERSION,
        "topology": topology.to_normalized_dict(declared_labels),
        "lp_solution": {
            "variables": normalized_assignment(assignment, domains),
        },
    }
    if objective is not None:
        payload["objective"] = objective
    return payload


def _parse_D_entries(raw: Any, domain: set[int]) -> dict[int, Fraction]:
    if not isinstance(raw, list):
        raise ValueError("lp_solution.variables.D: must be a list")
    result: dict[int, Fraction] = {}
    for index, entry in enumerate(raw):
        if not isinstance(entry, dict):
            raise ValueError(f"lp_solution.variables.D[{index}]: must be an object")
        if set(entry) != {"i", "value"}:
            raise ValueError(f"lp_solution.variables.D[{index}]: fields must be i,value")
        i = _entry_int(entry["i"], f"lp_solution.variables.D[{index}].i")
        if i in result:
            raise ValueError(f"lp_solution.variables.D[{index}]: duplicate D_{i}")
        if i not in domain:
            raise ValueError(f"lp_solution.variables.D[{index}]: unknown D_{i}")
        result[i] = parse_rational(entry["value"], f"lp_solution.variables.D[{index}].value")
    return result


def _parse_X_entries(raw: Any, domain: set[tuple[int, int]]) -> dict[tuple[int, int], Fraction]:
    if not isinstance(raw, list):
        raise ValueError("lp_solution.variables.X: must be a list")
    result: dict[tuple[int, int], Fraction] = {}
    for index, entry in enumerate(raw):
        if not isinstance(entry, dict):
            raise ValueError(f"lp_solution.variables.X[{index}]: must be an object")
        if set(entry) != {"i", "j", "value"}:
            raise ValueError(f"lp_solution.variables.X[{index}]: fields must be i,j,value")
        i = _entry_int(entry["i"], f"lp_solution.variables.X[{index}].i")
        j = _entry_int(entry["j"], f"lp_solution.variables.X[{index}].j")
        key = (i, j)
        if key in result:
            raise ValueError(f"lp_solution.variables.X[{index}]: duplicate X_{i}_{j}")
        if key not in domain:
            raise ValueError(f"lp_solution.variables.X[{index}]: unknown X_{i}_{j}")
        result[key] = parse_rational(entry["value"], f"lp_solution.variables.X[{index}].value")
    return result


def _parse_Z_entries(
    raw: Any, domain: set[tuple[int, int, int]]
) -> dict[tuple[int, int, int], Fraction]:
    if not isinstance(raw, list):
        raise ValueError("lp_solution.variables.Z: must be a list")
    result: dict[tuple[int, int, int], Fraction] = {}
    for index, entry in enumerate(raw):
        if not isinstance(entry, dict):
            raise ValueError(f"lp_solution.variables.Z[{index}]: must be an object")
        if set(entry) != {"k", "i", "j", "value"}:
            raise ValueError(f"lp_solution.variables.Z[{index}]: fields must be k,i,j,value")
        k = _entry_int(entry["k"], f"lp_solution.variables.Z[{index}].k")
        i = _entry_int(entry["i"], f"lp_solution.variables.Z[{index}].i")
        j = _entry_int(entry["j"], f"lp_solution.variables.Z[{index}].j")
        if i >= j:
            raise ValueError(
                f"lp_solution.variables.Z[{index}]: proof mode requires i < j"
            )
        key = (k, i, j)
        if key in result:
            raise ValueError(f"lp_solution.variables.Z[{index}]: duplicate Z_{k}_{i}_{j}")
        if key not in domain:
            raise ValueError(f"lp_solution.variables.Z[{index}]: unknown Z_{k}_{i}_{j}")
        result[key] = parse_rational(entry["value"], f"lp_solution.variables.Z[{index}].value")
    return result


def _entry_int(value: Any, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{field}: must be an integer")
    return value


def _require_exact_keys(
    family: str,
    seen: set[Any],
    expected: set[Any],
    formatter: Any,
) -> None:
    missing = expected - seen
    unknown = seen - expected
    if missing:
        formatted = ", ".join(formatter(key) for key in sorted(missing))
        raise ValueError(f"lp_solution.variables.{family}: missing variables {formatted}")
    if unknown:
        formatted = ", ".join(formatter(key) for key in sorted(unknown))
        raise ValueError(f"lp_solution.variables.{family}: unknown variables {formatted}")


def _format_D_key(key: int) -> str:
    return f"D_{key}"


def _format_X_key(key: tuple[int, int]) -> str:
    i, j = key
    return f"X_{i}_{j}"


def _format_Z_key(key: tuple[int, int, int]) -> str:
    k, i, j = key
    return f"Z_{k}_{i}_{j}"


def _append_ge_violation(
    violations: list[ConstraintViolation],
    family: str,
    indices: dict[str, int | str],
    lhs: Fraction,
    rhs: Fraction,
) -> None:
    slack = lhs - rhs
    if slack < 0:
        violations.append(
            ConstraintViolation(
                family=family,
                indices=indices,
                lhs=lhs,
                rhs=rhs,
                sense=">=",
                slack=slack,
            )
        )


def _append_le_violation(
    violations: list[ConstraintViolation],
    family: str,
    indices: dict[str, int | str],
    lhs: Fraction,
    rhs: Fraction,
) -> None:
    slack = rhs - lhs
    if slack < 0:
        violations.append(
            ConstraintViolation(
                family=family,
                indices=indices,
                lhs=lhs,
                rhs=rhs,
                sense="<=",
                slack=slack,
            )
        )


def _strict_ancestor_sets(
    vertices: Iterable[int], parent: dict[int, int | None]
) -> dict[int, set[int]]:
    result: dict[int, set[int]] = {}
    for vertex in vertices:
        ancestors: set[int] = set()
        current = parent[vertex]
        while current is not None:
            ancestors.add(current)
            current = parent[current]
        result[vertex] = ancestors
    return result


def _lowest_common_ancestor(
    first: int,
    second: int,
    ancestors: dict[int, set[int]],
    parent: dict[int, int | None],
) -> int | None:
    first_chain = [first]
    current = parent[first]
    while current is not None:
        first_chain.append(current)
        current = parent[current]
    second_ancestors_or_self = set(ancestors[second])
    second_ancestors_or_self.add(second)
    for vertex in first_chain:
        if vertex in second_ancestors_or_self:
            return vertex
    return None
