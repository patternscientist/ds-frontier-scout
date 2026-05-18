"""Suite-level JSON evaluator for deterministic list-update policies."""

from __future__ import annotations

import argparse
import ast
import inspect
import json
import multiprocessing as mp
import sys
from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations
from pathlib import Path
from queue import Empty
from typing import Iterable

from scripts.list_update.exact_evaluator import offline_optimum
from scripts.list_update.model import FULL_COST_MODEL_NAME

from .baselines import get_baseline_policies
from .policy_api import (
    InvalidPolicyError,
    PolicySpec,
    evaluate_policy_on_trace,
    load_external_policy,
    trace_evaluation_record,
)
from .workloads import TraceCase, build_suite, suite_names

BASELINE_RATIO_NAMES = ("move_to_front", "transpose", "frequency_count")
SCHEMA_VERSION = "list_update_eval.milestone1.v0"


@dataclass(frozen=True)
class PolicyRun:
    name: str
    records: tuple[dict[str, object], ...]
    invalid_policy: bool = False
    timeout: bool = False
    error: str | None = None
    complexity: dict[str, int | str | None] | None = None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m list_update_eval.evaluate")
    parser.add_argument("--suite", choices=suite_names(), default="smoke")
    parser.add_argument("--policy", help="path to a candidate policy module")
    parser.add_argument("--policy-name", help="display name for --policy")
    parser.add_argument("--all-baselines", action="store_true")
    parser.add_argument("--out", required=True, help="JSON report path")
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=2.0,
        help="wall-clock bound for external policy evaluation",
    )
    args = parser.parse_args(argv)

    try:
        if not args.all_baselines and not args.policy:
            raise ValueError("provide --all-baselines or --policy")
        report = build_report(
            suite_name=args.suite,
            all_baselines=args.all_baselines,
            policy_path=args.policy,
            policy_name=args.policy_name,
            timeout_seconds=args.timeout_seconds,
        )
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(_compact_summary(report, out_path))
        return _exit_status(report)
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


def build_report(
    suite_name: str,
    all_baselines: bool = False,
    policy_path: str | None = None,
    policy_name: str | None = None,
    timeout_seconds: float = 2.0,
) -> dict[str, object]:
    cases = build_suite(suite_name)
    oracle_records = _oracle_records(cases)
    static_optimal_records = _static_optimal_records(cases)

    baseline_runs = {
        name: _run_builtin_policy(policy, cases)
        for name, policy in get_baseline_policies().items()
    }
    baseline_totals = {
        name: _total_cost(run.records) for name, run in baseline_runs.items()
    }
    baseline_totals["static_optimal"] = sum(
        record["cost"] for record in static_optimal_records.values()
    )

    selected_runs: list[PolicyRun] = []
    if all_baselines:
        selected_runs.extend(baseline_runs.values())
    if policy_path:
        selected_runs.append(
            _run_external_policy(
                policy_path,
                policy_name,
                cases,
                timeout_seconds=timeout_seconds,
            )
        )

    policy_payloads = {
        run.name: _policy_metrics(
            run,
            cases,
            baseline_totals,
            oracle_records,
            static_optimal_records,
        )
        for run in selected_runs
    }

    return {
        "schema_version": SCHEMA_VERSION,
        "cost_model": _cost_model_payload(),
        "suite": {
            "name": suite_name,
            "trace_count": len(cases),
            "request_count": sum(len(case.trace) for case in cases),
            "families": sorted({case.family for case in cases}),
            "cases": [case.to_json() for case in cases],
        },
        "oracle": {
            "available": True,
            "kind": "exact_offline_optimum_per_trace",
            "source": "scripts.list_update.exact_evaluator.offline_optimum",
            "adversarial_trace_source": "scripts.list_update.adversarial_traces.worst_traces_by_policy",
            "finite_minimax_value_available": False,
            "finite_minimax_todo": (
                "No public interface was found for a true minimax value over online "
                "policy strategy spaces; this harness integrates the exact offline "
                "trace oracle and finite adversarial trace enumerator."
            ),
        },
        "baseline_totals": baseline_totals,
        "static_optimal_comparator": {
            case_id: record for case_id, record in static_optimal_records.items()
        },
        "offline_oracle_by_case": {
            case_id: record for case_id, record in oracle_records.items()
        },
        "policies": policy_payloads,
    }


