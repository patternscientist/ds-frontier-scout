# Scouting Batch 002 Adversarial Audit

Date: 2026-05-15

Purpose: try to disqualify, downgrade, sharpen, or reframe every Batch 002 lead. This is intentionally hostile to promotion.

## Executive Downgrades

- `persistent_arrays` is downgraded to discard/background as originally stated. Straka's paper is titled and abstracted as giving optimal worst-case access and update time, so the blind target "linear space and worst-case O(log log m)" is likely already answered by the cited source. Only a bibliographic/formalization task remains unless a stricter model is isolated.
- `history_independent_allocation` is downgraded sharply. Naor-Teague's 2001 variable-size allocation open problem is not a safe current open claim after the FOCS 2023 paper "Strongly History-Independent Storage Allocation." Residual exact overhead/model tradeoffs may exist, but the Batch 002 claim is stale.
- `dynamic_text_indexing` is downgraded to background until the model is separated from known dynamic compressed self-index work, especially signature-encoding/compressed-index results. A toy evaluator would be misleading for the bit-space claim.
- `kinetic_high_dim_extent`, `all_purpose_hashing_residual`, `retroactive_lower_bounds`, `history_independent_concurrent_hashing`, and `dynamic_stream_mincut_space` are not promotion-ready. They are source-gathering lanes, not theorem targets.
- `range_mode_queries` and `imprecise_comparison_sorting` remain the best Batch 002 candidates after audit, but both need narrower statements and modern citation sweeps before top-shortlist promotion.

## Candidate Decisions

### `range_mode_queries`

- Open-problem claim: explicit/inferred and still plausible, but the exact modern frontier is not the simple `O(sqrt n)` vs logarithmic gap stated in the blind prompt.
- Newer/source check: Chan et al. remain a primary anchor. Later papers and surveys discuss static/dynamic/approximate range-mode variants; I did not find a closure of the linear-space exact query-time gap, but the known upper-bound wording should be `O(sqrt(n / log n))`-style where applicable, not merely `O(sqrt n)`.
- Saturation: moderate. Range searching is mature; exact range mode is narrower and less saturated than general range-reporting lower bounds.
- Smallest meaningful subproblem: linear-word static exact range mode under word-RAM rank/select assumptions; prove a lower bound or improvement for a named block/candidate-list framework.
- Best use: `OpenEvolve_project`, with theorem sidecar.
- Score action: slight downgrade/clarification, not disqualification.
- Weak sources/notes: range alpha-majority is adjacent and should not be bundled as evidence for exact range mode.
- Blind-prompt warning: it asks to "improve on O(sqrt n)" even though the audited frontier should mention stronger known refinements. Mark as stale, not fatal.

### `persistent_arrays`

- Open-problem claim: likely solved/stale as stated.
- Newer/source check: the Batch 002 source itself is the problem: Straka's "Fully persistent arrays with optimal worst-case access and update time" appears to claim the exact target, and the abstract says it presents the first worst-case optimal implementation.
- Saturation: low, but because the candidate is likely not open, low saturation does not help.
- Smallest meaningful subproblem: formalize Dietz/Straka model assumptions, or search for a stricter purely functional/pointer-machine/cache-oblivious variant with an explicit open statement.
- Best use: `background_context` or `Lean_formalization_project` for existing results; discard as an open theorem target.
- Score action: major downgrade.
- Weak sources/notes: secondary summaries caused the false open claim. The primary Straka PDF/thesis must be treated as a potential solution, not support for openness.
- Blind-prompt warning: it asks for a known-or-likely-known result as if open.

### `dynamic_text_indexing`

- Open-problem claim: explicit in the 2007 source, but stale and model-dependent.
- Newer/source check: dynamic compressed text-index papers after 2007, including dynamic compressed self-indexes using signature encodings, appear to solve nearby update/search goals in compressed-space measures. They do not automatically prove the exact `O(|T|)` bits single-text target, but they make the Batch 002 statement too broad.
- Saturation: medium-high. Dynamic string indexing and compressed indexing have substantial literature.
- Smallest meaningful subproblem: choose static alphabet, bit model, online substring insertion/deletion, worst-case vs amortized update time, and whether "linear bits" means `O(|T| log sigma)` or entropy/compressed space.
- Best use: `background_context` until narrowed.
- Score action: downgrade OpenEvolve fit. Exact small-string oracles test correctness, not compactness or asymptotic compressed-space guarantees.
- Weak sources/notes: ResearchGate/snippet source is weak; use ACM/TALG and later primary papers.
- Blind-prompt warning: acceptable as a broad exploration prompt, but not a verified open theorem target.

