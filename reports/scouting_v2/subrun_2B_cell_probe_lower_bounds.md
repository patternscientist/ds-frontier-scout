# Subrun 2B: Cell-Probe And Lower-Bound Mini-Frontiers

Date searched: 2026-05-17

Status: completed background-lane subrun.

Background-lane rule: this report is source gathering for later synthesis and control-panel review. It does not supersede, re-rank, or interrupt the current STT / DS(k,1) foreground theorem project.

## Scope And Duplicate Check

Read for duplicate/saturation context:

- `reports/scouting_v2/README.md`
- `reports/top_20_shortlist.md`
- `reports/candidate_matrix.md`
- `candidate_topics/*/problem.md`
- `candidate_topics/*/skeptical_audit.md`

Existing nearby slugs checked:

- `range_mode_queries`
- `dynamic_graph_structures`
- `dynamic_min_tree_cut`
- `dynamic_stream_mincut_space`
- `retroactive_data_structures`
- `hashing_dictionaries`
- `history_independent_data_structures`
- `concurrent_shi_cell_capacity`
- `cache_oblivious_implicit_scanning`
- `external_memory_structures`

Result: one non-duplicate viable lower-bound mini-frontier survived. Several more literal cell-probe leads were rejected as duplicates, solved/narrowed by 2025-2026 papers, or too broad/saturated under the Scouting v2 narrowing rule.

## Viable Candidates

### 1. `randomized_linear_list_labeling_lower_bound`

1. slug: `randomized_linear_list_labeling_lower_bound`

2. source pool and exact source:
   - Source pool lane: FOCS/STOC/SODA residual lower-bound claims defining crisp data-structure mini-frontiers; adjacent lower-bound mini-frontier rather than cell-probe proper.
   - Primary current source: Michael A. Bender, Alex Conway, Martin Farach-Colton, Hanna Komlos, Michal Koucky, William Kuszmaul, Michael Saks, "Nearly Optimal List Labeling", FOCS 2024, DOI `10.1109/FOCS61266.2024.00132`, arXiv `2405.00807`, https://arxiv.org/abs/2405.00807.
   - Prior lower-bound source: Jan Bulanek, Michal Koucky, Michael Saks, "Tight Lower Bounds for the Online Labeling Problem", preliminary STOC 2012; author PDF https://sites.math.rutgers.edu/~saks/PUBS/labeling-122214.pdf.
   - Search terms: `"Nearly Optimal List Labeling" "open problem" randomized lower bound`, `"list labeling" "randomized lower bound" "open problem" "2024"`, `"online labeling" "randomized" "lower bound" "open problem"`, `"list-labeling" "closing this gap" "major open problem" data structures`.
   - Date searched: 2026-05-17.

3. self-contained problem statement:

   In the online list-labeling/file-maintenance problem, maintain up to `n` ordered items in an array of size `m = (1 + Theta(1))n`. Each inserted item arrives with an order position relative to the existing items; the data structure must assign array locations/labels preserving sorted order, paying one unit whenever an item is placed or moved/relabelled. Randomized algorithms may make random choices and are judged by amortized expected cost. Prove a randomized lower bound asymptotically larger than `Omega(log n)` for the linear-space regime, ideally matching the 2024 randomized upper bound up to constants or clarifying the remaining `polyloglog n` gap.

4. exact open gap:

   The 2024 FOCS paper gives a randomized `O(log n polyloglog n)` amortized expected upper bound for `m = (1 + Theta(1))n`. The best randomized lower bound remains `Omega(log n)`. Deterministic linear-space lower bounds and lower bounds for smooth/history-independent/restricted algorithm classes do not close the general randomized gap.

5. open_status: explicit.

   The FOCS 2024 abstract explicitly says the best randomized lower bound remains `Omega(log n)` and that closing the gap is a major open problem in data structures.

