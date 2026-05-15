# Skeptical Audit

Why this might not actually be open:

- The full traversal conjecture is old and widely discussed; a recent paper may close a restricted formulation under different terminology.
- Empty-tree insertion, aligned-tree preorder, balanced-target preorder, flat initial tree for Greedy, and permutation-initial-tree for Greedy are solved/partial baselines, not the arbitrary-initial-tree Splay target.
- Berendsohn-Kozma-Opler resolve constant amortized offline OPT for fixed-pattern-avoiding inputs. Any claim that "pattern-avoiding BST cost is open" is now false.

Why this might be too saturated:

- Dynamic optimality, traversal, deque, split, Greedy, and Splay are flagship topics.
- This candidate is only defensible as a narrow 231-avoiding/preorder corner with exact initial-state distinctions.

Why automatic evaluation might fail:

- Small Catalan-class simulations may miss nested bad sequences.
- Exact offline BST optimum is expensive; using Greedy or Splay as a proxy can hide the actual competitiveness question.
- Greedy geometric-model evidence does not transfer automatically to Splay rotations.

What would falsify interest:

- A post-2025 source proves Splay linear for arbitrary initial tree on preorder/231-avoiding permutations.
- The only remaining formulation is equivalent to full dynamic optimality or the subsequence property.
- Experiments fail to find a stable invariant beyond known empty/aligned/balanced-target cases.

Primary sources to check before promotion:

- Chalermsook-Goswami-Kozma-Mehlhorn-Saranurak 2015 for traversal and 231-free/preorder equivalence.
- Levy-Tarjan 2019 for empty insertion and balanced-target Splay variants.
- Pareek 2025 for Greedy on permutation initial trees.
- Berendsohn-Kozma-Opler v4, 2025-11-24, for offline OPT on fixed-pattern-avoiding input.
- Author pages/citations of the above for 2026 follow-ups.

Smallest acceptable project:

- Pick one nontrivial initial-tree class not covered by empty/aligned/balanced/permutation-initial-tree results and prove Splay linear or construct an obstruction.
