import json
from fractions import Fraction
from pathlib import Path
import unittest

from src.ds22_depth_inclusion_check import _verify_dual_entry, parse_rational
from src.ds22_h1_depth_polytope import (
    DEFAULT_CERTIFICATE,
    depth_objective_coefficients,
    h1_system,
)
from src.ds22_true_schedules import VERTICES, enumerate_true_schedules


class DS22DepthInclusionTests(unittest.TestCase):
    @classmethod
    def certificate(cls):
        path = Path(DEFAULT_CERTIFICATE)
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def test_h1_and_true_schedule_counts(self):
        system = h1_system()
        schedules = enumerate_true_schedules()
        self.assertEqual(len(system.connected_subsets), 28)
        self.assertEqual(len(system.variables), 84)
        self.assertEqual(system.simplex_rows, 28)
        self.assertEqual(system.heredity_rows, 380)
        self.assertEqual(len(system.rows), 436)
        self.assertEqual(len(schedules), 214)
        self.assertEqual(len({schedule.depth_vector for schedule in schedules}), 214)

    def test_checked_in_certificate_summary(self):
        data = self.certificate()
        self.assertEqual(data["schema"], "ds22_full_objective_depth_inclusion_v0")
        self.assertEqual(data["result"], "success")
        self.assertEqual(data["cell_cover"]["blocker_vertex_count"], 943)
        self.assertEqual(len(data["h1_dual_certificates"]), 943)
        self.assertEqual(
            data["result_statement"],
            "certificate-backed DS(2,2) full-objective H1 exactness",
        )

    def test_first_certificate_duals_verify_exactly(self):
        data = self.certificate()
        system = h1_system()
        blockers = {
            entry["id"]: tuple(
                parse_rational(entry["weights"][vertex], f"{entry['id']}.{vertex}")
                for vertex in VERTICES
            )
            for entry in data["cell_cover"]["blocker_vertices"]
        }
        for entry in data["h1_dual_certificates"][:10]:
            with self.subTest(weight_id=entry["weight_id"]):
                _verify_dual_entry(system, blockers[entry["weight_id"]], entry)

    def test_depth_objective_uses_user_strict_ancestor_direction(self):
        system = h1_system()
        coeffs = depth_objective_coefficients(
            system, tuple(Fraction(1 if vertex == "a" else 0) for vertex in VERTICES)
        )
        nonzero = {
            system.variables[index]: value
            for index, value in enumerate(coeffs)
            if value
        }
        self.assertEqual(
            set(nonzero),
            {
                (("a", "b"), "b"),
                (("a", "b", "r"), "r"),
                (("a", "b", "s"), "s"),
                (("a", "li"), "li"),
                (("a", "lj"), "lj"),
            },
        )


if __name__ == "__main__":
    unittest.main()

