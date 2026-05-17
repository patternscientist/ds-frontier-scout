# Subrun 2A: Geometry Source Pool

Status: complete for this pass.

Date searched: 2026-05-17 UTC.

Branch: `scouting-v2-source-saturation`.

Background-lane boundary: this subrun only records geometry candidates for later synthesis and control-panel review. It does not supersede or interrupt the current STT / DS(k,1) foreground theorem project.

Duplicate check: checked `candidate_topics/` slugs and `reports/top_20_shortlist.md` before proposing candidates. Existing geometry-adjacent slugs include `connected_circle_segment_queries`, `geometric_data_structures`, `kinetic_data_structures`, and `kinetic_high_dim_extent`; `connected_circle_segment_queries` is already in the top-20 shortlist.

Search discipline: searched only the assigned geometry source pool and immediately adjacent references: SoCG/Dagstuhl proceedings, CCCG proceedings/problem-session papers, JoCG papers with open-problem sections, Jeff Erickson problem pages, TOPP entries only when they were adjacent to dynamic geometric data-structure source trails, and author-maintained geometry/data-structure pages.

Candidate count: 4 viable candidates. I did not create or update any `candidate_topics/` folders.

## Viable Candidates

### 1. `dynamic_planar_nearest_neighbor_logarithmic_full`

1. slug: `dynamic_planar_nearest_neighbor_logarithmic_full`
2. source pool and exact source:
   - Source pool: dynamic geometric proximity with explicit source trail; SoCG adjacent update.
   - Exact sources:
     - TOPP Problem 63, "Dynamic Planar Nearest Neighbors", https://topp.openproblem.net/p63.
     - John Iacono and Yakov Nekrich, "Incremental Planar Nearest Neighbor Queries with Optimal Query Time", SoCG 2025, DOI `10.4230/LIPIcs.SoCG.2025.59`, https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2025.59.
   - Search terms:
     - `"Dynamic Planar Nearest Neighbors" "O(log n)"`
     - `"dynamic planar nearest neighbor" "SoCG 2025"`
     - `"fully dynamic planar nearest neighbor" "O(log n)"`
     - `"dynamic 3D convex hull" "nearest neighbor" "2026" "retracted"`
   - Date searched: 2026-05-17 UTC.
3. self-contained problem statement: Maintain a dynamic set of `n` planar points under arbitrary insertions and deletions, and answer exact Euclidean nearest-neighbor queries, with all operations in `O(log n)` worst-case or amortized time using near-linear space.
4. exact open gap: TOPP states the fully dynamic `O(log n)` target as open. SoCG 2025 gives `O(log n)` query time with `O(log^(1+epsilon) n)` amortized insertion time in the insertion-only setting, and analogous semi-online/offline variants, but does not close the arbitrary deletion case.
5. open_status: explicit.
6. freshness check:
   - Last-24-month sources checked: SoCG 2025 Iacono-Nekrich; search results for 2025/2026 dynamic planar nearest neighbor and dynamic 3D convex hull applications.
   - Result: the 2025 result is a substantial freshness signal but only for insertion-only, semi-online, and offline/persistent variants. A SODA 2026 result surfaced in search as "RETRACTED: Dynamic 3D Convex Hulls Revisited and Applications"; because it is retracted, this subrun does not use it as a closure signal.
7. why it matters: Dynamic planar nearest neighbor is the closest 2D analogue of balanced search trees for ordered sets. The lifting equivalence to 3D dynamic convex hulls makes progress here relevant to several geometric data-structure primitives.
8. literal under-attendedness score with anchor justification: 3. The problem is not obscure; it is a specialist geometric data-structure problem with regular but slow progress and at least one very recent SoCG paper. It has no apparent AI-collaboration attention, but it is too central for a 4 or 5.
9. AI-collaboration fit: medium. AI can help isolate semi-dynamic-to-fully-dynamic obstacles, search for fractional-cascading certificates, and stress-test candidate decomposable-search schemes on finite update traces.
10. theorem-project fit: medium. The statement is crisp, but the likely proof burden is high and technical, with mature lower-envelope and 3D hull machinery.
11. OpenEvolve/evaluator fit: medium. Exact finite evaluators exist for update/query traces: maintain a point set, compare candidate nearest-neighbor structures against brute force, and generate adversarial update sequences. This helps falsify proposed invariants but does not certify asymptotic bounds.
12. evolvable object if any: update schedules plus hierarchical decompositions of point sets/Voronoi diagrams; candidate certificate rules that decide when a substructure can be skipped during a query.
13. Lean/certificate fit: low to medium. Small geometric certificates can be checked, but formalizing dynamic randomized geometry and nearest-neighbor correctness would be heavy.
14. risks/downgrades:
   - The full problem is a classic, not deeply under-attended.
   - Recent partial progress may indicate the remaining fully dynamic case is technically saturated.
   - Need to separate Euclidean nearest neighbor from general-distance, approximate, semi-online, offline, and 3D hull variants.
