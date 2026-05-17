# Scouting v2 Synthesis

Status: complete synthesis of completed Scouting v2 background subruns.

Date synthesized: 2026-05-17.

Branch: `scouting-v2-source-saturation`.

Input files read: `reports/scouting_v2/README.md`, subruns `2A`, `2B`, `2F`, `2I`, `2R`, `reports/top_20_shortlist.md`, `reports/candidate_matrix.md`, and candidate-topic `score.yaml` plus `skeptical_audit.md` files.

Budget status: the first recorded v2 subrun date is 2026-05-16 America/Los_Angeles for `2F`; the five-calendar-day deadline would be 2026-05-21. Optional `subrun_2R_v1_area_remining.md` is present and was included. All planned v2 subruns listed in the framework are complete, so this synthesis does not need to take the absent-2R path.

Boundary: STT / DS(k,1) remains the foreground proof project. This document is a recommendation artifact only. A pivot, split, or side experiment below is not an executed project decision.

## 1. Consolidated Candidate Table

Legend: `new` means no existing top-20 slug before v2; `existing` means already in the top-20 shortlist; `update` means v2 added source evidence to an existing top-20 candidate. `Gate` is assigned in the next section and is repeated here for scanability.

| Slug | Status | Source pool(s) | Open/source status | Gate | Short synthesis note |
| --- | --- | --- | --- | --- | --- |
| `path_compression_topdown` | existing + update | top-20; 2F author pages | explicit 2025 Tarjan/Dagstuhl proof problem | pass | Very under-attended proof/formalization target; exact recurrence must be copied before a blind run. |
| `karp_rabin_collision_detection` | existing + update | top-20; 2F author pages | explicit 2025 Farach-Colton/Dagstuhl problem | pass | Crisp string/data-structure algorithm problem with exact small-instance collision oracles. |
| `search_trees_on_trees_lp` | existing + update | top-20; 2I OpenEvolve objects | explicit/high confidence in Sadeh-Kaplan-Zwick 2025 | pass | Still excellent for certified STT enumeration, LP witnesses, and inequality search; not the most literally under-attended. |
| `unified_bound_heaps` | existing + update | top-20; 2F author pages; 2I rejection context | explicit 2025 Iacono/Dagstuhl pointer-model target | pass | Strong theorem lead after fixing the exact working-set variant and excluding non-pointer heap results. |
| `dynamic_connectivity_level_elimination` | new | 2R v1 area re-mining | explicit 2025 Dagstuhl problem inside KKM-style dynamic connectivity | pass | Narrow simplification target in an otherwise saturated dynamic-graph area. |
| `lazy_b_trees` | existing | top-20; 2I rejection context | explicit but formulation-sensitive 2025 MFCS lead | pass | Niche theorem lead with weak evaluator support; needs exact operation/bound extraction. |
| `higher_dim_rectangle_stabbing_word_ram_linear_space` | new | 2A geometry | explicit JoCG/ICALP higher-dimensional word-RAM open problem | pass | Narrow geometry theorem lead; technical and not very evaluator-friendly. |
| `connected_circle_segment_queries` | existing + update | top-20; 2A duplicate update; 2I rejection context | explicit ISAAC 2025 future-work/lower-bound lead | pass | Recent connected-geometry lower-bound/tradeoff lead; finite tests can mislead. |
| `range_mode_queries` | existing + update | top-20; 2I OpenEvolve objects; 2B duplicate context | open with medium-high confidence | pass | Good exact-oracle OpenEvolve/theorem hybrid, but the modern upper/lower frontier still needs source refresh. |
| `pairing_heaps` | existing + update | top-20; 2I OpenEvolve objects | open with medium-high confidence | pass | Strong artifact-search target; high saturation and variant-confusion risk keep it below first theorem pilots. |
| `list_update` | existing + update | top-20; 2F author pages; 2I OpenEvolve objects | older explicit gap, 2024 source support | pass | Best clean finite-game OpenEvolve target; theorem generalization remains hard. |
| `quadratic_probing` | existing + update | top-20; 2I OpenEvolve objects | open/narrow after ICALP 2024 | pass | Good hashing side experiment if witness/certificate search is separated from empirical probing. |
| `randomized_linear_list_labeling_lower_bound` | new | 2B cell-probe/lower-bound mini-frontiers | explicit FOCS 2024 residual lower-bound gap | pass | Fresh lower-bound mini-frontier with exact tiny-game and adversary-search artifacts. |
| `lz77_linear_compressed_matching` | new | 2R v1 area re-mining | explicit 2025 Dagstuhl LZ matching question | pass | Crisp stringology split from broad succinct/compressed folder; LZ model must be fixed. |
| `dynamic_planar_nearest_neighbor_logarithmic_full` | new | 2A geometry | explicit TOPP problem; fresh 2025 insertion-only progress | pass | Fully dynamic residual is explicit, but the proof burden is high and the area is central geometry. |
| `dynamic_stream_mincut_space` | existing | top-20 | explicit ITCS 2025 streaming open question | pass | Explicit and important, but lower-bound-heavy and only weakly evaluator-friendly. |
| `directed_roundtrip_compact_routing` | existing | top-20 | explicit DISC/arXiv 2025 open problem | pass | Source-supported, but active compact-routing theory and weak OpenEvolve fit reduce theorem-pilot appeal. |
| `dynamic_disconnected_planar_point_location` | new | 2A geometry | inferred residual after connected-case closure | flag | Plausibly under-attended, but needs a modern citation sweep under point-location/ray-shooting terminology. |
| `dynamic_orthogonal_range_reporting_update_exponent` | new | 2A geometry | inferred update-exponent gap | flag | Precise enough to remember, but the open statement is inferred and source freshness is weaker. |
| `deferred_work_io_tradeoff` | new | 2R v1 area re-mining | inferred fresh work/I/O tradeoff target | flag | Interesting external-memory lead, but the Dagstuhl HTML lacks formal parameters and no manuscript was located. |
| `cache_oblivious_implicit_scanning` | existing + update | top-20; 2R duplicate update; 2I rejection context | explicit old strict-implicit gap, low-medium confidence | flag | Keep only in exact `n`-cell implicit model; source age prevents clean pass. |
| `imprecise_comparison_sorting` | existing | top-20; 2I rejection context | open, modern status uncertain | flag | Excellent finite game, but exact model/follow-up terminology needs verification and it is not object-first DS rediscovery. |
| `succinct_compressed_structures` | existing + update | top-20; 2R duplicate/update; 2I rejection context | open but bundled | flag | Must split LZ matching from grammar/DAG sampling; 2026 grammar-access work is a major freshness warning. |
| `optimal_static_bst_subquadratic` | new | 2F author pages | stale 2003 open claim; uncertain current status | flag | Very clean if still open, but needs a serious modern fine-grained/DP search before promotion. |
| `splay_preorder_231` | existing + update | top-20; 2I OpenEvolve objects | uncertain narrow open status; severe saturation | flag | Good background OpenEvolve rediscovery experiment, not a first theorem pilot. |
| `dynamic_min_tree_cut` | existing | top-20; 2I rejection context | plausible but not crisp | fail | Dynamic min-cut saturation and recent 2025/2026 progress make the residual unsafe. |
| `kinetic_high_dim_extent` | existing + update | top-20; 2A duplicate update; 2R rejection context | uncertain and too broad | fail | Needs a single 3D measure/motion model and current primary source before promotion. |
| `dynamic_text_indexing` | existing | top-20; 2I/2R rejection context | stale open claim needing reformulation | fail | Broad dynamic compressed indexing is a literature-review trap until one exact residual is isolated. |
| `concurrent_shi_cell_capacity` | existing | top-20 | inferred fragile residual after STOC 2025 | fail | The current formulation may be wrong; best use is model extraction/checking, not theorem search. |

