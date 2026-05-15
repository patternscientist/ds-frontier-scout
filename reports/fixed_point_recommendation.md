# Fixed-Point Recommendation

Date: 2026-05-15

Scope: cross-batch synthesis of Batch 001, Batch 001 adversarial audit, Batch 002 non-Dagstuhl saturation, Batch 002 adversarial audit, the score matrix, source log, and all current candidate folders.

## Executive Summary

The recommendations are **partially stable**. The evaluator-driven cluster has stabilized enough to start a pilot project; the theorem-only cluster is still less stable because several attractive statements need source recovery, exact model choices, or post-2025 citation checks.

The strongest fixed-point recommendation is `search_trees_on_trees_lp`. It rose after audit because it has an explicit current open problem, a narrow specialist community, reproducible computational artifacts, exact finite certificates, and a plausible staged theorem workflow. It should be the first OpenEvolve/certificate project and also the first theorem-side pilot, but only on a narrow subproblem such as edge-diameter-3 / almost-star LP integrality or depth-space projection integrality.

The next most stable evaluator candidates are `quadratic_probing`, `imprecise_comparison_sorting`, `range_mode_queries`, `list_update`, `karp_rabin_collision_detection`, and `pairing_heaps`. These should not be collapsed into one score: they have different risks. Some are explicit but hard (`pairing_heaps`), some are source-current but model-narrowed (`quadratic_probing`), some are finite-combinatorial but modern-status uncertain (`imprecise_comparison_sorting`, `range_mode_queries`), and some have exact oracles but problem-statement nuance (`karp_rabin_collision_detection`).

The best theorem-only candidates after audit are `search_trees_on_trees_lp`, `unified_bound_heaps`, `lazy_b_trees`, and `path_compression_topdown`. Of these, `path_compression_topdown` is a proof-simplification/formalization project rather than a new data-structure theorem, and `unified_bound_heaps` must remain pointer-model-specific.

The largest downgrades are important: `persistent_arrays` and `history_independent_allocation` should be discarded as open theorem targets unless a stricter residual model is sourced. `dynamic_graph_structures`, `dynamic_min_tree_cut`, `dynamic_text_indexing`, `splay_preorder_231`, and `succinct_compressed_structures` remain useful context or narrow probes, but not top recommendations in their current form.

## Current Top 10 Theorem-Project Candidates

1. `search_trees_on_trees_lp` - Best theorem pilot. Attack a narrow STT LP/subclass theorem, not the full polynomial-time optimality problem first.
2. `unified_bound_heaps` - Strong theorem texture if kept to the pointer-model working-set/decrease-key formulation.
3. `lazy_b_trees` - Explicit recent external-memory biased-search-tree gap; good design/proof target after formalizing exact operations and bounds.
4. `path_compression_topdown` - Excellent staged proof project once the exact Seidel-Sharir recurrence and Ackermann normalization are copied into the prompt.
5. `karp_rabin_collision_detection` - Crisp statement and exact finite instances; theorem work must separate deterministic detection from randomized false rejection.
6. `imprecise_comparison_sorting` - Clean randomized finite-combinatorial theorem target, with modern-status uncertainty.
7. `range_mode_queries` - Good theorem sidecar to evaluator work; must update the linear-space upper-bound frontier before any claim.
8. `quadratic_probing` - Probabilistic theorem target after fixing the ICALP 2024 model and avoiding the stale "prove anything nontrivial" framing.
9. `succinct_compressed_structures` - Promising only after splitting LZ indexing from grammar/DAG length sampling and recovering missing notation.
10. `pairing_heaps` - Important but hard and saturated; use restricted potential lemmas rather than "final analysis" as the first theorem goal.

Near miss: `splay_preorder_231` has rich theorem texture, but the audit makes saturation risk severe. Promote only if the next step is a sharply defined initial-tree subcase not already covered by known Splay, Greedy, or offline-OPT results.

## Current Top 10 OpenEvolve Candidates

1. `search_trees_on_trees_lp` - Enumerate STTs/topologies, solve LPs exactly, reproduce known counterexamples, and generate certified subclass evidence.
2. `quadratic_probing` - Search witness configurations, thresholds, and model-specific obstruction families beyond the ICALP 2024 positive regime.
3. `imprecise_comparison_sorting` - Finite randomized games, adversary LPs, and certificate checking for error-2 maximum finding.
4. `range_mode_queries` - Exact small-array oracles and hard-array generation for block/candidate-list schemes.
5. `list_update` - Offline optimum, adversarial request sequences, randomized policy search, and LP/game lower-bound certificates.
6. `karp_rabin_collision_detection` - Exact brute-force collision oracle for strings/moduli, plus candidate algorithm benchmarking.
7. `pairing_heaps` - Potential-function and adversarial-trace search for the standard two-pass heap.
8. `succinct_compressed_structures` - Best on the grammar/DAG sampling side; LZ indexing needs exact notation first.
9. `splay_preorder_231` - Useful for counterexample and invariant mining, not as a direct dynamic-optimality solver.
10. `dynamic_min_tree_cut` - Trace-generation sandbox only after the exact maintained-tree model is fixed; high saturation risk.

## Current Top 10 Lean/Formalization/Certificate Candidates

