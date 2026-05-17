# Subrun 2I: OpenEvolve Evolvable Objects

Status: completed for scouting-v2 source-saturation background lane.

Date searched: 2026-05-17.

Boundary: this is an OpenEvolve side-experiment report only. It does not supersede, interrupt, or re-rank the current STT / DS(k,1) foreground theorem project. Any promoted experiment below is for later synthesis and control-panel review.

## Scope And Method

This subrun asks whether an OpenEvolve-style loop could plausibly discover a data structure, rediscover a known structure, or produce theorem-relevant artifacts by evolving a concrete object against a concrete evaluator. It intentionally does not use "has an exact checker" as enough evidence by itself. A lead is kept only if the mutable object is explicit: a rule, policy, grammar, potential template, adversarial generator, inequality template, or related object.

Input files checked:

- `reports/scouting_v2/README.md`
- `reports/top_20_shortlist.md`
- `reports/candidate_matrix.md`
- `candidate_topics/*/problem.md`
- `candidate_topics/*/openevolve_fit.md`
- `candidate_topics/*/skeptical_audit.md`
- relevant `candidate_topics/*/sources.yaml` files for candidates and serious rejections

Additional freshness searches were lightweight and object-focused, not a broad literature review. Search terms are recorded per lead.

## Summary Ranking

Promoted side-experiment candidates:

| priority | slug | evolvable object | exact evaluator | side-experiment verdict |
| --- | --- | --- | --- | --- |
| 1 | `list_update` | finite-state randomized list-update policy plus adversarial request generator | exact offline optimum / work-function game for small lists | best direct rediscovery experiment |
| 2 | `splay_preorder_231` | local BST rotation/access rule plus potential-template falsifier | exact Splay simulator and small offline BST optimum | best BST rediscovery experiment, with high saturation risk |
| 3 | `pairing_heaps` | heap-linking/pass rule and potential-function template | exact heap simulator plus small-trace amortized inequality checker | best self-adjusting heap artifact search |
| 4 | `quadratic_probing` | probing/hash-family parameterization and witness-family generator | finite table simulator and exact witness/collision metrics | good hashing experiment, but model-sensitive |
| 5 | `search_trees_on_trees_lp` | valid-inequality template, LP rounding rule, topology generator | STT enumeration and rational LP certificates | excellent theorem-artifact generator, less DS-rediscovery-like |
| 6 | `range_mode_queries` | candidate-list/block-summary data-structure grammar and hard-array generator | brute-force exact mode for every interval | useful stress-test, weaker rediscovery story |

Not promoted despite useful exact oracles: `imprecise_comparison_sorting`, `karp_rabin_collision_detection`, `cache_oblivious_implicit_scanning`, `succinct_compressed_structures`, `dynamic_text_indexing`, `connected_circle_segment_queries`, `dynamic_min_tree_cut`, `unified_bound_heaps`, `lazy_b_trees`, and `hashing_dictionaries`.

## Candidate 1: `list_update`

Problem or domain: classical online list update, especially the randomized competitive-ratio gap between the known lower and upper bounds.

Scores kept separate:

- theorem_project_suitability: 2/5
- openevolve_suitability: 5/5
- intellectual_interest: 4/5

Concrete evolvable object:

- finite-state randomized online policy;
- projective or non-projective pairwise decision table;
- move-to-front / transpose / paid-exchange mixture rule;
- adversarial request-sequence generator.

Exact evaluator:

- For a fixed list size `n` and request length `T`, compute candidate policy cost exactly or by exact rational transition matrices.
- Compare against exact offline optimum by dynamic programming over all permutations, or by work-function-style state values.
- Minimax loop: candidate policy proposes transition probabilities, adversary proposes request distributions or explicit traces, evaluator returns competitive ratio on the finite game.

Finite oracle or benchmark source:

- Ambuehl, Gaertner, and von Stengel, "Optimal Lower Bounds for Projective List Update Algorithms", arXiv:1002.2440, https://arxiv.org/abs/1002.2440.
- Existing repo source status: verified, access date 2026-05-15.

Mutation representation:

- discrete genome for deterministic primitive after each access: keep, move-to-front, move forward by `k`, transpose, conditional swap;
- rational probability vector over primitives;
- small finite-state automaton whose state is updated by accessed rank, last accessed item class, and local pair order;
- adversary genome as grammar over ranks, repeated phases, and perturbation blocks.

Failure modes and benchmark-overfit risks:

