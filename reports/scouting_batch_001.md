# Scouting Batch 001: Broad Under-Attended Data-Structure Theory Search

Date: 2026-05-14

Purpose: first-pass, source-grounded scouting of candidate open problems before choosing a theorem-discovery or OpenEvolve-style computational-search project.

Important caveat: this is a scouting report, not a literature review. "Open" below means the cited source explicitly identifies an open question or unsolved gap. "Uncertain" means the topic looks promising but the exact open status needs a deeper source check.

## Executive Takeaways

The strongest first-pass candidates for this repository are not the most famous ones. The best current fits look like:

1. Quadratic probing hash tables: high OpenEvolve fit; small-instance simulation and adversarial trace generation are natural.
2. Working-set heaps with decrease-key: fresh, explicit Dagstuhl problem; theorem fit is strong, evaluator fit moderate.
3. Pairing heap exact amortized complexity: classic under-resolved self-adjusting heap problem; excellent for automated potential-search experiments.
4. Karp-Rabin collision detection: very concrete algorithmic open problem; unusually strong evaluator story.
5. Lazy B-tree / external biased-search-tree gap: niche but current; good external-memory data-structure theory target.
6. List update competitive-ratio gap: old but narrow enough for finite-state/evolutionary search.
7. Top-down path-compression proof: proof-reformulation problem, not a new data structure; excellent blind-prompt candidate.
8. Grammar/LZ compressed random access: compact-data-structure niche with explicit open questions from Dagstuhl.

Dynamic optimality remains important, but it is deliberately not over-ranked here because it is saturated and probably too hard as a first target unless narrowed to a specific lemma, lower-bound equivalence, or restricted access class.

## Candidate Reports

### 1. Quadratic Probing Correctness Beyond Tiny Load Factors

- short name: quadratic_probing
- open_status: open, but exact modern frontier needs follow-up.
- self-contained problem statement: Analyze quadratic probing hash tables under natural random hashing assumptions. Prove strong expected-time/correctness guarantees at larger constant load factors, or identify the true threshold behavior for insertion/search success.
- primary source: William Kuszmaul and Zoe Xi, "Towards an Analysis of Quadratic Probing," ICALP 2024, DOI: https://doi.org/10.4230/LIPIcs.ICALP.2024.103; summarized in Dagstuhl 25191, https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html
- exact open gap: Dagstuhl 25191 says quadratic probing had been a simple open hash-table question since 1968 and the 2024 work gives first tangible progress. The remaining gap is to sharpen the analysis beyond the currently proved positive-constant regime and understand high-load behavior.
- why it matters: quadratic probing is a simple open-addressing scheme that practitioners know, but theory still lags behind its practical simplicity.
- why under-attended: too elementary-looking for modern theory taste, and hard to analyze because dependencies in the probe sequence are awkward.
- theorem-project suitability: 4/5.
- OpenEvolve suitability: 5/5.
- AI-collaboration fit: strong for generating adversarial occupancy configurations, conjecturing thresholds, searching for witness families, and inventing potential/martingale arguments.
- risks / reasons to downgrade: could require deep probabilistic combinatorics; the main open gap may have narrowed after the 2024 paper; the "right" model of hashing must be chosen carefully.
- suggested blind no-internet prompt: "Consider an open-addressing hash table of size m. A key with hash h probes h, h+1^2, h+2^2, ... modulo m until it finds an empty slot. Assume fully random initial hashes. For load alpha, prove or disprove that insertion has constant expected probe count for every fixed alpha below some absolute constant. Develop rigorous bounds or construct obstruction families."

### 2. Working-Set Heaps With Constant-Time Decrease-Key

