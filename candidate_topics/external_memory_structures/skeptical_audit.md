# Skeptical Audit

Why this might not actually be open:

- The original "is DecreaseKey degradation necessary?" question is answered affirmatively by Eenberg-Larsen-Yu.
- Remaining simultaneous work/I/O optimality questions are not yet one precise data-structure theorem.

Why this might be too saturated:

- External memory lower bounds and cache-oblivious structures are technically mature.
- Work/I/O tradeoffs may already be under active development after Dagstuhl 25191.

Why automatic evaluation might fail:

- Cache-aware, cache-oblivious, comparison, cell-probe, amortized, randomized, and word-RAM models differ sharply.
- Toy I/O simulators rarely certify asymptotic lower bounds.

What would falsify interest:

- No clean single theorem target emerges after separating priority queues, deferred structures, red-blue sorting, and lazy B-tree context.

Primary sources to check before promotion:

- Eenberg-Larsen-Yu STOC 2017.
- Afshani Dagstuhl 25191 simultaneous work/I/O statement and any 2025 manuscript.
- Lazy B-Trees only for the biased-search-tree subproblem, not as evidence for the broad cluster.
