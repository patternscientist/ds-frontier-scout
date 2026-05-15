# Problem

Scouting target: isolate a narrow, source-grounded version of the splay traversal problem on preorder / 231-avoiding access sequences.

Given two binary search trees on the same key set, let `preorder(T)` be the permutation obtained by visiting the root, then the left subtree, then the right subtree. The classical traversal conjecture asks whether splaying an arbitrary initial tree `T0` according to `preorder(T1)` always costs `O(n)`.

For this repository, the candidate should not be "solve dynamic optimality." The sharper target is:

- prove a new restricted traversal theorem for Splay on preorder sequences, 231-avoiding permutations, or a closely related fixed-pattern-avoiding class;
- or find a small structural lemma/counterexample barrier explaining why current Greedy / forbidden-submatrix methods do not transfer to Splay;
- or build exact small-instance evidence comparing Splay, Greedy, and offline optimum on 231-avoiding and other fixed-pattern-avoiding permutations.

Open status: uncertain. Checked sources explicitly leave the arbitrary-initial-tree traversal conjecture unresolved in 2015/2019-era statements, and 2024/2025 work resolves nearby offline-optimal or Greedy-in-special-initial-tree questions rather than the full Splay statement. A final promotion needs a fresh post-2025 verification pass.
