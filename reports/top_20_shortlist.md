# Top 20 Shortlist

Date: 2026-05-15

This is a ranked scouting shortlist, not a claim that every item is promotion-ready. Items near the bottom are retained as background or residual-search lanes because their current open status is uncertain.

## 1. `search_trees_on_trees_lp`

- Best use: OpenEvolve project and narrow theorem project.
- Problem: Determine polynomial-time exact optimization and LP/integrality behavior for static search trees on tree topologies.
- Why it matters: STTs generalize optimal BSTs and expose a small, modern polyhedral data-structure frontier.
- Why niche: The active community is small and the problem lives between data structures and polyhedral optimization.
- AI fit: Excellent; exact STT enumeration, rational LP certificates, and subclass proof search all fit staged AI collaboration.
- Main risk: Small-case enumeration may not scale, and paths/stars must not be misstated as open exact-optimization cases.
- Next verification: Reproduce Sadeh-Kaplan-Zwick tables from the arXiv source and check post-v2 citations.

## 2. `quadratic_probing`

- Best use: OpenEvolve-first probabilistic-combinatorics project.
- Problem: Improve the load-factor/model frontier for constant expected insertion time in quadratic probing.
- Why it matters: A simple practical hash-table scheme still has surprisingly delicate theory.
- Why niche: It looks elementary but the dependencies in probe sequences are technically awkward.
- AI fit: Strong for witness-configuration search, threshold experiments, and proof-certificate scaffolding.
- Main risk: The old "prove anything" gap is solved; remaining targets may be narrow constant improvement.
- Next verification: Extract exact ICALP 2024 theorem statements and stated open directions.

## 3. `imprecise_comparison_sorting`

- Best use: OpenEvolve project with theorem sidecar.
- Problem: Decide whether randomized error-2 maximum finding under adversarial imprecise comparisons can use `O(n)` comparisons.
- Why it matters: It is a crisp adaptive-sorting/partial-information problem with finite game structure.
- Why niche: It sits just outside mainstream data structures and is easy to overlook as a sorting-model corner.
- AI fit: Excellent for randomized strategy synthesis, adversary LPs, and certificate checking.
- Main risk: A follow-up under noisy, uncertain, tournament, or interval-order terminology may already close the exact model.
- Next verification: Run a post-2015 citation sweep separating model assumptions.

## 4. `range_mode_queries`

- Best use: OpenEvolve project with lower-bound/theorem sidecar.
- Problem: Determine the optimal query time for exact static range mode using linear or near-linear space.
- Why it matters: Range mode is a canonical hard range-query problem where idempotent tricks fail.
- Why niche: Exact mode is narrower and less glamorous than broader range searching or approximate majority.
- AI fit: Strong for hard-array generation and candidate-list/block-decomposition stress tests.
- Main risk: The current `O(sqrt n)` blind baseline is stale and modern upper/lower bounds need verification.
- Next verification: Check final Chan-Durocher-Larsen-Morrison-Wilkinson and post-2012 range-mode papers.

## 5. `karp_rabin_collision_detection`

- Best use: OpenEvolve project plus crisp theorem project.
- Problem: Detect whether a fixed string and prime modulus induce equal-length Karp-Rabin fingerprint collisions faster than quadratic time.
- Why it matters: Collision certification matters for randomized string algorithms and string data structures.
- Why niche: It is a technical fingerprinting subroutine rather than a flagship stringology problem.
- AI fit: Strong; small strings and moduli give exact brute-force oracles and adversarial instances.
- Main risk: Deterministic exact detection and randomized false rejection are different problem variants.
- Next verification: Locate full Dagstuhl notes/slides and search for alternate stringology terminology.

## 6. `list_update`

- Best use: OpenEvolve project.
- Problem: Close the `1.5` to `1.6` randomized competitive-ratio gap for classical online list update.
- Why it matters: List update is a canonical self-organizing online data-structure problem.
- Why niche: The gap is old, small, and unfashionable rather than broadly active.
- AI fit: Strong for finite-state policies, adversarial sequences, and LP/game lower bounds.
- Main risk: Finite-state improvements may not generalize to arbitrary list size.
- Next verification: Check post-2012 online algorithms and advice/variant literature for ratio updates.

## 7. `pairing_heaps`