## 2. Feasibility Gate

Gate criteria applied before ranking:

- explicit or high-confidence open status;
- nontriviality as a theorem/data-structure problem;
- plausible two-week artifact path, such as a blind prompt, frontier document, exact checker, finite certificate search, or model-extraction note;
- no likely-solved or severe staleness issue.

`Pass` does not mean "ready to solve"; it means the candidate can be ranked without violating the source standards. `Flag` means preserve as a lead but do not include in theorem-pilot rankings. `Fail` means do not promote without a new primary-source event.

| Gate | Candidates | Reason |
| --- | --- | --- |
| pass | `path_compression_topdown`, `karp_rabin_collision_detection`, `search_trees_on_trees_lp`, `unified_bound_heaps`, `dynamic_connectivity_level_elimination`, `lazy_b_trees`, `higher_dim_rectangle_stabbing_word_ram_linear_space`, `connected_circle_segment_queries`, `range_mode_queries`, `pairing_heaps`, `list_update`, `quadratic_probing`, `randomized_linear_list_labeling_lower_bound`, `lz77_linear_compressed_matching`, `dynamic_planar_nearest_neighbor_logarithmic_full`, `dynamic_stream_mincut_space`, `directed_roundtrip_compact_routing` | Source-supported enough for ranking; each has at least one plausible two-week artifact path. |
| flag | `dynamic_disconnected_planar_point_location`, `dynamic_orthogonal_range_reporting_update_exponent`, `deferred_work_io_tradeoff`, `cache_oblivious_implicit_scanning`, `imprecise_comparison_sorting`, `succinct_compressed_structures`, `optimal_static_bst_subquadratic`, `splay_preorder_231` | Interesting but blocked by inferred/stale/bundled open status, missing parameters, or severe saturation. |
| fail | `dynamic_min_tree_cut`, `kinetic_high_dim_extent`, `dynamic_text_indexing`, `concurrent_shi_cell_capacity` | Current formulations are too uncertain, broad, stale, likely changed by recent work, or not crisp enough to evaluate automatically. |

