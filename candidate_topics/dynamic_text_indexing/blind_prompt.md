# Blind Prompt

Maintain a mutable string `T` under insertion and deletion of substrings. Build an index using linear bits, up to lower-order terms, that reports all occurrences of a pattern `P` in time `O((|P|+occ) polylog |T|)` and updates a substring of length `s` in `O(s polylog |T|)` time.

Either propose a data structure or isolate a barrier for compact dynamic suffix/BWT-style indexes.
