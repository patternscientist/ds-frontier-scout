# Scouting Batch 001 Adversarial Audit

Date: 2026-05-15

Scope: Batch 001 plus Patch 001A/001B-style additions, especially `splay_preorder_231`, `search_trees_on_trees_lp`, `unified_bound_heaps`, `quadratic_probing`, `path_compression_topdown`, and `karp_rabin_collision_detection`.

Audit posture: disqualify first. A candidate survives only if the checked source gives a precise enough open target or if the remaining smallest subproblem is clearly useful.

## Executive Downgrades

1. `dynamic_graph_structures` is not a top candidate as written. The `~O(m^(4/3))` incremental topological ordering target is already achieved by Bhattacharya-Kulkarni for randomized expected total time. The only defensible residual target is deterministic/combinatorial simplification or a different density-regime guarantee.
2. `path_compression_topdown` is not a new data-structure theorem. It is a proof-simplification / exposition / possible Lean-formalization target. Keep only if we explicitly want proof archaeology.
3. `unified_bound_heaps` must be phrased as a pointer-model problem with a specific working-set definition. A broad "working-set heap with O(1) decrease-key" is misleading because recent beyond-worst-case heap work already gives a non-pointer-model heap with Fibonacci-like bounds and a working-set guarantee.
4. `quadratic_probing` remains promising, but the blind prompt must not imply the pre-2024 "prove anything nontrivial" gap remains. Kuszmaul-Xi prove constant expected time at load factor at least `0.089`; the remaining target is improving the load regime/model, not first correctness.
5. `splay_preorder_231` survives only as a narrow, saturation-aware Splay-vs-Greedy/initial-tree project. Offline OPT on fixed-pattern-avoiding sequences is now constant, and Greedy has several near/linear results under special initial models. Do not pitch this as under-attended dynamic optimality.

## Candidate-by-Candidate Audit

### quadratic_probing

- Open-problem claim: explicit for the historical pre-2024 gap, but the remaining gap is inferred from the partial nature of the ICALP 2024 theorem and Dagstuhl discussion.
- Newer work checked: Kuszmaul-Xi ICALP 2024 proves constant expected insertion time for all fixed-offset schemes at load factor `alpha >= 0.089`, and chunked schemes reach high-load regimes when block size grows.
- Saturation: low-to-medium. It is fresh and elementary-looking, but now visible after ICALP 2024.
- Smallest meaningful subproblem: reproduce the witness-string analysis and search for a certificate improving `0.089`, under the exact fixed-offset/full-random-hash model.
- Best use: OpenEvolve_project first; theorem_project second.
- Evaluator warning: simulations at finite table sizes may overstate high-load thresholds; use exact occupancy witnesses and model tags.
- Decision: remains top-tier, but patch prompt and score to avoid overstating the old open gap.

### unified_bound_heaps

- Open-problem claim: explicit only for pointer-model structures in Dagstuhl 25191.
- Newer/nearby work checked: Haeupler-Hladik-Rozhon-Tarjan-Tetek build a heap with a working-set bound and Fibonacci-like amortized bounds for Dijkstra universal optimality; this makes any non-pointer-model formulation look already addressed or at least ambiguous.
- Saturation: medium. Heap adaptivity is active after the Dijkstra work.
- Smallest meaningful subproblem: prove or disprove the pointer-model version for the "operations while item is present" age bound with `O(1)` amortized decrease-key.
- Best use: theorem_project. Not a clean OpenEvolve project without a formal pointer-machine model and lower-bound oracle.
- Evaluator warning: automated search over heap variants will be misleading unless it enforces pointer-model restrictions and the exact working-set measure.
- Decision: keep, but downgrade confidence and explicitly separate working-set, unified-bound, decrease-key, smooth/slim/pairing, and Dijkstra-heap claims.

### pairing_heaps

- Open-problem claim: explicit historically; still unresolved for the standard two-pass pairing heap's exact amortized decrease-key complexity.
- Newer work checked: slim/smooth heap analysis reaches `O(log log n)` decrease-key for related self-adjusting heaps, not the standard pairing heap; Isabelle/AFP material is formalization of variants/correctness/amortized analyses, not a closure of the classic standard-heap gap.
- Saturation: medium-high. Decades old and attacked by specialists.
- Smallest meaningful subproblem: potential-function search for standard two-pass pairing heap sequences that either certify Pettie-style bounds on restricted operation schedules or produce adversarial families.
- Best use: OpenEvolve_project for potential/counterexample mining; theorem_project only with narrow scope.
- Evaluator warning: small heaps heavily underfit amortized lower-bound behavior.
- Decision: keep as computationally useful, but not as an easy theorem target.

### karp_rabin_collision_detection

