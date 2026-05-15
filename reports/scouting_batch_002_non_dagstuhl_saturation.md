# Scouting Batch 002: Non-Dagstuhl-Heavy Saturation Pass

Date: 2026-05-15

Purpose: broaden the search space away from the Batch 001 cluster around Dagstuhl 25191, dynamic optimality, splay-like adaptivity, and heap folklore. This is a saturation pass, not a promotion memo. I prefer recording a niche uncertain lead over turning it into a false theorem target.

## Executive Takeaways

The best new leads are small, old-fashioned, and certificate-friendly:

1. `range_mode_queries`: exact range mode with linear or near-linear space remains a crisp range-query gap with cell-probe lower-bound context and finite-instance evaluators.
2. `persistent_arrays`: fully persistent arrays with linear space and worst-case `O(log log m)` update/lookup remains a sharp persistent-structure tradeoff target, but the primary open statement still needs Straka thesis verification beyond secondary summaries.
3. `dynamic_text_indexing`: compact dynamic text indexing has a clean old open formulation: linear-bit space with polylogarithmic substring update and pattern-search overheads.
4. `imprecise_comparison_sorting`: randomized error-2 maximum finding / sorting under imprecise comparisons is a very finite-combinatorial adaptive-sorting target.
5. `dynamic_min_tree_cut`: dynamic min-tree-cut / dynamic min-cut looks like the crispest dynamic-graph lead, but the area is hot and the project should be a subroutine or small-certificate search, not "solve dynamic min-cut."
6. `history_independent_allocation`: history-independent variable-size allocation is a tiny but real privacy/data-structure corner; it is under-attended, though the exact modern frontier needs checking.
7. `kinetic_high_dim_extent`: higher-dimensional kinetic convex hull/extent maintenance remains appealing but much less evaluator-friendly.

## Candidate Reports

### 1. Exact Range Mode With Linear Space

- short name: `range_mode_queries`
- open_status: open, with exact modern frontier requiring follow-up.
- self-contained problem statement: Preprocess an array `A[1..n]` into `O(n)` words or near-linear space so that, for any interval `[i,j]`, the data structure returns an element of maximum frequency in `A[i..j]` as fast as possible. Determine the optimal query time for linear-space exact range mode.
- primary source: Chan, Durocher, Larsen, Morrison, and Wilkinson, "Linear-Space Data Structures for Range Mode Query in Arrays," STACS 2012 / Theory of Computing Systems; arXiv page: https://arxiv.org/abs/1101.4068. Adjacent lower-bound source: Greve, Jorgensen, Larsen, and Truelsen, "Cell probe lower bounds and approximations for range mode," ICALP 2010.
- exact open gap: Durocher-Morrison/Chan et al. give the first linear-space `O(sqrt n)`-style worst-case query bound and tradeoffs; known cell-probe lower bounds are only nearly logarithmic for broad space regimes. The exact linear-space query complexity remains unresolved.
- why it matters: range mode is a canonical example of why idempotent range-query tricks fail; it matters to the small range-query / sequence-data-structure community.
- why it may be under-attended: exact mode is less glamorous than predecessor, orthogonal range reporting, or compressed indexing, and the lower bound is far from the upper bound.
- theorem-project suitability: 4/5.
- OpenEvolve suitability: 5/5.
- Lean/formalization suitability: 3/5.
- AI-collaboration fit: strong for constructing hard arrays, testing block decompositions, searching for small lower-bound reductions, and formalizing candidate query certificates.
- risks / reasons to downgrade: there may be newer conditional lower bounds or combinatorial reductions not checked here; finite hard instances may not scale; exact mode has many variants including approximate, dynamic, tree, and colored versions.
- suggested blind no-internet prompt: "Given an array `A[1..n]`, design a static data structure using `O(n)` words that returns a most frequent element in any query interval `[i,j]`. Improve on `O(sqrt n)` query time or prove a lower bound for a natural class of block/candidate-list data structures. You may use word-RAM rank/select primitives but not superlinear tables."

### 2. Fully Persistent Arrays At Linear Space And Worst-Case Log-Log Time

