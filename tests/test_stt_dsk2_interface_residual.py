import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

from scripts.stt_checker.dsk2_interface_residual import (
    VERIFIED_H1_CERTIFICATE_STATUS,
    check_interface_identity,
    grouped_dual_rows,
    search_dsk2_h1_gap,
    write_outputs,
)


class DSK2InterfaceIdentityTests(unittest.TestCase):
    def test_corrected_residual_identity_holds_for_k_1_2_3(self):
        for k in (1, 2, 3):
            with self.subTest(k=k):
                audit = check_interface_identity(k)
                self.assertTrue(audit.identity_holds)
                self.assertGreater(audit.variables, 0)


class DSK2SearchHarnessTests(unittest.TestCase):
    def test_small_search_uses_verified_h1_certificates(self):
        data = search_dsk2_h1_gap(max_cases=3, integer_bound=1, dangerous_high=6)
        self.assertEqual(data["schema"], "dsk2_interface_residual_v0")
        self.assertEqual(len(data["cases"]), 3)
        self.assertTrue(all(audit.identity_holds for audit in data["identity_audits"]))
        self.assertTrue(
            all(
                case.h1.certificate_status == VERIFIED_H1_CERTIFICATE_STATUS
                for case in data["cases"]
            )
        )
        groups = grouped_dual_rows(data["cases"][0].h1)
        self.assertIn("promotion_rows_eta_le_y", groups["counts"])
        self.assertIn("interface_gap_rows_epsilon", groups["counts"])

    def test_write_outputs_emits_report_and_json(self):
        with TemporaryDirectory() as directory:
            report = Path(directory) / "report.md"
            certificates = Path(directory) / "certificates.json"
            result = write_outputs(
                report_path=report,
                certificate_path=certificates,
                max_cases=2,
                integer_bound=1,
                dangerous_high=6,
            )
            self.assertEqual(result["identity_failures"], 0)
            self.assertTrue(report.read_text(encoding="utf-8").startswith("# DS(k,2)"))
            self.assertIn(
                "representative_dangerous_chamber_certificates",
                certificates.read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
