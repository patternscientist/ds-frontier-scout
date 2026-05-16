# Comparing a Clean-Room STT Note to the Public Frontier (Sadeh–Kaplan–Zwick, Golinsky, Berendsohn–Kozma)

## A. Executive summary

GPT's clean-room note sits in a hybrid position. Roughly two-thirds of its scaffolding — the recursive STT model, the depth polytope P(U), the LP relaxation built around ancestry/LCA variables, the 2-approximation route, and even the explicit recognition that the lower envelope D(U) = P(U) + ℝ_{≥0}^V is what matters for nonneg-weight minimization — is a **clean rediscovery** of material already in Golinsky (2023) and Sadeh–Kaplan–Zwick ("SKZ", arXiv:2501.17563, v2 Aug 2025). However, GPT's specific LP — what it calls the *hereditary first-hit relaxation* — is **strictly stronger than Golinsky's LP** because it uses root variables on every connected subset, not only on path-sets, and it enforces inclusion-poset monotonicity rather than just the loosely-LCA path inequality. This means SKZ's known counterexamples to Golinsky's extended-formulation conjecture do **not** automatically refute GPT's "Q(U) ⊆ D(U)" conjecture; they only show that the *weaker* path-LP fails. The Möbius / branching-flow / complete-monotonicity framework GPT introduces, together with the explicit mixed-second-difference inequalities on paths, is **not present in any public STT paper I could locate**, and is the most plausibly novel material in the note. The P_3 result is essentially trivial (n ≤ 4 is integer in Golinsky's LP, hence in GPT's tighter LP). The good-root failure example is interesting but addresses a proof strategy, not the conjecture itself.

In one sentence: GPT independently arrived at the question SKZ leave open in §5.3 and §6 — whether path-monotonicity-style strengthenings of Golinsky's LP achieve objective exactness on subclasses like almost-stars — and proposes a specific, more aggressive strengthening (full inclusion-poset heredity, with a complete-monotonicity tower underneath) that the public literature has not explicitly written down.

## B. Mapping table: GPT's terms ↔ public STT literature

| GPT's term | Closest public-literature counterpart | Source |
|---|---|---|
| Underlying tree U | Underlying topology U | SKZ Definition 1.1 |
| Recursive search tree on a tree (RSTT) | STT (search tree on tree) | Bose et al. 2019; Berendsohn–Kozma SODA 2022; SKZ Def. 1.1 |
| Depth vector d_T | (D_v + 1) vector; SKZ uses D, with depth = D + 1 | SKZ Remark 1.5 |
| P(U) = convex hull of depth vectors | "STT-induced polytope" P in D-space | SKZ §2.2 |
| D(U) = P(U) + ℝ_{≥0}^V | P′ = "Minkowski sum of P with the positive orthant", "lower envelope" | SKZ §2.2, especially Figure 4 caption: "the facets of the lower-envelope of P" |
| Ancestry variable x_{ij} (i ancestor of j) | X_{ij} | Golinsky (via SKZ §1.1) |
| LCA variable z_{k,ij} | Z_{kij}, defined only for k ∈ (i ↭ j) (interior of path) | Golinsky / SKZ Def. 1.2 |
| First-hit variable z_{A,r} (r is earliest among connected A) | **Path-restricted version only** appears in Golinsky: Z_{kij} = "k is LCA of i,j" = "k earliest along path [i↭j]". No general-connected-subset version is in any public STT paper I located. | — |
| Branching-flow x_{S,r} (S connected, r ∈ S chosen root of subproblem S) | **Not in public STT literature** in this form. The closest cousin is "tubings" (Carr–Devadoss; cited in Berendsohn–Kozma) and graph associahedra, which are combinatorial rather than LP objects. | — |
| Hereditary first-hit relaxation Q(U) | Discussed implicitly under "path-monotonicity constraints" | SKZ §5.3 ("Are Path-monotonicity Constraints Helpful?") |
| Objective exactness "Q(U) ⊆ D(U)" (LP value ≥ best STT for w ≥ 0) | Conjecture 1 of Golinsky = "Conjecture 3.1 of [9]" in SKZ: for every nonneg w, ∃ STT inducing an LP optimum. SKZ disprove this for the long star U(7,3). | SKZ §1.2, §2.1 |
| Extended formulation conjecture (P(U) = projection of LP polytope) | Same Conjecture 1; SKZ point out it is logically stronger (every LP vertex is STT-induced). They disprove it via the normals method. | SKZ §1.2, §2.2 |
| Mixed-second-difference / complete-monotonicity inequalities on paths | **Not in any STT paper I located.** They are a Möbius/incidence-algebra construct standard in probability (de Finetti, Hausdorff moment problem) but not previously coupled to STT LPs. | — |
| "Good-root" induction | Closest analogs: centroid-tree analysis in Berendsohn–Golinsky–Kaplan–Kozma ICALP 2023 (2-approximation via centroid); Golinsky's "root rounding" in SKZ Def. 1.6 | BGKK 2023; SKZ Def. 1.6 |
| Bellman recurrence F_w(S) = min_r [W(S) − w_r + Σ_C F_w(C)] | Standard generalization of Knuth's 1971 BST DP. Stated informally in Bose–Cardinal–Iacono–Koumoutsos–Langerman: "dynamic programming also does not have an obvious polynomial-time solution as the number of connected subtrees of a tree is exponential." Berendsohn's PhD (FU Berlin 2024), Ch. 5, pursues *k-cut* search-tree subgraphs as a tractable subfamily. | Bose et al. 2019 §1.1; Berendsohn PhD 2024 Ch. 5–6 |