15. blind prompt:

```text
Let S be a dynamic set of n points in the Euclidean plane. The data structure must support insertion of a point, deletion of a point, and exact nearest-neighbor query for an arbitrary query point q. Give a near-linear-space data structure with O(log n) time per operation, or prove a meaningful barrier in a standard comparison, pointer-machine, word-RAM, or cell-probe model. You may use standard static planar point-location and Voronoi-diagram facts, but do not assume any dynamic nearest-neighbor theorem beyond balanced binary search trees in one dimension.
```

Source says: TOPP explicitly marks the fully dynamic `O(log n)` problem open; SoCG 2025 explicitly solves insertion-only and related restricted dynamic scenarios with optimal query time.

Inference from sources: the exact residual target is the arbitrary insertion/deletion case with the same logarithmic operation bound.

### 2. `dynamic_disconnected_planar_point_location`

1. slug: `dynamic_disconnected_planar_point_location`
2. source pool and exact source:
   - Source pool: SoCG point-location proceedings and author-maintained geometry/data-structure page.
   - Exact sources:
     - Eunjin Oh and Hee-Kap Ahn, "Point Location in Dynamic Planar Subdivisions", SoCG 2018, DOI `10.4230/LIPIcs.SoCG.2018.63`, https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2018.63.
     - Yakov Nekrich author page, "Point Location", https://pages.mtu.edu/~yakov/research.html.
     - Yakov Nekrich, "Dynamic planar point location in optimal time", STOC 2021, DOI `10.1145/3406325.3451100`, used only as adjacent freshness context for the connected case.
   - Search terms:
     - `"Point Location in Dynamic Planar Subdivisions" "not necessarily connected"`
     - `"dynamic planar point location" "non-connected" "2025"`
     - `"dynamic planar subdivisions" "point location" "2024" "2025"`
     - `"Optimal-Time Dynamic Planar Point Location in Connected Subdivisions" non-connected`
   - Date searched: 2026-05-17 UTC.
3. self-contained problem statement: Maintain a possibly disconnected planar subdivision under edge insertions and deletions, and answer point-location queries asking for the face containing a query point, ideally with linear space and near-logarithmic or logarithmic update and query time.
4. exact open gap: Oh-Ahn give linear space, `O(sqrt(n) log n (log log n)^(3/2))` amortized update time, and `O(log n (log log n)^2)` query time for possibly disconnected subdivisions. Nekrich's 2021 optimal result resolves connected subdivisions. The apparent residual is to obtain logarithmic or near-logarithmic update time for fully dynamic possibly disconnected subdivisions.
5. open_status: inferred.
6. freshness check:
   - Last-24-month sources checked: searches for 2024-2026 non-connected/general dynamic planar subdivision point location; Nekrich's maintained point-location page.
   - Result: found connected-case closure and continuing citations, but no assigned-pool closure of the disconnected/general fully dynamic update gap.
7. why it matters: Dynamic point location is a core geometric dictionary problem. The disconnected case blocks a clean "all planar subdivisions are solved" story and may require a different structural invariant than connected vertical-ray-shooting reductions.
8. literal under-attendedness score with anchor justification: 4. The connected case received major attention and was resolved, but this disconnected residual appears to have few explicit modern citations by name and no AI-collab attention.
9. AI-collaboration fit: medium. AI can help search for reductions from disconnected to connected instances, generate adversarial subdivisions, and test local update decompositions.
10. theorem-project fit: medium-high. The residual is crisp enough for staged proof attempts once the update model is pinned down, though the literature machinery is nontrivial.
11. OpenEvolve/evaluator fit: medium. A finite evaluator can maintain planar embeddings, run exact face queries, and stress-test candidate update schemes, especially for disconnected components nesting and merging.
12. evolvable object if any: a decomposition of a disconnected subdivision into maintained connected pieces plus auxiliary search structure over containment/nesting.
13. Lean/certificate fit: medium. Planar subdivision invariants and face-location certificates are formalizable in principle; the dynamic amortized analysis would be the harder part.
14. risks/downgrades:
   - The exact target may have been closed under another name such as vertical ray shooting, dynamic trapezoidal maps, or dynamic planar maps.
   - The problem may be considered less natural if applications mostly need connected subdivisions.
   - Need to distinguish arbitrary segment insert/delete from topologically valid subdivision updates.
