# Skeptical Audit

Batch 002 adversarial audit, 2026-05-15:

- Open status: explicit in Ajtai-Feldman-Hassidim-Nelson, with modern status still uncertain. Quick search did not find a primary closure of randomized `O(n)` error-2 maximum or randomized error-`k` sorting.
- Why might this not actually be open? Follow-up work under noisy comparisons, uncertain comparisons, tournament sorting, or interval-order models may solve an equivalent special case under different terminology.
- Why might it be too saturated? It is not saturated as a data-structure topic. The bigger risk is that it is adjacent to, rather than inside, data-structure theory.
- Smallest meaningful subproblem: randomized error-2 maximum under adversarial imprecise comparisons, with a fixed success probability and explicit comparison budget.
- Best use after audit: OpenEvolve project. The finite adversary/game structure is the strongest surviving Batch 002 evaluator fit.
- Why might automation fail or mislead? Small randomized strategies may overfit low `n`; Monte Carlo success against sampled adversaries is not a proof. Prefer exact adversary LPs, minimax formulations, or certificate checkers.
- Weak-source flag: noisy-comparison papers are not interchangeable with this model; every source must state its reliability/adversary assumptions.
- What would falsify interest? A later `O(n)` randomized error-2 algorithm, a matching lower bound, or a proof that the question is a direct corollary of known noisy-tournament results.
- Primary sources to check next: citations of arXiv:1501.02911 after 2015; noisy/uncertain sorting papers that explicitly match adversarial near-tie comparisons.
