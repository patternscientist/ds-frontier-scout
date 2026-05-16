import unittest
import json
from fractions import Fraction
from tempfile import TemporaryDirectory
from pathlib import Path

from scripts.stt_checker.star_depth_projection import (
    build_star_hierarchy_lp,
    build_symmetric_star_hierarchy_lp,
    evaluate_objective,
    run_scout,
    star_connected_subsets,
    star_topology,
    stt_depth_optimum,
    structural_star_stts,
    verify_structural_stts,
    write_report,
)
from scripts.stt_checker.star_audit import (
    depth_dominant_audit,
    feasibility_audit,
    star4_instance,
)


class StarDepthProjectionModelTests(unittest.TestCase):
    _scout_data = None

    @classmethod
    def scout_data(cls):
        if cls._scout_data is None:
            cls._scout_data = run_scout()
        return cls._scout_data

    def test_star_connected_sets_are_singletons_and_center_sets(self):
        self.assertEqual(
            star_connected_subsets(3),
            (
                (0,),
                (1,),
                (2,),
                (3,),
                (0, 1),
                (0, 2),
                (0, 3),
                (0, 1, 2),
                (0, 1, 3),
                (0, 2, 3),
                (0, 1, 2, 3),
            ),
        )
        topology = star_topology(3)
        self.assertEqual(topology.edges, ((0, 1), (0, 2), (0, 3)))

    def test_structural_stt_enumeration_matches_generic_small_stars(self):
        for d in range(1, 6):
            with self.subTest(d=d):
                self.assertTrue(verify_structural_stts(d))
        self.assertEqual(len(structural_star_stts(4)), 65)

    def test_structural_stt_optimum_can_query_all_leaves_before_center(self):
        optimum, vector = stt_depth_optimum(2, (0, 1, 1))
        self.assertEqual(optimum, Fraction(1))
        self.assertIn(vector, ((2, 0, 1), (2, 1, 0)))

    def test_full_h2_objectives_match_stt_for_probe_weights(self):
        for weights in (
            (10, 1, 1, 1),
            (0, 1, 1, 1),
            (1, 8, 8, 1),
            (2, 0, 1, 2),
        ):
            with self.subTest(weights=weights):
                result = evaluate_objective(3, weights, 2, "probe")
                self.assertEqual(result.gap, Fraction(0))
                self.assertTrue(result.certificate.verified)

    def test_h3_h4_objectives_match_stt_for_tiny_probe(self):
        for k in (3, 4):
            with self.subTest(k=k):
                result = evaluate_objective(3, (1, 8, 8, 1), k, "two_leaf_heavy")
                self.assertEqual(result.gap, Fraction(0))
                self.assertTrue(result.certificate.verified)

    def test_symmetric_reduction_matches_full_h2(self):
        for d in range(1, 5):
            for center_weight, leaf_weight in ((0, 1), (1, 1), (4, 1), (10, 1), (1, 4)):
                weights = tuple([Fraction(center_weight)] + [Fraction(leaf_weight)] * d)
                with self.subTest(d=d, weights=weights):
                    full = evaluate_objective(d, weights, 2, "full")
                    symmetric = evaluate_objective(d, weights, 2, "symmetric", symmetric=True)
                    self.assertEqual(full.h_optimum, symmetric.h_optimum)
                    self.assertGreaterEqual(symmetric.gap, Fraction(0))
                    self.assertTrue(symmetric.certificate.verified)

    def test_model_counts_for_four_leaf_star_h2(self):
        lp = build_star_hierarchy_lp(4, (1, 1, 1, 1, 1), k=2)
        self.assertEqual(len(lp.variables), 52)
        self.assertEqual(len(lp.rows), 520)
        symmetric = build_symmetric_star_hierarchy_lp(4, 1, 1, k=2)
        self.assertEqual(symmetric.symmetric_variable_labels, ("c_0", "c_1", "c_2", "c_3", "c_4", "l_1", "l_2", "l_3", "l_4"))

    def test_audited_star4_z_obstruction_is_h2_feasible_and_depth_dominated(self):
        star = star4_instance()
        self.assertTrue(feasibility_audit(star).feasible)
        self.assertTrue(depth_dominant_audit(star).is_member)

    def test_reported_objectives_have_nonnegative_gap_and_exact_certificates(self):
        data = self.scout_data()
        reported = data["full_results"] + data["h3_h4_results"] + data["symmetric_results"]
        self.assertGreater(len(reported), 0)
        for result in reported:
            with self.subTest(d=result.d, k=result.k, family=result.family, weights=result.weights):
                self.assertGreaterEqual(result.gap, Fraction(0))
                self.assertTrue(result.certificate.verified)

    def test_report_generator_writes_compact_symmetric_h2_summary(self):
        with TemporaryDirectory() as directory:
            report_path = Path(directory) / "report.md"
            summary_path = Path(directory) / "summary.json"
            write_report(report_path, summary_path, data=self.scout_data())
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
        self.assertEqual(summary["schema"], "stt_star_symmetric_h2_summary_v0")
        self.assertEqual(len(summary["runs"]), 40)
        for run in summary["runs"]:
            with self.subTest(run=run):
                self.assertIn("d", run)
                self.assertIn("weights", run)
                self.assertIn("stt_optimum", run)
                self.assertIn("h2_optimum", run)
                self.assertIn("gap", run)
                self.assertEqual(
                    run["certificate_verification_status"],
                    "verified_exact_primal_dual_after_floating_basis_reconstruction",
                )


if __name__ == "__main__":
    unittest.main()
