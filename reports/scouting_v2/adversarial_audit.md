# Scouting v2 Adversarial Audit

Status: complete.

Date audited: 2026-05-17.

Branch: `scouting-v2-source-saturation`.

Scope: hostile audit of the local Scouting v2 artifacts only. This audit did not start Scouting v3, did not add candidate folders, and did not use unlogged new candidates to repair v2. It checks whether the records support their own claims, rankings, duplicate handling, freshness discipline, OpenEvolve fit, and non-interruption boundary for the current STT / DS(k,1) lane.

## Bottom Line

Scouting v2 is useful background triage, but it is not strong enough to justify interrupting DS(k,1). The synthesis mostly obeys its own ranking protocol: feasibility gate before primary ranking, lexicographic primary ranking, and a separate OpenEvolve side-experiment recommendation. The main methodological weakness is that v2 promotes several new slugs into pass-ranked synthesis tables without candidate folders, full skeptical audits, or reusable source metadata in `candidate_topics/`.

The theorem-pilot recommendation `path_compression_topdown` follows the stated primary ranking, but it is a proof-exposition/formalization problem, is numerically tied with `karp_rabin_collision_detection` on the visible primary-ranking tuple, and still needs recurrence extraction before a blind prompt is valid. Treat it as a control-panel option only, not as a foreground replacement for DS(k,1).

The separate OpenEvolve side experiment is properly `list_update`. That recommendation survives the audit because it has a concrete mutable object and exact finite-game evaluator. It should remain a side experiment, not a theorem-lane pivot.

Final verdict: v2 supports continuing STT / DS(k,1) as foreground theorem project and names a separate OpenEvolve side experiment.

## Clear Patches Applied

Only clear factual or score inconsistencies were patched.

| File | Patch | Reason |
| --- | --- | --- |
| `reports/scouting_v2/README.md` | changed stale status from "subruns not started" to completed-framework status | The subruns and synthesis are present and complete. |
| `reports/scouting_v2/subrun_2I_openevolve_objects.md` | normalized `splay_preorder_231` to `openevolve_suitability: 3/5 overall` while preserving the 4/5 counterexample-search and 2/5 theorem-discovery nuance | The candidate folder score is 3; v2 needs one score per required axis. |
| `reports/scouting_v2/synthesis.md` | removed `karp_rabin_collision_detection` from the OpenEvolve side-experiment ranking and added a note explaining exclusion | Subrun `2I` explicitly rejected it for object-first OpenEvolve despite its strong oracle. |

## 19-Point Audit

