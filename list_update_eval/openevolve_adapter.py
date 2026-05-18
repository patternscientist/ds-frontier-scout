"""OpenEvolve-facing scoring adapter for list-update candidate policies.

This module intentionally wraps the deterministic Milestone 1 evaluator. It
does not run OpenEvolve, call an LLM, or claim that any evolved policy has been
found. Its job is to turn one candidate module into a scalar fitness plus
structured diagnostics suitable for a later OpenEvolve run.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .evaluate import build_report
from .workloads import suite_names

ADAPTER_SCHEMA_VERSION = "list_update_eval.openevolve_adapter.milestone2.v0"
FITNESS_FORMULA_VERSION = "transparent_penalty_v0"
DEFAULT_TIMEOUT_SECONDS = 2.0

FITNESS_FORMULA = (
    "combined_score = 1000 - penalties, where penalties are: "
    "10000 for invalid policy behavior; 5000 for timeout; 2500 for detected "
    "nondeterminism; 1000 each when baseline/oracle metrics are unavailable; "
    "200 * max(0, ratio_vs_mtf - 1); "
    "150 * max(0, offline_oracle_ratio - 1); "
    "1 * max(0, offline_oracle_regret); "
    "max(0, source_length - 1200) / 100; "
    "max(0, ast_node_count - 200) / 20; and "
    "25 * max(0, average_position_shift_per_request - 1.25). "
    "Higher combined_score is better."
)


def evaluate_candidate(
    policy_path: str,
    suite: str = "smoke",
    out_path: str | None = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """Evaluate one candidate policy and optionally write an adapter JSON report."""

    resolved_policy = str(Path(policy_path).resolve())
    evaluator_report = build_report(
        suite_name=suite,
        policy_path=resolved_policy,
        timeout_seconds=timeout_seconds,
    )
    report_path = str(Path(out_path).resolve()) if out_path else None
    adapter_report = score_evaluator_report(
        evaluator_report=evaluator_report,
        policy_path=resolved_policy,
        report_path=report_path,
    )

    if out_path:
        destination = Path(out_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(adapter_report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    return adapter_report


def score_evaluator_report(
    evaluator_report: dict[str, Any],
    policy_name: str | None = None,
    policy_path: str | None = None,
    report_path: str | None = None,
) -> dict[str, Any]:
    """Parse a Milestone 1 evaluator report and compute adapter fitness."""

    selected_name, evaluator_metrics = _select_policy(evaluator_report, policy_name)
    suite_payload = evaluator_report.get("suite", {})
    suite_name = str(suite_payload.get("name", "unknown"))
    invalid_policy = bool(evaluator_metrics.get("invalid_policy", False))
    timeout = bool(evaluator_metrics.get("timeout", False))
    error = evaluator_metrics.get("error")
    nondeterminism = _detect_nondeterminism(error)
    valid = not invalid_policy and not timeout and not nondeterminism

    total_cost = _int_or_none(evaluator_metrics.get("total_cost"))
    ratio_vs_mtf = _nested_float(
        evaluator_metrics,
        ("baseline_ratios", "move_to_front", "value"),
    )
    offline_oracle_ratio = _nested_float(
        evaluator_metrics,
        ("oracle", "competitive_ratio", "value"),
    )
    offline_oracle_regret = _nested_int(
        evaluator_metrics,
        ("oracle", "total_regret"),
    )
    policy_complexity = _dict_or_empty(evaluator_metrics.get("policy_complexity"))
    movement_aggressiveness = _dict_or_empty(
        evaluator_metrics.get("movement_aggressiveness")
    )
    penalties = _fitness_penalties(
        invalid_policy=invalid_policy,
        timeout=timeout,
        nondeterminism=nondeterminism,
        ratio_vs_mtf=ratio_vs_mtf,
        offline_oracle_ratio=offline_oracle_ratio,
        offline_oracle_regret=offline_oracle_regret,
        policy_complexity=policy_complexity,
        movement_aggressiveness=movement_aggressiveness,
    )
    combined_score = round(1000.0 - sum(penalties.values()), 6)

    metrics = {
        "combined_score": combined_score,
        "fitness": combined_score,
        "valid": valid,
        "invalid_policy": invalid_policy,
        "timeout": timeout,
        "nondeterminism": nondeterminism,
        "total_cost": total_cost,
        "ratio_vs_mtf": ratio_vs_mtf,
        "offline_oracle_ratio": offline_oracle_ratio,
        "offline_oracle_regret": offline_oracle_regret,
        "source_length": _int_or_none(policy_complexity.get("source_length")),
        "ast_node_count": _int_or_none(policy_complexity.get("ast_node_count")),
        "average_position_shift_per_request": _float_or_none(
            movement_aggressiveness.get("average_position_shift_per_request")
        ),
        "policy_complexity": policy_complexity,
        "movement_aggressiveness": movement_aggressiveness,
        "suite": suite_name,
        "policy_name": selected_name,
        "report_path": report_path,
        "fitness_formula_version": FITNESS_FORMULA_VERSION,
        "penalties": penalties,
    }
    artifacts = {
        "policy_path": policy_path,
        "policy_name": selected_name,
        "suite": suite_name,
        "adapter_report_path": report_path,
        "fitness_formula": FITNESS_FORMULA,
        "evaluator_schema_version": evaluator_report.get("schema_version"),
        "evaluator_error": error,
        "evaluator_diagnostics": evaluator_report,
    }

    return {
        "schema_version": ADAPTER_SCHEMA_VERSION,
        "fitness_formula_version": FITNESS_FORMULA_VERSION,
        "policy_path": policy_path,
        "suite": suite_name,
        "combined_score": combined_score,
        "fitness": combined_score,
        "valid": valid,
        "invalid_policy": invalid_policy,
        "timeout": timeout,
        "nondeterminism": nondeterminism,
        "total_cost": total_cost,
        "ratio_vs_mtf": ratio_vs_mtf,
        "offline_oracle_ratio": offline_oracle_ratio,
        "offline_oracle_regret": offline_oracle_regret,
        "policy_complexity": policy_complexity,
        "movement_aggressiveness": movement_aggressiveness,
        "report_path": report_path,
        "metrics": metrics,
        "artifacts": artifacts,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m list_update_eval.openevolve_adapter"
    )
    parser.add_argument("--policy", required=True, help="candidate policy module path")
    parser.add_argument("--suite", choices=suite_names(), default="smoke")
    parser.add_argument("--out", required=True, help="adapter JSON report path")
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="wall-clock bound delegated to the Milestone 1 evaluator",
    )
    args = parser.parse_args(argv)

    try:
        report = evaluate_candidate(
            policy_path=args.policy,
            suite=args.suite,
            out_path=args.out,
            timeout_seconds=args.timeout_seconds,
        )
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print(_compact_summary(report))
    return 0


def _select_policy(
    evaluator_report: dict[str, Any],
    policy_name: str | None,
) -> tuple[str, dict[str, Any]]:
    policies = evaluator_report.get("policies")
    if not isinstance(policies, dict) or not policies:
        raise ValueError("evaluator report contains no policy metrics")
    if policy_name is not None:
        try:
            metrics = policies[policy_name]
        except KeyError as exc:
            known = ", ".join(sorted(str(name) for name in policies))
            raise ValueError(
                f"policy {policy_name!r} not found in evaluator report; known: {known}"
            ) from exc
        if not isinstance(metrics, dict):
            raise ValueError(f"policy metrics for {policy_name!r} are not a dictionary")
        return policy_name, metrics
    if len(policies) != 1:
        known = ", ".join(sorted(str(name) for name in policies))
        raise ValueError(
            "evaluator report has multiple policies; pass policy_name explicitly "
            f"to score one of: {known}"
        )
    selected_name, metrics = next(iter(policies.items()))
    if not isinstance(metrics, dict):
        raise ValueError(f"policy metrics for {selected_name!r} are not a dictionary")
    return str(selected_name), metrics


def _fitness_penalties(
    *,
    invalid_policy: bool,
    timeout: bool,
    nondeterminism: bool,
    ratio_vs_mtf: float | None,
    offline_oracle_ratio: float | None,
    offline_oracle_regret: int | None,
    policy_complexity: dict[str, Any],
    movement_aggressiveness: dict[str, Any],
) -> dict[str, float]:
    source_length = _int_or_none(policy_complexity.get("source_length"))
    ast_node_count = _int_or_none(policy_complexity.get("ast_node_count"))
    average_shift = _float_or_none(
        movement_aggressiveness.get("average_position_shift_per_request")
    )
    penalties = {
        "invalid_policy": 10000.0 if invalid_policy else 0.0,
        "timeout": 5000.0 if timeout else 0.0,
        "nondeterminism": 2500.0 if nondeterminism else 0.0,
        "missing_ratio_vs_mtf": 1000.0 if ratio_vs_mtf is None else 0.0,
        "ratio_vs_mtf": (
            0.0 if ratio_vs_mtf is None else 200.0 * max(0.0, ratio_vs_mtf - 1.0)
        ),
        "missing_offline_oracle_ratio": (
            1000.0 if offline_oracle_ratio is None else 0.0
        ),
        "offline_oracle_ratio": (
            0.0
            if offline_oracle_ratio is None
            else 150.0 * max(0.0, offline_oracle_ratio - 1.0)
        ),
        "missing_offline_oracle_regret": (
            1000.0 if offline_oracle_regret is None else 0.0
        ),
        "offline_oracle_regret": (
            0.0
            if offline_oracle_regret is None
            else float(max(0, offline_oracle_regret))
        ),
        "source_length": (
            0.0 if source_length is None else max(0.0, source_length - 1200.0) / 100.0
        ),
        "ast_node_count": (
            0.0
            if ast_node_count is None
            else max(0.0, ast_node_count - 200.0) / 20.0
        ),
        "movement_aggressiveness": (
            0.0 if average_shift is None else 25.0 * max(0.0, average_shift - 1.25)
        ),
    }
    return {name: round(value, 6) for name, value in penalties.items()}


def _detect_nondeterminism(error: object) -> bool:
    return isinstance(error, str) and "nondeterministic" in error.lower()


def _nested_float(payload: dict[str, Any], path: tuple[str, ...]) -> float | None:
    value: Any = payload
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return _float_or_none(value)


def _nested_int(payload: dict[str, Any], path: tuple[str, ...]) -> int | None:
    value: Any = payload
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return _int_or_none(value)


def _dict_or_empty(value: object) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _float_or_none(value: object) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _int_or_none(value: object) -> int | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return value
    return None


def _compact_summary(report: dict[str, Any]) -> str:
    metrics = report["metrics"]
    return (
        f"policy={metrics['policy_name']} suite={metrics['suite']} "
        f"combined_score={metrics['combined_score']} valid={str(metrics['valid']).lower()} "
        f"invalid={str(metrics['invalid_policy']).lower()} "
        f"timeout={str(metrics['timeout']).lower()} "
        f"nondeterminism={str(metrics['nondeterminism']).lower()} "
        f"total_cost={metrics['total_cost']} ratio_vs_mtf={metrics['ratio_vs_mtf']} "
        f"offline_oracle_ratio={metrics['offline_oracle_ratio']} "
        f"wrote {metrics['report_path']}"
    )


if __name__ == "__main__":
    raise SystemExit(main())
