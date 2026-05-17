"""Policy interface and per-trace execution for list-update candidates.

Candidate modules expose exactly one function:

    choose_update(state, request, history) -> target_index

``state`` is the current list permutation before the access, ``request`` is the
requested item, and ``history`` is the tuple of previous requests in the same
trace. The return value is the 0-based position to which the requested item is
moved after access. It must be an integer in ``0..rank`` where ``rank`` is the
requested item's 0-based rank before access.
"""

from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from scripts.list_update.model import (
    ListState,
    RequestTrace,
    access_cost,
    access_rank,
    initial_state_for_n,
    move_accessed_to_position,
    validate_n,
    validate_state,
    validate_trace,
)

ChooseUpdate = Callable[[ListState, int, RequestTrace], int]


class InvalidPolicyError(ValueError):
    """Raised when a candidate policy violates the evaluator interface."""


@dataclass(frozen=True)
class PolicySpec:
    name: str
    choose_update: ChooseUpdate
    source_path: str | None = None
    kind: str = "builtin"


@dataclass(frozen=True)
class PolicyStep:
    request: int
    state_before: ListState
    access_rank_0_based: int
    access_cost: int
    target_index_0_based: int
    position_shift: int
    state_after: ListState


@dataclass(frozen=True)
class TraceEvaluation:
    policy_name: str
    n: int
    trace: RequestTrace
    initial_state: ListState
    total_cost: int
    final_state: ListState
    total_position_shift: int
    steps: tuple[PolicyStep, ...]

    @property
    def request_count(self) -> int:
        return len(self.trace)


def load_external_policy(path: str | Path, name: str | None = None) -> PolicySpec:
    """Load a candidate module with a ``choose_update`` function."""

    resolved = Path(path).resolve()
    if not resolved.exists():
        raise InvalidPolicyError(f"policy file does not exist: {resolved}")
    if not resolved.is_file():
        raise InvalidPolicyError(f"policy path is not a file: {resolved}")

    module_name = f"_list_update_candidate_{resolved.stem}"
    spec = importlib.util.spec_from_file_location(module_name, resolved)
    if spec is None or spec.loader is None:
        raise InvalidPolicyError(f"could not import policy file: {resolved}")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:  # pragma: no cover - message depends on candidate.
        raise InvalidPolicyError(f"policy import failed: {exc}") from exc

    choose_update = getattr(module, "choose_update", None)
    if not callable(choose_update):
        raise InvalidPolicyError("policy module must define callable choose_update")

    return PolicySpec(
        name=name or resolved.stem,
        choose_update=choose_update,
        source_path=str(resolved),
        kind="external",
    )


def evaluate_policy_on_trace(
    policy: PolicySpec,
    trace: list[int] | tuple[int, ...],
    n: int,
    initial_state: ListState | None = None,
) -> TraceEvaluation:
    """Evaluate a deterministic policy on one trace under the standard model."""

    validate_n(n)
    trace_tuple = validate_trace(trace, n)
    if initial_state is None:
        state = initial_state_for_n(n)
    else:
        state = validate_state(initial_state, n, field="initial_state")
    start_state = state

    history: list[int] = []
    steps: list[PolicyStep] = []
    total_cost = 0
    total_position_shift = 0

    for request in trace_tuple:
        rank = access_rank(state, request)
        cost = access_cost(state, request)
        target_index = _checked_target_index(policy, state, request, tuple(history), rank)
        state_after = move_accessed_to_position(state, request, target_index)
        position_shift = rank - target_index

        steps.append(
            PolicyStep(
                request=request,
                state_before=state,
                access_rank_0_based=rank,
                access_cost=cost,
                target_index_0_based=target_index,
                position_shift=position_shift,
                state_after=state_after,
            )
        )
        total_cost += cost
        total_position_shift += position_shift
        history.append(request)
        state = state_after

    return TraceEvaluation(
        policy_name=policy.name,
        n=n,
        trace=trace_tuple,
        initial_state=start_state,
        total_cost=total_cost,
        final_state=state,
        total_position_shift=total_position_shift,
        steps=tuple(steps),
    )


def trace_evaluation_record(case_id: str, family: str, evaluation: TraceEvaluation) -> dict[str, object]:
    return {
        "case_id": case_id,
        "family": family,
        "n": evaluation.n,
        "trace": list(evaluation.trace),
        "request_count": evaluation.request_count,
        "total_cost": evaluation.total_cost,
        "final_state": list(evaluation.final_state),
        "total_position_shift": evaluation.total_position_shift,
        "steps": [
            {
                "request": step.request,
                "state_before": list(step.state_before),
                "access_rank_0_based": step.access_rank_0_based,
                "access_cost": step.access_cost,
                "target_index_0_based": step.target_index_0_based,
                "position_shift": step.position_shift,
                "state_after": list(step.state_after),
            }
            for step in evaluation.steps
        ],
    }


def _checked_target_index(
    policy: PolicySpec,
    state: ListState,
    request: int,
    history: RequestTrace,
    rank: int,
) -> int:
    try:
        raw_target = policy.choose_update(tuple(state), request, tuple(history))
    except Exception as exc:
        raise InvalidPolicyError(
            f"{policy.name}: choose_update raised {type(exc).__name__}: {exc}"
        ) from exc

    if isinstance(raw_target, bool) or not isinstance(raw_target, int):
        raise InvalidPolicyError(
            f"{policy.name}: choose_update must return an integer target index"
        )
    if raw_target < 0 or raw_target > rank:
        raise InvalidPolicyError(
            f"{policy.name}: target index {raw_target} is outside allowed range 0..{rank}"
        )
    return raw_target
