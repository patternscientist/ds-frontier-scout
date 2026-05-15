"""JSON certificate loading, checking, and normalization."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import json
from pathlib import Path
from typing import Any

from .enumerate_stts import integer_optimum_by_enumeration, weighted_cost
from .rationals import parse_rational, rational_to_string
from .stt import STTResult, validate_parent_array, validate_stt
from .topology import TreeTopology, declared_labels_from_topology_dict


SUPPORTED_SCHEMA_VERSION = "stt-cert-v0"
SUPPORTED_WEIGHT_TYPE = "vertex_frequency"
SUPPORTED_INTEGER_CERTIFICATE = "checker_enumerates_all_stts"
LP_FIELD_NAMES = ("lp_solution", "root_rounding", "integrality_gap")


@dataclass(frozen=True)
class CertificateCheck:
    certificate_id: str
    topology: TreeTopology
    weights: dict[int, Fraction]
    stt: STTResult
    weighted_cost: Fraction
    normalized: dict[str, Any]

    def normalized_json(self) -> str:
        return json.dumps(self.normalized, indent=2, sort_keys=True) + "\n"


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("certificate: top-level JSON value must be an object")
    return data


def check_file(path: str | Path, max_enumeration: int = 100_000) -> CertificateCheck:
    return check_certificate(load_json(path), max_enumeration=max_enumeration)


def check_certificate(
    data: dict[str, Any], max_enumeration: int = 100_000
) -> CertificateCheck:
    if data.get("schema_version") != SUPPORTED_SCHEMA_VERSION:
        raise ValueError(
            f"schema_version: expected {SUPPORTED_SCHEMA_VERSION!r}, got "
            f"{data.get('schema_version')!r}"
        )
    if "mode" not in data:
        raise ValueError("mode: missing")
    mode = data["mode"]
    if mode not in ("proof", "audit"):
        raise ValueError("mode: must be 'proof' or 'audit'")
    if mode == "proof":
        present_lp_fields = [name for name in LP_FIELD_NAMES if name in data]
        if present_lp_fields:
            raise ValueError(
                "proof mode does not support LP-derived fields yet: "
                + ", ".join(present_lp_fields)
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

    weights = _parse_weights(data.get("weights"), topology)
    cost_data = data.get("cost", {})
    if cost_data is None:
        cost_data = {}
    if not isinstance(cost_data, dict):
        raise ValueError("cost: must be an object")
    depth_base = cost_data.get("depth_base", 1)
    if not isinstance(depth_base, int) or isinstance(depth_base, bool) or depth_base not in (0, 1):
        raise ValueError("cost.depth_base: must be 0 or 1")

    stt = validate_stt(topology, data.get("stt"), depth_base=depth_base)
    validate_parent_array(topology, stt.parent, data.get("stt_parent"))
    _check_vertex_depths(cost_data.get("vertex_depths"), stt)

    computed_cost = weighted_cost(stt.depth, weights)
    if "weighted_cost" in cost_data:
        claimed_cost = parse_rational(cost_data["weighted_cost"], "cost.weighted_cost")
        if claimed_cost != computed_cost:
            raise ValueError(
                "cost.weighted_cost: claimed "
                f"{rational_to_string(claimed_cost)}, computed "
                f"{rational_to_string(computed_cost)}"
            )

    normalized_integer_optimum: dict[str, Any] | None = None
    if "integer_optimum" in data:
        normalized_integer_optimum = _check_integer_optimum(
            data["integer_optimum"],
            topology,
            weights,
            depth_base,
            max_enumeration,
        )

    normalized = {
        "schema_version": SUPPORTED_SCHEMA_VERSION,
        "certificate_id": certificate_id,
        "mode": mode,
        "topology": topology.to_normalized_dict(declared_labels),
        "weights": _normalize_weights(data["weights"], topology, weights),
        "stt": {
            "component_roots": stt.to_normalized_component_roots(),
            "parent": {str(v): stt.parent[v] for v in topology.vertices},
        },
        "cost": {
            "depth_base": depth_base,
            "vertex_depths": {str(v): stt.depth[v] for v in topology.vertices},
            "weighted_cost": rational_to_string(computed_cost),
        },
    }
    if normalized_integer_optimum is not None:
        normalized["integer_optimum"] = normalized_integer_optimum
    if mode == "audit":
        unsupported = {name: data[name] for name in LP_FIELD_NAMES if name in data}
        if unsupported:
            normalized["unsupported_lp_metadata"] = unsupported

    return CertificateCheck(
        certificate_id=certificate_id,
        topology=topology,
        weights=weights,
        stt=stt,
        weighted_cost=computed_cost,
        normalized=normalized,
    )


def _parse_weights(raw: Any, topology: TreeTopology) -> dict[int, Fraction]:
    if not isinstance(raw, dict):
        raise ValueError("weights: missing object")
    if raw.get("type") != SUPPORTED_WEIGHT_TYPE:
        raise ValueError("weights.type: only vertex_frequency is supported")
    values = raw.get("values")
    if not isinstance(values, dict):
        raise ValueError("weights.values: must be an object")

    weights: dict[int, Fraction] = {}
    for vertex in topology.vertices:
        key = str(vertex)
        if key not in values:
            raise ValueError(f"weights.values: missing vertex {vertex}")
        weight = parse_rational(values[key], f"weights.values.{key}")
        if weight < 0:
            raise ValueError(f"weights.values.{key}: must be nonnegative")
        weights[vertex] = weight
    extra = set(values) - {str(v) for v in topology.vertices}
    if extra:
        raise ValueError(f"weights.values: extra vertices {sorted(extra)}")

    normalization = raw.get("normalization", "unnormalized")
    if normalization not in ("sum_1", "unnormalized"):
        raise ValueError("weights.normalization: must be sum_1 or unnormalized")
    if normalization == "sum_1" and sum(weights.values(), Fraction(0, 1)) != 1:
        raise ValueError("weights.normalization: weights do not sum to 1")
    return weights


def _normalize_weights(
    raw: dict[str, Any], topology: TreeTopology, weights: dict[int, Fraction]
) -> dict[str, Any]:
    return {
        "type": SUPPORTED_WEIGHT_TYPE,
        "normalization": raw.get("normalization", "unnormalized"),
        "values": {str(v): rational_to_string(weights[v]) for v in topology.vertices},
    }


def _check_vertex_depths(raw: Any, stt: STTResult) -> None:
    if raw is None:
        return
    if not isinstance(raw, dict):
        raise ValueError("cost.vertex_depths: must be an object")
    expected_keys = {str(v) for v in stt.depth}
    if set(raw) != expected_keys:
        raise ValueError("cost.vertex_depths: keys must match topology vertices")
    for vertex, depth in stt.depth.items():
        claimed = raw[str(vertex)]
        if not isinstance(claimed, int) or isinstance(claimed, bool) or claimed != depth:
            raise ValueError(
                f"cost.vertex_depths.{vertex}: expected {depth}, got {claimed!r}"
            )


def _check_integer_optimum(
    raw: Any,
    topology: TreeTopology,
    weights: dict[int, Fraction],
    depth_base: int,
    max_enumeration: int,
) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ValueError("integer_optimum: must be an object")
    cert_type = raw.get("certificate_type")
    if cert_type != SUPPORTED_INTEGER_CERTIFICATE:
        raise ValueError(
            "integer_optimum.certificate_type: only "
            f"{SUPPORTED_INTEGER_CERTIFICATE!r} is supported"
        )
    claimed_value = parse_rational(raw.get("value"), "integer_optimum.value")
    optimum, best_stt, count = integer_optimum_by_enumeration(
        topology, weights, depth_base=depth_base, max_count=max_enumeration
    )
    if claimed_value != optimum:
        raise ValueError(
            "integer_optimum.value: claimed "
            f"{rational_to_string(claimed_value)}, computed {rational_to_string(optimum)}"
        )
    if "stt_count" in raw:
        claimed_count = raw["stt_count"]
        if not isinstance(claimed_count, int) or isinstance(claimed_count, bool):
            raise ValueError("integer_optimum.stt_count: must be an integer")
        if claimed_count != count:
            raise ValueError(
                f"integer_optimum.stt_count: claimed {claimed_count}, computed {count}"
            )
    return {
        "certificate_type": SUPPORTED_INTEGER_CERTIFICATE,
        "value": rational_to_string(optimum),
        "stt_count": count,
        "best_stt": {"component_roots": best_stt.to_normalized_component_roots()},
    }