- Small lists can favor policies that do not factor or scale to arbitrary `n`.
- Projective policies may rediscover known lower-bound barriers rather than escape them.
- Random simulation against sampled traces is not enough; exact finite games are needed to avoid false positives.
- Competitive ratio estimates can be brittle when the offline optimum has many tied optimal transitions.

Theorem-relevant artifact that could result:

- a finite non-projective randomized policy beating known projective mixtures on all `n <= n0`, with exact certificates;
- a small adversarial trace family separating candidate policies from the `1.5` lower-bound intuition;
- LP/game dual certificates suggesting a stronger lower-bound template.

Two-week side-experiment plan:

1. Implement exact list-update DP for `n <= 5`, `T <= 12`, with costs and offline optimum independently recomputed by exhaustive permutation transitions.
2. Encode known policies and sanity-check them against hand-computed tiny cases.
3. Evolve finite-state randomized policies with exact rational or high-precision evaluation on the full trace set for small `n,T`.
4. Co-evolve adversarial trace grammars and rerun exact exhaustive checks on finalists.
5. Output policy tables, adversarial traces, and ratio certificates, not just sampled scores.

Separate from or compatible with theorem pilot:

- Separate from the STT / DS(k,1) theorem pilot. It is a clean side experiment and should not consume foreground theorem attention unless it produces a surprising certificate.

Source/source-search log:

- Sources: arXiv:1002.2440, https://arxiv.org/abs/1002.2440.
- Search terms: "list update randomized competitive ratio 1.5 1.6 post 2012"; "optimal lower bounds projective list update algorithms".
- Date searched: 2026-05-17.
- Freshness note: quick search did not surface a closure, but post-2012 online-algorithms and advice-complexity variants still need a deeper sweep before any theorem promotion.

## Candidate 2: `splay_preorder_231`

Problem or domain: Splay and nearby online BST algorithms on preorder / 231-avoiding access sequences, with careful separation of arbitrary initial-tree Splay from solved empty/aligned/special-initial-tree cases.

Scores kept separate:

- theorem_project_suitability: 3/5
- openevolve_suitability: 4/5 for counterexample and rule search, 2/5 for full theorem discovery
- intellectual_interest: 5/5

Concrete evolvable object:

- local BST rotation rule after access;
- bounded-state variant of splaying;
- access-path potential-function template;
- restricted initial-tree/access-sequence generator.

Exact evaluator:

- Exact simulator for Splay and candidate local rotation rules on all BST initial trees and all 231-avoiding permutations up to a small `n`.
- Optional small offline BST optimum via dynamic programming or integer programming for `n` small enough to audit.
- Falsifier checks candidate potentials by enumerating access steps and testing amortized inequalities.

Finite oracle or benchmark source:

- Sleator and Tarjan, "Self-Adjusting Binary Search Trees", https://www.cs.cmu.edu/~sleator/papers/Self-Adjusting.htm and stable PDF https://www.cs.cmu.edu/~sleator/papers/self-adjusting.pdf.
- Chalermsook, Goswami, Kozma, Mehlhorn, and Saranurak, "Pattern-Avoiding Access in Binary Search Trees", arXiv:1507.06953, https://arxiv.org/abs/1507.06953.
- Levy and Tarjan, "Splaying Preorders and Postorders", arXiv:1907.06309, https://arxiv.org/abs/1907.06309.
- Pareek, "Greedy BST on Permutation Initial Tree", arXiv:2407.03666, https://arxiv.org/abs/2407.03666.
- Berendsohn, Kozma, and Opler, "Optimization with Pattern-Avoiding Input", arXiv:2310.04236, https://arxiv.org/abs/2310.04236.

Mutation representation:

- decision tree over local access-path features: parent/child orientation, depth, subtree-size bins, previous access direction, and whether to stop early;
- grammar of rotation macros such as zig, zig-zig, zig-zag, semi-splay, rotate-to-depth-`d`;
- integer/rational coefficients in potentials using rank, depth, exposed ancestors, and finger-distance features.

Failure modes and benchmark-overfit risks:

- The area is saturated. A local rule may rediscover Splay or a known semi-splay variant.
- Small Catalan classes can miss recursive bad patterns.
- Greedy/geometric BST evidence does not transfer automatically to Splay rotations.
- Offline optimum for dynamic BSTs becomes expensive quickly; using Greedy as a proxy can answer the wrong question.

Theorem-relevant artifact that could result:

- a minimal obstruction to a tempting Splay-on-231 potential;
- a verified invariant for a narrow initial-tree regime not covered by empty/aligned/balanced/permutation-initial-tree results;
- a local rotation rule that rediscovers Splay-like behavior on structured access sequences, giving a direct response to the original data-structure rediscovery brief.

