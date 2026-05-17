# Subrun 2R: V1 Area Re-Mining

Date searched: 2026-05-17 America/Los_Angeles.

Status: completed background-lane source scan. This report does not supersede, interrupt, or re-rank the current STT / DS(k,1) foreground theorem project. It is only input for later synthesis and control-panel review.

Source-pool boundary: re-mined the v1 dynamic/kinetic, external-memory/cache-oblivious, strings/succinct/compressed, and heap/hash/union-find/persistent/retroactive areas. I checked the requested local files first: `reports/scouting_v2/README.md`, `reports/top_20_shortlist.md`, `reports/candidate_matrix.md`, and all `candidate_topics/*/problem.md` plus `candidate_topics/*/skeptical_audit.md`. New source checks were targeted only at v1-adjacent leads, duplicate updates, freshness, and rejections.

Duplicate boundary: existing v1 slugs were treated as exclusion constraints, especially `dynamic_min_tree_cut`, `cache_oblivious_implicit_scanning`, `dynamic_text_indexing`, `pairing_heaps`, `quadratic_probing`, `unified_bound_heaps`, `lazy_b_trees`, `retroactive_data_structures`, `succinct_compressed_structures`, `kinetic_high_dim_extent`, `path_compression_topdown`, `persistent_arrays`, `hashing_dictionaries`, and `history_independent_data_structures`.

Returned viable candidates: 3. I did not pad to five.

## Candidate Findings

### 1. `dynamic_connectivity_level_elimination`

1. slug: `dynamic_connectivity_level_elimination`
2. source pool and exact source:
   - Dagstuhl 25191 report, Quanquan C. Liu and Valerie King, "Monte Carlo Batch-Dynamic Connectivity", section 4.9, https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html.
   - Baseline source cited in the report: Bruce M. Kapron, Valerie King, and Ben Mountjoy, "Dynamic graph connectivity in polylogarithmic worst case time", SODA 2013, DOI 10.1137/1.9781611973105.81.
   - Adjacent baseline source: David Gibb, Bruce Kapron, Valerie King, and Nolan Thorn, "Dynamic graph connectivity with improved worst case update time and sublinear space", arXiv:1509.06464.
3. self-contained problem statement: Fully dynamic undirected connectivity maintains a graph under edge insertions/deletions and answers whether two vertices are connected. The Kapron-King-Mountjoy line of Monte Carlo worst-case polylogarithmic algorithms uses a hierarchy of levels and cutset/connectivity substructures. The remined subproblem is: can the level data structure be eliminated altogether, in either the sequential Monte Carlo dynamic connectivity algorithm or the new batch-dynamic parallel version, while retaining worst-case polylogarithmic update/query guarantees and one-sided-error correctness?
4. exact open gap: The Dagstuhl 25191 report explicitly says the authors "present an open problem regarding whether we can eliminate the level data structure altogether in both the sequential dynamic algorithm and our algorithm." This is not the broad dynamic-connectivity problem; it is a simplification/structural question inside one randomized worst-case framework.
5. open_status: explicit.
6. freshness check:
   - Search terms: `eliminate the level data structure dynamic connectivity`, `Monte Carlo Batch-Dynamic Connectivity Liu King Cann level data structure`, `Kapron King Mountjoy dynamic connectivity level data structure`, `dynamic graph connectivity polylogarithmic worst case time level data structure 2025`.
   - Date searched: 2026-05-17.
   - Sources checked: Dagstuhl 25191 HTML/PDF report; SODA 2013 KKM source; arXiv:1509.06464; quick web search for exact quoted phrase.
   - Result: the problem source is May 2025, inside the last 24 months. No later source found in the search results closing the exact level-elimination question. Freshness confidence is medium because the batch-dynamic manuscript itself was not located as a full separate preprint.
