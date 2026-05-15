import copy
import io
import json
import tempfile
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
from scripts.stt_checker.frontier_artifacts import build_frontier_artifact
from scripts.stt_checker.rationals import parse_rational, rational_to_string
from scripts.stt_checker.stt import validate_stt
from scripts.stt_checker.topology import TreeTopology
from scripts.stt_checker.topology_generation import (
    decode_prufer_code,
    generate_labeled_tree_topologies,
    generate_unlabeled_tree_topologies,
    tree_canonical_form,
)


ROOT = Path(__file__).resolve().parents[1]


def _independent_stt_count(topology, component=None):
    """Count recursive STTs without constructing STTResult objects."""

    if component is None:
        component = tuple(topology.vertices)
    component = tuple(sorted(component))
    total = 0
    for root in component:
        subtotal = 1
        for child in topology.connected_components_after_removing(root, component):
            subtotal *= _independent_stt_count(topology, child)
        total += subtotal
    return total


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


class TopologyGenerationTests(unittest.TestCase):
    def test_prufer_decoding_tiny_examples(self):
        self.assertEqual(decode_prufer_code([], 1), [])
        self.assertEqual(decode_prufer_code([], 2), [(0, 1)])
        self.assertEqual(decode_prufer_code([0, 0], 4), [(0, 1), (0, 2), (0, 3)])
        self.assertEqual(decode_prufer_code([1, 2], 4), [(0, 1), (1, 2), (2, 3)])
        with self.assertRaises(ValueError):
            decode_prufer_code([0], 2)
        with self.assertRaises(ValueError):
            decode_prufer_code([4, 0], 4)

    def test_labeled_generation_covers_cayley_counts(self):
        for n in range(1, 6):
            generated = list(generate_labeled_tree_topologies(n))
            expected = 1 if n == 1 else n ** (n - 2)
            self.assertEqual(len(generated), expected)
            edge_sets = {topology.edges for topology in generated}
            self.assertEqual(len(edge_sets), expected)
            for topology in generated:
                self.assertEqual(topology.vertices, tuple(range(n)))
                self.assertEqual(len(topology.edges), n - 1)

    def test_canonical_form_matches_isomorphic_relabelings(self):
        one_center_first = TreeTopology.from_dict(
            {"n": 5, "vertices": [0, 1, 2, 3, 4], "edges": [[0, 1], [1, 2], [2, 3], [2, 4]]}
        )
        one_center_second = TreeTopology.from_dict(
            {"n": 5, "vertices": [0, 1, 2, 3, 4], "edges": [[3, 0], [0, 4], [4, 1], [4, 2]]}
        )
        self.assertEqual(
            tree_canonical_form(one_center_first),
            tree_canonical_form(one_center_second),
        )

        two_center_first = TreeTopology.from_dict(
            {
                "n": 6,
                "vertices": [0, 1, 2, 3, 4, 5],
                "edges": [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]],
            }
        )
        two_center_second = TreeTopology.from_dict(
            {
                "n": 6,
                "vertices": [0, 1, 2, 3, 4, 5],
                "edges": [[5, 0], [0, 3], [3, 2], [2, 4], [4, 1]],
            }
        )
        self.assertEqual(
            tree_canonical_form(two_center_first),
            tree_canonical_form(two_center_second),
        )

    def test_canonical_form_separates_non_isomorphic_shapes(self):
        path = TreeTopology.from_dict(
            {"n": 4, "vertices": [0, 1, 2, 3], "edges": [[0, 1], [1, 2], [2, 3]]}
        )
        star = TreeTopology.from_dict(
            {"n": 4, "vertices": [0, 1, 2, 3], "edges": [[0, 1], [0, 2], [0, 3]]}
        )
        self.assertNotEqual(tree_canonical_form(path), tree_canonical_form(star))

    def test_unlabeled_generation_counts_through_seven(self):
        expected = {1: 1, 2: 1, 3: 1, 4: 2, 5: 3, 6: 6, 7: 11}
        generated = generate_unlabeled_tree_topologies(7)
        counts = {n: 0 for n in expected}
        for item in generated:
            counts[item["n"]] += 1
            topology = item["topology"]
            self.assertEqual(topology.vertices, tuple(range(item["n"])))
            self.assertEqual(len(topology.edges), item["n"] - 1)
        self.assertEqual(counts, expected)

    def test_edge_diameter_filtering(self):
        generated = generate_unlabeled_tree_topologies(6)
        edge_diameter_3 = [item for item in generated if item["edge_diameter"] == 3]
        edge_diameter_at_most_3 = [
            item for item in generated if item["edge_diameter"] <= 3
        ]
        self.assertTrue(edge_diameter_3)
        self.assertTrue(all("edge-diameter-3" in item["derived_labels"] for item in edge_diameter_3))
        self.assertLess(len(edge_diameter_at_most_3), len(generated))
        self.assertTrue(all(item["edge_diameter"] <= 3 for item in edge_diameter_at_most_3))


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

    def test_counts_match_independent_recurrence(self):
        for item in generate_unlabeled_tree_topologies(6):
            topology = item["topology"]
            self.assertEqual(len(enumerate_stts(topology)), _independent_stt_count(topology))

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

    def test_edge_diameter3_checker_only_certificate_passes(self):
        result = check_certificate(self.load_example("edge_diameter3_checker_only_7.json"))
        self.assertEqual(result.weighted_cost, Fraction(48, 23))
        self.assertEqual(result.normalized["integer_optimum"]["stt_count"], 807)
        self.assertIn("edge-diameter-3", result.normalized["topology"]["derived_subclass_labels"])

    def test_skz_long_star_certificate_passes(self):
        result = check_certificate(self.load_example("skz_long_star_7_stt_optimum.json"))
        self.assertEqual(result.weighted_cost, Fraction(53, 23))
        self.assertEqual(result.normalized["integer_optimum"]["stt_count"], 662)
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


