# Blind Prompt

Design an ordered dictionary stored only as a permutation of its `n` keys, with `O(1)` extra machine words between operations. Do not use gaps, `(1+epsilon)n` cells, packed-memory arrays, or other non-implicit linear-space structures.

Support search, insert, and delete in `O(log_B n)` block transfers cache-obliviously. Also support scanning or reporting the next `r` keys from a query position in `O(log_B n + r/B)` block transfers, or prove this is impossible under the implicit cache-oblivious model.
