# Top 20 Shortlist

Date: 2026-05-15

Status: post-Batch-003 and post-Batch-003 adversarial audit. This is a ranked scouting shortlist, not a claim that every item is ready for theorem work. Explicit current open status, evaluator clarity, saturation risk, and certificate potential outrank raw numeric score averaging.

## 1. `search_trees_on_trees_lp`

- Best use: First pilot; combined theorem, OpenEvolve, and certificate project.
- Problem: Determine exact optimization and LP/integrality behavior for static search trees on tree topologies.
- Why it matters: STTs generalize optimal BSTs and expose a modern polyhedral data-structure frontier.
- AI fit: Excellent for exact STT enumeration, rational certificates, and subclass proof search.
- Risk: Small-case enumeration may not scale, and paths/stars must not be misstated as open exact-optimization cases.
- Next verification: Reproduce Sadeh-Kaplan-Zwick small certificates and check post-v2 citations plus Golinsky's original LP source.

## 2. `quadratic_probing`

- Best use: OpenEvolve-first probabilistic-combinatorics project.
- Problem: Improve the load-factor/model frontier for constant expected insertion time in quadratic probing.
- Why it matters: A simple practical hash-table scheme still has delicate unresolved theory.
- AI fit: Strong for witness-configuration search, threshold experiments, and obstruction families.
- Risk: The old "prove anything nontrivial" gap is solved, so remaining targets may be narrow constant/model improvements.
- Next verification: Extract exact ICALP 2024 theorem statements, assumptions, and stated open directions.

## 3. `imprecise_comparison_sorting`

- Best use: OpenEvolve project with theorem sidecar.
- Problem: Decide whether randomized error-2 maximum finding under adversarial imprecise comparisons can use `O(n)` comparisons.
- Why it matters: It is a crisp adaptive-sorting/partial-information problem with finite game structure.
- AI fit: Excellent for randomized strategy synthesis, adversary LPs, and certificate checking.
- Risk: A follow-up under noisy, uncertain, tournament, or interval-order terminology may already close the exact model.
- Next verification: Run a post-2015 citation sweep separating model assumptions before treating the open status as high confidence.

## 4. `range_mode_queries`

- Best use: OpenEvolve project with lower-bound/theorem sidecar.
- Problem: Determine the optimal query time for exact static range mode using linear or near-linear space.
- Why it matters: Range mode is a canonical hard range-query problem where idempotent tricks fail.
- AI fit: Strong for hard-array generation and candidate-list/block-decomposition stress tests.
- Risk: The `O(sqrt n)` blind baseline is stale and the current upper/lower frontier needs verification.
- Next verification: Check the final Chan-Durocher-Larsen-Morrison-Wilkinson line and post-2012 exact range-mode papers.

## 5. `karp_rabin_collision_detection`

- Best use: OpenEvolve project plus crisp theorem project.
- Problem: Detect whether a fixed string and prime modulus induce equal-length Karp-Rabin fingerprint collisions faster than quadratic time.
- Why it matters: Collision certification matters for randomized string algorithms and string data structures.
- AI fit: Strong; small strings and moduli give exact brute-force oracles and adversarial instances.
- Risk: Deterministic exact detection and randomized false rejection are different problem variants.
- Next verification: Locate full Dagstuhl notes/slides and search for alternate stringology terminology.

## 6. `list_update`

- Best use: OpenEvolve project.
- Problem: Close the `1.5` to `1.6` randomized competitive-ratio gap for classical online list update.
- Why it matters: List update is a canonical self-organizing online data-structure problem.
- AI fit: Strong for finite-state policies, adversarial sequences, and LP/game lower bounds.
- Risk: Finite-state improvements may not generalize to arbitrary list size.
- Next verification: Check post-2012 online algorithms and advice/variant literature for ratio updates.

## 7. `pairing_heaps`