6. freshness check:
   - Last-24-month sources checked:
     - FOCS 2024 final metadata and DOI page via university publication mirrors, dated 2024.
     - arXiv `2405.00807`, submitted 2024-05-01; just outside the strict 24-month window by submission date, but the FOCS 2024 publication and seminar trail are within the last 24 months.
     - Waterloo seminar announcement, 2024-10-02, for the same result.
     - Search on 2026-05-17 for post-2024 "randomized lower bound list labeling" and "online labeling randomized lower bound open problem".
   - Freshness result: no post-FOCS-2024 primary source found closing the randomized lower-bound gap. The most recent visible primary source is still the near-optimal upper bound plus explicit residual lower-bound gap.

7. why it matters:

   List labeling is a core abstraction behind order maintenance, file maintenance, packed-memory/cache-oblivious dictionaries, and ordered dynamic storage. The lower-bound gap is unusually clean: deterministic and restricted lower bounds are strong, but randomization appears to bypass decades of adversarial techniques up to a small `polyloglog n` factor.

8. literal under-attendedness score with anchor justification:

   Score: 3.

   Anchor: this is a specialist subfield with regular but slow work and no visible AI-collaboration line. It is not a score-5 obscure exercise because the 2024 source calls it a major open problem and the author set is broad. It is not disqualified by the "3+ broad surveys or 50+ citations" rule as a narrow randomized linear-space lower-bound residual: the exact post-2024 residual is recent and source-specific, even though the historical list-labeling problem is old.

9. AI-collaboration fit:

   Good for finite adversary/game exploration. An AI system can implement online labeling algorithms, adversarial insertion strategies, and small randomized games, then mine candidate hard distributions and potential functions. The main caution is that finite evidence will not by itself prove an asymptotic randomized lower bound.

10. theorem-project fit:

   Moderate. A staged theorem project could start from a blind prompt about randomized file maintenance, then add frontier notes on deterministic segment-chain adversaries and the See-Saw algorithm. The proof target is combinatorial and model-sensitive, but less dependent on heavy external machinery than many cell-probe lower-bound programs.

11. OpenEvolve/evaluator fit:

   Moderate-high. Plausible evaluators include exact dynamic programming for tiny arrays, minimax/LP games for bounded insertion universes, Monte Carlo evaluation of randomized algorithms against evolved adversaries, and automated search for segment-chain potential inequalities.

12. evolvable object if any:

   Adaptive insertion adversaries; distributions over insertion sequences; candidate potential functions measuring crowding at multiple scales; restricted randomized relabeling strategies; finite game certificates separating classes of algorithms.

13. Lean/certificate fit:

   Moderate. Small finite-game certificates and deterministic lower-bound lemmas over nested intervals are plausible formalization targets. A full randomized asymptotic lower bound would likely require substantial probability and adversary formalization.

14. risks/downgrades:

   - The source itself says this is a "major open problem", so the candidate is not deeply neglected.
   - The remaining upper/lower gap is only `polyloglog n` after FOCS 2024; exact closure may be technically fussy rather than conceptually broad.
   - Randomization, adaptive versus oblivious adversaries, amortized expected cost, and deletion support must be fixed before any blind prompt is meaningful.
   - A hidden 2025/2026 manuscript under "file maintenance", "online labeling", or "packed memory arrays" terminology could narrow the gap further.
   - Automation can overfit to small arrays and miss the multi-scale adversary structure.

15. blind prompt:

   ```text
   Consider the online list-labeling problem. There are at most n ordered items stored in an array of m = c n cells for a fixed constant c > 1. Items are inserted one at a time, each new item specifying its rank among the current items. After every insertion, the occupied cells must respect the item order. Moving an existing item or placing the new item costs 1. A randomized algorithm may use private randomness, and its performance is measured by amortized expected cost over a worst-case insertion sequence.

   Prove a lower bound asymptotically larger than Omega(log n) on the amortized expected cost of any randomized algorithm, or give a randomized algorithm with O(log n) amortized expected cost. If the full problem is too hard, isolate a restricted adversary model or finite game whose solution would suggest a path to one side.
   ```

