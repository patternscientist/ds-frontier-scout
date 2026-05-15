# Frontier

Verified source:

- Franceschini and Grossi, "Optimal Cache-Oblivious Implicit Dictionaries," ICALP 2003.
- They solve the long-standing implicit dictionary search/update target with `O(log n)` time and cache-oblivious `O(log_B n)` block transfers, using exactly `n` cells.
- They note that their structure does not support efficient scanning.
- They state that efficient scanning with comparable `O(log_B n)` bounds is also open for cache-oblivious data structures alone.

Adjacent sources to check:

- Brodal, Kejlberg-Rasmussen, and Truelsen on cache-oblivious implicit dictionaries with working-set properties.
- Brodal and Kejlberg-Rasmussen on implicit predecessor dictionaries with working-set bounds.

TODO: verify source:

- Determine whether later implicit/cache-oblivious dictionaries support scans under the exact `n`-cell implicit model.
