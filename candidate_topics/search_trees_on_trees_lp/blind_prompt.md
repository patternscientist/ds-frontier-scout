# Blind Prompt

You are studying the following self-contained problem.

Let `U` be an undirected tree whose vertices are the searchable items. A search tree on `U` is defined recursively: choose a root vertex `r`; remove `r` from `U`; for each connected component of `U - r`, attach as a child of `r` a search tree recursively built on that component. Thus the search tree has the same vertex set as `U`, but a different edge structure.

Given nonnegative query weights `w_v`, the static cost of a search tree `T` is:

`cost(T) = sum_v w_v * depth_T(v)`,

where the root has depth 1.

Problem: understand exact optimization and LP behavior for search trees on tree topologies beyond the already-understood baseline cases.

Baseline sanity checks, not open targets:

- paths correspond to ordinary optimal binary search trees and should be used to validate definitions and algorithms;
- stars are a solved/integral case for the LP frontier and should be used as a second baseline.

Actual research targets:

- prove or refute LP integrality, depth-projection integrality, or root-rounding guarantees for a precise non-baseline subclass;
- characterize almost-stars and edge-diameter-3 topologies, where every two edges are connected by a path of at most 3 edges;
- find a strengthened LP, a valid inequality family, or a modified rounding rule that avoids known small counterexamples;
- design a polynomial-time exact algorithm for a nontrivial topology class not already covered by paths or stars.

Try dynamic programming, exchange arguments, root-choice characterizations, or a linear-programming relaxation. If you propose an LP, define variables and prove whether all extreme points correspond to search trees for the claimed subclass. Treat paths and stars as tests that your formalization has not drifted away from the known baselines.

Do not use literature or web search. State exact claims and failure modes.