- Best use: OpenEvolve potential/counterexample mining.
- Problem: Determine the exact amortized decrease-key complexity of the standard two-pass pairing heap.
- Why it matters: Pairing heaps are simple, practical, and still analytically unresolved.
- AI fit: Excellent for exact simulation, adversarial traces, and potential-inequality search.
- Risk: The problem has resisted specialists for decades and small traces may underfit amortized behavior.
- Next verification: Check later standard-pairing-heap analyses and keep slim/smooth/rank-pairing variants separate.

## 8. `unified_bound_heaps`

- Best use: Theorem project.
- Problem: Build a pointer-model heap with constant-time decrease-key and working-set-style extract-min bounds.
- Why it matters: It would connect adaptive priority queues with graph-algorithm-friendly decrease-key.
- AI fit: Good for candidate structures and amortized potential exploration after definitions are fixed.
- Risk: Broad non-pointer formulations are ambiguous after recent Dijkstra working-set heap work.
- Next verification: Read Iacono's exact Dagstuhl statement and the Dijkstra universal-optimality heap papers.

## 9. `lazy_b_trees`

- Best use: Theorem project.
- Problem: Construct an external-memory biased search tree with linear block space and weighted-search I/O guarantees.
- Why it matters: It could remove a key obstacle in lazy B-trees and adaptive external-memory dictionaries.
- AI fit: Good for design-space pruning and local lemma search.
- Risk: "Fully satisfactory" must be turned into a precise theorem before proof attempts.
- Next verification: Extract exact target operations and bounds from the MFCS 2025 full version.

## 10. `dynamic_stream_mincut_space`

- Best use: Theorem/lower-bound project with limited evaluator support.
- Problem: Determine the exact one-pass dynamic-stream space complexity of `(1+epsilon)` approximate min-cut in simple weighted graphs.
- Why it matters: It asks whether deletions force sparsifier-scale space for a sharper task than all-cut preservation.
- AI fit: Useful for explicit hard-distribution sketches and small graph-family collision searches.
- Risk: Finite sketch collisions are only hypothesis generators and may not yield the required communication lower bound.
- Next verification: Read the full ITCS 2025/arXiv version and extract the route suggested around Open Question 15.

## 11. `cache_oblivious_implicit_scanning`

- Best use: Theorem project after strict-model verification.
- Problem: Support range scans in an exact `n`-cell implicit cache-oblivious ordered dictionary with `O(log_B n)` search/update.
- Why it matters: It probes whether implicitness, cache-oblivious locality, and scan locality can coexist.
- AI fit: Moderate for layout simulation and cache-miss checking across unknown block sizes.
- Risk: Broad cache-oblivious scanning is stale; only the strict exact-`n`-cell implicit model survives the audit.
- Next verification: Check later implicit cache-oblivious dictionary follow-ups for exact range-scan support.

## 12. `path_compression_topdown`

- Best use: Lean/formalization and staged proof project.
- Problem: Give a simple direct inverse-Ackermann proof from the Seidel-Sharir top-down path-compression recurrence.
- Why it matters: It could clarify a foundational union-find analysis.
- AI fit: Excellent once the exact recurrence is available.
- Risk: This is proof archaeology rather than a new data-structure theorem, and a clean proof may exist in notes.
- Next verification: Copy the exact recurrence and Ackermann normalization from Seidel-Sharir/Tarjan sources.

## 13. `connected_circle_segment_queries`

- Best use: Geometry theorem lead with evaluator side support.
- Problem: Prove lower bounds or improve tradeoffs for circle-segment reporting on connected geometric graphs.
- Why it matters: Connectivity is a natural promise for road networks, meshes, and trajectory-like segment sets.
- AI fit: Good for connected instance generation, oracle checking, and partition-tree stress tests.
- Risk: The clean explicit theory gap is lower-bound/tradeoff oriented; construction-time suggestions may be implementation work.
- Next verification: Use the PDF/source to confirm the exact ISAAC 2025 formulas and isolate one finite lower-bound family.

## 14. `succinct_compressed_structures`

