# Scouting Batch 003: Underexplored Mini-Frontiers

Date: 2026-05-15

Purpose: targeted pass over underexplored areas named in `reports/search_space_gaps.md`, plus a transition artifact for the `search_trees_on_trees_lp` pilot. This is not a broad sweep. I promoted only candidates where the source trail is primary and the remaining gap is narrow enough to audit.

## Executive Takeaways

Batch 003 promotes five sharper mini-frontiers:

1. `dynamic_stream_mincut_space`: one-pass dynamic-stream `(1+epsilon)` min-cut space complexity.
2. `directed_roundtrip_compact_routing`: compact roundtrip routing in weighted directed graphs beyond the new `k=3` breakthrough.
3. `concurrent_shi_cell_capacity`: exact cell-width/progress frontier for strongly history-independent concurrent hash tables.
4. `connected_circle_segment_queries`: lower bounds and construction/query tradeoffs for circle-segment reporting on connected geometric graphs.
5. `cache_oblivious_implicit_scanning`: efficient scans/range reporting in cache-oblivious implicit dictionaries with `O(log_B n)` search/update.

Not promoted in this pass:

- Succinct/compressed structures: the 2026 grammar-random-access result looks too fresh and may close much of the obvious grammar-compression gap. The old bundled LZ/grammar Dagstuhl questions should still be split later, but not promoted from Batch 003 without exact notation.
- Range alpha-majority output sensitivity: the 2011/2013 open line is partly blunted by later encoding/compressed range-majority work; keep as context for `range_mode_queries`.
- Kinetic high-dimensional extent: still interesting, but the exact open line remains too broad for a promoted Batch 003 candidate.
- Systems-only concurrency and DHT engineering questions: filtered out for lack of a clean theory model.

## Candidate 1: Dynamic-Stream Min-Cut Space

- short name: `dynamic_stream_mincut_space`
- open_status: explicit
- target area: streaming/sketching data structures; dynamic-stream graph sketches.
- self-contained problem statement: In a one-pass turnstile stream of edge insertions and deletions defining a simple weighted undirected graph, compute a `(1+epsilon)` approximation to the global minimum cut. Determine the exact space complexity, up to polylogarithmic factors, as a function of `n` and `epsilon`.
- primary source: Ding, Garces, Li, Lin, Nelson, Shah, and Woodruff, "Space Complexity of Minimum Cut Problems in Single-Pass Streams," ITCS 2025, DOI `10.4230/LIPIcs.ITCS.2025.43`, https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2025.43.
- exact open gap: Open Question 15 asks for the exact space complexity of `(1+epsilon)` approximate min-cut in one-pass dynamic streams. The source places the gap between the insertion-only lower bound `~Omega(n/epsilon)` and known dynamic-stream algorithms using `~O(n/epsilon^2)` space.
- why solving it matters: graph sketching and sparsification are central to streaming algorithms; min-cut is a sharper task than preserving all cuts, so resolving the gap would say whether dynamic deletions force full sparsifier-scale space.
- why it may be under-attended: it is a streaming lower-bound problem adjacent to data structures, not a classic online update/query data structure; progress likely requires communication-complexity machinery.
- theorem-project suitability: 3/5.
- OpenEvolve/evaluator suitability: 4/5.
- Lean/formalization/certificate suitability: 2/5.
- AI-collaboration fit: good for constructing finite turnstile hard distributions, testing sketch relaxations, and enumerating small graph families where cut sketches collapse distinct instances.
- risks / reasons to downgrade: lower bounds may require non-small communication games; the candidate may be too far from core data-structure theory; a follow-up after ITCS 2025 could narrow the gap.
- suggested blind no-internet prompt: "In a one-pass turnstile stream over weighted edges of an `n`-vertex simple graph, maintain enough information to output a `(1+epsilon)` approximation to the global minimum cut. Either design a sketch using `~O(n/epsilon)` space or prove that deletions require `~Omega(n/epsilon^2)` space. Favor reductions on explicit small graph families."
- next verification task: read the full arXiv version and extract the alternative proof of Theorem 12 promised as a possible route to a dynamic-stream lower bound.

## Candidate 2: Directed Compact Roundtrip Routing

