# Skeptical Audit

Why this might not actually be open:

- The current source does not state a single formal theorem target.
- Existing history-independent priority queue results may already solve weak or strong variants depending on operation set and memory model.

Why this might be too saturated:

- The Dagstuhl report says participants explored this direction; follow-up publications may already be in progress.

Why automatic evaluation might fail:

- Testing whether representation distributions depend only on current state is hard beyond very small instances.
- Weak vs strong history independence and adversary model choices can completely change the problem.

What would falsify interest:

- No formal source can be found beyond the Dagstuhl discussion.
- The cleanest formalization is already solved or too far from data-structure theory.

Primary sources to check before promotion:

- Conway/Kuszmaul history-independent heap papers or slides.
- Recent list-labeling papers using history independence.
- Dagstuhl follow-up publications from the history-independent heaps working group.

Batch 002 adversarial addendum, 2026-05-15:

- `history_independent_concurrent_hashing` should not be promoted as a clean open theorem. The 2025 concurrent hash-table paper is already a solution/narrowing paper for strongly history-independent concurrent dictionaries.
- Residual promise, if any, must be model-specific: fixed cell capacity, progress condition, base-object strength, or exact lower-bound threshold.
- Best use for the concurrent lead is Lean/model-checking background for tiny linearizable histories, not OpenEvolve-style large search.
- Weak-source flag: "concurrent SHI dictionaries are open" is too broad after 2025; cite the 2025 paper as narrowing/resolving the broad problem.
