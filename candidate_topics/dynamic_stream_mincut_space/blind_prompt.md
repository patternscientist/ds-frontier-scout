# Blind Prompt

In a one-pass turnstile stream, edges of a simple weighted `n`-vertex graph are inserted and deleted. At the end, output a `(1+epsilon)` approximation to the global minimum cut.

Can this be done in `~O(n/epsilon)` space, matching insertion-only min-cut, or do deletions require `~Omega(n/epsilon^2)` space as in dynamic-stream cut sparsification?

Try either:

- a sketch using only information relevant to near-minimum cuts; or
- a communication-complexity lower bound on explicit graph families.
