"""Initial conservative policy for future list-update OpenEvolve runs."""

from __future__ import annotations


def choose_update(state, request, history):
    """Move the requested item to the front after every access."""

    # EVOLVE-BLOCK-START
    target_index = 0
    # EVOLVE-BLOCK-END
    return target_index