15. blind prompt:

```text
Design a linear-space fully dynamic data structure for point location in a planar subdivision whose underlying embedded graph may be disconnected. Updates insert or delete noncrossing open edges while preserving a valid planar subdivision. A query point must return its containing face. Aim for O(log n polyloglog n) or O(log n) query and update time. Clearly state the update model and prove correctness of the maintained decomposition.
```

Source says: SoCG 2018 explicitly handles non-connected subdivisions with sublinear update time; Nekrich's maintained page explicitly says the connected dynamic point-location problem was completely resolved.

Inference from sources: the disconnected fully dynamic logarithmic-update case remains a plausible residual gap, but this needs a focused citation sweep before promotion.

### 3. `dynamic_orthogonal_range_reporting_update_exponent`

1. slug: `dynamic_orthogonal_range_reporting_update_exponent`
2. source pool and exact source:
   - Source pool: JoCG and SoCG dynamic geometric range searching with explicit source trail.
   - Exact sources:
     - Timothy M. Chan and Konstantinos Tsakalidis, "Dynamic Orthogonal Range Searching on the RAM, Revisited", JoCG 9(2):45-66, DOI `10.20382/jocg.v9i2a5`, https://jocg.org/index.php/jocg/article/view/3065.
     - SoCG 2017 proceedings version, DOI `10.4230/LIPIcs.SoCG.2017.28`, https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2017.28.
   - Search terms:
     - `"Dynamic orthogonal range searching on the RAM, revisited" open problem`
     - `"dynamic 2-d orthogonal range reporting" "2025"`
     - `"dynamic orthogonal range reporting" "word RAM" "update time"`
     - `"dynamic orthogonal range searching" "O(log n / log log n + k)" "update"`
   - Date searched: 2026-05-17 UTC.
3. self-contained problem statement: Store a dynamic set of planar points on a word RAM so that axis-aligned rectangle reporting queries return all `k` points in the query rectangle in optimal `O(log n / log log n + k)` query time, while minimizing amortized update time with near-linear space.
4. exact open gap: Chan-Tsakalidis achieve optimal query time with `O(log^(2/3+o(1)) n)` amortized update time, and `O(log^(1/2+epsilon) n)` update time for 3-sided queries. The residual is to improve the update exponent, or prove that a nontrivial update lower bound separates fully dynamic reporting from partially dynamic or simpler orthogonal-search problems.
5. open_status: inferred.
6. freshness check:
   - Last-24-month sources checked: JoCG page, SoCG version, dblp/current search for 2024-2026 dynamic orthogonal range reporting updates.
   - Result: no assigned-pool result found closing the update-exponent gap. Freshness is weaker than candidate 1 because the main source is 2017/2019.
7. why it matters: Dynamic orthogonal range reporting is a central geometric data-structure benchmark in the word RAM. The query bound is essentially optimal, making the update exponent a clean residual frontier.
8. literal under-attendedness score with anchor justification: 3. This is a mature specialist area with regular but slow work and no visible AI-collaboration focus; it is not obscure enough for a 4 because it sits in a central range-searching line.
9. AI-collaboration fit: medium. AI can help search for simplified decompositions, candidate recurrence improvements, and finite counterexamples to proposed grid/recursive schemes.
10. theorem-project fit: medium. The target is precise, but proofs rely on low-level word-RAM packing and dynamic range-reporting machinery.
11. OpenEvolve/evaluator fit: medium-low. Finite evaluators can test recursive grid layouts and update/query traces, but asymptotic exponent improvements will be hard to certify from small instances.
12. evolvable object if any: recursive grid decomposition parameters, bucketing thresholds, rebuilding schedules, and packed-table microstructures for dynamic reporting.
13. Lean/certificate fit: low. Word-RAM bit packing and amortized rebuilds are awkward for Lean. A smaller recurrence/cost certificate might be formalized.
14. risks/downgrades:
   - The open target is inferred rather than explicitly posed as an open problem in the abstract.
   - The area is technically mature and may be too saturated for quick AI-assisted proof gains.
   - A follow-up may have improved the exponent under adjacent terminology such as dynamic dominance, stabbing, or vertical ray shooting.
