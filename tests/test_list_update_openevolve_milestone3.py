import importlib.util
import json
from pathlib import Path

import pytest

from list_update_eval.openevolve_adapter import evaluate_candidate

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "examples" / "list_update_openevolve" / "config_tiny_milestone3.yaml"
RUNNER = ROOT / "scripts" / "run_list_update_openevolve_tiny_milestone3.py"


def _load_runner():
    spec = importlib.util.spec_from_file_location(
        "run_list_update_openevolve_tiny_milestone3",
        RUNNER,
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
