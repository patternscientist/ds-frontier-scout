# Subrun 2F: Author Problem Pages

Date searched: 2026-05-16 America/Los_Angeles.

Status: completed background-lane source scan. This report does not supersede or interrupt the current STT / DS(k,1) theorem project. It is only input for later synthesis and control-panel review.

Source-pool boundary: searched only author/problem/course pages in the assigned pool and immediately adjacent references: John Iacono problem notes, Tarjan problem notes where available, Brodal pages/slides/surveys, Jeff Erickson open-problem pages outside geometry where useful, Cardinal-related searches, Demaine/Iacono/Hesterberg-style 6.897/6.851 pages, and precise data-structure items in the Dagstuhl 25191 author problem report.

Duplicate check: `candidate_topics/` and `reports/top_20_shortlist.md` were checked before recording candidates. Most viable hits are source updates to existing slugs, not new promotions. No candidate folders were created or updated.

## Candidate Findings

Returned viable candidates: 5. Three are duplicate-source updates to existing slugs, one is an existing-slug reinforcement from the Demaine/Iacono course page, and one is a stale-but-precise new lead with low confidence.

### 1. `unified_bound_heaps`

1. slug: `unified_bound_heaps`
2. source pool and exact source: John Iacono problem note in Dagstuhl 25191, "Working set heaps with decrease-key", https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html#5.1.
3. self-contained problem statement: Design a pointer-model priority queue supporting `decrease-key` in constant amortized time and an `extract-min` working-set guarantee, where one variant charges logarithmically in the number of heap operations performed while the extracted item was present.
4. exact open gap: Iacono's statement says no pointer-model structure is known with both the working-set property and constant-time `decrease-key`; the precise working-set definition still has variants.
5. open_status: explicit.
6. freshness check: source is a May 2025 Dagstuhl report, within the last 24 months. Search terms: `working set heaps decrease-key Iacono 2025`, `working set priority queue constant decrease-key`, `Partition-based Simple Heaps working set decrease-key`. Checked adjacent source: arXiv:2603.01206, "Partition-based Simple Heaps" by Brodal, Iacono, Rysgaard, Wild, submitted 2026-03-01, https://arxiv.org/abs/2603.01206. Result: recent simple heaps get amortized `O(log log n)` insert/decrease-key and `O(log n)` extract-min, but the searched abstract does not claim the working-set plus constant decrease-key target.
7. why it matters: It links adaptive priority queues to graph-algorithm uses of `decrease-key`, especially beyond-worst-case shortest paths.
8. literal under-attendedness score: 4. Anchor justification: recent Dagstuhl working group attention and a 2026 adjacent priority-queue paper show active specialists, but the exact pointer-model working-set/decrease-key target appears to have one small source cluster and no AI-collaboration footprint.
9. AI-collaboration fit: strong for definition splitting, candidate heap-rule generation, amortized trace search, and potential-function sketching.
10. theorem-project fit: high after the exact working-set variant is fixed; blind prompt should use one precise age/work metric and pointer-model operation set.
11. OpenEvolve/evaluator fit: moderate. Exact simulators can generate adversarial operation traces and compare empirical working-set cost, but asymptotic guarantees need proof.
12. evolvable object if any: heap linking/cutting/consolidation rule plus a potential-function template scored against generated operation traces.
13. Lean/certificate fit: moderate for formalizing operation semantics and potential inequalities on finite traces; weaker for the full asymptotic construction search.
14. risks/downgrades: duplicate of existing slug; variants of working-set priority queues can create fake gaps; recent Dijkstra/universal-optimality heap work must be separated from the pointer-model target.
15. blind prompt: "Design or rule out a pointer-model priority queue supporting `insert`, `find-min`, `extract-min`, and `decrease-key`. Require amortized `O(1)` `decrease-key` and require the cost of extracting item `x` to be `O(1 + log a_x)`, where `a_x` is the number of heap operations performed after `x` was inserted and before it is extracted. Either give a data structure and amortized proof, or prove an obstruction for this exact model."

### 2. `path_compression_topdown`

