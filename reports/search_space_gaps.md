# Search Space Gaps

Date: 2026-05-15

This file records underexplored scouting territory after Batches 001 and 002. It is not a list of promoted candidates. The goal is to guide a targeted Batch 003 without re-running the same dynamic-optimality-heavy search.

## Summary

The current repo is strongest on self-adjusting heaps/BST-adjacent problems, a few hashing/string/range-query leads, and the new STT LP candidate. It is weaker on geometry, streaming/sketching, succinct indexes beyond two bundled Dagstuhl questions, concurrency, distributed/network data structures, and clean lower-bound mini-frontiers.

Recommended next scouting pass: **Batch 003: underexplored mini-frontiers**. It should produce fewer candidates than the first two batches, but each should have a sharper source trail and an explicit evaluator/formalization story if possible.

## Dynamic And Online Geometric Structures

Current coverage:

- `kinetic_high_dim_extent` is broad and not line-level verified.
- `geometric_data_structures` is still a placeholder.

Gaps:

- Dynamic geometric range searching, dynamic planar point location, dynamic nearest neighbor under restricted models, kinetic proximity structures, connected-segment intersection reporting, and polyline/trajectory data structures have not been saturated.
- The repo has not separated static geometric reporting, dynamic geometry, kinetic geometry, and online geometric maintenance.

Batch 003 task:

- Choose two or three narrow geometry sources with explicit open questions and exact asymptotic targets. Prefer one dynamic/online query problem and one kinetic event-complexity problem.

## Streaming And Sketching Data Structures

Current coverage:

- Dynamic-stream min-cut appears only inside `dynamic_graph_structures` notes.

Gaps:

- Turnstile sketches, streaming graph sparsifiers, dynamic-stream cut/connectivity/matching, sliding-window sketches, and succinct streaming dictionaries have not been systematically checked.
- The repo has not decided when streaming lower-bound problems are close enough to data-structure theory for promotion.

Batch 003 task:

- Scout explicit open questions with finite communication games, small sketch lower-bound gadgets, or certificate-checking angles.

## Succinct Indexes And Compressed Data Structures

Current coverage:

- `succinct_compressed_structures` bundles LZ indexing and grammar/DAG random access.
- `dynamic_text_indexing` is stale until later compressed self-index work is reconciled.

Gaps:

- Succinct trees/graphs, compressed rank/select variants, dynamic succinct structures, document retrieval indexes, grammar/LZ/RLBWT distinctions, and lower-order-space overhead questions are underexplored.
- The repo needs separate candidates for LZ, grammar/DAG, dynamic text, and compressed graph indexes.

Batch 003 task:

- Split the current bundled succinct folder after recovering exact notation, then scout one non-string succinct structure problem.

## Lower-Bound And Cell-Probe Mini-Frontiers

Current coverage:

- `range_mode_queries` has cell-probe context.
- `retroactive_data_structures` is an inferred lower-bound lane.
- Dynamic-stream min-cut is noted but not promoted.

Gaps:

- No systematic pass over small explicit cell-probe gaps, chronogram variants, range-query lower bounds, predecessor/dictionary residuals, or data-structure lower bounds with finite certificate analogues.

Batch 003 task:

- Search for open lower-bound problems where the candidate can name a model, operation set, known upper/lower bounds, and a plausible finite hard-instance generator.

## Concurrency And Lock-Free Data Structures

Current coverage:

- History-independent concurrent hashing appears only as a cautionary note under `history_independent_data_structures`.

Gaps:

- Lock-free/wait-free dictionaries, queues, memory reclamation, concurrent hashing, linearizability plus privacy, and contention-sensitive data structures have not been scouted.
- Many concurrency questions may be too systems-flavored; the repo needs a filter for theory-facing model clarity.

Batch 003 task:

- Look for one or two explicit theoretical open questions with model-checkable small executions or proof-assistant-friendly invariants.

## Distributed And Network Data Structures

Current coverage:

- `self_adjusting_networks` is a placeholder.

Gaps:

- Distributed dictionaries, compact routing, self-adjusting networks, skip-graph variants, distributed hash tables with theory guarantees, network decomposition data structures, and dynamic distributed graph maintenance are mostly absent.

Batch 003 task:

- Decide whether this area belongs in scope. If yes, focus on self-adjusting networks or compact routing where the data-structure analogy is strongest.

## Dynamic Graph Subareas

Current coverage:

- Incremental topological ordering, dynamic connectivity simplification, dynamic min-tree-cut, and streaming min-cut notes.

Gaps:

- Dynamic reachability/transitive closure, dynamic matching, dynamic spanners/sparsifiers, dynamic arboricity/orientation, dynamic shortest paths under restrictions, dynamic planar graphs, and decremental/incremental model-specific residuals are not saturated.

Batch 003 task:

- Avoid broad "dynamic graph" promotion. Select subroutine-shaped candidates with explicit open status and one exact maintained object.

## Cache-Oblivious And External-Memory Subareas

Current coverage:

- `lazy_b_trees` is strong but narrow.
- `external_memory_structures` is broad context.

Gaps:

- Cache-oblivious dictionaries, buffer trees, packed memory arrays, I/O lower bounds for update/query tradeoffs, simultaneous RAM/I/O optimality, external-memory hashing, and external-memory range reporting need targeted scouting.

Batch 003 task:

- Separate cache-aware, cache-oblivious, external-memory, and database-indexing models. Look for explicit work/I/O tradeoff questions with primary sources.

## Hashing And Dictionaries

Current coverage:

- `quadratic_probing` is strong.
- `hashing_dictionaries` is vague after audit.

Gaps:

- Cuckoo/Robin Hood/resizable/stable/succinct/hash-table tradeoffs beyond quadratic probing have not been cleanly extracted.
- The repo has not found a residual all-purpose hashing theorem that survives recent solution papers.

Batch 003 task:

- Read modern hashing solution papers specifically for "future work" or residual theorem statements, not broad motivation.

## Persistence, Retroactivity, And Temporal Data Structures

Current coverage:

- `persistent_arrays` is likely solved as stated.
- `retroactive_data_structures` lacks an explicit residual.

Gaps:

- Partial/full/confluent persistence, retroactivity transformations, retroactive lower bounds, versioned dictionaries, and rollback/undo data structures have not been systematically separated.

Batch 003 task:

- Treat temporal data structures as a model taxonomy first. Promote only a named residual open problem with a primary source.

## Online And Adaptive Structures Beyond BSTs

Current coverage:

- `list_update`, `pairing_heaps`, `unified_bound_heaps`, `splay_preorder_231`, and `imprecise_comparison_sorting`.

Gaps:

- Adaptive priority queues beyond working-set/decrease-key, online set cover-like data structures, adaptive sorting under partial orders, self-organizing dictionaries, and locality-sensitive online structures have not been broadly checked.

Batch 003 task:

- Scout one non-BST, non-heap online/adaptive structure with a crisp evaluator such as an exact offline optimum or minimax game.

## Formalization And Certificate-Checking Infrastructure

Current coverage:

- The repo has identified likely certificate candidates but has no formal checker infrastructure yet.

Gaps:

- No Lean/Isabelle target has been selected.
- No standard certificate format exists for LP witnesses, finite games, heap potential inequalities, range-query hard arrays, or Karp-Rabin collisions.

Batch 003 task:

- Alongside scouting, define a minimal certificate schema for `search_trees_on_trees_lp`; this can become the template for later candidates.
