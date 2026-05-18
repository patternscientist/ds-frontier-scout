"""Valid static/no-move candidate used by adapter tests."""

from __future__ import annotations


def choose_update(state, request, history):
    return state.index(request)
