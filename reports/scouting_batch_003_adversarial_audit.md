# Scouting Batch 003 Adversarial Audit

Date: 2026-05-15

Purpose: hostile review of the five Batch 003 mini-frontiers and the STT LP certificate schema. This audit tries to disqualify, downgrade, sharpen, or reframe the candidates; it is not a promotion document.

## Executive Verdict

Batch 003 over-scored evaluator readiness. None of the five candidates should dislodge `search_trees_on_trees_lp` as the fixed-point pilot.

- `dynamic_stream_mincut_space`: survives as an explicit open problem, but is lower-bound-heavy and only weakly evaluator-friendly.
- `directed_roundtrip_compact_routing`: survives as explicit, but it is active compact-routing theory rather than an under-attended data-structure residual; OpenEvolve fit is poor.
- `concurrent_shi_cell_capacity`: downgraded sharply. The Batch 003 formulation likely misstates the cell-capacity residual; the source lower-bounds two-element cells under stronger progress assumptions.
- `connected_circle_segment_queries`: survives as a narrow geometry lead, but only the lower-bound/tradeoff part is a clean theory problem. Construction/fractional-cascading ideas partly read as implementation future work.
- `cache_oblivious_implicit_scanning`: survives only in the strict exact-`n`-cell implicit model. Broad "cache-oblivious scanning remains open" language is stale.

## Candidate Audits

### dynamic_stream_mincut_space

Open status: explicit. Ding et al. ITCS 2025 Open Question 15 asks for the exact one-pass dynamic-stream space complexity of `(1+epsilon)` approximate min-cut in simple weighted graphs.

Newer-work check: quick search found no primary closure. Dynamic graph min-cut papers from SODA 2025/2026 are about update-time algorithms, not one-pass turnstile sketches. A Waterloo seminar abstract says the paper resolves the streaming min-cut question, but the ITCS paper itself separates insertion-only results from the dynamic-stream open question.

Required distinctions:

- insertion-only versus turnstile/dynamic streams;
- simple weighted undirected graphs versus multigraph/arbitrary graph encodings;
- randomized versus deterministic algorithms;
- exact min-cut versus `(1+epsilon)` value approximation;
- min-cut value sketches versus full cut sparsifiers;
- `~Omega(n/epsilon)` insertion-only lower bound versus `~O(n/epsilon^2)` dynamic-stream sparsifier upper bound.

Smallest meaningful subproblem: randomized one-pass turnstile streams over simple weighted undirected graphs, outputting only the min-cut value, with a target separation between `~O(n/epsilon)` and `~O(n/epsilon^2)`.

Best use: theorem_project. OpenEvolve can generate toy hard distributions, but finite sketch collisions do not establish the asymptotic communication lower bound.

Score action: `overall_score` 7.2 -> 6.8; `openevolve_suitability` 4 -> 3; `saturation_risk` medium -> medium_high.

### directed_roundtrip_compact_routing

Open status: explicit. Kadria and Roditty arXiv v3 / DISC 2025 ask for the best stretch of weighted directed compact roundtrip routing with `~O(n^{1/k})` local storage.

Newer-work check: arXiv v3 is dated 2025-08-31. Quick search found no later primary source closing general directed `k`.

Required distinctions:

- routing schemes versus distance oracles, labels, spanners, and emulators;
- local routing tables plus destination labels plus packet headers versus labels alone;
- weighted versus unweighted directed graphs;
- strongly connected directed graphs;
- topology-dependent versus name-independent models;
- actual routed-path stretch versus estimated roundtrip distance.

Smallest meaningful subproblem: the directed weighted `k=4` case with `~O(n^{1/4})` local storage, asking for any real routing stretch improvement over the inherited `4k+epsilon`-style scheme.

Best use: theorem_project/background_context. Finite graph search can falsify proposed local rules but is weak for discovering or certifying asymptotic compact-routing schemes.

Score action: `overall_score` 6.6 -> 6.2; `openevolve_suitability` 2 -> 1; `saturation_risk` medium_high -> high.

### concurrent_shi_cell_capacity

Open status: inferred and fragile. The source is strong, but the residual is not stated as a standalone open problem.

Evidence causing downgrade: the arXiv/STOC 2025 abstract says the positive construction is lock-free, SQHI, LL/SC-based, and stores two elements plus two bits per cell. It also says no history-independent concurrent dictionary with wait-free membership queries and obstruction-free insertions/deletions can store only two elements plus `O(1)` bits per memory cell, even for two processes and unbounded step complexity. That conflicts with Batch 003's "lower bounds for one-element cells" summary and makes the one-key-versus-two-key formulation suspect.

Required distinctions:

- one element per cell versus two elements/lookahead per cell;
- LL/SC versus CAS/register base objects;
- lock-free versus obstruction-free versus wait-free;
- wait-free membership queries versus wait-free updates;
- SQHI versus stronger concurrent history independence;
- specific Robin-Hood/open-addressing hash table versus arbitrary dictionary.

Smallest meaningful subproblem: formalize the exact two-process lower-bound model and ask whether the positive lock-free two-element LL/SC construction can support stronger wait-free lookup/progress guarantees without extra representation leakage.

Best use: Lean_formalization_project or background_context. Do model extraction first; do not run theorem prompts against the current one-key blind prompt.

Score action: `overall_score` 6.2 -> 5.1; `open_status_confidence` medium -> low; `openevolve_suitability` 2 -> 1; `saturation_risk` medium -> medium_high.

### connected_circle_segment_queries

Open status: explicit but mixed. The ISAAC 2025 future-work section explicitly asks for lower bounds on data-size/query-time tradeoffs in the connected-graph setting. The construction-time and fractional-cascading suggestions are less clean until formalized.

