"""Invalid candidate that violates the policy return-type contract."""

from __future__ import annotations


def choose_update(state, request, history):
    return "front"
