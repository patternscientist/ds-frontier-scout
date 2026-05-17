# Scouting v2 Closeout

Status: complete closeout for Scouting v2.

Date closed: 2026-05-17.

Branch: `scouting-v2-closeout-v0`.

Scope: this document closes Scouting v2 using only the completed local subruns, synthesis, adversarial audit, top-20 shortlist, and candidate matrix. It does not start Scouting v3, add candidates, create candidate folders, or promote any lead beyond what `adversarial_audit.md` supports.

## Final Verdict

Scouting v2 is useful background triage, but it does not justify interrupting the active STT / DS(k,1) proof lane. The correct foreground decision is: continue DS(k,1), keep Scouting v2 as a decision artifact, and require later control-panel approval before any theorem-pilot pivot or side experiment.

The most important v2 outputs are:

- Foreground remains `search_trees_on_trees_lp` / DS(k,1).
- Later theorem-pilot options are `path_compression_topdown` and `karp_rabin_collision_detection`.
- The clean OpenEvolve side-experiment option is `list_update`.
- Several new pass-ranked v2 leads are only leads until folder population and skeptical audits exist.
- The audit's flagged and failed candidates should stay flagged or failed unless a new primary-source event changes their status.

## Why DS(k,1) Remains Foreground

The audit found no hidden anchoring problem in keeping DS(k,1) foreground. `search_trees_on_trees_lp` remains the best prepared theorem infrastructure because it already has certificate-shaped artifacts: STT enumeration, LP witnesses, rational certificates, topology generators, and inequality checks. Its pilot-readiness is stronger than the new v2 leads even though it is not the most literally under-attended topic.

The alternatives above it in the v2 primary ranking do not force an interruption. `path_compression_topdown` is a proof-exposition/formalization problem, not a new data-structure bound. `karp_rabin_collision_detection` is crisp and source-supported, but is a stringology/algorithm pilot with variant-risk around deterministic collision detection versus randomized false rejection. Neither provides stronger immediate evidence than the active DS(k,1) proof lane.

Control-panel implication: continue DS(k,1) unless a later chat explicitly decides to run a small theorem pilot elsewhere.

## Later Theorem-Pilot Options

`path_compression_topdown` is the first later theorem option under the v2 lexicographic ranking. It is attractive because the exact 2025 Tarjan/Dagstuhl proof-translation problem is very under-attended and has a strong staged-proof/Lean shape. It is not ready for a blind run until the exact Seidel-Sharir recurrence and Ackermann normalization are copied into the candidate folder/frontier material. Do not describe it as a new union-find bound.

`karp_rabin_collision_detection` is the fallback theorem option if the control panel decides `path_compression_topdown` is too expository for the theorem lane. It has a compact statement and exact small-instance oracles. Before promotion, separate deterministic exact collision detection from the randomized false-rejection variant, and search stringology/fingerprint terminology for hidden closure.

## Side-Experiment Option

`list_update` is the OpenEvolve side-experiment that survives the audit. It has the cleanest mutable object/evaluator pair: finite-state randomized online policies and adversarial request generators, evaluated against exact offline optimum or work-function games on small lists.

This should be a side experiment only. The deliverables should be policy tables, adversarial traces, finite-game LP/DP certificates, and careful notes on whether any finite behavior generalizes. Do not let it consume the theorem lane unless it produces an unexpectedly strong certificate.

## Leads Requiring Folder Population Before Promotion

The largest governance defect in Scouting v2 is that several new pass-ranked slugs appear in synthesis without `candidate_topics/<slug>/` folders, `score.yaml`, `sources.yaml`, and standalone skeptical audits. They may remain rankable leads, but they are not pilot-ready.

Before promoting any of these, create the folder and populate:

- `problem.md` with the exact scoped problem statement;
- `sources.yaml` with stable identifiers, access dates, search terms, and date searched;
- `score.yaml` with separated theorem, OpenEvolve, and intellectual-interest scores;
- `skeptical_audit.md` with not-open, saturation, evaluator, falsifier, and required-source checks;
- if relevant, `blind_prompt.md`, `frontier.md`, and `openevolve_fit.md`.

Affected leads: `dynamic_connectivity_level_elimination`, `higher_dim_rectangle_stabbing_word_ram_linear_space`, `randomized_linear_list_labeling_lower_bound`, `lz77_linear_compressed_matching`, and `dynamic_planar_nearest_neighbor_logarithmic_full`.

## Stay Flagged Or Failed

Keep the following flagged unless primary-source checks repair the exact issue named by the audit: `dynamic_disconnected_planar_point_location`, `dynamic_orthogonal_range_reporting_update_exponent`, `deferred_work_io_tradeoff`, `cache_oblivious_implicit_scanning`, `imprecise_comparison_sorting`, `succinct_compressed_structures`, `optimal_static_bst_subquadratic`, and `splay_preorder_231`.