Formula check: the source abstract/PDF gives the main data structure as `O((n+C) log^3 n)` time and space, with query time `O(k log^3 n)`, where `C` is the number of crossings and `k` is output size. Theorem 7 gives an oracle with `O(log^2 n)` query time and `O((n+C) log^2 n)` construction/space. HTML formulas are mangled and should not be the only cited source.

Required distinctions:

- graph-theoretic connectivity versus merely connected segment arrangement;
- planar (`C=0`) versus non-planar crossing-rich graphs;
- circle-boundary reporting versus disk reporting;
- lower-bound tradeoffs versus implementation/CGAL improvements;
- proving a lower bound against all structures versus showing the 2025 edge-partition tree can be forced to visit many nodes.

Smallest meaningful subproblem: planar connected geometric graphs, near-linear space, circle-boundary reporting, and a pointer-machine/cell-probe lower bound that genuinely uses connectedness.

Best use: theorem_project with limited evaluator support. Finite partition-tree adversaries are useful for stress tests, not for proving lower bounds.

Score action: `overall_score` 7.0 -> 6.7; `openevolve_suitability` 4 -> 3; `saturation_risk` low_medium -> medium.

### cache_oblivious_implicit_scanning

Open status: explicit old statement, modern strict-implicit status uncertain.

Evidence causing downgrade/reframe: Franceschini and Grossi explicitly state their structure lacks efficient scanning, and contrast it with cache-aware implicit B-trees that scan in `O(log_B n + r/B)` and pointerless `(1+epsilon)n` structures that scan in `O(1+r/B)`. Later non-implicit cache-oblivious B-tree/PMA-style dictionaries support range scans, so the broad "cache-oblivious alone" phrasing is stale. The only surviving crisp target is exact `n`-cell implicit cache-oblivious scanning/range reporting.

Required distinctions:

- exact `n` key cells plus `O(1)` registers versus `(1+epsilon)n` cells;
- implicit permutation-only encoding versus pointerless linear-space structures with gaps;
- cache-oblivious versus cache-aware;
- search/update/predecessor/successor versus reporting consecutive keys;
- amortized versus worst-case update bounds.

Smallest meaningful subproblem: exact-`n`-cell implicit ordered dictionary with cache-oblivious `O(log_B n)` search/update and range reporting in `O(log_B n + r/B)` amortized block transfers.

Best use: theorem_project. OpenEvolve layout search is risky because it may rediscover non-implicit gap-based layouts outside the model.

Score action: `overall_score` 7.1 -> 6.5; `open_status_confidence` medium -> low_medium; `openevolve_suitability` 3 -> 2.

## Blind Prompt Flags

- `dynamic_stream_mincut_space`: acceptable, but should explicitly say the cut-sparsifier lower bound does not automatically apply to min-cut value estimation.
- `directed_roundtrip_compact_routing`: lower-bound language is too ambitious unless the model is fixed; conditional girth-style lower bounds should not be presented as unconditional routing lower bounds.
- `concurrent_shi_cell_capacity`: unsafe in its original Batch 003 form. It asked about one-key cells even though the source's abstract lower-bounds two-element cells under stronger progress assumptions. The local prompt now has an audit warning; replace fully after theorem extraction.
- `connected_circle_segment_queries`: acceptable for exploration, but the edge-partition-tree adversary is only a lower bound against that technique, not all possible data structures.
- `cache_oblivious_implicit_scanning`: acceptable only if it forbids gaps, `(1+epsilon)n` arrays, and non-implicit PMA/cache-oblivious B-tree structures.

## STT LP Certificate Schema Audit

The schema is directionally usable but not checker-ready without a few clarifications.

Internal consistency issues:

- `relaxation: golinsky_stt_lp` is too vague. A checker needs a versioned constraint set and explicit variable domains.
- `X`, `Z`, and `D` variables are named but their index domains, symmetry conventions, and absent-variable defaults are not specified in the schema.
- Root-rounding `candidate_root_scores` do not define the scoring formula. A checker cannot replay the rounding from a free-text rule.
- `complete_enumeration` with only `stt_count` and a digest is not a proof unless the checker independently enumerates below a threshold or reads the actual enumeration list.
- `almost-star` is explicitly unverified; it must remain advisory until the convention is fixed.

Minimal changes before writing a checker:

- Add a schema/checker version and a `relaxation_version`.
- Require an LP variable-domain section for each relaxation.
- Require rounding rules to be machine-readable identifiers with formulas or checker-implemented names.
- Restrict external digests to audit mode and require enumeration or dual certificates for proof mode.
- Make subclass labels computed-or-advisory field-by-field.

## Source Weakness Flags

- `concurrent_shi_cell_capacity`: source is strong, but Batch 003's interpretation is weak and likely wrong.
- `cache_oblivious_implicit_scanning`: source is primary but old; modern status is not verified.
- `connected_circle_segment_queries`: HTML is too mangled for exact formulas; use PDF/source.
- `directed_roundtrip_compact_routing`: lower-bound context may rely on adjacent models; cite routing-specific statements only.
- `dynamic_stream_mincut_space`: source is strong; beware secondary abstracts that blur insertion-only and dynamic-stream results.

## Current Ranking Implication

After audit, none of the Batch 003 candidates should enter the top fixed-point slot. The best survivor is `dynamic_stream_mincut_space` as a serious explicit lower-bound problem, but it is not as evaluator-ready as Batch 003 suggested. The most useful immediate Batch 003 follow-up is not solving any candidate; it is correcting formulations, especially for concurrent SHI and strict implicit cache-oblivious scans.