7. why it matters: This is a rare dynamic-graph lead where the open target is not "beat the frontier" but "simplify the machinery without losing the frontier guarantee." A successful result could make randomized worst-case dynamic connectivity more teachable, implementable, and portable to batch/parallel settings.
8. literal under-attendedness score with anchor justification: 4. The exact phrase appears to have one fresh source cluster and no visible AI-collaboration work. Dynamic connectivity itself is highly active, so this is not a 5, but the level-elimination subproblem is narrower than the saturated flagship problem.
9. AI-collaboration fit: moderate-high for model extraction, invariant tracking, and counterexample generation against attempted level-free cutset summaries. AI can help isolate what each level buys and search for equivalent flat summaries.
10. theorem-project fit: 3/5. The theorem statement is crisp after the KKM/Liu-King-Cann framework is formalized, but it is embedded in a sophisticated randomized dynamic graph data structure.
11. OpenEvolve/evaluator fit: 3/5. An evaluator can simulate candidate level-free summaries on small update sequences and compare against exact connectivity, but it cannot certify worst-case polylogarithmic bounds or randomized failure probabilities by itself.
12. evolvable object if any: a replacement summary rule for maintaining sampled replacement edges/cutset witnesses using Euler-tour trees only, plus an adversarial update-sequence generator.
13. Lean/certificate fit: low-moderate. Finite execution invariants and one-sided-error statements can be formalized locally, but the randomized dynamic-graph proof stack is not a natural first Lean target.
14. risks/downgrades: Dynamic connectivity is saturated; the "level data structure" may be indispensable in a way only visible after reading the full batch-dynamic manuscript. A level-free simulator could pass small tests while failing cutset coverage or independence requirements. This must remain background context unless the full manuscript gives a clean standalone theorem target.
15. blind prompt: "Design a Monte Carlo fully dynamic connectivity data structure for undirected graphs with worst-case polylogarithmic update and query time, one-sided error, and no hierarchy of graph levels. You may use Euler-tour trees and random cutset sketches, but the maintained state should not include level-indexed subgraphs. Either give a replacement invariant proving that every needed reconnecting edge is found with high probability, or prove that a natural level-free summary cannot maintain the KKM-style guarantee."

### 2. `deferred_work_io_tradeoff`

1. slug: `deferred_work_io_tradeoff`
2. source pool and exact source:
   - Dagstuhl 25191 report, Peyman Afshani, "Simultaneous Work And I/O Optimality", section 4.10, https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html.
   - Classical baseline: Richard M. Karp, Rajeev Motwani, and Prabhakar Raghavan, "Deferred Data Structuring", SIAM Journal on Computing 17(5):883-902, DOI 10.1137/0217055.
3. self-contained problem statement: In deferred data structuring, an unsorted set of `n` values is stored for an online sequence of queries, but the total number `k` of queries is not known in advance. For predecessor/membership-like queries, Karp-Motwani-Raghavan obtain optimal RAM-work behavior such as `O(n log k)` total work when `k` is the final number of queries. The external-memory remining question is: characterize the optimal tradeoff between RAM work and block transfers for deferred predecessor/search structures when the query count is unknown online.
4. exact open gap: Afshani's Dagstuhl report says a similar performance can be achieved in the I/O model, but achieving both the RAM-work optimum and I/O optimum "seems to be impossible", leading to a work/I/O tradeoff. The exact gap to promote is not "find any external-memory deferred structure"; it is to prove or match the Pareto frontier for deferred predecessor-like queries.
5. open_status: inferred. The source gives a fresh research target and says simultaneous optimality appears impossible, but the report is not a full theorem statement with formal lower-bound parameters.
6. freshness check:
   - Search terms: `deferred data structures work I/O trade-off Afshani Brodal Sitchinava`, `Simultaneous Work And I/O Optimality deferred data structures`, `Karp Motwani deferred data structures predecessor search O(n log k)`, `deferred data structuring I/O model predecessor`.
   - Date searched: 2026-05-17.
   - Sources checked: Dagstuhl 25191 HTML/PDF snippets; Karp-Motwani-Raghavan DOI page; searches for the 2025 Afshani-Brodal-Sitchinava manuscript.
   - Result: the work/I/O tradeoff lead is fresh in the May 2025 Dagstuhl report. No full public manuscript was found in the quick check; open status stays inferred until the claimed impossibility/tradeoff parameters are extracted from a primary manuscript.