1. slug: `path_compression_topdown`
2. source pool and exact source: Robert E. Tarjan problem note in Dagstuhl 25191, "Top-down analysis of path compression", https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html#5.3; adjacent primary reference Seidel and Sharir, "Top-Down Analysis of Path Compression", DOI:10.1137/S0097539703439088.
3. self-contained problem statement: Give a simple direct proof that the Seidel-Sharir top-down recurrence for path compression implies the classical inverse-Ackermann upper bound, using the classical Ackermann definition rather than the paper's related `J` function.
4. exact open gap: The gap is proof-expository/formal: translate the top-down recurrence into the standard inverse-Ackermann framework without the detour through `J`.
5. open_status: explicit.
6. freshness check: source is a May 2025 Tarjan problem statement. Search terms: `Tarjan top-down path compression Ackermann proof 2025`, `Seidel Sharir top-down path compression direct proof`, `path compression top-down recurrence Ackermann`. Result: no located source in the assigned pool claims a direct classical-Ackermann proof after the 2025 problem note.
7. why it matters: It could simplify a foundational union-find analysis and produce a clean formalization target rather than a new data-structure bound.
8. literal under-attendedness score: 5. Anchor justification: fewer than five visible recent mentions of this exact proof-translation problem, one named source, and no AI-collaboration work found.
9. AI-collaboration fit: strong for staged proof attempts, recurrence normalization, lemma mining, and checking small recurrence tables.
10. theorem-project fit: high as a proof project, not as a new theorem frontier; blind prompt must include the exact recurrence.
11. OpenEvolve/evaluator fit: weak. Numeric recurrence exploration can suggest mappings but cannot certify the asymptotic proof.
12. evolvable object if any: recurrence-to-Ackermann ranking functions or candidate inequalities.
13. Lean/certificate fit: high. This is the best formalization-shaped lead in the source pool.
14. risks/downgrades: duplicate of existing slug; a clean proof may already exist in private lecture notes; without the exact recurrence, prompts solve the wrong problem.
15. blind prompt: "Given the Seidel-Sharir top-down recurrence for path compression, prove directly that its solution is bounded by `O((m+n) alpha(m,n))` using the classical Ackermann hierarchy and inverse-Ackermann definition. Avoid introducing an unrelated auxiliary hierarchy unless it is explicitly mapped back to classical Ackermann."

### 3. `karp_rabin_collision_detection`

1. slug: `karp_rabin_collision_detection`
2. source pool and exact source: Martin Farach-Colton problem note in Dagstuhl 25191, "Detecting collisions in Karp-Rabin fingerprinting", https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html#5.5.
3. self-contained problem statement: Given a string and a prime modulus used for Karp-Rabin fingerprints, decide whether there exist two distinct same-length substrings with the same fingerprint.
4. exact open gap: Quadratic time is straightforward via suffix trees; the problem asks whether linear time, or at least a subquadratic time bound, is possible. The note allows randomized false rejection of some non-colliding primes/polynomials with small probability.
5. open_status: explicit.
6. freshness check: source is a May 2025 problem note. Search terms: `Karp Rabin collision detection fixed prime subquadratic`, `collision-free fingerprint certification Karp Rabin 2025`, `substring polynomial hash collision checking prime`. Result: no assigned-pool source found closing the exact all-length collision-detection problem after the 2025 note.
7. why it matters: Fingerprints are a basic randomized string-algorithm primitive; a fast certificate for bad moduli would sharpen correctness guarantees for string data structures.
8. literal under-attendedness score: 5. Anchor justification: exact problem has one fresh Dagstuhl statement, few apparent named citations, and no AI-collab work found.
9. AI-collaboration fit: high for brute-force oracles, adversarial string/modulus generation, and algorithm sketch stress-testing.
10. theorem-project fit: moderate-high. The statement is crisp, but the right algebraic/stringology lens must be identified.
11. OpenEvolve/evaluator fit: high. Exact small-string/modulus exhaustive search is natural.
12. evolvable object if any: collision detector or rejection heuristic scored against exhaustive same-length substring-pair oracles.
13. Lean/certificate fit: moderate. Finite collision certificates are easy; subquadratic algorithm proofs are harder.
14. risks/downgrades: duplicate of existing slug; deterministic exact detection and allowed randomized rejection are different variants; alternate terminology may hide a solution.
15. blind prompt: "Input a string `S` of length `n` over integer alphabet, a base equal to the alphabet size, and a prime modulus `p`. The Karp-Rabin fingerprint of a substring is its polynomial value modulo `p`. Determine whether any two distinct substrings of equal length have the same fingerprint. Give an algorithm asymptotically faster than checking all substring pairs, or prove a barrier for a natural model."

### 4. `list_update`