- Best use: OpenEvolve potential/counterexample mining.
- Problem: Determine the exact amortized decrease-key complexity of the standard two-pass pairing heap.
- Why it matters: Pairing heaps are simple, practical, and still analytically unresolved.
- Why niche: Famous within heap theory but narrow and technically stubborn.
- AI fit: Excellent for exact simulation, adversarial traces, and potential-inequality search.
- Main risk: The problem has resisted specialists for decades and small traces may underfit amortized behavior.
- Next verification: Check later standard-pairing-heap analyses and keep variants separate.

## 8. `unified_bound_heaps`

- Best use: Theorem project.
- Problem: Build a pointer-model heap with constant-time decrease-key and working-set-style extract-min bounds.
- Why it matters: It would connect adaptive priority queues with graph-algorithm-friendly decrease-key.
- Why niche: The open version is a narrow pointer-model heap-adaptivity question.
- AI fit: Good for candidate structures and amortized potential exploration after definitions are fixed.
- Main risk: Broad non-pointer formulations are ambiguous after recent Dijkstra working-set heap work.
- Next verification: Read Iacono's exact Dagstuhl statement and the Dijkstra universal-optimality heap papers.

## 9. `lazy_b_trees`

- Best use: Theorem project.
- Problem: Construct an external-memory biased search tree with linear block space and weighted-search I/O guarantees.
- Why it matters: It could remove a key obstacle in lazy B-trees and adaptive external-memory dictionaries.
- Why niche: It is very recent and technical, between database-style B-trees and biased search theory.
- AI fit: Good for design-space pruning and local lemma search.
- Main risk: "Fully satisfactory" must be turned into a precise theorem before proof attempts.
- Next verification: Extract exact target operations and bounds from the MFCS 2025 full version.

## 10. `path_compression_topdown`

- Best use: Lean/formalization and staged proof project.
- Problem: Give a simple direct inverse-Ackermann proof from the Seidel-Sharir top-down path-compression recurrence.
- Why it matters: It could clarify a foundational union-find analysis.
- Why niche: It is proof archaeology/pedagogy, not a new data-structure bound.
- AI fit: Excellent once the recurrence is exact.
- Main risk: A clean proof may already exist in lecture notes or unpublished material.
- Next verification: Copy the exact recurrence and Ackermann normalization from Seidel-Sharir/Tarjan sources.

## 11. `succinct_compressed_structures`

- Best use: Theorem project after splitting; grammar-DAG side may become OpenEvolve.
- Problem: Improve LZ compressed indexing or remove expansion-length overhead in grammar-compressed random access.
- Why it matters: Compact random access and compressed indexes are core succinct/string data-structure tools.
- Why niche: The relevant open questions are small technical subproblems inside a large literature.
- AI fit: Good for grammar/DAG sampling schemes and small counterexample generators.
- Main risk: The folder bundles two distinct problems and the Dagstuhl HTML omits crucial notation.
- Next verification: Recover exact PDF/slides notation and split LZ from grammar/DAG.

## 12. `splay_preorder_231`

- Best use: Background context or narrow theorem/evaluator probe.
- Problem: Prove or refute restricted Splay traversal bounds on preorder/231-avoiding access sequences under a precise initial-tree regime.
- Why it matters: It tests narrow pieces of the dynamic-optimality landscape.
- Why niche: Only the sharply restricted initial-tree corner qualifies; broad dynamic optimality is saturated.
- AI fit: Good for exact Splay simulation, Catalan generators, and candidate invariant falsification.
- Main risk: Severe saturation and many nearby Splay/Greedy/offline-OPT results already narrow the target.
- Next verification: Check post-2025 follow-ups for arbitrary-initial-tree Splay preorder.

## 13. `dynamic_min_tree_cut`

- Best use: Background or narrow trace-generation project.
- Problem: Maintain the minimum cut induced by any edge of a maintained spanning tree under dynamic graph updates.
- Why it matters: It is a subroutine-shaped handle on dynamic min-cut.
- Why niche: The subroutine may be under-attended even though dynamic min-cut is active.
- AI fit: Moderate for adversarial update generation and invariant testing.
- Main risk: Open status is not crisp and recent dynamic min-cut progress may change the frontier.
- Next verification: Read full 2025/2026 dynamic min-cut papers and isolate a standalone min-tree-cut statement.