## 3. Lexicographic Primary Theorem Ranking

This ranking uses only feasibility-gated candidates. It is lexicographic, not averaged:

1. literal under-attendedness on the anchored 1--5 scale;
2. AI-collaboration fit;
3. theorem-project suitability.

Ties are noted rather than hidden. STT's previous top-20 rank is informational only.

| Rank | Slug | Source pool(s) | Under-attendedness | AI-collab fit | Theorem fit | Rationale |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `path_compression_topdown` | top-20; 2F | 5 | 5 | 4 | Exact Tarjan 2025 proof-translation problem; tiny named source cluster; strong staged proof/formalization shape. |
| 2 | `karp_rabin_collision_detection` | top-20; 2F | 5 | 5 | 4 | Fresh Dagstuhl problem, few named citations, exact brute-force oracles; nearly tied with rank 1. |
| 3 | `search_trees_on_trees_lp` | top-20; 2I | 4 | 5 | 4 | Small active STT community, explicit 2025 open LP/static STT frontier, excellent certificate pipeline. |
| 4 | `unified_bound_heaps` | top-20; 2F | 4 | 4 | 4 | Explicit 2025 pointer-model heap target; good amortized-proof search once definitions are fixed. |
| 5 | `dynamic_connectivity_level_elimination` | 2R | 4 | 4 | 3 | One fresh source cluster asks for level elimination; AI can inspect invariants, but dynamic connectivity remains technically saturated. |
| 6 | `lazy_b_trees` | top-20 | 4 | 3 | 4 | Low-saturation external-memory theorem lead; weaker evaluator path than the top candidates. |
| 7 | `higher_dim_rectangle_stabbing_word_ram_linear_space` | 2A | 4 | 3 | 3 | Explicit JoCG/ICALP higher-dimensional word-RAM gap; likely technical geometry proof work. |
| 8 | `connected_circle_segment_queries` | top-20; 2A | 4 | 3 | 3 | Explicit ISAAC 2025 lower-bound/tradeoff lead; finite connected-instance generators help but do not certify lower bounds. |
| 9 | `range_mode_queries` | top-20; 2I | 3 | 5 | 4 | Strong exact oracle and theorem sidecar; less literally under-attended than ranks 1--8. |
| 10 | `pairing_heaps` | top-20; 2I | 3 | 5 | 3 | Excellent potential/counterexample mining target; well-known specialist problem with high saturation. |
| 11 | `list_update` | top-20; 2F/2I | 3 | 5 | 2 | Superb finite-game object, but theorem lift to arbitrary lists is the bottleneck. |
| 12 | `quadratic_probing` | top-20; 2I | 3 | 4 | 3 | Fresh narrowed hashing frontier after ICALP 2024; model sensitivity limits theorem pilot rank. |
| 13 | `randomized_linear_list_labeling_lower_bound` | 2B | 3 | 4 | 3 | Explicit FOCS 2024 residual lower-bound gap with finite-game artifacts. |
| 14 | `lz77_linear_compressed_matching` | 2R | 3 | 4 | 3 | Explicit 2025 LZ matching question; stringology machinery and model variants lower immediate theorem fit. |
| 15 | `dynamic_planar_nearest_neighbor_logarithmic_full` | 2A | 3 | 3 | 3 | Explicit fully dynamic geometry residual; central and technical rather than deeply neglected. |
| 16 | `dynamic_stream_mincut_space` | top-20 | 2 | 3 | 3 | Explicit and important, but active streaming/lower-bound setting. |
| 17 | `directed_roundtrip_compact_routing` | top-20 | 2 | 2 | 3 | Explicit but high-traffic compact-routing theory and weak evaluator transfer. |

