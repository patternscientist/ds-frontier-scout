"""OpenEvolve-style evaluator entry point for list-update policies.

This file is a Milestone 2 adapter stub. It is safe to import locally and does
not start an evolutionary search.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from list_update_eval.openevolve_adapter import evaluate_candidate


def evaluate(program_path):
    """Return OpenEvolve-compatible metrics for one candidate program."""

    report = evaluate_candidate(program_path, suite="smoke")
    metrics = report["metrics"]
    artifacts = report["artifacts"]
    try:
        from openevolve.evaluation_result import EvaluationResult
    except ImportError:
        return {"metrics": metrics, "artifacts": artifacts}
    return EvaluationResult(metrics=metrics, artifacts=artifacts)
