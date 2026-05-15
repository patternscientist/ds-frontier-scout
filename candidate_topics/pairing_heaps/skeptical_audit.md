# Skeptical Audit

Why this might not actually be open:

- Variants such as rank-pairing, smooth, slim, hollow, and other heaps have strong decrease-key bounds; those do not settle the standard two-pass pairing heap.
- Formalizations of pairing-heap variants may prove correctness or known amortized bounds without closing the classic exact-complexity gap.

Why this might be too saturated:

- The standard pairing heap has resisted analysis for decades.
- Specialists have already tried many potential functions; automated search may rediscover known dead ends.

Why automatic evaluation might fail:

- Small heaps and short traces do not expose amortized lower-bound behavior.
- Charging delete-min work back to previous decrease-key operations is subtle; a local step-cost evaluator can be wrong about amortized complexity.

What would falsify interest:

- A recent paper closes the standard two-pass pairing heap's decrease-key upper bound.
- Search only finds potentials for known variants, not the standard structure.

Primary sources to check before promotion:

- Fredman-Sedgewick-Sleator-Tarjan 1986.
- Fredman's decrease-key lower bound in the pure heap model.
- Pettie 2006 and later standard-pairing-heap analyses.
- 2023/2025 smooth/slim heap papers only as adjacent context, not as solutions.