- short name: working_set_heaps_decrease_key
- open_status: open.
- self-contained problem statement: Design a pointer-model priority queue supporting constant-time decrease-key while also satisfying a working-set-style extract-min bound, where extracting an item costs about the logarithm of the number of operations performed while that item was present.
- primary source: John Iacono, "Working set heaps with decrease-key," open-problem section of Dagstuhl 25191, https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html
- exact open gap: the Dagstuhl report says no pointer-model data structure is known with both the working-set property and constant-time decrease-key.
- why it matters: beyond-worst-case shortest-path algorithms motivate heaps that adapt to item lifetimes while preserving graph-algorithm-friendly decrease-key.
- why under-attended: priority queues are old, but this exact adaptivity/decrease-key combination is a small specialist problem.
- theorem-project suitability: 5/5.
- OpenEvolve suitability: 3/5.
- AI-collaboration fit: strong for candidate invariants, amortized potentials, and restricted model exploration; weaker for full automated verification.
- risks / reasons to downgrade: source is a seminar problem statement, not a full paper; exact definition of "working set" for heaps has variants; impossibility may hold under natural restrictions.
- suggested blind no-internet prompt: "Define a priority queue in the pointer model with Insert, FindMin, ExtractMin, and DecreaseKey. Let the age of an extracted item be the number of heap operations performed while it was present. Seek a structure with O(1) amortized DecreaseKey and ExtractMin cost O(log age). Either propose and analyze such a structure or prove a barrier for a natural class."

### 3. Pairing Heap Exact Decrease-Key Complexity

- short name: pairing_heaps
- open_status: open.
- self-contained problem statement: Determine the true amortized complexity of decrease-key and related operations in the standard pairing heap, or close the gap between known lower and upper bounds.
- primary sources: Fredman, Sedgewick, Sleator, and Tarjan, "The Pairing Heap," Algorithmica 1986, author page: https://www.cs.cmu.edu/~sleator/papers/Pairing-Heaps.htm; Seth Pettie, "Towards a Final Analysis of Pairing Heaps," DagSemProc 06091, https://drops.dagstuhl.de/entities/document/10.4230/DagSemProc.06091.5
- exact open gap: the original paper says complete analysis remains open; Pettie says the basic complexity of this popular data structure remains open and gives a sublogarithmic upper bound near Fredman's lower bound.
- why it matters: pairing heaps are simple, practical, and self-adjusting; a final analysis would clarify a decades-old gap in amortized data-structure theory.
- why under-attended: famous among heap people, but narrow; the exact standard-heap analysis is technical and has resisted standard potentials.
- theorem-project suitability: 4/5.
- OpenEvolve suitability: 5/5.
- AI-collaboration fit: excellent for potential-function search, operation-sequence adversaries, and testing candidate amortized inequalities on small heaps.
- risks / reasons to downgrade: may be extremely hard; variants with better bounds may distract from the standard structure; automated search may rediscover known bad potentials.
- suggested blind no-internet prompt: "Analyze the standard two-pass pairing heap. Model link, insert, meld, delete-min, and decrease-key exactly. Search for a potential function proving an amortized decrease-key bound below O(log n), ideally O(log log n), while preserving O(log n) delete-min. If proof fails, construct adversarial sequences that force large decrease-key cost."

### 4. Lazy B-Trees And External Biased Search Trees

- short name: lazy_b_trees
- open_status: open for the general biased-tree subproblem; uncertain for the best project formulation.
- self-contained problem statement: Build a fully satisfactory external-memory biased search tree using linear blocks and logarithmic-in-weight I/O search guarantees, and use it to remove shortcomings in lazy B-trees or enable buffered lazy B-trees.
- primary source: Casper Moldrup Rysgaard and Sebastian Wild, "Lazy B-Trees," MFCS 2025, https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.MFCS.2025.87 and HTML full version https://drops.dagstuhl.de/storage/00lipics/lipics-vol345-mfcs2025/html/LIPIcs.MFCS.2025.87/LIPIcs.MFCS.2025.87.html
- exact open gap: the paper says the top layer of lazy search trees needs an external biased search tree; it explicitly leaves a general-purpose external-memory biased search tree as an open problem and says no known structure achieves the desired I/Os with linear blocks.
- why it matters: bridges adaptive sorted dictionaries, external memory, database cracking, and priority queues with decrease-key.
- why under-attended: very recent and technical; sits between theory of search trees and external-memory database indexing.
- theorem-project suitability: 4/5.
- OpenEvolve suitability: 2/5.
- AI-collaboration fit: good for local lemma search and design-space exploration; less obvious as an automated evaluator target.
- risks / reasons to downgrade: definitions are intricate; may require full absorption of the 2025 paper; "fully satisfactory" must be turned into a precise theorem before proof attempts.
- suggested blind no-internet prompt: "Design an external-memory data structure for a sorted set of weighted keys. Searching a key of weight w among total weight W should cost O(log_B(W/w)+1) I/Os, updates should be polylogarithmic in the same parameters, and space should be O(n/B) blocks. Either give a construction or prove a bottleneck for natural B-tree-like designs."

