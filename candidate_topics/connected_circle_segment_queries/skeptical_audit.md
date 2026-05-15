# Skeptical Audit

Batch 003 adversarial audit date: 2026-05-15.

Verdict: keep as a narrow recent geometry lead, but downgrade evaluator enthusiasm and separate theory from implementation wishes.

- Open-problem claim: explicit but mixed. The future-work section explicitly asks for lower bounds on data-size/query-time tradeoffs in the connected-graph setting. It also suggests bottom-up construction and fractional-cascading improvements, but those suggestions are partly implementation/construction-efficiency ideas unless formalized as asymptotic theorems.
- Formula verification: the Dagstuhl/Pure abstract and PDF snippets give the main result as construction time and space `O((n+C) log^3 n)` and query time `O(k log^3 n)`, where `C` is the number of crossings and `k` is output size. Theorem 7 gives a circle-graph decision oracle with `O(log^2 n)` query time and `O((n+C) log^2 n)` construction/space. HTML formulas are indeed mangled, so do not cite the HTML alone for exact asymptotics.
- Model distinctions: connected graph as graph-theoretic connectivity versus merely connected segment arrangement; planar case `C=0` versus crossing-rich non-planar inputs; circle boundary reporting versus disk reporting; static reporting versus dynamic geometry; lower-bound model versus engineering/CGAL baseline performance.
- Newer-work check: source is ISAAC 2025 with publication date 2025-11-27; no later primary source found in quick search. Because it is very recent, this is fragile.
- Saturation risk: medium. The exact connected circle-segment query is niche, but geometric range-reporting lower bounds and partition-tree improvements are mature and model-sensitive.
- Smallest meaningful subproblem: planar connected geometric graphs (`C=0`) with near-linear space, circle-boundary reporting, and a cell-probe/pointer-machine lower bound separating connected segment graphs from arbitrary segment sets. A weaker finite task is to construct connected planar families where the edge-partition-tree oracle visits `Omega(k log n)` nodes.
- Best use after audit: theorem_project/OpenEvolve hybrid, but not top-tier. OpenEvolve can test partition heuristics and adversarial instances; it cannot certify the lower-bound tradeoff.
- Blind prompt risk: acceptable if it emphasizes a lower-bound or asymptotic tradeoff. The restricted "edge-partition-tree oracle must visit many nodes" is a critique of one technique, not a lower bound against all data structures.
- Evaluator caveat: finite AABB/oracle false-positive experiments can make one implementation look bad without saying anything about optimal connected-graph data structures.
- Falsifier: a follow-up giving a near-linear-space `O(log^O(1) n + k)` or better connected-graph structure, or a known lower bound from curved-object intersection reporting that already applies to connected graphs.

Primary sources to recheck before promotion:

- Afshani, Bosch, and Storandt, ISAAC 2025 PDF/source for theorem statements and future-work wording.
- Gupta, Janardan, and Smid 1994 plus later curved-object intersection-searching lower bounds, to see whether the "connected" lower-bound gap is genuinely new.