### `history_independent_allocation`

- Open-problem claim: explicit in Naor-Teague 2001, stale in current form.
- Newer/source check: FOCS 2023 "Strongly History-Independent Storage Allocation" directly addresses history-independent storage allocation with variable-sized blocks. That does not settle every overhead variant, but it disqualifies the Batch 002 claim that the Naor-Teague open problem can be promoted unchanged.
- Saturation: medium. The niche is small but the exact problem has modern direct attention.
- Smallest meaningful subproblem: residual tradeoffs for strong history independence with deamortized/worst-case operations, exact fragmentation bounds, or a restricted block/RAM model not handled by the 2023 paper.
- Best use: `background_context` until residuals are extracted from the 2023 paper.
- Score action: major downgrade.
- Weak sources/notes: Naor-Teague alone is too stale for current open status.
- Blind-prompt warning: likely presents a solved/narrowed problem as open.

### `history_independent_concurrent_hashing`

- Open-problem claim: partially resolved by the cited 2025 paper.
- Newer/source check: the cited 2025 concurrent hash-table paper is already a solution paper, not just an open-problem statement. Residual cell-capacity/progress-condition gaps need extraction.
- Saturation: medium-high because it is very recent and author-active.
- Smallest meaningful subproblem: model-check tiny linearizable strongly history-independent dictionaries under a fixed cell capacity/progress condition.
- Best use: `Lean_formalization_project` or background.
- Score action: do not create/promote a candidate.
- Weak sources/notes: any broad "concurrent SHI dictionaries are open" claim is too weak after 2025.

### `kinetic_high_dim_extent`

- Open-problem claim: uncertain/broad, mostly inferred from classic KDS context.
- Newer/source check: no closure was found in a quick sweep, but the candidate is too broad because "convex hull, diameter, width, or extent in dimension >2" contains many different problems.
- Saturation: low-medium but old; risk is vagueness, not hype.
- Smallest meaningful subproblem: 3D kinetic diameter or width for bounded-degree algebraic motion with explicit event bound target.
- Best use: `background_context`.
- Score action: slight downgrade and keep unpromoted.
- Weak sources/notes: handbook/classic-survey pointers are not enough; need line-level statements from Basch-Guibas-Hershberger or Agarwal-Guibas-Hershberger-Veach.
- Evaluator warning: finite event simulations can find examples, but they cannot certify asymptotic KDS bounds.

### `imprecise_comparison_sorting`

- Open-problem claim: explicit in Ajtai-Feldman-Hassidim-Nelson; modern status still uncertain after a quick search.
- Newer/source check: I did not find a primary closure of randomized `O(n)` error-2 maximum or randomized error-`k` sorting. Noisy sorting literature is adjacent but model assumptions differ.
- Saturation: low-medium; not a classic data-structure flagship.
- Smallest meaningful subproblem: randomized error-2 maximum under adversarial unresolved comparisons, with success probability and comparison budget fixed.
- Best use: `OpenEvolve_project`.
- Score action: keep high but mark confidence medium, not high.
- Weak sources/notes: follow-up sweep must separate imprecise-comparison, noisy-comparison, tournament, and interval-order models.
- Evaluator warning: small randomized strategies may overfit finite `n`; use adversary LPs/certificates rather than only Monte Carlo search.

### `dynamic_min_tree_cut`

- Open-problem claim: plausible but inferred through a dynamic-min-cut bottleneck; not a clean standalone source statement yet.
- Newer/source check: SODA 2025/2026 dynamic min-cut progress changes the baseline. I did not see evidence that it closes polylogarithmic min-tree-cut, but this area is too active for a broad claim.
- Saturation: high.
- Smallest meaningful subproblem: dynamic min-tree-cut for an explicit maintained tree, unweighted graph, fully dynamic edge updates, and a specified update/query model.
- Best use: `background_context` or tightly scoped `OpenEvolve_project` for adversarial trace generation.
- Score action: downgrade from candidate-grade 7.1 to a narrower/high-risk 6-ish score.
- Weak sources/notes: SIAM proceedings links are context until full paper details are checked; do not claim recent work leaves the exact subroutine open without reading it.
- Evaluator warning: simulators can test candidate summaries but cannot validate worst-case update bounds.

