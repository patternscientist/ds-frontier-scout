import json
import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

from scripts.stt_checker.ds21_normal_cones import (
    _certificates_json,
    run_coverage,
    run_scan,
    write_outputs,
)


class DS21NormalConeTests(unittest.TestCase):
    def test_grid_bound_two_discovers_only_tied_incoherent_faces(self):
        data = run_scan(grid_bound=2)
        faces = data["certificates"]
        self.assertGreaterEqual(len(faces), 1)
        self.assertFalse(
            any(face.outcome == "reduced_lb_h1_counterexample" for face in faces)
        )
        self.assertTrue(
            all(
                face.outcome
                == "exposed_incoherent_face_tied_with_coherent_deterministic_witness"
                for face in faces
            )
        )
        self.assertEqual(data["arrangement"]["variable_count"], 18)
        self.assertEqual(data["arrangement"]["row_count_without_nonnegativity"], 43)

    def test_write_outputs_emits_report_and_json(self):
        with TemporaryDirectory() as directory:
            report = Path(directory) / "report.md"
            certificates = Path(directory) / "certificates.json"
            result = write_outputs(report, certificates, grid_bound=1)
            self.assertTrue(report.read_text(encoding="utf-8").startswith("# DS(2,1)"))
            payload = json.loads(certificates.read_text(encoding="utf-8"))
            self.assertEqual(payload["schema"], "stt_ds21_normal_cones_v1_coverage")
            self.assertIn("strict_heavy_cells", payload)
            self.assertEqual(result["unresolved"], 0)

    def test_v1_coverage_has_structural_classifiers_for_v0_faces(self):
        data = run_coverage()
        self.assertEqual(data["settings"]["kink_cells_considered"], 576)
        self.assertFalse(
            any(
                cert.outcome == "rational_reduced_counterexample"
                for cert in data["coverage_certificates"]
            )
        )
        payload = _certificates_json(data)
        self.assertGreaterEqual(len(payload["v0_discovered_faces"]), 1)
        self.assertIn(
            "structural_classification",
            payload["v0_discovered_faces"][0],
        )
        self.assertIn("witness_class", payload["v0_discovered_faces"][0])


if __name__ == "__main__":
    unittest.main()
