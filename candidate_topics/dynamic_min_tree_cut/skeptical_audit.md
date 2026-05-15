# Skeptical Audit

Batch 002 adversarial audit, 2026-05-15:

- Open status: plausible but not crisp. The min-tree-cut subroutine is identified through dynamic min-cut literature, but Batch 002 has not verified a standalone modern open-problem statement for exactly this dynamic problem.
- Why might this not actually be open? SODA 2025/2026 dynamic min-cut progress may include subroutines or reductions that improve or bypass min-tree-cut. Full papers must be checked before claiming the subroutine remains a bottleneck.
- Why might it be too saturated? Fully dynamic min-cut and dynamic graph algorithms are very active. A broad "dynamic min-cut" target is not under-attended.
- Smallest meaningful subproblem: unweighted fully dynamic graph, explicitly maintained spanning tree, maintain the minimum tree-edge cut value under edge insertions/deletions, with a specified worst-case/amortized update target.
- Best use after audit: background context or a narrow OpenEvolve project for adversarial trace generation; not a broad theorem candidate.
- Why might automation fail or mislead? Simulators can find update traces that break candidate summaries, but they do not validate asymptotic worst-case update bounds or cell-probe barriers.
- Weak-source flag: the 2025/2026 SIAM proceedings links are contextual until full details are read; do not cite them as proving the min-tree-cut gap remains open.
- What would falsify interest? A known polylogarithmic min-tree-cut data structure, or evidence that modern min-cut algorithms no longer use this subroutine as a bottleneck.
- Primary sources to check next: Henzinger-Krinninger-Nanongkai-Saranurak hardness paper; Thorup dynamic min-cut papers; El-Hayek-Henzinger-Li 2025/2026 full papers.
