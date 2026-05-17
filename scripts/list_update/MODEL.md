# List-Update Exact Evaluator Model

Status: scaffold model for finite exact evaluation only.

This package uses the full-cost standard list-update model.

- A list state is a permutation of item labels `0..n-1`.
- An access to an item at 0-based rank `r` costs `r + 1`.
- Free exchanges after access are allowed: immediately after the access, the requested item may be moved to any earlier position, including the front, while preserving the relative order of all other items. Keeping the item in place is also allowed.
- The offline optimum may use the standard paid exchange operation: one adjacent swap costs `1`.
- Paid exchanges are canonicalized as occurring before an access in the DP. A paid rearrangement after an access can be charged before the next access without changing total cost.
- No alternate paid-exchange variants are included here. In particular, this scaffold does not mix partial-cost accounting, non-adjacent paid swaps, discounted swaps, or variants where non-requested items move for free.

The exact evaluator is intentionally small:

- supported sizes are `n <= 5`;
- request traces are fixed finite traces;
- costs and randomized-policy expectations are exact integers or `Fraction` values;
- output is suitable for policy tables, trace audits, and exact finite ratio examples;
- no sampled-score claims or theorem claims are produced by this scaffold.
