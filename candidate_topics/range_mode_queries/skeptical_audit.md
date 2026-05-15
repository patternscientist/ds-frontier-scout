# Skeptical Audit

Batch 002 adversarial audit, 2026-05-15:

- Open status: still plausible, but partly inferred. The source trail supports a real static exact range-mode gap; this audit did not find a closure. However, the blind prompt's `O(sqrt n)` target is stale if stronger `O(sqrt(n / log n))`-style refinements are the right current upper-bound baseline.
- Why might this not actually be open? Later range-mode, conditional-lower-bound, or word-RAM papers may have narrowed the linear-space exact query gap more than Batch 002 recorded. Need the ToCS/final versions and post-2012 citations before top-shortlist promotion.
- Why might it be too saturated? Range searching is mature and lower-bound-heavy. The candidate survives only because exact static range mode is a crisp niche, not because range queries are under-attended broadly.
- Smallest meaningful subproblem: linear-word static exact range mode on arrays, with word-RAM rank/select available, and either an improved upper bound or a lower bound for a named block/candidate-list framework.
- Best use after audit: OpenEvolve project with theorem sidecar. Exact small-instance oracles are useful for testing candidate lists and adversarial arrays.
- Why might automation fail or mislead? Finite arrays may reward block heuristics that do not scale; brute-force lower-bound search does not establish cell-probe lower bounds.
- Weak-source flag: range alpha-majority output-sensitivity is adjacent context only and should not be used as evidence for exact range-mode openness.
- What would falsify interest? A modern linear-space polylogarithmic exact range-mode structure, a strong matching lower bound, or evidence that all plausible finite-evaluator subproblems have already been exhausted.
- Primary sources to check next: the final Chan-Durocher-Larsen-Morrison-Wilkinson paper, Greve-Jorgensen-Larsen-Truelsen ICALP 2010, and post-2018 range-mode/range-majority papers.
