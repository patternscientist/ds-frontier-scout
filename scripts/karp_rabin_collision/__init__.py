"""Exact finite Karp-Rabin collision-detection helpers."""

from .fixed_length import CollisionWitness, find_fixed_length_collision
from .oracle import OracleResult, all_length_oracle, find_collision

__all__ = [
    "CollisionWitness",
    "OracleResult",
    "all_length_oracle",
    "find_collision",
    "find_fixed_length_collision",
]