- short name: `persistent_arrays`
- open_status: uncertain_open.
- self-contained problem statement: Maintain a fully persistent array under point updates and point lookups over `m` updates and array length `n`, using `O(n+m)` space, with both lookup and update worst-case `O(log log m)` time.
- primary source: Dietz, "Fully persistent arrays," WADS 1989, DOI: https://doi.org/10.1007/3-540-51542-9_8. Follow-up source to verify: Milan Straka, "Fully persistent arrays with optimal worst-case access and update time," https://ufal.mff.cuni.cz/~straka/papers/2009-perarray.pdf, and Straka's thesis "Functional Data Structures and Algorithms," https://dspace.cuni.cz/handle/20.500.11956/52896.
- exact open gap: secondary summaries of Straka state a split between linear space with `O((log log m)^2 / log log log m)` worst-case time and `O(log log m)` worst-case time with superlinear space; the exact open gap is whether `O(log log m)` worst-case time is possible with linear space.
- why it matters: persistent arrays are the random-access primitive behind many persistent RAM simulations and functional data structures.
- why it may be under-attended: the problem looks like a low-level implementation tradeoff, and the best results sit in theses/older persistent-structure literature.
- theorem-project suitability: 4/5.
- OpenEvolve suitability: 3/5.
- Lean/formalization suitability: 4/5.
- AI-collaboration fit: good for formal model cleanup, recurrence/invariant checking, and small version-tree experiments; less good for discovering a new word-RAM layout unaided.
- risks / reasons to downgrade: the open statement is not yet verified from the thesis text; word-RAM/pointer-machine distinctions are easy to muddle; a newer paper may have closed the gap.
- suggested blind no-internet prompt: "Design a fully persistent array supporting `lookup(version, index)` and `update(version, index, value)` over `m` updates and initial length `n`. Use only `O(n+m)` machine words. Seek worst-case `O(log log m)` time for both operations, or prove a barrier for version-tree/order-maintenance based designs."

### 3. Compact Dynamic Text Indexing Under Substring Updates

- short name: `dynamic_text_indexing`
- open_status: open in the cited source, modern status uncertain.
- self-contained problem statement: Maintain a single dynamic text `T` under insertion and deletion of substrings. Support pattern-search queries for a pattern `P`, reporting occurrences of `P` in `T`, while using `O(|T|)` bits or otherwise compact compressed-index space.
- primary source: Chan, Hon, Lam, and Sadakane, "Compressed indexes for dynamic text collections," ACM Transactions on Algorithms 2007 / preliminary SODA-style line; PDF snippets identify the dynamic single-text question. Search result source: https://www.researchgate.net/publication/220390557_Compressed_indexes_for_dynamic_text_collections
- exact open gap: the paper asks whether a dynamic index for a single text can use `O(|T|)` bits, update a substring of length `s` in `O(s polylog |T|)` time, and search a pattern of length `p` in `O((p+occ) polylog |T|)` time.
- why it matters: dynamic compressed indexing is the string-data-structure version of "can compact indexes survive real edits?"
- why it may be under-attended: very specialized; modern compressed-index work often targets static repetitive texts or practical engineering, while fully dynamic worst-case theory is harder to state cleanly.
- theorem-project suitability: 3/5.
- OpenEvolve suitability: 4/5.
- Lean/formalization suitability: 2/5.
- AI-collaboration fit: strong for toy dynamic suffix structures, adversarial edit sequences, and checking candidate decompositions against exact suffix-array or suffix-tree oracles.
- risks / reasons to downgrade: the cited open problem is old; recent dynamic BWT/FM-index or grammar-compressed indexes may partially resolve it; "O(|T|) bits" must be reconciled with alphabet and output conventions.
- suggested blind no-internet prompt: "Maintain a mutable string under insertion/deletion of substrings. Build a compact index using linear bits, up to lower-order terms, that answers pattern-occurrence queries in near-linear-in-pattern-plus-output time times polylogarithmic overhead. Either give a data structure or isolate an obstruction."

### 4. History-Independent Variable-Size Allocation

