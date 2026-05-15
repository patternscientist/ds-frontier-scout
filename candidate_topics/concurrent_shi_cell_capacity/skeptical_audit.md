# Skeptical Audit

Batch 003 adversarial audit date: 2026-05-15.

Verdict: downgrade sharply. The residual is inferred and Batch 003 appears to have misstated the cell-capacity frontier.

- Open-problem claim: inferred, not explicit. The STOC 2025/arXiv abstract gives a lock-free SQHI hash table with two elements and two bits per memory cell, and an impossibility result for dictionaries with wait-free membership queries and obstruction-free insertions/deletions when each cell stores only two elements plus `O(1)` bits. This is stronger and more subtle than the Batch 003 phrasing "lower bounds for one-element cells."
- Likely correction: the live residual is not simply "one key plus metadata versus two-key lookahead." The primary source suggests that two-key cells are already insufficient under stronger progress assumptions, while two-key cells suffice for the paper's lock-free construction. The real boundary is progress condition plus base-object model plus quiescence notion, not just cell width.
- Model distinctions: LL/SC versus CAS/registers; lock-free versus obstruction-free versus wait-free; wait-free lookup alone versus wait-free updates; state-quiescent history independence versus stronger concurrent history independence; hash-table-specific construction versus arbitrary dictionary.
- Newer-work check: no later closure found, but the full version must be read before any promotion because the abstract already undermines the current folder formulation.
- Saturation risk: medium-high. This is a fresh STOC 2025 paper that solves the broad problem and leaves only model-boundary residue. It may be more of an appendix-tightness exercise than an under-attended frontier.
- Smallest meaningful subproblem: formalize the two-process lower-bound model and ask whether the positive lock-free LL/SC construction can be strengthened to wait-free membership queries without increasing cell capacity or exposing pending-operation metadata. Do not start from one-element cells unless the full paper explicitly leaves that case open.
- Best use after audit: Lean_formalization_project/background_context. The right immediate work is model extraction and small-execution checking, not theorem hunting under a guessed residual.
- Blind prompt risk: high. The original Batch 003 prompt asked whether a lock-free open-addressing dictionary can use one key plus `O(1)` bits per cell; this may be already impossible, irrelevant to the positive construction, or not the paper's residual. The local prompt now carries an audit warning, but it still needs replacement after the full lower-bound theorem is extracted.
- Evaluator caveat: small-state linearizability/SQHI model checking is valuable for finding counterexamples to toy protocols, but misleading for proving impossibility in unbounded dictionaries with randomized hash functions and progress assumptions.
- Falsifier: the full STOC/arXiv version explicitly states that the one-key case is closed, or that the only open issue is wait-free versus lock-free two-key cells.

Primary sources to recheck before promotion:

- Attiya, Bender, Farach-Colton, Oshman, and Schiller, arXiv:2503.21016 full version, especially formal theorem statements and lower-bound assumptions.
- The STOC 2025 final PDF, because the abstract's "two elements" lower-bound phrasing conflicts with the Batch 003 summary.
