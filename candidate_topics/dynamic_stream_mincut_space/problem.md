# Problem

Determine the exact space complexity of computing a `(1+epsilon)` approximation to global minimum cut in a one-pass dynamic stream of edge insertions and deletions for simple weighted graphs.

The promoted residual is not general graph sparsification. It asks whether approximate min-cut itself can be sketched in `~O(n/epsilon)` space in the turnstile model, or whether deletions force the `~O(n/epsilon^2)` space scale of dynamic-stream sparsifiers.

Open status: explicit in Ding, Garces, Li, Lin, Nelson, Shah, and Woodruff (ITCS 2025), Open Question 15.