### Top 5 Source-Based Justifications

1. `path_compression_topdown`: The 2F author-page scan found Tarjan's May 2025 Dagstuhl problem asking for a direct classical-Ackermann proof from the Seidel-Sharir top-down recurrence. The candidate folder scores it as high-confidence, low-saturation, and best for Lean/formalization. Its main risk is that a clean proof may exist in notes; that is a small-source-check risk, not a saturation signal.

2. `karp_rabin_collision_detection`: The 2F scan records Farach-Colton's May 2025 Dagstuhl statement: given a string and prime modulus, detect equal-length Karp-Rabin collisions faster than quadratic time. The existing audit says exact small strings and moduli give natural oracles, while warning not to merge deterministic exact detection with randomized false rejection.

3. `search_trees_on_trees_lp`: The 2I report identifies concrete evolvable objects: STT LP valid-inequality templates, topology generators, root-rounding rules, and rational certificates. The existing audit says general static STT remains explicitly open in Sadeh-Kaplan-Zwick 2025, while warning that paths/stars must not be misstated as open exact-optimization cases.

4. `unified_bound_heaps`: The 2F report cites Iacono's 2025 Dagstuhl note, which explicitly asks for a pointer-model working-set heap with constant-time `decrease-key`. The source evidence is fresh and narrow, but the audit requires separating this from recent Dijkstra/universal-optimality heap work outside the pointer-model target.

5. `dynamic_connectivity_level_elimination`: The 2R report found a fresh Dagstuhl 25191 statement by Liu and King asking whether the level data structure can be eliminated in sequential and batch-dynamic Monte Carlo connectivity. The exact subproblem is under-attended, even though dynamic connectivity as a whole is not.

## 4. Pilot-Readiness Ranking

This ranking is informational. It estimates prep cost and two-week artifact feasibility; it does not override the primary theorem ranking by itself.

Priority order:

1. artifact feasibility;
2. AI-collaboration fit;
3. theorem significance;
4. under-attendedness.

