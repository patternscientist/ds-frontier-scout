import copy
import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from fractions import Fraction
from pathlib import Path

from scripts.stt_checker.certificates import check_certificate, load_json
from scripts.stt_checker.cli import main as cli_main
from scripts.stt_checker.enumerate_stts import (
    EnumerationLimitExceeded,
    enumerate_stts,
    integer_optimum_by_enumeration,
)
from scripts.stt_checker.rationals import parse_rational, rational_to_string
from scripts.stt_checker.stt import validate_stt
from scripts.stt_checker.topology import TreeTopology


ROOT = Path(__file__).resolve().parents[1]


class RationalTests(unittest.TestCase):
    def test_parse_and_normalize(self):
        self.assertEqual(parse_rational("10/20"), Fraction(1, 2))
        self.assertEqual(parse_rational("-2/5"), Fraction(-2, 5))
        self.assertEqual(parse_rational(3), Fraction(3, 1))
        self.assertEqual(parse_rational({"num": 6, "den": 8}), Fraction(3, 4))
        self.assertEqual(rational_to_string(Fraction(10, 20)), "1/2")

    def test_reject_float(self):
        with self.assertRaises(ValueError):
            parse_rational(0.5)
        with self.assertRaises(ValueError):
            parse_rational("0.5")
        with self.assertRaises(ValueError):
            parse_rational("1/0")
        with self.assertRaises(ValueError):
            parse_rational({"num": 1, "den": 0})
        with self.assertRaises(ValueError):
            parse_rational({"num": 1, "den": 2, "extra": 0})


class TopologyTests(unittest.TestCase):
    def test_invalid_topology_cases(self):
        with self.assertRaises(ValueError):
            TreeTopology.from_dict(
                {"n": 3, "vertices": [0, 1, 2], "edges": [[0, 1], [1, 1]]}
            )
        with self.assertRaises(ValueError):
            TreeTopology.from_dict(
                {"n": 3, "vertices": [0, 1, 2], "edges": [[0, 1], [1, 0]]}
            )
        with self.assertRaises(ValueError):
            TreeTopology.from_dict(
                {"n": 4, "vertices": [0, 1, 2, 3], "edges": [[0, 1], [2, 3], [0, 2], [1, 3]]}
            )
        with self.assertRaises(ValueError):
            TreeTopology.from_dict(
                {"n": 3, "vertices": [1, 2, 3], "edges": [[1, 2], [2, 3]]}
            )

    def test_derived_labels(self):
        path = TreeTopology.from_dict(
            {"n": 4, "vertices": [0, 1, 2, 3], "edges": [[0, 1], [1, 2], [2, 3]]}
        )
        self.assertIn("path", path.derived_subclass_labels())
        self.assertIn("edge-diameter-2", path.derived_subclass_labels())

        star = TreeTopology.from_dict(
            {"n": 4, "vertices": [0, 1, 2, 3], "edges": [[0, 1], [0, 2], [0, 3]]}
        )
        self.assertIn("star", star.derived_subclass_labels())
        self.assertIn("edge-diameter-1", star.derived_subclass_labels())

        with self.assertRaises(ValueError):
            star.validate_declared_labels(["path"])
        with self.assertRaises(ValueError):
            star.validate_declared_labels(["not-a-schema-label"])
        star.validate_declared_labels(["unknown", "almost-star"])

    def test_edge_diameter_boundary_cases(self):
        one = TreeTopology.from_dict({"n": 1, "vertices": [0], "edges": []})
        self.assertIn("path", one.derived_subclass_labels())
        self.assertIn("star", one.derived_subclass_labels())
        self.assertIn("edge-diameter-0", one.derived_subclass_labels())

        two = TreeTopology.from_dict(
            {"n": 2, "vertices": [0, 1], "edges": [[0, 1]]}
        )
        self.assertIn("path", two.derived_subclass_labels())
        self.assertIn("star", two.derived_subclass_labels())
        self.assertIn("edge-diameter-0", two.derived_subclass_labels())