def _run_builtin_policy(policy: PolicySpec, cases: Iterable[TraceCase]) -> PolicyRun:
    records = tuple(_evaluate_policy_records(policy, cases))
    return PolicyRun(
        name=policy.name,
        records=records,
        complexity=_policy_complexity(policy),
    )


def _run_external_policy(
    policy_path: str,
    policy_name: str | None,
    cases: tuple[TraceCase, ...],
    timeout_seconds: float,
) -> PolicyRun:
    if timeout_seconds <= 0:
        raise ValueError("--timeout-seconds must be positive")

    first = _isolated_external_once(policy_path, policy_name, cases, timeout_seconds)
    if first.invalid_policy or first.timeout:
        return first

    second = _isolated_external_once(policy_path, policy_name, cases, timeout_seconds)
    if second.invalid_policy or second.timeout:
        return second
    if first.records != second.records:
        return PolicyRun(
            name=first.name,
            records=(),
            invalid_policy=True,
            error="policy is nondeterministic: two isolated runs produced different records",
            complexity=first.complexity,
        )
    return first


def _isolated_external_once(
    policy_path: str,
    policy_name: str | None,
    cases: tuple[TraceCase, ...],
    timeout_seconds: float,
) -> PolicyRun:
    ctx = mp.get_context("spawn")
    queue = ctx.Queue()
    case_payloads = [case.to_json() for case in cases]
    process = ctx.Process(
        target=_external_worker,
        args=(policy_path, policy_name, case_payloads, queue),
    )
    process.start()
    process.join(timeout_seconds)
    resolved = str(Path(policy_path).resolve())
    name = policy_name or Path(policy_path).stem
    complexity = _source_complexity(resolved)
    if process.is_alive():
        process.terminate()
        process.join()
        return PolicyRun(
            name=name,
            records=(),
            invalid_policy=True,
            timeout=True,
            error=f"policy exceeded timeout_seconds={timeout_seconds}",
            complexity=complexity,
        )
    try:
        payload = queue.get_nowait()
    except Empty:
        return PolicyRun(
            name=name,
            records=(),
            invalid_policy=True,
            error=f"policy worker exited without a result; exitcode={process.exitcode}",
            complexity=complexity,
        )
    if not payload["ok"]:
        return PolicyRun(
            name=payload["name"],
            records=(),
            invalid_policy=True,
            error=payload["error"],
            complexity=complexity,
        )
    return PolicyRun(
        name=payload["name"],
        records=tuple(payload["records"]),
        complexity=complexity,
    )


def _external_worker(
    policy_path: str,
    policy_name: str | None,
    case_payloads: list[dict[str, object]],
    queue,
) -> None:
    name = policy_name or Path(policy_path).stem
    try:
        policy = load_external_policy(policy_path, name=name)
        cases = tuple(
            TraceCase(
                id=str(payload["id"]),
                family=str(payload["family"]),
                n=int(payload["n"]),
                trace=tuple(int(item) for item in payload["trace"]),
                source=str(payload["source"]),
            )
            for payload in case_payloads
        )
        queue.put(
            {
                "ok": True,
                "name": policy.name,
                "records": list(_evaluate_policy_records(policy, cases)),
            }
        )
    except Exception as exc:
        queue.put(
            {
                "ok": False,
                "name": name,
                "error": f"{type(exc).__name__}: {exc}",
            }
        )