### 5. Karp-Rabin Fingerprint Collision Detection

- short name: karp_rabin_collision_detection
- open_status: open.
- self-contained problem statement: Given a string and a prime modulus used for Karp-Rabin fingerprints, decide whether any two distinct equal-length substrings collide under that modulus, faster than the straightforward quadratic approach.
- primary source: Martin Farach-Colton, "Detecting collisions in Karp-Rabin fingerprinting," Dagstuhl 25191, https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html
- exact open gap: the Dagstuhl report asks how fast one can detect whether any equal-length substrings collide, and asks for linear or near-linear time rather than quadratic.
- why it matters: Karp-Rabin hashing underlies many string data structures and randomized string algorithms; certifying bad moduli would be useful.
- why under-attended: feels like a technical string-algorithm subroutine rather than a flagship problem.
- theorem-project suitability: 4/5.
- OpenEvolve suitability: 5/5.
- AI-collaboration fit: excellent; finite strings and moduli give exact oracles, counterexample search, and candidate algorithm benchmarking.
- risks / reasons to downgrade: may depend on number theory and suffix-structure details; approximate rejection allowed in the problem statement must be formalized.
- suggested blind no-internet prompt: "Given string S of length n over integer alphabet and prime p, define the Karp-Rabin fingerprint of substring S[i..i+l-1] as its polynomial value modulo p. Design an algorithm faster than O(n^2) to determine whether there exist two distinct substrings of equal length with equal fingerprint but different content. Randomized one-sided error is allowed."

### 6. List Update Randomized Competitive Ratio Gap

- short name: list_update
- open_status: open.
- self-contained problem statement: Close the gap between lower and upper bounds on the optimal randomized competitive ratio for the classical online list update problem, especially beyond projective/list-factoring algorithms.
- primary source: Christoph Ambuehl, Bernd Gaertner, and Bernhard von Stengel, "Optimal Lower Bounds for Projective List Update Algorithms," arXiv:1002.2440, https://arxiv.org/abs/1002.2440
- exact open gap: the source says the optimal competitive ratio is open and lies between 1.5 and 1.6; it proves that projective algorithms cannot beat 1.6 in the partial-cost model.
- why it matters: list update is a canonical self-organizing online data-structure problem and a testbed for competitive-analysis techniques.
- why under-attended: old and no longer fashionable; the main gap is small and technically stubborn.
- theorem-project suitability: 3/5.
- OpenEvolve suitability: 5/5.
- AI-collaboration fit: strong for finite-state randomized algorithm search, adversarial sequence generation, LP/game formulations, and lower-bound certificates.
- risks / reasons to downgrade: global optimality over all online algorithms is probably hard; finite-state search may not generalize.
- suggested blind no-internet prompt: "In the online list update problem under the partial-cost model, an algorithm pays the position of the requested item and may move it forward for free. Randomized algorithms are compared against offline optimum. Find a randomized online algorithm with competitive ratio below 1.6, or prove no broad class extending projective algorithms can beat 1.6."

### 7. Top-Down Analysis Of Path Compression

