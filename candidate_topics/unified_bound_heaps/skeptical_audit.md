# Skeptical Audit

Why this might not actually be open:

- The broad phrase "working-set heap with decrease-key" is too loose. Haeupler, Hladik, Rozhon, Tarjan, and Tetek design a heap with a working-set bound and Fibonacci-like amortized bounds for Dijkstra universal optimality.
- Dagstuhl's explicit remaining claim is narrower: no known pointer-model data structure combines the working-set property with constant-time decrease-key.
- Several working-set definitions exist for heaps: item age by operations while present, number of later insertions, maximum live working-set size, and unified/queueish variants. Mixing them can create a fake open problem.

Why this might be too saturated:

- The post-2023 Dijkstra heap line makes this active.
- Heap adaptivity has a small but strong specialist community, and seminar collaborations may already be pursuing this exact pointer-model question.

Why automatic evaluation might fail:

- Automated heap search will be misleading unless it enforces the pointer model and exact operation costs.
- Small operation traces cannot distinguish amortized lower-bound barriers from merely bad constants.
- A simulator can find a fast structure in a RAM/array model that does not answer the stated pointer-model question.

What would falsify interest:

- A pointer-model version of the Dijkstra working-set heap exists in unpublished notes.
- The best formalization becomes a lower-bound problem in an overly artificial model.

Primary sources to check before promotion:

- Iacono's Dagstuhl 25191 statement.
- Haeupler-Hladik-Rozhon-Tarjan-Tetek, "Universal Optimality of Dijkstra via Beyond-Worst-Case Heaps."
- Haeupler-Hladik-Iacono-Rozhon-Tarjan-Tetek, "Fast and Simple Sorting Using Partial Information," for exact heap definitions.
- Elmasry/Farzan/Iacono distribution-sensitive priority queue papers, to separate working-set, queueish, and unified bounds.
