"""Timeout candidate used to verify bounded adapter failure handling."""

from __future__ import annotations

import time


def choose_update(state, request, history):
    time.sleep(5.0)
    return state.index(request)
