# Frontier Note v4.5: Connected First-Hit Hierarchy for Static Search Trees on Trees

**Date:** 2026-05-16  
**Project:** AI and Data Structures / STT LP frontier  
**Status:** v4.4 plus pure-star depth-projection theorem; fresh-context handoff for the connected first-hit hierarchy and next spider/double-star push  
**Conventions:** root-depth-0 weighted depth unless explicitly stated otherwise

**Patch note:** This version patches the v4.5 audit issue that incorrectly listed double-stars among the classes ruled out by the SKZ \(U(7,3)\) H1 gap. The \(U(7,3)\) example rules out extension to all spiders/subdivided stars and all max-degree-3 trees, but not to double-stars. It also standardizes depth-dominance language as membership in \(\operatorname{conv}(\mathrm{STTDepth})+\mathbb R_{\ge0}^V\).

---

## 0. Step-back verdict: v4.5, not v5

This is a **v4.5** frontier note, not v5.

The update from Frontier Note v4.4 is mathematically meaningful: the previously unresolved depth-projection behavior of H2/Hk on stars is now resolved positively, and in a stronger form:

> **Pure-star depth-projection theorem.** On every star \(K_{1,d}\), H1 already has exact depth projection. Equivalently, every H1-feasible first-hit system has a depth vector lying in \(\operatorname{conv}(\text{true star STT depth vectors})+\mathbb R_{\ge0}^{d+1}\); equivalently, some convex combination of true star STT depth vectors is coordinatewise no larger. Hence H2 and every higher \(H_k\) are also depth-exact on pure stars.

This is theorem-level and should be carried forward.

However, it does not reorganize the whole project. The main v4.4 narrative remains correct:

- the complete connected first-hit/Möbius formulation \(Q(T)\) is exact but exponential;
- H2 is a useful low-order truncation;
- H2 is exact on paths;
- H2 closes the tested SKZ \(U(7,3)\) depth-vector gap;
- H2 fails in full \(z\)-space on the 4-leaf star;
- the 4-leaf star full-\(z\) obstruction is not a depth-projection obstruction;
- degree-at-least-4 embedding remains provisional.

A v5 should wait for one of the following:

1. H2 depth-projection exactness or failure on all spiders/subdivided stars;
2. H2 depth-projection exactness or failure on all double-stars;
3. H2 exactness/failure on all max-degree-3 trees;
4. a new public-context or novelty correction comparable to the Golinsky/SKZ comparison patch;
5. a compact structural theorem that changes the likely route toward the original optimization problem.

The immediate new frontier is:

> **Spider H2 depth projection.** Does H2 have exact depth projection on every subdivided star/spider?

---

## 1. Public problem statement and public frontier

A **static search tree on a tree** (STT) is defined recursively. Given a finite tree \(T=(V,E)\), choose a root \(r\in V\), delete \(r\), and recurse on each connected component of \(T-r\). The resulting rooted tree has the same vertex set \(V\). The depth \(d_\tau(v)\) of a vertex \(v\) in an STT \(\tau\) is its number of strict ancestors.

Given nonnegative weights \(w_v\), the weighted root-depth-0 objective is

\[
\operatorname{cost}_w(\tau)=\sum_{v\in V} w_v d_\tau(v).
\]

The public exact optimization problem is:

> Given \(T\) and \(w\ge0\), compute an STT minimizing \(\operatorname{cost}_w\).

Public context, as checked for v4.5:

- Sadeh--Kaplan--Zwick study Golinsky's LP relaxation for optimal STTs. They state that Golinsky conjectured the LP to be an extended formulation of the convex hull of depth vectors of STTs, then disprove that conjecture using the normals method. Their paper also enumerates directions toward resolving whether optimal STTs on trees can be computed in polynomial time.
- Berendsohn's thesis records that no polynomial-time exact algorithm is known for the optimal static search-tree problem on graphs, even when the underlying graph is a tree.
- Berendsohn--Golinsky--Kaplan--Kozma's centroid-tree work gives efficient weighted centroid-tree construction and a tight 2-approximation, not exact optimization.

This project should therefore not claim:

- a polynomial-time exact algorithm for optimal STTs;
- a compact exact extended formulation;
- that H2 solves optimal STT computation;
- that the public SKZ counterexample is new;
- that the 4-leaf star full-\(z\) obstruction is a depth-projection obstruction.

---

## 2. Core definitions

Let \(\operatorname{Conn}(T)\) be the family of nonempty connected vertex subsets of \(T\).