- short name: `history_independent_allocation`
- open_status: open in the original source; modern status uncertain.
- self-contained problem statement: Design a history-independent memory allocator for variable-size records with low space and time overhead, so that the memory layout distribution reveals only the current set of allocated records and sizes, not the allocation/deallocation history.
- primary source: Naor and Teague, "Anti-persistence: History Independent Data Structures," STOC 2001; author page: https://www.wisdom.weizmann.ac.il/~naor/PAPERS/history_abs.html and PDF: https://theory.stanford.edu/~vteague/STOC01.pdf.
- exact open gap: Naor-Teague explicitly leave as their main open problem whether variable-size record allocation can be implemented with low overhead under history independence.
- why it matters: variable-size allocation is a foundational primitive for making richer history-independent dictionaries, file systems, and authenticated/privacy-preserving storage layouts.
- why it may be under-attended: history independence is a small privacy-theory/data-structure niche, and allocator details look unglamorous.
- theorem-project suitability: 3/5.
- OpenEvolve suitability: 3/5.
- Lean/formalization suitability: 3/5.
- AI-collaboration fit: useful for model formalization, exhaustive small-state layout checks, and distinguishing weak/strong history independence.
- risks / reasons to downgrade: the 2001 open problem may have been resolved in later allocator/file-system work; "low overhead" must be made quantitative; randomized layout distributions are hard to exhaustively certify.
- suggested blind no-internet prompt: "Define strong history independence for a memory allocator managing variable-size records. The observable memory state should depend only on the current multiset of live records and sizes. Design an allocator with polylogarithmic or constant expected overhead per operation and small fragmentation, or prove a lower bound in a simple RAM/block model."

### 5. Concurrent Strongly History-Independent Hash Tables

- short name: `history_independent_concurrent_hashing`
- open_status: partially resolved; residual frontier uncertain.
- self-contained problem statement: Characterize the space and synchronization needed for linearizable concurrent dictionaries whose memory representation is strongly history independent.
- primary source: Attiya, Bender, Farach-Colton, Oshman, and Schiller, "History-Independent Concurrent Objects," arXiv:2403.14445, https://arxiv.org/abs/2403.14445; and "History-Independent Concurrent Hash Tables," arXiv:2503.21016, https://arxiv.org/abs/2503.21016.
- exact open gap: the 2025 paper studies an explicit open problem and gives a lock-free strongly history-independent hash table with Robin-Hood-style structure plus lower bounds for very small cells. What remains for scouting is the tight frontier under different progress conditions, base objects, and cell capacities.
- why it matters: this brings history independence into shared-memory algorithms, a tiny but clean interface between privacy and concurrency.
- why it may be under-attended: it sits between two communities that rarely share benchmarks: concurrent algorithms and history-independent data structures.
- theorem-project suitability: 3/5.
- OpenEvolve suitability: 2/5.
- Lean/formalization suitability: 4/5.
- AI-collaboration fit: good for model checking tiny concurrent executions and representation equivalence; weak for large asymptotic algorithm invention.
- risks / reasons to downgrade: not a clean open theorem yet; the 2025 paper may already settle the most natural version; concurrency formalization cost is high.
- suggested blind no-internet prompt: "Model a concurrent set/dictionary with operations lookup, insert, and delete. Require linearizability and strong history independence: for each abstract set, all completed histories leading to it induce the same distribution on memory states. Determine the minimum cell capacity or synchronization primitive strength needed for nonblocking updates."

### 6. Higher-Dimensional Kinetic Convex Hull / Extent Maintenance

- short name: `kinetic_high_dim_extent`
- open_status: open in classic/secondary summaries; primary line needs exact verification.
- self-contained problem statement: Maintain the convex hull, diameter, width, or related extent measures of moving points in dimension greater than two using a kinetic data structure with good compactness, locality, responsiveness, and event complexity.
- primary source: Basch, Guibas, and Hershberger, "Data Structures for Mobile Data," Journal of Algorithms 1999. Handbook chapter by Guibas: https://geometry.stanford.edu/paper/g-KDS_DS-Handbook-04/g-KDS_DS-Handbook-04.pdf. Adjacent extent paper: Agarwal, Guibas, Hershberger, and Veach, "Maintaining the Extent of a Moving Point Set," Discrete & Computational Geometry 2001.
- exact open gap: higher-dimensional kinetic convex hull and extent structures are repeatedly identified as open or poorly understood; the exact target should be narrowed to one measure such as diameter or width in 3D under algebraic motion of bounded degree.
- why it matters: kinetic structures are a geometry-theory model for continuously moving data, with applications in simulation, robotics, and motion planning.
- why it may be under-attended: kinetic geometry is specialized and event-complexity proofs are technically unpleasant.
- theorem-project suitability: 3/5.
- OpenEvolve suitability: 3/5.
- Lean/formalization suitability: 2/5.
- AI-collaboration fit: moderate; useful for small moving-point instance generation and event-count counterexamples, weaker for full geometric proof synthesis.
- risks / reasons to downgrade: source verification is not yet line-level; may be too broad; higher-dimensional hull complexity can overwhelm any tidy evaluator.
- suggested blind no-internet prompt: "For `n` points in 3D moving along algebraic trajectories of constant degree, design a kinetic data structure maintaining the diameter or width. Bound number of events, processing time per event, and locality. If full maintenance is too hard, construct explicit moving-point families forcing many certificate changes."

