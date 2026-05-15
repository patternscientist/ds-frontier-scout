import copy
import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from fractions import Fraction
from pathlib import Path

from scripts.stt_checker.certificates import load_json
from scripts.stt_checker.cli import main as cli_main
from scripts.stt_checker.enumerate_stts import enumerate_stts
from scripts.stt_checker.lp_feasibility import (
    check_constraints,
    check_lp_certificate,
    generate_variable_domains,
    parse_dense_assignment,
    stt_certificate_to_lp_certificate,
    stt_induced_assignment,
)
from scripts.stt_checker.stt import validate_stt
from scripts.stt_checker.topology import TreeTopology


ROOT = Path(__file__).resolve().parents[1]


class STTLPFeasibilityTests(unittest.TestCase):
    def load_lp_example(self, name):
        return load_json(ROOT / "examples" / "stt_lp" / name)

    def load_stt_example(self, name):
        return load_json(ROOT / "examples" / "stt" / name)

    def test_variable_domains_path_and_star(self):
        path = TreeTopology.from_dict(
            {"n": 4, "vertices": [0, 1, 2, 3], "edges": [[0, 1], [1, 2], [2, 3]]}
        )
        path_domains = generate_variable_domains(path)
        self.assertEqual(path_domains.D, (0, 1, 2, 3))
        self.assertEqual(len(path_domains.X), 12)
        self.assertEqual(
            set(path_domains.Z),
            {(1, 0, 2), (1, 0, 3), (2, 0, 3), (2, 1, 3)},
        )

        star = TreeTopology.from_dict(
            {"n": 4, "vertices": [0, 1, 2, 3], "edges": [[0, 1], [0, 2], [0, 3]]}
        )
        star_domains = generate_variable_domains(star)
        self.assertEqual(len(star_domains.X), 12)
        self.assertEqual(set(star_domains.Z), {(0, 1, 2), (0, 1, 3), (0, 2, 3)})

    def test_variable_domains_tiny_edge_cases(self):
        one = TreeTopology.from_dict({"n": 1, "vertices": [0], "edges": []})
        one_domains = generate_variable_domains(one)
        self.assertEqual(one_domains.D, (0,))
        self.assertEqual(one_domains.X, ())
        self.assertEqual(one_domains.Z, ())
        one_result = check_lp_certificate(
            {
                "schema_version": "stt-lp-cert-v0",
                "certificate_id": "one-vertex-zero-depth",
                "mode": "proof",
                "relaxation": "golinsky_stt_lp",
                "relaxation_version": "golinsky_stt_lp_v0",
                "topology": {"n": 1, "vertices": [0], "edges": []},
                "lp_solution": {
                    "variables": {
                        "D": [{"i": 0, "value": "0"}],
                        "X": [],
                        "Z": [],
                    }
                },
                "objective": {"frequency": {"0": "5"}, "value": "0"},
            }
        )
        self.assertTrue(one_result.feasible)
        self.assertEqual(one_result.objective.search_cost_value, Fraction(5))

        two = TreeTopology.from_dict(
            {"n": 2, "vertices": [0, 1], "edges": [[0, 1]]}
        )
        two_domains = generate_variable_domains(two)
        self.assertEqual(two_domains.D, (0, 1))
        self.assertEqual(set(two_domains.X), {(0, 1), (1, 0)})
        self.assertEqual(two_domains.Z, ())

    def test_proof_mode_rejects_missing_unknown_and_duplicate_variables(self):
        data = self.load_lp_example("path_4_stt_induced_lp.json")
        topology = TreeTopology.from_dict(data["topology"])
        domains = generate_variable_domains(topology)

        missing = copy.deepcopy(data["lp_solution"])
        missing["variables"]["X"].pop()
        with self.assertRaisesRegex(ValueError, "missing variables"):
            parse_dense_assignment(missing, domains)

        unknown = copy.deepcopy(data["lp_solution"])
        unknown["variables"]["X"].append({"i": 0, "j": 0, "value": "0"})
        with self.assertRaisesRegex(ValueError, "unknown X_0_0"):
            parse_dense_assignment(unknown, domains)

        duplicate = copy.deepcopy(data["lp_solution"])
        duplicate["variables"]["D"].append({"i": 0, "value": "1"})
        with self.assertRaisesRegex(ValueError, "duplicate D_0"):
            parse_dense_assignment(duplicate, domains)

    def test_schema_and_unsupported_proof_fields_are_enforced(self):
        cases = [
            ("schema_version", "not-this-version", "schema_version"),
            ("mode", "audit", "mode"),
            ("relaxation", "other_lp", "relaxation"),
            ("relaxation_version", "other_version", "relaxation_version"),
        ]
        for field, value, message in cases:
            with self.subTest(field=field):
                data = self.load_lp_example("path_4_stt_induced_lp.json")
                data[field] = value
                with self.assertRaisesRegex(ValueError, message):
                    check_lp_certificate(data)

        for field in ("root_rounding", "integrality_gap"):
            with self.subTest(field=field):
                data = self.load_lp_example("path_4_stt_induced_lp.json")
                data[field] = {}
                with self.assertRaisesRegex(ValueError, "does not support"):
                    check_lp_certificate(data)

        data = self.load_lp_example("path_4_stt_induced_lp.json")
        data["lp_solution"]["relaxation_version"] = "shadowed_version"
        with self.assertRaisesRegex(ValueError, "lp_solution: unsupported fields"):
            check_lp_certificate(data)

    def test_float_and_decimal_values_are_rejected(self):
        data = self.load_lp_example("path_4_stt_induced_lp.json")
        topology = TreeTopology.from_dict(data["topology"])
        domains = generate_variable_domains(topology)

        decimal_string = copy.deepcopy(data["lp_solution"])
        decimal_string["variables"]["D"][0]["value"] = "0.5"
        with self.assertRaisesRegex(ValueError, "invalid rational string"):
            parse_dense_assignment(decimal_string, domains)

        json_float = copy.deepcopy(data["lp_solution"])
        json_float["variables"]["D"][0]["value"] = 0.5
        with self.assertRaisesRegex(ValueError, "floats are not exact"):
            parse_dense_assignment(json_float, domains)

    def test_constraint_violation_families(self):
        data = self.load_lp_example("path_4_stt_induced_lp.json")
        topology = TreeTopology.from_dict(data["topology"])
        domains = generate_variable_domains(topology)
        assignment = parse_dense_assignment(data["lp_solution"], domains)

        nonnegative = copy.deepcopy(assignment)
        nonnegative.D[0] = Fraction(-1)
        nonnegative_violations = check_constraints(topology, domains, nonnegative)
        self.assertIn("nonnegativity", {violation.family for violation in nonnegative_violations})
        self.assertEqual(nonnegative_violations[0].sense, ">=")
        self.assertEqual(nonnegative_violations[0].lhs, Fraction(-1))
        self.assertEqual(nonnegative_violations[0].rhs, Fraction(0))
        self.assertEqual(nonnegative_violations[0].slack, Fraction(-1))

        ancestry = copy.deepcopy(assignment)
        ancestry.X[(0, 1)] = Fraction(0)
        ancestry.X[(1, 0)] = Fraction(0)
        ancestry_families = {
            violation.family for violation in check_constraints(topology, domains, ancestry)
        }
        self.assertIn("ancestry", ancestry_families)

        loose_lca = copy.deepcopy(assignment)
        loose_lca.Z[(1, 0, 2)] = Fraction(2)
        loose_lca_families = {
            violation.family for violation in check_constraints(topology, domains, loose_lca)
        }
        self.assertIn("loose_lca", loose_lca_families)

        depth = copy.deepcopy(assignment)
        depth.D[3] = Fraction(0)
        depth_families = {
            violation.family for violation in check_constraints(topology, domains, depth)
        }
        self.assertIn("depth", depth_families)

        combined = copy.deepcopy(assignment)
        combined.D[0] = Fraction(-1)
        combined.X[(0, 1)] = Fraction(0)
        combined.X[(1, 0)] = Fraction(0)
        families = {violation.family for violation in check_constraints(topology, domains, combined)}
        self.assertIn("nonnegativity", families)
        self.assertIn("ancestry", families)

    def test_objective_recomputes_exactly(self):
        result = check_lp_certificate(self.load_lp_example("path_4_stt_induced_lp.json"))
        self.assertIsNotNone(result.objective)
        self.assertEqual(result.objective.computed_value, Fraction(1))
        self.assertEqual(result.objective.search_cost_value, Fraction(2))

        bad = self.load_lp_example("path_4_stt_induced_lp.json")
        bad["objective"]["value"] = "2"
        with self.assertRaisesRegex(ValueError, "objective.value"):
            check_lp_certificate(bad)

    def test_unnormalized_objective_and_frequency_keys(self):
        data = self.load_lp_example("path_4_stt_induced_lp.json")
        data["objective"] = {
            "frequency": {"0": "2", "1": "0", "2": "3/2", "3": "5/2"},
            "value": "17/2",
        }
        result = check_lp_certificate(data)
        self.assertEqual(result.objective.computed_value, Fraction(17, 2))
        self.assertEqual(result.objective.frequency_sum, Fraction(6))
        self.assertEqual(result.objective.search_cost_value, Fraction(29, 2))

        missing = self.load_lp_example("path_4_stt_induced_lp.json")
        del missing["objective"]["frequency"]["3"]
        with self.assertRaisesRegex(ValueError, "keys must match topology vertices"):
            check_lp_certificate(missing)

        extra = self.load_lp_example("path_4_stt_induced_lp.json")
        extra["objective"]["frequency"]["4"] = "0"
        with self.assertRaisesRegex(ValueError, "keys must match topology vertices"):
            check_lp_certificate(extra)

    def test_stt_induced_assignment_passes_for_path_and_star(self):
        for stt_name in ("path_4_proof.json", "star_4_proof.json"):
            stt_cert = self.load_stt_example(stt_name)
            lp_cert = stt_certificate_to_lp_certificate(stt_cert)
            result = check_lp_certificate(lp_cert)
            self.assertTrue(result.feasible)

            topology = TreeTopology.from_dict(stt_cert["topology"])
            stt = validate_stt(topology, stt_cert["stt"], depth_base=1)
            assignment = stt_induced_assignment(topology, stt)
            domains = generate_variable_domains(topology)
            self.assertFalse(check_constraints(topology, domains, assignment))

    def test_stt_induced_assignment_passes_for_non_path_non_star_tree(self):
        stt_cert = {
            "schema_version": "stt-cert-v0",
            "certificate_id": "t-shape-5-proof",
            "mode": "proof",
            "topology": {
                "n": 5,
                "vertices": [0, 1, 2, 3, 4],
                "edges": [[0, 1], [1, 2], [1, 3], [3, 4]],
            },
            "weights": {
                "type": "vertex_frequency",
                "normalization": "sum_1",
                "values": {"0": "1/5", "1": "1/5", "2": "1/5", "3": "1/5", "4": "1/5"},
            },
            "stt": {
                "component_roots": [
                    {"component": [0, 1, 2, 3, 4], "root": 1},
                    {"component": [3, 4], "root": 3},
                ]
            },
        }
        topology = TreeTopology.from_dict(stt_cert["topology"])
        self.assertNotIn("path", topology.derived_subclass_labels())
        self.assertNotIn("star", topology.derived_subclass_labels())

        lp_cert = stt_certificate_to_lp_certificate(stt_cert)
        result = check_lp_certificate(lp_cert)
        self.assertTrue(result.feasible)

    def test_fractional_feasible_point_need_not_be_stt_induced(self):
        data = {
            "schema_version": "stt-lp-cert-v0",
            "certificate_id": "edge-2-fractional-feasible-not-stt-induced",
            "mode": "proof",
            "relaxation": "golinsky_stt_lp",
            "relaxation_version": "golinsky_stt_lp_v0",
            "topology": {
                "n": 2,
                "vertices": [0, 1],
                "edges": [[0, 1]],
                "declared_subclass_labels": ["path", "star", "edge-diameter-0"],
            },
            "lp_solution": {
                "variables": {
                    "D": [{"i": 0, "value": "1/2"}, {"i": 1, "value": "1/2"}],
                    "X": [
                        {"i": 0, "j": 1, "value": "1/2"},
                        {"i": 1, "j": 0, "value": "1/2"},
                    ],
                    "Z": [],
                }
            },
            "objective": {"frequency": {"0": "1/2", "1": "1/2"}, "value": "1/2"},
        }
        result = check_lp_certificate(data)
        topology = result.topology
        induced_assignments = [
            stt_induced_assignment(topology, stt)
            for stt in enumerate_stts(topology, depth_base=1)
        ]
        self.assertTrue(result.feasible)
        self.assertNotIn(result.assignment, induced_assignments)

    def test_checked_in_lp_examples_pass(self):
        path = check_lp_certificate(self.load_lp_example("path_4_stt_induced_lp.json"))
        self.assertEqual(path.objective.computed_value, Fraction(1))

        star = check_lp_certificate(self.load_lp_example("star_4_stt_induced_lp.json"))
        self.assertEqual(star.objective.computed_value, Fraction(3, 4))

    def test_invalid_lp_certificate_fails(self):
        with self.assertRaisesRegex(ValueError, "LP feasibility failed"):
            check_lp_certificate(self.load_lp_example("path_4_negative_d_invalid.json"))

    def test_cli_check_lp_pass_and_fail(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            code = cli_main(
                ["check-lp", str(ROOT / "examples" / "stt_lp" / "path_4_stt_induced_lp.json")]
            )
        self.assertEqual(code, 0)
        self.assertIn("PASS", stdout.getvalue())
        self.assertIn("depth_objective=1", stdout.getvalue())

        stderr = io.StringIO()
        with redirect_stderr(stderr):
            code = cli_main(
                [
                    "check-lp",
                    str(ROOT / "examples" / "stt_lp" / "path_4_negative_d_invalid.json"),
                ]
            )
        self.assertEqual(code, 1)
        self.assertIn("nonnegativity", stderr.getvalue())

    def test_cli_check_lp_verbose_and_normalized_json(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            code = cli_main(
                [
                    "check-lp",
                    str(ROOT / "examples" / "stt_lp" / "star_4_stt_induced_lp.json"),
                    "--verbose",
                    "--normalized-json",
                ]
            )
        output = stdout.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("Variable counts: D=4 X=12 Z=3", output)
        self.assertIn('"feasible": true', output)
        self.assertIn('"computed_depth_objective_value": "3/4"', output)


if __name__ == "__main__":
    unittest.main()
