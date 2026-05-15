# Problem

Preprocess an array `A[1..n]` so that a query interval `[i,j]` returns an element of maximum frequency in `A[i..j]`.

Open status: open. The exact optimal query time for exact range mode with linear or near-linear space remains unresolved after the known `O(sqrt(n))`-type linear-space upper bounds and much smaller cell-probe lower bounds.

Batch 002 framing: this is a strong OpenEvolve-first candidate because exact small-instance oracles are trivial and block/candidate-list data structures can be stress-tested automatically.