### 7. Randomized Error-2 Maximum Finding With Imprecise Comparisons

- short name: `imprecise_comparison_sorting`
- open_status: open in the cited paper, modern status uncertain.
- self-contained problem statement: In a comparison model where comparisons are reliable only when item values differ by at least one threshold unit, find a maximum element within error 2 using as few comparisons as possible; especially determine whether randomized `O(n)` comparisons suffice.
- primary source: Ajtai, Feldman, Hassidim, and Nelson, "Sorting and Selection with Imprecise Comparisons," ICALP 2009 / arXiv:1501.02911, https://arxiv.org/abs/1501.02911 and author PDF: https://people.eecs.berkeley.edu/~minilek/publications/papers/tournament_full.pdf.
- exact open gap: the paper's conclusion lists open questions including the complexity of deterministic maximum finding with error 2 and whether randomized error 2 can be achieved using `O(n)` comparisons; it also leaves randomized sorting with error `k` open.
- why it matters: this is adaptive sorting under partial/reliable information, with clean tournament-graph interpretations.
- why it may be under-attended: it is not packaged as a data-structure problem, but its finite tournament certificates are extremely data-structure-adjacent.
- theorem-project suitability: 4/5.
- OpenEvolve suitability: 5/5.
- Lean/formalization suitability: 4/5.
- AI-collaboration fit: excellent for finite tournament search, randomized strategy synthesis, adversary LPs, and certificate checking.
- risks / reasons to downgrade: may have follow-up work in noisy sorting/tournament literature; a result for max-finding may not transfer to sorting; randomization definitions must be precise.
- suggested blind no-internet prompt: "There are `n` unknown real-valued items. A comparison between two items is guaranteed correct only if their true values differ by at least 1; otherwise either answer may be returned adversarially. Give a randomized algorithm using `O(n)` comparisons that returns an item within value 2 of the maximum with high probability, or prove a lower bound."

### 8. Dynamic Min-Tree Cut As A Subroutine For Dynamic Min-Cut

- short name: `dynamic_min_tree_cut`
- open_status: open/uncertain after recent subpolynomial progress.
- self-contained problem statement: Maintain, under edge insertions and deletions in a graph with a maintained spanning tree, the minimum cut among cuts induced by deleting one tree edge. Seek polylogarithmic update time or a lower bound.
- primary source: Henzinger, Krinninger, Nanongkai, and Saranurak, "Unifying and Strengthening Hardness for Dynamic Problems," STOC 2015 / arXiv-style PDFs including https://people.csail.mit.edu/virgi/6.s078/papers/omv.pdf. Dynamic min-cut context: El-Hayek, Henzinger, and Li, "Fully Dynamic Approximate Minimum Cut in Subpolynomial Time per Operation," SODA 2025, https://epubs.siam.org/doi/book/10.1137/1.9781611978322; and SODA 2026 proceedings page for exact/superpolylog cut-size progress: https://epubs.siam.org/doi/10.1137/1.9781611978971.
- exact open gap: the hardness paper highlights that polylogarithmic update time is unknown even for the min-tree-cut subroutine. Recent work gives `n^{o(1)}` dynamic min-cut progress, but does not obviously close the polylog/min-tree-cut question.
- why it matters: min-tree cut is a smaller handle on fully dynamic min-cut, a central dynamic graph problem.
- why it may be under-attended: dynamic min-cut is active, but this exact subroutine may be easier to isolate for computational search.
- theorem-project suitability: 3/5.
- OpenEvolve suitability: 4/5.
- Lean/formalization suitability: 2/5.
- AI-collaboration fit: good for generating edge-update adversaries, testing tree-cut maintained summaries, and searching for small hard instances or reductions.
- risks / reasons to downgrade: dynamic graph area is saturated; recent 2025/2026 advances may have changed the frontier; finite experiments may not reveal asymptotic obstacles.
- suggested blind no-internet prompt: "A graph `G` changes by edge insertions/deletions, and a spanning forest `T` is maintained. For every tree edge `e`, removing `e` defines a cut in `T`; maintain the minimum number or weight of graph edges crossing any such tree cut. Design a polylogarithmic-update data structure, or produce a lower-bound reduction for this restricted dynamic problem."

