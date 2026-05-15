# Frontier

Verified source:

- Attiya, Bender, Farach-Colton, Oshman, and Schiller, "History-Independent Concurrent Hash Tables," STOC 2025 / arXiv:2503.21016.
- The paper initiates the study of history-independent concurrent hash tables.
- It asks whether there is a linearizable lock-free SQHI hash table using `O(m)` cells of width `O(log u)`, independent of the number of concurrent operations.
- It gives a lock-free construction using LL/SC where each cell stores two elements and two bits.
- The arXiv/STOC abstract states a lower bound for dictionaries with wait-free membership queries and obstruction-free insertions/deletions even when each cell stores two elements plus `O(1)` bits. This conflicts with the earlier Batch 003 shorthand about "one-element cells" and must be checked against the formal theorem statement.

Inferred frontier:

- The remaining crisp boundary is not yet known. It likely concerns progress conditions and base-object assumptions around the two-element-cell lock-free construction, not simply one-element versus two-element cells.
- Small-state model checking may help extract model assumptions and find toy counterexamples, but it should not be treated as evidence for the asymptotic lower bound.

TODO: verify source:

- Read the tightness discussion and formal lower-bound assumptions line by line.