- Open-problem claim: explicit in Dagstuhl 25191.
- Exact statement recovered: given a string and a prime modulus, decide whether any two distinct equal-length substrings have equal Karp-Rabin fingerprint; quadratic via suffix trees is straightforward; target is linear or near-linear, and false rejection of good polynomials/moduli is allowed with small probability.
- Saturation: low-to-medium. Stringology has many adjacent fingerprinting uses, but this exact certification problem appears narrow.
- Smallest meaningful subproblem: fixed length `ell` collision detection across all substrings, then all lengths; separate deterministic exact detection from randomized one-sided rejection.
- Best use: OpenEvolve_project plus theorem_project.
- Evaluator warning: if the problem permits false rejection, an evaluator must distinguish exact collision-finding from randomized certification. A deterministic exhaustive oracle is still fine for small instances.
- Decision: remains promising after sharpening.

### lazy_b_trees

- Open-problem claim: explicit for external biased search trees in the MFCS 2025 Lazy B-Trees paper, but the project formulation is still fuzzy.
- Newer work checked: none found beyond the 2025 primary paper during this pass.
- Saturation: low but technically dense.
- Smallest meaningful subproblem: external-memory biased search for static weighted keys with linear block space and `O(log_B(W/w)+1)` search I/Os; postpone update-heavy formulations.
- Best use: theorem_project or background_context until definitions are extracted.
- Evaluator warning: poor automated evaluator; experiments on toy B-trees will not validate asymptotic weighted I/O guarantees.
- Decision: keep, but not OpenEvolve-first.

### list_update

- Open-problem claim: explicit in Ambuehl-Gaertner-von Stengel 2012 for optimal randomized ratio between `1.5` and `1.6`.
- Newer work checked: quick search did not find a newer primary closure; related work mostly variants such as advice/delays/time windows.
- Saturation: old and somewhat stale rather than saturated.
- Smallest meaningful subproblem: finite-state randomized non-projective algorithms with certifiable lower-bound games on small list sizes.
- Best use: OpenEvolve_project.
- Evaluator warning: finite-state improvements may not lift to arbitrary list length.
- Decision: keep as evaluator playground, not theorem-first.

### path_compression_topdown

- Open-problem claim: explicit, but it is a proof problem. The inverse-Ackermann theorem itself is long solved.
- Newer work checked: Dagstuhl 25191 attributes the problem to Tarjan and cites Seidel-Sharir 2005. The value is a direct bridge from the `J` recurrence to classical Ackermann.
- Saturation: low as a niche proof-exposition target.
- Smallest meaningful subproblem: formalize the exact Seidel-Sharir recurrence and prove a clean comparison lemma between `J` and a chosen classical Ackermann hierarchy.
- Best use: Lean_formalization_project or theorem_project for proof simplification.
- Evaluator warning: OpenEvolve is essentially useless here except for recurrence experimentation.
- Decision: downgrade as a "new theorem" candidate; keep for blind proof workflow only after recurrence extraction.

### succinct_compressed_structures

- Open-problem claim: explicit in Dagstuhl, but currently bundled too broadly.
- Newer work checked: only the Dagstuhl source in this pass. The HTML loses important notation.
- Saturation: medium; compressed indexing is large.
- Smallest meaningful subproblem: split into two candidates: LZ indexing with `O(n)` space and `O(log N)` access, and grammar/DAG expansion-length sampling.
- Best use: theorem_project after source recovery; grammar/DAG side may become OpenEvolve_project.
- Evaluator warning: LZ/grammar toy instances may not capture known compressed-index lower-bound barriers.
- Decision: hold unless split and formalized.

### search_trees_on_trees_lp

- Open-problem claim: explicit for general polynomial-time optimal static STT; explicit for LP/open directions in Sadeh-Kaplan-Zwick 2025.
- Newer work checked: arXiv v2 from 2025-08-01; no post-v2 closure found in this pass.
- Saturation: low-to-medium. Small but active expert group.
- Important correction: paths and stars are baselines, not open exact-optimization targets. Paths reduce to ordinary optimal BSTs; stars are proved LP-integral with a polynomial-time optimal algorithm. The open LP question about paths is about LP/root-rounding/projection behavior, not about whether optimal search trees on path topologies can be computed.
- Smallest meaningful subproblem: reproduce Sadeh-Kaplan-Zwick's code/counterexamples, then attack edge-diameter-3/almost-star LP integrality or D-space projection integrality.
- Best use: OpenEvolve_project and theorem_project.
- Evaluator warning: polytope enumeration will scale badly and can produce false confidence from tiny topologies.
- Decision: remains one of the strongest candidates, after narrowing away from solved path/star baselines.

### splay_preorder_231