class FrontierArtifactTests(unittest.TestCase):
    def test_frontier_artifact_smoke(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = build_frontier_artifact(
                max_n=5,
                max_enumeration=100_000,
                data_dir=root / "data",
                report_path=root / "reports" / "stt_v0_frontier_artifact.md",
            )
            self.assertTrue(paths.json_path.exists())
            self.assertTrue(paths.csv_path.exists())
            self.assertTrue(paths.report_path.exists())
            payload = json.loads(paths.json_path.read_text(encoding="utf-8"))
            self.assertFalse(payload["lp_feasibility_checked"])
            self.assertEqual(len(payload["topologies"]), 8)
            self.assertIn("No LP feasibility is checked", paths.report_path.read_text(encoding="utf-8"))

    def test_frontier_artifact_records_caps_without_optima(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = build_frontier_artifact(
                max_n=5,
                max_enumeration=10,
                data_dir=root / "data",
                report_path=root / "reports" / "stt_v0_frontier_artifact.md",
            )
            payload = json.loads(paths.json_path.read_text(encoding="utf-8"))
            capped = [
                record
                for record in payload["topologies"]
                if record["enumeration"]["exceeded_cap"]
            ]
            self.assertTrue(capped)
            for record in capped:
                self.assertFalse(record["enumeration"]["completed"])
                self.assertIsNone(record["enumeration"]["stt_count"])
                self.assertIsNone(record["uniform_weights"]["optimum"])
                self.assertIsNone(record["leaf_heavy_weights"]["optimum"])

    def test_frontier_artifact_deterministic_rerun(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = build_frontier_artifact(
                max_n=5,
                max_enumeration=100_000,
                data_dir=root / "first" / "data",
                report_path=root / "first" / "reports" / "stt_v0_frontier_artifact.md",
            )
            second = build_frontier_artifact(
                max_n=5,
                max_enumeration=100_000,
                data_dir=root / "second" / "data",
                report_path=root / "second" / "reports" / "stt_v0_frontier_artifact.md",
            )
            self.assertEqual(
                first.json_path.read_text(encoding="utf-8"),
                second.json_path.read_text(encoding="utf-8"),
            )
            self.assertEqual(
                first.csv_path.read_text(encoding="utf-8"),
                second.csv_path.read_text(encoding="utf-8"),
            )
            self.assertEqual(
                first.report_path.read_text(encoding="utf-8"),
                second.report_path.read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