- short name: `directed_roundtrip_compact_routing`
- open_status: explicit
- target area: distributed/network data structures; compact routing.
- self-contained problem statement: Given a weighted strongly connected directed graph, preprocess local routing tables and labels of size about `~O(n^{1/k})` per vertex so that routing decisions are made locally and the route has low roundtrip stretch. Determine the best possible stretch for every `k`.
- primary source: Kadria and Roditty, "Compact Routing Schemes in Undirected and Directed Graphs," DISC 2025 / arXiv:2503.13753, https://arxiv.org/abs/2503.13753 and https://drops.dagstuhl.de/storage/00lipics/lipics-vol356-disc2025/LIPIcs.DISC.2025.38/LIPIcs.DISC.2025.38.pdf.
- exact open gap: Problem 3 asks for the best stretch of compact roundtrip routing in weighted directed graphs using `~O(n^{1/k})` local storage. The paper improves the `k=3` case from `(12+epsilon)` to 7 stretch, but the general directed tradeoff remains open.
- why solving it matters: compact routing is a distributed data structure for shortest-path information; directed roundtrip distances are one of the few ways to get meaningful compact routing in directed graphs.
- why it may be under-attended: it lives between distributed computing, graph algorithms, and distance-oracle data structures; it is less visible than undirected stretch-oracle work.
- theorem-project suitability: 3/5.
- OpenEvolve/evaluator suitability: 2/5.
- Lean/formalization/certificate suitability: 3/5.
- AI-collaboration fit: useful for finite directed graph searches, checking stretch of proposed local-label schemes, and generating extremal instances; weak for inventing the main asymptotic routing construction automatically.
- risks / reasons to downgrade: this is active after the 2025 improvement; the lower-bound side leans on girth-conjecture-style assumptions; finite search may not generalize.
- suggested blind no-internet prompt: "Design a compact labeled routing scheme for weighted directed graphs under roundtrip distance `d(u,v)+d(v,u)`. Each vertex stores `~O(n^{1/k})` words. For general `k`, beat the known `4k+epsilon`-style stretch or prove a lower bound approaching `2k-1`."
- next verification task: check the arXiv v3 full version for any additional open-problem refinements after the DISC proceedings version.

## Candidate 3: Concurrent SHI Cell-Capacity Frontier

- short name: `concurrent_shi_cell_capacity`
- open_status: inferred
- target area: concurrency/history-independent residuals.
- self-contained problem statement: Characterize the minimum shared-cell width and progress guarantees needed for a linearizable concurrent dictionary whose quiescent shared-memory representation is strongly history independent.
- primary source: Attiya, Bender, Farach-Colton, Oshman, and Schiller, "History-Independent Concurrent Hash Tables," STOC 2025 / arXiv:2503.21016, https://arxiv.org/abs/2503.21016 and https://hagit.net.technion.ac.il/files/2025/02/STOC2025.pdf.
- exact open gap: the paper solves a broad open problem by giving a lock-free SQHI hash table with each cell storing two elements and two bits, and proves impossibility for one-element cells under stronger wait-free-style conditions. The residual candidate is the exact boundary for lock-free or obstruction-free SQHI dictionaries with one-element cells plus `O(1)` metadata versus two-element lookahead cells.
- why solving it matters: it is a clean theory-facing interface between privacy, representation independence, and concurrent dictionaries.
- why it may be under-attended: the problem sits between concurrent algorithms and history-independent data structures, and the main 2025 paper may make the residual look like a detail even though it defines the exact model boundary.
- theorem-project suitability: 3/5.
- OpenEvolve/evaluator suitability: 2/5.
- Lean/formalization/certificate suitability: 4/5.
- AI-collaboration fit: strong for small-state linearizability/SQHI model checking and for testing representation-equivalence invariants; weak for asymptotic concurrent algorithm discovery.
- risks / reasons to downgrade: the open status is inferred from the gap between the positive and negative results, not stated as a standalone open problem; model choices could make the residual trivial or already settled in the full paper.
- suggested blind no-internet prompt: "Model a concurrent set with lookup, insert, and delete. Require linearizability and state-quiescent strong history independence. Can a lock-free open-addressing dictionary store only one key plus `O(1)` bits per shared cell, or is a two-key lookahead cell necessary? Prove a lower bound or give a construction in a small LL/SC model."
- next verification task: read the full STOC 2025 proof of Theorem 2 and the tightness discussion to pin down which progress conditions are already ruled out.

## Candidate 4: Connected Circle-Segment Query Tradeoffs

- short name: `connected_circle_segment_queries`
- open_status: explicit
- target area: dynamic/online geometric data structures and trajectory/polyline-style geometric indexing.
- self-contained problem statement: Preprocess the edge segments of a connected geometric graph so that a query circle reports all intersected segments output-sensitively. Determine optimal space/query/construction tradeoffs in the connected-graph setting, and whether nested convex-hull or segment-Voronoi structures can be merged or cascaded across the edge-partition tree.
- primary source: Afshani, Bosch, and Storandt, "Circle-Segment Intersection Queries in Connected Geometric Graphs," ISAAC 2025, DOI `10.4230/LIPIcs.ISAAC.2025.3`, https://drops.dagstuhl.de/storage/00lipics/lipics-vol359-isaac2025/html/LIPIcs.ISAAC.2025.3/LIPIcs.ISAAC.2025.3.html.
- exact open gap: the paper's future-work section asks for lower bounds on data-size/query-time tradeoffs in the connected-graph setting and suggests improving construction/query times by bottom-up construction or fractional-cascading-style reuse over nested convex hulls.
- why solving it matters: road networks, map matching, meshes, and moving-object proximity all need circle/disk versus segment-network queries; this is a rare geometry data structure where connectivity is the main exploitable promise.
- why it may be under-attended: it is a very specific geometry problem, newer than the standard point-range-searching canon, and its best-known structure is partly motivated by implementation.
- theorem-project suitability: 3/5.
- OpenEvolve/evaluator suitability: 4/5.
- Lean/formalization/certificate suitability: 2/5.
- AI-collaboration fit: good for generating connected segment instances, measuring AABB false positives, testing partition-tree variants, and searching for lower-bound gadgets with many oracle positives but small output.
- risks / reasons to downgrade: asymptotic formulas in the HTML rendering are mangled and should be checked in PDF/source; lower-bound methods for geometry may be too hard for finite search; "improve construction time" could be engineering rather than theory unless formalized.
- suggested blind no-internet prompt: "A connected geometric graph has `m` straight-line edges in the plane. Build a data structure that reports all edges intersecting a query circle. Use connectivity essentially. Seek output-sensitive query time with near-linear space, or prove a data-size/query-time lower bound for connected inputs distinct from arbitrary segment sets."
- next verification task: recover the PDF/LaTeX formulas for Theorems 7 and 8 and define one concrete finite lower-bound family.