| Rank | Slug | Artifact path | AI fit | Theorem significance | Under-attendedness | Readiness rationale |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `search_trees_on_trees_lp` | Reproduce/enlarge STT enumeration, rational LP certificates, inequality falsifiers | 5 | 5 | 4 | Existing folder and foreground context make prep cheapest; artifacts are certificate-shaped. |
| 2 | `karp_rabin_collision_detection` | Exhaustive string/modulus oracle, collision-detector grammar, adversarial instances | 5 | 4 | 5 | Crisp source statement and small-instance oracle; little folder work needed beyond variant separation. |
| 3 | `path_compression_topdown` | Exact recurrence extraction, blind proof prompt, recurrence inequality checker/Lean skeleton | 5 | 3 | 5 | Very low prep after recurrence copy; significance is expository/foundational rather than a new DS frontier. |
| 4 | `randomized_linear_list_labeling_lower_bound` | Tiny-array minimax/LP games, adversary distributions, potential templates | 4 | 4 | 3 | FOCS 2024 source is fresh and explicit; finite artifacts are plausible within two weeks. |
| 5 | `list_update` | Exact small-list game, randomized policy tables, adversarial traces | 5 | 3 | 3 | Best finite game infrastructure, but theorem lift is weaker than ranks 1--4. |
| 6 | `pairing_heaps` | Simulator, trace generator, potential-inequality checker | 5 | 4 | 3 | High artifact value, high risk of rediscovering variants rather than proving standard two-pass bounds. |
| 7 | `range_mode_queries` | All-interval exact mode oracle, hard-array generator, candidate-list grammar | 5 | 4 | 3 | Good evaluator; modern frontier verification remains a prep task. |
| 8 | `unified_bound_heaps` | Operation semantics, working-set trace generator, potential templates | 4 | 4 | 4 | Strong theorem target, but exact definition splitting must happen first. |
| 9 | `quadratic_probing` | Table simulator, witness-family generator, proof-template checks | 4 | 3 | 3 | Feasible side artifact; theorem target is model-sensitive after ICALP 2024. |
| 10 | `lz77_linear_compressed_matching` | LZ parse generator, decompressing oracle, phrase-boundary algorithm schema tests | 4 | 4 | 3 | Crisp, but stringology model cleanup costs more than ranks 1--7. |

### Top 5 Source-Based Justifications

1. `search_trees_on_trees_lp`: The 2I report gives the strongest artifact path: enumerate STTs, solve Golinsky-style LP instances, check inequalities against integral points and fractional vertices, and output exact rational certificates. The top-20 audit already identifies reproducing the Sadeh-Kaplan-Zwick pipeline as the next concrete step.

2. `karp_rabin_collision_detection`: The Dagstuhl problem statement gives a compact input/output task; 2F and the candidate audit both identify exhaustive small strings/moduli as a natural checker. Prep is mostly about fixing deterministic exact detection versus allowed randomized rejection.

3. `path_compression_topdown`: The source-backed problem is a proof transformation. A two-week artifact can be a recurrence-normalization document, a blind prompt, and a small recurrence table/inequality checker. The only hard prerequisite is copying the exact Seidel-Sharir recurrence and Ackermann normalization.

4. `randomized_linear_list_labeling_lower_bound`: 2B records the FOCS 2024 statement that randomized linear-space list labeling still has only an `Omega(log n)` lower bound against an `O(log n polyloglog n)` upper bound. Small exact games, LPs, and adversary distributions are credible two-week artifacts.

5. `list_update`: 2F records the older Demaine/Iacono gap and a 2024 Cambridge source still describing the randomized 1.5 versus 1.6 gap. 2I identifies the cleanest finite-game evaluator among all side experiments: exact offline optimum/work-function values for small lists.

## 5. OpenEvolve Side-Experiment Ranking

This ranking is separate from theorem-pilot choice. It uses:

1. clarity of evolvable object;
2. evaluator quality;
3. theorem-relevant artifact potential;
4. benchmark-overfit risk, where lower risk ranks higher;
5. two-week feasibility.