For a deterministic STT \(\tau\) and connected set \(I\in\operatorname{Conn}(T)\), define

\[
\rho_\tau(I)=\text{the first vertex of }I\text{ queried by }\tau.
\]

For a distribution over STTs, define first-hit variables

\[
z[I,r]=\Pr(\rho_\tau(I)=r),\qquad I\in\operatorname{Conn}(T),\ r\in I.
\]

For a deterministic STT, \(z[I,r]=1_{\rho_\tau(I)=r}\).

The root-depth-0 depth projection is

\[
D_v(z)=\sum_{u\ne v} z[P(u,v),u],
\]

where \(P(u,v)\) is the vertex set of the unique path from \(u\) to \(v\). In a deterministic STT, \(u\) is an ancestor of \(v\) iff \(u\) is the first-hit vertex of the path \(P(u,v)\), so this projection recovers ordinary depths.

---

## 3. H1, H2, and complete connected first-hit consistency

### H1

For every connected \(I\):

\[
z[I,r]\ge0,\qquad \sum_{r\in I}z[I,r]=1.
\]

For connected \(B\subset A\) and \(r\in B\):

\[
z[A,r]\le z[B,r].
\]

### H2

For connected \(S,A,B,A\cup B\), with \(S\subseteq A\), \(S\subseteq B\), and \(r\in S\):

\[
z[S,r]-z[A,r]-z[B,r]+z[A\cup B,r]\ge0.
\]

### Complete Möbius/zeta formulation

For each connected \(C\) and \(r\in C\), introduce \(m[C,r]\ge0\) and require

\[
z[I,r]=\sum_{\substack{C\in\operatorname{Conn}(T)\\C\supseteq I}}m[C,r].
\]

Substitution into simplex gives the rooted connected-subtree cover polytope

\[
Q(T)=
\left\{
m\ge0:
\sum_{\substack{r\in I\\C\in\operatorname{Conn}(T),\,C\supseteq I}}
m[C,r]=1
\quad\forall I\in\operatorname{Conn}(T)
\right\}.
\]

---

## 4. Every STT satisfies H1 and H2

### Theorem 4.1

Every distribution over STTs induces first-hit variables satisfying H1 and H2.

### Proof

It is enough to prove the claim for deterministic STTs and then take convex combinations.

For a deterministic STT, exactly one vertex of every connected set \(I\) is first-hit, so simplex and nonnegativity hold.

For H1 heredity, let \(B\subset A\) be connected and let \(r\in B\). If \(\rho(A)=r\), then no vertex of \(A\) is queried before \(r\). Since \(B\subset A\), no vertex of \(B\) is queried before \(r\), hence \(\rho(B)=r\). Thus

\[
1_{\rho(A)=r}\le 1_{\rho(B)=r}.
\]

For H2, define \(E_C^r=\{\rho(C)=r\}\). For \(S\subseteq A,B\) and \(r\in S\),

\[
E_{A\cup B}^r=E_A^r\cap E_B^r.
\]

Indeed, if \(r\) is first in \(A\cup B\), it is first in both \(A\) and \(B\). Conversely, if \(r\) is first in both \(A\) and \(B\), then no vertex of \(A\cup B\) occurs before \(r\), so \(r\) is first in \(A\cup B\).

Also \(E_A^r,E_B^r\subseteq E_S^r\). Therefore

\[
1_{E_S^r}-1_{E_A^r}-1_{E_B^r}+1_{E_{A\cup B}^r}
=
1_{E_S^r\setminus(E_A^r\cup E_B^r)}
\ge0.
\]

Taking expectations gives H2. ∎

---

## 5. Complete formulation is exact

### Theorem 5.1

The \(0/1\) points of \(Q(T)\) are exactly STTs.

### Proof

Given an STT \(\tau\), let \(C_r\) be the recursive connected subproblem in which \(r\) is chosen as root. Set

\[
m[C,r]=1 \Longleftrightarrow C=C_r.
\]

For connected \(I\), let \(r=\rho_\tau(I)\). When \(r\) is queried, all of \(I\) is still inside the active subproblem \(C_r\), so \((C_r,r)\) covers \(I\). This covering pair is unique: if another selected \((C_s,s)\) with \(s\in I\) covered \(I\), then whichever of \(r,s\) was queried earlier would separate the later one from the active problem containing all of \(I\), a contradiction. Hence the cover equations hold.