class STTTests(unittest.TestCase):
    def test_validate_stt_with_omitted_singletons(self):
        topology = TreeTopology.from_dict(
            {"n": 4, "vertices": [0, 1, 2, 3], "edges": [[0, 1], [1, 2], [2, 3]]}
        )
        result = validate_stt(
            topology,
            {
                "component_roots": [
                    {"component": [0, 1, 2, 3], "root": 1},
                    {"component": [2, 3], "root": 2},
                ]
            },
            depth_base=1,
        )
        self.assertEqual(result.parent, {1: None, 0: 1, 2: 1, 3: 2})
        self.assertEqual(result.depth, {1: 1, 0: 2, 2: 2, 3: 3})

    def test_reject_unreached_component(self):
        topology = TreeTopology.from_dict(
            {"n": 4, "vertices": [0, 1, 2, 3], "edges": [[0, 1], [1, 2], [2, 3]]}
        )
        with self.assertRaises(ValueError):
            validate_stt(
                topology,
                {
                    "component_roots": [
                        {"component": [0, 1, 2, 3], "root": 1},
                        {"component": [0, 1], "root": 0},
                        {"component": [2, 3], "root": 2},
                    ]
                },
            )


class EnumerationTests(unittest.TestCase):
    def test_counts_and_optimum(self):
        path = TreeTopology.from_dict(
            {"n": 4, "vertices": [0, 1, 2, 3], "edges": [[0, 1], [1, 2], [2, 3]]}
        )
        self.assertEqual(len(enumerate_stts(path)), 14)
        weights = {v: Fraction(1, 4) for v in path.vertices}
        optimum, _best, count = integer_optimum_by_enumeration(path, weights)
        self.assertEqual(count, 14)
        self.assertEqual(optimum, Fraction(2, 1))

        star = TreeTopology.from_dict(
            {"n": 4, "vertices": [0, 1, 2, 3], "edges": [[0, 1], [0, 2], [0, 3]]}
        )
        self.assertEqual(len(enumerate_stts(star)), 16)

    def test_enumeration_safety_cap(self):
        path = TreeTopology.from_dict(
            {"n": 4, "vertices": [0, 1, 2, 3], "edges": [[0, 1], [1, 2], [2, 3]]}
        )
        with self.assertRaises(EnumerationLimitExceeded):
            enumerate_stts(path, max_count=13)


class CertificateTests(unittest.TestCase):
    def load_example(self, name):
        return load_json(ROOT / "examples" / "stt" / name)

    def test_path_certificate_passes(self):
        result = check_certificate(self.load_example("path_4_proof.json"))
        self.assertEqual(result.weighted_cost, Fraction(2, 1))
        self.assertEqual(result.normalized["integer_optimum"]["stt_count"], 14)

    def test_star_certificate_passes(self):
        result = check_certificate(self.load_example("star_4_proof.json"))
        self.assertEqual(result.weighted_cost, Fraction(7, 4))

    def test_long_star_certificate_passes(self):
        result = check_certificate(self.load_example("long_star_7.json"))
        self.assertEqual(result.weighted_cost, Fraction(48, 23))
        self.assertEqual(result.normalized["integer_optimum"]["stt_count"], 807)
        self.assertIn("edge-diameter-3", result.normalized["topology"]["derived_subclass_labels"])

    def test_cost_mismatch_fails(self):
        data = self.load_example("path_4_proof.json")
        data["cost"]["weighted_cost"] = "3"
        with self.assertRaises(ValueError):
            check_certificate(data)

    def test_missing_mode_fails(self):
        data = self.load_example("path_4_proof.json")
        del data["mode"]
        with self.assertRaises(ValueError):
            check_certificate(data)

    def test_lp_field_rejected_in_proof_mode(self):
        data = self.load_example("path_4_proof.json")
        data["lp_solution"] = {"relaxation_version": "unsupported"}
        with self.assertRaises(ValueError):
            check_certificate(data)

    def test_audit_mode_keeps_lp_metadata_unsupported(self):
        data = self.load_example("path_4_proof.json")
        data["mode"] = "audit"
        data["lp_solution"] = {"relaxation_version": "unsupported"}
        result = check_certificate(data)
        self.assertIn("unsupported_lp_metadata", result.normalized)


class CliTests(unittest.TestCase):
    def test_check_exit_codes(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            code = cli_main(["check", str(ROOT / "examples" / "stt" / "path_4_proof.json")])
        self.assertEqual(code, 0)
        self.assertIn("PASS", stdout.getvalue())

        stderr = io.StringIO()
        with redirect_stderr(stderr):
            code = cli_main(["check", str(ROOT / "examples" / "stt" / "missing.json")])
        self.assertEqual(code, 1)
        self.assertIn("FAIL", stderr.getvalue())

    def test_subcommand_max_enumeration_option(self):
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            code = cli_main(
                [
                    "enumerate",
                    str(ROOT / "examples" / "stt" / "path_4_proof.json"),
                    "--max-enumeration",
                    "13",
                ]
            )
        self.assertEqual(code, 1)
        self.assertIn("safety cap 13", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