## Rejection Ledger

### `retroactive_cell_probe_linear_overhead`

- reason_rejected: duplicate/update to existing `retroactive_data_structures`, not a new slug. The 6.851 notes provide the missing primary-ish explicit residual that Batch 002 wanted, but promotion should update/audit the existing retroactivity lane rather than create a new Scouting v2 candidate.
- source_urls_or_ids:
  - MIT 6.851 Spring 2021 Lecture 2 page, https://courses.csail.mit.edu/6.851/spring21/lectures/
  - MIT 6.851 Spring 2021 Lecture 2 scribe notes, https://courses.csail.mit.edu/6.851/spring21/scribe/lec2.pdf
  - Demaine, Iacono, Langerman, "Retroactive Data Structures", ACM TALG 2007, author page link from 6.851: https://erikdemaine.org
  - Frandsen, Frandsen, Miltersen, I&C 2001 lower-bound source linked from 6.851: https://www.brics.dk
- search_terms:
  - `site:courses.csail.mit.edu/6.851 cell probe lower bounds open problems data structures`
  - `"retroactive data structures" "cell probe" "OPEN problem" "Omega(r)"`
  - `"general transformation" retroactive "cell-probe" lower bound`
- date_searched: 2026-05-17.
- freshness_or_closure_signal: The 2021 lecture page says a better cell-probe lower bound such as `Omega(r / polylog r)` is open; no fresh closure was found in this subrun, but the lead is already represented locally as `retroactive_data_structures`.
- could_revisit_if: existing `retroactive_data_structures` is split into a narrow `retroactive_cell_probe_linear_overhead` residual after primary paper checks.

### `dynamic_boolean_cell_probe_log_squared`

- reason_rejected: likely solved/closed in 2026 as originally posed. This was a canonical cell-probe lower-bound open direction, but Young Kun Ko's 2026 preprint claims an `Omega((log n / log log n)^2)` lower bound for the Boolean multiphase/inner-product setting, closing the gap left by the 2018 Boolean `log^{1.5}` result.
- source_urls_or_ids:
  - Larsen, Weinstein, Yu, "Crossing the Logarithmic Barrier for Dynamic Boolean Data Structure Lower Bounds", arXiv `1703.03575`, https://arxiv.org/abs/1703.03575.
  - Ko, "An Omega((log n / log log n)^2) Cell-Probe Lower Bound for Dynamic Boolean Data Structures", arXiv `2603.25914`, https://arxiv.org/abs/2603.25914.
  - ECCC TR26-047, https://eccc.weizmann.ac.il/report/2026/047.
- search_terms:
  - `"Patrascu" "five important open problems" data structures`
  - `"multiphase problem" "open problem" "cell-probe"`
  - `"Boolean dynamic data structure" "cell-probe" "2026"`
- date_searched: 2026-05-17.
- freshness_or_closure_signal: 2026 arXiv/ECCC source explicitly says it resolves the long-standing Boolean dynamic data-structure hardness open problem.
- could_revisit_if: the 2026 result is withdrawn, restricted in a way that leaves a named Boolean dynamic problem open, or a new residual beyond the chronogram `log^2` ceiling is posed crisply.

### `dynamic_range_counting_one_bit_output`

- reason_rejected: serious but not viable as a fresh under-attended candidate. Larsen 2012 explicitly posed one-bit-output superlog lower bounds as an open technique frontier; later 2017 and 2026 work substantially close that frontier for Boolean/range-counting-style problems. The remaining "beyond log-squared" direction is broad technique/circuit-complexity territory rather than a small residual data-structure mini-frontier.
- source_urls_or_ids:
  - Kasper Green Larsen, "The Cell Probe Complexity of Dynamic Range Counting", author PDF https://cs.au.dk/~larsen/papers/cell_dyn_range.pdf.
  - Larsen, Weinstein, Yu, arXiv `1703.03575`, https://arxiv.org/abs/1703.03575.
  - Ko, arXiv `2603.25914`, https://arxiv.org/abs/2603.25914.