Two-week side-experiment plan:

1. Generate all BSTs and all 231-avoiding permutations up to `n = 8` where feasible.
2. Implement exact Splay, semi-splay, and a generic rotation-rule interpreter.
3. Score rules on total rotation/search cost and compare to exact small offline optimum for `n <= 6`.
4. Run potential-template falsification before any optimization score is trusted.
5. Deliver a table separating empty initial tree, aligned target tree, balanced target tree, permutation initial tree, and arbitrary initial tree.

Separate from or compatible with theorem pilot:

- Separate from STT / DS(k,1). It is compatible only as a background self-adjusting-BST rediscovery experiment and should not be treated as a pivot.

Source/source-search log:

- Sources: https://www.cs.cmu.edu/~sleator/papers/Self-Adjusting.htm; https://arxiv.org/abs/1507.06953; https://arxiv.org/abs/1907.06309; https://arxiv.org/abs/2407.03666; https://arxiv.org/abs/2310.04236.
- Search terms: "splay preorder traversal conjecture 231 avoiding latest 2025 2026"; "Pattern-Avoiding Access in Binary Search Trees preorder 231"; "Splaying Preorders and Postorders".
- Date searched: 2026-05-17.
- Freshness note: quick search did not find a post-2025 closure of arbitrary-initial-tree Splay on preorder/231-avoiding permutations, but author-page and citation checks remain required.

## Candidate 3: `pairing_heaps`

Problem or domain: standard two-pass pairing heap decrease-key complexity and potential-function/counterexample mining.

Scores kept separate:

- theorem_project_suitability: 3/5
- openevolve_suitability: 5/5
- intellectual_interest: 5/5

Concrete evolvable object:

- heap-linking/pass rule;
- delete-min pairing schedule;
- decrease-key cut/meld variant, explicitly marked if not standard;
- potential-function template over heap features;
- adversarial operation-trace generator.

Exact evaluator:

- Exact simulator for the standard pairing heap and candidate variants on operation traces.
- Potential inequality checker: for each primitive operation in enumerated small heap states, verify `actual_cost + Phi(after) - Phi(before) <= claimed_bound`.
- Trace adversary: maximize actual cost, amortized violation, or gap against known potentials.

Finite oracle or benchmark source:

- Fredman, Sedgewick, Sleator, and Tarjan, "The Pairing Heap: A New Form of Self-Adjusting Heap", https://www.cs.cmu.edu/~sleator/papers/Pairing-Heaps.htm.
- Pettie, "Towards a Final Analysis of Pairing Heaps", Dagstuhl document 10.4230/DagSemProc.06091.5, https://drops.dagstuhl.de/entities/document/10.4230/DagSemProc.06091.5.
- Dorfman, Kaplan, Kozma, and Zwick adjacent multipass source found in freshness search, "Improved bounds for multipass pairing heaps", PDF result https://danidorfman.com/publication/pairing-heaps-multipass/pairing-heaps-multipass.pdf.
- Adjacent self-adjusting heaps freshness source: "Efficiency of Self-Adjusting Heaps", arXiv:2307.02772, https://arxiv.org/abs/2307.02772.

Mutation representation:

- linking schedule grammar for delete-min: left-to-right, right-to-left, multipass, rank-biased, bucketed, randomized pairings;
- feature vector for potential: subtree size, rank, degree, left/right sibling position, number of marked/cut descendants, local monotonicity;
- integer/rational coefficient search with exact arithmetic and inequality violation feedback.

Failure modes and benchmark-overfit risks:

- Variants with good behavior do not solve the standard two-pass pairing heap question.
- Small traces may not expose long amortized bad behavior.
- A potential can pass all enumerated states yet fail under larger recursive constructions.
- A rule can improve empirical decrease-key by becoming a different heap, which must be labeled as rediscovery/variant rather than progress on standard pairing heaps.

Theorem-relevant artifact that could result:

- a falsified potential family, with minimal counterexample traces;
- a candidate potential that survives exhaustive small-state checking and is simple enough for proof work;
- rediscovery of multipass/smooth/slim-like ideas from an unconstrained linking-rule grammar, directly testing whether evolution can find known self-adjusting heap structure.

Two-week side-experiment plan:

1. Implement a pointer-level standard pairing-heap simulator with operation-trace replay.
2. Add exact enumeration of small heap shapes and short sequences including many decrease-key operations.
3. Search potential templates first, keeping the structure fixed to standard two-pass.
4. Only after that, enable linking-rule mutation and label all nonstandard outputs as rediscovery candidates.
5. Produce minimal violating traces and coefficient tables.