def _evaluate_policy_records(
    policy: PolicySpec,
    cases: Iterable[TraceCase],
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for case in cases:
        evaluation = evaluate_policy_on_trace(policy, case.trace, case.n)
        records.append(trace_evaluation_record(case.id, case.family, evaluation))
    return records


def _policy_metrics(
    run: PolicyRun,
    cases: tuple[TraceCase, ...],
    baseline_totals: dict[str, int],
    oracle_records: dict[str, dict[str, object]],
    static_optimal_records: dict[str, dict[str, object]],
) -> dict[str, object]:
    if run.invalid_policy or run.timeout:
        return {
            "invalid_policy": run.invalid_policy,
            "timeout": run.timeout,
            "error": run.error,
            "policy_complexity": run.complexity or {},
            "total_cost": None,
            "mean_cost": None,
            "worst_trace_cost": None,
            "baseline_ratios": {},
            "oracle": {},
            "movement_aggressiveness": {},
            "locality_sensitivity_proxy": None,
        }

    total_cost = _total_cost(run.records)
    request_count = sum(int(record["request_count"]) for record in run.records)
    trace_count = len(run.records)
    worst = max(
        run.records,
        key=lambda record: (int(record["total_cost"]), record["case_id"]),
    )
    baseline_ratios = {
        name: _ratio_payload(total_cost, baseline_totals[name])
        for name in BASELINE_RATIO_NAMES
    }
    baseline_ratios["static_safe"] = _ratio_payload(total_cost, baseline_totals["static_safe"])
    baseline_ratios["static_optimal"] = _ratio_payload(
        total_cost,
        baseline_totals["static_optimal"],
    )

    oracle_total = sum(int(record["cost"]) for record in oracle_records.values())
    regrets = {
        record["case_id"]: int(record["total_cost"])
        - int(oracle_records[str(record["case_id"])]["cost"])
        for record in run.records
    }
    worst_regret_case = max(regrets, key=lambda case_id: (regrets[case_id], case_id))
    worst_ratio_record = max(
        run.records,
        key=lambda record: (
            Fraction(
                int(record["total_cost"]),
                int(oracle_records[str(record["case_id"])]["cost"]),
            ),
            str(record["case_id"]),
        ),
    )

    total_shift = sum(int(record["total_position_shift"]) for record in run.records)
    return {
        "invalid_policy": False,
        "timeout": False,
        "trace_count": trace_count,
        "request_count": request_count,
        "total_cost": total_cost,
        "mean_cost": total_cost / request_count if request_count else None,
        "mean_trace_cost": total_cost / trace_count if trace_count else None,
        "worst_trace_cost": {
            "case_id": worst["case_id"],
            "family": worst["family"],
            "n": worst["n"],
            "trace": worst["trace"],
            "cost": worst["total_cost"],
        },
        "baseline_ratios": baseline_ratios,
        "oracle": {
            "available": True,
            "total_offline_cost": oracle_total,
            "total_regret": total_cost - oracle_total,
            "competitive_ratio": _ratio_payload(total_cost, oracle_total),
            "worst_trace_regret": {
                "case_id": worst_regret_case,
                "regret": regrets[worst_regret_case],
            },
            "worst_trace_competitive_ratio": {
                "case_id": worst_ratio_record["case_id"],
                "ratio": _ratio_payload(
                    int(worst_ratio_record["total_cost"]),
                    int(oracle_records[str(worst_ratio_record["case_id"])]["cost"]),
                ),
            },
        },
        "static_optimal_gap": {
            "total_static_optimal_cost": sum(
                int(record["cost"]) for record in static_optimal_records.values()
            ),
            "regret": total_cost
            - sum(int(record["cost"]) for record in static_optimal_records.values()),
        },
        "movement_aggressiveness": {
            "total_position_shift": total_shift,
            "average_position_shift_per_request": total_shift / request_count
            if request_count
            else None,
        },
        "locality_sensitivity_proxy": _locality_sensitivity(run.records),
        "policy_complexity": run.complexity or {},
        "trace_records": list(run.records),
    }


def _oracle_records(cases: tuple[TraceCase, ...]) -> dict[str, dict[str, object]]:
    records: dict[str, dict[str, object]] = {}
    for case in cases:
        result = offline_optimum(case.trace, case.n)
        records[case.id] = {
            "case_id": case.id,
            "n": case.n,
            "trace": list(case.trace),
            "cost": result.cost,
            "final_state": list(result.final_state),
        }
    return records


def _static_optimal_records(cases: tuple[TraceCase, ...]) -> dict[str, dict[str, object]]:
    return {case.id: _static_optimal_record(case) for case in cases}


def _static_optimal_record(case: TraceCase) -> dict[str, object]:
    best_state = None
    best_cost = None
    for state in permutations(range(case.n)):
        cost = sum(state.index(request) + 1 for request in case.trace)
        if best_cost is None or (cost, state) < (best_cost, best_state):
            best_cost = cost
            best_state = state
    if best_state is None or best_cost is None:
        raise ValueError(f"could not compute static optimum for {case.id}")
    return {
        "case_id": case.id,
        "n": case.n,
        "trace": list(case.trace),
        "cost": best_cost,
        "permutation": list(best_state),
        "note": "trace-aware fixed-order comparator, not an online policy",
    }


def _total_cost(records: Iterable[dict[str, object]]) -> int:
    return sum(int(record["total_cost"]) for record in records)


def _ratio_payload(numerator: int, denominator: int) -> dict[str, object]:
    if denominator <= 0:
        return {"exact": None, "value": None}
    ratio = Fraction(numerator, denominator)
    exact = str(ratio.numerator) if ratio.denominator == 1 else f"{ratio.numerator}/{ratio.denominator}"
    return {"exact": exact, "value": float(ratio)}


def _locality_sensitivity(records: tuple[dict[str, object], ...]) -> dict[str, object] | None:
    family_means: dict[str, float] = {}
    for family in ("locality_biased", "random_fixed_seed"):
        family_records = [record for record in records if record["family"] == family]
        if not family_records:
            return None
        total_cost = sum(int(record["total_cost"]) for record in family_records)
        total_requests = sum(int(record["request_count"]) for record in family_records)
        family_means[family] = total_cost / total_requests
    return {
        "locality_mean_cost": family_means["locality_biased"],
        "random_mean_cost": family_means["random_fixed_seed"],
        "locality_to_random_ratio": family_means["locality_biased"]
        / family_means["random_fixed_seed"],
    }


def _policy_complexity(policy: PolicySpec) -> dict[str, int | str | None]:
    try:
        source = inspect.getsource(policy.choose_update)
    except OSError:
        return {"source": policy.kind, "source_length": None, "ast_node_count": None}
    return _complexity_from_source(source, policy.kind)


def _source_complexity(path: str) -> dict[str, int | str | None]:
    try:
        source = Path(path).read_text(encoding="utf-8")
    except OSError:
        return {"source": path, "source_length": None, "ast_node_count": None}
    return _complexity_from_source(source, path)


def _complexity_from_source(source: str, source_label: str) -> dict[str, int | str | None]:
    try:
        node_count = sum(1 for _node in ast.walk(ast.parse(source)))
    except SyntaxError:
        node_count = None
    return {
        "source": source_label,
        "source_length": len(source),
        "ast_node_count": node_count,
    }


def _cost_model_payload() -> dict[str, object]:
    return {
        "name": FULL_COST_MODEL_NAME,
        "access_cost_convention": "item at 0-based rank r costs r + 1",
        "internal_positions": "0-indexed",
        "free_exchanges": (
            "after an access, the requested item may move for free to any "
            "earlier 0-based position, including staying in place"
        ),
        "candidate_paid_exchanges": "not allowed",
        "offline_oracle_paid_exchanges": (
            "unit-cost adjacent exchanges, canonicalized before access by the existing DP"
        ),
    }


def _compact_summary(report: dict[str, object], out_path: Path) -> str:
    suite = report["suite"]
    oracle = report["oracle"]
    lines = [
        f"suite={suite['name']} traces={suite['trace_count']} requests={suite['request_count']}",
        f"oracle_available={str(oracle['available']).lower()} finite_minimax_value_available={str(oracle['finite_minimax_value_available']).lower()}",
        "policy total_cost mean_cost ratio_vs_mtf ratio_vs_offline invalid timeout",
    ]
    for name, metrics in report["policies"].items():
        if metrics["invalid_policy"] or metrics["timeout"]:
            lines.append(
                f"{name} NA NA NA NA {str(metrics['invalid_policy']).lower()} {str(metrics['timeout']).lower()}"
            )
            continue
        lines.append(
            f"{name} {metrics['total_cost']} {metrics['mean_cost']:.6g} "
            f"{metrics['baseline_ratios']['move_to_front']['exact']} "
            f"{metrics['oracle']['competitive_ratio']['exact']} false false"
        )
    lines.append(f"wrote {out_path}")
    return "\n".join(lines)


def _exit_status(report: dict[str, object]) -> int:
    for metrics in report["policies"].values():
        if metrics["invalid_policy"] or metrics["timeout"]:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