- search_terms:
  - `"open problem" "cell-probe" "range counting" "one bit output"`
  - `"dynamic range counting" "cell probe" "open problem"`
  - `"regular counting" "same lower bound" "cell probe"`
- date_searched: 2026-05-17.
- freshness_or_closure_signal: 2026 source claims the Boolean `log^2`-scale lower bound; not promoted.
- could_revisit_if: a source after 2026 states a narrow unweighted/exact-counting residual not implied by parity or Boolean lower bounds.

### `dynamic_connectivity_log_gap`

- reason_rejected: too saturated and already represented by `dynamic_graph_structures`/`dynamic_min_tree_cut` context. The upper/lower gap around dynamic connectivity is a famous active area, not an under-attended lower-bound mini-frontier.
- source_urls_or_ids:
  - Patrascu and Demaine, "Logarithmic Lower Bounds in the Cell-Probe Model", arXiv `cs/0502041`, https://arxiv.org/abs/cs/0502041.
  - MIT 6.851 Spring 2021 dynamic graph lower-bound lecture page, https://courses.csail.mit.edu/6.851/spring21/lectures/.
  - Wulff-Nilsen, "Fully Dynamic Connectivity in O(log n (log log n)^2) Amortized Expected Time", https://theoretics.episciences.org/9645.
- search_terms:
  - `"dynamic connectivity" "cell-probe" "lower bound" "open problem"`
  - `"Fully Dynamic Connectivity" "log n" "log log" "cell probe lower bounds"`
- date_searched: 2026-05-17.
- freshness_or_closure_signal: recent upper bounds come close to the Patrascu-Demaine/Patrascu-Thorup lower bounds; no narrow under-attended residual isolated.
- could_revisit_if: a source states a crisp restricted lower-bound gap, e.g. a single graph class or update/query distribution outside existing dynamic-graph saturation.

### `range_mode_cell_probe_gap`

- reason_rejected: duplicate of existing `range_mode_queries`. The exact static range-mode upper/lower gap remains useful, but it is already on the shortlist and needs its own source update rather than a new lower-bound subrun slug.
- source_urls_or_ids:
  - Greve, Jorgensen, Larsen, Truelsen, "Cell probe lower bounds and approximations for range mode", DOI `10.1007/978-3-642-14165-2_51`.
  - Existing local folder `candidate_topics/range_mode_queries`.
- search_terms:
  - `"open problem" "cell-probe" "range mode"`
  - `"range mode" "linear space" "query time" "open problem"`
- date_searched: 2026-05-17.
- freshness_or_closure_signal: no closure found in this subrun, but duplicate policy blocks a new candidate.
- could_revisit_if: the later range-mode source audit identifies a sharper lower-bound-only subcase distinct from the current `range_mode_queries` candidate.

### `transdichotomous_point_location_lower_bound`

- reason_rejected: outside this subrun's lower-bound mini-frontier after narrowing, and likely belongs to geometry scouting. The Patrascu blog archive says "Open problem: lower bound" for sublogarithmic point location, but the Chan-Patrascu point-location line is well-known and geometry-heavy.
- source_urls_or_ids:
  - Patrascu blog archive February 2008, https://infoweekly.blogspot.com/2008/02/.
  - Chan and Patrascu, "Transdichotomous Results in Computational Geometry, I: Point Location in Sublogarithmic Time", DOI `10.1137/07068669X`.
- search_terms:
  - `"sublogarithmic point location" "lower bound" Patrascu Chan open problem`
  - `"Sublogarithmic point location" "lower bound" "open"`
- date_searched: 2026-05-17.
- freshness_or_closure_signal: 2018 dynamic orthogonal point-location work is adjacent, but not a clean closure of the original broad lower-bound wish. Rejected for scope/saturation, not solved.
- could_revisit_if: Subrun 2A isolates a very narrow cell-probe or word-RAM lower-bound subcase not covered by broad computational-geometry attention.

