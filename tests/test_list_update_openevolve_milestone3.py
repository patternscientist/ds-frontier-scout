import importlib.util
import json
from pathlib import Path

import pytest

from list_update_eval.openevolve_adapter import evaluate_candidate

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "examples" / "list_update_openevolve" / "config_tiny_milestone3.yaml"
ZERO_CONFIG = (
    ROOT
    / "examples"
    / "list_update_openevolve"
    / "config_tiny_milestone3_ollama.yaml"
)
RUNNER = ROOT / "scripts" / "run_list_update_openevolve_tiny_milestone3.py"
ZERO_RUNNER = (
    ROOT
    / "scripts"
    / "run_list_update_openevolve_zero_money_milestone3.py"
)


def _load_runner():
    spec = importlib.util.spec_from_file_location(
        "run_list_update_openevolve_tiny_milestone3",
        RUNNER,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _load_zero_runner():
    spec = importlib.util.spec_from_file_location(
        "run_list_update_openevolve_zero_money_milestone3",
        ZERO_RUNNER,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_tiny_milestone3_config_uses_smoke_paths_and_local_artifacts():
    text = CONFIG.read_text(encoding="utf-8")

    assert "integration dry-run only" in text
    assert "not a\n# serious search" in text
    assert "examples/list_update_openevolve/initial_program.py" in text
    assert "examples/list_update_openevolve/evaluator.py" in text
    assert "api_key: ${OPENAI_API_KEY}" in text
    assert "population_size: 2" in text
    assert "max_iterations: 1" in text
    assert "timeout: 10" in text
    assert "db_path: runs/list_update_openevolve_milestone3_tiny/database" in text
    assert "artifacts_base_path: runs/list_update_openevolve_milestone3_tiny/artifacts" in text
    assert (ROOT / "examples" / "list_update_openevolve" / "initial_program.py").exists()
    assert (ROOT / "examples" / "list_update_openevolve" / "evaluator.py").exists()


def test_zero_money_local_config_has_ollama_one_iteration_shape():
    text = ZERO_CONFIG.read_text(encoding="utf-8")

    assert "zero-money local-model" in text
    assert "api_base: http://localhost:11434/v1" in text
    assert "api_key: ollama" in text
    assert "OPENAI_API_KEY" not in text
    assert "api.openai.com" not in text
    assert "primary_model: qwen2.5-coder:1.5b" in text
    assert "max_tokens: 512" in text
    assert "max_iterations: 1" in text
    assert "population_size: 2" in text
    assert "use_llm_feedback: false" in text
    assert "not discovery" in text


def test_runner_fails_gracefully_when_openevolve_is_unavailable(monkeypatch, tmp_path):
    runner = _load_runner()
    monkeypatch.setattr(
        runner,
        "_find_openevolve_invocation",
        lambda _config, _run_dir: None,
    )

    status_path = tmp_path / "status.json"
    run_dir = tmp_path / "run"
    status = runner.main(
        [
            "--run-dir",
            str(run_dir),
            "--status-out",
            str(status_path),
        ]
    )

    assert status == 2
    payload = json.loads(status_path.read_text(encoding="utf-8"))
    assert payload["status"] == "blocked"
    assert payload["openevolve_available"] is False
    assert payload["artifact_dir"] == str(run_dir.resolve())
    assert "find_spec('openevolve')" in payload["blockers"][0]
    assert "openevolve" in " ".join(payload["setup_instructions"]).lower()
    assert (run_dir / CONFIG.name).exists()


def test_runner_blocks_cleanly_when_openevolve_has_no_api_key(monkeypatch, tmp_path):
    runner = _load_runner()
    fake_cli = runner.OpenEvolveInvocation(["openevolve-run", "fake"], "cli")
    monkeypatch.setattr(runner, "_find_openevolve_invocation", lambda _config, _run_dir: fake_cli)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    status_path = tmp_path / "status.json"
    status = runner.main(
        [
            "--run-dir",
            str(tmp_path / "run"),
            "--status-out",
            str(status_path),
        ]
    )

    assert status == 2
    payload = json.loads(status_path.read_text(encoding="utf-8"))
    assert payload["status"] == "blocked"
    assert payload["openevolve_available"] is True
    assert payload["command"] == ["openevolve-run", "fake"]
    assert "OPENAI_API_KEY is not set" in payload["blockers"][0]


def test_zero_money_runner_blocks_gracefully_when_local_endpoint_is_unavailable(
    monkeypatch,
    tmp_path,
):
    runner = _load_zero_runner()
    fake_cli = runner.OpenEvolveInvocation(["openevolve-run", "fake"], "cli")
    monkeypatch.setattr(runner, "_find_openevolve_invocation", lambda _config, _run_dir: fake_cli)
    monkeypatch.setattr(
        runner,
        "probe_ollama_cli",
        lambda: {
            "installed": False,
            "path": None,
            "list_attempted": False,
            "list_returncode": None,
            "models": [],
            "stdout": "",
            "stderr": "",
            "reason": "ollama executable was not found on PATH",
        },
    )
    monkeypatch.setattr(
        runner,
        "probe_local_model_endpoint",
        lambda _api_base, timeout_seconds=2.0: {
            "available": False,
            "api_base": "http://localhost:11434/v1",
            "models_url": "http://localhost:11434/v1/models",
            "status_code": None,
            "reason": "ConnectionRefusedError: test endpoint down",
            "models": [],
            "raw_model_count": 0,
        },
    )

    status_path = tmp_path / "status.json"
    status = runner.main(
        [
            "--run-dir",
            str(tmp_path / "run"),
            "--status-out",
            str(status_path),
        ]
    )

    assert status == 2
    payload = json.loads(status_path.read_text(encoding="utf-8"))
    assert payload["status"] == "blocked"
    assert payload["zero_money_local_model_test"] is True
    assert payload["stubbed_transport"] is False
    assert payload["openevolve_available"] is True
    assert "local OpenAI-compatible endpoint is unavailable" in payload["blockers"][0]
    assert "OPENAI_API_KEY" in payload["setup_instructions"][-1]
    assert payload["real_local_llm_run_attempted"] is False
    assert payload["real_local_llm_mutation_obtained"] is False


def test_zero_money_candidate_hash_and_structural_classification(tmp_path):
    runner = _load_zero_runner()
    initial_path = ROOT / "examples" / "list_update_openevolve" / "initial_program.py"
    initial_text = initial_path.read_text(encoding="utf-8")
    run_dir = tmp_path / "run"
    run_dir.mkdir()

    unchanged_snapshot = run_dir / "initial_program.py"
    generated_identical = run_dir / "program_001.py"
    line_ending_copy = run_dir / "best_program.py"
    evolve_only = run_dir / "program_002.py"
    outside_evolve = run_dir / "program_003.py"

    initial_bytes = initial_path.read_bytes()
    unchanged_snapshot.write_bytes(initial_bytes)
    generated_identical.write_bytes(initial_bytes)
    line_ending_copy.write_bytes(initial_text.replace("\n", "\r\n").encode("utf-8"))
    evolve_only.write_text(
        initial_text.replace("target_index = 0", "target_index = len(state) - 1"),
        encoding="utf-8",
    )
    outside_evolve.write_text(
        initial_text.replace("future list-update OpenEvolve runs", "outside edit"),
        encoding="utf-8",
    )

    snapshot_record = runner.classify_candidate_path(
        unchanged_snapshot,
        initial_path,
        run_dir,
    )
    identical_record = runner.classify_candidate_path(
        generated_identical,
        initial_path,
        run_dir,
    )
    line_ending_record = runner.classify_candidate_path(
        line_ending_copy,
        initial_path,
        run_dir,
    )
    evolve_record = runner.classify_candidate_path(evolve_only, initial_path, run_dir)
    outside_record = runner.classify_candidate_path(outside_evolve, initial_path, run_dir)

    assert len(snapshot_record["initial_sha256"]) == 64
    assert len(evolve_record["candidate_sha256"]) == 64
    assert snapshot_record["structural_class"] == "unchanged_initial_snapshot"
    assert snapshot_record["generated_changed_candidate"] is False
    assert identical_record["structural_class"] == "generated_candidate_identical_to_initial"
    assert identical_record["generated_changed_candidate"] is False
    assert line_ending_record["raw_sha256_changed"] is True
    assert line_ending_record["text_equal_to_initial_ignoring_line_endings"] is True
    assert line_ending_record["structural_class"] == "generated_candidate_identical_to_initial"
    assert line_ending_record["generated_changed_candidate"] is False
    assert evolve_record["structural_class"] == "generated_candidate_changed_evolve_block_only"
    assert evolve_record["changes_only_evolve_block"] is True
    assert evolve_record["generated_changed_candidate"] is True
    assert outside_record["structural_class"] == "candidate_changed_outside_evolve_block"
    assert outside_record["changes_only_evolve_block"] is False
    assert outside_record["generated_changed_candidate"] is True


def test_zero_money_candidate_evaluation_classes_are_distinct(tmp_path):
    runner = _load_zero_runner()
    initial_path = ROOT / "examples" / "list_update_openevolve" / "initial_program.py"
    initial_text = initial_path.read_text(encoding="utf-8")
    candidate = tmp_path / "candidate.py"
    candidate.write_text(
        initial_text.replace("target_index = 0", "target_index = len(state) - 1"),
        encoding="utf-8",
    )

    def classify_with(report):
        return runner.classify_candidate_path(
            candidate,
            initial_path,
            tmp_path,
            {
                "adapter_command": ["python", "-m", "list_update_eval.openevolve_adapter"],
                "adapter_report_path": str(tmp_path / "report.json"),
                "adapter_command_returncode": 0,
                "stdout": "",
                "stderr": "",
                "report": report,
            },
        )["final_class"]

    assert classify_with({"invalid_policy": True, "timeout": False, "nondeterminism": False}) == "invalid_candidate"
    assert classify_with({"invalid_policy": False, "timeout": True, "nondeterminism": False}) == "timeout_candidate"
    assert classify_with({"invalid_policy": False, "timeout": False, "nondeterminism": True}) == "nondeterministic_candidate"
    assert (
        classify_with({"invalid_policy": False, "timeout": False, "nondeterminism": False})
        == "generated_candidate_changed_evolve_block_only"
    )


def test_zero_money_extracts_openevolve_json_program_candidates(tmp_path):
    runner = _load_zero_runner()
    initial_path = ROOT / "examples" / "list_update_openevolve" / "initial_program.py"
    program_dir = tmp_path / "database" / "programs"
    program_dir.mkdir(parents=True)
    program_json = program_dir / "candidate.json"
    program_json.write_text(
        json.dumps(
            {
                "id": "candidate:with spaces",
                "code": initial_path.read_text(encoding="utf-8").replace(
                    "target_index = 0",
                    "target_index = len(state) - 1",
                ),
            }
        ),
        encoding="utf-8",
    )

    extracted = runner.extract_program_json_candidates(tmp_path)

    assert len(extracted) == 1
    assert extracted[0].name == "candidate_with_spaces.py"
    assert "target_index = len(state) - 1" in extracted[0].read_text(encoding="utf-8")


def test_generated_policy_artifacts_if_present_satisfy_policy_interface():
    runner = _load_runner()
    run_dir = ROOT / "runs" / "list_update_openevolve_milestone3_tiny"
    candidates = runner.discover_candidate_paths(run_dir)
    if not candidates:
        pytest.skip("No generated Milestone 3 candidates are present in this checkout.")

    for candidate in candidates:
        block_check = runner.check_evolve_block_only(
            candidate,
            ROOT / "examples" / "list_update_openevolve" / "initial_program.py",
        )
        assert block_check["ok"], block_check["reason"]
        report = evaluate_candidate(str(candidate), suite="smoke")
        assert report["schema_version"].startswith("list_update_eval.openevolve_adapter")
        assert "valid" in report


def test_zero_money_generated_candidates_if_present_are_evolve_only_and_evaluable():
    runner = _load_zero_runner()
    run_dir = ROOT / "runs" / "list_update_openevolve_milestone3z_zero_money"
    records = runner.classify_candidate_tree(
        run_dir,
        ROOT / "examples" / "list_update_openevolve" / "initial_program.py",
    )
    changed_records = [record for record in records if record["generated_changed_candidate"]]
    if not changed_records:
        pytest.skip("No generated Milestone 3z candidates are present in this checkout.")

    for record in changed_records:
        assert record["changes_only_evolve_block"], record["reason"]
        report = evaluate_candidate(record["candidate_path"], suite="smoke")
        assert report["schema_version"].startswith("list_update_eval.openevolve_adapter")
        assert "valid" in report
