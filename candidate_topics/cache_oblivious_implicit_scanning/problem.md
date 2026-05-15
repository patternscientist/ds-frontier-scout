# Problem

Maintain an ordered dictionary as an implicit cache-oblivious data structure using exactly the `n` key cells and `O(1)` registers, while supporting efficient ordered scans or range reporting.

The target is to combine `O(log_B n)` cache-oblivious search/update bounds with scan cost `O(log_B n + r/B)` or ideally `O(1+r/B)` after locating the range.

Open status: explicit in Franceschini and Grossi (ICALP 2003), modern status uncertain.
