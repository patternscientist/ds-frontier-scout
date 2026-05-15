# Search Space Gaps

Date: 2026-05-15

Status: post-Batch-003 and post-Batch-003 adversarial audit. This file now distinguishes later scouting lanes from areas that are covered enough for the first pilot. It should not trigger another broad scouting batch before the `search_trees_on_trees_lp` pilot.

## Summary

The repository is now saturated enough to begin the first pilot. Batches 001 and 002 found the main evaluator-friendly cluster, and Batch 003 checked the largest missing areas: streaming/sketching, geometry, concurrency/history independence, distributed/network data structures, and cache-oblivious/external-memory structures. Batch 003 produced useful second-wave candidates but did not dislodge STT LP.

Recommended action: **begin the STT LP pilot now**. Keep the gaps below as later scouting lanes or background checks, not as blockers.

## Gaps Covered Enough For The First Pilot

### STT / Certificate Infrastructure

- `search_trees_on_trees_lp` is covered enough to start: it has explicit open status, a concrete LP/counterexample source, exact finite artifacts, and a draft certificate schema.
- Remaining work is implementation, not scouting: fix checker-blocking schema details, validate STT enumeration/costs, and reproduce small certificates.

### Streaming And Sketching

- Batch 003 promoted `dynamic_stream_mincut_space` from an earlier note into a source-backed candidate.
- The area is covered enough for pilot selection because the best lead is explicit but lower-bound-heavy and weaker than STT LP as an evaluator project.
- Later scouting should read the full ITCS 2025 version and search for follow-ups, but this is not a pilot blocker.

### Geometry

- Batch 003 promoted `connected_circle_segment_queries` as the sharpest geometry lead.
- Dynamic geometry and kinetic structures remain broad, but the repository now has one concrete connected-geometry data-structure problem with a primary source.
- Later work should isolate a lower-bound family; the first pilot does not need more geometry scouting.

### Distributed / Network Data Structures

- Batch 003 promoted `directed_roundtrip_compact_routing`.
- This establishes that compact routing belongs in scope as a data-structure-adjacent lane, but the audit found high saturation and weak OpenEvolve fit.
- No further network scouting is needed before the STT pilot.

### Concurrency And History Independence

- Batch 003 promoted and then sharply downgraded `concurrent_shi_cell_capacity`.
- The area is covered enough for first-pilot selection: there is a strong source, but the residual is fragile and must be model-extracted before any theorem prompt.
- Later work should focus on formal model extraction, not broad concurrency scouting.

### Cache-Oblivious And External Memory

- `lazy_b_trees` and `cache_oblivious_implicit_scanning` now cover the most promising external-memory/cache-oblivious lanes.
- The strict implicit scan problem is interesting but modern-status uncertain; `lazy_b_trees` is explicit but definition-heavy.
- This is enough coverage to defer further cache/external scouting until after the STT pilot starts.

## Gaps Still Worth Scouting Later

### STT Source And Certificate Details

- Verify Golinsky's original LP source and any post-2025 citations of Sadeh-Kaplan-Zwick.
- Fix the exact `almost-star` convention or avoid the label in proof-mode certificates.
- Extract a versioned Golinsky LP constraint set before implementing LP proof-mode checks.

### Strict Implicit Cache-Oblivious Scans

- Check whether later implicit cache-oblivious dictionaries support exact `n`-cell range scans.
- Keep exact `n` cells plus `O(1)` registers separate from `(1+epsilon)n` layouts, PMAs, cache-oblivious B-trees, and pointerless non-implicit structures.

### Dynamic-Stream Min-Cut Space

- Read the full ITCS 2025/arXiv version around Open Question 15.
- Preserve distinctions between insertion-only and turnstile streams, min-cut value and cut sparsifiers, simple weighted graphs and multigraphs, randomized and deterministic algorithms.

### Connected Circle-Segment Lower Bounds

- Recover exact formulas from the ISAAC 2025 PDF/source, not only the HTML rendering.
- Separate lower bounds for all data structures from lower bounds against the 2025 edge-partition-tree technique.

### Directed Roundtrip Routing

- Check arXiv v3 and later citations for the general `k` directed weighted compact-routing tradeoff.
- Keep routing schemes distinct from distance oracles, labels, spanners, emulators, and conditional girth-style lower bounds.

### Range Mode And Imprecise Comparisons

- `range_mode_queries` needs a modern static exact range-mode frontier check.
- `imprecise_comparison_sorting` needs a post-2015 sweep separating imprecise comparisons from noisy comparisons and tournament models.
- Both remain strong second-wave evaluator candidates, but neither blocks the STT pilot.

### Succinct / Compressed Structures

- Split `succinct_compressed_structures` into LZ indexing and grammar/DAG length-sampling before promotion.
- Check newer grammar-random-access work before claiming that the old Dagstuhl grammar gap remains open.

## Gaps Now Deprioritized

### Broad Dynamic Optimality And Splay Variants

- `splay_preorder_231` remains interesting only as a sharply defined initial-tree subproblem.
- Broad dynamic optimality, traversal, Greedy, and fixed-pattern-avoidance scouting is too saturated for the first pilot.

### Broad Dynamic Graph Maintenance

- `dynamic_graph_structures` is background because the incremental topological-ordering target was stale as stated.
- `dynamic_min_tree_cut` is plausible but too active and too weakly sourced as a standalone current gap.

### Persistent Arrays

- `persistent_arrays` is likely solved as stated by the Straka source.
- Keep only as proof archaeology/formalization unless a stricter residual model is sourced.

### History-Independent Allocation

- `history_independent_allocation` is stale after modern strongly history-independent storage-allocation work.
- Later scouting should extract residual tradeoffs from the 2023 paper rather than replay Naor-Teague's 2001 formulation.

### Broad Dynamic Text Indexing

- `dynamic_text_indexing` is background until the 2007 linear-bit question is reconciled with later dynamic compressed self-index work.
- Toy evaluators test correctness, not the bit-space theorem gap.

### Broad Hashing Residuals

- `hashing_dictionaries` remains too vague after All-Purpose Hashing and follow-up tradeoff work.
- `quadratic_probing` is the concrete hashing candidate; broad residual extraction can wait.

### Retroactivity And Temporal Data Structures

- `retroactive_data_structures` lacks an explicit residual open statement.
- Promote only after a primary source names a problem/model/lower-bound gap.

### Kinetic High-Dimensional Extent

- `kinetic_high_dim_extent` is still too broad and line-level source fragile.
- Later scouting should pick one measure such as 3D kinetic diameter or width.

## Pilot Boundary

Further scouting is not required before the first pilot. The next useful work is to turn `reports/stt_lp_certificate_schema.md` into a minimal checker and to run the first blind theorem attempt against edge-diameter-3 depth-projection integrality.