Conversely, suppose \(m\in Q(T)\) is \(0/1\). For singleton \(\{v\}\), the equation

\[
\sum_{C\ni v}m[C,v]=1
\]

selects a unique connected set \(C_v\) for each vertex \(v\). For \(I=V\), exactly one selected pair has \(C=V\); call its root \(\rho\). Declare \(\rho\) to be the STT root.

Let \(K\) be a component of \(T-\rho\), and let \(v\in K\). If \(C_v\) contained a vertex outside \(K\), then since \(C_v\) is connected it would contain \(\rho\). Then the path \(P(v,\rho)\) would be covered both by \((C_v,v)\) and by \((V,\rho)\), contradicting the cover equation. Hence \(C_v\subseteq K\).

Apply the cover equation to \(I=K\). Since selected sets rooted in \(K\) are contained in \(K\), some selected pair must be \((K,r)\) with \(r\in K\), and it is unique. Recurse on components. This is exactly the recursive definition of an STT. ∎

### Theorem 5.2

\(Q(T)\) is integral for every tree.

### Proof

Let \(c[C,r]\) be any real objective. Define a Bellman value \(F(S)\) for all \(S\subseteq V\). Set \(F(\emptyset)=0\). If \(S\) is disconnected, define

\[
F(S)=\sum_{K\in\operatorname{comp}(T[S])}F(K).
\]

If \(C\) is connected, define

\[
F(C)=
\min_{r\in C}
\left(
c[C,r]+\sum_{K\in\operatorname{comp}(C\setminus\{r\})}F(K)
\right).
\]

Choosing minimizing roots recursively gives an STT incidence vector in \(Q(T)\) with cost \(F(V)\).

Now form the Boolean Möbius transform

\[
\widehat F(S)=\sum_{R\subseteq S}(-1)^{|S|-|R|}F(R).
\]

If \(S\) is disconnected, \(\widehat F(S)=0\). To see this, write \(S=S_1\sqcup\cdots\sqcup S_q\) as connected components with \(q\ge2\). Since \(F(R)=\sum_jF(R\cap S_j)\), each term in the Möbius transform factors through an alternating sum over at least one nonempty component \(S_\ell\) not used by that summand, giving \((1-1)^{|S_\ell|}=0\).

Define dual variables \(y_I=\widehat F(I)\) for connected \(I\). The dual constraint for \((C,r)\) is

\[
\sum_{\substack{I\subseteq C\\I\in\operatorname{Conn}(T)\\r\in I}}y_I\le c[C,r].
\]

Using the vanishing of disconnected Möbius coefficients,

\[
\sum_{\substack{I\subseteq C\\r\in I}} \widehat F(I)
=
F(C)-F(C\setminus\{r\}).
\]

The Bellman recurrence gives

\[
F(C)-F(C\setminus\{r\})\le c[C,r],
\]

so \(y\) is dual feasible. Its objective is

\[
\sum_{I\in\operatorname{Conn}(T)}y_I
=
\sum_{S\subseteq V}\widehat F(S)
=
F(V).
\]

Thus every linear objective over \(Q(T)\) has an integral primal optimum with matching dual value. Since \(Q(T)\) is bounded by singleton equations and nonnegativity, a standard rational-polytope separation argument implies that every vertex is integral: otherwise a rational objective exposing a nonintegral vertex uniquely would contradict the existence of an integral optimum for that objective. ∎

### Corollary 5.3

The complete connected first-hit Möbius formulation is exactly the convex hull of true STT first-hit systems.

### Proof

The map \(m\mapsto z\) is linear:

\[
z[I,r]=\sum_{C\supseteq I}m[C,r].
\]

By Theorems 5.1 and 5.2, \(Q(T)\) is the convex hull of STT rooted-subproblem incidence vectors. Applying the linear map sends these incidence vectors to deterministic first-hit systems and sends convex combinations to convex combinations. ∎

---

## 6. H2 exactness on paths

### Theorem 6.1

For every path, H2 first-hit feasible points are exactly convex combinations of true path STT/BST first-hit systems.

### Proof

Let the path be \([n]\). Connected sets are intervals. Fix root \(r\). Intervals containing \(r\) are \([i,j]\) with \(i\le r\le j\). Ordered by inclusion, these form a product of two chains.

Write

\[
g(i,j)=z[[i,j],r],
\]

with boundary values \(g(i,j)=0\) outside the path. Define

\[
m[[a,b],r]
=
g(a,b)-g(a-1,b)-g(a,b+1)+g(a-1,b+1).
\]

