import unittest
import json
import re
from dataclasses import replace
from fractions import Fraction
from tempfile import TemporaryDirectory
from pathlib import Path

from scripts.stt_checker.double_star_depth_projection import (
    double_star_spec,
    double_star_topology,
)
from scripts.stt_checker.dsk1_h1_coarea import (
    H2_SANDWICH_STATUS,
    VERIFIED_H1_CERTIFICATE_STATUS,
    _assert_all_h1_certificates_verified,
    bellman_phi,
    bellman_true_optimum,
    evaluate_case,
    run_scout,
    small_integer_weight_vectors,
    write_outputs,
)
from scripts.stt_checker.enumerate_stts import (
    enumerate_stts,
    integer_optimum_by_enumeration,
)


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
V1_REPORT = WORKSPACE_ROOT / "reports" / "stt_dsk1_h1_coarea_v1.md"
V1_CERTIFICATES = (
    WORKSPACE_ROOT / "examples" / "stt_lp" / "dsk1_h1_coarea_v1_certificates.json"
)


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

    def test_bellman_and_phi_match_generic_enumeration_for_small_integer_orbits(self):
        for k in (1, 2, 3):
            spec = double_star_spec(k, 1)
            topology = double_star_topology(k, 1)
            stts = enumerate_stts(topology, depth_base=0, max_count=1_000_000)
            classified = []
            for stt in stts:
                ancestors_of_a = _strict_ancestors(stt.parent, spec.a)
                left_ancestors = tuple(
                    leaf for leaf in spec.left_leaves if leaf in ancestors_of_a
                )
                depths = tuple(stt.depth[vertex] for vertex in topology.vertices)
                classified.append((left_ancestors, depths))

            for _family, weights in small_integer_weight_vectors(k, bound=2):
                bellman = bellman_true_optimum(k, weights)
                brute = min(_depth_cost(weights, depths) for _subset, depths in classified)
                self.assertEqual(bellman, brute, (k, weights))

                phi = bellman_phi(k, weights)
                for subset, value in phi.phi.items():
                    brute_phi = min(
                        _depth_cost(weights, depths)
                        for classified_subset, depths in classified
                        if classified_subset == subset
                    )
                    self.assertEqual(value, brute_phi, (k, weights, subset))


class DSK1HarnessTests(unittest.TestCase):
    def test_evaluate_case_certifies_h1_and_h2_by_sandwich(self):
        case = evaluate_case(2, (2, 1, 1, 0, 3), "sample")
        self.assertEqual(case.true_optimum, Fraction(6))
        self.assertEqual(case.h1_gap, Fraction(0))
        self.assertEqual(case.h2_gap, Fraction(0))
        self.assertTrue(case.h1.certificate.verified)
        self.assertEqual(case.h1.certificate_status, VERIFIED_H1_CERTIFICATE_STATUS)
        self.assertEqual(case.h2_status, H2_SANDWICH_STATUS)

    def test_run_refuses_unverified_h1_certificates(self):
        case = evaluate_case(1, (1, 0, 1, 0), "sample")
        bad_h1 = replace(case.h1, certificate_status="floating_only")
        bad_case = replace(case, h1=bad_h1)
        with self.assertRaisesRegex(RuntimeError, "verified exact H1"):
            _assert_all_h1_certificates_verified([bad_case])

    def test_bounded_report_generator_writes_artifacts(self):
        data = run_scout(
            exhaustive_bound=0,
            random_count=0,
            include_regressions=False,
            include_large=False,
        )
        self.assertEqual(data["schema"], "stt_dsk1_h1_coarea_v1")
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
            self.assertIn("stt_dsk1_h1_coarea_v1", certificates.read_text(encoding="utf-8"))
            self.assertEqual(result["h1_gaps"], 0)

    def test_reported_h1_no_gap_cases_have_verified_exact_status(self):
        data = json.loads(V1_CERTIFICATES.read_text(encoding="utf-8"))
        bad = [
            case
            for case in data["cases"]
            if case["h1_gap"] == "0"
            and case["h1_certificate_status"] != VERIFIED_H1_CERTIFICATE_STATUS
        ]
        self.assertEqual(bad, [])
        self.assertEqual(data["summary"]["h1_certificate_failures"], 0)

    def test_markdown_report_has_real_heading_structure(self):
        text = V1_REPORT.read_text(encoding="utf-8").replace("\r\n", "\n")
        self.assertIn("Finite evidence only / do not promote to theorem", text)
        self.assertIn("\n## Candidate DS(k,1) theorem suggested by v1\n", text)
        self.assertIn("\n## Exact Certificate Audit\n", text)
        for line in text.splitlines():
            if line.startswith("#"):
                self.assertRegex(line, r"^#{1,6} [^#].+")
            else:
                self.assertNotRegex(line, r"#{1,6} [A-Za-z]")


def _strict_ancestors(parent: dict[int, int | None], vertex: int) -> set[int]:
    ancestors: set[int] = set()
    current = parent[vertex]
    while current is not None:
        ancestors.add(current)
        current = parent[current]
    return ancestors


def _depth_cost(weights: tuple[Fraction, ...], depths: tuple[int, ...]) -> Fraction:
    return sum(weights[index] * depths[index] for index in range(len(weights)))


if __name__ == "__main__":
    unittest.main()