### `dynamic_interval_union_query_sparse_tradeoff`

- reason_rejected: the tempting query-sparse interval-union gap in the introduction of Yu STOC 2016 is resolved by the same paper's main theorem for the relevant hard distribution; no crisp residual was isolated.
- source_urls_or_ids:
  - Huacheng Yu, "Cell-Probe Lower Bounds for Dynamic Problems via a New Communication Model", STOC 2016, DOI `10.1145/2897518.2897556`, arXiv `1512.01293`, https://arxiv.org/abs/1512.01293.
  - Author PDF https://www.cs.princeton.edu/~hy2/files/dynintun.pdf.
- search_terms:
  - `"dynamic interval union" "open problem" "cell probe"`
  - `"dynamic interval union" "open" "lower bound" data structure`
- date_searched: 2026-05-17.
- freshness_or_closure_signal: no later open residual found; the main paper already rules out the motivating low-update/high-query loophole.
- could_revisit_if: a later Klee's-measure or interval-union paper poses a precise remaining exponent tradeoff.

### `static_linear_space_cell_probe_barrier`

- reason_rejected: too broad, technique-centric, and explicitly saturated by lower-bound/circuit-complexity programs. It violates the extra narrowing rule unless a small named data-structure subcase is extracted.
- source_urls_or_ids:
  - "Static Data Structure Lower Bounds Imply Rigidity", PDF result found at https://golovnev.org/papers/ds.pdf.
  - STOC/FOCS/SODA 2025-2026 proceedings snippets on static data-structure lower bounds and circuit/range-avoidance connections.
- search_terms:
  - `"static data structure lower bounds" "major open problem" "linear space"`
  - `"static data structure lower bounds imply rigidity"`
  - `"cell probe" "linear space" "major open problem"`
- date_searched: 2026-05-17.
- freshness_or_closure_signal: active 2025-2026 complexity-theory work; not under-attended.
- could_revisit_if: a primary source states a small explicit static DS problem with a finite evaluator and a lower-bound gap not already in broad surveys.

### `open_addressing_oblivious_hashing_lower_bound`

- reason_rejected: interesting recent lower-bound context, but no crisp open problem was found in the assigned search. It also overlaps existing `hashing_dictionaries` and `concurrent_shi_cell_capacity` lanes.
- source_urls_or_ids:
  - Bender, Kuszmaul, Zhou, "Optimal Non-Oblivious Open Addressing", STOC 2025, DOI `10.1145/3717823.3718215`, arXiv `2503.13628`, https://arxiv.org/abs/2503.13628.
  - STOC 2025 table of contents, https://acm-stoc.org/stoc2025/toc.html.
- search_terms:
  - `"oblivious open-addressed hash tables" lower bound open problem`
  - `"history-independent" "open addressing" hash tables lower bound open problem`
  - `"Bender Kuszmaul Zhou" "oblivious" "open-addressed" hash tables lower bound`
- date_searched: 2026-05-17.
- freshness_or_closure_signal: 2025 result is fresh, but the located source frames it as resolving/bypassing a tradeoff rather than posing a lower-bound residual.
- could_revisit_if: a follow-up states an explicit lower-bound frontier for oblivious, history-independent, or metadata-free open addressing.

## Notes For Synthesis

- The literal cell-probe source pool was less fertile than expected because several famous lower-bound frontiers have either been closed/narrowed recently or are too saturated for Scouting v2.
- The retroactivity lead is the best duplicate-source update: it gives an explicit cell-probe lower-bound open statement for the existing `retroactive_data_structures` lane.
- `randomized_linear_list_labeling_lower_bound` is not a pure cell-probe problem, but it fits the "lower-bound mini-frontier" part of this subrun and has a concrete finite-game/evaluator angle.
- No candidate folders were created or updated.