Separate from or compatible with theorem pilot:

- Separate from STT / DS(k,1). It is compatible as a pure side experiment because it can produce artifacts without asking for theorem-pilot bandwidth.

Source/source-search log:

- Sources: https://www.cs.cmu.edu/~sleator/papers/Pairing-Heaps.htm; https://drops.dagstuhl.de/entities/document/10.4230/DagSemProc.06091.5; https://arxiv.org/abs/2307.02772.
- Search terms: "standard pairing heap decrease key open problem 2025 standard two-pass pairing heap"; "improved bounds multipass pairing heaps standard two-pass open problem"; "Efficiency of Self-Adjusting Heaps pairing heap".
- Date searched: 2026-05-17.
- Freshness note: 2025/2026 search results show adjacent progress on slim/smooth/multipass heaps and still describe intermixed standard/multipass decrease-key questions as open or intriguing. This needs full-paper reading before theorem promotion.

## Candidate 4: `quadratic_probing`

Problem or domain: quadratic probing under random hashing assumptions, now narrowed after the 2024 constant-expected-time result.

Scores kept separate:

- theorem_project_suitability: 3/5
- openevolve_suitability: 5/5
- intellectual_interest: 4/5

Concrete evolvable object:

- probe-sequence parameterization;
- hash-family/table-size/load-factor parameter schedule;
- witness-family or obstruction generator;
- martingale/chunking certificate template.

Exact evaluator:

- Finite table simulator for insertions/searches under fixed table size, load factor, and probe rule.
- Exhaustive or adversarial key/hash placement search for small tables.
- Witness checker that scores clustering events, maximum displacement, insertion failure, and empirical thresholds.
- For proof-artifact mode, evaluate whether a generated witness family matches the hypotheses used in Kuszmaul-Xi-style analysis.

Finite oracle or benchmark source:

- Kuszmaul and Xi, "Towards an Analysis of Quadratic Probing", LIPIcs ICALP 2024.103, DOI 10.4230/LIPIcs.ICALP.2024.103, https://doi.org/10.4230/LIPIcs.ICALP.2024.103.
- Dagstuhl 25191 "Quadratic probing hash tables" discussion by William Kuszmaul, https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html.

Mutation representation:

- integer coefficients in polynomial/triangular probe offsets;
- table-size arithmetic choices, including power-of-two and prime-sized regimes;
- adversarial insertion-order grammar and initial-hash-position multiset;
- witness-family parameters such as cluster spacing, chunk length, and local load spikes.

Failure modes and benchmark-overfit risks:

- Simulations at finite `m` can badly overstate high-load asymptotics.
- A mutated probing rule may no longer be quadratic probing in the source-supported sense.
- Hashing model choices are decisive: full randomness, limited independence, fixed-offset probing, deletions, and rebuilds must not be mixed.
- Empirical probe counts alone are too weak; prefer obstruction or certificate search.

Theorem-relevant artifact that could result:

- a finite obstruction family suggesting why a load-factor threshold cannot be pushed by the existing proof template;
- a refined witness/certificate generator for improving constants;
- a rediscovery of known probing variants and their failure modes under the same evaluator.

Two-week side-experiment plan:

1. Reproduce finite insertion simulations for the exact ICALP 2024 model assumptions.
2. Build adversarial hash-position search for small table sizes with exact replay.
3. Evolve witness-family generators, not just probing rules.
4. Compare candidate obstruction families to the proof's chunk/witness definitions.
5. Deliver plots only as diagnostics; the main artifact is a machine-checkable family generator.

Separate from or compatible with theorem pilot:

- Separate from STT / DS(k,1). It is compatible as a compact hashing side experiment, but it should not be framed as solving the foreground theorem problem.

Source/source-search log:

- Sources: DOI 10.4230/LIPIcs.ICALP.2024.103, https://doi.org/10.4230/LIPIcs.ICALP.2024.103; Dagstuhl report https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html.
- Search terms: "quadratic probing hash tables Kuszmaul Xi follow-up 2025"; "Towards an Analysis of Quadratic Probing ICALP 2024"; "quadratic probing constant expected insertion time 0.089".
- Date searched: 2026-05-17.
- Freshness note: quick search found adjacent 2025 hashing work and expository coverage, but not a closure of the narrowed quadratic-probing frontier.

## Candidate 5: `search_trees_on_trees_lp`

Problem or domain: static search trees on trees, Golinsky's LP relaxation, integrality gaps, valid inequalities, and topology subclasses.