- short name: path_compression_topdown
- open_status: open as a proof problem.
- self-contained problem statement: Give a simple direct proof of the inverse-Ackermann upper bound for path compression using the Seidel-Sharir top-down recurrence and the classical Ackermann function.
- primary source: Robert E. Tarjan, "Top-down analysis of path compression," Dagstuhl 25191, with reference to Seidel and Sharir, SIAM J. Comput. 2005, https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html
- exact open gap: the Dagstuhl problem asks for a simple, direct proof connecting the top-down recurrence to the classical Ackermann definition.
- why it matters: union-find/path compression is foundational; a cleaner proof could improve pedagogy and sharpen amortized-analysis tools.
- why under-attended: it is a proof-style refinement rather than a new bound.
- theorem-project suitability: 5/5.
- OpenEvolve suitability: 1/5.
- AI-collaboration fit: excellent for staged theorem discovery: blind recurrence analysis, then frontier notes, then literature.
- risks / reasons to downgrade: may be more about exposition than publishable novelty unless genuinely new; needs exact recurrence from the paper before serious attack.
- suggested blind no-internet prompt: "You are given a top-down recurrence arising in path compression analysis, based on a hierarchy J_k rather than the classical Ackermann hierarchy A_k. Prove directly that the recurrence yields an inverse-Ackermann bound when inverse Ackermann is defined using A_k. Seek a clean mapping between the two hierarchies."

### 8. Lempel-Ziv Compressed Pattern Matching And Indexing

- short name: lz_compressed_indexing
- open_status: open.
- self-contained problem statement: Improve pattern matching and random access/indexing data structures for texts represented by Lempel-Ziv compression, targeting the time/space tradeoffs posed in Dagstuhl 25191.
- primary source: Pawel Gawrychowski, "Two problems on Lempel-Ziv compression," Dagstuhl 25191, https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html
- exact open gap: the report asks two explicit questions: faster pattern matching on an LZ-compressed text, and a compact data structure for fast character indexing from an LZ representation.
- why it matters: compressed indexes are central to string algorithms and storage-heavy applications.
- why under-attended: very specialized; requires both compression combinatorics and data-structure lower/upper-bound taste.
- theorem-project suitability: 4/5.
- OpenEvolve suitability: 3/5.
- AI-collaboration fit: good for small grammar/LZ instance exploration and candidate decomposition lemmas; less direct for full theorem verification.
- risks / reasons to downgrade: notation missing from the report HTML must be recovered from slides/papers; adjacent literature is large.
- suggested blind no-internet prompt: "A string T of length N is represented by an LZ-style parse of size n. Design a compact auxiliary data structure using close to n words or n log N bits that supports random access T[i] in polylogarithmic or target time, or prove a barrier. Also consider pattern matching for a pattern P of length m directly on the compressed representation."

### 9. Grammar-Compressed Random Access Without Expansion-Length Overhead

- short name: grammar_compressed_random_access
- open_status: open.
- self-contained problem statement: Given a context-free grammar of size n producing one text T, support fast random access without storing the usual extra expansion-length term for every nonterminal.
- primary source: Gonzalo Navarro, "A graph problem with applications to grammar compression," Dagstuhl 25191, https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html
- exact open gap: the report asks whether the extra space for expansion lengths can be removed while retaining efficient access, reducing the question to a sparse DAG problem.
- why it matters: grammar-compressed text access is a compact-data-structure staple; shaving systematic overhead matters.
- why under-attended: looks like a small technical graph/DAG problem inside compressed indexing.
- theorem-project suitability: 4/5.
- OpenEvolve suitability: 4/5.
- AI-collaboration fit: strong for DAG sampling, sparse counterexamples, and conjecturing sampling schemes.
- risks / reasons to downgrade: source is brief; need the exact formal DAG problem before serious work.
- suggested blind no-internet prompt: "A straight-line grammar is a DAG whose nonterminals expand to a single text. Standard random access stores expansion lengths at many nodes. Find a sparse set of sampled nodes so every needed expansion length can be recovered in polylogarithmic time, using asymptotically less auxiliary space than storing all lengths."

### 10. Incremental Topological Sort In Near m^(4/3) Time

