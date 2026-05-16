import unittest
from fractions import Fraction

from scripts.stt_checker.star_audit import (
    DEFAULT_EMBEDDING_BRANCH_LENGTHS,
    depth_dominant_audit,
    depth_projection,
    embedding_audits,
    feasibility_audit,
    mobius_masses,
    negative_masses,
    star4_instance,
)


class STTV4StarAuditTests(unittest.TestCase):
    def setUp(self):
        self.star = star4_instance()

    def test_star4_h2_feasibility_exact(self):
        audit = feasibility_audit(self.star)
        self.assertTrue(audit.feasible)
        self.assertEqual(audit.simplex_count, 20)
        self.assertEqual(audit.z_variable_count, 52)
        self.assertEqual(audit.h1_count, 173)
        self.assertEqual(audit.h2_ordered_count, 1449)
        self.assertEqual(audit.h2_canonical_nontrivial_count, 181)
        self.assertEqual(audit.max_simplex_residual, Fraction(0))
        self.assertEqual(audit.min_h1_slack, Fraction(0))
        self.assertEqual(audit.min_h2_ordered_slack, Fraction(0))
        self.assertEqual(audit.min_h2_canonical_slack, Fraction(0))

    def test_star4_negative_mobius_masses(self):
        masses = mobius_masses(self.star)
        self.assertEqual(masses[((0,), 0)], Fraction(-1, 3))
        self.assertEqual(
            negative_masses(self.star),
            (
                (((0,), 0), Fraction(-1, 3)),
                (((0, 1), 1), Fraction(-1, 12)),
                (((0, 2), 2), Fraction(-1, 12)),
                (((0, 3), 3), Fraction(-1, 12)),
                (((0, 4), 4), Fraction(-1, 12)),
            ),
        )

    def test_star4_depth_projection(self):
        self.assertEqual(
            depth_projection(self.star),
            (Fraction(8, 3), Fraction(11, 6), Fraction(11, 6), Fraction(11, 6), Fraction(11, 6)),
        )

    def test_star4_depth_dominant_membership(self):
        audit = depth_dominant_audit(self.star)
        self.assertTrue(audit.is_member)
        self.assertEqual(len(audit.depth_vectors), 65)
        self.assertEqual(audit.certificate[0][0], Fraction(1))
        self.assertEqual(audit.certificate[0][1], (0, 1, 1, 1, 1))

    def test_sampled_degree4_embeddings_h2_feasible(self):
        audits = embedding_audits(DEFAULT_EMBEDDING_BRANCH_LENGTHS)
        self.assertEqual(len(audits), 5)
        for audit in audits:
            with self.subTest(branch_lengths=audit.branch_lengths):
                self.assertTrue(audit.feasibility.feasible)
                self.assertEqual(audit.feasibility.max_simplex_residual, Fraction(0))
                self.assertEqual(audit.feasibility.min_h1_slack, Fraction(0))
                self.assertEqual(audit.feasibility.min_h2_ordered_slack, Fraction(0))
                self.assertEqual(audit.center_root_mass, Fraction(-1, 3))
                self.assertLess(audit.center_root_mass, 0)


if __name__ == "__main__":
    unittest.main()