7. why it matters: It is a clean external-memory/cache-aware cousin of a classic lazy/deferred data-structure idea. Unlike broad cache-oblivious dictionary gaps, it asks for a specific two-resource frontier where the two single-resource optima conflict.
8. literal under-attendedness score with anchor justification: 4. Deferred data structures are old and niche, and the work/I/O simultaneous-optimality angle appears concentrated in a fresh small expert group. The broader external-memory lower-bound area is active, preventing a score of 5.
9. AI-collaboration fit: good for building formal cost models, generating candidate tradeoff algorithms, and stress-testing adversarial query sequences that expose work versus I/O tension.
10. theorem-project fit: 3/5 until parameters are fixed; potentially 4/5 after a clean predecessor-only statement is recovered.
11. OpenEvolve/evaluator fit: 3/5. One can simulate deferred partitioning/partial-sorting policies with both comparison-work and cache-miss/block-transfer costs, but finite traces are only heuristic for optimal asymptotic tradeoffs.
12. evolvable object if any: a deferred partition/refinement policy deciding when to sort, sample, split blocks, or build auxiliary indexes as queries arrive.
13. Lean/certificate fit: moderate for finite adversarial traces and simple lower-bound reductions; low for full external-memory lower-bound proofs.
14. risks/downgrades: The Dagstuhl HTML has mangled notation and does not expose exact bounds. The lead may already be handled in an unpublished Afshani-Brodal-Sitchinava manuscript. It is also easy to drift into `lazy_b_trees`; keep the target on query-driven preprocessing with unknown `k`, not biased updates in a B-tree.
15. blind prompt: "You are given an unsorted static set of `n` keys in external memory. Online predecessor queries arrive, and the final number `k` of queries is not known in advance. Design a deferred data structure that incrementally refines the data only as queries require it. Track two costs separately: RAM comparisons/work and I/O block transfers. Try to match the best possible RAM total work as a function of `n` and `k` and the best possible I/O bound simultaneously, or prove a tradeoff showing that both optima cannot be achieved together."

### 3. `lz77_linear_compressed_matching`

1. slug: `lz77_linear_compressed_matching`
2. source pool and exact source:
   - Dagstuhl 25191 report, Pawel Gawrychowski, "Two problems on Lempel-Ziv compression", section 5.4, https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html.
   - Baseline source: Pawel Gawrychowski, "Pattern matching in Lempel-Ziv compressed strings: fast, simple, and deterministic", ESA 2011, arXiv:1104.4203, DOI 10.1007/978-3-642-23719-5_36.
   - Earlier baseline: Martin Farach and Mikkel Thorup, "String Matching in Lempel-Ziv Compressed Strings", STOC 1995.
3. self-contained problem statement: Given a text represented by a Lempel-Ziv compressed representation of length `n` and an uncompressed pattern of length `m`, decide whether the pattern occurs in the text, without decompressing the text. The target remined subproblem is whether exact pattern matching can be done in `O(n + m)` time in the natural LZ model of the Dagstuhl statement.
4. exact open gap: The Dagstuhl report explicitly asks whether pattern matching on a Lempel-Ziv compressed text can be done in `O(n + m)` time. The 2011 Gawrychowski algorithm gives a deterministic `O(n log(N/n) + m)`-type bound, so the remaining gap is the logarithmic factor in the compressed-text term for the exact LZ model.
5. open_status: explicit.
6. freshness check:
   - Search terms: `Can pattern matching on a Lempel-Ziv compressed text be done in O(n+m)`, `Pattern matching in Lempel-Ziv compressed strings Fast simple deterministic`, `String matching in Lempel-Ziv compressed strings 2025 linear time`, `Lempel-Ziv compressed text O(n+m) pattern matching`.
   - Date searched: 2026-05-17.
   - Sources checked: Dagstuhl 25191 report; arXiv:1104.4203; DOI 10.1007/978-3-642-23719-5_36; CPM 2025 run-length grammar matching result as adjacent but not a direct LZ closure.
   - Result: the explicit question is from May 2025, inside the last 24 months. Quick search found adjacent grammar/RLSLP compressed matching progress, including CPM 2025 run-length grammar matching in linear time, but no source closing the exact LZ compressed-text `O(n+m)` question.
