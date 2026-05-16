# Frontier Note v4.4: Connected First-Hit Hierarchy for Static Search Trees on Trees

**Date:** 2026-05-15/16  
**Project:** AI and Data Structures / STT LP frontier  
**Status:** Golinsky-thesis-aware, public-source-patched, and internally polished frontier note; suitable as current fresh-context handoff and near-paper-draft source, pending author-courtesy/public-overlap check and final independent audit  
**Conventions:** root-depth-0 weighted depth unless explicitly stated otherwise

---

## 0. Step-back assessment

This note patches Frontier Note v4.3 after targeted public-source comparison, direct inspection of Ishay Golinsky's Master's thesis, and a final wording pass focused on novelty boundaries and next-step discipline. The uploaded PDF is indeed that thesis: the title page identifies the exact title, author, institution, advisor, and date.

The main new v4.3 change is not a new theorem. It is a novelty-risk correction: Golinsky's original LP, the SKZ follow-up, and the public DP/STT literature overlap with several path-variable and dynamic-programming aspects of this project. The connected first-hit hierarchy remains viable, but it must be framed as a connected-subset/Möbius coordinate framework and certificate/theorem package, not as the discovery of the public gap, the public LP, or the standard connected-subproblem recurrence.

The current status is sharper than v4:

- **H1 is dead as a depth relaxation.** The SKZ `U(7,3)` long-star depth vector has value `59/2 < 30` and admits the earlier H1 connected first-hit lift.
- **H2 exactly closes the SKZ `U(7,3)` depth-vector gap.** The repository contains an exact primal/dual certificate proving H2 optimum `30` for weights `[3,2,0,2,3,3,10]`, and the public SKZ fractional depth vector has no H2 lift.
- **H2 is exact on paths**, assuming the path proof below is included with the interval/product-of-chains Möbius details.
- **H2 fails in full first-hit `z`-space on the 4-leaf star.** The audited star system satisfies simplex, H1, and H2 exactly, but its complete Möbius inverse has negative masses.
- **The audited 4-leaf star obstruction is not a depth-projection obstruction.** Its depth vector is in the STT dominant, dominated by the center-root STT depth vector `(0,1,1,1,1)`.
- **Degree-at-least-4 embedding is not yet a theorem in this note.** The merged audit gives finite exact support for subdivided-star host trees and preserves the negative center mass, but a general proof requires careful cross-boundary H2 analysis. It is therefore recorded as a supported/provisional embedding claim.

The strategic conclusion is also sharper:

> H2 is useful but not generally exact. The real object is the **connected first-hit Möbius hierarchy**: complete Möbius consistency is exact but exponential; H2 is a low-order truncation that is exact on paths and strong enough to close the canonical SKZ `U(7,3)` depth-vector gap, but too weak for full `z`-space exactness on branching stars.

This appears to be in paper-worthy territory as a short theorem/certificate note after an author-courtesy/public-overlap check and one final independent audit of the proof package and related-work language. It should not be oversold as a compact formulation, a polynomial-time exact algorithm, or a solution of optimal STT computation.

---

## 1. Public context and provenance

A **static search tree on a tree** (STT) generalizes binary search trees from paths to arbitrary tree topologies. In a connected subproblem, the search tree chooses a root vertex, removes it, and recurses on the connected components left behind.

The public optimization problem is: given a tree topology and nonnegative search frequencies/weights, construct an STT minimizing weighted search cost.

Relevant public context:

- Sadeh--Kaplan--Zwick (SKZ), *Search Trees on Trees via LP*, study Golinsky's LP relaxation for optimal static STTs. They state that Golinsky conjectured the LP was an extended formulation of the convex hull of STT depth vectors, then disprove the conjecture by finding LP points that beat every STT. They enumerate small topologies and list directions toward stronger formulations, dual use, and DP/LP connections.  
  URL: https://arxiv.org/abs/2501.17563