- short name: incremental_topological_sort
- open_status: open.
- self-contained problem statement: Maintain a topological ordering under edge insertions with a combinatorial total update-time bound around m^(4/3), matching or beating known dense/sparse tradeoffs.
- primary source: Jeremy Fineman, "Incremental topological sort," Dagstuhl 25191, https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html
- exact open gap: the report says there is reason to believe an m^(4/3)-type combinatorial bound should be possible for incremental topological sort.
- why it matters: topological maintenance is a basic dynamic graph primitive, and a combinatorial bound would clarify the gap with related cycle-detection algorithms.
- why under-attended: dynamic graph theory is active, but this exact combinatorial-maintenance target is narrower than fully dynamic connectivity or shortest paths.
- theorem-project suitability: 3/5.
- OpenEvolve suitability: 4/5.
- AI-collaboration fit: good for adversarial edge-order generation, invariant discovery, and testing local reordering strategies.
- risks / reasons to downgrade: dynamic graph area is competitive; the report statement is informal; may be too algorithm-engineering-heavy.
- suggested blind no-internet prompt: "Given a DAG on n vertices receiving m edge insertions online, maintain a valid topological ordering or detect a cycle. Seek a purely combinatorial algorithm with total update time about m^(4/3) up to polylog factors. Analyze affected intervals, relabeling strategies, and adversarial insertion sequences."

### 11. Batch-Dynamic Connectivity Without A Level Data Structure

- short name: dynamic_connectivity_no_levels
- open_status: open.
- self-contained problem statement: Simplify Monte Carlo dynamic connectivity by eliminating the level data structure in sequential or batch-dynamic algorithms while preserving worst-case small update/query guarantees.
- primary source: Quanquan C. Liu and Valerie King, "Monte Carlo Batch-Dynamic Connectivity," Dagstuhl 25191, https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html
- exact open gap: the report explicitly asks whether the level data structure can be eliminated in both sequential and batch-dynamic settings.
- why it matters: dynamic connectivity is fundamental; simplification may improve implementability and parallelism.
- why under-attended: the broad problem is saturated, but this simplification subproblem is narrow.
- theorem-project suitability: 3/5.
- OpenEvolve suitability: 3/5.
- AI-collaboration fit: moderate; useful for invariant search and randomized algorithm simulation.
- risks / reasons to downgrade: may depend heavily on details of Kapron-King-Mountjoy-style algorithms; full proof may be intricate.
- suggested blind no-internet prompt: "Consider randomized fully dynamic graph connectivity algorithms that maintain a hierarchy of levels plus Euler-tour trees. Can the hierarchy be replaced by a simpler randomized sampling or certificate scheme while preserving polylogarithmic update/query guarantees? Formalize the invariant and prove or refute it."

### 12. History-Independent Priority Queues

- short name: history_independent_priority_queues
- open_status: uncertain for exact theorem; active open-question cluster.
- self-contained problem statement: Determine how efficient a history-independent priority queue can be, especially whether optimal or near-optimal heap bounds can coexist with memory-layout distributions that reveal no operation history.
- primary source: Alexander Conway, "History independent priority queues," Dagstuhl 25191, plus executive summary discussion of history-independent heaps, https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html
- exact open gap: Dagstuhl describes active questions about reconciling history independence with optimal efficiency in priority queues, but the report excerpt does not state a single formal theorem target.
- why it matters: history independence has privacy/security motivation and recently influenced list-labeling data structures.
- why under-attended: combines privacy-flavored definitions with classic heaps; small community.
- theorem-project suitability: 3/5.
- OpenEvolve suitability: 2/5.
- AI-collaboration fit: useful for model formalization and small-state distributional checks; less direct without a fixed target theorem.
- risks / reasons to downgrade: needs a sharper primary source or notes from the talk; risk of being too vague.
- suggested blind no-internet prompt: "Define strong history independence for a priority queue: the memory representation distribution depends only on the current set of key-priority pairs. Design a heap with near-optimal Insert, FindMin, DeleteMin, and DecreaseKey, or prove a lower bound under a natural pointer or array model."

### 13. Geometric Intersection Reporting For Connected Segments And Polylines

