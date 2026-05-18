"""Run the Milestone 3 tiny OpenEvolve/list-update integration check.

This runner is intentionally small and defensive. It either invokes an
available OpenEvolve command on the tiny Milestone 3 config, or writes a
recoverable blocked status explaining that OpenEvolve is unavailable.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import site
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = (
    REPO_ROOT / "examples" / "list_update_openevolve" / "config_tiny_milestone3.yaml"
)
DEFAULT_INITIAL_PROGRAM = (
    REPO_ROOT / "examples" / "list_update_openevolve" / "initial_program.py"
)
DEFAULT_EVALUATOR = REPO_ROOT / "examples" / "list_update_openevolve" / "evaluator.py"
DEFAULT_RUN_DIR = REPO_ROOT / "runs" / "list_update_openevolve_milestone3_tiny"
DEFAULT_STATUS_PATH = DEFAULT_RUN_DIR / "milestone3_tiny_run_status.json"
DEFAULT_BEST_REPORT = REPO_ROOT / "reports" / "list_update_openevolve_milestone3_best_smoke.json"
SCHEMA_VERSION = "list_update_openevolve_milestone3_runner.v0"


class OpenEvolveInvocation:
    def __init__(self, command: list[str], kind: str) -> None:
        self.command = command
        self.kind = kind


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python scripts/run_list_update_openevolve_tiny_milestone3.py"
    )
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--run-dir", default=str(DEFAULT_RUN_DIR))
    parser.add_argument("--status-out", default=None)
    parser.add_argument("--process-timeout-seconds", type=float, default=180.0)
    args = parser.parse_args(argv)

    config_path = Path(args.config).resolve()
    run_dir = Path(args.run_dir).resolve()
    status_path = (
        Path(args.status_out).resolve()
        if args.status_out
        else run_dir / DEFAULT_STATUS_PATH.name
    )
    run_dir.mkdir(parents=True, exist_ok=True)

    if not config_path.exists():
        status = _status_payload(
            status="failed",
            config_path=config_path,
            run_dir=run_dir,
            blockers=[f"config file does not exist: {config_path}"],
        )
        _write_json(status_path, status)
        print(f"FAIL: missing config; wrote {status_path}", file=sys.stderr)
        return 1

    shutil.copy2(config_path, run_dir / config_path.name)
    invocation = _find_openevolve_invocation(config_path, run_dir)
    if invocation is None:
        blockers = [
            "importlib.util.find_spec('openevolve') returned None",
            "no 'openevolve-run' executable was found on PATH or in the Python user Scripts directory",
        ]
        status = _status_payload(
            status="blocked",
            config_path=config_path,
            run_dir=run_dir,
            openevolve_available=False,
            blockers=blockers,
        )
        _write_json(status_path, status)
        print("BLOCKED: OpenEvolve is not importable or runnable in this Python environment.")
        print(f"wrote {status_path}")
        return 2

    setup_blockers = _setup_blockers()
    if setup_blockers:
        status = _status_payload(
            status="blocked",
            config_path=config_path,
            run_dir=run_dir,
            openevolve_available=True,
            command=invocation.command,
            blockers=setup_blockers,
        )
        _write_json(status_path, status)
        print("BLOCKED: OpenEvolve is installed, but this environment is missing required run setup.")
        print(f"wrote {status_path}")
        return 2

    command_path = run_dir / "openevolve_command.json"
    stdout_path = run_dir / "openevolve_stdout.txt"
    stderr_path = run_dir / "openevolve_stderr.txt"
    _write_json(
        command_path,
        {
            "schema_version": SCHEMA_VERSION,
            "cwd": str(REPO_ROOT),
            "command": invocation.command,
            "invocation_kind": invocation.kind,
        },
    )

    try:
        completed = subprocess.run(
            invocation.command,
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            timeout=args.process_timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stdout_path.write_text(exc.stdout or "", encoding="utf-8")
        stderr_path.write_text(exc.stderr or "", encoding="utf-8")
        status = _status_payload(
            status="failed",
            config_path=config_path,
            run_dir=run_dir,
            openevolve_available=True,
            command=invocation.command,
            returncode=124,
            stdout_path=stdout_path,
            stderr_path=stderr_path,
            blockers=[f"OpenEvolve process exceeded {args.process_timeout_seconds} seconds"],
        )
        _write_json(status_path, status)
        print(f"FAIL: OpenEvolve timed out; wrote {status_path}", file=sys.stderr)
        return 124

    stdout_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")
    candidates = discover_candidate_paths(run_dir)
    candidate_checks = [
        check_evolve_block_only(candidate, DEFAULT_INITIAL_PROGRAM)
        for candidate in candidates
    ]
    candidate_evaluations = evaluate_generated_candidates(
        candidates,
        run_dir / "candidate_evaluations",
    )
    best_report_path = write_best_candidate_report(candidate_evaluations)

    status_name = "succeeded" if completed.returncode == 0 else "failed"
    if completed.returncode == 0 and not candidates:
        status_name = "partial"
    if completed.returncode == 0 and any(not check["ok"] for check in candidate_checks):
        status_name = "failed"

    status = _status_payload(
        status=status_name,
        config_path=config_path,
        run_dir=run_dir,
        openevolve_available=True,
        command=invocation.command,
        returncode=completed.returncode,
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        candidate_paths=[str(path) for path in candidates],
        evolve_block_checks=candidate_checks,
        candidate_evaluations=candidate_evaluations,
        best_candidate_report_path=str(best_report_path) if best_report_path else None,
    )
    _write_json(status_path, status)
    print(f"{status_name.upper()}: OpenEvolve returncode={completed.returncode}; wrote {status_path}")
    return 0 if status_name == "succeeded" else 1


def discover_candidate_paths(run_dir: Path) -> list[Path]:
    """Return generated-looking policy modules under the run artifact tree."""

    if not run_dir.exists():
        return []
    candidates: list[Path] = []
    for path in sorted(run_dir.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if "def choose_update" in text:
            candidates.append(path.resolve())
    return candidates


def check_evolve_block_only(candidate_path: Path, initial_path: Path) -> dict[str, Any]:
    """Check that a candidate changed only the marked EVOLVE block."""

    try:
        initial = _split_evolve_block(initial_path.read_text(encoding="utf-8"))
        candidate = _split_evolve_block(candidate_path.read_text(encoding="utf-8"))
    except ValueError as exc:
        return {
            "candidate_path": str(candidate_path),
            "ok": False,
            "reason": str(exc),
        }

    ok = initial["prefix"] == candidate["prefix"] and initial["suffix"] == candidate["suffix"]
    return {
        "candidate_path": str(candidate_path),
        "ok": ok,
        "reason": None if ok else "candidate changed text outside the marked EVOLVE block",
    }


def evaluate_generated_candidates(
    candidates: list[Path],
    report_dir: Path,
) -> list[dict[str, Any]]:
    """Evaluate every generated candidate through the deterministic adapter."""

    if not candidates:
        return []
    from list_update_eval.openevolve_adapter import evaluate_candidate

    report_dir.mkdir(parents=True, exist_ok=True)
    evaluations: list[dict[str, Any]] = []
    for index, candidate in enumerate(candidates):
        report_path = report_dir / f"candidate_{index:03d}_{candidate.stem}_smoke.json"
        report = evaluate_candidate(
            policy_path=str(candidate),
            suite="smoke",
            out_path=str(report_path),
        )
        evaluations.append(
            {
                "candidate_path": str(candidate),
                "adapter_report_path": str(report_path.resolve()),
                "valid": report["valid"],
                "invalid_policy": report["invalid_policy"],
                "timeout": report["timeout"],
                "nondeterminism": report["nondeterminism"],
                "combined_score": report["combined_score"],
                "total_cost": report["total_cost"],
                "ratio_vs_mtf": report["ratio_vs_mtf"],
                "offline_oracle_ratio": report["offline_oracle_ratio"],
                "offline_oracle_regret": report["offline_oracle_regret"],
            }
        )
    return evaluations


def write_best_candidate_report(
    candidate_evaluations: list[dict[str, Any]],
) -> Path | None:
    """Copy the best generated-candidate adapter report to the stable reports path."""

    valid_evaluations = [
        evaluation for evaluation in candidate_evaluations if evaluation["valid"]
    ]
    if not valid_evaluations:
        return None
    best = max(
        valid_evaluations,
        key=lambda evaluation: (
            float(evaluation["combined_score"]),
            str(evaluation["candidate_path"]),
        ),
    )
    source = Path(str(best["adapter_report_path"]))
    DEFAULT_BEST_REPORT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, DEFAULT_BEST_REPORT)
    return DEFAULT_BEST_REPORT.resolve()


def _find_openevolve_invocation(
    config_path: Path,
    run_dir: Path,
) -> OpenEvolveInvocation | None:
    cli = (
        shutil.which("openevolve-run")
        or shutil.which("openevolve-run.exe")
        or _user_scripts_openevolve_run()
    )
    if cli:
        return OpenEvolveInvocation(
            command=[
                cli,
                str(DEFAULT_INITIAL_PROGRAM),
                str(DEFAULT_EVALUATOR),
                "--config",
                str(config_path),
                "--output",
                str(run_dir),
                "--iterations",
                "1",
                "--log-level",
                "INFO",
            ],
            kind="cli",
        )
    if importlib.util.find_spec("openevolve") is not None:
        return OpenEvolveInvocation(
            command=[
                sys.executable,
                "-m",
                "openevolve.cli",
                str(DEFAULT_INITIAL_PROGRAM),
                str(DEFAULT_EVALUATOR),
                "--config",
                str(config_path),
                "--output",
                str(run_dir),
                "--iterations",
                "1",
                "--log-level",
                "INFO",
            ],
            kind="python_module",
        )
    return None


def _user_scripts_openevolve_run() -> str | None:
    scripts_dir = (
        Path(site.USER_BASE)
        / f"Python{sys.version_info.major}{sys.version_info.minor}"
        / "Scripts"
    )
    for name in ("openevolve-run.exe", "openevolve-run"):
        candidate = scripts_dir / name
        try:
            if candidate.exists():
                return str(candidate)
        except OSError:
            continue
    return None


def _setup_blockers() -> list[str]:
    blockers: list[str] = []
    if not os_environ_truthy("OPENAI_API_KEY"):
        blockers.append(
            "OPENAI_API_KEY is not set; OpenEvolve can be imported but cannot request the one tiny mutation"
        )
    return blockers


def os_environ_truthy(name: str) -> bool:
    import os

    return bool(os.environ.get(name))


def _split_evolve_block(text: str) -> dict[str, str]:
    start_marker = "# EVOLVE-BLOCK-START"
    end_marker = "# EVOLVE-BLOCK-END"
    start = text.find(start_marker)
    end = text.find(end_marker)
    if start < 0 or end < 0 or end < start:
        raise ValueError("missing or malformed EVOLVE block markers")
    block_start = text.find("\n", start)
    if block_start < 0:
        raise ValueError("EVOLVE block start marker is not followed by a newline")
    return {
        "prefix": text[: block_start + 1],
        "block": text[block_start + 1 : end],
        "suffix": text[end:],
    }


def _status_payload(
    *,
    status: str,
    config_path: Path,
    run_dir: Path,
    openevolve_available: bool | None = None,
    command: list[str] | None = None,
    returncode: int | None = None,
    stdout_path: Path | None = None,
    stderr_path: Path | None = None,
    blockers: list[str] | None = None,
    candidate_paths: list[str] | None = None,
    evolve_block_checks: list[dict[str, Any]] | None = None,
    candidate_evaluations: list[dict[str, Any]] | None = None,
    best_candidate_report_path: str | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "openevolve_available": openevolve_available,
        "config_path": str(config_path),
        "artifact_dir": str(run_dir),
        "command": command,
        "returncode": returncode,
        "stdout_path": str(stdout_path) if stdout_path else None,
        "stderr_path": str(stderr_path) if stderr_path else None,
        "blockers": blockers or [],
        "setup_instructions": _setup_instructions(),
        "candidate_paths": candidate_paths or [],
        "evolve_block_checks": evolve_block_checks or [],
        "candidate_evaluations": candidate_evaluations or [],
        "best_candidate_report_path": best_candidate_report_path,
    }


def _setup_instructions() -> list[str]:
    return [
        "Install the intended OpenEvolve package into the Python environment used by this repository.",
        "Verify either `python -c \"import openevolve\"` succeeds or `openevolve-run --help` is available.",
        "Set OPENAI_API_KEY for the tiny one-iteration mutation request.",
        "Rerun `python scripts/run_list_update_openevolve_tiny_milestone3.py` from the repository root.",
    ]


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
