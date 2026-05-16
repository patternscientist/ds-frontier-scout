import unittest
from fractions import Fraction

from scripts.stt_checker.hereditary_lp import (
    SKZ_LONG_STAR_TOPOLOGY,
    SKZ_LONG_STAR_WEIGHTS,
    build_hereditary_lp,
    compute_tree_paths,
    enumerate_connected_subsets,
    rationalize_solution,
    solve_hereditary_lp,
)
from scripts.stt_checker.topology import TreeTopology


class HereditaryLPEnumerationTests(unittest.TestCase):
    def test_connected_subsets_edge_and_p3(self):
        edge = TreeTopology.from_dict(
            {"n": 2, "vertices": [0, 1], "edges": [[0, 1]]}
        )
        self.assertEqual(
            enumerate_connected_subsets(edge),
            ((0,), (1,), (0, 1)),
        )

        p3 = TreeTopology.from_dict(
            {"n": 3, "vertices": [0, 1, 2], "edges": [[0, 1], [1, 2]]}
        )
        self.assertEqual(
            enumerate_connected_subsets(p3),
            ((0,), (1,), (2,), (0, 1), (1, 2), (0, 1, 2)),
        )

    def test_connected_subsets_skz_count(self):
        topology = TreeTopology.from_dict(SKZ_LONG_STAR_TOPOLOGY)
        subsets = enumerate_connected_subsets(topology)
        self.assertEqual(len(subsets), 36)
        self.assertIn((0, 1, 2, 3, 4, 5, 6), subsets)
        self.assertNotIn((0, 2), subsets)


class HereditaryLPPathTests(unittest.TestCase):
    def test_compute_tree_paths_p3(self):
        topology = TreeTopology.from_dict(
            {"n": 3, "vertices": [0, 1, 2], "edges": [[0, 1], [1, 2]]}
        )
        paths = compute_tree_paths(topology)
        self.assertEqual(paths[(0, 0)], (0,))
        self.assertEqual(paths[(0, 2)], (0, 1, 2))
        self.assertEqual(paths[(2, 0)], (2, 1, 0))

    def test_compute_tree_paths_skz_long_star(self):
        topology = TreeTopology.from_dict(SKZ_LONG_STAR_TOPOLOGY)
        paths = compute_tree_paths(topology)
        self.assertEqual(paths[(0, 4)], (0, 1, 2, 3, 4))
        self.assertEqual(paths[(4, 6)], (4, 3, 2, 5, 6))


class HereditaryLPConstructionTests(unittest.TestCase):
    def test_edge_lp_construction_and_solve(self):
        topology = TreeTopology.from_dict(
            {"n": 2, "vertices": [0, 1], "edges": [[0, 1]]}
        )
        lp = build_hereditary_lp(topology, [1, 1])
        self.assertEqual(len(lp.connected_subsets), 3)
        self.assertEqual(len(lp.variables), 4)
        self.assertEqual(lp.simplex_constraint_count, 3)
        self.assertEqual(len(lp.heredity_constraints), 2)
        self.assertEqual(
            lp.objective_coefficients[lp.variable_index[((0, 1), 0)]],
            Fraction(1),
        )
        self.assertEqual(
            lp.objective_coefficients[lp.variable_index[((0, 1), 1)]],
            Fraction(1),
        )

        solution = solve_hereditary_lp(topology, [1, 1])
        self.assertEqual(solution.status, 0)
        self.assertAlmostEqual(solution.objective_value, 1.0)
        self.assertEqual(rationalize_solution(solution).exact_objective, Fraction(1))

    def test_p3_lp_construction_and_good_root_weights(self):
        topology = TreeTopology.from_dict(
            {"n": 3, "vertices": [0, 1, 2], "edges": [[0, 1], [1, 2]]}
        )
        lp = build_hereditary_lp(topology, [1, 4, 4])
        self.assertEqual(len(lp.connected_subsets), 6)
        self.assertEqual(len(lp.variables), 10)
        self.assertEqual(lp.simplex_constraint_count, 6)
        self.assertEqual(len(lp.heredity_constraints), 11)

        solution = solve_hereditary_lp(topology, [1, 4, 4])
        self.assertEqual(solution.status, 0)
        self.assertAlmostEqual(solution.objective_value, 5.0)
        rational = rationalize_solution(solution)
        self.assertTrue(rational.feasible)
        self.assertEqual(rational.exact_objective, Fraction(5))


class HereditaryLPSKZRegressionTests(unittest.TestCase):
    def test_skz_long_star_solve_has_fractional_certificate_below_30(self):
        topology = TreeTopology.from_dict(SKZ_LONG_STAR_TOPOLOGY)
        lp = build_hereditary_lp(topology, SKZ_LONG_STAR_WEIGHTS)
        self.assertEqual(len(lp.connected_subsets), 36)
        self.assertEqual(len(lp.variables), 120)
        self.assertEqual(lp.simplex_constraint_count, 36)
        self.assertEqual(len(lp.heredity_constraints), 681)

        solution = solve_hereditary_lp(topology, SKZ_LONG_STAR_WEIGHTS)
        self.assertEqual(solution.status, 0)
        self.assertAlmostEqual(solution.objective_value, 29.5)
        self.assertLess(solution.objective_value, 30.0)
        rational = rationalize_solution(solution, max_denominator=2)
        self.assertTrue(rational.feasible)
        self.assertEqual(rational.exact_objective, Fraction(59, 2))
        self.assertEqual(rational.max_simplex_residual, Fraction(0))
        self.assertEqual(rational.max_heredity_violation, Fraction(0))


if __name__ == "__main__":
    unittest.main()
