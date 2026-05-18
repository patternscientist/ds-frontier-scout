# List-Update Evaluator Policy Interface

Candidate policies are deterministic Python modules with one callable:

```python
def choose_update(state, request, history):
    ...
```

- `state` is an immutable tuple containing the current list order before access.
- `request` is the requested item label.
- `history` is an immutable tuple of previous requests in the same trace, not including the current request.
- The return value is an integer 0-based target index for the requested item after access.
- If the requested item is at 0-based rank `r`, the target must be in `0..r`.
- Returning anything else marks the policy invalid.

The evaluator copies immutable tuples into candidate calls. External candidates
are run in an isolated worker process with a wall-clock timeout and are evaluated
twice to reject obvious nondeterminism. Candidate policies are not allowed paid
exchanges or free movement of non-requested items.

Cost model:

- internal positions are 0-indexed;
- accessing rank `r` costs `r + 1`;
- after the access, the requested item may move to any earlier position for free,
  including staying in place;
- candidate policies cannot perform paid exchanges;
- the offline oracle comparator uses the existing exact DP from
  `scripts.list_update.exact_evaluator.offline_optimum`, where unit-cost adjacent
  paid exchanges are canonicalized before access.
