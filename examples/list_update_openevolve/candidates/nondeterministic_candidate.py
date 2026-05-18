"""Detectably unstable candidate used by adapter tests.

The Milestone 1 evaluator runs external policies twice in isolated worker
processes. This candidate keys off the worker process sequence number so the
two runs produce different trace records without relying on wall-clock timing
or randomness.
"""

from __future__ import annotations

import multiprocessing as mp


def choose_update(state, request, history):
    rank = state.index(request)
    process_name = mp.current_process().name
    suffix = process_name.rsplit("-", 1)[-1]
    if suffix.isdigit() and int(suffix) % 2 == 0:
        return rank
    return 0