15. blind prompt:

```text
In the word RAM model, maintain a dynamic set of n points in rank space under insertions and deletions. A query is an axis-aligned rectangle and must report all k contained points. Assume the goal query time is O(log n / log log n + k) with near-linear space. Try to improve the amortized update time below O(log^(2/3+o(1)) n), or identify a barrier for a natural recursive grid-and-rebuilding framework.
```

Source says: the JoCG/SoCG source explicitly presents the current update/query bounds and calls the problem longstanding.

Inference from sources: the remaining open gap is update-time improvement or lower bounds under optimal query time.

### 4. `higher_dim_rectangle_stabbing_word_ram_linear_space`

1. slug: `higher_dim_rectangle_stabbing_word_ram_linear_space`
2. source pool and exact source:
   - Source pool: JoCG open-problem section; geometric range searching / rectangle stabbing.
   - Exact sources:
     - Timothy M. Chan, Yakov Nekrich, Saladi Rahul, and Konstantinos Tsakalidis, "Orthogonal Point Location and Rectangle Stabbing Queries in 3-d", JoCG 13(1):399-428, DOI `10.20382/jocg.v13i1a15`, https://jocg.org/index.php/jocg/article/download/4009/3143/11907.
     - ICALP 2018 proceedings version, DOI `10.4230/LIPIcs.ICALP.2018.31`, https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2018.31.
   - Search terms:
     - `"4-d rectangle stabbing" "word RAM" "open problem"`
     - `"Orthogonal Point Location and Rectangle Stabbing Queries in 3-d" "higher dimensions"`
     - `"higher-dimensional rectangle stabbing" "word RAM" "linear space"`
     - `"rectangle stabbing" "challenging open problem" "word RAM"`
   - Date searched: 2026-05-17 UTC.
3. self-contained problem statement: Preprocess `n` axis-aligned boxes/rectangles in dimension `d >= 4` using linear or near-linear word-RAM space so that a query point reports all `k` boxes containing it with query time matching the best plausible lower-bound scale, ideally near `O(log_w n + k)` or the natural high-dimensional analogue.
4. exact open gap: The 2022 JoCG paper obtains optimal/near-optimal 3D rectangle-stabbing and related point-location structures. In its higher-dimensional discussion, it says that closing the higher-dimensional rectangle-stabbing gap in the word RAM would be a challenging open problem; the simple segment-tree extension costs factors of `log n` per extra dimension.
5. open_status: explicit.
6. freshness check:
   - Last-24-month sources checked: searches for 2024-2026 higher-dimensional rectangle stabbing, orthogonal point location, and word-RAM rectangle stabbing; dblp/current pages for authors.
   - Result: no assigned-pool closure found. Some recent shallow-cutting/I/O-model results surfaced but did not appear to close the word-RAM linear-space stabbing target.
7. why it matters: Rectangle stabbing is a canonical geometric intersection-query problem. A higher-dimensional word-RAM breakthrough would clarify how far the 3D bit-packing/grid techniques scale.
8. literal under-attendedness score with anchor justification: 4. It is in a specialist subfield with a small active circle and no visible AI-collaboration attention; it appears less frequently cited by name than dynamic nearest neighbor or dynamic range reporting.
9. AI-collaboration fit: medium-low. AI can explore recursive reductions and produce finite obstruction examples, but the likely proof is technical.
10. theorem-project fit: medium. The open gap is explicit, narrow, and source-supported; however, it likely requires deep knowledge of orthogonal range lower/upper-bound frameworks.
11. OpenEvolve/evaluator fit: low to medium. Finite evaluators can compare recursive stabbing decompositions and microstructure choices, but they will not certify asymptotic word-RAM optimality.
12. evolvable object if any: recursive dimension-reduction scheme, grid-cell encoding, packed lookup microstructure, or threshold schedule for high-dimensional stabbing.
13. Lean/certificate fit: low. Could formalize a recurrence-bound certificate, but not the full word-RAM construction easily.
14. risks/downgrades:
   - "Higher-dimensional analogue" must be fixed precisely before proof attempts.
   - There may be model-specific lower bounds in pointer-machine or cell-probe literature that make some targets impossible.
   - The problem could be too close to active range-searching theory and not sufficiently evaluator-friendly.
15. blind prompt:

```text
Consider static rectangle stabbing in dimension d >= 4 on the word RAM: preprocess n axis-aligned boxes so that a query point reports all boxes containing it. Seek a linear- or near-linear-space data structure improving the standard segment-tree lift from 3D, or prove a lower bound for a natural recursive grid/segment-tree framework. State the dimension, word-size assumptions, and target query bound explicitly.
```

Source says: the JoCG paper explicitly identifies higher-dimensional word-RAM rectangle stabbing as a challenging open problem after giving 3D results.

Inference from sources: the strongest scoutable target is to beat the naive per-dimension logarithmic lift while retaining linear-ish space.

## Duplicate / Existing-Lead Updates Not Counted As New Candidates

### `connected_circle_segment_queries`

- Duplicate status: existing folder and top-20 shortlist item.
- Source pool hit: ISAAC/geometry data-structure lead already recorded by prior batch; this subrun did not create a new slug.
- Action: no new folder update. Later synthesis can treat this as already represented in the geometry lane.

### `kinetic_high_dim_extent`

- Duplicate status: existing folder.
- Source pool hit:
  - Leonidas Guibas, "Kinetic Data Structures" handbook chapter PDF, https://geometry.stanford.edu/paper/g-KDS_DS-Handbook-04/g-KDS_DS-Handbook-04.pdf.
  - Handbook of Discrete and Computational Geometry motion chapter mirror, https://www.csun.edu/~ctoth/Handbook/chap53.pdf.
- Search terms:
  - `"kinetic data structures" "open problems" "3D" "diameter"`
  - `"kinetic convex hull" "dimensions d >= 3" "open problems"`
  - `"kinetic width" "open problem" "three dimensions"`
- Date searched: 2026-05-17 UTC.
- Source signal: the KDS chapter explicitly lists efficient, responsive, local, compact KDSs for convex hull in dimensions `d >= 3`, smallest enclosing disk, Voronoi-event bounds, and kinetic triangulation as open problems.
- Reason not counted as a new viable candidate: it overlaps `kinetic_high_dim_extent`, and the existing audit already says the candidate is too broad. A future promotion should split it, probably to `kinetic_3d_convex_hull_kds` or `kinetic_smallest_enclosing_disk_2d`, after checking post-2016 kinetic extent/proximity work.

## Rejection Ledger