- short name: geometric_intersection_reporting
- open_status: open.
- self-contained problem statement: Build improved intersection-reporting data structures for special geometric inputs: connected segment graphs, half-plane queries for segment/line intersection pairs, and more general polyline inputs.
- primary source: Sabine Storandt, "Some Intersection Problems," Dagstuhl 25191, https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html
- exact open gap: the report asks for an efficient segment-circle intersection structure when input segments form a connected graph, and says polyline/generalized scenarios are wide open.
- why it matters: intersection reporting is central in computational geometry; connectedness and polylines model real networks and trajectories.
- why under-attended: geometric data structures are broad, but this input-restricted reporting niche is small.
- theorem-project suitability: 3/5.
- OpenEvolve suitability: 3/5.
- AI-collaboration fit: moderate; small geometric instance generators and lower-bound reductions might help.
- risks / reasons to downgrade: missing exact asymptotic targets in the report HTML; geometry lower bounds can be reduction-heavy.
- suggested blind no-internet prompt: "Given n line segments in the plane forming a connected embedded graph, preprocess them to report all intersections with a query circle in time near O(log n + k), using near-linear or mildly superlinear space. Exploit connectedness if possible, or prove it does not help."

### 14. Kinetic Convex Hull / Extent Locality In Higher Dimensions

- short name: kinetic_data_structures
- open_status: uncertain from non-primary search result; needs primary-source verification.
- self-contained problem statement: Develop efficient, compact, responsive, and local kinetic data structures for maintaining convex hull, width, diameter, or related extent measures for moving points beyond the classic 2D setting.
- primary source: Leonidas Guibas, "Kinetic Data Structures" handbook chapter, Stanford PDF: https://geometry.stanford.edu/paper/g-KDS_DS-Handbook-04/g-KDS_DS-Handbook-04.pdf
- exact open gap: secondary search snippets and the handbook chapter point to open problems in kinetic extent structures, especially locality and higher-dimensional maintenance. Needs direct line-level verification before promotion.
- why it matters: kinetic structures connect computational geometry, motion planning, graphics, and collision detection.
- why under-attended: mature but specialized; many problems are old and technically geometric.
- theorem-project suitability: 3/5.
- OpenEvolve suitability: 2/5.
- AI-collaboration fit: useful for small moving-point event simulation; hard for full theorem proving without a precise subproblem.
- risks / reasons to downgrade: current source verification is weaker than other candidates; may require substantial computational-geometry background.
- suggested blind no-internet prompt: "For n points moving along algebraic trajectories in R^d, design a kinetic data structure maintaining the convex hull or diameter. Target compactness, responsiveness, efficiency, and locality. Identify which property fails for natural tournament-based methods and attempt to repair it."

### 15. Dynamic Optimality / Splay Tree Narrow Lemmas

- short name: splay_dynamic_optimality_narrow
- open_status: open.
- self-contained problem statement: Instead of attacking full dynamic optimality directly, isolate a narrow lemma: splay loglog-competitiveness, subsequence property, traversal/deque conjecture implication, or lower-bound equivalence in the geometric BST model.
- primary sources: Robert Tarjan, "Results and problems on self-adjusting search trees and related data structures," SWAT 2006, https://collaborate.princeton.edu/en/publications/results-and-problems-on-self-adjusting-search-trees-and-related-d; Caleb Levy and Robert Tarjan, "A New Path from Splay to Dynamic Optimality," SODA 2019, https://epubs.siam.org/doi/10.1137/1.9781611975482.80
- exact open gap: Tarjan identifies dynamic optimality and splay loglog-competitiveness as open; Levy-Tarjan states the dynamic optimality conjecture still stands and proposes the subsequence property route.
- why it matters: central self-adjusting search-tree problem.
- why under-attended: not under-attended globally; only narrow technical sublemmas may qualify.
- theorem-project suitability: 3/5 for full problem, 4/5 for a narrow lemma.
- OpenEvolve suitability: 3/5.
- AI-collaboration fit: good for restricted access-sequence classes, geometric-model search, and lower-bound comparison; poor for full conjecture.
- risks / reasons to downgrade: saturated and famously hard; easy to waste effort rediscovering known partial results.
- suggested blind no-internet prompt: "In the BST model with rotations after each search, define the cost of serving an access sequence. Investigate whether splay tree cost satisfies a subsequence monotonicity property: the cost on any subsequence is at most a constant times the cost on the original sequence plus linear overhead. Prove it for a restricted access class or find a counterexample."

