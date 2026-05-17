"""Exhaustive trace enumeration for tiny deterministic list-update policies."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import Iterable

from .exact_evaluator import competitive_ratio, fraction_to_string, offline_optimum
from .model import FULL_COST_MODEL_NAME, ListState, RequestTrace, validate_n
from .policies import (
    DETERMINISTIC_POLICIES,
    DeterministicPolicy,
    evaluate_deterministic_policy,
)


MAX_ADVERSARIAL_N = 4
DEFAULT_N = 4
DEFAULT_MAX_LENGTH = 5
DEFAULT_TOP_K = 10


@dataclass(frozen=True)
class TraceScore:
    policy_name: str
    trace: RequestTrace
    policy_cost: int
    offline_cost: int
    ratio_to_offline: Fraction
    final_state: ListState
    offline_final_state: ListState


def enumerate_request_traces(n: int, max_length: int) -> tuple[RequestTrace, ...]:
    """Enumerate all nonempty request traces of length at most ``max_length``."""

    _validate_adversarial_n(n)
    if max_length < 1:
        raise ValueError("max_length must be at least 1")
    return tuple(
        trace
        for length in range(1, max_length + 1)
        for trace in product(range(n), repeat=length)
    )


def worst_traces_by_policy(
    n: int = DEFAULT_N,
    max_length: int = DEFAULT_MAX_LENGTH,
    top_k: int = DEFAULT_TOP_K,
    policy_names: Iterable[str] | None = None,
) -> dict[str, tuple[TraceScore, ...]]:
    """Return the top finite trace witnesses for each deterministic policy."""

    if top_k < 0:
        raise ValueError("top_k must be nonnegative")

    traces = enumerate_request_traces(n, max_length)
    policies = _select_policies(policy_names)
    scores: dict[str, list[TraceScore]] = {name: [] for name in policies}

    for trace in traces:
        offline = offline_optimum(trace, n)
        for name, policy in policies.items():
            evaluation = evaluate_deterministic_policy(policy, trace, n)
            scores[name].append(
                TraceScore(
                    policy_name=name,
                    trace=trace,
                    policy_cost=evaluation.cost,
                    offline_cost=offline.cost,
                    ratio_to_offline=competitive_ratio(evaluation.cost, offline.cost),
                    final_state=evaluation.final_state,
                    offline_final_state=offline.final_state,
                )
            )

    return {
        name: tuple(sorted(policy_scores, key=_worst_first_key)[:top_k])
        for name, policy_scores in scores.items()
    }


def build_adversarial_payload(
    n: int = DEFAULT_N,
    max_length: int = DEFAULT_MAX_LENGTH,
    top_k: int = DEFAULT_TOP_K,
    policy_names: Iterable[str] | None = None,
) -> dict[str, object]:
    traces = enumerate_request_traces(n, max_length)
    worst = worst_traces_by_policy(
        n=n,
        max_length=max_length,
        top_k=top_k,
        policy_names=policy_names,
    )
    return {
        "model": FULL_COST_MODEL_NAME,
        "n": n,
        "max_length": max_length,
        "trace_count": len(traces),
        "top_k": top_k,
        "policies": {
            name: [_score_payload(score) for score in scores]
            for name, scores in worst.items()
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m scripts.list_update.adversarial_traces"
    )
    parser.add_argument("--n", type=int, default=DEFAULT_N)
    parser.add_argument("--max-length", type=int, default=DEFAULT_MAX_LENGTH)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument(
        "--policy",
        action="append",
        dest="policies",
        choices=sorted(DETERMINISTIC_POLICIES),
        help="deterministic policy to include; repeat to select several",
    )
    args = parser.parse_args(argv)

    try:
        payload = build_adversarial_payload(
            n=args.n,
            max_length=args.max_length,
            top_k=args.top_k,
            policy_names=args.policies,
        )
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


def _validate_adversarial_n(n: int) -> None:
    validate_n(n)
    if n > MAX_ADVERSARIAL_N:
        raise ValueError(f"adversarial trace enumeration supports n <= {MAX_ADVERSARIAL_N}")


def _select_policies(
    policy_names: Iterable[str] | None,
) -> dict[str, DeterministicPolicy]:
    if policy_names is None:
        return dict(DETERMINISTIC_POLICIES)

    selected: dict[str, DeterministicPolicy] = {}
    for name in policy_names:
        try:
            selected[name] = DETERMINISTIC_POLICIES[name]
        except KeyError as exc:
            raise ValueError(f"unknown deterministic policy {name!r}") from exc
    return selected


def _worst_first_key(score: TraceScore) -> tuple[Fraction, int, RequestTrace, str]:
    return (-score.ratio_to_offline, len(score.trace), score.trace, score.policy_name)


def _score_payload(score: TraceScore) -> dict[str, object]:
    return {
        "trace": list(score.trace),
        "policy_cost": str(score.policy_cost),
        "offline_cost": str(score.offline_cost),
        "ratio_to_offline": fraction_to_string(score.ratio_to_offline),
        "final_state": list(score.final_state),
        "offline_final_state": list(score.offline_final_state),
    }


if __name__ == "__main__":
    raise SystemExit(main())
