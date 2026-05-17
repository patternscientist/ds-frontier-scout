from pathlib import Path

from list_update_eval.baselines import BASELINE_POLICIES
from list_update_eval.evaluate import build_report, main as evaluate_main
from list_update_eval.policy_api import evaluate_policy_on_trace
from list_update_eval.workloads import build_suite


def test_hand_computed_tiny_trace_costs_and_shifts():
    evaluation = evaluate_policy_on_trace(
        BASELINE_POLICIES["move_to_front"],
        trace=(1, 0),
        n=2,
    )

    assert evaluation.total_cost == 4
    assert tuple(step.access_cost for step in evaluation.steps) == (2, 2)
    assert tuple(step.position_shift for step in evaluation.steps) == (1, 1)
    assert evaluation.final_state == (0, 1)


def test_frequency_count_baseline_uses_history_under_same_interface():
    evaluation = evaluate_policy_on_trace(
        BASELINE_POLICIES["frequency_count"],
        trace=(2, 1, 2),
        n=3,
    )

    assert evaluation.total_cost == 7
    assert tuple(step.state_after for step in evaluation.steps) == (
        (2, 0, 1),
        (2, 1, 0),
        (2, 1, 0),
    )


def test_workload_generation_is_deterministic():
    assert build_suite("random_fixed_seed") == build_suite("random_fixed_seed")
    assert build_suite("locality_biased") == build_suite("locality_biased")


def test_invalid_external_policy_is_rejected(tmp_path: Path):
    policy_path = tmp_path / "bad_policy.py"
    policy_path.write_text(
        "def choose_update(state, request, history):\n"
        "    return 'front'\n",
        encoding="utf-8",
    )

    report = build_report(
        suite_name="smoke",
        policy_path=str(policy_path),
        timeout_seconds=5.0,
    )

    metrics = report["policies"]["bad_policy"]
    assert metrics["invalid_policy"] is True
    assert metrics["timeout"] is False
    assert "choose_update must return an integer" in metrics["error"]


def test_json_report_contains_required_metric_fields():
    report = build_report(suite_name="smoke", all_baselines=True)
    metrics = report["policies"]["move_to_front"]

    assert report["schema_version"] == "list_update_eval.milestone1.v0"
    assert metrics["total_cost"] == 42
    assert metrics["mean_cost"] == 2
    assert metrics["worst_trace_cost"]["cost"] == 14
    assert set(("move_to_front", "transpose", "frequency_count")).issubset(
        metrics["baseline_ratios"]
    )
    assert metrics["oracle"]["available"] is True
    assert metrics["invalid_policy"] is False
    assert metrics["timeout"] is False
    assert "source_length" in metrics["policy_complexity"]
    assert "average_position_shift_per_request" in metrics["movement_aggressiveness"]


def test_smoke_cli_writes_json_report(tmp_path: Path, capsys):
    out_path = tmp_path / "smoke.json"

    status = evaluate_main(
        [
            "--suite",
            "smoke",
            "--all-baselines",
            "--out",
            str(out_path),
        ]
    )

    captured = capsys.readouterr()
    assert status == 0
    assert out_path.exists()
    assert "suite=smoke traces=5 requests=21" in captured.out
    assert "move_to_front 42 2" in captured.out