- Ishay Golinsky, *A study on search trees on trees* (Master's thesis, Tel Aviv University, April 2023), is now directly inspected. The thesis defines STTs, emphasizes their alternate names (tubings, vertex rankings, ordered colorings, elimination trees), gives the LP that SKZ later studies, proves the integer/2-approximation partial results, and records empirical evidence plus failed proof attempts. In the thesis LP, the primary variables are ordered ancestry variables `X_{u,v}`; Section 3.4 linearizes the path-min constraints with `Z^w_{u,v}` variables and only upper bounds `Z <= X`, not arbitrary connected-subset first-hit variables. No occurrence of first-hit probabilities over arbitrary connected subsets, complete Möbius consistency, or extension rectangles was found in the inspected thesis text.  
  Local source: uploaded PDF `Ishay Golinsky 9933528218504146.pdf`.

- Berendsohn's thesis records that no polynomial-time algorithm is known for optimal static search trees on graphs, even when the underlying graph is a tree, and discusses exact exponential algorithms, approximation algorithms, and bounded-treewidth/general-graph hardness context.  
  URL: https://refubium.fu-berlin.de/handle/fub188/45994

- Berendsohn--Golinsky--Kaplan--Kozma's centroid-tree work gives fast construction and 2-approximation results for centroid trees, while noting that optimal STTs are not known to be polynomial-time computable.  
  URL: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2023.19

Internal provenance used in this note:

- Branch `stt-h2-dual-cert-v0`, commit `73f9ca4`, report `reports/stt_h2_dual_cert_v0.md`: exact H2 primal/dual certificate for SKZ `U(7,3)`.
- Main merge commit `9d135d0`, “Merge v4 star obstruction audit,” report `reports/stt_v4_star_audit_v0.md`: exact audit of the 4-leaf star obstruction and sampled degree-4 embeddings.
- Frontier Note v4: previous state of the connected first-hit hierarchy, patched here.
- Claude adversarial audit of Frontier Note v4.1: confirmed the core theorem package, requested precision patches for integrality, reverse-cover proof details, degree-4 embedding status, and public-overlap caveats.
- Direct v4.3 inspection of Golinsky's thesis: confirmed the original LP is path/ancestry-based and does not visibly contain connected-subset first-hit variables, complete Möbius masses, or extension rectangles; also confirmed several public-overlap zones around projection to connected subgraphs, depth-space focus, and DP/LP suggestions.

A standard polyhedral fact used below is the characterization of rational integral polytopes by integral optima for all linear objectives; for a textbook reference, see Schrijver, *Theory of Linear and Integer Programming*, Chapter/Section 22 on integral polyhedra.

This note uses public sources only for context and comparison. The theorem statements below are internal project results unless explicitly marked public or standard.

---

## 2. Basic definitions

Let `T=(V,E)` be a finite undirected tree. A nonempty subset `C subset V` is **connected** if the induced subgraph `T[C]` is connected. Let `Conn(T)` denote the family of nonempty connected vertex sets.

An **STT on T** is defined recursively:

1. If the current connected set is empty, stop.
2. If the current connected set is `C`, choose a root `r in C`.
3. Remove `r`; the remaining vertices split into the connected components of `T[C \ {r}]`.
4. Recurse independently on each component and attach the resulting recursive roots as children of `r` in the search tree.

The depth `d(v)` is the number of strict ancestors of `v` in the STT; the root has depth 0. The weighted depth objective is

```math
\sum_{v\in V}w_v d(v).
```

For a connected set `I` and a true STT `tau`, define the **first-hit vertex**

```math
\rho_\tau(I)=\text{the vertex of }I\text{ with minimum STT depth}.
```

This is well-defined and unique: along the recursive construction, the first subproblem root belonging to `I` is unique.

For a distribution over STTs, define first-hit probabilities

```math
z[I,r]=\Pr(\rho_\tau(I)=r),\qquad I\in Conn(T),\ r\in I.
```

---

## 3. H1, H2, and the finite-difference hierarchy

### H1: simplex plus heredity

For every connected `I`:

```math
z[I,r]\ge0,\qquad \sum_{r\in I}z[I,r]=1.
```

For connected `B subset A` and `r in B`:

```math
z[A,r]\le z[B,r].
```

### H2: extension rectangles

For connected `S,A,B,A union B`, with `S subset A`, `S subset B`, and `r in S`:

```math
z[S,r]-z[A,r]-z[B,r]+z[A\cup B,r]\ge0.
```

Since `A` and `B` both contain nonempty connected `S`, their union is connected in a tree; nevertheless, it is harmless and implementation-friendly to state connectedness explicitly.

### Hk: order-k union finite differences

For `t >= 1`, choose a connected base set `S`, a root `r in S`, and connected supersets `A_1,...,A_t` of `S` such that every union appearing below is connected. Define the `t`-fold finite difference

```math
\Delta_t(S;A_1,\ldots,A_t;r)
=
\sum_{B\subseteq[t]}(-1)^{|B|}
 z\!\left[\bigcup_{i\in B}A_i,r\right],
```

with the convention that the `B=emptyset` term is `z[S,r]`. Equivalently, one can write the differences over connected supersets of a base connected set by replacing each `A_i` with `S union A_i`. H1 is the order-1 part. H2 is the order-2 part.

The complete formulation below enforces all orders through nonnegative Möbius masses. Equivalently, this is finite differencing on the upper lattice of connected supersets of `S`, with `S` as the basepoint.

---

## 4. True STTs satisfy H1 and H2

### Theorem 4.1

Every distribution over STTs induces first-hit variables satisfying H1 and H2.

### Proof

It is enough to prove the statement for a deterministic STT and then take convex combinations.

For a deterministic STT, define

```math
z[I,r]=1_{\rho(I)=r}.
```

For each connected `I`, exactly one vertex is first-hit, so nonnegativity and simplex hold.

For heredity, let `B subset A` be connected and let `r in B`. If `rho(A)=r`, then no vertex of `A` occurs before `r` in the STT. Since `B subset A` and `r in B`, no vertex of `B` occurs before `r`, hence `rho(B)=r`. Therefore

```math
1_{\rho(A)=r}\le1_{\rho(B)=r},
```

which is H1.

For H2, for each connected set `C` and root `r in C`, define the event

```math
E_C^r=\{\rho(C)=r\}.
```

Let `S subset A`, `S subset B`, and `r in S`. If `r` is first in `A union B`, then it is first in both `A` and `B`, so

```math
E_{A\cup B}^r\subseteq E_A^r\cap E_B^r.
```

Conversely, if `r` is first in both `A` and `B`, then no vertex of `A` occurs before `r` and no vertex of `B` occurs before `r`; hence no vertex of `A union B` occurs before `r`. Since `r in A union B`,

```math
E_A^r\cap E_B^r\subseteq E_{A\cup B}^r.
```

Thus

```math
E_{A\cup B}^r=E_A^r\cap E_B^r.
```

Also `E_A^r subset E_S^r` and `E_B^r subset E_S^r` by H1/heredity of first-hit events. Therefore

```math
1_{E_S^r}-1_{E_A^r}-1_{E_B^r}+1_{E_{A\cup B}^r}
=1_{E_S^r\setminus(E_A^r\cup E_B^r)}\ge0.
```

Taking expectations gives H2. ∎

---

## 5. Projection to Golinsky/SKZ-style path variables

Let `P(u,v)` be the vertex set of the unique path between `u` and `v` in `T`. Define

```math
X_{u,v}=z[P(u,v),u]
```

for `u != v`. For an interior path vertex `k in P(u,v) \ {u,v}`, define

```math
Z^k_{u,v}=z[P(u,v),k].
```

Define root-depth-0 depth projection

```math
D_v=\sum_{u\ne v}X_{u,v}.
```

### Theorem 5.1: H1 gives the basic path/LCA constraints

For every `u != v`,

```math
X_{u,v}+X_{v,u}+\sum_{k\in P(u,v)\setminus\{u,v\}}Z^k_{u,v}=1.
```

For every interior `k in P(u,v)`,

```math
Z^k_{u,v}\le X_{k,u},\qquad Z^k_{u,v}\le X_{k,v}.
```

### Proof

The first identity is exactly the simplex constraint on the connected path set `P(u,v)`:

```math
\sum_{r\in P(u,v)}z[P(u,v),r]=1.
```

For the upper bounds, observe that `P(k,u) subset P(u,v)` and `P(k,v) subset P(u,v)`. By H1 heredity,

```math
z[P(u,v),k]\le z[P(k,u),k]
```

and

```math
z[P(u,v),k]\le z[P(k,v),k].
```

These are exactly

```math
Z^k_{u,v}\le X_{k,u},\qquad Z^k_{u,v}\le X_{k,v}.
```

∎

### Theorem 5.2: H2 gives the refined lower bound

For every interior `k in P(u,v)`, H2 implies

```math
Z^k_{u,v}\ge X_{k,u}+X_{k,v}-1.
```

### Proof

Apply H2 with

```math
S={k},\qquad A=P(k,u),\qquad B=P(k,v),\qquad A\cup B=P(u,v),\qquad r=k.
```

Then `z[{k},k]=1`, so H2 gives

```math
1-z[P(k,u),k]-z[P(k,v),k]+z[P(u,v),k]\ge0.
```

Rearranging yields

```math
z[P(u,v),k]\ge z[P(k,u),k]+z[P(k,v),k]-1,
```

which is the claimed inequality. ∎

### Public-overlap caveat

The path cover identity and upper LCA/ancestry bounds are already the basic Golinsky LP constraints. In Golinsky's thesis, the LP is first described through the nonlinear path condition

```math
X_{u,v}+X_{v,u}+\sum_{w\in(u,v)}\min\{X_{w,u},X_{w,v}\}\ge 1,
```

and then linearized in Section 3.4 by variables `Z^w_{u,v}` with constraints `Z^w_{u,v} <= X_{w,u}` and `Z^w_{u,v} <= X_{w,v}`. Thus H1 is best understood as a connected-subset extension whose path projection recovers the original Golinsky/SKZ path-cover and upper-bound semantics.

The lower bound

```math
Z^k_{u,v}\ge X_{k,u}+X_{k,v}-1
```

does **not** appear in Golinsky's original Section 3.4 formulation as inspected here, but it appears to correspond to SKZ Section 5.1's later "Refining `Z`" strengthening. Therefore this projected inequality should not be claimed as novel. The contribution is that H2 derives it uniformly as a path-shadow of the connected-subset extension rectangle system, while also imposing rectangle constraints on non-path connected subsets.

### Public comparison caution

This projection shows that H1/H2 naturally imply or recover several path-variable constraints in the Golinsky/SKZ language. It does not by itself prove that H2 implies every SKZ/Golinsky refinement, nor that H2 solves the public LP relaxation. The full public SKZ `X/Z` fractional point has not been checked as a fixed lift in the current repository; only the public depth vector has been ruled out as an H2 lift.

---

## 6. Certified SKZ `U(7,3)` H2 result

This is a certificate-backed result, not merely a numerical observation.

The internal exact certificate report uses the SKZ `U(7,3)` long-star topology with edges

```text
[[0,1],[1,2],[2,3],[3,4],[2,5],[5,6]]
```

and weights

```text
[3,2,0,2,3,3,10].
```

The H2 audit reports:

```text
connected_subsets = 36
z_variables = 120
canonical_nontrivial H2 rectangles = 1257
implemented_rectangles = 1257
missing_nontrivial_rows = 0
extra_rows = 0
```

The exact primal/dual verifier reports:

```text
verified H2 certificate: primal=30 dual_max=-30 lower_bound=30
```

Thus H2 optimum is exactly `30` for this weight vector.

The fixed-depth test uses the public SKZ fractional depth vector

```math
D=(2,2,9/2,2,2,3/2,1/2).
```

This vector forces weighted objective

```math
3\cdot 2+2\cdot2+0\cdot(9/2)+2\cdot2+3\cdot2+3\cdot(3/2)+10\cdot(1/2)=59/2.
```

The exact H2 dual proves every H2-feasible point has objective at least `30`; hence this depth vector has no H2 lift. Equivalently, the fixed-D system gives a Farkas-style contradiction with right-hand side `-1/2`.

### Correct interpretation

- The public SKZ topology, weights, fractional depth vector, and `59/2 < 30` gap are not new.
- The project contribution is the connected first-hit H2 extension, which is structurally richer than Golinsky's path-variable LP in two distinct ways: (i) it carries variables `z[I,r]` for every connected subset `I` of `T`, not only path subsets; and (ii) it enforces inclusion-poset consistency over connected sets, not only path-restricted ancestry/LCA-style constraints. The exact certificate shows that this connected-subset extension rules out the public fractional depth vector.
- This does not prove H2 is exact for all trees or for all weights on `U(7,3)`. A direct fixed-`X/Z` lift test for the full public SKZ path-variable assignment has not been run, but fixed-`D` infeasibility already rules out any H2 lift matching that point's depth projection.

---

## 7. Complete first-hit Möbius formulation and Q(T)

For every connected `C` and `r in C`, introduce a nonnegative variable

```math
m[C,r]\ge0.
```

The complete first-hit Möbius/zeta formulation is

```math
z[I,r]=\sum_{\substack{C\in Conn(T)\\ C\supseteq I}}m[C,r]
```

for every connected `I` and `r in I`, together with simplex

```math
\sum_{r\in I}z[I,r]=1.
```

Substituting the zeta relation into simplex gives the **rooted connected-subtree cover polytope** `Q(T)`:

```math
Q(T)=\left\{m\ge0:
\sum_{\substack{r\in I\\ C\in Conn(T),\ C\supseteq I}}m[C,r]=1
\text{ for every }I\in Conn(T)
\right\}.
```

Interpretation: each connected query set `I` is covered exactly once by a rooted connected subproblem `(C,r)` such that `r in I subset C`.

### Theorem 7.1: integral points of Q(T) are exactly STTs

The `0/1` points of `Q(T)` are exactly incidence vectors of STTs, where `m[C,r]=1` means that `r` is the root of recursive connected subproblem `C`.

### Proof

First let `tau` be an STT. Every vertex `r` is the root of exactly one recursive connected subproblem `C_r`. Set

```math
m[C,r]=1 \quad\Longleftrightarrow\quad C=C_r.
```

Fix connected `I`. Let `r=rho_tau(I)` be the first vertex of `I` queried by the STT. When `r` is queried, all vertices of `I` are still in the same recursive connected subproblem `C_r`; if an earlier query had separated them, that earlier query would have been a vertex whose removal separated the active subproblem, contradicting that `r` is the first queried vertex of `I`. Hence `I subset C_r` and `(C_r,r)` covers `I`.

Uniqueness follows because if two selected pairs `(C_r,r)` and `(C_s,s)` covered the same connected `I`, with `r,s in I`, then whichever of `r,s` is first queried in the STT would be `rho_tau(I)`. The later one cannot have a recursive subproblem containing the earlier root, so its selected set cannot contain all of `I`. Thus exactly one selected pair covers `I`.

Conversely, suppose `m in Q(T)` is `0/1`. For singleton `I={v}`,

```math
\sum_{C\ni v}m[C,v]=1,
```

so every vertex `v` selects a unique connected set `C_v` containing `v`.

For `I=V`, the only possible covering variables have `C=V`, so exactly one vertex `rho` satisfies `m[V,rho]=1`. Declare `rho` to be the STT root.

Let `K` be a component of `T-rho`, and let `v in K`. We claim `C_v subset K`. Suppose for contradiction that `C_v` contains some `w notin K`. Since `C_v` is connected in `T` and contains both `v in K` and `w notin K`, the unique `T`-path from `v` to `w` lies in `C_v`. Because `K` is a component of `T \ {rho}`, every `T`-path from a vertex of `K` to a vertex outside `K` passes through `rho`; hence `rho in C_v`. Then the connected path `P(v,rho)` is contained in `C_v` and also in `V`, so the connected set `P(v,rho)` is covered by both `(C_v,v)` and `(V,rho)`, contradicting the cover equation for `I=P(v,rho)`. Therefore `C_v subset K`.

Now apply the cover equation to the connected set `I=K`. Some selected pair `(C_r,r)` with `r in K` must cover `K`. Since all selected `C_r` with `r in K` are contained in `K`, this forces `C_r=K`. The covering root is unique. Recursing on each component gives exactly the recursive definition of an STT. ∎

### Theorem 7.2: Q(T) is bounded

Every variable `m[C,r]` satisfies `0 <= m[C,r] <= 1`.

### Proof

Nonnegativity is part of the definition. The singleton equation for `I={r}` is

```math
\sum_{C\ni r}m[C,r]=1.
```

Since every term is nonnegative and `m[C,r]` appears in this sum, `m[C,r] <= 1`. ∎

### Public-overlap caveat: Bellman recurrence vs polyhedral packaging

The Bellman recurrence used in the proof below is not new. Golinsky's thesis and Berendsohn's thesis both use recursive connected-subproblem reasoning for STTs, and Berendsohn's exact DP over connected induced subgraphs is the standard exponential exact algorithmic viewpoint.

The candidate contribution in this note is more specific: the rooted connected-subtree cover polytope `Q(T)`, its first-hit `z`-coordinate/Möbius interpretation, and the explicit Boolean-Möbius dual certificate proving integrality of this exponential marginal/cover formulation. This should be presented as a DP-derived/marginal-polytope specialization, not as a compact formulation or a polynomial-time algorithm.

### Theorem 7.3: Q(T) is integral for every tree

For every tree `T`, the polytope `Q(T)` is integral.

### Proof

Let `c[C,r]` be an arbitrary real cost vector. Consider the primal LP

```math
\min \sum_{C,r}c[C,r]m[C,r]
```

subject to the equations defining `Q(T)` and `m>=0`.

Define a Bellman value `F(S)` for every subset `S subset V` as follows. Set `F(empty)=0`. If `S` is disconnected, let

```math
F(S)=\sum_{K\in comp(T[S])}F(K),
```

where the sum is over connected components of the induced forest. If `C` is connected, define

```math
F(C)=\min_{r\in C}\left(c[C,r]+\sum_{K\in comp(C\setminus\{r\})}F(K)\right).
```

Choosing a minimizing root recursively for `V` and then for each component produces an STT incidence vector in `Q(T)` with cost `F(V)`. Therefore the primal optimum is at most `F(V)`.

Now construct a dual solution. The primal has equality constraints indexed by connected `I`, so the dual has unrestricted variables `y_I` and constraints

```math
\sum_{\substack{I\subseteq C\\ I\in Conn(T)\\ r\in I}}y_I\le c[C,r]
```

for every connected `C` and `r in C`.

Extend `F` to all subsets as above and define its Boolean Möbius transform

```math
\widehat F(S)=\sum_{R\subseteq S}(-1)^{|S|-|R|}F(R).
```

If `S` is disconnected, then `\widehat F(S)=0`. To see this, write the connected components of `T[S]` as `S_1,...,S_q` with `q>=2`. For each `R subset S`, additivity gives

```math
F(R)=\sum_{j=1}^q F(R\cap S_j).
```

Then

```math
\widehat F(S)
=\sum_{R\subseteq S}(-1)^{|S|-|R|}\sum_{j=1}^q F(R\cap S_j).
```

For a fixed `j`, the summation factors into an alternating sum over every component `S_l` with `l != j`. Since each such `S_l` is nonempty,

```math
\sum_{R_l\subseteq S_l}(-1)^{|S_l|-|R_l|}=(1-1)^{|S_l|}=0.
```

Thus every term cancels and `\widehat F(S)=0`.

Define

```math
y_I=\widehat F(I)
```

for connected `I`.

For connected `C` and `r in C`,

```math
\sum_{\substack{I\subseteq C\\ I\in Conn(T)\\ r\in I}}y_I
=
\sum_{\substack{I\subseteq C\\ r\in I}}\widehat F(I)
=
F(C)-F(C\setminus\{r\}).
```

The first equality uses `\widehat F(I)=0` for disconnected `I`. The second is the Boolean zeta/Möbius identity, subtracting the expansion of `F(C\setminus{r})` from the expansion of `F(C)`.

Since

```math
F(C\setminus\{r\})=\sum_{K\in comp(C\setminus\{r\})}F(K),
```

the Bellman recurrence gives

```math
F(C)-F(C\setminus\{r\})\le c[C,r].
```

Therefore `y` is dual feasible. Its objective value is

```math
\sum_{I\in Conn(T)}y_I
=
\sum_{S\subseteq V}\widehat F(S)
=F(V),
```

again using vanishing of disconnected Möbius coefficients and Boolean inversion.

Thus every linear objective has an integral feasible solution of value `F(V)` and a dual feasible solution of the same value. Hence the LP optimum is attained by an integral STT incidence vector for every cost vector `c`.

It remains to justify why this implies integrality. By Theorem 7.2, `Q(T)` is a bounded polytope defined by rational data. A standard characterization of rational integral polytopes says that a rational polytope is integral iff every linear-objective LP over it attains an integral optimum. Equivalently, if `Q(T)` had a nonintegral vertex `x`, then some rational objective vector in the relative interior of the normal cone at `x` would expose `x` as the unique optimum, contradicting the existence of an integral optimum at the same value. Therefore every vertex is integral, and `Q(T)` is integral. ∎

---

## 8. Complete formulation is exact

The complete first-hit Möbius formulation is exactly `Q(T)` in `z`-coordinates. It is exponential in general because it has variables indexed by rooted connected subproblems; it does not imply a polynomial-time exact algorithm unless additional compression or separation structure is found.

### Theorem 8.1

The feasible `z`-points admitting nonnegative masses

```math
z[I,r]=\sum_{C\supseteq I}m[C,r],\qquad m[C,r]\ge0,
```

with simplex are exactly the convex hull of true STT first-hit systems.

### Proof

Substituting the zeta relation into simplex gives the equations of `Q(T)`. By Theorems 7.1 and 7.3, `Q(T)` is the convex hull of STT rooted-subproblem incidence vectors. Applying the linear map

```math
m\mapsto z,
\qquad
z[I,r]=\sum_{C\supseteq I}m[C,r],
```

maps each STT incidence vector to its deterministic first-hit system and maps convex combinations to convex combinations. Therefore the complete formulation is exact. ∎

---

## 9. H2 exactness on paths

This section expands the path proof. It is a stable theorem-level result.

Let the tree be the path `[n]`. Connected sets are intervals. Fix a root `r`. Intervals containing `r` are indexed by two endpoints:

```math
[i,j],\qquad 1\le i\le r\le j\le n.
```

Ordered by inclusion,

```math
[i,j]\subseteq[i',j']\quad\Longleftrightarrow\quad i'\le i\text{ and }j\le j'.
```

Thus intervals containing `r` form a product of two chains: one chain for expanding left, and one chain for expanding right.

For fixed `r`, write

```math
g(i,j)=z[[i,j],r].
```

Define boundary values `g(i,j)=0` when `i<1` or `j>n`. Define candidate masses

```math
m[[a,b],r]
=
 g(a,b)-g(a-1,b)-g(a,b+1)+g(a-1,b+1)
```

for `a <= r <= b`.

### Lemma 9.1: H2 implies these masses are nonnegative

If `1<a<=r<=b<n`, then apply H2 with

```math
S=[a,b],\qquad A=[a-1,b],\qquad B=[a,b+1],\qquad A\cup B=[a-1,b+1].
```

This gives exactly

```math
g(a,b)-g(a-1,b)-g(a,b+1)+g(a-1,b+1)\ge0.
```

Boundary cases reduce to H1 or nonnegativity:

- If `a=1` and `b<n`, then

```math
m[[1,b],r]=g(1,b)-g(1,b+1)\ge0
```

by H1, since `[1,b] subset [1,b+1]`.

- If `a>1` and `b=n`, then

```math
m[[a,n],r]=g(a,n)-g(a-1,n)\ge0
```

by H1, since `[a,n] subset [a-1,n]`.

- If `a=1` and `b=n`, then

```math
m[[1,n],r]=g(1,n)\ge0.
```

Thus all interval masses are nonnegative. ∎

### Lemma 9.2: telescoping recovers z

For every interval `[i,j]` containing `r`,

```math
z[[i,j],r]=\sum_{\substack{a\le i\\ b\ge j}}m[[a,b],r].
```

### Proof

Substitute the definition of `m`. The sum

```math
\sum_{a\le i,\ b\ge j}
\big(g(a,b)-g(a-1,b)-g(a,b+1)+g(a-1,b+1)\big)
```

telescopes first over `a` and then over `b`, leaving exactly `g(i,j)`. The boundary terms vanish by the convention `g(a,b)=0` outside the path. ∎

### Lemma 9.3: simplex becomes the interval-root cover polytope

The simplex constraint

```math
\sum_{r\in I}z[I,r]=1
```

becomes

```math
\sum_{\substack{r\in I\\ J\supseteq I}}m[J,r]=1
```

for every interval `I`.

This is exactly the interval specialization of `Q(T)`.

### Theorem 9.4: H2 is exact on paths

For every path, H2 first-hit feasible points are exactly convex combinations of BST/STT first-hit systems.

### Proof

By Lemmas 9.1 and 9.2, every H2-feasible `z` on a path admits nonnegative interval masses `m[J,r]` with

```math
z[I,r]=\sum_{J\supseteq I}m[J,r].
```

By Lemma 9.3, simplex gives the interval-root cover polytope. This is `Q(T)` for the path, and `Q(T)` is integral and exact by Theorems 7.1 and 7.3. Therefore `z` is a convex combination of path STT/BST first-hit systems. ∎

### Consequence

H2 depth projection is exact on paths. This is a meaningful public-facing subclass result. It is not the same statement as exactness of the SKZ `Z`-eliminated path LP; it is an exactness theorem for the connected first-hit H2 formulation on paths. It does not imply H2 is exact on all trees.

---

## 10. The audited 4-leaf star obstruction

Let `T` be the star with center `0` and leaves `1,2,3,4`. Write

```math
O_S=\{0\}\cup S,
\qquad S\subseteq\{1,2,3,4\}.
```

Define `z` as follows.

For singletons:

```math
z[\{v\},v]=1.
```

For `O_S`, define the center value

```math
z[O_S,0]=
\begin{cases}
1,& |S|=0,\\
1/3,& |S|=1,\\
0,& |S|\ge2.
\end{cases}
```

For each leaf `i in S`, define

```math
z[O_S,i]=\frac{1-z[O_S,0]}{|S|}.
```

Thus

```math
z[\{0,i\},0]=1/3,
\qquad
z[\{0,i\},i]=2/3,
```

and for `|S|>=2`,

```math
z[O_S,0]=0,
\qquad
z[O_S,i]=1/|S|\quad(i\in S).
```

All other values are zero.

### Exact audit status

The merged star audit checked all constraints exactly over rational `Fraction` arithmetic. It reports:

```text
simplex equations = 20
z variables = 52
H1 heredity constraints = 173
H2 ordered rectangles = 1449
H2 canonical rectangles = 181
simplex residual = 0
min H1 slack = 0
min H2 ordered slack = 0
min H2 canonical slack = 0
```

Therefore the v4 star system is exactly H2-feasible.

### Analytic H1/H2 verification summary

Simplex is immediate from the construction:

```math
z[O_S,0]+\sum_{i\in S}z[O_S,i]=1.
```

H1 holds because the center values are

```math
1,\ 1/3,\ 0,\ 0,\ 0
```

as the leaf set grows, while for a fixed leaf `i` the values are

```math
1,\ 2/3,\ 1/2,\ 1/3,\ 1/4.
```

For H2, symmetry reduces the center-root cases to the set function

```math
f(\emptyset)=1,
\qquad
f(\{i\})=1/3,
\qquad
f(S)=0\quad(|S|\ge2),
```

whose pairwise finite differences are nonnegative. For a leaf root, the nontrivial values are the finite list

```math
1,\ 2/3,\ 1/2,\ 1/3,\ 1/4,
```

and the nonzero pairwise cases reduce to inequalities such as

```math
2/3-1/2-1/2+1/3=0,
```

```math
2/3-1/2-1/3+1/4=1/12,
```

```math
1/2-1/3-1/3+1/4=1/12.
```

A complete leaf-root case enumeration appears in the audit code. The inequalities verified include the center-root family, parametrized by the set function `f(S)=z[O_S,0]`, and the leaf-root family, parametrized by `g(S)=(1-f(S))/|S|` together with the singleton value `z[{i},i]=1`. In these coordinates, H2 reduces to nonnegativity of pairwise mixed second differences on the relevant Boolean lattices.

The exact audit is the authoritative finite check.

### Complete Möbius inversion: five negative masses

The complete-form inversion uses

```math
z[I,r]=\sum_{C\supseteq I}m[C,r].
```

The audit reports five negative masses:

```text
m[[0],0] = -1/3
m[[0, 1],1] = -1/12
m[[0, 2],2] = -1/12
m[[0, 3],3] = -1/12
m[[0, 4],4] = -1/12
```

The simplest analytic witness is the center-root mass. For center root `0`, Boolean inversion over the four leaves gives

```math
m[\{0\},0]
=
\sum_{S\subseteq\{1,2,3,4\}}(-1)^{|S|}z[O_S,0]
=
1-4\cdot(1/3)
=-1/3.
```

Thus the star `z`-system cannot be represented by nonnegative complete masses `m[C,r]`, and hence is not a convex combination of STT first-hit systems.

### Depth projection is not obstructed

The depth projection is

```math
(8/3,11/6,11/6,11/6,11/6),
```

with center depth `8/3` and each leaf depth `11/6`.

This vector lies in the STT dominant. The audit gives the exact dominant membership certificate: weight `1` on the center-root STT depth vector

```math
(0,1,1,1,1),
```

with component roots

```text
[([0,1,2,3,4],0), ([1],1), ([2],2), ([3],3), ([4],4)].
```

Since

```math
(8/3,11/6,11/6,11/6,11/6)
= (0,1,1,1,1)+(8/3,5/6,5/6,5/6,5/6),
```

and the slack vector is nonnegative, the star example is **not** a depth-projection obstruction under the root-depth-0 dominant convention.

### Correct conclusion

The 4-leaf star kills H2 exactness in full first-hit/`z`-space. It does **not** kill H2 depth-projection exactness.

---

## 11. Degree-at-least-4 embedding status

### Supported embedding claim, not yet a theorem

The natural conjecture is that the 4-leaf star obstruction embeds into any tree with a vertex of degree at least 4. The intended construction chooses four branches incident to a high-degree vertex and places the star obstruction on the center plus one neighbor from each branch, with deterministic behavior inside the branches.

The merged audit gives exact finite support for subdivided-star host trees. The tested branch-length vectors were:

```text
[1,1,1,1]
[2,1,1,1]
[2,2,1,1]
[2,2,2,2]
[3,2,1,1]
```

All sampled embeddings satisfy simplex/H1/H2 exactly and preserve

```text
m[{0},0] = -1/3
```

with five negative masses.

However, these finite checks are not a formal general proof. The remaining burden is to prove all cross-boundary H2 cases for arbitrary branch lengths and arbitrary host-tree attachments.

Concretely, the cross-boundary H2 cases that remain to be proved in general include the following types, indexed by where `S`, `A`, and `B` sit relative to the core/branch boundary:

1. `S` is contained in the core, while `A` and `B` both extend into the same branch at different depths.
2. `S` is contained in the core, while `A` extends into branch `X` and `B` extends into branch `Y`, with `X != Y`.
3. `S` straddles the core/branch boundary, while `A` and `B` extend farther into the same branch.
4. `S` is a singleton in a branch, while `A` and `B` extend toward or away from the core.

Each case type subdivides further according to whether the root `r` lies in the core or in a branch. The deterministic behavior within branches should collapse many within-branch inequalities to H1 monotonicity, but the across-boundary inequalities require the central star-obstruction values to interact correctly with branch values. A complete proof should either give a uniform case reduction or an induction on total branch length, with the audited pure 4-leaf star as the base case.

Until that proof is written, the degree-at-least-4 embedding should be labeled:

> **Provisional / certificate-supported:** finite exact audits support the embedding theorem, but a complete general proof remains open.

The note should not state the degree-at-least-4 embedding as a settled theorem.

---

## 12. Hierarchy interpretation

The complete first-hit Möbius formulation enforces all nonnegative Möbius masses on the connected-set inclusion posets.

This hierarchy should be described as a concrete response to SKZ Section 6's open directions on stronger formulations, DP-to-LP transformations, dual certificates, decomposition/peeling, path subclasses, almost-star subclasses, and depth-space projections. It should not be described as if the public literature had not already suggested stronger LPs and DP-derived LPs.

For a fixed root `r`, consider the poset

```math
Conn_r(T)=\{I\in Conn(T): r\in I\}
```

ordered by inclusion. The complete formulation requires that the upper Möbius inverse of `z[.,r]` on this poset be nonnegative.

H1 is order-1 monotonicity. H2 is the order-2/pairwise union finite-difference truncation. Higher `H_k` levels impose higher finite differences but still may be weaker than complete Möbius nonnegativity unless `k` is large enough for the branching dimension of the local connected-superset poset.

This explains the current results:

- On paths, connected supersets of a fixed root form a product of two chains. Pairwise mixed differences suffice; H2 is exact.
- On a 4-leaf star centered at `0`, connected supersets of `0` form a Boolean lattice of dimension 4. Pairwise differences do not force fourth-order Möbius mass nonnegativity; H2 fails in full `z`-space.
- The complete formulation is exact for all trees but exponential.

---

## 13. Killed, corrected, and demoted claims

### Killed / corrected

- **“H1 might be enough as a depth relaxation.”** Dead. The SKZ `U(7,3)` depth vector has an H1 lift and value `59/2 < 30`.
- **“H2 might be globally exact in full z-space.”** Dead. The audited 4-leaf star is H2-feasible but has negative complete Möbius masses.
- **“The 4-leaf star obstruction proves H2 fails as a depth relaxation.”** False. Its depth vector is in the STT dominant.

### Demoted / provisional

- **Degree-at-least-4 embedding theorem.** Supported by exact finite audits but not yet fully proved. Cross-boundary H2 cases require a complete proof.
- **Direct fixed-`X/Z` lift audit.** Not run as a separate path-variable fixed-lift test. However, fixed-`D` infeasibility already rules out any H2 lift matching the public SKZ point's depth projection.

### Stable

- Complete `Q(T)` formulation exact/integral for all trees.
- H2 exact on paths.
- H2 exact-certified on the SKZ `U(7,3)` weight direction and fixed-D vector has no H2 lift.
- 4-leaf star obstruction in full first-hit space.

---

## 14. Paper-worthiness assessment

The project appears to have reached paper-worthy territory as a short theorem/certificate note, pending an author-courtesy/public-overlap check and one more independent audit of the main proofs and the public-comparison language. The direct Golinsky thesis inspection improves the attribution picture: it did not reveal connected-subset first-hit variables, complete Möbius masses, or extension rectangles, but it did confirm substantial overlap with the original path/ancestry LP, depth-space focus, and standard recursive STT reasoning. Concretely, a clean paper draft should wait until all of the following are independently audited:

1. `Q(T)` integrality proof, including boundedness and the “linear objectives imply integrality” step.
2. H2 path exactness proof, including product-of-chains Möbius inversion.
3. 4-leaf star obstruction, including exact H1/H2 feasibility and all negative complete-Möbius masses.
4. SKZ `U(7,3)` H2 certificate, including exact primal/dual verification and fixed-D infeasibility.
5. Public Golinsky/SKZ comparison, written precisely: Golinsky's original LP and SKZ's path-variable refinements must be attributed; the public 7-node gap must not be claimed as new; the H2 lower `Z` path inequality should be treated as corresponding to SKZ's `Refining Z` discussion.
6. Degree-at-least-4 embedding either proved fully or clearly labeled as provisional.

The paper should **not** claim:

- a polynomial-time exact algorithm for optimal STTs;
- a compact extended formulation;
- that H2 solves optimal STT computation;
- that H2 fails as a depth relaxation because of the 4-leaf star;
- that the SKZ 7-node counterexample itself is new.

---

## 15. Best next theorem targets

### Target A: bounded-order hierarchy lower bound on stars

Prove that for every fixed `k`, there exists a star with sufficiently many leaves and an `H_k`-feasible first-hit system whose complete Möbius inverse has a negative higher-order mass.

Important distinction: this would be a full `z`-space hierarchy lower bound, not automatically a depth-projection lower bound.

### Target B: degree-at-least-4 embedding proof

Turn the finite audited embedding evidence into a theorem by proving all cross-boundary H2 cases for arbitrary host trees with a degree-at-least-4 vertex.

### Target C: depth-projection behavior of H2/Hk on stars

The 4-leaf star obstruction is not a depth obstruction. The next depth-focused question is whether H2, or bounded `H_k`, is depth-projection exact on stars and small bounded-degree trees.

### Target D: public LP comparison

Classify which SKZ/Golinsky constraints correspond to H1, H2, or higher-order first-hit conditions. H2 already implies the refined lower bound

```math
Z^k_{u,v}\ge X_{k,u}+X_{k,v}-1.
```

A clean comparison table would make the project easier to communicate. The current v4.3 comparison is: original Golinsky LP = path/ancestry `X` plus path-min linearization `Z`; SKZ refinements = path monotonicity, ancestry transitivity, LCA separation, refined `Z`, row-min/column-max; connected first-hit hierarchy = arbitrary connected-set `z[I,r]` plus finite-difference/Möbius consistency, whose path projection recovers some of the public constraints but whose non-path rectangles live in a different extension space.

---

## 16. Best next computational targets

Computations should remain theorem-driven.

1. **Depth-projection tests for stars.** Since the audited star obstruction is not a depth obstruction, test H2 and small `H_k` depth-projection behavior on stars with increasing leaves.
2. **Small bounded-degree trees.** Test H2/Hk depth-projection behavior on small trees of maximum degree 3 and 4, separating full-`z` failure from depth failure.
3. **Embedding proof support.** Generate symbolic or exact case classifications for cross-boundary H2 inequalities in subdivided-star embeddings, aimed at a proof rather than a benchmark table.
4. **SKZ benchmark continuation.** After theory cleanup, test H2 on the public small SKZ gap directions beyond `U(7,3)`.

Avoid random broad sweeps unless they are tied to one of the above questions.

---

## 17. Stable theorem-level claims

1. Every STT induces first-hit variables satisfying H1 and H2.
2. H1 projects to the basic path/LCA Golinsky/SKZ-style constraints; H2 implies the refined lower bound `Z >= X+X-1`.
3. The complete first-hit Möbius formulation is exactly `Q(T)`.
4. Integral points of `Q(T)` are exactly STTs.
5. `Q(T)` is bounded and integral for every tree by a Bellman/Boolean-Möbius dual proof.
6. H2 is exact on paths.
7. The 4-leaf star system is H2-feasible but not complete-Möbius representable, hence H2 is not exact in full `z`-space.

---

## 18. Certificate-backed claims

1. H2 closes the SKZ `U(7,3)` weight-direction gap exactly for the public weight vector `[3,2,0,2,3,3,10]`: H2 optimum is exactly `30` for these weights. H2 has not been checked exhaustively against other nonnegative weight vectors on `U(7,3)`.
2. The public SKZ fractional depth vector `(2,2,9/2,2,2,3/2,1/2)` has no H2 lift.
3. The 4-leaf star audit checked exactly:
   - simplex residual `0`;
   - min H1 slack `0`;
   - min H2 slack `0`.
4. The 4-leaf star complete-Möbius inversion has five negative masses:
   - `m[[0],0] = -1/3`;
   - `m[[0,1],1] = -1/12`;
   - `m[[0,2],2] = -1/12`;
   - `m[[0,3],3] = -1/12`;
   - `m[[0,4],4] = -1/12`.
5. The 4-leaf star depth vector `(8/3,11/6,11/6,11/6,11/6)` is in the STT dominant, dominated by `(0,1,1,1,1)`.

---

## 19. Provisional claims

1. The 4-leaf star obstruction likely embeds in any tree with a vertex of degree at least 4. Finite exact audits support this, but a general cross-boundary H2 proof remains to be written.
2. Bounded-order `H_k` likely fails on high-degree stars in full `z`-space. This is the best next theorem target.
3. H2/Hk depth-projection behavior on stars is unresolved. The existing 4-leaf star obstruction does not settle it.

---

## 20. Killed/demoted claims

1. H1 as a viable depth relaxation: killed by SKZ `U(7,3)`.
2. H2 as a globally exact full-`z` formulation: killed by the 4-leaf star.
3. 4-leaf star as a depth-projection obstruction: killed by the dominant certificate.
4. Degree-at-least-4 embedding as settled theorem: demoted to supported/provisional until the cross-boundary proof is complete.

---

## 21. Next Codex task

```text
Create branch: stt-star-depth-projection-v0

Goal:
Test H2 and small H_k depth-projection behavior on stars, separating full-z obstruction from depth obstruction.

Tasks:
1. Derive and implement the symmetric star reduction first. Variables and constraints should be grouped by leaf-permutation orbits, and the report should explain the orbit types before any objective sweep.
2. Implement H_k finite-difference constraints for stars for k=2,3,4 where feasible.
3. For d-leaf stars with d increasing, optimize structured small-integer depth objectives first, using random objectives only as secondary scouting, over:
   - true STT dominant;
   - H2 depth projection;
   - H3/H4 depth projections when feasible;
   - complete Q(T) projection as a check.
4. Compare the symmetric reduction against the full LP for small d.
5. Produce exact rational certificates for any depth-projection gap.
6. If no gaps are found for small d, report this only as evidence, not a theorem, and extract candidate theorem patterns or dual certificates.
7. Include the audited 4-leaf star full-z obstruction and verify again that its depth vector is dominated by center-root STT.
8. Output a Markdown report and JSON artifacts.
```

This task is intentionally depth-focused. It should not merely reproduce the known full-`z` star obstruction.

---

## 22. Next adversarial audit task

```text
Audit Frontier Note v4.4 for mathematical overclaims.

Focus especially on:
1. The Q(T) integrality proof:
   - boundedness;
   - dual construction;
   - vanishing disconnected Möbius coefficients;
   - why every objective having an integral optimum implies polytope integrality.
2. The H2 path exactness proof:
   - product-of-two-chains structure;
   - boundary cases in adjacent mixed differences;
   - telescoping inversion;
   - reduction to Q(T).
3. The 4-leaf star section:
   - exact H1/H2 feasibility;
   - all five negative masses;
   - depth vector and dominant membership;
   - clear statement that this is not a depth-projection obstruction.
4. The degree-at-least-4 embedding status:
   - confirm it is properly downgraded to provisional;
   - identify what cross-boundary H2 cases remain for a full proof.
5. Public-context caution:
   - no claim that the SKZ counterexample is new;
   - no claim of polynomial-time optimal STT computation;
   - no claim that H2 solves optimal STTs.

Return a self-contained audit with corrections and suggested patches.
```

---

## 23. Source-comparison status after Golinsky thesis inspection

The v4.2 source-comparison chores have now mostly been addressed.

### 23.1 Confirmed public-overlap zones

1. **Original LP variables and constraints.** Golinsky's thesis uses ordered ancestry variables `X_{u,v}` and the path-min condition with `min{X_{w,u},X_{w,v}}`. Section 3.4 linearizes this with `Z^w_{u,v}` variables and upper bounds `Z <= X`. This is exactly the public path-variable world that SKZ later studies.
2. **Depth-space focus.** Golinsky explicitly reformulates the conjecture in terms of the depth operator `phi(X)_v=sum_{u!=v}X_{u,v}` and suggests studying the image `phi(D(T))`. Thus any depth-projection framing must be attributed.
3. **Connected-subgraph projection.** Golinsky proves a projection theorem for restricting a true search tree to a connected subgraph `H`, with paths intersected with `H`. This is not the same as connected-subset first-hit variables, but it is related STT-on-connected-subgraphs structure and should be cited when discussing first-hit restriction/projection intuition.
4. **Standard recursive DP/Bellman recurrence.** The complete `Q(T)` formulation should be described as DP-derived, not as a new recurrence.

### 23.2 Checked and not found in Golinsky thesis

Direct text search and reading of Sections 3.1--3.5 and Appendix A found no visible occurrence of:

- variables indexed by arbitrary connected subsets `I` and roots `r in I`;
- first-hit probabilities `z[I,r]`;
- complete Möbius or zeta inversion over connected-set inclusion posets;
- extension rectangles `z[S,r]-z[A,r]-z[B,r]+z[A union B,r] >= 0`;
- rooted connected-subtree cover equations `sum_{r in I, C superset I} m[C,r]=1`.

This absence is evidence, not proof, of novelty. It should be phrased as "not found in inspected public sources/thesis," not as a categorical novelty claim.

### 23.3 Remaining source-comparison risks

1. **Graph associahedra / elimination-tree polytopes.** Public graph-associahedron literature has vertices corresponding to elimination trees/search trees and edges corresponding to rotations. This is close object-level territory, but appears different from `Q(T)`, whose variables are rooted connected subproblem marginals and whose constraints are first-hit cover equations.
2. **DP-to-LP / marginal-polytope literature.** The `Q(T)` proof may be an instance of standard dynamic-programming-as-LP or parse-tree marginal-polytope machinery. The STT specialization and Boolean-Möbius dual certificate remain useful, but novelty should be stated carefully.
3. **SKZ Section 5.1 refinements.** The projected H2 lower `Z` bound corresponds to SKZ's `Refining Z` item. Treat this as recovered/rederived, not new.
4. **Depth projection of stars.** The 4-leaf star obstruction is full-`z`, not depth-projection. This remains a key place to prevent overclaiming.

### 23.4 Courtesy-email status

An author courtesy email is no longer needed merely to obtain Golinsky's thesis. It may still be useful before public posting to ask whether connected-subset first-hit variables, complete Möbius consistency, or extension rectangles appeared in unpublished notes.

## 24. Current bottom line

The project is in a good state. After direct Golinsky thesis inspection, the public-overlap boundary is clearer. The project has a coherent mathematical hierarchy and multiple independently meaningful results:

- complete exact exponential formulation;
- H2 exactness on paths;
- H2 certified repair of the public SKZ `U(7,3)` depth vector;
- audited full-`z` failure on the 4-leaf star;
- a clear next frontier around bounded-order hierarchy lower bounds and depth-projection behavior.

The main danger is overclaiming. The right framing is:

> H2 is a useful low-order truncation of an exact connected first-hit Möbius formulation. It is exact on paths and fixes an important public small gap, but it is not globally exact in full first-hit space. The complete formulation is exact but exponential.


## References and checked sources

- Ishay Golinsky, *A study on search trees on trees*, Master's thesis, Tel Aviv University, April 2023. Uploaded PDF inspected directly.
- Yaniv Sadeh, Haim Kaplan, Uri Zwick, *Search Trees on Trees via LP*, arXiv:2501.17563. URL: https://arxiv.org/abs/2501.17563
- Benjamin Aram Berendsohn, *Search trees on graphs*, PhD thesis, Berlin University, 2024. URL: https://refubium.fu-berlin.de/handle/fub188/45994
- Benjamin Aram Berendsohn, Ishay Golinsky, Haim Kaplan, Laszlo Kozma, *Fast Approximation of Search Trees on Trees with Centroid Trees*, ICALP 2023 / arXiv:2209.08024. URL: https://arxiv.org/abs/2209.08024
- Jean Cardinal, Arturo Merino, Torsten Muetze, *Efficient generation of elimination trees and graph associahedra*, SODA 2022. Used as prior-name context for elimination trees and graph associahedra, not as an identified prior occurrence of `Q(T)`.
