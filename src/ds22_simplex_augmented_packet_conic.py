"""Exact DS(2,2) simplex-augmented packet-conic factorizations.

This module works in the H1 first-hit coordinate system from
``src.ds22_h1_depth_polytope``.  It uses floating-point simplex only to locate a
candidate basis for small packet packing LPs; every stored factorization and
deficit certificate is reconstructed and checked with ``Fraction`` arithmetic.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import json
from pathlib import Path
from typing import Any, Iterable

from scripts.stt_checker.hereditary_lp import DEFAULT_TOLERANCE, _simplex_maximize

from .ds22_depth_inclusion_check import parse_rational
from .ds22_h1_depth_polytope import (
    DEFAULT_CERTIFICATE,
    H1System,
    SparseRow,
    _solve_square_linear_system,
    depth_objective_coefficients,
    h1_system,
    rational_to_string,
)
from .ds22_true_schedules import VERTICES, Component, Vertex, canonical_component


ATLAS_SCHEMA = "ds22_leaf_swap_blocker_orbit_atlas_v0"
FACTORIZATION_SCHEMA = "ds22_simplex_augmented_packet_factorizations_v0"
RESIDUAL_SCHEMA = "ds22_simplex_augmented_packet_residuals_v0"

DEFAULT_ATLAS = Path("data/ds22_blocker_orbits.json")
DEFAULT_FACTORIZATIONS = Path("data/ds22_simplex_augmented_packet_factorizations.json")
DEFAULT_RESIDUALS = Path("data/ds22_simplex_augmented_packet_residuals.json")
DEFAULT_REPORT = Path("reports/ds22_simplex_augmented_packet_conic_report.md")

LEFT_LEAVES: tuple[Vertex, ...] = ("li", "lj")
RIGHT_LEAVES: tuple[Vertex, ...] = ("r", "s")
SPECIAL_ORBITS: tuple[str, ...] = ("o069", "o055", "o057", "o058", "o011", "o080")


@dataclass(frozen=True)
class PacketAtom:
    atom_id: str
    kind: str
    vector: tuple[Fraction, ...]
    parameters: dict[str, Any]


@dataclass(frozen=True)
class ExactPacketLPSolution:
    status: int
    message: str
    optimum: Fraction
    coefficients: tuple[Fraction, ...]
    residual: tuple[Fraction, ...]
    dual: tuple[Fraction, ...]
    nonzero_coefficients: int


def component_key(component: Component) -> str:
    return ",".join(component)


def variable_key(variable: tuple[Component, Vertex]) -> str:
    component, root = variable
    return f"{component_key(component)}|{root}"


def parse_fraction(value: Any, field: str = "value") -> Fraction:
    return parse_rational(value, field)


def canonical_weight_json(weight: Iterable[Fraction]) -> dict[str, str]:
    return {
        vertex: rational_to_string(value)
        for vertex, value in zip(VERTICES, tuple(weight))
    }


def build_blocker_orbit_atlas(certificate: dict[str, Any]) -> dict[str, Any]:
    """Group the 943 blocker vertices by independent left/right leaf swaps.

    The representative order is the certificate blocker order.  This reproduces
    the 302-orbit atlas used by the packet-conic scratch runs.
    """

    blocker_entries = certificate["cell_cover"]["blocker_vertices"]
    blockers: list[tuple[str, tuple[Fraction, ...], dict[str, Any]]] = []
    for entry in blocker_entries:
        weight = tuple(
            parse_fraction(entry["weights"][vertex], f"{entry['id']}.{vertex}")
            for vertex in VERTICES
        )
        blockers.append((entry["id"], weight, entry))

    blocker_id_by_weight = {weight: blocker_id for blocker_id, weight, _ in blockers}
    blocker_index = {blocker_id: index for index, (blocker_id, _weight, _entry) in enumerate(blockers)}
    blocker_entry_by_id = {blocker_id: entry for blocker_id, _weight, entry in blockers}

    transforms = _leaf_swap_transforms()
    seen: set[tuple[Fraction, ...]] = set()
    representatives: list[dict[str, Any]] = []
    for blocker_id, weight, entry in blockers:
        if weight in seen:
            continue
        orbit_weights = {
            _apply_weight_transform(weight, transform["mapping"]) for transform in transforms
        }
        orbit_weights = {candidate for candidate in orbit_weights if candidate in blocker_id_by_weight}
        seen.update(orbit_weights)
        member_ids = sorted(
            (blocker_id_by_weight[candidate] for candidate in orbit_weights),
            key=blocker_index.__getitem__,
        )
        representatives.append(
            {
                "id": f"o{len(representatives):03d}",
                "representative_blocker_id": blocker_id,
                "weights": canonical_weight_json(weight),
                "support": sum(1 for coordinate in weight if coordinate != 0),
                "orbit_size": len(member_ids),
                "member_blocker_ids": member_ids,
                "tight_depth_vector_ids": entry.get("tight_depth_vector_ids", []),
            }
        )

    return {
        "schema": ATLAS_SCHEMA,
        "source_certificate": str(DEFAULT_CERTIFICATE),
        "source_certificate_schema": certificate.get("schema"),
        "source_blocker_vertex_count": len(blockers),
        "orbit_group": {
            "description": "independent swaps of li/lj and r/s with anchors a,b fixed",
            "transforms": transforms,
        },
        "orbit_representative_count": len(representatives),
        "representatives": representatives,
        "source_blockers_by_id": {
            blocker_id: {
                "weights": canonical_weight_json(weight),
                "tight_depth_vector_ids": blocker_entry_by_id[blocker_id].get(
                    "tight_depth_vector_ids", []
                ),
            }
            for blocker_id, weight, _entry in blockers
        },
    }


def packet_atoms(system: H1System | None = None, *, include_sigma: bool = True) -> tuple[PacketAtom, ...]:
    system = h1_system() if system is None else system
    variable_count = len(system.variables)
    atoms: list[PacketAtom] = []

    if include_sigma:
        for component in system.connected_subsets:
            vector = _zero_vector(variable_count)
            for root in component:
                _add_term(vector, system, component, root)
            atoms.append(
                PacketAtom(
                    atom_id=f"Sigma[{component_key(component)}]",
                    kind="Sigma",
                    vector=tuple(vector),
                    parameters={"S": list(component)},
                )
            )

    left_spine = _component("a", "li", "lj")
    for ell in LEFT_LEAVES:
        source = _component("a", ell)
        vector = _sigma_vector(system, left_spine)
        _add_term(vector, system, source, "a")
        _add_term(vector, system, left_spine, "a", -1)
        atoms.append(
            PacketAtom(
                atom_id=f"Lambda[{ell}]",
                kind="Lambda",
                vector=tuple(vector),
                parameters={"ell": ell, "L": list(left_spine), "source": list(source)},
            )
        )

    right_spine = _component("b", "r", "s")
    for x in RIGHT_LEAVES:
        source = _component("b", x)
        vector = _sigma_vector(system, right_spine)
        _add_term(vector, system, source, "b")
        _add_term(vector, system, right_spine, "b", -1)
        atoms.append(
            PacketAtom(
                atom_id=f"Gamma[{x}]",
                kind="Gamma",
                vector=tuple(vector),
                parameters={"x": x, "R": list(right_spine), "source": list(source)},
            )
        )

    for ell in LEFT_LEAVES:
        cap = _component("a", "b", ell)
        for source in (_component("a", "b"), _component("a", ell)):
            vector = _sigma_vector(system, cap)
            _add_term(vector, system, source, "a")
            _add_term(vector, system, cap, "a", -1)
            atoms.append(
                PacketAtom(
                    atom_id=f"Delta[{ell};P={component_key(source)}]",
                    kind="Delta",
                    vector=tuple(vector),
                    parameters={"ell": ell, "D": list(cap), "P": list(source)},
                )
            )

    for x in RIGHT_LEAVES:
        cap = _component("a", "b", x)
        for source in (_component("a", "b"), _component("b", x)):
            vector = _sigma_vector(system, cap)
            _add_term(vector, system, source, "b")
            _add_term(vector, system, cap, "b", -1)
            atoms.append(
                PacketAtom(
                    atom_id=f"Omega[{x};Q={component_key(source)}]",
                    kind="Omega",
                    vector=tuple(vector),
                    parameters={"x": x, "C": list(cap), "Q": list(source)},
                )
            )

    for x in RIGHT_LEAVES:
        for ell in LEFT_LEAVES:
            cell = _component("a", "b", x, ell)
            left_sources = (
                _component("a", "b"),
                _component("a", ell),
                _component("a", "b", x),
            )
            right_sources = (
                _component("a", "b"),
                _component("b", x),
                _component("a", "b", ell),
            )
            for left_source in left_sources:
                for right_source in right_sources:
                    vector = _sigma_vector(system, cell)
                    _add_term(vector, system, left_source, "a")
                    _add_term(vector, system, cell, "a", -1)
                    _add_term(vector, system, right_source, "b")
                    _add_term(vector, system, cell, "b", -1)
                    atoms.append(
                        PacketAtom(
                            atom_id=(
                                f"Pi[{x},{ell};P={component_key(left_source)};"
                                f"Q={component_key(right_source)}]"
                            ),
                            kind="Pi",
                            vector=tuple(vector),
                            parameters={
                                "x": x,
                                "ell": ell,
                                "U": list(cell),
                                "P": list(left_source),
                                "Q": list(right_source),
                            },
                        )
                    )

    return tuple(atoms)


def solve_packet_mass_lp(
    objective: tuple[Fraction, ...],
    atoms: tuple[PacketAtom, ...],
    *,
    tolerance: float = DEFAULT_TOLERANCE,
) -> ExactPacketLPSolution:
    """Maximize total packet mass subject to packet sum <= objective."""

    row_count = len(objective)
    atom_count = len(atoms)
    rows: tuple[SparseRow, ...] = tuple(
        {
            atom_index: atom.vector[coordinate]
            for atom_index, atom in enumerate(atoms)
            if atom.vector[coordinate] != 0
        }
        for coordinate in range(row_count)
    )
    rhs = tuple(objective)
    max_objective = tuple(Fraction(1) for _ in atoms)
    simplex_result = _simplex_maximize(
        [
            [float(rows[row].get(atom_index, Fraction(0))) for atom_index in range(atom_count)]
            for row in range(row_count)
        ],
        [float(value) for value in rhs],
        [1.0 for _ in atoms],
        tolerance=tolerance,
    )
    if simplex_result.status != 0:
        return ExactPacketLPSolution(
            status=simplex_result.status,
            message=simplex_result.message,
            optimum=Fraction(0),
            coefficients=tuple(Fraction(0) for _ in atoms),
            residual=rhs,
            dual=tuple(Fraction(0) for _ in objective),
            nonzero_coefficients=0,
        )

    coefficients, dual = _exact_primal_dual_from_basis(
        rows,
        rhs,
        max_objective,
        simplex_result.basis,
        simplex_result.nonbasis,
        atom_count,
    )
    residual = tuple(
        rhs[row]
        - sum(rows[row].get(atom_index, Fraction(0)) * coefficients[atom_index] for atom_index in range(atom_count))
        for row in range(row_count)
    )
    optimum = sum(coefficients)
    _verify_lp_solution(rows, rhs, max_objective, coefficients, residual, dual, optimum)
    return ExactPacketLPSolution(
        status=0,
        message="optimal_exact_basis_verified",
        optimum=optimum,
        coefficients=coefficients,
        residual=residual,
        dual=dual,
        nonzero_coefficients=sum(1 for value in coefficients if value != 0),
    )


def build_artifacts(
    *,
    certificate_path: Path = DEFAULT_CERTIFICATE,
    tolerance: float = DEFAULT_TOLERANCE,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], str]:
    with certificate_path.open("r", encoding="utf-8") as handle:
        certificate = json.load(handle)

    system = h1_system()
    atlas = build_blocker_orbit_atlas(certificate)
    augmented_atoms = packet_atoms(system, include_sigma=True)
    five_packet_atoms = packet_atoms(system, include_sigma=False)
    atom_by_id = {atom.atom_id: atom for atom in augmented_atoms}

    factorizations: list[dict[str, Any]] = []
    residual_entries: list[dict[str, Any]] = []
    five_packet_entries: list[dict[str, Any]] = []
    augmented_failures: list[dict[str, Any]] = []
    special_deficits: dict[str, dict[str, Any]] = {}

    for representative in atlas["representatives"]:
        orbit_id = representative["id"]
        weight = _weight_from_json(representative["weights"])
        objective = depth_objective_coefficients(system, weight)

        augmented_solution = solve_packet_mass_lp(
            objective,
            augmented_atoms,
            tolerance=tolerance,
        )
        if augmented_solution.status != 0 or augmented_solution.optimum < 1:
            augmented_failures.append(
                {
                    "orbit_id": orbit_id,
                    "representative_blocker_id": representative["representative_blocker_id"],
                    "status": augmented_solution.message,
                    "maximum_packet_mass": rational_to_string(augmented_solution.optimum),
                    "deficit": rational_to_string(1 - augmented_solution.optimum),
                }
            )
            coefficients = augmented_solution.coefficients
            residual = augmented_solution.residual
        else:
            coefficients = _mass_one_coefficients(augmented_solution.coefficients)
            residual = _residual_from_coefficients(objective, augmented_atoms, coefficients)
            _verify_mass_one_factorization(objective, augmented_atoms, coefficients, residual)

        nonzero_coefficients = [
            {
                "atom_id": atom.atom_id,
                "kind": atom.kind,
                "coefficient": rational_to_string(coefficients[index]),
            }
            for index, atom in enumerate(augmented_atoms)
            if coefficients[index] != 0
        ]
        sigma_mass = sum(
            coefficients[index]
            for index, atom in enumerate(augmented_atoms)
            if atom.kind == "Sigma"
        )
        factorizations.append(
            {
                "orbit_id": orbit_id,
                "representative_blocker_id": representative["representative_blocker_id"],
                "weights": representative["weights"],
                "support": representative["support"],
                "objective_nonzero_terms": _nonzero_terms(system, objective),
                "packet_mass": rational_to_string(sum(coefficients)),
                "sigma_mass": rational_to_string(sigma_mass),
                "nonzero_packet_coefficients": nonzero_coefficients,
                "residual_nonzero_count": sum(1 for value in residual if value != 0),
            }
        )
        residual_entries.append(
            {
                "orbit_id": orbit_id,
                "representative_blocker_id": representative["representative_blocker_id"],
                "minimum_residual_coordinate": rational_to_string(min(residual)),
                "nonzero_residual_terms": _nonzero_terms(system, residual),
            }
        )

        five_packet_solution = solve_packet_mass_lp(
            objective,
            five_packet_atoms,
            tolerance=tolerance,
        )
        if five_packet_solution.status != 0:
            raise ValueError(
                f"{orbit_id}: five-packet LP failed with {five_packet_solution.message}"
            )
        five_deficit = Fraction(1) - five_packet_solution.optimum
        five_coefficients = [
            {
                "atom_id": atom.atom_id,
                "kind": atom.kind,
                "coefficient": rational_to_string(five_packet_solution.coefficients[index]),
            }
            for index, atom in enumerate(five_packet_atoms)
            if five_packet_solution.coefficients[index] != 0
        ]
        five_entry = {
            "orbit_id": orbit_id,
            "representative_blocker_id": representative["representative_blocker_id"],
            "weights": representative["weights"],
            "support": representative["support"],
            "status": "closes" if five_deficit <= 0 else "deficient",
            "maximum_packet_mass": rational_to_string(five_packet_solution.optimum),
            "deficit": rational_to_string(max(Fraction(0), five_deficit)),
            "nonzero_packet_coefficients": five_coefficients,
            "residual_nonzero_count": sum(1 for value in five_packet_solution.residual if value != 0),
            "minimum_residual_coordinate": rational_to_string(min(five_packet_solution.residual)),
            "nonzero_residual_terms": _nonzero_terms(system, five_packet_solution.residual),
            "dual_upper_bound_terms": _nonzero_terms(system, five_packet_solution.dual),
        }
        if orbit_id in SPECIAL_ORBITS:
            special_deficits[orbit_id] = dict(five_entry)
        five_packet_entries.append(five_entry)

        # A small sanity guard that catches accidental catalog drift while building.
        for coefficient in nonzero_coefficients:
            if coefficient["atom_id"] not in atom_by_id:
                raise ValueError(f"unknown packet atom {coefficient['atom_id']}")

    factorization_data = {
        "schema": FACTORIZATION_SCHEMA,
        "source_certificate": str(certificate_path),
        "blocker_orbit_atlas": str(DEFAULT_ATLAS),
        "h1_coordinate_system": _coordinate_system_json(system),
        "packet_atom_count": len(augmented_atoms),
        "packet_kind_counts": _kind_counts(augmented_atoms),
        "packet_atoms": [_atom_json(system, atom) for atom in augmented_atoms],
        "orbit_representative_count": len(factorizations),
        "augmented_failures": augmented_failures,
        "factorizations": factorizations,
        "notes": [
            "Floating-point simplex was used only to locate bases.",
            "Stored packet coefficients and residuals are exact rationals.",
            "No H2, refined-Z, path-monotonicity, ancestry-transitivity, "
            "LCA-separation, or mixed-second-difference rows are used.",
        ],
    }
    residual_data = {
        "schema": RESIDUAL_SCHEMA,
        "source_factorizations": str(DEFAULT_FACTORIZATIONS),
        "augmented_basis": {
            "status": "success" if not augmented_failures else "has_failures",
            "failure_count": len(augmented_failures),
            "failures": augmented_failures,
            "residuals": residual_entries,
        },
        "five_packet_without_sigma": {
            "packet_atom_count": len(five_packet_atoms),
            "packet_kind_counts": _kind_counts(five_packet_atoms),
            "success_count": sum(1 for entry in five_packet_entries if entry["status"] == "closes"),
            "failure_count": sum(1 for entry in five_packet_entries if entry["status"] == "deficient"),
            "special_orbit_deficits": special_deficits,
            "representatives": five_packet_entries,
        },
    }
    report = render_report(atlas, factorization_data, residual_data)
    return atlas, factorization_data, residual_data, report


def write_artifacts(
    *,
    certificate_path: Path = DEFAULT_CERTIFICATE,
    atlas_path: Path = DEFAULT_ATLAS,
    factorization_path: Path = DEFAULT_FACTORIZATIONS,
    residual_path: Path = DEFAULT_RESIDUALS,
    report_path: Path = DEFAULT_REPORT,
    tolerance: float = DEFAULT_TOLERANCE,
) -> dict[str, Any]:
    atlas, factorization_data, residual_data, report = build_artifacts(
        certificate_path=certificate_path,
        tolerance=tolerance,
    )
    for path, payload in (
        (atlas_path, atlas),
        (factorization_path, factorization_data),
        (residual_path, residual_data),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    return {
        "atlas": str(atlas_path),
        "factorizations": str(factorization_path),
        "residuals": str(residual_path),
        "report": str(report_path),
        "orbit_representatives": factorization_data["orbit_representative_count"],
        "packet_atoms": factorization_data["packet_atom_count"],
        "five_packet_failures": residual_data["five_packet_without_sigma"]["failure_count"],
    }


def render_report(
    atlas: dict[str, Any],
    factorization_data: dict[str, Any],
    residual_data: dict[str, Any],
) -> str:
    h1 = factorization_data["h1_coordinate_system"]
    five = residual_data["five_packet_without_sigma"]
    special_lines = [
        (
            f"- `{orbit_id}`: five-packet maximum mass "
            f"`{entry['maximum_packet_mass']}`, deficit `{entry['deficit']}`."
        )
        for orbit_id, entry in sorted(five["special_orbit_deficits"].items())
    ]
    lines = [
        "# DS(2,2) Simplex-Augmented Packet-Conic Closure",
        "",
        "## Result",
        "",
        "All 302 leaf-swap atlas orbit representatives factor exactly into the simplex-augmented packet basis `Sigma/Lambda/Gamma/Delta/Omega/Pi` plus a nonnegative coordinate residual. Each stored factorization has total packet mass exactly `1`.",
        "",
        "Floating-point simplex was used only to identify candidate LP bases. The checked artifacts store exact rational coefficients, exact rational residuals, and exact rational dual upper-bound certificates for the five-packet optima.",
        "",
        "## Counts",
        "",
        f"- H1 variables: `{h1['variable_count']}` over `{h1['connected_subset_count']}` connected subsets.",
        f"- Certificate blocker vertices: `{atlas['source_blocker_vertex_count']}`.",
        f"- Leaf-swap orbit representatives: `{atlas['orbit_representative_count']}`.",
        f"- Simplex-augmented packet atoms: `{factorization_data['packet_atom_count']}` with kind counts `{factorization_data['packet_kind_counts']}`.",
        f"- Five-packet atoms without `Sigma`: `{five['packet_atom_count']}`.",
        f"- Augmented-basis failures: `{len(factorization_data['augmented_failures'])}`.",
        f"- Five-packet failures without `Sigma`: `{five['failure_count']}` of `{atlas['orbit_representative_count']}`.",
        "",
        "## Correction Note",
        "",
        "`Lambda/Gamma/Delta/Omega/Pi` alone are insufficient. In the exact LP audit without `Sigma`, 287 of the 302 orbit representatives have maximum packet mass below `1`; the raw simplex atoms supply the missing mass.",
        "",
        "`Sigma_S = sigma_S` is a raw H1 simplex-row atom, not a new packet type with independent structural content. The augmented closure is therefore best read as an exact DS(2,2) computational atlas and a bookkeeping decomposition for the packet deficit, not as a conceptual packet-basis theorem.",
        "",
        "Special representatives requested in the task:",
        "",
        *special_lines,
        "",
        "## Exact Objects",
        "",
        "- `Sigma_S = sigma_S` for each connected `S`.",
        "- `Lambda`, `Gamma`, `Delta`, `Omega`, and `Pi` atoms are represented as exact H1 coordinate vectors in the factorization JSON.",
        "- For each representative, `w dot d` is reconstructed from the blocker weights and the H1 path-depth objective.",
        "- The residual vector is `w dot d - packet_combination`, checked coordinatewise nonnegative over all 84 H1 coordinates.",
        "",
        "## Scope Guardrails",
        "",
        "This branch uses only H1 first-hit coordinates, raw simplex rows, and packet-coordinate arithmetic. It does not use H2, refined-Z, path-monotonicity, ancestry-transitivity, LCA-separation, or mixed-second-difference rows.",
        "",
        "The result is a finite DS(2,2) packet-closure certificate over this atlas. It does not imply DS(k,2), DS(2,m), or DS(k,m) exactness, and it should not be promoted as a standalone conceptual closure until the role of the simplex atoms is explained by a non-tautological proof template.",
        "",
        "## Artifacts",
        "",
        f"- Orbit atlas: `{DEFAULT_ATLAS}`.",
        f"- Factorizations: `{DEFAULT_FACTORIZATIONS}`.",
        f"- Residuals and five-packet deficits: `{DEFAULT_RESIDUALS}`.",
        f"- Verifier/test entry point: `tests/test_ds22_simplex_augmented_packet_conic.py`.",
        "",
        "## Verification Commands",
        "",
        "```powershell",
        "python -m src.ds22_simplex_augmented_packet_conic --verify",
        "python -m unittest tests.test_ds22_simplex_augmented_packet_conic",
        "```",
    ]
    return "\n".join(lines) + "\n"


def verify_artifact_files(
    factorization_path: Path = DEFAULT_FACTORIZATIONS,
    residual_path: Path = DEFAULT_RESIDUALS,
    atlas_path: Path = DEFAULT_ATLAS,
) -> dict[str, int]:
    with factorization_path.open("r", encoding="utf-8") as handle:
        factorization_data = json.load(handle)
    with residual_path.open("r", encoding="utf-8") as handle:
        residual_data = json.load(handle)
    with atlas_path.open("r", encoding="utf-8") as handle:
        atlas = json.load(handle)
    return verify_artifacts(factorization_data, residual_data, atlas)


def verify_artifacts(
    factorization_data: dict[str, Any],
    residual_data: dict[str, Any],
    atlas: dict[str, Any],
) -> dict[str, int]:
    if factorization_data.get("schema") != FACTORIZATION_SCHEMA:
        raise ValueError("factorization schema mismatch")
    if residual_data.get("schema") != RESIDUAL_SCHEMA:
        raise ValueError("residual schema mismatch")
    if atlas.get("schema") != ATLAS_SCHEMA:
        raise ValueError("atlas schema mismatch")

    system = h1_system()
    atoms = packet_atoms(system, include_sigma=True)
    atom_by_id = {atom.atom_id: atom for atom in atoms}
    if len(atom_by_id) != len(atoms):
        raise ValueError("duplicate packet atom ids")
    _verify_atom_catalog(system, factorization_data.get("packet_atoms", []), atoms)

    reps_by_id = _entries_by_orbit_id(atlas.get("representatives", []), "atlas")
    expected_orbits = set(reps_by_id)
    if factorization_data.get("orbit_representative_count") != len(expected_orbits):
        raise ValueError("factorization orbit_representative_count mismatch")
    if factorization_data.get("packet_atom_count") != len(atoms):
        raise ValueError("packet atom count mismatch")
    if factorization_data.get("packet_kind_counts") != _kind_counts(atoms):
        raise ValueError("packet kind counts mismatch")

    factorization_by_orbit = _entries_by_orbit_id(
        factorization_data.get("factorizations", []),
        "factorizations",
        expected_orbits,
    )
    residual_entry_by_orbit = _entries_by_orbit_id(
        residual_data["augmented_basis"]["residuals"],
        "augmented residuals",
        expected_orbits,
    )

    factorization_count = 0
    for orbit_id, entry in sorted(factorization_by_orbit.items()):
        representative = reps_by_id[orbit_id]
        _verify_representative_metadata(entry, representative, "factorization")
        residual_entry = residual_entry_by_orbit[orbit_id]
        _verify_representative_metadata(
            residual_entry,
            representative,
            "augmented residual",
            require_weights=False,
            require_support=False,
        )
        coefficients = _coefficients_from_entries(
            atoms,
            entry["nonzero_packet_coefficients"],
            orbit_id,
        )
        if sum(coefficients) != 1 or parse_fraction(entry["packet_mass"]) != 1:
            raise ValueError(f"{orbit_id}: packet mass is not exactly 1")

        objective = depth_objective_coefficients(system, _weight_from_json(representative["weights"]))
        residual = _vector_from_terms(system, residual_entry["nonzero_residual_terms"])
        _verify_mass_one_factorization(objective, atoms, tuple(coefficients), residual)
        if sum(1 for value in residual if value != 0) != entry["residual_nonzero_count"]:
            raise ValueError(f"{orbit_id}: residual nonzero count mismatch")
        if rational_to_string(min(residual)) != residual_entry["minimum_residual_coordinate"]:
            raise ValueError(f"{orbit_id}: residual minimum mismatch")
        factorization_count += 1

    five_atoms = packet_atoms(system, include_sigma=False)
    if residual_data["five_packet_without_sigma"].get("packet_atom_count") != len(five_atoms):
        raise ValueError("five-packet atom count mismatch")
    if residual_data["five_packet_without_sigma"].get("packet_kind_counts") != _kind_counts(five_atoms):
        raise ValueError("five-packet kind counts mismatch")
    five_by_orbit = _entries_by_orbit_id(
        residual_data["five_packet_without_sigma"]["representatives"],
        "five-packet representatives",
        expected_orbits,
    )
    five_failures = 0
    for orbit_id, entry in sorted(five_by_orbit.items()):
        representative = reps_by_id[orbit_id]
        _verify_representative_metadata(entry, representative, "five-packet")
        objective = depth_objective_coefficients(system, _weight_from_json(representative["weights"]))
        optimum = parse_fraction(entry["maximum_packet_mass"], f"{orbit_id}.maximum_packet_mass")
        deficit = parse_fraction(entry["deficit"], f"{orbit_id}.deficit")
        coefficients = _coefficients_from_entries(
            five_atoms,
            entry["nonzero_packet_coefficients"],
            orbit_id,
        )
        residual = _vector_from_terms(system, entry["nonzero_residual_terms"])
        _verify_packet_primal(objective, five_atoms, tuple(coefficients), residual, optimum)
        if sum(1 for value in residual if value != 0) != entry["residual_nonzero_count"]:
            raise ValueError(f"{orbit_id}: five-packet residual nonzero count mismatch")
        if rational_to_string(min(residual)) != entry["minimum_residual_coordinate"]:
            raise ValueError(f"{orbit_id}: five-packet residual minimum mismatch")
        dual = _vector_from_terms(system, entry["dual_upper_bound_terms"])
        _verify_dual_upper_bound(objective, five_atoms, dual, optimum)
        if entry["status"] == "deficient":
            five_failures += 1
            if optimum >= 1 or deficit != 1 - optimum:
                raise ValueError(f"{orbit_id}: bad five-packet deficit")
        elif entry["status"] == "closes":
            if optimum < 1 or deficit != 0:
                raise ValueError(f"{orbit_id}: bad five-packet success entry")
        else:
            raise ValueError(f"{orbit_id}: unknown five-packet status")

    return {
        "orbit_representatives": factorization_count,
        "packet_atoms": len(atoms),
        "five_packet_failures": five_failures,
    }


def _entries_by_orbit_id(
    entries: list[dict[str, Any]],
    label: str,
    expected_orbits: set[str] | None = None,
) -> dict[str, dict[str, Any]]:
    if not isinstance(entries, list):
        raise ValueError(f"{label} must be a list")
    result: dict[str, dict[str, Any]] = {}
    for entry in entries:
        orbit_id = entry.get("id", entry.get("orbit_id"))
        if not isinstance(orbit_id, str) or not orbit_id:
            raise ValueError(f"{label}: missing orbit id")
        if orbit_id in result:
            raise ValueError(f"{label}: duplicate orbit id {orbit_id}")
        result[orbit_id] = entry
    if expected_orbits is not None and set(result) != expected_orbits:
        missing = sorted(expected_orbits - set(result))
        extra = sorted(set(result) - expected_orbits)
        raise ValueError(
            f"{label}: orbit id set mismatch; missing={missing[:5]} extra={extra[:5]}"
        )
    return result


def _verify_representative_metadata(
    entry: dict[str, Any],
    representative: dict[str, Any],
    label: str,
    *,
    require_weights: bool = True,
    require_support: bool = True,
) -> None:
    orbit_id = representative["id"]
    if entry.get("representative_blocker_id") != representative["representative_blocker_id"]:
        raise ValueError(f"{orbit_id}: {label} representative_blocker_id mismatch")
    if require_weights and _weight_from_json(entry.get("weights", {})) != _weight_from_json(representative["weights"]):
        raise ValueError(f"{orbit_id}: {label} weights mismatch")
    if require_support and entry.get("support") != representative["support"]:
        raise ValueError(f"{orbit_id}: {label} support mismatch")


def _coefficients_from_entries(
    atoms: tuple[PacketAtom, ...],
    coefficient_entries: list[dict[str, Any]],
    orbit_id: str,
) -> tuple[Fraction, ...]:
    if not isinstance(coefficient_entries, list):
        raise ValueError(f"{orbit_id}: coefficient list missing")
    atom_index_by_id = {atom.atom_id: index for index, atom in enumerate(atoms)}
    coefficients = [Fraction(0) for _ in atoms]
    seen: set[str] = set()
    for coefficient_entry in coefficient_entries:
        atom_id = coefficient_entry.get("atom_id")
        if atom_id not in atom_index_by_id:
            raise ValueError(f"{orbit_id}: unknown atom {atom_id}")
        if atom_id in seen:
            raise ValueError(f"{orbit_id}: duplicate coefficient for {atom_id}")
        seen.add(atom_id)
        atom = atoms[atom_index_by_id[atom_id]]
        if coefficient_entry.get("kind") != atom.kind:
            raise ValueError(f"{orbit_id}: kind mismatch for {atom_id}")
        value = parse_fraction(coefficient_entry.get("coefficient"), f"{orbit_id}.{atom_id}")
        if value <= 0:
            raise ValueError(f"{orbit_id}: packet coefficients must be positive when listed")
        coefficients[atom_index_by_id[atom_id]] = value
    return tuple(coefficients)


def solve_representative(
    orbit_entry: dict[str, Any],
    *,
    include_sigma: bool,
    tolerance: float = DEFAULT_TOLERANCE,
) -> ExactPacketLPSolution:
    system = h1_system()
    atoms = packet_atoms(system, include_sigma=include_sigma)
    objective = depth_objective_coefficients(system, _weight_from_json(orbit_entry["weights"]))
    return solve_packet_mass_lp(objective, atoms, tolerance=tolerance)


def _leaf_swap_transforms() -> list[dict[str, Any]]:
    transforms: list[dict[str, Any]] = []
    for transform_id, mapping in (
        ("identity", {}),
        ("swap_left", {"li": "lj", "lj": "li"}),
        ("swap_right", {"r": "s", "s": "r"}),
        ("swap_left_and_right", {"li": "lj", "lj": "li", "r": "s", "s": "r"}),
    ):
        full_mapping = {vertex: mapping.get(vertex, vertex) for vertex in VERTICES}
        transforms.append({"id": transform_id, "mapping": full_mapping})
    return transforms


def _apply_weight_transform(
    weight: tuple[Fraction, ...],
    mapping: dict[str, str],
) -> tuple[Fraction, ...]:
    output = [Fraction(0) for _ in VERTICES]
    for source_index, source in enumerate(VERTICES):
        target = mapping[source]
        output[VERTICES.index(target)] = weight[source_index]
    return tuple(output)


def _component(*vertices: Vertex) -> Component:
    return canonical_component(vertices)


def _zero_vector(length: int) -> list[Fraction]:
    return [Fraction(0) for _ in range(length)]


def _sigma_vector(system: H1System, component: Component) -> list[Fraction]:
    vector = _zero_vector(len(system.variables))
    for root in component:
        _add_term(vector, system, component, root)
    return vector


def _add_term(
    vector: list[Fraction],
    system: H1System,
    component: Component,
    root: Vertex,
    coefficient: Fraction | int = 1,
) -> None:
    vector[system.variable_index[(component, root)]] += Fraction(coefficient)


def _weight_from_json(weights: dict[str, Any]) -> tuple[Fraction, ...]:
    return tuple(parse_fraction(weights[vertex], f"weights.{vertex}") for vertex in VERTICES)


def _exact_primal_dual_from_basis(
    rows: tuple[SparseRow, ...],
    rhs: tuple[Fraction, ...],
    max_objective: tuple[Fraction, ...],
    basis: tuple[int, ...],
    nonbasis: tuple[int, ...],
    variable_count: int,
) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    if -1 in basis:
        raise ValueError("cannot reconstruct exact packet LP with artificial variable in basis")
    row_count = len(rows)
    basis_set = set(basis)
    basic_originals = [index for index in basis if 0 <= index < variable_count]
    nonbasic_slack_rows = [
        index - variable_count
        for index in range(variable_count, variable_count + row_count)
        if index not in basis_set
    ]
    if len(basic_originals) != len(nonbasic_slack_rows):
        raise ValueError(
            "basis shape is not reconstructible: "
            f"{len(basic_originals)} basic originals vs "
            f"{len(nonbasic_slack_rows)} nonbasic slacks"
        )
    matrix = [
        [rows[row].get(variable, Fraction(0)) for variable in basic_originals]
        for row in nonbasic_slack_rows
    ]
    tight_rhs = [rhs[row] for row in nonbasic_slack_rows]
    basic_values = _solve_square_linear_system(matrix, tight_rhs) if basic_originals else []
    coefficients = [Fraction(0) for _ in range(variable_count)]
    for variable, value in zip(basic_originals, basic_values):
        coefficients[variable] = value

    dual_rows = [
        index - variable_count
        for index in nonbasis
        if variable_count <= index < variable_count + row_count
    ]
    dual_system = [
        [rows[row].get(variable, Fraction(0)) for row in dual_rows]
        for variable in basic_originals
    ]
    dual_values = (
        _solve_square_linear_system(
            dual_system,
            [max_objective[variable] for variable in basic_originals],
        )
        if basic_originals
        else []
    )
    dual = [Fraction(0) for _ in range(row_count)]
    for row, value in zip(dual_rows, dual_values):
        dual[row] = value
    return tuple(coefficients), tuple(dual)


def _verify_lp_solution(
    rows: tuple[SparseRow, ...],
    rhs: tuple[Fraction, ...],
    max_objective: tuple[Fraction, ...],
    coefficients: tuple[Fraction, ...],
    residual: tuple[Fraction, ...],
    dual: tuple[Fraction, ...],
    optimum: Fraction,
) -> None:
    if min(coefficients, default=Fraction(0)) < 0:
        raise ValueError("packet LP primal has a negative coefficient")
    if min(residual, default=Fraction(0)) < 0:
        raise ValueError("packet LP primal has a negative residual")
    if min(dual, default=Fraction(0)) < 0:
        raise ValueError("packet LP dual has a negative coordinate price")
    for row, row_rhs in enumerate(rhs):
        lhs = sum(
            rows[row].get(variable, Fraction(0)) * coefficients[variable]
            for variable in range(len(coefficients))
        )
        if row_rhs - lhs != residual[row]:
            raise ValueError("packet LP residual mismatch")
    for variable, coefficient in enumerate(max_objective):
        lhs = sum(rows[row].get(variable, Fraction(0)) * dual[row] for row in range(len(rows)))
        if lhs < coefficient:
            raise ValueError("packet LP dual is not feasible")
    primal_value = sum(max_objective[index] * coefficients[index] for index in range(len(coefficients)))
    dual_value = sum(rhs[row] * dual[row] for row in range(len(rows)))
    if primal_value != optimum or dual_value != optimum:
        raise ValueError(
            f"packet LP strong-duality mismatch: primal={primal_value}, "
            f"dual={dual_value}, optimum={optimum}"
        )


def _mass_one_coefficients(coefficients: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    total = sum(coefficients)
    if total < 1:
        raise ValueError("cannot scale a deficient packet solution to mass 1")
    if total == 1:
        return coefficients
    return tuple(value / total for value in coefficients)


def _residual_from_coefficients(
    objective: tuple[Fraction, ...],
    atoms: tuple[PacketAtom, ...],
    coefficients: tuple[Fraction, ...],
) -> tuple[Fraction, ...]:
    return tuple(
        objective[coordinate]
        - sum(coefficients[index] * atoms[index].vector[coordinate] for index in range(len(atoms)))
        for coordinate in range(len(objective))
    )


def _verify_mass_one_factorization(
    objective: tuple[Fraction, ...],
    atoms: tuple[PacketAtom, ...],
    coefficients: tuple[Fraction, ...],
    residual: tuple[Fraction, ...],
) -> None:
    if len(coefficients) != len(atoms):
        raise ValueError("coefficient count does not match packet atoms")
    if len(residual) != len(objective):
        raise ValueError("residual length does not match objective")
    if sum(coefficients) != 1:
        raise ValueError("packet mass is not exactly 1")
    if min(coefficients, default=Fraction(0)) < 0:
        raise ValueError("negative packet coefficient")
    if min(residual, default=Fraction(0)) < 0:
        raise ValueError("negative residual coordinate")
    recomputed = _residual_from_coefficients(objective, atoms, coefficients)
    if recomputed != residual:
        raise ValueError("residual does not equal objective minus packet combination")


def _verify_packet_primal(
    objective: tuple[Fraction, ...],
    atoms: tuple[PacketAtom, ...],
    coefficients: tuple[Fraction, ...],
    residual: tuple[Fraction, ...],
    claimed_mass: Fraction,
) -> None:
    if len(coefficients) != len(atoms):
        raise ValueError("coefficient count does not match packet atoms")
    if len(residual) != len(objective):
        raise ValueError("residual length does not match objective")
    if min(coefficients, default=Fraction(0)) < 0:
        raise ValueError("negative packet coefficient")
    if min(residual, default=Fraction(0)) < 0:
        raise ValueError("negative residual coordinate")
    if sum(coefficients) != claimed_mass:
        raise ValueError("packet mass does not match claimed optimum")
    recomputed = _residual_from_coefficients(objective, atoms, coefficients)
    if recomputed != residual:
        raise ValueError("residual does not equal objective minus packet combination")


def _verify_dual_upper_bound(
    objective: tuple[Fraction, ...],
    atoms: tuple[PacketAtom, ...],
    dual: tuple[Fraction, ...],
    claimed_upper_bound: Fraction,
) -> None:
    if min(dual, default=Fraction(0)) < 0:
        raise ValueError("negative dual coordinate price")
    for atom in atoms:
        atom_price = sum(atom.vector[index] * dual[index] for index in range(len(dual)))
        if atom_price < 1:
            raise ValueError("dual upper-bound certificate underprices a packet atom")
    objective_price = sum(objective[index] * dual[index] for index in range(len(dual)))
    if objective_price != claimed_upper_bound:
        raise ValueError("dual upper-bound objective mismatch")


def _coordinate_system_json(system: H1System) -> dict[str, Any]:
    return {
        "vertices": list(VERTICES),
        "definition": "H1 coordinates z[S,v] for connected S and v in S",
        "connected_subset_count": len(system.connected_subsets),
        "variable_count": len(system.variables),
        "variables": [
            {
                "index": index,
                "key": variable_key(variable),
                "component": list(variable[0]),
                "root": variable[1],
            }
            for index, variable in enumerate(system.variables)
        ],
    }


def _atom_json(system: H1System, atom: PacketAtom) -> dict[str, Any]:
    return {
        "id": atom.atom_id,
        "kind": atom.kind,
        "parameters": atom.parameters,
        "nonzero_terms": _nonzero_terms(system, atom.vector),
    }


def _kind_counts(atoms: tuple[PacketAtom, ...]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for atom in atoms:
        counts[atom.kind] = counts.get(atom.kind, 0) + 1
    return counts


def _nonzero_terms(system: H1System, vector: tuple[Fraction, ...]) -> list[dict[str, Any]]:
    return [
        {
            "coordinate": variable_key(system.variables[index]),
            "component": list(system.variables[index][0]),
            "root": system.variables[index][1],
            "value": rational_to_string(value),
        }
        for index, value in enumerate(vector)
        if value != 0
    ]


def _vector_from_terms(system: H1System, terms: list[dict[str, Any]]) -> tuple[Fraction, ...]:
    index_by_key = {variable_key(variable): index for index, variable in enumerate(system.variables)}
    vector = [Fraction(0) for _ in system.variables]
    for term in terms:
        key = term["coordinate"]
        if key not in index_by_key:
            raise ValueError(f"unknown coordinate {key}")
        vector[index_by_key[key]] = parse_fraction(term["value"], key)
    return tuple(vector)


def _verify_atom_catalog(
    system: H1System,
    catalog: list[dict[str, Any]],
    atoms: tuple[PacketAtom, ...],
) -> None:
    catalog_by_id = {entry["id"]: entry for entry in catalog}
    if set(catalog_by_id) != {atom.atom_id for atom in atoms}:
        raise ValueError("packet atom catalog id set mismatch")
    for atom in atoms:
        vector = _vector_from_terms(system, catalog_by_id[atom.atom_id]["nonzero_terms"])
        if vector != atom.vector:
            raise ValueError(f"packet atom catalog vector mismatch for {atom.atom_id}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m src.ds22_simplex_augmented_packet_conic"
    )
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--atlas", type=Path, default=DEFAULT_ATLAS)
    parser.add_argument("--factorizations", type=Path, default=DEFAULT_FACTORIZATIONS)
    parser.add_argument("--residuals", type=Path, default=DEFAULT_RESIDUALS)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--verify", action="store_true", help="verify existing artifacts")
    args = parser.parse_args(argv)

    if args.verify:
        summary = verify_artifact_files(args.factorizations, args.residuals, args.atlas)
        print(
            "verified ds22 simplex-augmented packet conic artifacts: "
            f"orbit_representatives={summary['orbit_representatives']} "
            f"packet_atoms={summary['packet_atoms']} "
            f"five_packet_failures={summary['five_packet_failures']}"
        )
        return 0

    result = write_artifacts(
        certificate_path=args.certificate,
        atlas_path=args.atlas,
        factorization_path=args.factorizations,
        residual_path=args.residuals,
        report_path=args.report,
    )
    print(
        "wrote ds22 simplex-augmented packet conic artifacts: "
        f"atlas={result['atlas']} "
        f"factorizations={result['factorizations']} "
        f"residuals={result['residuals']} "
        f"report={result['report']} "
        f"orbit_representatives={result['orbit_representatives']} "
        f"packet_atoms={result['packet_atoms']} "
        f"five_packet_failures={result['five_packet_failures']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