For interior \(a,b\), H2 applied to

\[
S=[a,b],\quad A=[a-1,b],\quad B=[a,b+1]
\]

gives \(m[[a,b],r]\ge0\). Boundary cases reduce to H1 monotonicity or nonnegativity:

\[
m[[1,b],r]=g(1,b)-g(1,b+1)\ge0,
\]
\[
m[[a,n],r]=g(a,n)-g(a-1,n)\ge0,
\]
\[
m[[1,n],r]=g(1,n)\ge0.
\]

The inversion telescopes:

\[
z[[i,j],r]
=
\sum_{\substack{a\le i\\b\ge j}}m[[a,b],r].
\]

Substituting into simplex gives exactly the path specialization of \(Q(T)\). Since \(Q(T)\) is integral, every H2-feasible path first-hit system is a convex combination of true path STTs. ∎

---

## 7. Certificate-backed \(U(7,3)\) result

This is certificate-backed, not purely hand-proved in this note.

The SKZ \(U(7,3)\) long-star topology has edges

```text
[[0,1],[1,2],[2,3],[3,4],[2,5],[5,6]]
```

and weights

```text
[3,2,0,2,3,3,10].
```

This is a subdivided 3-star/spider with center \(2\) and three arms of length 2:

\[
2-1-0,\qquad 2-3-4,\qquad 2-5-6.
\]

The public fractional depth vector is

\[
D=(2,2,9/2,2,2,3/2,1/2)
\]

with weighted value

\[
3\cdot2+2\cdot2+0\cdot(9/2)+2\cdot2+3\cdot2+3\cdot(3/2)+10\cdot(1/2)=59/2.
\]

The true optimum/certified H2 value is \(30\). The internal exact H2 primal/dual certificate verifies H2 optimum \(30\), so this public depth vector has no H2 lift.

Consequences:

- H1 is dead as a general depth relaxation.
- The pure-star H1 theorem below does not extend to subdivided stars.
- H2 remains plausible on spiders because it repairs this tested \(U(7,3)\) gap direction, but no all-spider theorem is known.

---

## 8. The 4-leaf star full-\(z\) obstruction

Let \(T\) be the star with center \(0\) and leaves \(1,2,3,4\). Write

\[
O_S=\{0\}\cup S,\qquad S\subseteq\{1,2,3,4\}.
\]

The audited construction sets

\[
z[O_S,0]=
\begin{cases}
1,& |S|=0,\\
1/3,& |S|=1,\\
0,& |S|\ge2,
\end{cases}
\]

and for leaves \(i\in S\),

\[
z[O_S,i]=\frac{1-z[O_S,0]}{|S|}.
\]

The exact audit verified simplex, H1, and H2 over rational arithmetic. However, complete Möbius inversion has negative masses:

\[
m[\{0\},0]=-1/3,
\]

and

\[
m[\{0,i\},i]=-1/12\qquad i=1,2,3,4.
\]

Thus H2 is not exact in full first-hit \(z\)-space.

The depth projection is

\[
(8/3,11/6,11/6,11/6,11/6),
\]

which is dominated by the true center-root STT depth vector

\[
(0,1,1,1,1).
\]

Therefore this example is **not** a depth-projection obstruction.

---

## 9. New theorem: H1/H2 depth exactness on pure stars

This is the main v4.5 update.

Let \(K_{1,d}\) be the star with center \(0\) and leaves \([d]=\{1,\ldots,d\}\). For \(S\subseteq[d]\), write

\[
O_S=\{0\}\cup S.
\]

### Theorem 9.1: star STT structure

Every STT on \(K_{1,d}\) consists of:

1. an ordered prefix of leaves queried before the center;
2. the center;
3. all remaining leaves as singleton children of the center.

For any chosen before-center leaf set \(A\), the minimum weighted STT with exactly this set queries the leaves of \(A\) in nonincreasing weight order.

### Proof

If the root is the center, deleting it isolates every leaf, so the STT is the center followed by singleton leaves.

If the root is a leaf, deleting it leaves a smaller connected star on the center and remaining leaves. Thus the next recursive root is again either the center or another leaf. This continues until the center is selected. Once the center is selected, deleting it isolates all remaining leaves, which become singleton subproblems. Hence every STT has the claimed leaf-prefix/center/suffix form.

