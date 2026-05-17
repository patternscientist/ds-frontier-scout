import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
import unittest

from src.ds22_h1_depth_polytope import h1_system
from src.ds22_simplex_augmented_packet_conic import (
    DEFAULT_ATLAS,
    DEFAULT_FACTORIZATIONS,
    DEFAULT_RESIDUALS,
    FACTORIZATION_SCHEMA,
    RESIDUAL_SCHEMA,
    SPECIAL_ORBITS,
    packet_atoms,
    parse_fraction,
    solve_representative,
    verify_artifact_files,
)


SPECIAL_DEFICITS = {
    "o011": ("10/11", "1/11"),
    "o055": ("47/56", "9/56"),
    "o057": ("41/50", "9/50"),
    "o058": ("6/7", "1/7"),
    "o069": ("32/39", "7/39"),
    "o080": ("31/36", "5/36"),
}


class DS22SimplexAugmentedPacketConicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.atlas = json.loads(Path(DEFAULT_ATLAS).read_text(encoding="utf-8"))
        cls.factorizations = json.loads(
            Path(DEFAULT_FACTORIZATIONS).read_text(encoding="utf-8")
        )
        cls.residuals = json.loads(Path(DEFAULT_RESIDUALS).read_text(encoding="utf-8"))

    def test_packet_atom_counts_and_coordinate_nonnegativity(self):
        system = h1_system()
        atoms = packet_atoms(system, include_sigma=True)
        self.assertEqual(len(system.connected_subsets), 28)
        self.assertEqual(len(system.variables), 84)
        self.assertEqual(len(atoms), 76)
        self.assertEqual(
            Counter(atom.kind for atom in atoms),
            Counter({"Sigma": 28, "Lambda": 2, "Gamma": 2, "Delta": 4, "Omega": 4, "Pi": 36}),
        )
        self.assertTrue(all(min(atom.vector) >= 0 for atom in atoms))

        no_sigma = packet_atoms(system, include_sigma=False)
        self.assertEqual(len(no_sigma), 48)
        self.assertNotIn("Sigma", {atom.kind for atom in no_sigma})

    def test_checked_artifacts_verify_exactly(self):
        self.assertEqual(self.factorizations["schema"], FACTORIZATION_SCHEMA)
        self.assertEqual(self.residuals["schema"], RESIDUAL_SCHEMA)
        summary = verify_artifact_files()
        self.assertEqual(summary["orbit_representatives"], 302)
        self.assertEqual(summary["packet_atoms"], 76)
        self.assertEqual(summary["five_packet_failures"], 287)

    def test_atlas_has_302_leaf_swap_representatives(self):
        self.assertEqual(self.atlas["source_blocker_vertex_count"], 943)
        self.assertEqual(self.atlas["orbit_representative_count"], 302)
        self.assertEqual(
            {transform["id"] for transform in self.atlas["orbit_group"]["transforms"]},
            {"identity", "swap_left", "swap_right", "swap_left_and_right"},
        )
        reps = {entry["id"]: entry for entry in self.atlas["representatives"]}
        self.assertTrue(set(SPECIAL_ORBITS).issubset(reps))
        self.assertEqual(reps["o069"]["representative_blocker_id"], "w0190")

    def test_special_representatives_need_sigma_mass(self):
        factorizations = {
            entry["orbit_id"]: entry for entry in self.factorizations["factorizations"]
        }
        for orbit_id, (_maximum_mass, deficit) in SPECIAL_DEFICITS.items():
            with self.subTest(orbit_id=orbit_id):
                entry = factorizations[orbit_id]
                self.assertEqual(entry["packet_mass"], "1")
                self.assertEqual(entry["sigma_mass"], deficit)
                self.assertGreater(parse_fraction(entry["sigma_mass"]), 0)

    def test_five_packet_deficits_for_special_representatives(self):
        special = self.residuals["five_packet_without_sigma"]["special_orbit_deficits"]
        for orbit_id, (maximum_mass, deficit) in SPECIAL_DEFICITS.items():
            with self.subTest(orbit_id=orbit_id):
                entry = special[orbit_id]
                self.assertEqual(entry["status"], "deficient")
                self.assertEqual(entry["maximum_packet_mass"], maximum_mass)
                self.assertEqual(entry["deficit"], deficit)
                self.assertLess(parse_fraction(entry["maximum_packet_mass"]), Fraction(1))
                self.assertTrue(entry["dual_upper_bound_terms"])

    def test_rebuild_special_lp_bases_exactly(self):
        reps = {entry["id"]: entry for entry in self.atlas["representatives"]}
        for orbit_id, (maximum_mass, _deficit) in SPECIAL_DEFICITS.items():
            with self.subTest(orbit_id=orbit_id):
                augmented = solve_representative(reps[orbit_id], include_sigma=True)
                self.assertEqual(augmented.status, 0)
                self.assertEqual(augmented.optimum, Fraction(1))
                self.assertEqual(min(augmented.residual), Fraction(0))

                five_packet = solve_representative(reps[orbit_id], include_sigma=False)
                self.assertEqual(five_packet.status, 0)
                self.assertEqual(five_packet.optimum, parse_fraction(maximum_mass))


if __name__ == "__main__":
    unittest.main()
