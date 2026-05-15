# Frontier

Verified source:

- Ding, Garces, Li, Lin, Nelson, Shah, and Woodruff, "Space Complexity of Minimum Cut Problems in Single-Pass Streams," ITCS 2025.
- The paper gives near-optimal insertion-only results for minimum cut, including `~O(n/epsilon)`-space algorithms and matching lower bounds in relevant settings.
- The paper records that fully dynamic streaming algorithms for approximate min-cut use `~O(n/epsilon^2)` space.
- Open Question 15 asks for the exact space complexity of `(1+epsilon)` approximate min-cut in one-pass dynamic streams.

Inferred frontier:

- The most plausible proof route is not to build a full cut sparsifier, but to isolate whether min-cut can exploit the small number of near-minimum cuts even after deletions.
- The most plausible lower-bound route is a communication game or turnstile hard distribution that survives the global-min-cut promise.

TODO: verify source:

- Read the full arXiv version's alternative proof of Theorem 12 and record whether it naturally extends to deletions.