For the ordering claim, suppose two consecutive before-center leaves \(i,j\) are queried in the order \(j\) then \(i\), but \(u_i\ge u_j\). Swapping them decreases the depth of \(i\) by 1 and increases the depth of \(j\) by 1, changing cost by

\[
-u_i+u_j\le0.
\]

Repeated adjacent swaps sort the before-center prefix in nonincreasing weight order without increasing cost. ∎

### Theorem 9.2: H1 has exact depth projection on stars

For every star \(K_{1,d}\), every H1-feasible first-hit system has a depth vector in \(\operatorname{conv}(\text{true star STT depth vectors})+\mathbb R_{\ge0}^{d+1}\). Equivalently, some convex combination of true star STT depth vectors is coordinatewise no larger than the H1 depth vector. Consequently H2 and every higher \(H_k\) also have exact depth projection on stars.

### Proof

Fix a nonnegative weight vector. Let the center weight be \(\alpha\). Relabel leaves so that

\[
u_1\ge u_2\ge\cdots\ge u_d\ge0.
\]

For each leaf \(i\), define

\[
x_i=z[O_{\{i\}},0],
\qquad
y_i=z[O_{\{i\}},i]=1-x_i.
\]

The depth projection gives the weighted objective

\[
\alpha D_0+\sum_{j=1}^d u_jD_j
=
\alpha\sum_i z[O_{\{i\}},i]
+
\sum_j u_jz[O_{\{j\}},0]
+
\sum_{i\ne j}u_jz[O_{\{i,j\}},i].
\]

The first term accounts for leaves preceding the center on paths \(i-0\). The second term accounts for the center preceding leaf \(j\). The third term accounts for leaf \(i\) preceding leaf \(j\) on the path \(i-0-j\).

For a pair \(i<j\), set

\[
a=z[O_{\{i,j\}},i],\qquad
b=z[O_{\{i,j\}},j],\qquad
c=z[O_{\{i,j\}},0].
\]

H1 gives

\[
a\le y_i,\qquad b\le y_j,\qquad c\le x_i=1-y_i,\qquad c\le x_j=1-y_j,
\]

and simplex gives

\[
a+b+c=1.
\]

Therefore

\[
a+b=1-c\ge \max(y_i,y_j).
\]

Also

\[
b=(a+b)-a\ge \max(y_i,y_j)-y_i=(y_j-y_i)_+.
\]

Since \(u_i\ge u_j\),

\[
u_ja+u_ib
=
u_j(a+b)+(u_i-u_j)b
\ge
u_j\max(y_i,y_j)+(u_i-u_j)(y_j-y_i)_+.
\]

Equivalently,

\[
u_ja+u_ib
\ge
u_jy_i+u_i(y_j-y_i)_+.
\tag{1}
\]

Summing (1) over all \(i<j\), every H1-feasible point has weighted objective at least

\[
F(y)=
\alpha\sum_i y_i
+
\sum_i u_i(1-y_i)
+
\sum_{i<j}\left[u_jy_i+u_i(y_j-y_i)_+\right].
\tag{2}
\]

Now define threshold sets

\[
A_t=\{i:y_i\ge t\},\qquad 0\le t\le1.
\]

For any set \(A\subseteq[d]\), let \(\tau_A\) be the true star STT that queries leaves in \(A\) in nonincreasing weight order, then queries the center, then queries all remaining leaves as singleton children. By Theorem 9.1, these are exactly the cost-minimal STTs for fixed before-center set \(A\).

Let \(f(A)\) be the cost of \(\tau_A\). Decompose \(f(A)\) into center, center-leaf, and leaf-leaf pair contributions:

\[
f(A)=
\alpha |A|
+
\sum_i u_i1_{i\notin A}
+
\sum_{i<j}g_{ij}(1_{i\in A},1_{j\in A}),
\]

where

\[
g_{ij}(0,0)=0,\quad
g_{ij}(1,0)=u_j,\quad
g_{ij}(0,1)=u_i,\quad
g_{ij}(1,1)=u_j.
\]

These cases correspond respectively to neither leaf preceding the other, \(i\) preceding \(j\), \(j\) preceding \(i\), and both preceding the center with \(i\) before \(j\) because \(u_i\ge u_j\).

Now integrate \(f(A_t)\) over \(t\in[0,1]\). The singleton terms give

\[
\int_0^1 \alpha |A_t|\,dt=\alpha\sum_i y_i
\]

and

\[
\int_0^1\sum_i u_i1_{i\notin A_t}\,dt
=
\sum_i u_i(1-y_i).
\]