1. slug: `list_update`
2. source pool and exact source: Demaine/Iacono 6.897 project page, "Randomized self-organizing linear search", https://courses.csail.mit.edu/6.897/spring03/projects.html; adjacent freshness sources include Ambuehl, Gaertner, von Stengel, arXiv:1002.2440, and the 2024 Cambridge online chapter "List Accessing".
3. self-contained problem statement: Close the gap between lower and upper bounds on the optimal randomized competitive ratio for classical online list update in the Sleator-Tarjan cost model.
4. exact open gap: The Demaine/Iacono page records upper bound `1.6` and lower bound `1.5`; the projective/list-factoring line later showed `1.6` optimal among projective algorithms, leaving possible non-projective randomized algorithms.
5. open_status: explicit in older page and still supported by recent secondary/freshness sources; treat as inferred-current rather than fully reverified.
6. freshness check: search terms: `randomized list update competitive ratio 1.6 1.5 2024`, `list update 1.6 1.5 randomized competitive ratio open`, `Bit algorithm 1.75 list update`. Sources found: Cambridge "List Accessing" published online 2024-05-07 states the randomized gap as `1.6` vs `1.5`; ESA 2025 uniform-cost variant notes classical list update remains canonical with open questions; arXiv:1002.2440 states the classical gap and projective lower bound. Result: freshness supports the broad gap, but model variants are easy to confuse.
7. why it matters: List update is the canonical self-organizing linear-search problem and a clean online data-structure testbed.
8. literal under-attendedness score: 3. Anchor justification: specialist subfield with slow regular work; more than one active citation trail, but no observed AI-collaboration focus.
9. AI-collaboration fit: high for finite-list strategy synthesis, adversarial request sequence generation, and LP/game lower bounds.
10. theorem-project fit: low-moderate. Generalizing finite or non-projective strategies to all list sizes is the hard part.
11. OpenEvolve/evaluator fit: high. Exact finite games for small list sizes and finite-memory randomized policies are natural.
12. evolvable object if any: randomized online policy/state machine, scored by competitive-ratio LP/adversary search on small `n`.
13. Lean/certificate fit: moderate for finite adversary certificates and projective-policy proofs.
14. risks/downgrades: duplicate of existing slug; old Demaine page; classical, paid-exchange, full-cost, partial-cost, dynamic-list, and uniform-cost variants must not be merged.
15. blind prompt: "In the classical online list update problem under the Sleator-Tarjan partial-cost model, find a randomized online algorithm with competitive ratio strictly below `1.6`, or prove that no randomized online algorithm can beat `1.6`. Do not assume projectivity/list factoring unless you explicitly justify the restriction."

### 5. `optimal_static_bst_subquadratic`

1. slug: `optimal_static_bst_subquadratic`
2. source pool and exact source: Demaine/Iacono 6.897 project page, "Optimal binary search trees", https://courses.csail.mit.edu/6.897/spring03/projects.html.
3. self-contained problem statement: Given sorted keys and successful/unsuccessful search probabilities, compute an optimal static binary search tree in truly subquadratic time, or with polynomial time and `o(n^2)` space; alternatively prove a fine-grained lower bound such as 3SUM-hardness for subquadratic exact construction.
4. exact open gap: Knuth's dynamic program gives `Theta(n^2)` time and space; the page asks whether exact construction can beat quadratic time or quadratic space.
5. open_status: uncertain.
6. freshness check: search terms: `optimal binary search tree subquadratic time open problem 3SUM-hard`, `Optimal binary search trees subquadratic 2024`, `optimal binary search tree o(n^2) open`. Sources found include old approximate/special-case subquadratic algorithms, a 2015 paper on 2-way comparison search trees, and 2021 work on generalized binary split trees; no assigned-pool source in the last 24 months confirmed or closed the exact Knuth-model subquadratic question. Result: old and unconfirmed; downgrade confidence.
7. why it matters: It is a crisp fine-grained dynamic-programming/data-structure question at the boundary of classic search-tree optimization and conditional lower bounds.
8. literal under-attendedness score: 5. Anchor justification: exact subquadratic static-OBST construction seems to have very few recent named mentions and no AI-collaboration work found.
9. AI-collaboration fit: moderate-high for Monge/DP optimization searches, counterexample mining for quadrangle-like speedups, and conditional-reduction sketching.
10. theorem-project fit: moderate. The statement is clean, but modern status and exact probability model must be verified before a blind run.
11. OpenEvolve/evaluator fit: moderate-high. Knuth DP gives an exact oracle for small/medium `n`; candidate optimizers can be searched and falsified.
12. evolvable object if any: recurrence-pruning rule, root-window conjecture, or approximate-to-exact refinement algorithm tested against exact DP.
13. Lean/certificate fit: moderate. Optimality certificates for a proposed tree are possible via interval DP inequalities; lower-bound reductions are less Lean-friendly.
14. risks/downgrades: stale 2003 page; could have a later conditional lower bound or model-specific algorithm outside searched source pool; not clearly under-attended if framed as generic DP optimization.
15. blind prompt: "Given arrays of successful and unsuccessful search probabilities for sorted keys, compute the minimum expected-cost static binary search tree. Knuth's algorithm takes `Theta(n^2)` time and space. Seek a truly subquadratic exact algorithm, an `o(n^2)`-space polynomial-time exact algorithm, or a conditional fine-grained lower bound explaining why the quadratic barrier is real."

