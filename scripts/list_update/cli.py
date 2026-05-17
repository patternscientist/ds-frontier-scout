"""Small JSON CLI for the list-update exact evaluator."""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction

from .exact_evaluator import (
    competitive_ratio,
    fraction_to_string,
    offline_optimum,
)
from .model import FULL_COST_MODEL_NAME
from .policies import (
    DETERMINISTIC_POLICIES,
    RANDOMIZED_POLICIES,
    DeterministicEvaluation,
    RandomizedEvaluation,
    evaluate_deterministic_policy,
    evaluate_randomized_policy,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m scripts.list_update.cli")
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument(
        "--trace",
        required=True,
        help="comma-separated item labels, for example 2,1,2",
    )
    args = parser.parse_args(argv)

    try:
        trace = _parse_trace(args.trace)
        offline = offline_optimum(trace, args.n)
        payload = {
            "model": FULL_COST_MODEL_NAME,
            "n": args.n,
            "trace": trace,
            "offline_optimum": {
                "cost": str(offline.cost),
                "final_state": list(offline.final_state),
                "steps": [
                    {
                        "request": step.request,
                        "state_before": list(step.state_before),
                        "access_state": list(step.access_state),
                        "paid_exchange_cost": step.paid_exchange_cost,
                        "access_rank_0_based": step.access_rank,
                        "access_cost": step.access_cost,
                        "state_after": list(step.state_after),
                    }
                    for step in offline.steps
                ],
            },
            "deterministic_policies": {},
            "randomized_policies": {},
        }

        for name, policy in DETERMINISTIC_POLICIES.items():
            evaluation = evaluate_deterministic_policy(policy, trace, args.n)
            payload["deterministic_policies"][name] = _deterministic_payload(
                evaluation,
                offline.cost,
            )

        for name, policy in RANDOMIZED_POLICIES.items():
            evaluation = evaluate_randomized_policy(policy, trace, args.n)
            payload["randomized_policies"][name] = _randomized_payload(
                evaluation,
                offline.cost,
            )

        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


def _parse_trace(raw: str) -> list[int]:
    if not raw.strip():
        return []
    return [int(part.strip()) for part in raw.split(",")]


def _deterministic_payload(
    evaluation: DeterministicEvaluation,
    offline_cost: int,
) -> dict[str, object]:
    return {
        "cost": str(evaluation.cost),
        "ratio_to_offline": fraction_to_string(
            competitive_ratio(evaluation.cost, offline_cost)
        ),
        "final_state": list(evaluation.final_state),
        "steps": [
            {
                "request": step.request,
                "state_before": list(step.state_before),
                "access_rank_0_based": step.access_rank,
                "access_cost": step.access_cost,
                "state_after": list(step.state_after),
            }
            for step in evaluation.steps
        ],
    }


def _randomized_payload(
    evaluation: RandomizedEvaluation,
    offline_cost: int,
) -> dict[str, object]:
    return {
        "expected_cost": fraction_to_string(evaluation.expected_cost),
        "ratio_to_offline": fraction_to_string(
            Fraction(evaluation.expected_cost, offline_cost)
        ),
        "final_distribution": _distribution_payload(evaluation.final_distribution),
        "steps": [
            {
                "request": step.request,
                "expected_access_cost": fraction_to_string(step.expected_access_cost),
                "state_distribution_before": _distribution_payload(
                    step.state_distribution_before
                ),
                "state_distribution_after": _distribution_payload(
                    step.state_distribution_after
                ),
            }
            for step in evaluation.steps
        ],
    }


def _distribution_payload(distribution) -> list[dict[str, object]]:
    return [
        {"state": list(state), "probability": fraction_to_string(probability)}
        for state, probability in distribution
    ]


if __name__ == "__main__":
    raise SystemExit(main())