Scores kept separate:

- theorem_project_suitability: 4/5
- openevolve_suitability: 5/5
- intellectual_interest: 5/5

Concrete evolvable object:

- valid-inequality template for the STT depth polytope;
- LP rounding/root-selection rule;
- topology generator for edge-diameter-3, almost-star, and other constrained trees;
- objective/frequency distribution generator.

Exact evaluator:

- Enumerate all STTs for small underlying trees and compute exact depth vectors.
- Solve Golinsky-style LP instances with rational certificates where possible.
- Check candidate inequalities against all enumerated integral STT points and known fractional LP vertices.
- Compare rounded tree cost to exact optimum over enumerated STTs.

Finite oracle or benchmark source:

- Sadeh, Kaplan, and Zwick, "Search Trees on Trees via LP", arXiv:2501.17563, DOI 10.48550/arXiv.2501.17563, https://arxiv.org/abs/2501.17563.
- Bose, Cardinal, Iacono, Koumoutsos, and Langerman, "Competitive Online Search Trees on Trees", DOI 10.1137/1.9781611975994.115, arXiv:1908.00848, https://arxiv.org/abs/1908.00848.
- Berendsohn and Kozma, "Splay Trees on Trees", arXiv:2010.00931, DOI 10.1137/1.9781611977073.75, https://arxiv.org/abs/2010.00931.
- Berendsohn, Golinsky, Kaplan, and Kozma, "Fast Approximation of Search Trees on Trees with Centroid Trees", arXiv:2209.08024, DOI 10.4230/LIPIcs.ICALP.2023.19, https://arxiv.org/abs/2209.08024.
- Berendsohn thesis "Search Trees on Graphs", https://refubium.fu-berlin.de/handle/fub188/45994.

Mutation representation:

- inequality grammar over rooted-subtree, separator, component-size, and depth variables;
- coefficient vectors constrained to small integers/rationals;
- root-rounding decision tree over LP variables and topology features;
- topology generator with constrained degree sequence, diameter, and articulation patterns.

Failure modes and benchmark-overfit risks:

- Small-topology enumeration has already been pushed nontrivially; all-small-cases-pass evidence can be misleading.
- Random objective sampling can miss rare fractional vertices.
- Candidate inequalities may fail under simple topology composition.
- This is stronger as theorem-artifact search than as data-structure rediscovery.

Theorem-relevant artifact that could result:

- exact rational integrality-gap certificates;
- minimal topology/frequency witnesses for rounding failure;
- valid inequalities or falsified inequality families;
- proof-assistant-friendly small-instance enumeration logs.

Two-week side-experiment plan:

1. Reproduce the Sadeh-Kaplan-Zwick source-code tables and certificates before mutating anything.
2. Add a pure-Python enumeration layer for topologies and STTs, with Sage/LP calls isolated.
3. Evolve candidate inequalities and immediately falsify them against enumerated integral/fractional points.
4. Evolve root-rounding rules only on held-out topology families to reduce overfit.
5. Emit exact certificate files and a minimal-witness catalogue.

Separate from or compatible with theorem pilot:

- Compatible only as a background computational sidecar to the broader STT lane. It must not interrupt the foreground DS(k,1) theorem project unless the control panel later asks for a pivot.

Source/source-search log:

- Sources: https://arxiv.org/abs/2501.17563; https://arxiv.org/abs/1908.00848; https://arxiv.org/abs/2010.00931; https://arxiv.org/abs/2209.08024; https://refubium.fu-berlin.de/handle/fub188/45994.
- Search terms: "arXiv 2501.17563 Search Trees on Trees via LP follow-up 2026"; "Search Trees on Trees via LP"; "Golinsky STT LP relaxation".
- Date searched: 2026-05-17.
- Freshness note: quick search found the arXiv source and adjacent 2026 tree-search paper, but no obvious closure of static optimal STT or the LP subclass questions. Golinsky's original source remains TODO verified.

## Candidate 6: `range_mode_queries`

Problem or domain: exact static range mode query data structures, especially linear or near-linear space with improved query time.

Scores kept separate:

- theorem_project_suitability: 4/5
- openevolve_suitability: 5/5
- intellectual_interest: 4/5

Concrete evolvable object:

- block-summary/candidate-list data-structure grammar;
- query-time candidate-generation rule;
- adversarial array generator;
- lower-bound toy framework for named candidate-list schemes.

Exact evaluator:

- For each array up to a fixed `n`, brute-force exact mode for every interval.
- Given a candidate data-structure grammar, check whether its query candidate set always includes a true mode.
- Score space proxy, number of summaries, candidate-list size, and query scan work.
- Co-evolve hard arrays against proposed candidate-list rules.

Finite oracle or benchmark source:

- Chan, Durocher, Larsen, Morrison, and Wilkinson, "Linear-Space Data Structures for Range Mode Query in Arrays", arXiv:1101.4068, https://arxiv.org/abs/1101.4068.
- Greve, Jorgensen, Larsen, and Truelsen, "Cell probe lower bounds and approximations for range mode", DOI 10.1007/978-3-642-14165-2_50, https://doi.org/10.1007/978-3-642-14165-2_50.
- Durocher, He, Munro, Nicholson, and Skala, "Range majority in constant time and linear space", https://www.sciencedirect.com/science/article/pii/S0890540112001526. This is adjacent context, not evidence for exact range-mode closure.

Mutation representation:

- block partition sizes and hierarchy depth;
- stored summary fields such as top-`k` symbols, boundary-heavy symbols, sampled positions, and frequency thresholds;
- query rule grammar combining left/right fringes, full blocks, and sampled candidate sets;
- hard-array grammar: runs, periodic blocks, nested rare-heavy symbols, and adversarial boundary placements.

Failure modes and benchmark-overfit risks:

- Small arrays may reward summaries that cannot be stored in linear space asymptotically.
- Candidate-list correctness over all small intervals is not a cell-probe lower bound.
- Range majority and alpha-majority tricks are adjacent but can mislead exact mode search.
- Stronger modern upper bounds may make the old `O(sqrt n)` baseline stale.

Theorem-relevant artifact that could result:

- a small hard-array family falsifying a proposed block/candidate-list scheme;
- a grammar of summaries that consistently reduces candidate count and is simple enough to analyze;
- a benchmark suite for future exact range-mode data-structure proposals.

Two-week side-experiment plan:

1. Implement the exact all-interval mode oracle for arrays over small alphabets.
2. Encode baseline block decompositions from the known range-mode literature.
3. Evolve candidate-list rules, with a hard correctness gate before performance scoring.
4. Co-evolve adversarial arrays and hold out larger/randomized grammar families.
5. Produce a catalogue of failed rules and minimal counterexample arrays.

Separate from or compatible with theorem pilot:

- Separate from STT / DS(k,1). It is compatible as a future OpenEvolve benchmark because it is self-contained and oracle-heavy.

Source/source-search log:

- Sources: https://arxiv.org/abs/1101.4068; DOI 10.1007/978-3-642-14165-2_50; https://www.sciencedirect.com/science/article/pii/S0890540112001526.
- Search terms: "exact range mode query linear space latest 2024 2025"; "Linear-Space Data Structures for Range Mode Query in Arrays"; "cell probe lower bounds range mode".
- Date searched: 2026-05-17.
- Freshness note: quick search did not locate a closure, but the final ToCS line and post-2018 range-mode/range-majority papers must be checked before theorem promotion.

## Rediscovery Experiments

These are the most direct answers to the original OpenEvolve brief.

### Rediscovery Experiment A: List-Update Policy Evolution

Goal: test whether an evolutionary loop rediscovers move-to-front, transpose-like behavior, COMB-like randomized mixtures, or non-projective finite-state improvements.

Object: finite-state randomized list-update policy.

Evaluator: exact offline optimum / work-function game for small list sizes, with exhaustive traces or exact adversary LPs.

Success artifact: a policy table plus exact certificates showing whether it matches known strategies or escapes them on finite games.

Why this is first: it has the cleanest finite game, smallest infrastructure burden, and least ambiguity about the object being evolved.

### Rediscovery Experiment B: Local BST Rotation Rules

Goal: test whether evolution rediscovers Splay-like local rotations or finds useful restricted rules on preorder/231-avoiding access classes.

Object: local rotation macro grammar with bounded state.

Evaluator: exact simulator across all small initial trees and structured access sequences; optional offline BST optimum for tiny `n`.

Success artifact: rediscovered Splay/semi-splay rules, minimal counterexamples to naive rules, or a candidate invariant for a narrow initial-tree class.

Why this is second: it directly asks whether OpenEvolve can find self-adjusting data-structure behavior, but saturation and transfer-to-theorem risk are higher.

### Rediscovery Experiment C: Self-Adjusting Heap Linking Rules

Goal: test whether evolution rediscovers two-pass pairing, multipass-like, smooth/slim-like, or other known self-adjusting heap structures under a shared simulator.

Object: heap-linking and delete-min pairing schedule, optionally with a potential-template genome.

