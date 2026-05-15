# Frontier

Verified source:

- Attiya, Bender, Farach-Colton, Oshman, and Schiller, "History-Independent Concurrent Hash Tables," STOC 2025 / arXiv:2503.21016.
- The paper initiates the study of history-independent concurrent hash tables.
- It asks whether there is a linearizable lock-free SQHI hash table using `O(m)` cells of width `O(log u)`, independent of the number of concurrent operations.
- It gives a lock-free construction using LL/SC where each cell stores two elements and two bits.
- It proves lower bounds for one-element cells under stronger progress assumptions, including wait-free membership queries with obstruction-free updates.

Inferred frontier:

- The remaining crisp boundary is lock-free one-element-cell SQHI versus two-element-cell SQHI.
- Small-state model checking may reveal whether the lower-bound argument extends to lock-free updates.

TODO: verify source:

- Read the tightness discussion and formal lower-bound assumptions line by line.