## 14. `kinetic_high_dim_extent`

- Best use: Background/source-gathering.
- Problem: Maintain 3D kinetic diameter, width, hull, or related extent measures under algebraic motion.
- Why it matters: Kinetic data structures connect geometry, motion planning, and continuously changing data.
- Why niche: Kinetic geometry is specialized and old open questions are fragmented.
- AI fit: Moderate for symbolic instance generation and event-schedule experiments.
- Main risk: The current candidate is too broad and lacks line-level primary verification.
- Next verification: Choose one 3D measure and verify exact open status in primary KDS sources.

## 15. `dynamic_text_indexing`

- Best use: Background/source-gathering.
- Problem: Maintain a compact dynamic text index under substring updates with near-output-sensitive pattern search.
- Why it matters: Dynamic compressed indexing is central to mutable string data structures.
- Why niche: The exact bit-space/update model is specialized and easy to conflate with nearby compressed-index results.
- AI fit: Good for toy correctness oracles and literature triage, weak for the asymptotic bit-space gap.
- Main risk: The 2007 open statement is stale without reconciling later dynamic self-index work.
- Next verification: Use the final ACM/TALG source and later dynamic compressed-index papers.

## 16. `external_memory_structures`

- Best use: Background for lazy B-trees and work/I/O scouting.
- Problem: Isolate precise external-memory priority-queue or simultaneous work/I/O tradeoff questions after known lower bounds.
- Why it matters: External-memory bounds shape large-scale dictionaries and priority queues.
- Why niche: The remaining questions are model-sensitive and not yet one clean theorem.
- AI fit: Useful for narrowing and comparing lower-bound models.
- Main risk: The classic DecreaseKey question is already answered; broad formulations are misleading.
- Next verification: Separate priority queues, biased search, cache-oblivious structures, and simultaneous work/I/O targets.

## 17. `dynamic_graph_structures`

- Best use: Background context.
- Problem: Recover precise residuals around dynamic connectivity level elimination, incremental topological ordering, and dynamic-stream min-cut.
- Why it matters: Dynamic graph primitives are foundational.
- Why niche: Only narrow simplification/lower-bound subquestions qualify; the broad area is saturated.
- AI fit: Moderate for invariant and adversarial update exploration.
- Main risk: The topological-sort target is already achieved randomized as stated.
- Next verification: Recover Fineman's exact missing expression and check batch-dynamic connectivity follow-ups.

## 18. `history_independent_data_structures`

- Best use: Background or formal-model scouting.
- Problem: Find a precise open theorem about history-independent priority queues or residual concurrent dictionaries.
- Why it matters: History independence links data structures with privacy of memory representations.
- Why niche: The community is small and model choices are subtle.
- AI fit: Moderate for tiny-state representation-equivalence checks.
- Main risk: Current sources record a question cluster, not a theorem target; concurrent hashing is already partially resolved.
- Next verification: Locate formal Conway/Kuszmaul heap sources or residual cell-capacity/progress-condition gaps.

## 19. `retroactive_data_structures`

- Best use: Background/source-gathering.
- Problem: Identify an explicit residual lower-bound strengthening for retroactive data structures.
- Why it matters: Retroactivity explains when editing past updates is inherently expensive.
- Why niche: The literature is small and lower-bound-focused.
- AI fit: Moderate for explicit hard sequence search after a model is fixed.
- Main risk: The open target is inferred, not explicitly sourced, and may require fine-grained assumptions.
- Next verification: Find a named problem/model where the residual is stated as open in a primary source.

## 20. `hashing_dictionaries`

- Best use: Background/residual extraction.
- Problem: Extract one precise unsolved dynamic hashing tradeoff after All-Purpose Hashing and related time/space work.
- Why it matters: Hash-table space/time/stability tradeoffs are fundamental.
- Why niche: Only a model-specific residual would be under-attended; broad hashing is active.
- AI fit: Moderate for simulations, weak for high-probability/succinct-space proofs until a theorem is fixed.
- Main risk: "All properties at once" was historical motivation, not a current open claim.
- Next verification: Read the all-purpose and optimal time/space tradeoff papers for explicit residual statements.
