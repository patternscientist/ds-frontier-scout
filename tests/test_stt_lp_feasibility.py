import copy
import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from fractions import Fraction
from pathlib import Path

from scripts.stt_checker.certificates import load_json
from scripts.stt_checker.cli import main as cli_main
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
        self.assertIn(
            "nonnegativity",
            {violation.family for violation in check_constraints(topology, domains, nonnegative)},
        )

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

    def test_objective_recomputes_exactly(self):
        result = check_lp_certificate(self.load_lp_example("path_4_stt_induced_lp.json"))
        self.assertIsNotNone(result.objective)
        self.assertEqual(result.objective.computed_value, Fraction(1))
        self.assertEqual(result.objective.search_cost_value, Fraction(2))

        bad = self.load_lp_example("path_4_stt_induced_lp.json")
        bad["objective"]["value"] = "2"
        with self.assertRaisesRegex(ValueError, "objective.value"):
            check_lp_certificate(bad)

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


if __name__ == "__main__":
    unittest.main()
