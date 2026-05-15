# Skeptical Audit

Batch 003 adversarial audit date: 2026-05-15.

Verdict: keep, but downgrade from evaluator-first to theorem/lower-bound context.

- Open-problem claim: explicit. Ding et al. ITCS 2025 ask Open Question 15 for the exact one-pass dynamic-stream space complexity of `(1+epsilon)` approximate min-cut in simple weighted graphs.
- Narrowing required: the statement must keep the model distinctions visible: insertion-only versus turnstile/dynamic stream; simple weighted undirected graphs versus arbitrary multigraphs; randomized versus deterministic; exact versus `(1+epsilon)` approximation; min-cut value versus cut sparsifier; and `~O(n/epsilon)` versus `~O(n/epsilon^2)` up to polylog factors.
- Newer-work check: quick 2026 search found dynamic graph min-cut progress and unrelated streaming cut/max-cut work, but no primary source closing Open Question 15. The Waterloo seminar abstract is potentially misleading because it says the paper resolves the streaming min-cut question, but the paper's abstract and Open Question 15 distinguish insertion-only results from the dynamic-stream gap.
- Saturation risk: medium-high. Streaming graph sketching and sparsification are active, and the problem may be attacked by the same small set of specialists rather than neglected by the field.
- Smallest meaningful subproblem: randomized one-pass turnstile stream over simple weighted undirected graphs, output only the min-cut value within `(1+epsilon)`, and prove either an `~Omega(n/epsilon^2)` lower bound or an `~O(n/epsilon)` sketch that does not preserve all cuts.
- Best use after audit: theorem_project with limited OpenEvolve support. Automated experiments can search finite hard distributions or sketch collisions, but they are unlikely to certify the asymptotic communication lower bound.
- Blind prompt risk: acceptable if it preserves the exact model distinctions. It should not imply that dynamic-stream cut sparsification lower bounds already apply to min-cut.
- Evaluator caveat: a small-instance sketch/collision evaluator would be useful for hypothesis generation only. It would be misleading if reported as evidence for the asymptotic space gap.
- Falsifier: a post-ITCS 2025 paper giving either a dynamic-stream `~O(n/epsilon)` min-cut sketch or an `~Omega(n/epsilon^2)` randomized lower bound for min-cut value estimation.

Primary sources to recheck before top-shortlist promotion:

- Ding, Garces, Li, Lin, Nelson, Shah, and Woodruff, ITCS 2025 full version, especially Open Question 15 and the alternative proof of Theorem 12.
- Post-2025 papers citing arXiv:2412.01143.