## Comparison Matrix

| Candidate | Open status | Theorem fit | OpenEvolve fit | Best use |
| --- | --- | ---: | ---: | --- |
| quadratic_probing | open | 4 | 5 | OpenEvolve-first |
| working_set_heaps_decrease_key | open | 5 | 3 | theorem-first |
| pairing_heaps | open | 4 | 5 | dual theorem/evaluator |
| lazy_b_trees | open/uncertain formulation | 4 | 2 | theorem-first |
| karp_rabin_collision_detection | open | 4 | 5 | OpenEvolve-first |
| list_update | open | 3 | 5 | OpenEvolve-first |
| path_compression_topdown | open proof problem | 5 | 1 | blind theorem prompt |
| lz_compressed_indexing | open | 4 | 3 | theorem-first |
| grammar_compressed_random_access | open | 4 | 4 | dual |
| incremental_topological_sort | open | 3 | 4 | algorithm search |
| dynamic_connectivity_no_levels | open | 3 | 3 | skeptical follow-up |
| history_independent_priority_queues | uncertain target | 3 | 2 | source gathering |
| geometric_intersection_reporting | open | 3 | 3 | source gathering |
| kinetic_data_structures | uncertain | 3 | 2 | source verification |
| splay_dynamic_optimality_narrow | open | 3 | 3 | narrow only |

## Strongest Promotions

Promote now:

- `candidate_topics/quadratic_probing/`
- `candidate_topics/unified_bound_heaps/`
- `candidate_topics/lazy_b_trees/`
- `candidate_topics/list_update/`
- `candidate_topics/succinct_compressed_structures/`
- `candidate_topics/dynamic_graph_structures/`
- `candidate_topics/history_independent_data_structures/`
- `candidate_topics/external_memory_structures/`
- `candidate_topics/pairing_heaps/`
- `candidate_topics/karp_rabin_collision_detection/`
- `candidate_topics/path_compression_topdown/`

Hold for source deepening:

- kinetic extent structures;
- geometric intersection reporting;
- full dynamic optimality;
- retroactive cell-probe lower bounds;
- self-adjusting networks.

## Skeptical Notes

- Dagstuhl reports are good scouting sources, but they can be informal. Candidates sourced only to Dagstuhl need a follow-up paper, slide deck, or author note before final promotion.
- Dynamic optimality is over-famous relative to our goal. Use it only through narrow subclaims.
- "Under-attended" should not be confused with "easy." Several small candidates are likely very hard.
- OpenEvolve suitability should be judged by evaluator clarity, not mathematical importance. Quadratic probing, list update, Karp-Rabin collision detection, and pairing heaps currently have the best evaluator stories.

## Addendum: Scouting Patch 001A

Patch 001A fills two Batch 001 TODO-heavy high-priority folders:

- `candidate_topics/splay_preorder_231/`: narrowed from broad dynamic optimality to preorder / 231-avoiding Splay and fixed-pattern-avoidance subproblems, with Greedy, Splay, offline-OPT, and initial-tree distinctions separated.
- `candidate_topics/search_trees_on_trees_lp/`: promoted as a strong dual theorem/OpenEvolve candidate around static search trees on trees, Golinsky's LP, Sadeh-Kaplan-Zwick 2025 counterexamples, stars, paths, almost-stars, and polynomial-time optimality.

The addendum does not change the original Batch 001 rankings wholesale. It does suggest `search_trees_on_trees_lp` deserves near-term promotion for computational certification work, while `splay_preorder_231` should remain a narrow, saturation-aware theorem/evaluator probe.
