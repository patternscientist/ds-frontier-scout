import json
import unittest
from fractions import Fraction
from pathlib import Path

from scripts.star_support_oracle import (
    min_cut_F_value,
    pair_supports,
    residual_pair_lower_bounds,
    source_deletion_delta,
    support_oracle,
)


def pair_lambda(values):
    return {pair: value for pair, value in zip(pair_supports(len(values)), values) if value}


class StarSupportOracleTests(unittest.TestCase):
    def test_symmetric_k3_witness(self):
        u = (Fraction(1), Fraction(1), Fraction(1))
        alpha = Fraction(1)

        unit = support_oracle(
            3,
            u,
            alpha,
            {(0, 1): Fraction(1)},
        )
        triangle = support_oracle(
            3,
            u,
            alpha,
            {(0, 1): Fraction(1), (0, 2): Fraction(1), (1, 2): Fraction(1)},
        )

        self.assertEqual(unit.F, Fraction(3))
        self.assertEqual(unit.phi, Fraction(2))
        self.assertEqual(triangle.phi, Fraction(3))
        self.assertEqual(triangle.min_cost, Fraction(3))

    def test_min_cut_formula_boundary_regression(self):
        u = (Fraction(0), Fraction(1), Fraction(1))
        alpha = Fraction(0)
        F, active = min_cut_F_value(3, u, alpha)

        self.assertEqual(F, Fraction(1))
        self.assertIn((1, 2), active)
        self.assertEqual(source_deletion_delta(3, u, alpha, (1, 2)), Fraction(1))

    def test_direct_lp_cross_check_small_star(self):
        result = support_oracle(
            2,
            (Fraction(1), Fraction(1)),
            Fraction(1),
            {(0, 1): Fraction(1)},
            direct_lp_check=True,
        )

        self.assertEqual(result.min_cost, result.direct_lp_min_cost)
        self.assertEqual(result.phi, result.direct_lp_phi)

    def test_corrected_residual_pair_lower_bounds(self):
        bounds = residual_pair_lower_bounds(
            z=(Fraction(1), Fraction(2), Fraction(3)),
            t=(Fraction(0), Fraction(1), Fraction(0)),
            rho=Fraction(2),
            beta=Fraction(3),
            eta=Fraction(1),
            gamma=Fraction(2),
        )

        self.assertEqual(bounds[(0, 1)], Fraction(2))
        self.assertEqual(bounds[(0, 2)], Fraction(3))
        self.assertEqual(bounds[(1, 2)], Fraction(4))


class MixedSupportArtifactTests(unittest.TestCase):
    def test_generated_chamber_artifact_records_symmetric_fan(self):
        path = Path("data/k3_pair_antichain_chambers.json")
        payload = json.loads(path.read_text(encoding="utf-8"))
        symmetric = payload["symmetric_star_face"]

        self.assertEqual(symmetric["witness_check"]["status"], "verified")
        self.assertEqual(symmetric["witness_check"]["Phi_triangle"], "3")
        self.assertEqual(symmetric["chamber_count"], 7)
        self.assertTrue(
            any(
                chamber["phi_coefficients"]
                == {"lambda_12": "1", "lambda_13": "1", "lambda_23": "1"}
                for chamber in symmetric["chambers"]
            )
        )


if __name__ == "__main__":
    unittest.main()