For \(i<j\), the threshold lengths are:

\[
\lambda\{t:i,j\in A_t\}=\min(y_i,y_j),
\]

\[
\lambda\{t:i\in A_t,j\notin A_t\}=(y_i-y_j)_+,
\]

\[
\lambda\{t:i\notin A_t,j\in A_t\}=(y_j-y_i)_+.
\]

Thus

\[
\int_0^1 g_{ij}(1_{i\in A_t},1_{j\in A_t})\,dt
=
u_j\min(y_i,y_j)
+
u_j(y_i-y_j)_+
+
u_i(y_j-y_i)_+.
\]

If \(y_i\ge y_j\), this equals \(u_jy_i\). If \(y_j>y_i\), it equals \(u_jy_i+u_i(y_j-y_i)\). In all cases it equals the pair term in (2). Hence

\[
F(y)=\int_0^1 f(A_t)\,dt.
\]

Since \(f(A_t)\) is the cost of a true STT for every \(t\),

\[
F(y)\ge \min_A f(A)=\operatorname{OPT}_{K_{1,d}}(w).
\]

Therefore every H1-feasible point has weighted cost at least the true star optimum for every nonnegative weight vector. Since every true STT satisfies H1, equality of optimal values follows.

It remains to translate weighted-objective exactness into depth-dominance. Let \(P\) be the convex hull of true star STT depth vectors, and let

\[
P^\uparrow=P+\mathbb R_{\ge0}^{d+1}
\]

be its dominant. If an H1 depth vector \(D\) were not in \(P^\uparrow\), the separating-hyperplane theorem would give a nonnegative weight vector \(w\ge0\) such that

\[
w\cdot D<\min_{p\in P}w\cdot p,
\]

contradicting the weighted inequality just proved. Hence \(D\in P^\uparrow\).

Since H2 and all \(H_k\) are stronger than H1 but still contain all true STTs, their star depth projections are exact as well. ∎

### Corollary 9.3

The v4.4 computational target "test H2/Hk depth-projection behavior on stars" is now closed theorem-level for H1/H2/Hk on pure stars. No Codex search is needed for pure-star depth gaps.

---

## 10. Why the star proof does not extend unchanged

### Theorem 10.1

The H1 star depth-exactness theorem does not extend to all subdivided stars/spiders or all max-degree-3 trees.

### Proof

The \(U(7,3)\) topology is a subdivided 3-star with maximum degree 3. The internal/public certificate stack records an H1-feasible connected first-hit lift of the public SKZ fractional depth vector with weighted value \(59/2\), while the true optimum for the same weight vector is \(30\). Since

\[
59/2<30,
\]

H1 is not exact as a depth relaxation on this subdivided star. Therefore H1 exactness cannot extend from pure stars to all subdivided stars/spiders or all max-degree-3 trees. This argument does not address double-stars, which remain a separate active frontier. ∎

### Structural reason

The pure-star proof relies on the fact that every leaf-center branch has length 1. A threshold set \(A_t=\{i:y_i\ge t\}\) is automatically a valid before-center leaf set of a true star STT.

On a subdivided star/spider, a branch may contain several vertices. A threshold selection can choose a deeper vertex without choosing the intervening prefix toward the center. Such a set is not a valid "before-center prefix configuration" for an STT. Thus a spider theorem requires a stronger **branch-prefix coarea** argument, and H2 is the first plausible level that might impose enough path/branch compatibility.

---

## 11. DS(2,1) persistency side branch

This note is primarily about the connected first-hit hierarchy and depth projection. A related double-star reduced-functional branch currently has the following status:

> **DS(2,1) persistency.** For \(u_1\ge u_2\), every optimal face of the reduced DS(2,1) LP contains an orientation-coherent optimum with \(a_1\ge a_2\) and \(b_1\ge b_2\).

This result is certificate-backed theorem-level modulo its stated stable dependencies:

- fixed-orientation exactness;
- DS(1,1) reduced exactness;
- cross-Gamma decomposition by orientation;
- orientation-coherent fractional safety;
- comparable-profile swap;
- Codex v1 strict-heavy coverage certificate;
- Codex v2 pinned-boundary certificate.

It should not be used to claim all double-stars are solved, full H1 exactness on double-stars, or a polynomial-time STT algorithm. It is best treated as a parallel local structural theorem whose next target is \(DS(k,1)\), \(DS(2,2)\), or the invariant needed for all double-stars.

---

