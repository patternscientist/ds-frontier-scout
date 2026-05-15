# Frontier

Verified anchors:

- Sleator and Tarjan introduced splay trees and the dynamic optimality program in 1985. Their paper and later summaries identify traversal-style consequences of dynamic optimality for splay trees.
- Chaudhuri and Hoft proved the aligned-tree special case: if the nodes of a tree `T` are splayed in the preorder sequence of the same `T`, total time is `O(n)`.
- Chalermsook, Goswami, Kozma, Mehlhorn, and Saranurak (FOCS 2015 / arXiv 1507.06953) state the traversal conjecture as starting from an arbitrary initial tree and accessing the preorder of another tree. They note that only special cases were known, and prove for Greedy:
  - arbitrary initial tree: preorder cost at most `n 2^{alpha(n)^{O(1)}}`;
  - with linear preprocessing / flat geometric initial state: linear cost.
- The same 2015 paper records that `(2,3,1)`-free sequences are exactly preorder access sequences, and develops broader fixed-pattern-avoidance and `k`-decomposable bounds for Greedy.
- Levy and Tarjan, "Splaying Preorders and Postorders" (2019), prove that inserting into an empty BST via splaying in preorder or postorder order costs linear time. They explicitly use pattern avoidance: preorders avoid `(2,3,1)`, postorders avoid `(3,1,2)`.
- Levy and Tarjan also prove a balanced-target variant: if the target tree is weight-balanced, then splaying its preorder or postorder from any other initial tree costs linear time, via dynamic finger structure.
- Levy and Tarjan, "A New Path from Splay to Dynamic Optimality" (SODA 2019), introduce the subsequence property route. They show the subsequence property would imply dynamic optimality and traversal/deque consequences; this is a possible proof-theory link but is broader than this candidate.
- Chalermsook, Gupta, Jiamjitrak, Obscura Acosta, Pareek, and Yingchareonthawornchai (SODA 2023) improve Greedy pattern-avoidance bounds. For Greedy, preorder traversal holds up to `O(2^{alpha(n)})`; postorder is settled; deque and split get improved near-linear bounds.
- Chalermsook, Pettie, and Yingchareonthawornchai (SODA 2024 / arXiv 2307.02294) sharpen product-pattern extremal bounds, giving `O(n 2^{(1+o(1)) alpha(n)})` sorting for fixed pattern-avoiding permutations using GreedyFuture / SmoothHeap-style analyses.
- Berendsohn, Kozma, and Opler (arXiv 2310.04236, revised 2025) resolve the offline-optimum pattern-avoiding BST conjecture: for any fixed avoided pattern, an optimal BST has constant amortized cost. This raises the bar for online candidates: Splay and Greedy would need constant cost on fixed-pattern-avoiding inputs to match OPT.
- Pareek (arXiv 2407.03666, revised 2025) proves Greedy is linear on preorder sequences for a "permutation initial tree" class. This is not the arbitrary-initial-tree traversal conjecture, but it narrows the initial-tree issue.

Inferred frontier:

- The most promising narrow theorem-project formulation is not "Splay is dynamically optimal," but "Splay has linear or constant-amortized cost on a well-chosen subclass of 231-avoiding / fixed-pattern-avoiding permutations under a specific initial-tree regime."
- The current barrier is transfer: forbidden-submatrix techniques are powerful for Greedy's geometric execution log, while Splay's rotations do not expose the same clean matrix structure.
- The offline optimum is now known to be constant on fixed-pattern-avoiding inputs, so a superconstant upper bound for Splay/Greedy on these inputs is no longer merely a loose analysis; it is a concrete gap to OPT.

TODO: verify source:

- Check the final published versions of the 2023/2024/2025 pattern-avoidance papers for exact theorem numbering and whether "Greedy/Splay constant on fixed-pattern-avoiding inputs remains open" is stated explicitly in the paper or only on author pages.
- Check whether any 2025/2026 paper closes the Splay preorder traversal conjecture under arbitrary initial tree.
