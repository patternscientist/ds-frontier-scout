# Skeptical Audit

Batch 003 adversarial audit date: 2026-05-15.

Verdict: keep as an explicit open problem, but downgrade evaluator fit and treat as active graph-algorithmic context.

- Open-problem claim: explicit. Kadria and Roditty arXiv v3 / DISC 2025 state the directed weighted roundtrip-routing gap and ask for the best stretch with `~O(n^{1/k})` local storage.
- Narrowing required: distinguish compact routing schemes from distance oracles, labels alone, spanners, and emulators. The routing scheme has local routing tables, destination labels, and packet headers; a distance-estimation construction is not automatically a routing scheme.
- Model distinctions: weighted versus unweighted directed graphs; strongly connected directed graphs; topology-dependent labels/names versus name-independent variants; local storage per vertex versus average storage; stretch of an actual routed roundtrip path versus approximate roundtrip distance.
- Newer-work check: arXiv v3 is dated 2025-08-31 and still only claims the directed `k=3` improvement to stretch 7. Quick search found no later primary source closing general directed `k`.
- Saturation risk: high. Compact routing, roundtrip spanners, directed girth, and distance-oracle tradeoffs are active and technically mature. The candidate is not under-attended in the same sense as an old niche data-structure residual.
- Smallest meaningful subproblem: the `k=4` directed weighted case with `~O(n^{1/4})` local storage, asking whether one can beat the inherited `4k+epsilon`-style stretch by a construction that actually routes, not just estimates distance.
- Best use after audit: theorem_project or background_context. It is too construction-heavy for OpenEvolve except as a finite counterexample generator for candidate local routing rules.
- Blind prompt risk: the phrase "prove a lower bound showing that stretch close to `2k-1` is impossible" can accidentally overpromise, because known lower bounds may be conditional or for adjacent oracle/spanner models. Mark lower-bound targets as model-specific.
- Evaluator caveat: finite graph search can falsify a proposed local rule, but it will not certify asymptotic compact-routing lower bounds and may overfit to small directed-girth gadgets.
- Falsifier: a follow-up giving a general directed compact roundtrip routing scheme with substantially improved stretch for all `k`, or showing that the proper lower-bound model is already settled conditionally.

Primary sources to recheck before promotion:

- Kadria and Roditty arXiv:2503.13753 v3 and DISC 2025 proceedings version.
- Roditty, Thorup, and Zwick TALG 2008 for the exact older `4k+epsilon` routing model.
- Directed girth/roundtrip-spanner papers used for lower-bound context.