| # | Check | Verdict | Adversarial finding |
| --- | --- | --- | --- |
| 1 | Existing-slug duplicates | Mostly pass, with split risk | No duplicate folder was created, but `lz77_linear_compressed_matching` is a split/update of `succinct_compressed_structures`, `dynamic_connectivity_level_elimination` overlaps broad dynamic-graph context, and the geometry leads overlap broad placeholder geometry folders. These can be new narrow slugs later, but not pilot-ready without folders. |
| 2 | Cross-subrun duplicates | Pass | No promoted candidate appears twice as independent evidence. Repeated rejected leads such as simple successor-delete are handled as rejections, not promotions. |
| 3 | Stale, inferred, unsupported, or likely solved open claims | Fail as a clean-promotion standard | v2 correctly flags many, but the pass table still contains candidates needing modern source refresh: `range_mode_queries`, `lazy_b_trees`, `dynamic_stream_mincut_space`, and `directed_roundtrip_compact_routing` rely partly on prior folder audits rather than uniform v2 records. Flagged/fail examples include `optimal_static_bst_subquadratic`, `dynamic_disconnected_planar_point_location`, `dynamic_orthogonal_range_reporting_update_exponent`, `deferred_work_io_tradeoff`, `cache_oblivious_implicit_scanning`, `succinct_compressed_structures`, `dynamic_min_tree_cut`, `kinetic_high_dim_extent`, `dynamic_text_indexing`, and `concurrent_shi_cell_capacity`. |
| 4 | Under-attendedness scores on anchored scale | Mixed | The lexicographic table is directionally plausible, but `dynamic_connectivity_level_elimination` at 4 and `higher_dim_rectangle_stabbing_word_ram_linear_space` at 4 are aggressive because their parent areas are active. `path_compression_topdown` and `karp_rabin_collision_detection` at 5 depend on the exact named problem having very few mentions, not on the broader areas being neglected. |
| 5 | 24-month freshness check for every candidate | No | Every subrun candidate has a freshness paragraph, but not every synthesis-ranked incumbent has a v2-uniform 24-month log with search terms and sources. Some existing folders have access dates or newer-work notes, not the full v2 freshness template. |
| 6 | Exact sources, search terms, and date searched for every serious candidate and rejection | Partial | The subruns are strong here. Existing candidate folders are weaker: `sources.yaml` usually records URLs and access dates but not search terms or date-searched logs. New pass-ranked slugs have no folder metadata at all. |
| 7 | Sparse or empty pools reported | Pass | `2B` returned only one viable candidate and `2R` returned three. `2A` returned four. This argues against pure padding. |
| 8 | Rejection ledger in every subrun | Pass | All five subruns include rejection ledgers. `2I` was especially useful because it distinguished exact checkers from evolvable objects. |
| 9 | Feasibility gate before lexicographic ranking | Pass | The synthesis gates in Section 2 before primary ranking in Section 3. |
| 10 | Actual lexicographic ranking rather than averaging | Mostly pass | The primary theorem table is lexicographic by under-attendedness, AI-collab fit, then theorem fit. The `path_compression_topdown` versus `karp_rabin_collision_detection` tie is only described as "nearly tied"; it should be called an actual tie on visible scores unless an external tie-breaker is named. |
| 11 | Hidden anchoring on STT LP | Pass | STT LP drops from old top-20 rank 1 to primary rank 3, and the synthesis explicitly treats old rank as informational. |
| 12 | Overcorrection against STT LP | Pass | STT LP remains rank 3 primary, rank 1 pilot-readiness, and high in OpenEvolve. It was not punished merely for being incumbent. |
| 13 | Promotion from weak secondary source without primary support | Mixed | `optimal_static_bst_subquadratic` is correctly flagged, not promoted. `list_update` gets current support partly from a 2024 Cambridge chapter rather than a new primary closure sweep. Several incumbents need primary-source refresh before theorem promotion. |
| 14 | OpenEvolve ranking requires concrete evolvable object | Patched to pass | The original synthesis ranked `karp_rabin_collision_detection` despite `2I` rejecting it as not object-first. After patch, the remaining OpenEvolve side-experiment ranking uses concrete objects: policies, inequalities, adversaries, heap rules, probing witnesses, or range-mode grammars. |
| 15 | Folder population and skeptical audit before pilot-ready | Fail for new pass slugs | `dynamic_connectivity_level_elimination`, `higher_dim_rectangle_stabbing_word_ram_linear_space`, `randomized_linear_list_labeling_lower_bound`, `lz77_linear_compressed_matching`, and `dynamic_planar_nearest_neighbor_logarithmic_full` are pass-ranked without folders, `score.yaml`, `sources.yaml`, or standalone skeptical audits. They are rankable leads, not pilot-ready candidates. |
| 16 | Stopping condition | Pass | All planned v2 subruns listed in the framework are complete within the five-calendar-day budget. Stop; do not continue into v3 under this branch. |
| 17 | Theorem pilot chosen by primary ranking plus gate | Pass with caveat | The synthesis chooses `path_compression_topdown`, the first feasibility-gated primary-ranked candidate. Caveat: `path_compression_topdown` and `karp_rabin_collision_detection` are tied on visible primary scores, and `path_compression_topdown` needs the exact recurrence copied before a blind run. |
| 18 | Separate OpenEvolve side experiment | Pass | The synthesis separately recommends `list_update`, and that survives object/evaluator audit. |
| 19 | DS(k,1) interruption recommendation | Pass | The synthesis says not to interrupt DS(k,1). The evidence is not strong enough for an immediate pivot; any theorem-pilot switch belongs in a later control-panel decision. |

## Candidate-Level Audit

### `path_compression_topdown`