### `dynamic_stream_mincut_space`

- Open-problem claim: explicit in ITCS 2025 Open Question 15, but it is a streaming lower-bound problem rather than a data-structure candidate.
- Newer/source check: no closure found in this audit.
- Saturation: medium-high due to active cut-sketching/streaming literature.
- Smallest meaningful subproblem: one-pass turnstile/simple weighted graph `(1+epsilon)` min-cut space lower bound under a named communication game.
- Best use: `background_context`, not promoted candidate.
- Score action: keep inside `dynamic_graph_structures` notes only.
- Evaluator warning: finite sketch games can suggest distributions, but lower bounds need communication-complexity proof machinery.

### `range_alpha_majority_output_sensitive`

- Open-problem claim: explicit in older range-majority work but not verified as current.
- Newer/source check: later range-majority/colored range-reporting work likely changes the exact frontier; no promotion without a dedicated sweep.
- Saturation: medium.
- Smallest meaningful subproblem: output-sensitive reporting for fixed alpha regime with precise space target.
- Best use: background/context for `range_mode_queries`.
- Score action: do not promote separately.
- Weak sources/notes: not evidence for exact range-mode openness.

### `all_purpose_hashing_residual`

- Open-problem claim: uncertain/residual, not explicit enough.
- Newer/source check: All-Purpose Hashing and the optimal time/space tradeoff paper are solution/frontier papers. Without a single unsolved theorem, this is too easy to misstate.
- Saturation: high for recent hash-table theory.
- Smallest meaningful subproblem: one model-specific tradeoff, e.g. stable addresses plus succinct wasted space plus very-high-probability operations under a named hashing assumption.
- Best use: `background_context`.
- Score action: do not promote; leave `hashing_dictionaries` as TODO/context.
- Weak sources/notes: "all properties at once" is historical motivation, not a current open problem after Iceberg hashing.

### `retroactive_lower_bounds`

- Open-problem claim: inferred/uncertain. Recent conditional lower bounds do not by themselves imply an explicit open unconditional cell-probe target.
- Newer/source check: Chung-Demaine-Hendrickson-Lynch gives strong conditional lower bounds for retroactive structures; the remaining target needs a primary source.
- Saturation: low-medium, but lower-bound difficulty is high.
- Smallest meaningful subproblem: explicit separation for a named dynamic problem and retroactivity type under either unconditional cell-probe or a stated conjecture.
- Best use: `background_context`.
- Score action: do not promote.
- Weak sources/notes: Demaine-Iacono-Langerman is a classic transformations paper; do not confuse known transformations/known lower bounds with an open strengthening.

## Promotions After Audit

Keep as promising but narrowed:

- `range_mode_queries`: good OpenEvolve-first candidate if the prompt is updated to the modern upper-bound frontier and kept to exact static range mode.
- `imprecise_comparison_sorting`: good finite-combinatorial candidate if model distinctions are policed.

Keep as background or source-gathering:

- `dynamic_text_indexing`
- `dynamic_min_tree_cut`
- `kinetic_high_dim_extent`
- `dynamic_stream_mincut_space`
- `range_alpha_majority_output_sensitive`
- `all_purpose_hashing_residual`
- `retroactive_lower_bounds`
- `history_independent_concurrent_hashing`

Disqualify or discard as originally stated:

- `persistent_arrays`
- `history_independent_allocation`

## Source Reliability Notes

- Primary sources with explicit open statements: Ajtai-Feldman-Hassidim-Nelson for imprecise comparisons; ITCS 2025 min-cut streaming question; older Naor-Teague for historical allocation status only.
- Primary sources that undermine Batch 002: Straka 2009 for persistent arrays; FOCS 2023 history-independent storage allocation for variable-size allocation.
- Weak or incomplete sources: ResearchGate snippets for dynamic text indexing; handbook-level kinetic KDS summaries; broad All-Purpose Hashing motivation; inferred retroactive lower-bound gaps.

