"""Run the Milestone 3z zero-money OpenEvolve/list-update integration path.

This runner is intentionally honest about what did and did not happen. It
probes a local OpenAI-compatible endpoint, preferring Ollama at
http://localhost:11434/v1, and only invokes OpenEvolve when that local endpoint
is reachable. It never requires a paid API key.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import site
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = (
    REPO_ROOT
    / "examples"
    / "list_update_openevolve"
    / "config_tiny_milestone3_ollama.yaml"
)
DEFAULT_INITIAL_PROGRAM = (
    REPO_ROOT / "examples" / "list_update_openevolve" / "initial_program.py"
)
DEFAULT_EVALUATOR = REPO_ROOT / "examples" / "list_update_openevolve" / "evaluator.py"
DEFAULT_RUN_DIR = REPO_ROOT / "runs" / "list_update_openevolve_milestone3z_zero_money"
DEFAULT_STATUS_PATH = DEFAULT_RUN_DIR / "milestone3z_zero_money_status.json"
DEFAULT_BEST_REPORT = (
    REPO_ROOT / "reports" / "list_update_openevolve_milestone3z_best_smoke.json"
)
SCHEMA_VERSION = "list_update_openevolve_milestone3z_zero_money_runner.v0"
STUB_LABEL = (
    "Stubbed OpenAI-compatible transport test; fixed response, no model "
    "inference, no autonomous mutation, no policy discovery."
)


class OpenEvolveInvocation:
    def __init__(self, command: list[str], kind: str) -> None:
        self.command = command
        self.kind = kind


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python scripts/run_list_update_openevolve_zero_money_milestone3.py"
    )
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--run-dir", default=str(DEFAULT_RUN_DIR))
    parser.add_argument("--status-out", default=None)
    parser.add_argument("--api-base", default=None)
    parser.add_argument("--model", default=None)
    parser.add_argument("--endpoint-timeout-seconds", type=float, default=2.0)
    parser.add_argument("--process-timeout-seconds", type=float, default=300.0)
    parser.add_argument("--adapter-timeout-seconds", type=float, default=45.0)
    parser.add_argument("--stubbed-transport-label", default=None)
    args = parser.parse_args(argv)
    stubbed_transport_label = args.stubbed_transport_label

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
            api_base=args.api_base or "unknown",
            model=args.model or "unknown",
            blockers=[f"config file does not exist: {config_path}"],
        )
        _write_json(status_path, status)
        print(f"FAIL: missing config; wrote {status_path}", file=sys.stderr)
        return 1

    config_values = _read_local_config_values(config_path)
    api_base = args.api_base or config_values.get("api_base") or "http://localhost:11434/v1"
    model = args.model or config_values.get("primary_model") or "unknown-local-model"
    copied_config_path = run_dir / config_path.name
    if config_path != copied_config_path.resolve():
        shutil.copy2(config_path, copied_config_path)

    ollama_probe = probe_ollama_cli()
    endpoint_probe = probe_local_model_endpoint(
        api_base,
        timeout_seconds=args.endpoint_timeout_seconds,
    )
    invocation = _find_openevolve_invocation(config_path, run_dir)

    blockers: list[str] = []
    if not endpoint_probe["available"]:
        blockers.append(
            f"local OpenAI-compatible endpoint is unavailable at {api_base}: "
            f"{endpoint_probe['reason']}"
        )
    if invocation is None:
        blockers.append(
            "OpenEvolve is not runnable: importlib could not import openevolve "
            "and no openevolve-run executable was found on PATH or in the Python "
            "user Scripts directory"
        )

    if blockers:
        status = _status_payload(
            status="blocked",
            config_path=config_path,
            run_dir=run_dir,
            api_base=api_base,
            model=model,
            openevolve_available=invocation is not None,
            command=invocation.command if invocation else None,
            blockers=blockers,
            ollama_probe=ollama_probe,
            endpoint_probe=endpoint_probe,
            stubbed_transport_label=stubbed_transport_label,
        )
        _write_json(status_path, status)
        print("BLOCKED: zero-money local-model OpenEvolve run cannot start.")
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
            "zero_money_local_model_test": True,
            "stubbed_transport": bool(stubbed_transport_label),
            "stub_label": stubbed_transport_label,
            "api_base": api_base,
            "model": model,
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
    except OSError as exc:
        stdout_path.write_text("", encoding="utf-8")
        stderr_path.write_text(f"{type(exc).__name__}: {exc}\n", encoding="utf-8")
        status = _status_payload(
            status="failed",
            config_path=config_path,
            run_dir=run_dir,
            api_base=api_base,
            model=model,
            openevolve_available=True,
            command=invocation.command,
            returncode=None,
            stdout_path=stdout_path,
            stderr_path=stderr_path,
            blockers=[f"OpenEvolve process could not be started: {type(exc).__name__}: {exc}"],
            ollama_probe=ollama_probe,
            endpoint_probe=endpoint_probe,
            real_local_llm_run_attempted=not bool(stubbed_transport_label),
            stubbed_transport_label=stubbed_transport_label,
        )
        _write_json(status_path, status)
        print(f"FAIL: OpenEvolve could not start; wrote {status_path}", file=sys.stderr)
        return 1
    except subprocess.TimeoutExpired as exc:
        stdout_path.write_text(_safe_process_text(exc.stdout), encoding="utf-8")
        stderr_path.write_text(_safe_process_text(exc.stderr), encoding="utf-8")
        status = _status_payload(
            status="failed",
            config_path=config_path,
            run_dir=run_dir,
            api_base=api_base,
            model=model,
            openevolve_available=True,
            command=invocation.command,
            returncode=124,
            stdout_path=stdout_path,
            stderr_path=stderr_path,
            blockers=[f"OpenEvolve process exceeded {args.process_timeout_seconds} seconds"],
            ollama_probe=ollama_probe,
            endpoint_probe=endpoint_probe,
            real_local_llm_run_attempted=not bool(stubbed_transport_label),
            stubbed_transport_label=stubbed_transport_label,
        )
        _write_json(status_path, status)
        print(f"FAIL: OpenEvolve timed out; wrote {status_path}", file=sys.stderr)
        return 124

    stdout_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")

    extracted_candidate_paths = extract_program_json_candidates(run_dir)
    candidate_records = classify_candidate_tree(run_dir, DEFAULT_INITIAL_PROGRAM)
    candidate_records = evaluate_changed_candidates(
        candidate_records,
        run_dir / "candidate_evaluations",
        adapter_timeout_seconds=args.adapter_timeout_seconds,
    )
    best_report_path = write_best_changed_candidate_report(candidate_records)

    generated_changed = [
        record for record in candidate_records if record["generated_changed_candidate"]
    ]
    changed_outside_evolve = [
        record
        for record in generated_changed
        if record["structural_class"] == "candidate_changed_outside_evolve_block"
    ]
    failed_adapter = [
        record for record in generated_changed if record["final_class"] == "adapter_evaluation_failed"
    ]

    status_name = "succeeded" if completed.returncode == 0 else "failed"
    if completed.returncode == 0 and not generated_changed:
        status_name = "partial"
    if completed.returncode == 0 and (changed_outside_evolve or failed_adapter):
        status_name = "failed"

    status = _status_payload(
        status=status_name,
        config_path=config_path,
        run_dir=run_dir,
        api_base=api_base,
        model=model,
        openevolve_available=True,
        command=invocation.command,
        returncode=completed.returncode,
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        blockers=[] if status_name == "succeeded" else _post_run_blockers(
            completed.returncode,
            generated_changed,
            changed_outside_evolve,
            failed_adapter,
        ),
        candidate_records=candidate_records,
        extracted_candidate_paths=[str(path) for path in extracted_candidate_paths],
        best_candidate_report_path=str(best_report_path) if best_report_path else None,
        ollama_probe=ollama_probe,
        endpoint_probe=endpoint_probe,
        real_local_llm_run_attempted=not bool(stubbed_transport_label),
        real_local_llm_mutation_obtained=bool(generated_changed)
        and not bool(stubbed_transport_label),
        stubbed_transport_label=stubbed_transport_label,
    )
    _write_json(status_path, status)
    print(f"{status_name.upper()}: OpenEvolve returncode={completed.returncode}; wrote {status_path}")
    return 0 if status_name == "succeeded" else 1


def probe_ollama_cli() -> dict[str, Any]:
    """Return PATH and model-list information for a local Ollama install."""

    cli = shutil.which("ollama") or shutil.which("ollama.exe")
    probe: dict[str, Any] = {
        "installed": bool(cli),
        "path": cli,
        "list_attempted": False,
        "list_returncode": None,
        "models": [],
        "stdout": "",
        "stderr": "",
        "reason": None,
    }
    if not cli:
        probe["reason"] = "ollama executable was not found on PATH"
        return probe

    probe["list_attempted"] = True
    try:
        completed = subprocess.run(
            [cli, "list"],
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        probe["reason"] = f"ollama list failed: {type(exc).__name__}: {exc}"
        return probe

    probe["list_returncode"] = completed.returncode
    probe["stdout"] = completed.stdout
    probe["stderr"] = completed.stderr
    if completed.returncode == 0:
        probe["models"] = _parse_ollama_list_models(completed.stdout)
    else:
        probe["reason"] = f"ollama list returned {completed.returncode}"
    return probe


def probe_local_model_endpoint(
    api_base: str,
    *,
    timeout_seconds: float = 2.0,
) -> dict[str, Any]:
    """Probe a local OpenAI-compatible /models endpoint."""

    models_url = api_base.rstrip("/") + "/models"
    request = urllib.request.Request(
        models_url,
        headers={
            "Authorization": "Bearer ollama",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            body = response.read().decode("utf-8", errors="replace")
            payload = json.loads(body) if body else {}
            models = _extract_model_ids(payload)
            return {
                "available": True,
                "api_base": api_base,
                "models_url": models_url,
                "status_code": response.status,
                "reason": None,
                "models": models,
                "raw_model_count": len(models),
            }
    except urllib.error.HTTPError as exc:
        return {
            "available": False,
            "api_base": api_base,
            "models_url": models_url,
            "status_code": exc.code,
            "reason": f"HTTP {exc.code}: {exc.reason}",
            "models": [],
            "raw_model_count": 0,
        }
    except (OSError, TimeoutError, json.JSONDecodeError) as exc:
        return {
            "available": False,
            "api_base": api_base,
            "models_url": models_url,
            "status_code": None,
            "reason": f"{type(exc).__name__}: {exc}",
            "models": [],
            "raw_model_count": 0,
        }


def discover_candidate_paths(run_dir: Path) -> list[Path]:
    """Return policy-looking Python modules under the run artifact tree."""

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


def classify_candidate_tree(run_dir: Path, initial_path: Path) -> list[dict[str, Any]]:
    return [
        classify_candidate_path(candidate, initial_path, run_dir)
        for candidate in discover_candidate_paths(run_dir)
    ]


def extract_program_json_candidates(run_dir: Path) -> list[Path]:
    """Materialize OpenEvolve JSON program records as candidate .py files."""

    output_dir = run_dir / "extracted_candidates"
    extracted: list[Path] = []
    seen_destinations: set[Path] = set()
    if not run_dir.exists():
        return extracted
    for json_path in sorted(run_dir.rglob("*.json")):
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        if not isinstance(payload, dict):
            continue
        code = payload.get("code")
        if not isinstance(code, str) or "def choose_update" not in code:
            continue
        program_id = str(payload.get("id") or json_path.stem)
        destination = output_dir / f"{_safe_candidate_stem(program_id)}.py"
        resolved_destination = destination.resolve()
        if resolved_destination in seen_destinations:
            continue
        seen_destinations.add(resolved_destination)
        output_dir.mkdir(parents=True, exist_ok=True)
        if not code.endswith("\n"):
            code += "\n"
        destination.write_text(code, encoding="utf-8")
        extracted.append(resolved_destination)
    return extracted


def classify_candidate_path(
    candidate_path: Path,
    initial_path: Path = DEFAULT_INITIAL_PROGRAM,
    run_dir: Path | None = None,
    evaluation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Classify one candidate by hash, EVOLVE-block locality, and evaluation."""

    candidate_path = candidate_path.resolve()
    initial_path = initial_path.resolve()
    initial_sha256 = sha256_file(initial_path)
    candidate_sha256 = sha256_file(candidate_path)
    initial_text = initial_path.read_text(encoding="utf-8")
    candidate_text = candidate_path.read_text(encoding="utf-8")
    text_equal_to_initial = candidate_text == initial_text
    raw_sha256_changed = candidate_sha256 != initial_sha256
    changed_from_initial = not text_equal_to_initial
    record: dict[str, Any] = {
        "candidate_path": str(candidate_path),
        "candidate_sha256": candidate_sha256,
        "initial_path": str(initial_path),
        "initial_sha256": initial_sha256,
        "raw_sha256_changed": raw_sha256_changed,
        "text_equal_to_initial_ignoring_line_endings": text_equal_to_initial,
        "changed_from_initial": changed_from_initial,
        "generated_changed_candidate": changed_from_initial,
        "changes_only_evolve_block": False,
        "structural_class": None,
        "final_class": None,
        "reason": None,
        "adapter_evaluation": evaluation,
    }

    if not changed_from_initial:
        structural_class = (
            "unchanged_initial_snapshot"
            if _looks_like_initial_snapshot(candidate_path, initial_path, run_dir)
            else "generated_candidate_identical_to_initial"
        )
        record.update(
            {
                "generated_changed_candidate": False,
                "structural_class": structural_class,
                "final_class": structural_class,
                "reason": "candidate hash matches the initial program",
            }
        )
        return record

    try:
        initial_parts = _split_evolve_block(initial_text)
        candidate_parts = _split_evolve_block(candidate_text)
    except ValueError as exc:
        record.update(
            {
                "structural_class": "candidate_changed_outside_evolve_block",
                "final_class": "candidate_changed_outside_evolve_block",
                "reason": str(exc),
            }
        )
    else:
        changes_only_evolve = (
            initial_parts["prefix"] == candidate_parts["prefix"]
            and initial_parts["suffix"] == candidate_parts["suffix"]
            and initial_parts["block"] != candidate_parts["block"]
        )
        structural_class = (
            "generated_candidate_changed_evolve_block_only"
            if changes_only_evolve
            else "candidate_changed_outside_evolve_block"
        )
        record.update(
            {
                "changes_only_evolve_block": changes_only_evolve,
                "structural_class": structural_class,
                "final_class": structural_class,
                "reason": None
                if changes_only_evolve
                else "candidate changed text outside the marked EVOLVE block",
            }
        )

    if evaluation is not None:
        final_class = _evaluation_final_class(record, evaluation)
        record["final_class"] = final_class
        record["adapter_evaluation"] = evaluation
    return record


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def evaluate_changed_candidates(
    candidate_records: list[dict[str, Any]],
    report_dir: Path,
    *,
    adapter_timeout_seconds: float,
) -> list[dict[str, Any]]:
    """Run the adapter CLI for every candidate changed from the initial hash."""

    report_dir.mkdir(parents=True, exist_ok=True)
    updated_records: list[dict[str, Any]] = []
    changed_index = 0
    for record in candidate_records:
        if not record["generated_changed_candidate"]:
            updated_records.append(record)
            continue

        candidate = Path(str(record["candidate_path"]))
        report_path = report_dir / f"candidate_{changed_index:03d}_{candidate.stem}_smoke.json"
        command = [
            sys.executable,
            "-m",
            "list_update_eval.openevolve_adapter",
            "--policy",
            str(candidate),
            "--suite",
            "smoke",
            "--out",
            str(report_path),
        ]
        changed_index += 1
        evaluation: dict[str, Any] = {
            "adapter_command": command,
            "adapter_report_path": str(report_path.resolve()),
            "adapter_command_returncode": None,
            "stdout": "",
            "stderr": "",
            "report": None,
        }
        try:
            completed = subprocess.run(
                command,
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                timeout=adapter_timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            evaluation.update(
                {
                    "adapter_command_returncode": 124,
                    "stdout": _safe_process_text(exc.stdout),
                    "stderr": _safe_process_text(exc.stderr)
                    + f"\nAdapter process exceeded {adapter_timeout_seconds} seconds.",
                }
            )
        else:
            evaluation.update(
                {
                    "adapter_command_returncode": completed.returncode,
                    "stdout": completed.stdout,
                    "stderr": completed.stderr,
                }
            )
            if report_path.exists():
                try:
                    evaluation["report"] = json.loads(
                        report_path.read_text(encoding="utf-8")
                    )
                except json.JSONDecodeError as exc:
                    evaluation["stderr"] += f"\nCould not parse adapter JSON: {exc}"

        updated_records.append(
            classify_candidate_path(
                candidate,
                Path(str(record["initial_path"])),
                None,
                evaluation,
            )
        )
    return updated_records


def write_best_changed_candidate_report(candidate_records: list[dict[str, Any]]) -> Path | None:
    """Copy the best valid changed EVOLVE-block-only report to a stable path."""

    valid_records = [
        record
        for record in candidate_records
        if record["generated_changed_candidate"]
        and record["changes_only_evolve_block"]
        and record.get("adapter_evaluation")
        and record["adapter_evaluation"].get("report")
        and record["adapter_evaluation"]["report"].get("valid")
    ]
    if not valid_records:
        return None
    best = max(
        valid_records,
        key=lambda record: (
            float(record["adapter_evaluation"]["report"]["combined_score"]),
            str(record["candidate_path"]),
        ),
    )
    source = Path(str(best["adapter_evaluation"]["adapter_report_path"]))
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


def _read_local_config_values(config_path: Path) -> dict[str, str]:
    """Read the simple scalar fields this runner needs from its YAML config."""

    values: dict[str, str] = {}
    for line in config_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        if key in {"api_base", "primary_model"}:
            values[key] = value.strip().strip("\"'")
    return values


def _parse_ollama_list_models(stdout: str) -> list[str]:
    models: list[str] = []
    for index, line in enumerate(stdout.splitlines()):
        if index == 0 and line.lower().startswith("name"):
            continue
        parts = line.split()
        if parts:
            models.append(parts[0])
    return models


def _extract_model_ids(payload: object) -> list[str]:
    if not isinstance(payload, dict):
        return []
    data = payload.get("data")
    if not isinstance(data, list):
        return []
    model_ids = []
    for item in data:
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            model_ids.append(item["id"])
    return model_ids


def _safe_candidate_stem(value: str) -> str:
    safe = []
    for character in value:
        if character.isalnum() or character in {"-", "_"}:
            safe.append(character)
        else:
            safe.append("_")
    stem = "".join(safe).strip("._")
    return stem or "candidate"


def _looks_like_initial_snapshot(
    candidate_path: Path,
    initial_path: Path,
    run_dir: Path | None,
) -> bool:
    try:
        if candidate_path.resolve() == initial_path.resolve():
            return True
    except OSError:
        pass
    lowered_parts = [part.lower() for part in candidate_path.parts]
    if candidate_path.name.lower() == initial_path.name.lower():
        return True
    if any("initial" in part or "seed" in part or "baseline" in part for part in lowered_parts):
        return True
    if run_dir is not None:
        try:
            relative = candidate_path.resolve().relative_to(run_dir.resolve())
        except ValueError:
            return False
        return len(relative.parts) == 1 and relative.name.lower() == initial_path.name.lower()
    return False


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


def _evaluation_final_class(record: dict[str, Any], evaluation: dict[str, Any]) -> str:
    report = evaluation.get("report")
    if evaluation.get("adapter_command_returncode") != 0 or not isinstance(report, dict):
        return "adapter_evaluation_failed"
    if report.get("timeout"):
        return "timeout_candidate"
    if report.get("nondeterminism"):
        return "nondeterministic_candidate"
    if report.get("invalid_policy"):
        return "invalid_candidate"
    return str(record["structural_class"])


def _post_run_blockers(
    returncode: int,
    generated_changed: list[dict[str, Any]],
    changed_outside_evolve: list[dict[str, Any]],
    failed_adapter: list[dict[str, Any]],
) -> list[str]:
    blockers: list[str] = []
    if returncode != 0:
        blockers.append(f"OpenEvolve returned nonzero status {returncode}")
    if returncode == 0 and not generated_changed:
        blockers.append(
            "OpenEvolve completed but no candidate whose normalized text differs from the initial program was found"
        )
    if changed_outside_evolve:
        blockers.append(
            f"{len(changed_outside_evolve)} generated changed candidate(s) modified text outside the EVOLVE block"
        )
    if failed_adapter:
        blockers.append(
            f"{len(failed_adapter)} generated changed candidate(s) could not be independently re-evaluated"
        )
    return blockers


def _status_payload(
    *,
    status: str,
    config_path: Path,
    run_dir: Path,
    api_base: str,
    model: str,
    openevolve_available: bool | None = None,
    command: list[str] | None = None,
    returncode: int | None = None,
    stdout_path: Path | None = None,
    stderr_path: Path | None = None,
    blockers: list[str] | None = None,
    candidate_records: list[dict[str, Any]] | None = None,
    extracted_candidate_paths: list[str] | None = None,
    best_candidate_report_path: str | None = None,
    ollama_probe: dict[str, Any] | None = None,
    endpoint_probe: dict[str, Any] | None = None,
    real_local_llm_run_attempted: bool = False,
    real_local_llm_mutation_obtained: bool = False,
    stubbed_transport_label: str | None = None,
) -> dict[str, Any]:
    candidate_records = candidate_records or []
    generated_changed_paths = [
        record["candidate_path"]
        for record in candidate_records
        if record["generated_changed_candidate"]
    ]
    evolve_only_paths = [
        record["candidate_path"]
        for record in candidate_records
        if record["generated_changed_candidate"] and record["changes_only_evolve_block"]
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "zero_money_local_model_test": True,
        "stubbed_transport": bool(stubbed_transport_label),
        "stub_label": stubbed_transport_label,
        "api_base": api_base,
        "model": model,
        "config_path": str(config_path),
        "artifact_dir": str(run_dir),
        "openevolve_available": openevolve_available,
        "command": command,
        "returncode": returncode,
        "stdout_path": str(stdout_path) if stdout_path else None,
        "stderr_path": str(stderr_path) if stderr_path else None,
        "blockers": blockers or [],
        "setup_instructions": _setup_instructions(
            api_base,
            model,
            stubbed_transport=bool(stubbed_transport_label),
        ),
        "ollama_probe": ollama_probe or {},
        "endpoint_probe": endpoint_probe or {},
        "real_local_llm_run_attempted": real_local_llm_run_attempted,
        "real_local_llm_mutation_obtained": real_local_llm_mutation_obtained,
        "candidate_records": candidate_records,
        "extracted_candidate_paths": extracted_candidate_paths or [],
        "generated_changed_candidate_paths": generated_changed_paths,
        "evolve_block_only_changed_candidate_paths": evolve_only_paths,
        "best_candidate_report_path": best_candidate_report_path,
    }


def _setup_instructions(
    api_base: str,
    model: str,
    *,
    stubbed_transport: bool = False,
) -> list[str]:
    if stubbed_transport:
        return [
            STUB_LABEL,
            "Treat this only as plumbing evidence for OpenEvolve HTTP transport and adapter re-evaluation.",
            "It does not satisfy the autonomous Milestone 3 local-LLM criterion.",
            "For a real zero-money LLM mutation, install/start Ollama, pull a free local model such as qwen2.5-coder:1.5b, and rerun `python scripts/run_list_update_openevolve_zero_money_milestone3.py`.",
        ]
    return [
        "Install the free Ollama desktop/CLI if it is not already installed.",
        f"Pull the configured free local model, for example `ollama pull {model}`.",
        "Start the local server with `ollama serve` if it is not already running.",
        f"Verify the local endpoint with `Invoke-WebRequest {api_base.rstrip('/')}/models`.",
        "Install OpenEvolve into the Python environment if needed with `python -m pip install openevolve`.",
        "Rerun `python scripts/run_list_update_openevolve_zero_money_milestone3.py` from the repository root.",
        "Do not set OPENAI_API_KEY for this zero-money Ollama path.",
    ]


def _safe_process_text(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
