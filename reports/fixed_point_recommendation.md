# Fixed-Point Recommendation: Post-Batch-003

Date: 2026-05-15

Scope: final cross-batch synthesis after Batch 003 and its adversarial audit, using the Batch 001, Batch 002, and Batch 003 reports, all current candidate folders, the score matrix, the open-problem source log, and the STT LP certificate schema.

## Executive Summary

The recommendation is **stable enough to stop broad scouting and begin the first pilot**. This does not mean the whole research map is closed; it means the first-pilot decision has reached a fixed point. Batch 003 added useful mini-frontiers, but its adversarial audit downgraded their evaluator readiness and did not produce a candidate with the same combined source strength, theorem texture, finite certificate path, and implementation surface as `search_trees_on_trees_lp`.

Final pilot recommendation: begin a two-track `search_trees_on_trees_lp` pilot now. Do not run another scouting batch before the pilot. Keep later scouting as a side queue for strict implicit cache-oblivious scans, dynamic-stream min-cut space, connected circle-segment lower bounds, and directed roundtrip routing.

## Required Judgments

1. Does any Batch 003 candidate dislodge `search_trees_on_trees_lp`?
   No. The strongest Batch 003 survivor is `dynamic_stream_mincut_space`, but it is a lower-bound-heavy streaming problem with only hypothesis-generating finite evaluators. `cache_oblivious_implicit_scanning`, `connected_circle_segment_queries`, and `directed_roundtrip_compact_routing` are real leads but not as checker-ready. `concurrent_shi_cell_capacity` was downgraded because the residual was inferred and likely misstated.

2. Are the recommendations unstable, partially stable, or stable?
   Stable for the first pilot. Partially stable for the long-term ordering after the top cluster, because several second-wave candidates still need modern-status checks or model extraction.

3. Should we run more scouting, or begin the pilot?
   Begin the pilot. The search space is saturated enough for a first serious project, and another broad batch would mostly refine second-wave rankings.

4. What exactly is the first theorem target?
   Determine whether the depth-space projection of the versioned Golinsky STT LP equals the convex hull of STT depth vectors for every base tree whose edge-diameter is at most 3. Equivalently for the pilot: prove this subclass projection-integrality statement, or produce a minimal exact rational counterexample. Paths and stars are baselines, not open exact-optimization cases.

5. What exactly is the first computational/certificate/OpenEvolve target?
   Build a proof-mode STT certificate/checker scaffold that can validate topology, weights, recursive STTs, depths, exact costs, subclass labels, and complete small-`n` STT enumeration, then reproduce a Sadeh-Kaplan-Zwick-style small certificate such as the 7-node long-star data before searching edge-diameter-3 topologies for fractional depth-space behavior.

6. What are the checker-blocking clarifications in `stt_lp_certificate_schema.md`?
   The checker needs a schema/checker version and exact `relaxation_version`; explicit variable domains for `X`, `Z`, and `D`, including symmetry and absent-variable defaults; a machine-implemented LP constraint set; machine-readable root-rounding formulas; proof-mode enumeration or dual certificates rather than trusted digests; and a fixed convention for `almost-star`, which is currently advisory.

7. What should the first no-internet blind prompt be?
   Use the STT prompt in the pilot plan, centered on edge-diameter-3 depth-projection integrality. It must define STTs recursively, depth-based cost, paths/stars as sanity checks, and the target as either a proof or a counterexample without mentioning Sadeh-Kaplan-Zwick, Golinsky, or known counterexamples.

8. What should the first Codex implementation prompt be?
   Use the implementation prompt in the pilot plan: implement the STT LP certificate/checker scaffold, but do not guess Golinsky constraints until `relaxation_version` and variable domains are pinned down. The first accepted scope is exact rational parsing, topology validation, STT recursion/enumeration, cost checking, subclass-label derivation, JSON normalization, and tests.

## Final Top Theorem-Project Candidates