Evaluator: exact operation-trace simulator and small-state amortized inequality checker.

Success artifact: a rule lineage showing which known structures are rediscovered and which potential templates fail, with minimal adversarial traces.

Why this is third: it is theorem-relevant but risks confusing variants with progress on the standard two-pass pairing heap.

## Rejection Ledger

### `imprecise_comparison_sorting`

Reason rejected for this subrun: excellent finite-game OpenEvolve target, but not primarily a data-structure rediscovery object. It belongs in a broader algorithmic-game OpenEvolve queue, not the data-structure object-first report.

Source URLs/IDs:

- Ajtai, Feldman, Hassidim, and Nelson, "Sorting and Selection with Imprecise Comparisons", arXiv:1501.02911, https://arxiv.org/abs/1501.02911.
- PDF mirror in repo sources: https://people.eecs.berkeley.edu/~minilek/publications/papers/tournament_full.pdf.

Search terms:

- "imprecise comparisons randomized maximum error 2 O(n) comparisons follow-up"
- "Sorting and Selection with Imprecise Comparisons randomized error 2 maximum"

Date searched: 2026-05-17.

Could revisit if: the project explicitly wants a non-data-structure OpenEvolve finite-game benchmark. The evolvable object would be a randomized strategy table and adversary LP.

### `karp_rabin_collision_detection`

Reason rejected for this subrun: exact small-instance collision oracle is strong, but the evolvable object is less naturally a data structure. It is more an algorithm/witness-generator search unless a precise collision-detection data-structure grammar is defined.

Source URLs/IDs:

- Farach-Colton, "Detecting collisions in Karp-Rabin fingerprinting", Dagstuhl 25191 report, https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html.

Search terms:

- "Karp Rabin fingerprint collision detection fixed modulus all equal length substrings Dagstuhl 25191 Farach-Colton"
- "collision-free Karp Rabin fingerprint certification fixed prime"

Date searched: 2026-05-17.

Could revisit if: we define the evolvable object as a suffix-array/filtering algorithm grammar or as adversarial string/modulus families that feed a theorem-oriented conjecture.

### `cache_oblivious_implicit_scanning`

Reason rejected for this subrun: there is a concrete layout object, but finite cache simulations are likely to optimize outside the exact `n`-cell implicit model or miss the dynamic-update encoding barrier.

Source URLs/IDs:

- Franceschini and Grossi, "Optimal Cache-Oblivious Implicit Dictionaries", DOI 10.1007/3-540-45061-0_27, https://pages.di.unipi.it/grossi/PAPERS/icalp03.pdf.

Search terms:

- "implicit cache oblivious dictionary range reporting exact n cells"
- "Franceschini Grossi cache-oblivious implicit dictionary scanning open"

Date searched: 2026-05-17.

Could revisit if: the first object is static permutation-layout sampling with exact implicitness constraints, not a dynamic dictionary simulation.

### `succinct_compressed_structures`

Reason rejected for this subrun: grammar-DAG sampling has a plausible evolvable object, but the candidate folder bundles LZ indexing and grammar/DAG length-sampling, and the exact asymptotic notation still needs PDF/slide recovery.

Source URLs/IDs:

- Gawrychowski, "Two problems on Lempel-Ziv compression", Dagstuhl 25191 report, https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html.
- Navarro, "A graph problem with applications to grammar compression", Dagstuhl 25191 report, same URL.

Search terms:

- "Dagstuhl 25191 grammar compression DAG sampling expansion lengths Navarro"
- "Lempel-Ziv compressed indexing random access Gawrychowski Dagstuhl 25191"

Date searched: 2026-05-17.

Could revisit if: split into one precise grammar-DAG sampling problem with exact decompression oracle and space accounting.

### `dynamic_text_indexing`

Reason rejected for this subrun: small dynamic texts have exact pattern-matching oracles, but the mutable object would probably be a toy index layout and the open status is stale/model-dependent.

Source URLs/IDs:

- Chan, Hon, Lam, and Sadakane, "Compressed indexes for dynamic text collections", repo source URL https://www.researchgate.net/publication/220390557_Compressed_indexes_for_dynamic_text_collections.

Search terms:

- "dynamic compressed text index substring insertion deletion pattern search linear bits"
- "Compressed indexes for dynamic text collections follow-up dynamic self-index"

Date searched: 2026-05-17.

Could revisit if: a modern primary source gives one exact residual model and the evolvable object is a grammar of update/search decomposition with auditable bit accounting.

### `connected_circle_segment_queries`