### 9. Dynamic Minimum-Cut Streaming Space Gap

- short name: `dynamic_stream_mincut_space`
- open_status: open.
- self-contained problem statement: Determine the exact one-pass dynamic-stream space complexity of computing a `(1+epsilon)` approximation to the minimum cut of a simple weighted graph under edge insertions and deletions.
- primary source: Assadi, Kapralov, and collaborators, "Space Complexity of Minimum Cut Problems in ..." ITCS 2025, PDF: https://drops.dagstuhl.de/storage/00lipics/lipics-vol325-itcs2025/LIPIcs.ITCS.2025.43/LIPIcs.ITCS.2025.43.pdf.
- exact open gap: Open Question 15 asks for the exact space complexity in one-pass dynamic streams; known bounds leave a gap between insertion-only lower bounds and fully dynamic upper bounds.
- why it matters: streaming cut sketches are a lower-bound-flavored cousin of dynamic graph data structures.
- why it may be under-attended: it is a streaming problem, so it may fall just outside the core data-structure community.
- theorem-project suitability: 3/5.
- OpenEvolve suitability: 4/5.
- Lean/formalization suitability: 2/5.
- AI-collaboration fit: good for small sketch lower-bound games and explicit hard graph distributions.
- risks / reasons to downgrade: not a data structure in the classic update/query sense; lower bounds likely require communication complexity; may duplicate active streaming work.
- suggested blind no-internet prompt: "In a one-pass turnstile stream of weighted graph edges, approximate the global minimum cut within `1+epsilon`. Establish the right space bound between the known insertion-only lower-bound scale and dynamic-stream sketch upper bounds. Try explicit communication games on small graph families."

### 10. Range Alpha-Majority Space And Output Sensitivity

- short name: `range_alpha_majority_output_sensitive`
- open_status: open in cited source, modern status uncertain.
- self-contained problem statement: Preprocess an array so that range alpha-majorities can be reported faster and/or in less space, especially output-sensitive `O(k)` query time where `k` is the number of reported alpha-majorities.
- primary source: Durocher, He, Munro, Nicholson, and Skala, "Range majority in constant time and linear space," Information and Computation 2013, https://www.sciencedirect.com/science/article/pii/S0890540112001526.
- exact open gap: the paper asks whether the `O(n log(1/alpha+1))` word space can be improved while maintaining `O(1/alpha)` query time, and whether reporting can be made output-sensitive in `O(k)` time.
- why it matters: range majority is the tractable neighbor of range mode; sharper tradeoffs may inform exact mode.
- why it may be under-attended: approximate/frequency-threshold range queries are a small subarea, and exact mode often attracts the attention instead.
- theorem-project suitability: 3/5.
- OpenEvolve suitability: 4/5.
- Lean/formalization suitability: 3/5.
- AI-collaboration fit: good for candidate-list compression experiments and small-array verifier generation.
- risks / reasons to downgrade: likely follow-up papers exist; alpha-parameter conventions vary; may be less intellectually rich than exact range mode.
- suggested blind no-internet prompt: "For an array `A[1..n]` and threshold `alpha`, report every element whose frequency in query range `[i,j]` exceeds `alpha |i-j+1|`. Seek linear or near-linear space and query time proportional to the number of answers rather than `1/alpha`, or prove this is impossible for a natural indexing scheme."

### 11. All-Purpose Hashing Residual Tradeoffs