1. `search_trees_on_trees_lp` - First theorem pilot; explicit open status, narrow subclass targets, and a certificate path.
2. `unified_bound_heaps` - Strong theorem texture only in the pointer-model working-set/decrease-key formulation.
3. `lazy_b_trees` - Explicit recent external-memory biased-search-tree gap; needs exact operation/bound extraction.
4. `karp_rabin_collision_detection` - Crisp theorem target with exact finite instances; keep deterministic detection and randomized false rejection separate.
5. `imprecise_comparison_sorting` - Excellent finite-combinatorial theorem/evaluator target, but modern status is only medium confidence.
6. `range_mode_queries` - Good theorem sidecar after the current exact linear-space upper/lower frontier is verified.
7. `cache_oblivious_implicit_scanning` - Interesting strict-implicit theorem target, but old-source modern status is uncertain.
8. `dynamic_stream_mincut_space` - Explicit open lower-bound problem; theorem-heavy and only adjacent to classic data structures.
9. `path_compression_topdown` - Excellent proof-simplification/formalization target, not a new data-structure theorem.
10. `connected_circle_segment_queries` - Explicit geometry lead; lower-bound/tradeoff side is cleaner than construction-improvement suggestions.

## Final Top OpenEvolve / Evaluator Candidates

1. `search_trees_on_trees_lp` - Exact enumeration, rational LP certificates, depth-vector checks, and subclass search.
2. `quadratic_probing` - Witness-configuration and threshold search beyond the ICALP 2024 positive regime.
3. `imprecise_comparison_sorting` - Randomized finite games, adversary LPs, and certificate checking.
4. `range_mode_queries` - Exact small-array oracles and hard-array generation for block/candidate-list schemes.
5. `list_update` - Offline optimum, adversarial request sequences, finite-state policies, and LP/game lower bounds.
6. `karp_rabin_collision_detection` - Exact brute-force collision oracle and candidate algorithm benchmarking.
7. `pairing_heaps` - Potential-function and adversarial-trace search for the standard two-pass heap.
8. `connected_circle_segment_queries` - Connected geometric instance generation and partition-tree stress tests.
9. `dynamic_stream_mincut_space` - Toy hard distributions only; not proof evidence for the asymptotic lower bound.
10. `succinct_compressed_structures` - Potentially useful on the grammar/DAG side after the bundled problem is split.

## Final Top Lean / Formalization / Certificate Candidates

1. `search_trees_on_trees_lp` - Best immediate certificate project: exact rationals, topology/STT validation, LP witness checking after schema clarifications.
2. `path_compression_topdown` - Best pure proof-formalization target once the exact recurrence is recovered.
3. `imprecise_comparison_sorting` - Finite adversary LPs and randomized-strategy certificates.
4. `list_update` - Game/LP certificates for finite list sizes and policy classes.
5. `karp_rabin_collision_detection` - Certified substring-hash collision oracle.
6. `range_mode_queries` - Hard-array and candidate-list failure certificates for restricted frameworks.
7. `pairing_heaps` - Exact small heap-state potential-inequality checking.
8. `concurrent_shi_cell_capacity` - Model extraction and tiny-history linearizability/SQHI checking, not theorem hunting yet.
9. `cache_oblivious_implicit_scanning` - Layout and cache-miss checker only after strict implicit model validation.
10. `connected_circle_segment_queries` - Certified geometric intersection oracle for finite stress tests.

## Batch 003 Implication

Batch 003 covered the major previously underexplored areas well enough for a first pilot:

- Streaming/sketching produced `dynamic_stream_mincut_space`, explicit but not evaluator-first.
- Distributed/network data structures produced `directed_roundtrip_compact_routing`, explicit but active and weak for OpenEvolve.
- Concurrency/history independence produced `concurrent_shi_cell_capacity`, but the audit found the residual fragile.
- Geometry produced `connected_circle_segment_queries`, useful but lower-bound/model-sensitive.
- Cache-oblivious/external-memory scouting produced `cache_oblivious_implicit_scanning`, promising only under the exact `n`-cell implicit model.

These are good second-wave leads. None beats STT LP for a first integrated theorem/certificate/OpenEvolve pilot.

## Final Recommendation

Freeze broad scouting and start the `search_trees_on_trees_lp` pilot. The first week should produce a checker scaffold and at least one exact checked STT certificate, not a claimed new theorem. The first theorem attempt should target edge-diameter-3 depth-projection integrality, with failure treated as a useful counterexample/certificate outcome.
