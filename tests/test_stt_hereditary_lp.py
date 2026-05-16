import unittest
from fractions import Fraction
import json
from pathlib import Path

from scripts.stt_checker.hereditary_lp import (
    RectangleConstraint,
    SKZ_LONG_STAR_TOPOLOGY,
    SKZ_LONG_STAR_WEIGHTS,
    build_hereditary_lp,
    compute_tree_paths,
    enumerate_connected_subsets,
    rationalize_solution,
    solve_hereditary_lp,
)
from scripts.stt_checker.topology import TreeTopology


ROOT = Path(__file__).resolve().parents[1]
H1_SKZ_RESULT = ROOT / "examples" / "stt_lp" / "skz_long_star_7_hereditary_lp_result.json"


def parse_fraction(text):
    return Fraction(text)


def load_h1_skz_rational_values(lp):
    payload = json.loads(H1_SKZ_RESULT.read_text(encoding="utf-8"))
    values = {variable: Fraction(0) for variable in lp.variables}
    for item in payload["rationalized_certificate"]["nonzero_z_variables"]:
        values[(tuple(item["component"]), item["root"])] = parse_fraction(item["value"])
    return values


def rectangle_value(values, constraint):
    root = constraint.root
    return (
        values[(constraint.base, root)]
        - values[(constraint.extension_a, root)]
        - values[(constraint.extension_b, root)]
        + values[(constraint.union, root)]
    )


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

    def test_p3_path_weights_1_4_4(self):
        path_topology = TreeTopology.from_dict(
            {"n": 3, "vertices": [0, 1, 2], "edges": [[0, 1], [1, 2]]}
        )
        lp = build_hereditary_lp(path_topology, [1, 4, 4])
        self.assertEqual(len(lp.connected_subsets), 6)
        self.assertEqual(len(lp.variables), 10)
        self.assertEqual(lp.simplex_constraint_count, 6)
        self.assertEqual(len(lp.heredity_constraints), 11)

        solution = solve_hereditary_lp(path_topology, [1, 4, 4])
        self.assertEqual(solution.status, 0)
        self.assertAlmostEqual(solution.objective_value, 5.0)
        rational = rationalize_solution(solution)
        self.assertTrue(rational.feasible)
        self.assertEqual(rational.exact_objective, Fraction(5))

    def test_p3_good_root_failure_center_0(self):
        center_topology = TreeTopology.from_dict(
            {"n": 3, "vertices": [0, 1, 2], "edges": [[0, 1], [0, 2]]}
        )
        solution = solve_hereditary_lp(center_topology, [1, 4, 4])
        self.assertEqual(solution.status, 0)
        self.assertAlmostEqual(solution.objective_value, 6.0)
        rational = rationalize_solution(solution)
        self.assertTrue(rational.feasible)
        self.assertEqual(rational.exact_objective, Fraction(6))


class HereditaryLPH2RectangleTests(unittest.TestCase):
    def test_h2_rectangle_enumeration_tiny_trees(self):
        edge = TreeTopology.from_dict(
            {"n": 2, "vertices": [0, 1], "edges": [[0, 1]]}
        )
        edge_lp = build_hereditary_lp(edge, [1, 1], relaxation="h2")
        self.assertEqual(len(edge_lp.rectangle_constraints), 0)

        p3 = TreeTopology.from_dict(
            {"n": 3, "vertices": [0, 1, 2], "edges": [[0, 1], [1, 2]]}
        )
        p3_lp = build_hereditary_lp(p3, [1, 1, 1], relaxation="h2")
        self.assertEqual(
            p3_lp.rectangle_constraints,
            (
                RectangleConstraint(
                    base=(1,),
                    extension_a=(0, 1),
                    extension_b=(1, 2),
                    union=(0, 1, 2),
                    root=1,
                ),
            ),
        )

    def test_h1_certificate_violates_reported_h2_rectangle_by_minus_half(self):
        topology = TreeTopology.from_dict(SKZ_LONG_STAR_TOPOLOGY)
        lp = build_hereditary_lp(topology, SKZ_LONG_STAR_WEIGHTS, relaxation="h2")
        values = load_h1_skz_rational_values(lp)
        constraint = RectangleConstraint(
            base=(2, 3, 4),
            extension_a=(1, 2, 3, 4),
            extension_b=(2, 3, 4, 5),
            union=(1, 2, 3, 4, 5),
            root=3,
        )
        self.assertEqual(rectangle_value(values, constraint), Fraction(-1, 2))

    def test_h2_includes_constraint_cutting_old_h1_certificate(self):
        topology = TreeTopology.from_dict(SKZ_LONG_STAR_TOPOLOGY)
        lp = build_hereditary_lp(topology, SKZ_LONG_STAR_WEIGHTS, relaxation="h2")
        values = load_h1_skz_rational_values(lp)
        violations = [
            -rectangle_value(values, constraint)
            for constraint in lp.rectangle_constraints
        ]
        self.assertIn(
            RectangleConstraint(
                base=(2, 3, 4),
                extension_a=(1, 2, 3, 4),
                extension_b=(2, 3, 4, 5),
                union=(1, 2, 3, 4, 5),
                root=3,
            ),
            lp.rectangle_constraints,
        )
        self.assertEqual(max(violations), Fraction(1, 2))


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

    def test_skz_long_star_h2_solve_numerically_closes_h1_gap(self):
        topology = TreeTopology.from_dict(SKZ_LONG_STAR_TOPOLOGY)
        lp = build_hereditary_lp(topology, SKZ_LONG_STAR_WEIGHTS, relaxation="h2")
        self.assertEqual(len(lp.connected_subsets), 36)
        self.assertEqual(len(lp.variables), 120)
        self.assertEqual(lp.simplex_constraint_count, 36)
        self.assertEqual(len(lp.heredity_constraints), 681)
        self.assertEqual(len(lp.rectangle_constraints), 1257)

        solution = solve_hereditary_lp(
            topology,
            SKZ_LONG_STAR_WEIGHTS,
            relaxation="h2",
        )
        self.assertEqual(solution.status, 0)
        self.assertAlmostEqual(solution.objective_value, 30.0, places=8)
        rational = rationalize_solution(solution)
        self.assertTrue(rational.feasible)
        self.assertEqual(rational.exact_objective, Fraction(30))
        self.assertEqual(rational.max_simplex_residual, Fraction(0))
        self.assertEqual(rational.max_heredity_violation, Fraction(0))
        self.assertEqual(rational.max_h2_rectangle_violation, Fraction(0))


if __name__ == "__main__":
    unittest.main()