- Best use: Theorem project after splitting; grammar/DAG side may become OpenEvolve.
- Problem: Improve LZ compressed indexing or remove expansion-length overhead in grammar-compressed random access.
- Why it matters: Compact random access and compressed indexes are core succinct/string data-structure tools.
- AI fit: Good for grammar/DAG sampling schemes and small counterexample generators.
- Risk: The folder bundles two distinct problems and the Dagstuhl HTML omits crucial notation.
- Next verification: Recover exact PDF/slides notation and split LZ indexing from grammar/DAG length sampling.

## 15. `splay_preorder_231`

- Best use: Background context or narrow theorem/evaluator probe.
- Problem: Prove or refute restricted Splay traversal bounds on preorder/231-avoiding access sequences under a precise initial-tree regime.
- Why it matters: It tests narrow pieces of the dynamic-optimality landscape.
- AI fit: Good for exact Splay simulation, Catalan generators, and candidate invariant falsification.
- Risk: Severe saturation and many nearby Splay/Greedy/offline-OPT results already narrow the target.
- Next verification: Check post-2025 follow-ups for arbitrary-initial-tree Splay preorder.

## 16. `directed_roundtrip_compact_routing`

- Best use: Theorem/background project.
- Problem: Determine the best stretch of compact roundtrip routing in weighted directed graphs with `~O(n^{1/k})` local storage.
- Why it matters: Compact routing is a distributed data structure for shortest-path information in directed graphs.
- AI fit: Useful for finite directed graph falsification of proposed local rules, but weak for asymptotic construction discovery.
- Risk: Compact routing is active and lower-bound statements may belong to adjacent oracle/spanner models.
- Next verification: Check the arXiv v3 full version for refinements beyond the DISC proceedings version.

## 17. `dynamic_min_tree_cut`

- Best use: Background or narrow trace-generation project.
- Problem: Maintain the minimum cut induced by any edge of a maintained spanning tree under dynamic graph updates.
- Why it matters: It is a subroutine-shaped handle on dynamic min-cut.
- AI fit: Moderate for adversarial update generation and invariant testing.
- Risk: Open status is not crisp and recent dynamic min-cut progress may change the frontier.
- Next verification: Read full 2025/2026 dynamic min-cut papers and isolate a standalone min-tree-cut statement.

## 18. `kinetic_high_dim_extent`

- Best use: Background/source-gathering.
- Problem: Maintain 3D kinetic diameter, width, hull, or related extent measures under algebraic motion.
- Why it matters: Kinetic data structures connect geometry, motion planning, and continuously changing data.
- AI fit: Moderate for symbolic instance generation and event-schedule experiments.
- Risk: The current candidate is too broad and lacks line-level primary verification.
- Next verification: Choose one 3D measure and verify exact open status in primary KDS sources.

## 19. `dynamic_text_indexing`

- Best use: Background/source-gathering.
- Problem: Maintain a compact dynamic text index under substring updates with near-output-sensitive pattern search.
- Why it matters: Dynamic compressed indexing is central to mutable string data structures.
- AI fit: Good for toy correctness oracles, weak for the asymptotic bit-space gap.
- Risk: The 2007 open statement is stale without reconciling later dynamic self-index work.
- Next verification: Use the final ACM/TALG source and later dynamic compressed-index papers.

## 20. `concurrent_shi_cell_capacity`

- Best use: Model extraction, formalization, and tiny-state checking.
- Problem: Pin down residual progress/cell-capacity boundaries for strongly history-independent concurrent dictionaries after the STOC 2025 hash-table result.
- Why it matters: It links privacy of memory representations with concurrent dictionary correctness.
- AI fit: Good for small linearizability/SQHI model checking after the exact theorem statements are extracted.
- Risk: The Batch 003 one-key-versus-two-key residual was likely misstated, and the open status is inferred rather than explicit.
- Next verification: Read the full STOC 2025 lower-bound theorem and restate the residual in terms of progress condition, base object, and cell capacity.
