# Blind Prompt

Model a concurrent dictionary supporting lookup, insert, and delete over a universe `U`.

Require linearizability and state-quiescent strong history independence: whenever no update is in progress, the shared memory representation distribution depends only on the current set.

Can a lock-free open-addressing dictionary use one key plus `O(1)` bits per cell? Or is a two-key lookahead cell necessary? Work in a clean LL/SC or compare-and-swap model.
