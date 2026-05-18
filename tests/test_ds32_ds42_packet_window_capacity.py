import copy
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

import pytest

from src.ds32_ds42_packet_window_capacity import (
    DEFAULT_DS32_FACTORIZATIONS,
    DEFAULT_DS42_FACTORIZATIONS,
    DEFAULT_GAP_WITNESSES,
    FACTORIZATION_SCHEMA,
    GAP_SCHEMA,
    coordinate_capacity,
    h1_coordinate_system,
    packet_atoms,
    packet_lp_model,
    solve_packet_window_lp,
    true_depth_catalog,
    true_optimum,
    verify_artifact_files,
    verify_artifacts,
)


def test_topology_depth_and_packet_counts():
    expected = {
        3: {
            "connected": 49,
            "variables": 177,
            "schedules": 1135,
            "depth_vectors": 1135,
            "atoms": 228,
            "kinds": Counter(
                {"Sigma": 84, "Lambda": 6, "Gamma": 6, "Delta": 12, "Omega": 12, "Pi": 108}
            ),
        },
        4: {
            "connected": 90,
            "variables": 382,
            "schedules": 7284,
            "depth_vectors": 7284,
            "atoms": 456,
            "kinds": Counter(
                {"Sigma": 168, "Lambda": 12, "Gamma": 12, "Delta": 24, "Omega": 24, "Pi": 216}
            ),
        },
    }
    for k, counts in expected.items():
        system = h1_coordinate_system(k)
        catalog = true_depth_catalog(system.topology)
        atoms = packet_atoms(system)
        assert len(system.connected_subsets) == counts["connected"]
        assert len(system.variables) == counts["variables"]
        assert catalog.schedule_count == counts["schedules"]
        assert catalog.depth_vector_count == counts["depth_vectors"]
        assert len(atoms) == counts["atoms"]
        assert Counter(atom.kind for atom in atoms) == counts["kinds"]
        assert all(min(atom.vector) >= 0 for atom in atoms)


def test_uniform_packet_window_lp_closes_exactly():
    for k, expected_optimum in ((3, Fraction(8)), (4, Fraction(9))):
        system = h1_coordinate_system(k)
        catalog = true_depth_catalog(system.topology)
        weight = tuple(Fraction(1) for _ in system.topology.vertices)
        capacity = coordinate_capacity(system, weight)
        solution = solve_packet_window_lp(packet_lp_model(system), capacity)
        assert true_optimum(catalog, weight) == expected_optimum
        assert solution.status == 0
        assert solution.optimum == expected_optimum
        assert min(solution.coefficients) >= 0
        assert min(solution.residual) >= 0


@pytest.fixture(scope="module")
def packet_artifacts():
    return (
        json.loads(Path(DEFAULT_DS32_FACTORIZATIONS).read_text(encoding="utf-8")),
        json.loads(Path(DEFAULT_DS42_FACTORIZATIONS).read_text(encoding="utf-8")),
        json.loads(Path(DEFAULT_GAP_WITNESSES).read_text(encoding="utf-8")),
    )


def test_checked_artifacts_verify_exactly(packet_artifacts):
    ds32, ds42, gaps = packet_artifacts
    assert ds32["schema"] == FACTORIZATION_SCHEMA
    assert ds42["schema"] == FACTORIZATION_SCHEMA
    assert gaps["schema"] == GAP_SCHEMA
    summary = verify_artifact_files()
    assert summary["ds32_factorizations"] == 2186
    assert summary["ds42_factorizations"] == 255
    assert summary["gap_witnesses"] == 0
    assert summary["ds32_max_denominator"] == 3
    assert summary["ds42_max_denominator"] == 2


def test_artifacts_cover_declared_finite_universes(packet_artifacts):
    ds32, ds42, gaps = packet_artifacts
    assert ds32["universe"]["weight_count"] == 3**7 - 1
    assert ds42["universe"]["weight_count"] == 2**8 - 1
    assert ds32["factorization_count"] == ds32["universe"]["weight_count"]
    assert ds42["factorization_count"] == ds42["universe"]["weight_count"]
    assert ds32["failures"] == []
    assert ds42["failures"] == []
    assert gaps["status"] == "no_gaps_found"
    assert gaps["witnesses"] == []


def test_verifier_rejects_packet_coefficient_tampering(packet_artifacts):
    ds32, ds42, gaps = packet_artifacts
    tampered = copy.deepcopy(ds32)
    first = next(
        entry
        for entry in tampered["factorizations"]
        if entry["nonzero_packet_coefficients"]
    )
    first["nonzero_packet_coefficients"][0]["coefficient"] = "1/999"
    with pytest.raises(ValueError, match="mass|residual|minimum"):
        verify_artifacts(tampered, ds42, gaps)