Reason rejected for this subrun: connected segment generators and circle-query oracles are good stress tests, but they mostly evolve adversarial instances or partition heuristics, not data structures with theorem-level evaluation.

Source URLs/IDs:

- Afshani, Bosch, and Storandt, "Circle-Segment Intersection Queries in Connected Geometric Graphs", DOI 10.4230/LIPIcs.ISAAC.2025.3, https://drops.dagstuhl.de/storage/00lipics/lipics-vol359-isaac2025/html/LIPIcs.ISAAC.2025.3/LIPIcs.ISAAC.2025.3.html.

Search terms:

- "Circle-Segment Intersection Queries in Connected Geometric Graphs lower bounds connected"
- "connected geometric graph circle segment intersection query ISAAC 2025"

Date searched: 2026-05-17.

Could revisit if: the object is narrowed to a connected planar hard-instance generator for a named partition-tree oracle, with no claim of data-structure optimality.

### `dynamic_min_tree_cut`

Reason rejected for this subrun: exact small dynamic-graph recomputation is available, but the evolvable object is currently only an update-trace generator or heuristic summary, and the open status is not crisp after recent dynamic min-cut progress.

Source URLs/IDs:

- Henzinger, Krinninger, Nanongkai, and Saranurak, "Unifying and Strengthening Hardness for Dynamic Problems", https://people.csail.mit.edu/virgi/6.s078/papers/omv.pdf.
- El-Hayek, Henzinger, and Li, SODA 2025 context source, https://epubs.siam.org/doi/book/10.1137/1.9781611978322.
- El-Hayek, Henzinger, and Li, SODA 2026 context source, https://epubs.siam.org/doi/10.1137/1.9781611978971.

Search terms:

- "dynamic minimum tree cut maintained spanning tree update problem"
- "fully dynamic min cut min tree cut subroutine"

Date searched: 2026-05-17.

Could revisit if: a standalone min-tree-cut statement is verified and the evolved object is a maintained summary grammar with exact recomputation oracle.

### `unified_bound_heaps`

Reason rejected for this subrun: too broad for a first side experiment and partially subsumed by the cleaner `pairing_heaps` object search. The pointer-model working-set requirement is easy for an evaluator to violate accidentally.

Source URLs/IDs:

- Iacono, "Working set heaps with decrease-key", Dagstuhl 25191 report, https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html.

Search terms:

- "working set heaps decrease-key pointer model Dagstuhl 25191 Iacono"
- "universal optimality Dijkstra beyond worst case heaps decrease-key"

Date searched: 2026-05-17.

Could revisit if: after pairing-heap infrastructure exists, add pointer-model constraints and a working-set trace evaluator.

### `lazy_b_trees`

Reason rejected for this subrun: no obvious small exact oracle for the external-memory biased-search-tree theorem gap. Simulations are possible, but the object/evaluator pair would be weak and likely misleading.

Source URLs/IDs:

- Rysgaard and Wild, "Lazy B-Trees", DOI 10.4230/LIPIcs.MFCS.2025.87, https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.MFCS.2025.87.

Search terms:

- "Lazy B-Trees external biased search tree linear block space weighted search"
- "external memory biased search tree weighted I/O bounds"

Date searched: 2026-05-17.

Could revisit if: a static external biased-search layout problem is isolated with exact block-transfer evaluator and linear block-space accounting.

### `hashing_dictionaries`

Reason rejected for this subrun: no verified primary source or precise residual object in the candidate folder. Quadratic probing is the better hashing-side experiment.

Source URLs/IDs:

- Repo source status: TODO primary sources.

Search terms:

- "all-purpose hashing residual stable addresses succinct wasted space"
- "hashing dictionaries optimal time space tradeoff residual open problem"

Date searched: 2026-05-17.

Could revisit if: one explicit model-specific tradeoff is extracted from primary sources and paired with a concrete hash-family or probing-rule genome.

## Notes For Synthesis

- Best two-week side experiment: `list_update`, because the object and exact finite game are unusually clean.
- Best data-structure rediscovery experiment: `splay_preorder_231`, if saturation risk is acceptable.
- Best theorem-artifact generator: `search_trees_on_trees_lp`, because it can emit rational certificates and minimal witnesses.
- Best self-adjusting-structure experiment: `pairing_heaps`, but only if standard two-pass analysis and variant rediscovery are kept separate.
- Best hashing experiment: `quadratic_probing`, provided witness/certificate search is prioritized over empirical average probes.
- Background-lane rule remains active: none of these should interrupt the current STT / DS(k,1) foreground theorem project without later control-panel approval.