- Open-problem claim: explicit for traversal in older sources, but current exact status is a moving frontier and highly saturated.
- Newer work checked: Pareek 2025 proves Greedy linear for a permutation-initial-tree class; Berendsohn-Kozma-Opler v4 (2025-11-24) resolves offline OPT constant for fixed-pattern-avoiding inputs; Levy-Tarjan only proves empty insertion and balanced-target variants for Splay.
- Saturation: severe. This is dynamic optimality territory.
- Smallest meaningful subproblem: Splay on 231-avoiding permutations from one sharply defined nontrivial initial-tree class not covered by empty/aligned/balanced-target results; or a Splay-vs-Greedy obstruction lemma.
- Best use: theorem_project only if narrow; OpenEvolve_project only for counterexample/invariant scouting; otherwise background_context.
- Evaluator warning: exact offline OPT comparisons and small Catalan simulations can mislead; distinguish Splay, Greedy, arbitrary initial tree, flat/empty initial state, and preorder/permutation initial tree.
- Decision: downgraded from top promotion to narrow probe.

### dynamic_graph_structures

- Open-problem claim: mixed. Dynamic connectivity level-elimination is explicit. Incremental topological sort as written is not open.
- Newer work checked: Bhattacharya-Kulkarni already gives randomized `~O(m^(4/3))` incremental cycle detection/topological ordering; Dagstuhl asks for a combinatorial bound that would beat sparse algorithms for sufficiently dense graphs, but the HTML omits the exact expression.
- Saturation: high.
- Smallest meaningful subproblem: eliminate the level structure in Monte Carlo dynamic connectivity; or reconstruct Fineman's exact missing expression before using topological sort.
- Best use: background_context until sharpened.
- Evaluator warning: adversarial insertion simulators do not certify total update bounds.
- Decision: downgrade from promoted top candidate.

### history_independent_data_structures

- Open-problem claim: uncertain. Dagstuhl says participants explored reconciling history independence and optimal priority-queue efficiency, but no formal theorem target is recorded.
- Saturation: unclear; likely active after Dagstuhl.
- Smallest meaningful subproblem: define strong history independence for heaps and prove a lower/upper bound in a specified model without decrease-key first.
- Best use: background_context/source-gathering.
- Evaluator warning: distributional equivalence of memory layouts is hard to test exhaustively beyond tiny states.
- Decision: hold; source too weak for promotion.

### external_memory_structures

- Open-problem claim: mixed. The old external-memory priority-queue DecreaseKey necessity question is answered by lower bounds; remaining work/I/O tradeoffs are not yet one clean target.
- Saturation: medium.
- Smallest meaningful subproblem: one explicit simultaneous work/I/O tradeoff instance, not a broad "external memory structures" cluster.
- Best use: background_context unless split.
- Evaluator warning: cache/I/O toy models are easy to mis-specify.
- Decision: keep as context for `lazy_b_trees`, not a top candidate.

## Source Quality Flags

- Dagstuhl 25191 is useful, but terse. Candidates sourced only to Dagstuhl need either a full paper, slides, or author notes before promotion.
- `history_independent_data_structures`, `geometric_data_structures`, and `kinetic_data_structures` are too weakly sourced for top-candidate status.
- `succinct_compressed_structures` loses notation in HTML; use the PDF or talk notes before making exact asymptotic claims.
- `unified_bound_heaps` must cite the Dijkstra working-set heap paper as adjacent solved/near-solved context.
- `search_trees_on_trees_lp` should not rely only on Sadeh-Kaplan-Zwick for Golinsky's original conjecture; locate Golinsky's thesis/manuscript.

## Blind Prompt Flags

- `quadratic_probing/blind_prompt.md`: acceptable only if updated mentally to treat `alpha >= 0.089` as known in frontier mode. Blind mode can still ask for a proof, but should not claim no nontrivial result is known.
- `splay_preorder_231/blind_prompt.md`: good separation of Version A and B. Keep the warning that empty-tree insertion is not the main open target.
- `search_trees_on_trees_lp/blind_prompt.md`: good baseline separation for paths/stars. Add care that "paths open" means LP behavior, not exact optimal BST computation.
- `path_compression_topdown/blind_prompt.md`: not usable until the exact Seidel-Sharir recurrence and the chosen Ackermann normalization are copied into the prompt.
- `karp_rabin_collision_detection/blind_prompt.md`: should explicitly distinguish deterministic exact detection from randomized false rejection.

## Revised Promotion List

Promote now:

- `search_trees_on_trees_lp`
- `quadratic_probing`
- `karp_rabin_collision_detection`
- `pairing_heaps`
- `list_update`

Promote only after sharpening:

- `unified_bound_heaps`
- `lazy_b_trees`
- `succinct_compressed_structures`

Keep as proof/formalization:

- `path_compression_topdown`

Background/context or narrow probe:

- `splay_preorder_231`
- `dynamic_graph_structures`
- `history_independent_data_structures`
- `external_memory_structures`