1. `path_compression_topdown` - Formalize the recurrence-to-Ackermann comparison; best Lean-style proof target.
2. `search_trees_on_trees_lp` - Exact rational LP/STT enumeration certificates and checkable counterexample logs.
3. `imprecise_comparison_sorting` - Adversary LPs and randomized-strategy certificates for finite `n`.
4. `list_update` - Game/LP certificates for finite list sizes and policy classes.
5. `karp_rabin_collision_detection` - Certified substring-hash collision oracle and fixed-length/all-length distinction.
6. `range_mode_queries` - Checkable candidate-list failures and hard-array certificates for restricted frameworks.
7. `pairing_heaps` - Potential inequality checkers over exact small heap states.
8. `persistent_arrays` - Proof archaeology/formalization of Dietz/Straka-style known results, not an open-problem attack.
9. `succinct_compressed_structures` - Grammar/DAG sparse-sampling certificates after the formal problem is recovered.
10. `history_independent_data_structures` - Tiny-state distributional equivalence/model checking, but only after a precise model is sourced.

## Best Background/Context Candidates

- `splay_preorder_231` - Keep as background for dynamic-optimality-adjacent reasoning and Splay/Greedy/OPT distinctions; promote only a narrow initial-tree subproblem.
- `dynamic_min_tree_cut` - Keep as dynamic-graph subroutine context until recent min-cut papers are checked.
- `dynamic_graph_structures` - Keep for dynamic connectivity level-elimination and streaming min-cut notes, not for the stale topological-ordering target.
- `dynamic_text_indexing` - Keep as compressed-indexing context until the old linear-bit question is reconciled with modern dynamic self-indexes.
- `external_memory_structures` - Keep as context for `lazy_b_trees` and simultaneous work/I/O questions.
- `kinetic_high_dim_extent` - Keep as a geometry scouting lane, but narrow to one 3D measure before promotion.
- `history_independent_data_structures` - Keep for model taxonomy and formalization leads, not as a theorem target yet.
- `retroactive_data_structures` and `hashing_dictionaries` - Keep only as residual-extraction lanes.

## Stable Across Batches

- `quadratic_probing` remains high-value after audit, but its claim has narrowed from historical openness to load-factor/model improvement.
- `pairing_heaps` remains a strong evaluator/counterexample target, while being too hard and well-known for a first theorem proof.
- `karp_rabin_collision_detection` remains explicit, concrete, and source-backed.
- `list_update` remains a good evaluator-first old-gap problem, with the caveat that finite-state results may not lift.
- `path_compression_topdown` remains stable as a proof/formalization project, not as a new DS theorem.
- `lazy_b_trees` remains a niche theorem candidate with an explicit recent source, but not an evaluator-first project.

## Rose Sharply

- `search_trees_on_trees_lp` rose the most. It has an explicit 2025 open problem, known baselines, known counterexamples, reproducible code, exact rational certificates, and a narrow LP/subclass attack surface.
- `imprecise_comparison_sorting` rose after adversarial audit because it survived as a finite-combinatorial evaluator target with an explicit open question, despite modern-status uncertainty.
- `range_mode_queries` rose as the cleanest Batch 002 range-query lead, because exact small-instance oracles are trivial and the linear-space exact-mode gap appears plausible.

## Downgraded Or Discarded

- `persistent_arrays` - Discard as an open theorem target unless a stricter residual model is found; Straka likely solves the stated target.
- `history_independent_allocation` - Discard as stated; FOCS 2023 storage-allocation work likely narrows or answers the Naor-Teague historical problem.
- `dynamic_graph_structures` - Downgraded because the incremental topological-ordering target is stale/misstated and the remaining dynamic-connectivity simplification is saturated.
- `dynamic_min_tree_cut` - Downgraded because the open status is plausible but not crisp, and dynamic min-cut is highly active after 2025/2026 progress.
- `dynamic_text_indexing` - Downgraded until dynamic compressed self-index literature is reconciled with the old linear-bit single-text question.
- `splay_preorder_231` - Downgraded because the surrounding dynamic-optimality/pattern-avoidance area is severe-saturation territory.
- `succinct_compressed_structures` - Held back because it bundles two different Dagstuhl questions and lacks exact notation.
- `hashing_dictionaries` and `retroactive_data_structures` - Background only until a single residual theorem is sourced.

## Unresolved Uncertainties

- `search_trees_on_trees_lp`: verify post-v2 citations after 2025-08-01, Golinsky's original LP source, and Berendsohn thesis context.
- `quadratic_probing`: extract exact ICALP 2024 theorems, assumptions, and stated remaining gaps.
- `imprecise_comparison_sorting`: separate imprecise comparisons from noisy/uncertain/tournament variants in post-2015 literature.
- `range_mode_queries`: verify the strongest current static exact range-mode upper and lower bounds.
- `karp_rabin_collision_detection`: locate Dagstuhl slides/full notes and search stringology terminology for fixed-prime collision certification.
- `lazy_b_trees`: turn "fully satisfactory external biased search tree" into a precise theorem statement.
- `path_compression_topdown`: recover the exact recurrence before blind prompting.
- `succinct_compressed_structures`: split LZ and grammar/DAG problems and recover missing asymptotic notation.
- `dynamic_min_tree_cut`: read recent dynamic min-cut papers before treating min-tree-cut as current.

## Recommended Next Action

Start a **two-track pilot** rather than another broad recommendation pass:

1. OpenEvolve/certificate pilot: `search_trees_on_trees_lp`. Reproduce the Sadeh-Kaplan-Zwick LP/counterexample pipeline, then add certified search for edge-diameter-3 / almost-star LP integrality and depth-space projection behavior.
2. Theorem pilot: `search_trees_on_trees_lp` on the same narrow subclass. Use the staged workflow: blind STT subclass prompt, frontier document with LP/counterexamples, then literature mode.

In parallel, run a smaller **Scouting Batch 003: underexplored mini-frontiers** before freezing the long-term shortlist. Batch 003 should not revisit dynamic optimality. It should target gaps in dynamic/online geometry, streaming/sketching data structures, succinct indexes, lower-bound mini-frontiers, concurrency/history-independent residuals, distributed/network data structures, and cache-oblivious/external-memory subareas.