Keep the following failed unless a new primary-source event creates a crisp residual: `dynamic_min_tree_cut`, `kinetic_high_dim_extent`, `dynamic_text_indexing`, and `concurrent_shi_cell_capacity`.

## Control-Panel Decision Table

| Candidate | Role | Required next action | Do-not-overclaim warning |
| --- | --- | --- | --- |
| `search_trees_on_trees_lp` / DS(k,1) | foreground | Continue current proof lane; reproduce/check certificate artifacts as planned. | Do not treat small LP enumeration as proof of the general case. |
| `path_compression_topdown` | later theorem option | Extract exact recurrence and Ackermann normalization before blind/frontier prompts. | Do not call it a new data-structure bound; it is proof translation/formalization. |
| `karp_rabin_collision_detection` | later theorem option | Separate deterministic and randomized variants; check alternate stringology terminology before promotion. | Do not treat a strong small oracle as enough for OpenEvolve promotion or closure evidence. |
| `list_update` | side experiment | Build exact finite-list evaluator and emit policy/adversary certificates. | Do not infer arbitrary-list competitive ratios from small finite games. |
| `dynamic_connectivity_level_elimination` | flagged lead | Create candidate folder; extract KKM/Liu-King framework and exact "level data structure" target. | Do not claim dynamic connectivity is under-attended; only this narrow simplification might be. |
| `higher_dim_rectangle_stabbing_word_ram_linear_space` | flagged lead | Create candidate folder; fix dimension, word-size, space, and target query bound; refresh 2024-2026 follow-ups. | Do not overstate under-attendedness of the broader range-searching area. |
| `randomized_linear_list_labeling_lower_bound` | flagged lead | Create candidate folder; fix randomized/adversary/amortized model and finite-game evaluator. | Do not merge list labeling with list update or deterministic file-maintenance results. |
| `lz77_linear_compressed_matching` | flagged lead | Create candidate folder or explicit split note from `succinct_compressed_structures`; fix exact LZ model. | Do not assume grammar/RLSLP progress transfers without checking conversion costs. |
| `dynamic_planar_nearest_neighbor_logarithmic_full` | flagged lead | Create candidate folder; separate fully dynamic exact Euclidean NN from insertion-only/offline/approximate variants. | Do not ignore 2025 partial progress or central-geometry saturation. |
| `dynamic_disconnected_planar_point_location` | flagged lead | Run terminology sweep under point location, ray shooting, trapezoidal maps, and planar maps. | Do not promote from inferred open status. |
| `dynamic_orthogonal_range_reporting_update_exponent` | flagged lead | Refresh the word-RAM reporting literature and isolate an explicit update-exponent statement. | Do not present the old exponent gap as current without a modern source. |
| `deferred_work_io_tradeoff` | flagged lead | Locate full Afshani-Brodal-Sitchinava-style parameters or another primary manuscript. | Do not promote from mangled Dagstuhl HTML alone. |
| `cache_oblivious_implicit_scanning` | flagged lead | Verify the strict exact-`n`-cell implicit range-scan model against later implicit dictionary work. | Do not make broad cache-oblivious scanning claims. |
| `imprecise_comparison_sorting` | flagged lead | Use only if the project wants a non-DS finite-game benchmark after model refresh. | Do not treat it as an object-first data-structure candidate. |
| `succinct_compressed_structures` | flagged lead | Split LZ matching from grammar/DAG sampling; compare grammar/DAG side to 2026 random-access work. | Do not keep the bundled folder as a single promoted theorem target. |
| `optimal_static_bst_subquadratic` | flagged lead | Do a modern fine-grained/DP source sweep before any scoring or blind prompt. | Do not promote from the stale 2003 project page. |
| `splay_preorder_231` | flagged lead | Check post-2025 arbitrary-initial-tree Splay preorder status; use only as rediscovery/background. | Do not ignore severe saturation or transfer Greedy/offline-OPT facts to Splay. |
| `dynamic_min_tree_cut` | failed lead | Read 2025/2026 dynamic min-cut work before isolating any standalone residual. | Do not treat the current formulation as crisp or current. |
| `kinetic_high_dim_extent` | failed lead | Narrow to one 3D measure/motion model and find a current primary source. | Do not promote the broad kinetic-extent bundle. |
| `dynamic_text_indexing` | failed lead | Reconcile old dynamic compressed-index claims with modern self-index/signature-encoding work. | Do not use stale 2007-style claims as current open status. |
| `concurrent_shi_cell_capacity` | failed lead | First extract the exact STOC 2025 model and residual, if any. | Do not use the one-key/two-key framing; the audit says it is likely wrong. |

## Handoff Rule

A future control-panel chat should read this file first. It should only reopen the full Scouting v2 subruns when it needs source provenance, exact search terms, or candidate-specific audit details. The default post-v2 action is not more scouting; it is continuing DS(k,1), with optional later review of `path_compression_topdown`, `karp_rabin_collision_detection`, and the `list_update` side experiment.