## Candidate 5: Cache-Oblivious Implicit Dictionary Scans

- short name: `cache_oblivious_implicit_scanning`
- open_status: explicit_modern_status_uncertain
- target area: cache-oblivious/external-memory dictionaries; implicit data structures.
- self-contained problem statement: Maintain an ordered dictionary using exactly the `n` key cells and `O(1)` registers, with cache-oblivious `O(log_B n)` search/update bounds, while also supporting efficient ordered scans or range reporting in `O(log_B n + r/B)` or `O(1+r/B)` block transfers.
- primary source: Franceschini and Grossi, "Optimal Cache-Oblivious Implicit Dictionaries," ICALP 2003, DOI `10.1007/3-540-45061-0_27`, PDF https://pages.di.unipi.it/grossi/PAPERS/icalp03.pdf.
- exact open gap: the paper states that its implicit cache-oblivious dictionary does not support efficient scanning and that efficient scanning with comparable `O(log_B n)` bounds is also open for cache-oblivious data structures alone.
- why solving it matters: scans/range reporting are the operation that makes ordered dictionaries useful as external-memory indexes; this asks whether implicitness and cache-oblivious locality can coexist with sequential locality.
- why it may be under-attended: implicit dictionaries are niche, old, and technically fussy; later work focused on working-set/predecessor variants rather than scan locality.
- theorem-project suitability: 4/5.
- OpenEvolve/evaluator suitability: 3/5.
- Lean/formalization/certificate suitability: 3/5.
- AI-collaboration fit: good for simulating memory layouts across unknown block sizes, checking amortized rebuild schedules, and searching for permutation layouts with both search and scan locality.
- risks / reasons to downgrade: modern status is uncertain after later cache-oblivious implicit predecessor/working-set dictionaries; the exact scan target must distinguish implicit, pointerless, `(1+epsilon)n`-space, cache-aware, and cache-oblivious models.
- suggested blind no-internet prompt: "Design an implicit ordered dictionary stored only as a permutation of its `n` keys and using `O(1)` extra words. It should support search, insert, and delete in `O(log_B n)` cache misses cache-obliviously, and report the next `r` keys after a search key in `O(log_B n + r/B)` or better. If impossible, prove a locality lower bound for implicit cache-oblivious layouts."
- next verification task: inspect Brodal/Kejlberg-Rasmussen/Jacob follow-ups to see whether scan/range-reporting was later achieved under the exact implicit model.

## Cross-Area Audit

- Geometry: `connected_circle_segment_queries` is the only promoted geometry candidate. Dynamic planar point location and kinetic high-dimensional extent remain too broad or too source-fragile in this pass.
- Streaming/sketching: `dynamic_stream_mincut_space` is the strongest explicit open problem found; it is evaluator-friendly but lower-bound-heavy.
- Succinct/compressed: no new promotion. The newest grammar-compressed random-access work must be read before making a claim.
- Lower bounds/cell probe: the best finite-hard-instance angle is split between dynamic-stream min-cut and connected-geometry lower-bound gadgets, not a pure cell-probe candidate.
- Concurrency/history independence: `concurrent_shi_cell_capacity` is promoted with caution because the source is strong but the residual open status is inferred.
- Distributed/network: `directed_roundtrip_compact_routing` is the cleanest network-data-structure candidate.
- Cache-oblivious/external memory: `cache_oblivious_implicit_scanning` is old but crisp and unusually niche.

## Implication For The Fixed-Point Shortlist

Batch 003 does not dislodge `search_trees_on_trees_lp` as the leading pilot. The new candidates are useful as second-wave mini-frontiers, especially `dynamic_stream_mincut_space` and `cache_oblivious_implicit_scanning`, but none currently has the same combined theorem/certificate/OpenEvolve readiness as STT LP.

Do not rewrite `reports/fixed_point_recommendation.md` yet. The next step should be an adversarial audit of these five promoted mini-frontiers, plus a source-status check for the inferred/uncertain residuals.