## 12. Current theorem-level, certificate-backed, provisional, and killed claims

### Stable theorem-level claims

1. Every STT induces first-hit variables satisfying H1 and H2.
2. The complete \(Q(T)\) formulation is exact and integral for every tree.
3. H2 is exact in full first-hit space on paths.
4. The 4-leaf star system is H2-feasible but not complete-Möbius representable, so H2 is not exact in full \(z\)-space.
5. H1/H2/Hk have exact depth projection on pure stars.

### Certificate-backed claims

1. H2 closes the SKZ \(U(7,3)\) weight-direction gap exactly for weights \([3,2,0,2,3,3,10]\): H2 optimum is \(30\).
2. The public SKZ fractional depth vector \((2,2,9/2,2,2,3/2,1/2)\) has no H2 lift.
3. The 4-leaf star obstruction satisfies simplex, H1, and H2 exactly over rational arithmetic.
4. The 4-leaf star complete-Möbius inverse has five negative masses:
   \[
   m[\{0\},0]=-1/3,
   \]
   and
   \[
   m[\{0,i\},i]=-1/12,\qquad i=1,2,3,4.
   \]
5. DS(2,1) persistency is certificate-backed theorem-level modulo its stable-dependency caveats.

### Provisional / conjectural

1. The 4-leaf full-\(z\) star obstruction likely embeds in every tree with a vertex of degree at least 4, but the cross-boundary H2 proof remains open.
2. H2 may have exact depth projection on all spiders/subdivided stars. This is the best next positive target.
3. H2 may have exact depth projection on all max-degree-3 trees. This is more ambitious and should wait for spiders/double-stars.
4. Bounded-order \(H_k\) likely fails in full \(z\)-space on high-degree stars, but this is no longer a depth-projection target for pure stars because H1 already handles pure-star depth.

### Killed / corrected / demoted

1. H1 as a general depth relaxation: killed by \(U(7,3)\).
2. H2 as a globally exact full-\(z\) formulation: killed by the 4-leaf star.
3. The 4-leaf star as a depth-projection obstruction: killed by its dominant certificate and now superseded by Theorem 9.2.
4. Pure-star depth behavior as unresolved: solved positively at H1 level.
5. "Star STTs are only center-root or one-leaf-root": false. A star STT is a leaf-prefix path, then the center, then remaining leaves.
6. Degree-at-least-4 embedding as a theorem: still demoted to provisional.
7. DS(2,1) persistency as all-double-star exactness: false/overstrong.

---

## 13. Paper-worthiness and versioning

Paper-worthiness was already reached by v4.4. The v4.5 star theorem improves the paper package because it shows that the 4-leaf full-\(z\) obstruction is not merely "not a known depth obstruction"; on pure stars, no H1/H2/Hk depth obstruction exists at all.

This sharpens the narrative:

- full \(z\)-space consistency and depth projection are genuinely different;
- H2 can fail in full \(z\)-space even on a star;
- nevertheless, the weighted optimization objective can still be exact on that entire class, already at H1;
- the first real depth battleground beyond paths is spiders/subdivided stars, not pure stars.

This is still v4.5 rather than v5 because the global architecture is unchanged. A v5 should be reserved for a spider/double-star/max-degree-3 breakthrough or a major public-overlap correction.

---

## 14. Best next theorem targets

### Target A: Spider H2 depth-projection theorem

Prove or refute:

> For every subdivided star/spider, every H2-feasible first-hit system has a depth projection in the true spider STT depth dominant, i.e. in \(\operatorname{conv}(\text{true spider STT depth vectors})+\mathbb R_{\ge0}^{V}\).

This is now the best target. It directly follows the new star theorem and the \(U(7,3)\) H1 failure.

### Target B: Double-star H2/H1 reduced exactness bridge

Use the DS(2,1) persistency theorem as a local structural input and try to extend to \(DS(k,1)\), \(DS(2,2)\), or a double-star depth theorem.

### Target C: Degree-at-least-4 full-\(z\) embedding proof

Upgrade the provisional degree-at-least-4 embedding claim for the 4-leaf full-\(z\) obstruction by proving all cross-boundary H2 cases.

### Target D: Bounded-order full-\(z\) hierarchy lower bound

Prove that for every fixed \(k\), sufficiently large stars have \(H_k\)-feasible first-hit systems with negative higher-order complete Möbius masses. This is full-\(z\), not depth.

---

## 15. Codex recommendation