- Synthesis role: primary theorem rank 1 and recommended later theorem pilot.
- Evidence: explicit 2025 Tarjan/Dagstuhl proof problem plus Seidel-Sharir primary source.
- Strongest objection: this is not an open data-structure bound; it is proof archaeology/formalization. It is a good AI proof task only after the exact recurrence and Ackermann normalization are copied into the folder.
- Score concern: under-attendedness 5 is defensible for the exact proof-translation problem, but intellectual interest and theorem-project suitability should not be confused with field-level impact.
- Pilot-readiness: not ready until `frontier.md` and `blind_prompt.md` include the exact recurrence.
- Audit verdict: control-panel option only; no DS(k,1) interruption.

### `karp_rabin_collision_detection`

- Synthesis role: primary theorem rank 2 and pilot-readiness rank 2.
- Evidence: explicit 2025 Farach-Colton/Dagstuhl problem.
- Strongest objection: deterministic exact detection and allowed randomized false rejection are different variants; a search under stringology/fingerprint terminology could find a hidden closure or sharper known reduction.
- OpenEvolve concern: exact oracle is strong, but object-first OpenEvolve is weaker than for `list_update`; this was patched out of the OpenEvolve side-experiment ranking.
- Audit verdict: strong later theorem/algorithm pilot candidate, but not a reason to stop DS(k,1).

### `search_trees_on_trees_lp`

- Synthesis role: primary theorem rank 3, pilot-readiness rank 1, OpenEvolve rank 2 after the Karp-Rabin patch.
- Evidence: 2025 Sadeh-Kaplan-Zwick explicit static STT open problem and strong certificate infrastructure.
- Strongest objection: Golinsky's original LP source remains TODO verified, and small-case LP enumeration can overfit badly.
- Anchoring audit: no hidden anchoring found. It remains highly ranked because certificate artifacts are real, not because it was incumbent.
- Audit verdict: strongest foreground-continuation argument for the existing STT lane; continue DS(k,1) unless control panel decides otherwise.

### `unified_bound_heaps`

- Synthesis role: primary theorem rank 4.
- Evidence: explicit 2025 Iacono/Dagstuhl pointer-model working-set heap with constant `decrease-key` target.
- Strongest objection: exact working-set variant and pointer-model boundary are not yet fixed enough; non-pointer and Dijkstra/universal-optimality heap results can create fake gaps.
- Audit verdict: viable theorem lead after definition cleanup, not pilot-ready.

### New Pass-Ranked Slugs Without Folders

These are the biggest source-governance defect in v2. The synthesis can rank them as leads, but they must not be treated as pilot-ready until folder population and skeptical audits exist.

| Slug | Main risk | Required repair before promotion |
| --- | --- | --- |
| `dynamic_connectivity_level_elimination` | Dynamic connectivity is saturated; full batch-dynamic manuscript not located; small simulators can miss cutset independence. | Create folder; extract exact KKM/Liu-King framework; audit whether "level data structure" has a formal standalone theorem target. |
| `higher_dim_rectangle_stabbing_word_ram_linear_space` | Higher-dimensional word-RAM target is explicit but technically central range-searching work, not obviously under-attended at score 4. | Create folder; fix dimension, space, word size, and target query bound; check 2024-2026 rectangle-stabbing/orthogonal-point-location follow-ups. |
| `randomized_linear_list_labeling_lower_bound` | Not pure cell-probe; the source calls it a major open problem, so under-attendedness is moderate at best. | Create folder; fix adversary/randomization model; separate file-maintenance/list-labeling from list-update. |
| `lz77_linear_compressed_matching` | Split from `succinct_compressed_structures`; exact LZ model and grammar-conversion implications are unresolved. | Create folder or explicit split note; compare CPM 2025/RLSLP and 2026 grammar-access work before promotion. |
| `dynamic_planar_nearest_neighbor_logarithmic_full` | Classic central geometry problem; recent 2025 progress may mean remaining case is technically saturated. | Create folder; separate fully dynamic exact Euclidean NN from insertion-only, offline, approximate, and 3D hull variants. |

### Flagged And Failed Leads

The flagged/fail choices are mostly justified, and the audit should resist re-promoting them.

