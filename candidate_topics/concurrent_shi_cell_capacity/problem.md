# Problem

Characterize the exact shared-cell width and progress-condition frontier for linearizable concurrent dictionaries that are state-quiescent strongly history independent.

The focused residual is whether lock-free SQHI hash tables can use one key plus `O(1)` metadata per cell, or whether two-key lookahead cells are genuinely necessary.

Open status: inferred from the gap between the STOC 2025 construction and lower bounds.
