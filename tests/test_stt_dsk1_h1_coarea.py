import unittest
from fractions import Fraction
from tempfile import TemporaryDirectory
from pathlib import Path

from scripts.stt_checker.double_star_depth_projection import double_star_topology
from scripts.stt_checker.dsk1_h1_coarea import (
    bellman_phi,
    bellman_true_optimum,
    evaluate_case,
    run_scout,
    write_outputs,
)
from scripts.stt_checker.enumerate_stts import integer_optimum_by_enumeration


class DSK1BellmanTests(unittest.TestCase):
    def test_bellman_matches_generic_enumeration_on_ds31(self):
        k = 3
        weights = (3, 1, 2, 4, 0, 5)
        topology = double_star_topology(k, 1)
        weight_map = {vertex: Fraction(weights[vertex]) for vertex in topology.vertices}
        enumerated, _stt, _count = integer_optimum_by_enumeration(
            topology,
            weight_map,
            depth_base=0,
            max_count=100_000,
        )
        self.assertEqual(bellman_true_optimum(k, weights), enumerated)

    def test_phi_is_submodular_on_sample(self):
        result = bellman_phi(3, (2, 1, 0, 3, 1, 4))
        self.assertTrue(result.phi_submodular)
        self.assertEqual(result.phi_violations, ())


class DSK1HarnessTests(unittest.TestCase):
    def test_evaluate_case_certifies_h1_and_h2_by_sandwich(self):
        case = evaluate_case(2, (2, 1, 1, 0, 3), "sample")
        self.assertEqual(case.true_optimum, Fraction(6))
        self.assertEqual(case.h1_gap, Fraction(0))
        self.assertEqual(case.h2_gap, Fraction(0))
        self.assertTrue(case.h1.certificate.verified)
        self.assertEqual(
            case.h2_status,
            "exact_by_h1_equals_stt_sandwich_no_separate_h2_primal",
        )

    def test_bounded_report_generator_writes_artifacts(self):
        data = run_scout(
            exhaustive_bound=0,
            random_count=0,
            include_regressions=False,
            include_large=False,
        )
        self.assertEqual(data["schema"], "stt_dsk1_h1_coarea_v0")
        self.assertEqual(len(data["cases"]), 0)
        with TemporaryDirectory() as directory:
            report = Path(directory) / "report.md"
            certificates = Path(directory) / "certificates.json"
            result = write_outputs(
                report_path=report,
                certificate_path=certificates,
                exhaustive_bound=0,
                random_count=0,
                include_regressions=False,
                include_large=False,
            )
            self.assertTrue(report.read_text(encoding="utf-8").startswith("# DS(k,1)"))
            self.assertIn("stt_dsk1_h1_coarea_v0", certificates.read_text(encoding="utf-8"))
            self.assertEqual(result["h1_gaps"], 0)


if __name__ == "__main__":
    unittest.main()