## Rejection Ledger

```yaml
- title_or_slug: simple_successor_delete_analysis
  subrun: 2F_author_problem_pages
  reason_rejected: "Brodal's 2025 slide/report item is enticing and under-attended, but the open problem is a broad 'simple data structures with slightly worse bounds' program rather than a precise theorem target. The one-page slide asks for a simpler structure/proof/engineering path; the stripped Dagstuhl HTML does not expose a complete asymptotic target."
  source_urls_or_ids:
    - "https://cs.au.dk/~gerth/slides/dagstuhl25.pdf"
    - "https://doi.org/10.4230/LIPIcs.SEA.2025.8"
    - "https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html#4.6"
  search_terms:
    - "Gerth Brodal simple integer successor-delete data structure open problem"
    - "Simple Data Structures with Slightly Worse Bounds Brodal"
    - "successor delete union find unweighted linking path compression Brodal SEA 2025"
  date_searched: 2026-05-16
  freshness_or_closure_signal: "Fresh 2025 source; freshness is strong, precision is the problem."
  could_revisit_if: "The SEA 2025 full paper or talk notes state a concrete conjectured bound for the one-array unweighted path-compression successor-delete structure."

- title_or_slug: planar_point_location_integer_fusion
  subrun: 2F_author_problem_pages
  reason_rejected: "Old Demaine/Iacono 2003 project-page item appears substantially answered by Timothy Chan's FOCS 2006 transdichotomous point-location result with sublogarithmic query time and linear space."
  source_urls_or_ids:
    - "https://courses.csail.mit.edu/6.897/spring03/projects.html"
    - "https://doi.org/10.1109/FOCS.2006.62"
  search_terms:
    - "static planar point location integer coordinates fusion tree sublogarithmic query open"
    - "Planar point location fusion trees Demaine Iacono"
    - "Faster planar point location integer coordinates"
  date_searched: 2026-05-16
  freshness_or_closure_signal: "2006 source gives the desired o(log n) style result; no candidate."
  could_revisit_if: "A stricter space/model variant is extracted from Iacono's integer point-location papers rather than the broad 2003 prompt."

- title_or_slug: ordered_file_maintenance_log2_lower_bound
  subrun: 2F_author_problem_pages
  reason_rejected: "The 2003 page asks to prove an Omega(log^2 n) amortized bound or find a better algorithm. Subsequent lower bounds and the 2024 randomized 'Breaking the log^2 n Barrier' line mean the original prompt is stale and model-sensitive."
  source_urls_or_ids:
    - "https://courses.csail.mit.edu/6.897/spring03/projects.html"
    - "https://doi.org/10.1137/130907653"
    - "https://doi.org/10.1137/22M1534468"
    - "https://arxiv.org/abs/2203.02763"
  search_terms:
    - "ordered file maintenance lower bound O(log^2 n) open problem solved"
    - "ordered file maintenance lower bound amortized time 2024"
    - "file maintenance problem lower bound online monotonic list labeling 2025"
  date_searched: 2026-05-16
  freshness_or_closure_signal: "Recent randomized list-labeling progress changes the gap; likely not viable as stated."
  could_revisit_if: "A residual exact model is stated, e.g. deterministic packed-memory arrays with deletions and strict density constraints."

- title_or_slug: implicit_dictionary_logn
  subrun: 2F_author_problem_pages
  reason_rejected: "The 2003 page asks whether an exact implicit dictionary can support operations in O(log n). Later implicit/cache-oblivious implicit dictionaries report O(log n)-type bounds; the old prompt is likely solved or too broad."
  source_urls_or_ids:
    - "https://courses.csail.mit.edu/6.897/spring03/projects.html"
    - "https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2012.112"
    - "https://arxiv.org/abs/1112.5472"
  search_terms:
    - "implicit dictionary O(log n) insert delete predecessor exact n space open problem"
    - "implicit search tree O(log n) insertion deletion predecessor"
    - "Implicit Dictionaries O(log n) open problem"
  date_searched: 2026-05-16
  freshness_or_closure_signal: "Search results include exact-n implicit structures with O(log n) insert/delete and predecessor/search bounds."
  could_revisit_if: "The target is narrowed to exact cache-oblivious range scans, already tracked separately as `cache_oblivious_implicit_scanning`."

- title_or_slug: rambo_data_structures
  subrun: 2F_author_problem_pages
  reason_rejected: "Too broad: 'take your favorite data structure and make it faster on RAMBO' is a research-program prompt, not a precise candidate with a source-checkable open gap."
  source_urls_or_ids:
    - "https://courses.csail.mit.edu/6.897/spring03/projects.html"
  search_terms:
    - "RAMBO data structures open problem"
    - "Demaine Iacono RAMBO data structures"
  date_searched: 2026-05-16
  freshness_or_closure_signal: "No precise fresh residual found in assigned pool."
  could_revisit_if: "A named RAMBO operation set, model, and target bound are sourced."

- title_or_slug: offline_self_organizing_linear_search
  subrun: 2F_author_problem_pages
  reason_rejected: "Interesting but too close to existing `list_update` without enough modern source separation. The Demaine/Iacono page asks for better polynomial-time offline competitive ratios after NP-hardness of exact offline optimum, but this needs a separate modern sweep."
  source_urls_or_ids:
    - "https://courses.csail.mit.edu/6.897/spring03/projects.html"
  search_terms:
    - "offline self organizing linear search Munro Order By Next Request competitive ratio"
    - "offline list update polynomial time competitive ratio"
  date_searched: 2026-05-16
  freshness_or_closure_signal: "No last-24-month confirmation from assigned source pool."
  could_revisit_if: "A recent primary source distinguishes offline approximation from the online randomized list-update gap."

- title_or_slug: jeff_erickson_open_problem_pages
  subrun: 2F_author_problem_pages
  reason_rejected: "Jeff Erickson's open-problem pages are valuable but mostly computational geometry/topology; this subrun found no non-geometry data-structure item precise enough and not already covered by geometry runs."
  source_urls_or_ids:
    - "https://jeffe.cs.illinois.edu/open/"
    - "https://jeffe.cs.illinois.edu/"
  search_terms:
    - "Jeff Erickson open problems data structures problem page"
    - "site:jeffe.cs.illinois.edu open problems data structures Erickson"
  date_searched: 2026-05-16
  freshness_or_closure_signal: "Source itself warns not to cite the pages as evidence that problems remain open."
  could_revisit_if: "A non-geometry data-structure page with explicit current status is identified."

- title_or_slug: cardinal_surveys
  subrun: 2F_author_problem_pages
  reason_rejected: "Searches for Cardinal surveys/pages did not locate a precise author-maintained data-structure open problem suitable for this subrun; hits were mostly geometry, combinatorial optimization, or unrelated cardinal-number material."
  source_urls_or_ids:
    - "https://arxiv.org/abs/2311.12471"
    - "https://sublinear.info/"
  search_terms:
    - "Jean Cardinal data structures survey open problems"
    - "Cardinal survey data structures open problems algorithms"
    - "\"Cardinal\" \"open problems\" \"data structures\""
  date_searched: 2026-05-16
  freshness_or_closure_signal: "No viable precise statement found."
  could_revisit_if: "A named Cardinal-authored survey/problem page with explicit open questions is found."
```

## Notes For Synthesis

- Author problem pages were useful mainly as source saturation for existing candidates, not as a source of many new promotable slugs.
- Fresh explicit 2025 Dagstuhl statements reinforce `unified_bound_heaps`, `path_compression_topdown`, and `karp_rabin_collision_detection`.
- The Demaine/Iacono 2003 project page remains useful for provenance but is stale; old items should be downgraded unless a last-24-month source reconfirms the exact gap.
- No recommendation here should affect the foreground STT / DS(k,1) theorem lane without later control-panel review.