7. why it matters: Lempel-Ziv compression is a foundational repetitive-text model. Removing the remaining logarithmic factor would clarify whether compressed matching can be as fast as simply reading the compressed text plus pattern.
8. literal under-attendedness score with anchor justification: 3. Stringology and compressed indexing are active specialist areas, and this question comes from a major specialist. However, the exact `O(n+m)` LZ matching target is narrower than broad dynamic text indexing and does not appear to have AI-collaboration attention.
9. AI-collaboration fit: moderate-high for isolating model variants, generating hard LZ parses, testing candidate reductions to grammar matching, and searching for bottleneck examples in known algorithms.
10. theorem-project fit: 3/5. Crisp and self-contained after the LZ variant is fixed, but likely requires deep stringology machinery.
11. OpenEvolve/evaluator fit: 3/5. A finite evaluator can generate LZ parses, decompress as an oracle, and test candidate compressed matchers, but time-complexity proof is the real gap.
12. evolvable object if any: a compressed matching algorithm schema over phrase-boundary summaries, border tables, and occurrence-propagation rules; adversarial LZ parse generator.
13. Lean/certificate fit: low-moderate. Correctness of a finite compressed matcher is certifiable; asymptotic linear-time analysis over LZ references is less friendly.
14. risks/downgrades: This is close to the existing `succinct_compressed_structures` folder and must be treated as a split/update, not an independent broad string-candidate. The exact LZ model matters: LZ77 versus non-overlapping LZ77-like versus LZ78/LZW can change the answer. The CPM 2025 RLSLP result may imply a route via conversion only if the conversion preserves `O(n)` size/time for the exact LZ parse, which must be verified before promotion.
15. blind prompt: "A text `T` of length `N` is given by a Lempel-Ziv compressed representation of length `n`, and a pattern `P` has length `m`. Without decompressing `T`, decide whether `P` occurs in `T`. Existing deterministic approaches have a logarithmic factor in the compressed-text term. Seek an `O(n+m)` exact algorithm for the specified LZ model, or prove a barrier for algorithms based on phrase-boundary propagation and grammar conversion."

## Duplicate / Update Ledger

```yaml
- title_or_slug: grammar_dag_length_sampling
  subrun: 2R_v1_area_remining
  relation_to_existing_slug: "split/update of `succinct_compressed_structures`; not promoted as new candidate"
  update: "Navarro's Dagstuhl 25191 graph problem is very explicit, but a 2026 arXiv preprint on grammar-compressed random access is close enough that this must be treated as likely solved or at least heavily changed until compared line by line."
  source_urls_or_ids:
    - "Dagstuhl 25191, Gonzalo Navarro, A graph problem with applications to grammar compression, https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html"
    - "Anouk Duyster and Tomasz Kociumaka, Random Access in Grammar-Compressed Strings: Optimal Trade-Offs in Almost All Parameter Regimes, arXiv:2602.10864"
    - "Akito Takasaka and Tomohiro I, Space-Efficient SLP Encoding for O(log N)-Time Random Access, Theory of Computing Systems 2026, https://link.springer.com/article/10.1007/s00224-025-10243-w"
  search_terms:
    - "A graph problem with applications to grammar compression Navarro"
    - "expansion length of the nonterminals grammar compressed random access"
    - "Random Access in Grammar-Compressed Strings Optimal Trade-Offs in Almost All Parameter Regimes"
    - "Space-Efficient SLP Encoding O(log N)-Time Random Access"
  date_searched: 2026-05-17
  freshness_or_closure_signal: "Strong. arXiv:2602.10864 is dated 2026-02-11 and appears to attack grammar-compressed random access in the relevant low-space regime; Takasaka-I 2026 still explicitly discusses the expansion-length term."
  action_for_synthesis: "Do not promote Navarro DAG sampling without a direct comparison to arXiv:2602.10864 and the exact Dagstuhl graph formulation."

- title_or_slug: cache_oblivious_implicit_scanning
  subrun: 2R_v1_area_remining
  relation_to_existing_slug: "duplicate update only"
  update: "No new crisp subproblem beyond the existing exact-n-cell scan/range-reporting gap was found. The strict implicit model remains the only defensible formulation."
  source_urls_or_ids:
    - "Franceschini and Grossi, Optimal Cache-Oblivious Implicit Dictionaries, DOI 10.1007/3-540-45061-0_27"
    - "Brodal, Kejlberg-Rasmussen, and Truelsen, A Cache-Oblivious Implicit Dictionary with the Working Set Property, ISAAC 2010"
    - "Brodal and Kejlberg-Rasmussen, Cache-Oblivious Implicit Predecessor Dictionaries with the Working-Set Property, STACS 2012, DOI 10.4230/LIPIcs.STACS.2012.112"
  search_terms:
    - "implicit cache oblivious dictionary range reporting exact n cells"
    - "Franceschini Grossi cache-oblivious implicit dictionary scanning open"
    - "cache-oblivious implicit predecessor dictionary range queries"
  date_searched: 2026-05-17
  freshness_or_closure_signal: "No direct closure located in this targeted pass, but this remains v1 territory and should not be duplicated."
  action_for_synthesis: "Keep existing slug only."
```