| Rank | Slug | Evolvable object | Evaluator | Artifact potential | Overfit risk | Two-week feasibility | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `list_update` | finite-state randomized online policy and adversarial request generator | exact offline optimum/work-function game for small lists | policy tables, adversarial traces, finite LP/game certificates | medium | high | Best side experiment. |
| 2 | `search_trees_on_trees_lp` | LP inequality templates, root-rounding rules, topology/frequency generators | STT enumeration plus rational LP certificates | exact witnesses, valid/falsified inequalities | medium | medium-high | Best theorem-artifact generator. |
| 3 | `randomized_linear_list_labeling_lower_bound` | insertion adversaries, relabeling strategies, potential templates | tiny-array minimax/LP games and exact simulation | hard distributions, segment-chain potentials | medium-high | medium-high | Fresh lower-bound side experiment. |
| 4 | `pairing_heaps` | heap-linking/pass rules, operation traces, potential templates | exact heap simulator and amortized inequality checker | minimal traces, surviving potential families | high | medium-high | Strong, but variant confusion is serious. |
| 5 | `quadratic_probing` | witness-family generator and probe/hash parameter schedule | finite table simulator plus exact obstruction metrics | obstruction families and proof-template stress tests | high | medium-high | Good hashing experiment after model locking. |
| 6 | `range_mode_queries` | block-summary/candidate-list grammar and hard-array generator | brute-force exact mode for every interval | counterexample arrays and candidate-list rules | high | medium | Useful benchmark, not top side experiment. |
| 7 | `splay_preorder_231` | local BST rotation rule and potential-template falsifier | exact Splay simulator; small offline BST optimum | invariants or minimal obstructions | very high | medium | Good rediscovery experiment, but too saturated. |
| 8 | `karp_rabin_collision_detection` | collision-detector/filtering grammar or bad-modulus generator | exhaustive same-length substring collision oracle | algorithms or hard strings/moduli | medium | medium | Strong oracle, less obviously data-structure-object-first. |

### Top 5 Source-Based Justifications

1. `list_update`: 2I ranked it first because the mutable object and evaluator are both exceptionally clean. 2F confirms the classical randomized gap remains source-supported enough for finite policy/adversary experiments, with model-variant caution.

2. `search_trees_on_trees_lp`: 2I describes a direct pipeline from evolutionary search to theorem artifacts: inequality grammars, topology generators, exact enumeration, rational LP certificates, and minimal witness catalogues. It is less "rediscovery" than list update, but more theorem-relevant.

3. `randomized_linear_list_labeling_lower_bound`: 2B gives a fresh explicit FOCS 2024 residual and names exact dynamic programming, minimax/LP games, adversarial insertion sequences, and potential inequalities as plausible evaluators/artifacts.

4. `pairing_heaps`: 2I identifies exact simulators and potential inequality checkers as natural, and the existing top-20 folder confirms the standard two-pass decrease-key question remains open. The rank is capped by high specialist saturation and the risk that evolved variants do not answer the standard heap.

5. `quadratic_probing`: 2I and the top-20 shortlist agree that ICALP 2024 narrowed the problem rather than eliminating it. Evolving witness families and proof-template obstructions is more theorem-relevant than optimizing average probe counts.

## 6. Existing-Candidate Rank Changes

The new primary ranking is not comparable to the old top-20 numeric order because it is lexicographic and starts with literal under-attendedness. Material changes:

| Candidate | Old top-20 position | New primary position/status | Change explanation |
| --- | --- | --- | --- |
| `path_compression_topdown` | 12 | 1 | Rose because the new criterion rewards the exact under-attended 2025 proof problem and strong AI proof fit, even though it is proof archaeology rather than a new DS bound. |
| `karp_rabin_collision_detection` | 5 | 2 | Rose because v2 found fresh author-page support and gave it a score-5 under-attendedness anchor with strong exact oracles. |
| `search_trees_on_trees_lp` | 1 | 3 | Dropped only because two candidates are more literally under-attended. It still genuinely scores well: under-attendedness 4, AI fit 5, theorem fit 4. The drop is not an incumbent penalty. |
| `unified_bound_heaps` | 8 | 4 | Rose because the 2025 Iacono source makes the pointer-model target explicit and under-attended. |
| `range_mode_queries` | 4 | 9 | Dropped in theorem ranking because under-attendedness is only moderate; it remains strong for OpenEvolve and pilot-readiness. |
| `quadratic_probing` | 2 | 12 | Dropped under theorem-first criteria because it is OpenEvolve-first, model-sensitive, and less literally under-attended after ICALP 2024 progress. |
| `imprecise_comparison_sorting` | 3 | flagged | Dropped because v2 object-first criteria rejected it as not primarily a data-structure rediscovery object and its modern open status still needs a terminology sweep. |
| `pairing_heaps` | 7 | 10 | Still strong for artifacts, but high saturation prevents top theorem rank. |
| `splay_preorder_231` | 15 | flagged | Dropped because severe saturation and many nearby 2024/2025 BST results make the narrow residual fragile. |
| `cache_oblivious_implicit_scanning` | 11 | flagged | Dropped because the only defensible statement is old and exact-implicit; freshness must be improved before ranking. |
| `succinct_compressed_structures` | 14 | flagged | Dropped because v2 found a likely 2026 freshness issue for grammar/DAG sampling and a need to split LZ matching into its own lead. |
| `dynamic_text_indexing` | 19 | fail | Dropped further because 2R found no clean modern residual beyond the stale 2007-style claim. |
| `concurrent_shi_cell_capacity` | 20 | fail | Dropped because the 2025 source may already undermine the current one-key/two-key framing. |

No candidate should be treated as promoted solely because it was already an incumbent. Conversely, STT LP remains a top-three theorem candidate because it genuinely has unusually strong certificate infrastructure and source-supported open status, not because it began at rank 1.

## 7. Empty/Sparse-Pool Report

Sparse pools are signal, not failure.

| Subrun | Returned candidates | Search depth | Rejected candidates and signal |
| --- | --- | --- | --- |
| `2A_geometry` | 4 | SoCG/Dagstuhl/CCCG/JoCG/TOPP geometry source trails, author-maintained pages, duplicate checks against local folders and top-20 | Rejected/duplicate: `connected_circle_segment_queries`, `kinetic_3d_convex_hull_kds`, `proximate_planar_point_location_linear_space`, `hyperbolic_dynamic_approximate_nearest_neighbor`, `connected_dynamic_planar_point_location`, `non_orthogonal_square_or_triangular_range_reporting`, `klee_measure_3d_polylog`. Signal: geometry has many tempting old or adjacent leads, but current open status often depends on exact model and recent partial progress. |
| `2B_cell_probe_lower_bounds` | 1 | Candidate folders, top-20, dynamic/cell-probe lower-bound papers, lecture notes, 2025/2026 closure checks | Rejected/duplicate: `retroactive_cell_probe_linear_overhead`, `dynamic_boolean_cell_probe_log_squared`, `dynamic_range_counting_one_bit_output`, `dynamic_connectivity_log_gap`, `range_mode_cell_probe_gap`, `transdichotomous_point_location_lower_bound`, `dynamic_interval_union_query_sparse_tradeoff`, `static_linear_space_cell_probe_barrier`, `open_addressing_oblivious_hashing_lower_bound`. Signal: famous lower-bound frontiers are either saturated, duplicate existing leads, or recently narrowed/closed. |
| `2R_v1_area_remining` | 3 | Re-mined v1 dynamic/kinetic, external-memory/cache-oblivious, strings/succinct/compressed, heap/hash/union-find/persistent/retroactive areas with targeted freshness checks | Rejected/duplicate: `grammar_dag_length_sampling`, `cache_oblivious_implicit_scanning`, `kinetic_3d_exact_diameter_or_width`, `incremental_topological_sort_combinatorial_bound`, `history_independent_priority_queues`, `cache_pair_problem`, `simple_integer_successor_delete`, `persistent_arrays_stricter_model`, `retroactive_lower_bound_strengthening`, `hashing_dictionaries_all_purpose_residual`, `dynamic_text_indexing_linear_bits`. Signal: v1 had several broad or stale folders; the best new value came from splitting or downgrading them. |