- short name: `all_purpose_hashing_residual`
- open_status: uncertain.
- self-contained problem statement: Identify which combinations of high load, dynamic resizing, cache efficiency, stability/referential stability, very-high-probability bounds, and succinct wasted space can be achieved simultaneously by a dynamic hash table.
- primary source: Bender, Conway, Farach-Colton, Kuszmaul, and Tagliavini, "All-Purpose Hashing," arXiv:2109.04548, https://arxiv.org/abs/2109.04548. Adjacent source: Bender, Farach-Colton, John Kuszmaul, and William Kuszmaul, "On the Optimal Time/Space Tradeoff for Hash Tables," arXiv:2111.00602.
- exact open gap: "all properties at once" was a significant open problem before Iceberg hashing, and the follow-up tradeoff paper changes the space/time frontier. This pass does not yet identify a single unsolved residual theorem; use this as a source-gathering lane.
- why it matters: hash tables are the fundamental dictionary structure, and tiny asymptotic waste matters in succinct dynamic dictionaries.
- why it may be under-attended: much of the work is recent and technical; practitioners may not care about the exact asymptotics.
- theorem-project suitability: 2/5.
- OpenEvolve suitability: 3/5.
- Lean/formalization suitability: 2/5.
- AI-collaboration fit: moderate for simulation and finite-layout search; weak until a single residual conjecture is isolated.
- risks / reasons to downgrade: likely too recently active; easy to accidentally propose a solved tradeoff; not a strong candidate until the exact open line is extracted from the papers.
- suggested blind no-internet prompt: "Design a dynamic hash table storing `n` `Theta(log n)`-bit keys near the information-theoretic minimum, with high load, dynamic resizing, constant-time operations with high probability, good cache locality, and stable element addresses except during resizing. State which guarantees conflict and prove a tradeoff for a restricted framework."

### 12. Retroactive Data-Structure Lower-Bound Strengthening

- short name: `retroactive_lower_bounds`
- open_status: uncertain / lower-bound frontier.
- self-contained problem statement: Strengthen lower bounds for general transformations to retroactive data structures, especially in the cell-probe model, or find a clean explicit problem separating ordinary, partially retroactive, and fully retroactive complexity.
- primary source: Demaine, Iacono, and Langerman, "Retroactive Data Structures," ACM TALG 2007, author page: https://erikdemaine.org/papers/Retroactive_TALG/ and PDF: https://erikdemaine.org/papers/Retroactive_TALG/paper.pdf. Recent source: Chung, Demaine, Hendrickson, and Lynch, "Lower Bounds on Retroactive Data Structures," arXiv:2211.14664, https://arxiv.org/abs/2211.14664.
- exact open gap: Demaine-Iacono-Langerman record that efficient retroactivity is not automatic and cite weaker cell-probe lower bounds; Chung et al. give conditional `m^{1-o(1)}`-type lower bounds for partial retroactivity. The remaining attractive gap is an unconditional or cleaner cell-probe separation with explicit finite certificates, but this pass has not found a paper explicitly stating that exact version as open.
- why it matters: retroactivity is the temporal-data-structure analogue of persistence; lower bounds explain when time-travel operations are inherently expensive.
- why it may be under-attended: retroactivity has a small literature and the general lower-bound version is not tied to a popular application.
- theorem-project suitability: 3/5.
- OpenEvolve suitability: 4/5.
- Lean/formalization suitability: 2/5.
- AI-collaboration fit: good for explicit hard-operation sequence search and reductions from dynamic algebraic problems.
- risks / reasons to downgrade: open status is not crisp enough; lower bounds may require fine-grained conjectures rather than finite certificates; avoid treating solved priority-queue retroactivity as open.
- suggested blind no-internet prompt: "Define a simple dynamic problem with constant-time ordinary operations. Show that any partially retroactive version supporting insertion/deletion of past updates and present queries requires nearly linear overhead per operation in a strong model, or construct a faster retroactive structure. Favor explicit operation sequences and communication-style certificates."

## Promotion Decisions

Promote to candidate folders now:

- `range_mode_queries`
- `persistent_arrays`
- `dynamic_text_indexing`
- `history_independent_allocation`
- `kinetic_high_dim_extent`
- `imprecise_comparison_sorting`
- `dynamic_min_tree_cut`

Keep in report/source log only until sharpened:

- `history_independent_concurrent_hashing`
- `dynamic_stream_mincut_space`
- `range_alpha_majority_output_sensitive`
- `all_purpose_hashing_residual`
- `retroactive_lower_bounds`

## Audit Notes

- Do not overclaim old open problems. `dynamic_text_indexing`, `persistent_arrays`, and `imprecise_comparison_sorting` all need a post-2015/post-2020 follow-up sweep before promotion to top shortlist.
- Kinetic structures need line-level primary verification; the handbook chapter and encyclopedia-like summaries are useful pointers, not enough by themselves.
- Dynamic graph candidates should stay subroutine-shaped. Full dynamic min-cut is active and recent SODA 2025/2026 results changed the baseline.
- Range mode looks like the cleanest Batch 002 OpenEvolve-first candidate because finite exact oracles are easy and the high-level problem statement is stable.
