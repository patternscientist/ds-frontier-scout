from collections import Counter
import unittest

from scripts.stt_checker.ds21_pinned_boundary import (
    _pinned_boundary_cells,
    run_pinned_boundary_coverage,
)


class DS21PinnedBoundaryTests(unittest.TestCase):
    def test_pinned_boundary_enumerator_is_targeted(self):
        cells = tuple(_pinned_boundary_cells())
        self.assertEqual(len(cells), 6336)
        self.assertEqual(
            Counter(cell.family for cell in cells),
            {"A-pinned": 3168, "B-pinned": 3168},
        )
        self.assertTrue(all(cell.active_facets for cell in cells))
        self.assertEqual(
            {row for cell in cells for row in cell.psi_active},
            {25, 26, 27, 28},
        )

    def test_bounded_pinned_boundary_smoke_run_is_rational(self):
        data = run_pinned_boundary_coverage(cell_limit=32)
        self.assertEqual(data["schema"], "stt_ds21_pinned_boundary_v2")
        self.assertEqual(data["settings"]["full_pinned_cell_count"], 6336)
        self.assertEqual(data["settings"]["pinned_cells_considered"], 32)
        self.assertFalse(
            any(
                cert.outcome == "rational_reduced_counterexample"
                for cert in data["pinned_boundary_certificates"]
            )
        )
        for cert in data["pinned_boundary_certificates"]:
            self.assertIn(
                cert.cell_feasibility.status,
                {
                    "verified_exact_primal_from_basis",
                    "verified_exact_after_solution_rationalization",
                    "infeasible in simplex phase I",
                },
            )


if __name__ == "__main__":
    unittest.main()
