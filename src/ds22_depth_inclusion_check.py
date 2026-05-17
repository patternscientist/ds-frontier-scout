"""Verifier for the DS(2,2) full-objective H1 depth certificate."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
from typing import Any

from .ds22_h1_depth_polytope import (
    CERT_SCHEMA,
    DEFAULT_CERTIFICATE,
    SparseRow,
    depth_objective_coefficients,
    enumerate_blocking_vertices,
    h1_system,
    rational_to_string,
    true_depth_vectors,
)
from .ds22_true_schedules import VERTICES, enumerate_true_schedules


def parse_rational(value: Any, field: str) -> Fraction:
    if isinstance(value, bool) or isinstance(value, float):
        raise ValueError(f"{field}: expected exact rational, got {value!r}")
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, str):
        if "/" in value:
            num, den = value.split("/", 1)
            return Fraction(int(num), int(den))
        return Fraction(int(value))
    raise ValueError(f"{field}: expected exact rational string/int, got {value!r}")


def verify_certificate_file(
    path: Path = DEFAULT_CERTIFICATE,
    *,
    reenumerate_blockers: bool = True,
) -> dict[str, int]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("certificate top level must be an object")
    return verify_certificate(data, reenumerate_blockers=reenumerate_blockers)


def verify_certificate(
    data: dict[str, Any],
    *,
    reenumerate_blockers: bool = True,
) -> dict[str, int]:
    if data.get("schema") != CERT_SCHEMA:
        raise ValueError(f"schema mismatch: expected {CERT_SCHEMA!r}")
    if data.get("result") != "success":
        raise ValueError("certificate result is not success")

    system = h1_system()
    schedules = enumerate_true_schedules()
    depths = tuple(sorted(set(true_depth_vectors())))
    _check_counts(data, system, schedules, depths)
    _check_true_depths(data, schedules, depths)

    blocker_entries = data.get("cell_cover", {}).get("blocker_vertices")
    if not isinstance(blocker_entries, list):
        raise ValueError("cell_cover.blocker_vertices must be a list")
    blocker_weights = _parse_blocker_entries(blocker_entries)
    if reenumerate_blockers:
        expected = set(enumerate_blocking_vertices(depths))
        if set(blocker_weights.values()) != expected:
            missing = expected - set(blocker_weights.values())
            extra = set(blocker_weights.values()) - expected
            raise ValueError(
                "blocker vertex set mismatch: "
                f"missing={len(missing)} extra={len(extra)}"
            )

    depth_by_id = {
        entry["id"]: tuple(entry["depth"][vertex] for vertex in VERTICES)
        for entry in data["true_schedules"]["depth_vectors"]
    }
    for entry in blocker_entries:
        weight = blocker_weights[entry["id"]]
        minimum = min(_dot_depth(weight, depth) for depth in depths)
        if minimum != 1:
            raise ValueError(f"{entry['id']}: true schedule minimum is {minimum}, not 1")
        tight_ids = entry.get("tight_depth_vector_ids")
        if not isinstance(tight_ids, list) or not tight_ids:
            raise ValueError(f"{entry['id']}: missing tight depth provenance")
        for depth_id in tight_ids:
            if _dot_depth(weight, depth_by_id[depth_id]) != 1:
                raise ValueError(f"{entry['id']}: non-tight listed depth {depth_id}")

    dual_entries = data.get("h1_dual_certificates")
    if not isinstance(dual_entries, list):
        raise ValueError("h1_dual_certificates must be a list")
    if len(dual_entries) != len(blocker_weights):
        raise ValueError("dual certificate count does not match blocker count")
    seen_duals: set[str] = set()
    for entry in dual_entries:
        weight_id = entry.get("weight_id")
        if not isinstance(weight_id, str) or weight_id not in blocker_weights:
            raise ValueError("dual certificate has unknown weight_id")
        if weight_id in seen_duals:
            raise ValueError(f"duplicate dual certificate for {weight_id}")
        seen_duals.add(weight_id)
        _verify_dual_entry(system, blocker_weights[weight_id], entry)

    if seen_duals != set(blocker_weights):
        raise ValueError("some blocker vertices lack dual certificates")

    return {
        "true_schedules": len(schedules),
        "depth_vectors": len(depths),
        "blocker_vertices": len(blocker_weights),
        "dual_certificates": len(dual_entries),
        "h1_rows": len(system.rows),
    }


def _check_counts(data: dict[str, Any], system: Any, schedules: Any, depths: Any) -> None:
    h1 = data.get("h1_system")
    if not isinstance(h1, dict):
        raise ValueError("h1_system missing")
    expected_h1 = {
        "connected_subsets": len(system.connected_subsets),
        "variables": len(system.variables),
        "simplex_rows": system.simplex_rows,
        "heredity_rows": system.heredity_rows,
        "standard_form_rows": len(system.rows),
        "nonnegativity_rows": len(system.variables),
    }
    for key, expected in expected_h1.items():
        if h1.get(key) != expected:
            raise ValueError(f"h1_system.{key}: expected {expected}, got {h1.get(key)}")

    true = data.get("true_schedules")
    if not isinstance(true, dict):
        raise ValueError("true_schedules missing")
    if true.get("schedule_count") != len(schedules):
        raise ValueError("true_schedules.schedule_count mismatch")
    if true.get("depth_vector_count") != len(depths):
        raise ValueError("true_schedules.depth_vector_count mismatch")

    cover = data.get("cell_cover")
    if not isinstance(cover, dict):
        raise ValueError("cell_cover missing")
    if cover.get("blocker_vertex_count") != len(cover.get("blocker_vertices", [])):
        raise ValueError("cell_cover.blocker_vertex_count mismatch")


def _check_true_depths(
    data: dict[str, Any], schedules: Any, depths: tuple[tuple[int, ...], ...]
) -> None:
    true = data["true_schedules"]
    entries = true.get("depth_vectors")
    schedule_entries = true.get("schedules")
    if not isinstance(entries, list) or not isinstance(schedule_entries, list):
        raise ValueError("true schedule depth vectors/schedules must be lists")
    cert_depths = {
        tuple(entry["depth"][vertex] for vertex in VERTICES): entry["id"]
        for entry in entries
    }
    if set(cert_depths) != set(depths):
        raise ValueError("certificate depth-vector set does not match enumeration")
    schedule_by_id = {schedule.schedule_id: schedule for schedule in schedules}
    if set(schedule_by_id) != {entry["id"] for entry in schedule_entries}:
        raise ValueError("certificate schedule ids do not match enumeration")
    depth_id_by_vector = cert_depths
    for entry in schedule_entries:
        schedule = schedule_by_id[entry["id"]]
        expected_depth_id = depth_id_by_vector[schedule.depth_vector]
        if entry.get("depth_vector_id") != expected_depth_id:
            raise ValueError(f"{entry['id']}: depth_vector_id mismatch")
        expected_roots = [
            {"component": list(component), "root": root}
            for component, root in schedule.component_roots
        ]
        if entry.get("component_roots") != expected_roots:
            raise ValueError(f"{entry['id']}: component root provenance mismatch")


def _parse_blocker_entries(
    entries: list[dict[str, Any]]
) -> dict[str, tuple[Fraction, ...]]:
    result: dict[str, tuple[Fraction, ...]] = {}
    for entry in entries:
        weight_id = entry.get("id")
        if not isinstance(weight_id, str) or not weight_id:
            raise ValueError("blocker vertex id must be a nonempty string")
        if weight_id in result:
            raise ValueError(f"duplicate blocker id {weight_id}")
        weights = entry.get("weights")
        if not isinstance(weights, dict) or set(weights) != set(VERTICES):
            raise ValueError(f"{weight_id}: weights must have DS(2,2) vertex keys")
        vector = tuple(
            parse_rational(weights[vertex], f"{weight_id}.weights.{vertex}")
            for vertex in VERTICES
        )
        if min(vector) < 0:
            raise ValueError(f"{weight_id}: blocker weights must be nonnegative")
        if max(vector) > 1:
            raise ValueError(f"{weight_id}: blocker exceeds safe coordinate bound 1")
        result[weight_id] = vector
    return result


def _verify_dual_entry(system: Any, weight: tuple[Fraction, ...], entry: dict[str, Any]) -> None:
    claimed_minimum = parse_rational(entry.get("h1_minimum"), "h1_minimum")
    claimed_max = parse_rational(entry.get("dual_max_objective"), "dual_max_objective")
    claimed_lower = parse_rational(
        entry.get("dual_original_lower_bound"), "dual_original_lower_bound"
    )
    if claimed_minimum != 1 or claimed_lower != 1 or claimed_max != -1:
        raise ValueError(f"{entry.get('weight_id')}: expected normalized H1 bound 1")

    rows = entry.get("nonzero_dual_rows")
    if not isinstance(rows, list):
        raise ValueError("nonzero_dual_rows must be a list")
    dual = [Fraction(0) for _ in system.rows]
    seen: set[int] = set()
    for row_entry in rows:
        row_index = row_entry.get("row_index")
        if not isinstance(row_index, int) or isinstance(row_index, bool):
            raise ValueError("dual row_index must be an integer")
        if row_index < 0 or row_index >= len(system.rows):
            raise ValueError("dual row_index out of range")
        if row_index in seen:
            raise ValueError(f"duplicate dual row {row_index}")
        seen.add(row_index)
        if row_entry.get("row") != system.row_descriptors[row_index]:
            raise ValueError(f"dual row descriptor mismatch at row {row_index}")
        value = parse_rational(row_entry.get("value"), "nonzero_dual_rows.value")
        if value <= 0:
            raise ValueError("dual rows must have positive values")
        dual[row_index] = value

    max_objective = tuple(
        -coefficient for coefficient in depth_objective_coefficients(system, weight)
    )
    max_deficit = _max_dual_deficit(system.rows, max_objective, tuple(dual))
    if max_deficit != 0:
        raise ValueError(
            f"{entry.get('weight_id')}: dual feasibility deficit {max_deficit}"
        )
    dual_objective = sum(system.rhs[row] * dual[row] for row in range(len(system.rows)))
    if dual_objective != claimed_max:
        raise ValueError(
            f"{entry.get('weight_id')}: dual objective claimed "
            f"{claimed_max}, computed {dual_objective}"
        )
    if -dual_objective != claimed_minimum:
        raise ValueError(f"{entry.get('weight_id')}: original lower bound mismatch")


def _dot_depth(weight: tuple[Fraction, ...], depth: tuple[int, ...]) -> Fraction:
    return sum(weight[index] * depth[index] for index in range(len(VERTICES)))


def _max_dual_deficit(
    rows: tuple[SparseRow, ...],
    max_objective: tuple[Fraction, ...],
    dual_values: tuple[Fraction, ...],
) -> Fraction:
    deficit = Fraction(0)
    for variable, coefficient in enumerate(max_objective):
        lhs = sum(
            rows[row].get(variable, Fraction(0)) * dual_values[row]
            for row in range(len(rows))
        )
        deficit = max(deficit, coefficient - lhs)
    return deficit


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m src.ds22_depth_inclusion_check")
    parser.add_argument("certificate", type=Path, nargs="?", default=DEFAULT_CERTIFICATE)
    parser.add_argument(
        "--quick",
        action="store_true",
        help="skip independent blocker-vertex re-enumeration",
    )
    args = parser.parse_args(argv)
    summary = verify_certificate_file(
        args.certificate,
        reenumerate_blockers=not args.quick,
    )
    print(
        "verified ds22 depth inclusion certificate: "
        f"true_schedules={summary['true_schedules']} "
        f"depth_vectors={summary['depth_vectors']} "
        f"blocker_vertices={summary['blocker_vertices']} "
        f"dual_certificates={summary['dual_certificates']} "
        f"h1_rows={summary['h1_rows']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

