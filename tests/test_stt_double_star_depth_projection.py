import unittest
from collections import Counter
from fractions import Fraction
from tempfile import TemporaryDirectory
from pathlib import Path

from scripts.stt_checker.double_star_depth_projection import (
    double_star_spec,
    double_star_topology,
    enumerate_normal_form_stts,
    evaluate_objective,
    four_set_h2_rectangles,
    verify_normal_form_enumeration,
    write_report,
)
from scripts.stt_checker.hereditary_lp import build_hereditary_lp


class DoubleStarNormalFormTests(unittest.TestCase):
    def test_normal_form_enumeration_matches_generic_recursive_enumeration(self):
        expected_counts = {(1, 1): 14, (2, 1): 51, (2, 2): 214}
        for (m, n), count in expected_counts.items():
            with self.subTest(m=m, n=n):
                self.assertTrue(verify_normal_form_enumeration(m, n))
                self.assertEqual(len(enumerate_normal_form_stts(m, n)), count)


class DoubleStarModelConstructionTests(unittest.TestCase):
    def test_h1_h2_model_counts_for_small_double_stars(self):
        expected = {
            (1, 1): (10, 20, 36, 8),
            (2, 1): (17, 42, 124, 85),
            (2, 2): (28, 84, 380, 572),
        }
        for (m, n), counts in expected.items():
            with self.subTest(m=m, n=n):
                topology = double_star_topology(m, n)
                h1 = build_hereditary_lp(topology, [1] * topology.n, relaxation="h1")
                h2 = build_hereditary_lp(topology, [1] * topology.n, relaxation="h2")
                self.assertEqual(
                    (
                        len(h1.connected_subsets),
                        len(h1.variables),
                        len(h1.heredity_constraints),
                        len(h2.rectangle_constraints),
                    ),
                    counts,
                )


class DoubleStarCertificateTests(unittest.TestCase):
    def test_h1_exact_certificate_and_h2_sandwich_for_no_gap_case(self):
        run = evaluate_objective(2, 1, (8, 1, 1, 1, 1), "one_heavy_left_leaf")
        self.assertEqual(run.stt_optimum, Fraction(8))
        self.assertEqual(run.h1.optimum, run.stt_optimum)
        self.assertEqual(run.h2.optimum, run.stt_optimum)
        self.assertEqual(run.h1_gap, Fraction(0))
        self.assertTrue(run.h1.certificate.verified)
        self.assertEqual(
            run.h2.certificate_status,
            "exact_by_h1_equals_stt_sandwich_no_separate_h2_primal",
        )

    def test_no_gap_regression_cases(self):
        cases = [
            (1, 1, (1, 1, 1, 1), "uniform"),
            (1, 1, (9, 1, 1, 6), "asym_leaf_center"),
            (2, 2, (8, 1, 1, 1, 1, 8), "two_sides"),
        ]
        for m, n, weights, family in cases:
            with self.subTest(m=m, n=n, weights=weights):
                run = evaluate_objective(m, n, weights, family)
                self.assertEqual(run.h1_gap, Fraction(0))
                self.assertEqual(run.h2_gap, Fraction(0))
                self.assertTrue(run.h1.certificate.verified)

    def test_four_set_rectangles_group_by_center_roots_on_ds_1_1(self):
        spec = double_star_spec(1, 1)
        grouped = Counter(row["root"] for row in four_set_h2_rectangles(spec))
        self.assertEqual(grouped, Counter({"a": 3, "b": 3}))

    def test_report_generator_accepts_precomputed_small_data(self):
        run = evaluate_objective(1, 1, (1, 1, 1, 1), "uniform")
        data = {
            "settings": {"topologies": ["DS(1,1)"], "small_bound": 1},
            "normal_form_checks": {"DS(1,1)": True},
            "runs": [run],
            "skipped_h2": [],
        }
        with TemporaryDirectory() as directory:
            report = Path(directory) / "report.md"
            summary = Path(directory) / "summary.json"
            result = write_report(report, summary, data=data)
            self.assertEqual(result["runs"], 1)
            self.assertTrue(report.read_text(encoding="utf-8").startswith("# STT Double-Star"))
            self.assertIn("stt_double_star_depth_projection_v0_summary", summary.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
