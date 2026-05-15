# Why It Matters

The broad dynamic optimality problem is famous and saturated. This candidate matters only if we keep it narrow.

Preorder sequences are one of the cleanest "easy" access classes where offline optimum is linear. They are also exactly the 231-avoiding permutations, so the problem sits at a useful crossing point between BST geometry, permutation pattern avoidance, and forbidden-matrix extremal combinatorics.

A proof that Splay is linear on a new preorder / 231-avoiding subcase would be valuable because:

- it would test whether Splay can match the newer constant-OPT results for fixed-pattern-avoiding inputs;
- it would create a bridge between rotation-based amortized analysis and the forbidden-submatrix methods that currently work better for Greedy;
- it might produce reusable lemmas for traversal, deque, split, or subsequence-property routes.

The practical significance is secondary. The real value is as a small, exacting probe of why self-adjusting BST analysis is still hard after decades.