`2F_author_problem_pages` returned exactly five candidate findings, so it is not sparse, but most findings were source updates to existing slugs. `2I_openevolve_objects` promoted six side-experiment candidates, so it is not sparse; its rejection ledger is still important for separating exact oracles from real evolvable objects.

## 8. Rejection-Ledger Synthesis

The strongest rejection signals are:

- Recent lower-bound progress is closing old cell-probe prompts. The Boolean dynamic data-structure lower-bound line, one-bit-output frontiers, interval-union tradeoffs, and broad static DS lower-bound barriers are not good under-attended candidates without a new narrow residual.
- Stale author pages are useful provenance but poor open-status evidence. `optimal_static_bst_subquadratic` is intriguing but cannot be promoted from a 2003 page alone; Erickson's older pages explicitly warn against citing them as current status.
- Broad folders should be split before promotion. `succinct_compressed_structures`, `dynamic_text_indexing`, `kinetic_high_dim_extent`, `history_independent_data_structures`, and `hashing_dictionaries` all hide multiple model-specific problems under one label.
- Dynamic graph leads are usually saturated. `dynamic_connectivity_level_elimination` survives only because it is a narrow level-elimination question inside one framework; `dynamic_min_tree_cut` does not yet have that crispness.
- Exact finite oracles are not enough. Several rejected OpenEvolve leads have small-instance checkers, but no clean evolvable data-structure object or no path from finite scores to theorem artifacts.
- Freshness can downgrade a lead, not just promote it. The grammar/DAG sampling update is the clearest example: a 2026 arXiv preprint may change or solve the Dagstuhl formulation, so the candidate should wait for line-by-line comparison.

## 9. Pilot Recommendation

Theorem pilot recommendation from the primary ranking plus feasibility gate: `path_compression_topdown`.

This is a recommendation for later control-panel review, not an immediate project switch. It wins the primary ranking because it is the most literally under-attended source-supported proof problem and has high AI proof-collaboration fit. It is not chosen because it is more important than STT; it is chosen because the mandated lexicographic criterion starts with literal under-attendedness.

Minimum prep if the control panel later adopts this theorem pilot, capped at 3 days:

1. Extract the exact Seidel-Sharir recurrence, parameter conventions, and Ackermann/inverse-Ackermann normalization into the folder frontier.
2. Replace or annotate the blind prompt so it includes the recurrence without smuggling unrelated frontier hints.
3. Add a short audit note checking whether a direct proof appears in known lecture notes or private/public follow-ups.
4. Prepare one machine-checkable recurrence table or inequality harness as a proof-search sanity check.

OpenEvolve side-experiment recommendation: `list_update`.

It has the cleanest mutable object/evaluator pair: finite-state randomized list-update policies plus adversarial request generators, evaluated against exact offline optimum or work-function games for small lists. The deliverable should be policy tables, adversarial traces, and exact finite-game certificates, not sampled scores.

Fallback if the control panel decides `path_compression_topdown` is too expository for the theorem lane: the next primary theorem candidate is `karp_rabin_collision_detection`, with STT LP remaining the strongest pilot-readiness/certificate candidate.

## 10. DS(k,1) Interruption Check

Does this synthesis contain enough evidence to recommend interrupting the current DS(k,1) proof lane immediately?

No. The top alternatives are real and source-supported, but none supplies unusually strong evidence that an immediate interruption is better than continuing the current foreground proof lane.

Should DS(k,1) continue foreground while the scouting output waits for control-panel review?

Yes. DS(k,1) should continue as the foreground proof project. This synthesis can support later review of a small proof-pilot pivot, a `path_compression_topdown` blind run, a `karp_rabin_collision_detection` pilot, or a background `list_update` OpenEvolve side experiment, but it does not execute any of those decisions.
