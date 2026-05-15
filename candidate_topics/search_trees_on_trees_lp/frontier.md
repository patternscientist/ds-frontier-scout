# Frontier

Verified anchors:

- Bose, Cardinal, Iacono, Koumoutsos, and Langerman (SODA 2020) define and study adaptive search trees on trees, equivalent to BSTs when the topology is a path, and give an online `O(log log n)`-competitive structure.
- Berendsohn and Kozma (SODA 2022) give, for every integer `t >= 1`, a `(1 + 1/t)`-approximation for optimal static STT in time `O(n^{2t+1})`. They also generalize Splay to STTs and prove a static-optimality theorem for that generalized Splay.
- Berendsohn, Golinsky, Kaplan, and Kozma (ICALP 2023) study centroid trees for STTs. They state that optimal STTs are not known to be computable in polynomial time, give efficient centroid-tree construction, and prove centroid trees are 2-approximations with tight worst-case ratio.
- Sadeh, Kaplan, and Zwick (arXiv 2501.17563, revised 2025) study Golinsky's LP relaxation for static STT. Their presentation defines ancestry variables `X_ij`, LCA variables `Z^k_ij`, depth variables `D_i`, and root rounding.
- Golinsky's LP gives a constructive 2-approximation via root rounding. Golinsky conjectured the LP is an extended formulation of the convex hull of STT depth vectors, which would imply optimality.
- Sadeh-Kaplan-Zwick disprove the LP optimality conjecture and the root-rounding optimality conjecture. Their explicit first counterexample is a 7-node "long star" with three legs and frequency vector proportional to `[3,2,0,2,3,3,10]`.
- Their normals method enumerates vertices / false facets for all tree topologies up to 8 nodes in the tested regime. They report non-STT depth-space vertices for seven small topologies.
- Their best listed lower bound on the LP integrality gap is `95/93 ~= 1.0215`; the general upper bound from root rounding remains 2.
- Their listed lower bound for the approximation ratio of root rounding reaches `263/190 ~= 1.384` in the searched examples.
- Stars are analytically proved integral for the LP polytope, yielding a polynomial-time algorithm for optimal static STT on star topologies.
- Open subclasses identified by Sadeh-Kaplan-Zwick include paths and edge-diameter-3 topologies ("almost stars"), where they do not know whether the LP itself is integral.
- The LP is known non-integer for edge-diameter 4 and above by the path on 5 nodes, and the depth-space projection is non-integer for edge-diameter 5 and above by the long-star example.
- The 2025 paper's appendix says code is included in the arXiv source archive as `STTLP-sage-python3-source.zip`; the core polytope/LP functionality uses Sage, while some topology/STT enumeration can run in Python.

Inferred frontier:

- The best project shape is not to invent a brand-new STT theory immediately, but to reproduce the LP counterexample pipeline and then attack one clean subcase: paths, almost-stars, or depth-space projection integrality.
- The computational frontier is unusually concrete: small topologies have explicit names, edge lists, frequency vectors, candidate fractional vertices, and reproducibility scripts.

TODO: verify source:

- Locate and cite Golinsky's original thesis/manuscript where the LP relaxation and conjecture were introduced; current notes rely on Sadeh-Kaplan-Zwick's account.
- Extract the arXiv source zip and verify whether the scripts reproduce Tables 1, 2, 3, 6, and 7 unchanged.
- Check whether Berendsohn's 2024 thesis contains additional static-STT algorithms or subclass results relevant to paths/almost-stars.