## Rejection Ledger

```yaml
- title_or_slug: kinetic_3d_exact_diameter_or_width
  subrun: 2R_v1_area_remining
  reason_rejected: "This is the natural narrowing of `kinetic_high_dim_extent`, but this pass still did not find a primary source explicitly posing the exact 3D diameter/width KDS gap with current bounds. Older 2D extent papers and encyclopedia-style statements support the intuition, not enough for promotion."
  source_urls_or_ids:
    - "Agarwal, Guibas, Hershberger, and Veach, Maintaining the Extent of a Moving Point Set, DCG 2001, DOI 10.1007/s00454-001-0019-x"
    - "Author page for WADS/DCG version, https://graphics.stanford.edu/papers/extent/"
    - "Agarwal and Har-Peled, Maintaining Approximate Extent Measures of Moving Points, SODA 2001, http://dl.acm.org/citation.cfm?id=365411.365431"
  search_terms:
    - "kinetic data structures open problem 3D diameter width moving points"
    - "kinetic 3D diameter open problem data structure"
    - "kinetic width moving points 3D open problem"
    - "3D kinetic convex hull 2025 open"
  date_searched: 2026-05-17
  freshness_or_closure_signal: "Searches found old exact/approximate extent work and adjacent references, but no last-24-month primary closure or precise open-problem statement."
  could_revisit_if: "A modern kinetic-geometry survey or primary paper states an explicit 3D diameter/width KDS event/locality/responsiveness target."

- title_or_slug: incremental_topological_sort_combinatorial_bound
  subrun: 2R_v1_area_remining
  reason_rejected: "Existing `dynamic_graph_structures` audit already warned that the v1 formulation is stale or missing notation. This pass found no precise new statement beyond the Dagstuhl table entry; Bhattacharya-Kulkarni already give a randomized ~O(m^(4/3)) style result for incremental cycle detection/topological ordering."
  source_urls_or_ids:
    - "Dagstuhl 25191, Jeremy Fineman, Incremental topological sort, https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html"
    - "Bhattacharya and Kulkarni, An Improved Algorithm for Incremental Cycle Detection and Topological Ordering in Sparse Graphs, SODA/ToC source trail"
  search_terms:
    - "Dagstuhl 25191 Incremental topological sort Fineman open questions m^(4/3)"
    - "Incremental topological sort Jeremy Fineman Dagstuhl"
    - "An Improved Algorithm for Incremental Cycle Detection and Topological Ordering in Sparse Graphs"
  date_searched: 2026-05-17
  freshness_or_closure_signal: "No line-level exact Dagstuhl expression located; old v1 concern remains."
  could_revisit_if: "Fineman's slides/PDF expose a clean deterministic/combinatorial/density-regime target not covered by Bhattacharya-Kulkarni."

- title_or_slug: history_independent_priority_queues
  subrun: 2R_v1_area_remining
  reason_rejected: "The Dagstuhl report says Conway discussed open questions on history-independent priority queues and asks how efficient such queues can be, but this is too vague and overlaps `history_independent_data_structures` unless an exact operation set and history-independence notion are sourced."
  source_urls_or_ids:
    - "Dagstuhl 25191, Alexander Conway, History independent priority queues, https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html"
    - "Buchbinder and Petrank, Lower and Upper Bounds on Obtaining History Independence, DOI 10.1007/978-3-540-45146-4_26"
  search_terms:
    - "history independent priority queue open problem efficient"
    - "History independent priority queues Conway data structure"
    - "history-independent heap priority queue lower bound"
  date_searched: 2026-05-17
  freshness_or_closure_signal: "Fresh Dagstuhl mention, but no exact residual found in this targeted pass."
  could_revisit_if: "Conway slides or a paper state a precise weak/strong history-independent priority queue gap after the Buchbinder-Petrank bounds."

- title_or_slug: cache_pair_problem
  subrun: 2R_v1_area_remining
  reason_rejected: "Munro and Khodaee's cache-pair problem is fresh and interesting, but the report states hardness and an online resource-augmentation approximation rather than a crisp open problem. It is also closer to caching/online algorithms than a data-structure theorem candidate."
  source_urls_or_ids:
    - "Dagstuhl 25191, Ian Munro, Minimizing Cache Misses with Repeated Data: The Cache Pair Problem, https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html"
  search_terms:
    - "Cache Pair Problem Munro minimizing cache misses repeated data open problem"
    - "Minimizing Cache Misses with Repeated Data Cache Pair Problem"
    - "cache pair Munro Dagstuhl 25191"
  date_searched: 2026-05-17
  freshness_or_closure_signal: "Fresh 2025 source, but no source-backed open gap was found."
  could_revisit_if: "A follow-up states an explicit approximation/resource-augmentation gap or data-structure version."

- title_or_slug: simple_integer_successor_delete
  subrun: 2R_v1_area_remining
  reason_rejected: "Brodal's simple successor-delete structure is a nice micro-frontier but not an open gap as stated in the report; it is presented as a result/program about simple data structures with slightly worse bounds. This was already rejected in subrun 2F and remains rejected here."
  source_urls_or_ids:
    - "Dagstuhl 25191, Gerth Stolting Brodal, A Simple Integer Successor-Delete Data Structure, https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue05/25191/html/DagRep.15.5.1/DagRep.15.5.1.html"
    - "Gerth Stolting Brodal, Simple Data Structures with Slightly Worse Bounds, SEA 2025, DOI 10.4230/LIPIcs.SEA.2025.8"
  search_terms:
    - "Dagstuhl 25191 A Simple Integer Successor-Delete Data Structure Brodal open problem"
    - "integer successor-delete Brodal data structure"
    - "Simple Data Structures with Slightly Worse Bounds successor delete"
  date_searched: 2026-05-17
  freshness_or_closure_signal: "Fresh result, not a fresh open candidate."
  could_revisit_if: "The SEA paper or slides ask for a specific lower bound or simplification target around unweighted path compression."

- title_or_slug: persistent_arrays_stricter_model
  subrun: 2R_v1_area_remining
  reason_rejected: "The v1 persistent-array target remains likely solved or stale as stated. This pass did not find a stricter residual model precise enough to promote."
  source_urls_or_ids:
    - "Straka, Fully persistent arrays with optimal worst-case access and update time, 2009"
    - "Dietz, Fully Persistent Arrays, WADS 1989"
  search_terms:
    - "fully persistent arrays optimal worst-case access update time Straka residual open problem"
    - "persistent arrays cache-oblivious pointer machine residual"
    - "fully persistent array O(log log m) O(n+m) space"
  date_searched: 2026-05-17
  freshness_or_closure_signal: "No fresh residual found; existing audit warning stands."
  could_revisit_if: "A primary source explicitly leaves open a pointer-machine, purely functional, or cache-oblivious persistent-array variant."

- title_or_slug: retroactive_lower_bound_strengthening
  subrun: 2R_v1_area_remining
  reason_rejected: "No explicit primary source was found for a clean unconditional retroactive lower-bound strengthening in a named model. The lead still overlaps `retroactive_data_structures` and remains inferred."
  source_urls_or_ids:
    - "Demaine, Iacono, and Langerman, Retroactive Data Structures"
    - "Chung, Demaine, Hendrickson, and Lynch, Lower Bounds for Retroactive Data Structures"
  search_terms:
    - "retroactive data structures unconditional lower bound open problem"
    - "retroactive lower bounds cell probe dynamic problem open"
    - "lower bounds for retroactive data structures follow-up"
  date_searched: 2026-05-17
  freshness_or_closure_signal: "No last-24-month source-backed residual located."
  could_revisit_if: "A source states an explicit model, retroactivity type, operation set, and lower-bound target."

- title_or_slug: hashing_dictionaries_all_purpose_residual
  subrun: 2R_v1_area_remining
  reason_rejected: "The broad all-purpose hashing residual remains too vague after quadratic probing is separated out. No new under-attended model-specific hash-table gap was found that avoids overlap with `quadratic_probing` or recent active hash-table theory."
  source_urls_or_ids:
    - "Dagstuhl 25191, William Kuszmaul, Quadratic probing hash tables, DOI 10.4230/LIPIcs.ICALP.2024.103 as adjacent context"
  search_terms:
    - "all-purpose hashing residual stable addresses succinct wasted space"
    - "hashing dictionaries optimal time space tradeoff residual open problem"
    - "hash table stable addresses succinct space high probability open"
  date_searched: 2026-05-17
  freshness_or_closure_signal: "No precise residual located; active area, high fake-novelty risk."
  could_revisit_if: "A primary source states one exact combination of stability, succinct wasted space, update time, failure probability, and hash-family assumptions as open."

- title_or_slug: dynamic_text_indexing_linear_bits
  subrun: 2R_v1_area_remining
  reason_rejected: "No narrower source-backed residual was found beyond the existing stale `dynamic_text_indexing` candidate. Later dynamic compressed indexes and signature-encoding lines still make the old linear-bit substring-update target unsafe without a full model comparison."
  source_urls_or_ids:
    - "Chan, Hon, Lam, and Sadakane, Compressed indexes for dynamic text collections"
    - "Dynamic compressed self-index and signature-encoding papers, TODO exact comparison"
  search_terms:
    - "dynamic compressed text index substring insertion deletion pattern search linear bits"
    - "Compressed indexes for dynamic text collections follow-up dynamic self-index"
    - "dynamic self-index substring updates compressed space"
  date_searched: 2026-05-17
  freshness_or_closure_signal: "No clean last-24-month residual; existing v1 audit stands."
  could_revisit_if: "A modern primary source explicitly separates the single-text linear-bit substring-update model from grammar/BWT/signature compressed-space variants."
```

## Notes For Synthesis

- This subrun found only three candidate-worthy leads and one major likely-closure/update signal.
- Best new theorem candidate after cleanup: `deferred_work_io_tradeoff`, but only after the exact Afshani-Brodal-Sitchinava tradeoff statement is recovered.
- Best crisp dynamic lead: `dynamic_connectivity_level_elimination`, though it is embedded in a saturated dynamic-graph area.
- Best string lead: `lz77_linear_compressed_matching`, as a split from `succinct_compressed_structures`, not a separate broad compressed-indexing candidate.
- Do not promote `grammar_dag_length_sampling` before checking arXiv:2602.10864; this is the strongest freshness downgrade found in the run.
- Nothing here should affect the foreground STT / DS(k,1) proof lane without later synthesis and explicit control-panel approval.
