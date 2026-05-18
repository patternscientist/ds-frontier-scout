import importlib.util
import json
import sys
from pathlib import Path
from unittest import mock

from list_update_eval.evaluate import build_report
from list_update_eval.openevolve_adapter import (
    ADAPTER_SCHEMA_VERSION,
    evaluate_candidate,
    main as adapter_main,
    score_evaluator_report,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "list_update_openevolve"
CANDIDATES = EXAMPLES / "candidates"


def test_adapter_parses_milestone1_json_report_for_one_policy():
    evaluator_report = json.loads(
        (ROOT / "reports" / "list_update_eval_smoke.json").read_text(
            encoding="utf-8"
        )
    )

    report = score_evaluator_report(
        evaluator_report,
        policy_name="move_to_front",
        policy_path="builtin:move_to_front",
    )

    assert report["schema_version"] == ADAPTER_SCHEMA_VERSION
    assert report["valid"] is True
    assert report["total_cost"] == 42
    assert report["ratio_vs_mtf"] == 1.0
    assert report["offline_oracle_regret"] == 4
    assert report["metrics"]["combined_score"] == report["combined_score"]


def test_valid_candidate_scoring_and_report_fields():
    report = evaluate_candidate(str(CANDIDATES / "mtf_like.py"), suite="smoke")

    assert report["valid"] is True
    assert report["timeout"] is False
    assert report["nondeterminism"] is False
    assert report["total_cost"] == 42
    assert report["ratio_vs_mtf"] == 1.0
    assert report["offline_oracle_ratio"] == 42 / 38
    assert "source_length" in report["policy_complexity"]
    assert "average_position_shift_per_request" in report["movement_aggressiveness"]


def test_static_candidate_is_valid_but_scores_below_mtf_like_candidate():
    mtf = evaluate_candidate(str(CANDIDATES / "mtf_like.py"), suite="smoke")
    static = evaluate_candidate(str(CANDIDATES / "static_no_move.py"), suite="smoke")

    assert static["valid"] is True
    assert static["total_cost"] == 54
    assert static["ratio_vs_mtf"] == 54 / 42
    assert mtf["combined_score"] > static["combined_score"]


def test_invalid_candidate_is_penalized_not_silently_accepted():
    report = evaluate_candidate(
        str(CANDIDATES / "invalid_return_type.py"),
        suite="smoke",
    )

    assert report["valid"] is False
    assert report["invalid_policy"] is True
    assert report["timeout"] is False
    assert report["combined_score"] < 0
    assert "choose_update must return an integer" in report["artifacts"]["evaluator_error"]


def test_timeout_candidate_is_penalized_with_short_test_bound():
    report = evaluate_candidate(
        str(CANDIDATES / "timeout_candidate.py"),
        suite="smoke",
        timeout_seconds=0.2,
    )

    assert report["valid"] is False
    assert report["invalid_policy"] is True
    assert report["timeout"] is True
    assert report["combined_score"] < -1000


def test_nondeterministic_candidate_is_detected_and_penalized():
    report = evaluate_candidate(
        str(CANDIDATES / "nondeterministic_candidate.py"),
        suite="smoke",
    )

    assert report["valid"] is False
    assert report["invalid_policy"] is True
    assert report["nondeterminism"] is True
    assert report["combined_score"] < 0


def test_scoring_is_deterministic_on_repeated_calls():
    first = evaluate_candidate(str(CANDIDATES / "mtf_like.py"), suite="smoke")
    second = evaluate_candidate(str(CANDIDATES / "mtf_like.py"), suite="smoke")

    checked_keys = (
        "combined_score",
        "valid",
        "total_cost",
        "ratio_vs_mtf",
        "offline_oracle_ratio",
        "offline_oracle_regret",
        "policy_complexity",
        "movement_aggressiveness",
    )
    assert {key: first[key] for key in checked_keys} == {
        key: second[key] for key in checked_keys
    }


def test_adapter_cli_writes_json_report(tmp_path: Path):
    out_path = tmp_path / "adapter_report.json"

    status = adapter_main(
        [
            "--policy",
            str(EXAMPLES / "initial_program.py"),
            "--suite",
            "smoke",
            "--out",
            str(out_path),
        ]
    )

    assert status == 0
    payload = json.loads(out_path.read_text(encoding="utf-8"))
    assert payload["valid"] is True
    assert payload["policy_path"] == str((EXAMPLES / "initial_program.py").resolve())
    assert payload["report_path"] == str(out_path.resolve())


def test_evaluator_entry_point_works_without_openevolve_dependency():
    evaluator_path = EXAMPLES / "evaluator.py"
    spec = importlib.util.spec_from_file_location(
        "list_update_openevolve_example_evaluator",
        evaluator_path,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    with mock.patch.dict(
        sys.modules,
        {"openevolve": None, "openevolve.evaluation_result": None},
    ):
        result = module.evaluate(str(EXAMPLES / "initial_program.py"))

    assert isinstance(result, dict)
    assert result["metrics"]["valid"] is True
    assert result["metrics"]["combined_score"] == result["metrics"]["fitness"]
    assert result["artifacts"]["suite"] == "smoke"


def test_score_evaluator_report_requires_policy_name_for_multi_policy_reports():
    evaluator_report = build_report(suite_name="smoke", all_baselines=True)

    try:
        score_evaluator_report(evaluator_report)
    except ValueError as exc:
        assert "multiple policies" in str(exc)
    else:
        raise AssertionError("multi-policy report should require policy_name")