No Codex task is recommended for pure stars. The star depth-projection target is now theorem-level by hand.

A decision-relevant Codex task is recommended only if the next push is spider H2:

```text
Create branch: stt-spider-h2-depth-v0

Goal:
Test and illuminate H2 depth-projection exactness on spiders/subdivided stars.

Tasks:
1. Implement exact H2 depth-projection LPs for spiders with arm lengths:
   (2,2,2), (3,2,1), (3,3,1), (2,2,2,1), and (3,2,2).
2. Compare against the true STT depth dominant.
3. For any gap, output exact rational weights, H2 depth vector, and violated dominant inequality.
4. If no gaps appear, extract dual certificates or recurring inequalities suggesting a branch-prefix coarea theorem.
5. Include U(7,3) as a regression: H1 gap should appear; H2 should close the known weight direction.
6. Produce a Markdown report and JSON certificates/artifacts.
```

This should be run only when the manual spider proof attempt stalls or needs exact counterexample/certificate support.

---

## 16. Best next prompt

```text
Continue from Frontier Note v4.5 on the connected first-hit hierarchy.

You may use the internet only to keep public-frontier and novelty statements accurate; do not turn this into a broad literature review.

Current status:
- Complete Q(T) is exact but exponential.
- H2 is exact on paths.
- H2 closes the tested SKZ U(7,3) depth-vector gap.
- H2 fails in full z-space on the 4-leaf star.
- Pure stars are now solved for depth projection: H1 already has exact depth projection on K_{1,d}.
- The H1 star proof uses a threshold/coarea representation over before-center leaf sets.
- This does not extend to subdivided stars at H1 level: U(7,3) is a subdivided 3-star/max-degree-3 obstruction to H1 depth exactness.
- H2 depth projection on spiders remains open and is now the main frontier.

Task:
Do a deep ambitious theorem push on the Spider H2 depth-projection conjecture.

Primary target:
Prove or refute:

For every subdivided star/spider, every H2-feasible first-hit system has a depth projection in the true spider STT depth dominant, i.e. in \(\operatorname{conv}(\text{true spider STT depth vectors})+\mathbb R_{\ge0}^{V}\).

Required internal passes before reporting:

Pass 1 — Audit and normalization:
- Define a spider with center 0 and arms P_1,...,P_m.
- Re-derive true spider STT structure using recursive branch-prefix choices.
- Re-derive depth projection in path first-hit variables.
- Identify precisely where the pure-star H1 proof uses branch length 1.

Pass 2 — Extraction:
- Abstract the pure-star threshold proof into a branch-prefix coarea template.
- Determine which H2 inequalities enforce prefix validity along arms and compatibility across arms.
- Try to express H2 depth lower bounds as an integral/mixture over true spider STTs.

Pass 3 — Obstruction search:
- Try manually to build a rational H2 depth counterexample on spiders with arm lengths (2,2,2), (3,2,1), (3,3,1), and (2,2,2,1).
- If a counterexample appears, give exact weights, depth vector, and violated STT-dominant inequality.
- If no counterexample appears, isolate the exact missing lemma.

Pass 4 — Extension after first conclusion:
After reaching a plausible proof, counterexample, or blocker, do not report yet. Complete:
1. a break attempt against boundary/equality cases;
2. a generalization attempt to double-stars or max-degree-3 trees;
3. a dual weighted-objective interpretation.

Report only:
- strongest theorem/proof or counterexample found;
- exact lemmas/proofs/counterexamples;
- killed or demoted routes;
- exact blocker if unresolved;
- whether this changes the need for another frontier note;
- Codex recommendation only if decision-relevant, otherwise “No Codex task recommended”;
- chat-length/handoff status;
- best next prompt for an ambitious follow-up with the same internal-pass and compact-reporting requirements.
```

---

## References and checked public sources

- Yaniv Sadeh, Haim Kaplan, Uri Zwick, *Search Trees on Trees via LP*, arXiv:2501.17563.
- Benjamin Aram Berendsohn, *Search trees on graphs*, PhD thesis, Freie Universität Berlin, 2024.
- Benjamin Aram Berendsohn, Ishay Golinsky, Haim Kaplan, László Kozma, *Fast Approximation of Search Trees on Trees with Centroid Trees*, ICALP 2023 / arXiv:2209.08024.
- Ishay Golinsky, *A study on search trees on trees*, Master's thesis, Tel Aviv University, April 2023; local thesis inspection summarized in Frontier Note v4.4.