## C. Per-claim assessment of GPT's note

| # | Claim / construct | Status | Evidence |
|---|---|---|---|
| C1 | STT framework, recursive definition | **Known** | Bose et al. 2019; Berendsohn–Kozma SODA 2022; SKZ §1 |
| C2 | P(U) = conv hull of depth vectors | **Known** | SKZ §2.2 calls this P |
| C3 | D(U) = P(U) + ℝ_{≥0}^V; only D(U) matters for nonneg w | **Known**, explicit | SKZ §2.2: "P′ is the Minkowski sum of P with the positive orthant... by trading the finite P with the infinite P′ we removed every facet that was dominated by a vertex." Lower-envelope terminology is theirs. |
| C4 | LP with ancestry X_{ij}, LCA Z_{kij}, depth D_i = Σ X_{ji}; relaxed inequalities | **Known** — this *is* Golinsky's LP | SKZ Def. 1.2 (attributed to Golinsky [9]) |
| C5 | Branching-flow LP on x_{S,r} for connected S, exact extended formulation in (x,d) | **Implicit but not written down publicly.** It is the standard "subproblem indicator" extended formulation for a recursive combinatorial structure (analogous to Knuth's BST DP unrolled into an LP). I found no STT paper that writes it explicitly. It is exact essentially by definition of the recursion. Novelty here is mainly the explicit articulation. | No counter-source located |
| C6 | z_{A,r} = Σ_{S ⊇ A} x_{S,r} is a zeta transform; complete monotonicity recovers x ≥ 0 | **Plausibly novel for STT.** No public STT paper invokes Möbius inversion or completely-monotone sequences. Underlying mathematics (zeta/Möbius over inclusion posets) is classical. | — |
| C7 | Hereditary first-hit relaxation: z_{A,r} ≥ 0, Σ_r z_{A,r} = 1 on connected A, z_{A,r} ≤ z_{B,r} for B ⊆ A; with depth projection d_v = Σ_{u≠v} z_{P_U(u,v), u} | **Strictly stronger LP than Golinsky's** in two distinct ways: (i) it has variables for all connected subsets, not only path-sets [i↭j]; (ii) it enforces full inclusion-poset monotonicity, not just the path-restricted Z_{kij} ≤ X_{ki}, X_{kj} of Golinsky. SKZ §5.3 ("Are Path-monotonicity Constraints Helpful?") explicitly considers strengthening with monotonicity-like constraints but, by their section title, in a more limited path-restricted form. | SKZ §5.3 (title and placement) |
| C8 | P(U) ⊆ Q(U) | **Trivially correct**: every STT induces a 0/1 z-vector satisfying heredity. | — |
| C9 | Q(P_3) ⊆ D(P_3) (objective-exactness on n=3) | **Trivially known** under any of Golinsky's, SKZ's, or GPT's relaxations: SKZ Section 3.2 exhibits all 9 vertices of Golinsky's LP for the n=3 path and verifies they are all integer in D-space (Table 4). Property 2 in SKZ then implies LP optimum = STT optimum for any nonneg w. Since GPT's LP is tighter than Golinsky's, the conclusion is automatic. | SKZ §3.2, Table 4 |
| C10 | Good-root induction strategy fails for P_3 with w = (1,4,4) | **Internal to GPT's proof program**, not a public-literature claim. Notable that BGKK's centroid-tree analysis succeeds with a 2-approximation by a similar amortized-charge style, but does not (and is not claimed to) give exact optimality. The non-existence of a "single root with locally-paid separator charge ≥ W − w_r" is consistent with the broader observation that picking centroids — even weighted — gives 2-approx at best (BGKK 2023, lower bound is *tight* at 2). | BGKK ICALP 2023 |
| C11 | Hereditary = "first-order" monotonicity; exact extended formulation requires *complete* monotonicity (all Möbius-inverted x-masses ≥ 0); intermediate relaxations sit between | **Plausibly novel framing for STT.** Standard for Hausdorff moment / de Finetti exchangeable sequences. The hierarchy "branching-flow ⇔ completely monotone ⇒ hereditary" is logically straightforward once written. | No counter-source located |
| C12 | Mixed-second-difference inequalities z_{[i,j],r} − z_{[i−1,j],r} − z_{[i,j+1],r} + z_{[i−1,j+1],r} ≥ 0 on paths | **Plausibly novel for STT.** These are precisely the inclusion-exclusion / Möbius-on-the-interval-lattice inequalities. SKZ §5.3 hints at "path-monotonicity" but the title is a question, suggesting they did not pursue this beyond posing it. | SKZ §5.3 title only |

## D. The crucial Q(U) ⊆ D(U) question vs. SKZ's open questions

**Definitionally, GPT's main conjecture is:**

> For every tree U and every nonneg w, min_{z hereditary} Σ_v w_v d_v(z) = min_T Σ_v w_v d_T(v).

**SKZ's analogous open question (in their framing):**

> Is Golinsky's LP "objective-exact" for nonneg w on certain restricted topology classes (almost stars / edge-diameter ≤ 3)? Equivalently, does the lower envelope of Golinsky's LP polytope (projected to D-space) coincide with the lower envelope D(U) of the STT polytope on those classes?

These two questions are **logically distinct**. The relationship is:

- GPT's LP ⊆ Golinsky's LP (set inclusion in the path-coordinate projection): GPT's hereditary first-hit LP has *more* variables and *more* constraints, and the projection to (X, Z, D) is contained in Golinsky's polytope. Hence GPT-LP-value ≥ Golinsky-LP-value for every nonneg w.
- Therefore: **(SKZ's Conjecture 1 true) ⇒ (GPT's conjecture true)**, but the converse is not automatic.
- SKZ have *disproved* their (and Golinsky's) Conjecture 1: on the long star U(7,3) with w = (3,2,0,2,3,3,10), Golinsky's LP optimum is 29.5 < 30 = best STT, an integrality gap of 60/59.
- **This counterexample does NOT automatically transfer to GPT's tighter LP.** The point P in Figure 3 of SKZ has Z-values 1/2 across many path-LCA configurations. Whether it lifts to a feasible point of GPT's hereditary LP (which requires consistent z_{A,r} over *all* connected A, with monotonicity in the inclusion order) is a finite computational check the user has not yet made and which is not addressed in any public STT paper.

So GPT's conjecture is **strictly weaker than (i.e., logically implied by) Golinsky's original Conjecture 1 and the SKZ extended-formulation question**, but **strictly stronger than asking only for objective-exactness via *some* tightening of Golinsky's LP**. It is, however, **stronger than the open question SKZ leave for almost stars**: SKZ ask whether Golinsky's LP (unchanged) is objective-exact on edge-diameter ≤ 3 trees; GPT asks whether a *strengthened* LP is objective-exact for *all* trees. These are genuinely different questions, not the same question in different notation.

A side remark on terminology: SKZ do not seem to coin the phrase "objective-exact" or "lower envelope equality" as such. They use "lower envelope of P" geometrically (for the boundary of P′ = P + ℝ_{≥0}^V) and treat the failure of Conjecture 1 on U(7,3) as a failure of the LP to be an extended formulation. But the *demonstration* of failure (an explicit nonneg w with LP < STT) is, in GPT's language, a failure of objective-exactness for Golinsky's LP on U(7,3). The two collapse here because their normals method maximizes in nonneg directions only.

## E. Known counterexamples: extended formulation vs. objective-exactness

| Tree | n | What is known publicly | Does it kill Golinsky's LP as extended formulation? | Does it kill Golinsky's LP as objective-exact (nonneg w)? | Does it bear on GPT's tighter Q(U)? |
|---|---|---|---|---|---|
| P_3, P_4 (paths n ≤ 4) | ≤ 4 | All LP vertices integer in (X,Z,D) and projection (SKZ §3.2; Table 1 confirms U(3,0),(4,0),(4,1) have no non-STT D-vertices and XZD-denominator {1}) | No | No | Q(U) ⊆ D(U) holds trivially (LP is already exact) |
| P_5 (path, n=5) | 5 | Frac Vs = "." (no D-space fractional vertex); but XZD-space denominator ∈ {1,2,3} — i.e., LP polytope has non-integer vertices, yet projection to D-space is still the integer hull. | **No.** Although LP polytope has non-integer vertices, their D-projection is dominated by integer STT-induced points; SKZ explicitly observe partially-integer vertices project to non-vertices in D-space. | **No.** Optimum in any nonneg direction is achieved at an STT. | Trivially: GPT's tighter LP can only be tighter; nonneg-w optimum equals STT optimum. |
| P_6 | 6 | Partially integer vertex P_1 in SKZ Eq. (3): X_{6,3} = (..., 4, 4, 4, 2, 2, 6)/2 in D, but D-projection is dominated by STT depth vector (2,1,2,0,1,2). | Yes (LP has non-STT vertices in XZD) | **No** (no nonneg w realizes strict gap on P_6 in their table) | GPT's tighter LP plausibly still objective-exact on P_6 |
| Long star U(7,3): edges (0,1),(1,2),(2,3),(3,4),(2,5),(5,6) with one central node of degree 3 (SKZ call it "long star, three legs"; node "3" is the center) | 7 | 9 fractional D-space vertices, 39 false facets. With w=(3,2,0,2,3,3,10): LP = 29.5, best STT = 30. Integrality gap 60/59. | **Yes** | **Yes** — disproves objective-exactness of Golinsky's LP | **Unknown.** The specific point P (Figure 3, Eq. (1)) might or might not lift to GPT's hereditary LP. This is the key test GPT's note has not run. |
| 8-node topologies U(8,4), (8,5), (8,6), (8,11), (8,12), (8,13) | 8 | Various integrality gaps up to 95/93 ≈ 1.0215 | Yes | Yes | Unknown |

**Summary**: Every SKZ counterexample is a counterexample to *both* extended-formulation and objective-exactness for Golinsky's LP. None of them has been tested against GPT's stronger LP.

## F. Suggested next computational tests with explicit topologies and weights

The single most discriminating test is to take SKZ's explicit fractional vertex on U(7,3) and check whether it lifts to a feasible point of GPT's hereditary LP. Concretely:

1. **Lift test on U(7,3) with w = (3, 2, 0, 2, 3, 3, 10)** (SKZ Theorem 2.2). The candidate D-vector is (2, 2, 4.5, 2, 2, 1.5, 0.5), and the X, Z values are in SKZ Figure 3. Compute the corresponding "implied" z_{A,r} for *every* connected subset A ⊆ U(7,3) and check whether the inclusion-poset heredity z_{A,r} ≤ z_{B,r} for B ⊆ A holds. There are 2^{|V|} ≤ 128 subsets to check; many are disconnected. If heredity is satisfied, then GPT's Q(U) is also not contained in D(U) on the long star, and the conjecture is **already disproved** by an example in the public literature that the user has not yet realized applies. If heredity is violated, then GPT's conjecture survives this test and the long-star case becomes genuinely novel territory.

2. **Direct LP solve of GPT's hereditary LP on P_4, P_5, P_6, P_7 in exact rational arithmetic.** Vertices and weights with bounded denominators are tractable for n ≤ 7. For P_4 the LP is small enough to be solved by hand. For P_5 and P_6, SKZ's polytope-enumeration code (Sage; Appendix B of arXiv:2501.17563) can be adapted by adding constraints over all connected subsets. P_5 is the smallest topology with a non-integer XZD-vertex in Golinsky's LP, so it is the right test for whether GPT's strengthened LP recovers integrality at the XZD level.

3. **Star K_{1,n−1}** has Golinsky's LP integer (SKZ Theorem 3.9), so GPT's strictly tighter LP is also integer. No new information.

4. **The smallest non-star branching tree** with central degree 3 and three leaves at distances 1, 1, 2 (the "Y with one extended arm", n = 5, equivalent to U(5,2) "spider") — currently in SKZ Table 1 as integer in XZD (denominator {1}). Test confirms Golinsky-LP exactness, hence GPT-LP exactness. Easy positive check.

5. **U(8,4), (8,11), (8,12), (8,13)** with the SKZ-listed maximum-gap nonneg directions (Table 2 of SKZ) are the next-most-discriminating tests after the long star. Same lift procedure as test 1.

6. **The "almost stars" / edge-diameter ≤ 3 subclass.** This is explicitly listed in SKZ as an open subclass for Golinsky's LP. If the user can solve GPT's hereditary LP on all such trees up to n = 8 (a small finite list, easily enumerable) and find it always integer in D-space, that would be a meaningful new contribution. The catch: SKZ's *polytope enumeration* already checks all topologies n ≤ 8 in Golinsky's LP, so if Golinsky's LP is already objective-exact on every almost star up to n = 8 (Table 1 should confirm this — every non-path, edge-diameter ≤ 3 tree with n ≤ 8 has Frac Vs = "." in Table 1), then GPT's tighter LP gives nothing new in that class. The user should read SKZ Table 1 carefully to confirm.

7. **A dual / Bellman test.** Knuth's quadratic DP on paths and its generalization F_w(S) = min_r [W(S) − w_r + Σ_C F_w(C)] is an exponential DP on connected subsets. For all topologies with n ≤ 8 it is fully tractable. Compute F_w on the SKZ counterexample weight vectors and confirm the values match SKZ's reported "STT Best Value". No new mathematics; it is a sanity check.

## G. Practical advice for the user

1. **Read SKZ §5.3 carefully.** Section title "Are Path-monotonicity Constraints Helpful?" almost certainly contains the closest public discussion of GPT's heredity idea. If the user's hereditary LP is what SKZ already considered and found insufficient, that needs to be confirmed before claiming novelty. I was unable to fetch §5.3's full body due to rate limits, but the section is short.

2. **Read SKZ §6 carefully.** SKZ "enumerate several research directions". The user's existing summary already identifies the right list. Confirming whether SKZ ask specifically about extending Golinsky's LP with full-connected-subset monotonicity is the only step that would change the assessment.

3. **Try to obtain Golinsky's 2023 Tel Aviv master's thesis.** SKZ's bibliography reference [9] is the only public pointer. The thesis is not on arXiv. Direct request to Sadeh, Kaplan, or Golinsky is the realistic path. The thesis may or may not have considered branching-flow extended formulations — the SKZ description suggests it stopped at the (X, Z, D) LP plus rounding, but a definitive answer requires the thesis text.

4. **Contact Yaniv Sadeh.** SKZ's section §6 (open questions) and §5.3 (path-monotonicity) are precisely the topics GPT independently arrived at. The author is reachable (yanivsadeh@tau.ac.il is listed on the arXiv version). A short email asking "have you considered an LP with z_{A,r} variables for every connected A, with full inclusion-poset monotonicity?" is the cheapest possible way to determine whether GPT's hereditary LP is novel.

5. **Read Berendsohn's PhD thesis (FU Berlin 2024, Refubium handle 45994/phd.pdf), Chapters 5 and 6.** Chapter 5 covers "Dynamic programming on k-cut search trees" — a polynomial-time PTAS and exact DP on a restricted subclass — and Chapter 6 gives an FPTAS for trees. These are the closest public-literature analogs to GPT's Bellman recurrence and should be cited / compared before claiming the recurrence is novel.

## H. Sources

- Sadeh, Kaplan, Zwick. *Search Trees on Trees via LP*, arXiv:2501.17563 v2 (1 Aug 2025). https://arxiv.org/abs/2501.17563
- Berendsohn, Golinsky, Kaplan, Kozma. *Fast Approximation of Search Trees on Trees with Centroid Trees*, ICALP 2023, arXiv:2209.08024. https://arxiv.org/abs/2209.08024
- Berendsohn, Kozma. *Splay Trees on Trees*, SODA 2022, arXiv:2010.00931. https://arxiv.org/abs/2010.00931
- Bose, Cardinal, Iacono, Koumoutsos, Langerman. *Competitive Online Search Trees on Trees*, arXiv:1908.00848 (published ACM TALG 2023). https://arxiv.org/abs/1908.00848
- Berendsohn, B. A. *Search Trees on Graphs* (PhD dissertation, FU Berlin, 2024). https://refubium.fu-berlin.de/handle/fub188/45994
- Golinsky, I. *A Study on Search Trees on Trees* (Tel Aviv University M.Sc. thesis, 2023). Not publicly available; cited as [9] in Sadeh–Kaplan–Zwick.
- Voderholzer, A. *Algorithms for Optimal Search Trees on Trees* (FU Berlin BSc thesis, 2023). https://www.mi.fu-berlin.de/inf/groups/ag-ti/theses/download/Voderholzer23.pdf

### Methodological caveats

- I was not able to access Golinsky's master's thesis directly; everything stated about "Golinsky's LP" is from SKZ's exposition (which is self-contained for the LP itself but does not reveal what alternative formulations the thesis considered and rejected).
- I was rate-limited before being able to fetch the full text of SKZ §5.3 and §6 from arxiv.org/html. Section titles, abstracts, and §1–§3 text were retrieved in full, and §5.3 title alone ("Are Path-monotonicity Constraints Helpful?") strongly suggests SKZ explicitly raise (and possibly answer negatively in a limited form) a version of GPT's hereditary strengthening. The user should read §5.3 before making any novelty claim.
- I found no follow-up paper to SKZ in the 16 months between its January 2025 posting and May 2026. The 1 Aug 2025 v2 revision is minor (562 KB → 563 KB). No workshop / arXiv / conference follow-up by other authors has appeared so far as my searches detected.
- Claims in section C about novelty of the Möbius/complete-monotonicity framing for STT are negative claims based on absence in standard searches; they could be falsified by a paper I missed. They are most reliably falsified or confirmed by direct email to Sadeh.