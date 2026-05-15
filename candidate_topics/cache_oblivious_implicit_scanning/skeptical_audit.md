# Skeptical Audit

Batch 003 adversarial audit date: 2026-05-15.

Verdict: keep only after reframing to the strict implicit `n`-cell model; downgrade broad cache-oblivious claims as stale.

- Open-problem claim: explicit in Franceschini and Grossi 2003, but old. The source says their exact-`n`-cell cache-oblivious implicit dictionary does not support efficient scanning, while cache-aware implicit B-trees and `(1+epsilon)n` pointerless/cache-oblivious structures can support scans.
- Modern-status check: later Brodal/Kejlberg-Rasmussen/Truelsen implicit cache-oblivious dictionaries add working-set predecessor/successor behavior using exact `n` cells, but quick checks found no explicit range-scan closure. However, non-implicit cache-oblivious B-tree/PMA-style dictionaries do support range queries/scans, so the Batch 003 phrase "open for cache-oblivious data structures alone" is stale unless interpreted exactly as in 2003.
- Model distinctions: exact `n` key cells plus `O(1)` registers versus `(1+epsilon)n` cells; implicit permutation-only encoding versus pointerless linear-space structures with gaps; cache-oblivious versus cache-aware; search/update/predecessor/successor versus reporting `r` consecutive keys; amortized versus worst-case update bounds.
- Saturation risk: medium. The strict implicit niche is under-attended, but cache-oblivious dictionaries and PMA/B-tree variants are not.
- Smallest meaningful subproblem: exact-`n`-cell implicit cache-oblivious ordered dictionary with `O(log_B n)` search/update and range reporting in `O(log_B n + r/B)` amortized block transfers. A weaker first target is static or rebuild-only layouts showing whether sorted-order locality can coexist with the permutation encodings used for updates.
- Best use after audit: theorem_project. OpenEvolve can simulate layouts across block sizes, but the finite objective may reward layouts that fail dynamic update or exact implicitness constraints.
- Blind prompt risk: acceptable after adding "do not use gaps or `(1+epsilon)n` cells." Without that warning, a model may rediscover PMA/cache-oblivious B-tree solutions that are outside the claimed residual.
- Evaluator caveat: scan-locality benchmarks alone are misleading because they ignore the encoding overhead needed for dynamic updates in the exact implicit model.
- Falsifier: a later implicit exact-`n`-cell cache-oblivious dictionary with stated range-reporting bounds, or a lower bound proving the requested scan target impossible under implicit permutation encoding.

Primary sources to recheck before promotion:

- Franceschini and Grossi, ICALP 2003, especially the introduction's comparison with cache-aware implicit B-trees and `(1+epsilon)n` pointerless structures.
- Brodal, Kejlberg-Rasmussen, and Truelsen ISAAC 2010; Brodal and Kejlberg-Rasmussen STACS 2012.
- Cache-oblivious B-tree/PMA literature only as exclusion/context, not as solving the exact implicit problem.
