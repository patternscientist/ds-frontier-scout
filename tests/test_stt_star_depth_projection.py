import unittest
from fractions import Fraction

from scripts.stt_checker.star_depth_projection import (
    build_star_hierarchy_lp,
    build_symmetric_star_hierarchy_lp,
    evaluate_objective,
    star_connected_subsets,
    star_topology,
    stt_depth_optimum,
    structural_star_stts,
    verify_structural_stts,
)


class StarDepthProjectionModelTests(unittest.TestCase):
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
        self.assertTrue(verify_structural_stts(1))
        self.assertTrue(verify_structural_stts(2))
        self.assertTrue(verify_structural_stts(3))
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
        weights = (0, 1, 1, 1, 1)
        full = evaluate_objective(4, weights, 2, "full")
        symmetric = evaluate_objective(4, weights, 2, "symmetric", symmetric=True)
        self.assertEqual(full.h_optimum, symmetric.h_optimum)
        self.assertEqual(symmetric.gap, Fraction(0))
        self.assertTrue(symmetric.certificate.verified)

    def test_model_counts_for_four_leaf_star_h2(self):
        lp = build_star_hierarchy_lp(4, (1, 1, 1, 1, 1), k=2)
        self.assertEqual(len(lp.variables), 52)
        self.assertEqual(len(lp.rows), 520)
        symmetric = build_symmetric_star_hierarchy_lp(4, 1, 1, k=2)
        self.assertEqual(symmetric.symmetric_variable_labels, ("c_0", "c_1", "c_2", "c_3", "c_4", "l_1", "l_2", "l_3", "l_4"))


if __name__ == "__main__":
    unittest.main()