```yaml
- title_or_slug: connected_circle_segment_queries
  subrun: 2A_geometry
  reason_rejected: Duplicate existing candidate and top-20 item; not a new proposal for this subrun.
  source_urls_or_ids:
    - candidate_topics/connected_circle_segment_queries/problem.md
    - reports/top_20_shortlist.md
  search_terms:
    - "connected circle segment queries ISAAC 2025"
  date_searched: 2026-05-17 UTC
  freshness_or_closure_signal: Existing repo audit already records ISAAC 2025 future-work status.
  could_revisit_if: Later synthesis wants a geometry-incumbent comparison within the source pool.

- title_or_slug: kinetic_3d_convex_hull_kds
  subrun: 2A_geometry
  reason_rejected: Strong source signal but duplicate/overlap with existing broad `kinetic_high_dim_extent`; needs narrowing and post-2016 freshness before a new slug.
  source_urls_or_ids:
    - https://geometry.stanford.edu/paper/g-KDS_DS-Handbook-04/g-KDS_DS-Handbook-04.pdf
    - https://www.csun.edu/~ctoth/Handbook/chap53.pdf
  search_terms:
    - "kinetic data structures open problems 3D diameter"
    - "kinetic convex hull dimensions d >= 3 open problems"
  date_searched: 2026-05-17 UTC
  freshness_or_closure_signal: Open problem appears in handbook sources; no last-24-month closure found in quick assigned-pool search, but source is old and broad.
  could_revisit_if: Split to one exact measure/motion model and verify recent KDS literature.

- title_or_slug: proximate_planar_point_location_linear_space
  subrun: 2A_geometry
  reason_rejected: Interesting adaptive point-location lead, but the open gap is inferred rather than source-stated; searches found known O(n log log n)-space proximate point-location results and later adaptive point-location uses, not a crisp open-problem statement.
  source_urls_or_ids:
    - https://erikdemaine.org/papers/PointSearching_CCCG2002/paper.pdf
    - https://erikdemaine.org/papers/PointSearching_CGTA/paper.pdf
    - https://nyuscholars.nyu.edu/en/publications/proximate-planar-point-location
    - https://cse.hkust.edu.hk/faculty/scheng/pub/ptisaac2015full.pdf
  search_terms:
    - "Proximate planar point location open"
    - "Proximate planar point location O(n log log n) O(n)"
    - "point location dynamic finger 2024 computational geometry"
  date_searched: 2026-05-17 UTC
  freshness_or_closure_signal: 2026 ITCS prediction paper cites proximate point location as context, not as an open linear-space residual.
  could_revisit_if: A primary source explicitly asks for linear-space proximate point location or a sharper dynamic-finger analogue.

- title_or_slug: hyperbolic_dynamic_approximate_nearest_neighbor
  subrun: 2A_geometry
  reason_rejected: Likely solved as a dynamic approximate nearest-neighbor target by JoCG 2025 rather than open.
  source_urls_or_ids:
    - https://jocg.org/index.php/jocg/article/view/5499
    - DOI 10.20382/jocg.v16i2a5
  search_terms:
    - "dynamic approximate nearest neighbour hyperbolic space open problem"
    - "hyperbolic quadtree dynamic nearest neighbour JoCG 2025"
  date_searched: 2026-05-17 UTC
  freshness_or_closure_signal: JoCG 2025 states a dynamic data structure with O(log n) updates and queries for approximate NN in hyperbolic space.
  could_revisit_if: A different residual is extracted, such as exact NN, dimension dependence, or lower bounds for hyperbolic spanners.

- title_or_slug: connected_dynamic_planar_point_location
  subrun: 2A_geometry
  reason_rejected: Solved for connected subdivisions by Nekrich STOC 2021; not an open candidate.
  source_urls_or_ids:
    - https://pages.mtu.edu/~yakov/research.html
    - DOI 10.1145/3406325.3451100
  search_terms:
    - "dynamic planar point location connected subdivisions solved"
    - "Optimal-Time Dynamic Planar Point Location in Connected Subdivisions"
  date_searched: 2026-05-17 UTC
  freshness_or_closure_signal: Author-maintained page says the connected case was completely resolved.
  could_revisit_if: Only as background for the disconnected/general subdivision residual.

- title_or_slug: non_orthogonal_square_or_triangular_range_reporting
  subrun: 2A_geometry
  reason_rejected: CCCG 2008 source states a key open reporting-query gap, but the source is old and the modern status is uncertain; freshness search did not establish viability.
  source_urls_or_ids:
    - https://cccg.ca/proceedings/2008/paper03full.pdf
  search_terms:
    - "Non-Orthogonal Square Range Searching open problem"
    - "Achieving O(lg n + k) time for reporting queries Chazelle Liu"
    - "double-wedge O(log n + k) range searching"
  date_searched: 2026-05-17 UTC
  freshness_or_closure_signal: No clean 2024-2026 assigned-pool update found; the trail may be subsumed by modern semialgebraic/simplex range searching.
  could_revisit_if: A modern survey or primary paper restates the exact reporting gap.

- title_or_slug: klee_measure_3d_polylog
  subrun: 2A_geometry
  reason_rejected: Jeff Erickson page is explicitly stale and warns not to cite it as current open status; problem is also more broad geometry-algorithmic than data-structure-theory scouting for this subrun.
  source_urls_or_ids:
    - https://jeffe.cs.illinois.edu/open/
    - https://jeffe.cs.illinois.edu/open/klee.html
  search_terms:
    - "Jeff Erickson Klee's Measure Problem open problems computational geometry"
    - "Klee measure problem 3D O(n polylog n) open"
  date_searched: 2026-05-17 UTC
  freshness_or_closure_signal: Erickson page itself says it has not been significantly updated since 2001 and many listed problems may be solved.
  could_revisit_if: A modern SoCG/JoCG survey restates a narrow Klee-measure data-structure subproblem.
```

## Notes For Synthesis

- Best new theorem-style candidate from this subrun: `higher_dim_rectangle_stabbing_word_ram_linear_space`, because its open-problem status is explicit and narrow.
- Best evaluator-hybrid candidate from this subrun: `dynamic_planar_nearest_neighbor_logarithmic_full`, because finite update/query traces have exact brute-force oracles, though asymptotic proof remains difficult.
- Most under-attended plausible residual: `dynamic_disconnected_planar_point_location`, but it needs a careful modern citation sweep before promotion because the open status is inferred.
- Existing geometry lead preserved, not superseded: `connected_circle_segment_queries`.
- Existing kinetic lead should be split before promotion; the current `kinetic_high_dim_extent` scope is too broad.