| Slug | Audit stance |
| --- | --- |
| `dynamic_disconnected_planar_point_location` | Keep flagged. Open status is inferred and could be closed under ray-shooting/trapezoidal-map terminology. |
| `dynamic_orthogonal_range_reporting_update_exponent` | Keep flagged. The update-exponent gap is inferred from old JoCG/SoCG bounds; freshness is weak. |
| `deferred_work_io_tradeoff` | Keep flagged. Fresh idea, but Dagstuhl HTML lacks formal parameters and no manuscript was found. |
| `cache_oblivious_implicit_scanning` | Keep flagged. Only the strict exact-`n`-cell implicit model survives; broad scan claims are stale. |
| `imprecise_comparison_sorting` | Keep flagged for DS scouting. Excellent finite game, but not clearly a data-structure object. |
| `succinct_compressed_structures` | Keep flagged until split. Grammar/DAG sampling has a 2026 freshness warning; LZ matching should be separate. |
| `optimal_static_bst_subquadratic` | Keep flagged. Stale 2003 page with no last-24-month primary confirmation. |
| `splay_preorder_231` | Keep flagged. Good rediscovery benchmark, severe saturation, modern nearby results make the exact residual fragile. |
| `dynamic_min_tree_cut` | Keep failed. Dynamic min-cut progress and unclear standalone statement make it unsafe. |
| `kinetic_high_dim_extent` | Keep failed. Too broad; no single 3D measure/motion model has current source support. |
| `dynamic_text_indexing` | Keep failed. Old compressed-index open claim is stale and model-sensitive. |
| `concurrent_shi_cell_capacity` | Keep failed. The one-key/two-key framing is likely wrong after STOC 2025 source extraction. |

## Source-Provenance Audit

Subrun-level provenance is substantially better than the older candidate folders. Each subrun records exact sources, search terms, dates searched, and rejection ledgers. The defect is portability: most new v2 leads live only inside subrun markdown, not in `candidate_topics/<slug>/sources.yaml`, `score.yaml`, `problem.md`, and `skeptical_audit.md`.

Existing folders also do not uniformly record v2-style `freshness_check_24_months` blocks. Access dates are not enough. A future promotion should require:

- exact source metadata in `sources.yaml`;
- search terms and date searched;
- `open_status` using the v2 explicit/inferred/uncertain/likely-solved vocabulary or a clearly mapped local equivalent;
- a skeptical audit with falsifiers;
- a separate OpenEvolve object/evaluator statement if OpenEvolve suitability is above 2.

## Rejection-Ledger Audit

| Subrun | Ledger adequacy | Adversarial note |
| --- | --- | --- |
| `2A_geometry` | Adequate | Good duplicate and likely-solved handling. The inferred geometry leads should stay flagged until terminology sweeps are deeper. |
| `2B_cell_probe_lower_bounds` | Adequate | Sparse pool is credible. It correctly rejects saturated or likely closed Boolean/cell-probe frontiers. |
| `2F_author_problem_pages` | Adequate | Best at source updates, but old author pages remain dangerous. `optimal_static_bst_subquadratic` is correctly not promoted. |
| `2I_openevolve_objects` | Strong after patch | It correctly requires mutable objects. The synthesis initially violated this with Karp-Rabin; patched. |
| `2R_v1_area_remining` | Adequate | Good at downgrading broad v1 folders and catching the 2026 grammar-compression freshness warning. |

## Non-Interruption Audit

The synthesis does not claim that v2 supersedes STT or DS(k,1). It explicitly says a pivot requires later control-panel review and that DS(k,1) should continue foreground. This audit agrees.

The strongest reason not to interrupt is methodological, not emotional inertia: the only candidate with better primary under-attendedness than STT is either proof-expository (`path_compression_topdown`) or algorithm/stringology rather than the current STT theorem lane (`karp_rabin_collision_detection`). STT LP remains the best prepared certificate-bearing theorem infrastructure, and DS(k,1) is the active proof lane inside that infrastructure.

OpenEvolve should be separated cleanly: run `list_update` as a side experiment if resources allow, with exact finite games and certificates. Do not let it consume the theorem lane unless it produces an unexpectedly strong artifact.
