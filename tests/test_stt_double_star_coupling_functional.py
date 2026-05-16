import unittest
from fractions import Fraction
from tempfile import TemporaryDirectory
from pathlib import Path

from scripts.stt_checker.double_star_coupling_functional import (
    build_reduced_coupling_lp,
    evaluate_reduced_objective,
    gamma_allocation_value,
    left_interval,
    right_interval,
    solve_reduced_coupling_lp_exact,
    write_report,
)


class CouplingFunctionalIntervalTests(unittest.TestCase):
    def test_left_interval_uses_prompt_bounds(self):
        self.assertEqual(
            left_interval(Fraction(3, 5), Fraction(1, 4), Fraction(2, 5)),
            (Fraction(1, 5), Fraction(3, 5)),
        )
        self.assertEqual(
            left_interval(Fraction(1, 3), Fraction(3, 4), Fraction(5, 6)),
            (Fraction(0), Fraction(1, 6)),
        )

    def test_right_interval_uses_prompt_bounds(self):
        self.assertEqual(
            right_interval(Fraction(3, 5), Fraction(4, 5), Fraction(1, 2)),
            (Fraction(3, 10), Fraction(1, 2)),
        )
        self.assertEqual(
            right_interval(Fraction(1, 4), Fraction(1, 3), Fraction(5, 6)),
            (Fraction(0), Fraction(1, 6)),
        )


class CouplingFunctionalGammaTests(unittest.TestCase):
    def test_gamma_allocates_to_cheaper_endpoint_first(self):
        cost, vx, vy = gamma_allocation_value(5, 2, Fraction(3, 4), Fraction(1, 2), Fraction(1, 2))
        self.assertEqual((cost, vx, vy), (Fraction(9, 4), Fraction(1, 2), Fraction(1, 4)))

        cost, vx, vy = gamma_allocation_value(1, 7, Fraction(3, 5), Fraction(1, 2), Fraction(4, 5))
        self.assertEqual((cost, vx, vy), (Fraction(3, 5), Fraction(0), Fraction(3, 5)))

    def test_gamma_rejects_infeasible_endpoint_mass(self):
        with self.assertRaises(ValueError):
            gamma_allocation_value(1, 1, Fraction(3, 2), Fraction(1, 2), Fraction(1, 2))


class CouplingFunctionalLPTests(unittest.TestCase):
    def test_reduced_lp_contains_prompt_interval_and_gamma_rows(self):
        lp = build_reduced_coupling_lp(1, 1, (1, 1, 1, 1))
        kinds = {descriptor["kind"] for descriptor in lp.row_descriptors}
        self.assertIn("left_interval_lower_theta_minus_r", kinds)
        self.assertIn("right_interval_lower_q_minus_s", kinds)
        self.assertIn("cross_e_ge_r_plus_ax_minus_ay", kinds)
        self.assertIn("gamma_vsum_ge_e", kinds)

    def test_ds_1_1_uniform_reduced_optimization_matches_stt(self):
        run = evaluate_reduced_objective(1, 1, (1, 1, 1, 1), "uniform")
        self.assertEqual(run.stt_optimum, Fraction(4))
        self.assertEqual(run.reduced_optimum, run.stt_optimum)
        self.assertEqual(run.full_h1.optimum, run.stt_optimum)
        self.assertEqual(run.full_h2.optimum, run.stt_optimum)
        self.assertTrue(run.certificate.verified)

    def test_ds_1_1_heavy_left_reduced_solution_is_exact(self):
        _lp, optimum, values, certificate, status, _active_rows = solve_reduced_coupling_lp_exact(
            1, 1, (8, 1, 1, 1)
        )
        self.assertEqual(optimum, Fraction(5))
        self.assertIn("verified_exact", status)
        self.assertIsNotNone(certificate)
        self.assertTrue(certificate.verified)
        self.assertTrue(all(value >= 0 for value in values))

    def test_report_generator_accepts_precomputed_small_data(self):
        run = evaluate_reduced_objective(1, 1, (1, 1, 1, 1), "uniform")
        data = {
            "settings": {"topologies": ["DS(1,1)"], "small_bound": 1},
            "runs": [run],
        }
        with TemporaryDirectory() as directory:
            report = Path(directory) / "report.md"
            summary = Path(directory) / "summary.json"
            result = write_report(report, summary, data=data)
            self.assertEqual(result["runs"], 1)
            self.assertEqual(result["reduced_gaps"], 0)
            self.assertTrue(report.read_text(encoding="utf-8").startswith("# STT Double-Star Coupling"))
            self.assertIn("stt_double_star_coupling_functional_v0_summary", summary.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
