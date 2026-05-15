# Why It Matters

This is a compact, under-attended optimization problem sitting close to classic BST theory.

For paths, optimal static BSTs have dynamic-programming algorithms. For general tree topologies, STTs preserve the same recursive search idea but lose the simple interval structure. The result is a clean gap: good approximations exist, but exact polynomial-time optimality is still open.

The LP angle makes the candidate unusually scoutable:

- a natural conjectured extended formulation has just been disproved;
- the known gaps are small but explicit;
- stars are solved, while paths/almost-stars remain tempting;
- the 2025 paper gives concrete small topologies and reproducibility hooks.

If solved, even for a subclass, the result would clarify whether STTs are closer to optimal BST dynamic programming or to harder graph-search / elimination-tree polytopes.
