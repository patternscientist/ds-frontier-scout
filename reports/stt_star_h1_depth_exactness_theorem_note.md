# Theorem Note: H1 Has Exact Depth Projection on Stars

**Project:** Connected first-hit hierarchy for static search trees on trees  
**Status:** Polished theorem note for insertion into the next frontier note / paper draft  
**Convention:** root-depth-0 weighted depth throughout

## Public-boundary note

This note proves a theorem about the connected first-hit hierarchy, not about the public Golinsky/SKZ path-variable LP. Publicly, Golinsky's LP uses ordered ancestry variables and path-min linearization; SKZ study that LP, disprove its exactness, and frame stronger LP/depth-vector questions as open directions. The theorem below should be presented as an internal connected-first-hit result. It does not claim that the public SKZ/Golinsky star cases were open in this exact form, and it does not claim any polynomial-time algorithm for optimal STTs.

The theorem also does **not** contradict the audited 4-leaf star obstruction: that obstruction kills H2 exactness in full first-hit `z`-space, but it is not a depth-projection obstruction. The theorem below explains why: on stars, even H1 already has exact depth projection.

---

## 1. Exact depth projection: definition

For a family of trees \(\mathcal F\), say a relaxation has **exact depth projection** on \(\mathcal F\) if every projected depth vector lies in the upward STT depth dominant. Equivalently, for every nonnegative weighted depth objective, the relaxation optimum is no smaller than the true STT optimum.

For a fixed tree \(T\), let
\[
\mathcal D_T
=
\operatorname{conv}\{D(\tau):\tau\text{ is an STT on }T\}+\mathbb R_{\ge0}^{V(T)}.
\]
Then exact depth projection means:
\[
D(z)\in \mathcal D_T
\]
for every feasible first-hit point \(z\) in the relaxation.

---

## 2. Theorem statement

Let \(K_{1,d}\) be the \(d\)-leaf star with center \(0\) and leaves \([d]=\{1,\ldots,d\}\). Let \(z\) be any H1-feasible connected first-hit system on \(K_{1,d}\), meaning:

\[
z[I,r]\ge0,
\]
\[
\sum_{r\in I} z[I,r]=1
\]
for every connected set \(I\), and
\[
z[A,r]\le z[B,r]
\]
whenever \(B\subseteq A\) are connected and \(r\in B\).

Define the root-depth-0 depth projection by
\[
D_v(z)=\sum_{u\ne v} z[P(u,v),u],
\]
where \(P(u,v)\) is the vertex set of the unique path from \(u\) to \(v\).

**Theorem.** For every \(d\)-leaf star \(K_{1,d}\), every H1-feasible connected first-hit system projects to the STT depth dominant:
\[
D(z)
\in
\operatorname{conv}\{D(\tau):\tau\text{ is a star STT}\}+\mathbb R_{\ge0}^{d+1}.
\]
Equivalently, for every nonnegative weight vector \((\lambda,a_1,\ldots,a_d)\), where \(\lambda\) is the center weight and \(a_i\) is the weight of leaf \(i\),
\[
\lambda D_0(z)+\sum_{i=1}^d a_iD_i(z)
\ge
\min_{\tau\text{ star STT}}
\left(\lambda D_0(\tau)+\sum_{i=1}^d a_iD_i(\tau)\right).
\]

Consequently, H1 has exact depth projection on all stars. Since H2 and every stronger \(H_k\) relaxation add constraints to H1, H2 and all stronger \(H_k\) relaxations also have exact depth lower envelope on stars.

---

## 3. Star STTs and their depth vectors

### Lemma 3.1: star STTs are ordered leaf prefixes followed by the center

Every STT on a \(d\)-leaf star has the form
\[
\pi_1,\pi_2,\ldots,\pi_k,\;0,\;\text{then all remaining leaves as singleton children},
\]
where \((\pi_1,\ldots,\pi_k)\) is an ordered list of distinct leaves and \(0\le k\le d\). Conversely, every such ordered-prefix construction is a valid STT.

**Proof.** In any connected star subproblem, either the chosen root is the center or it is a leaf. If the chosen root is a leaf, deleting it leaves a smaller connected star with the same center and the remaining leaves. Thus leaves may be queried repeatedly before the center. Once the center is queried, deleting it disconnects every remaining leaf into a singleton component, so all remaining leaves become singleton children of the center. This proves the characterization, and the converse construction is immediate. ∎

### Depth vector formula

For a prefix \((\pi_1,\ldots,\pi_k)\), the root-depth-0 depth vector is:
\[
D_0=k,
\]
\[
D_{\pi_j}=j-1\qquad(1\le j\le k),
\]
and for leaves outside the prefix,
\[
D_i=k+1.
\]

Thus, for center weight \(\lambda\ge0\) and leaf weights \(a_i\ge0\), the weighted cost of prefix \((\pi_1,\ldots,\pi_k)\) is
\[
C(\pi,k)
=
\lambda k
+
\sum_{j=1}^{k}(j-1)a_{\pi_j}
+
(k+1)\sum_{i\notin\{\pi_1,\ldots,\pi_k\}}a_i.
\]

For fixed \(k\), the optimal prefix consists of the \(k\) heaviest leaves, queried in nonincreasing weight order. Relabel the leaves so that
\[
a_1\ge a_2\ge\cdots\ge a_d.
\]
Then the true star-STT optimum is
\[
\operatorname{OPT}_{\star}(\lambda,a)
=
\min_{0\le k\le d}
\left[
\lambda k
+
\sum_{j=1}^{k}(j-1)a_j
+
(k+1)\sum_{j>k}a_j
\right].
\]

The exchange argument is straightforward: within the prefix, smaller depth coefficients should be assigned to larger weights; outside the prefix, every leaf has coefficient \(k+1\), which is larger than every prefix coefficient \(0,1,\ldots,k-1\), so the \(k\) prefix leaves should be the \(k\) heaviest leaves.

---

## 4. H1 variables and projected depths on a star

For each leaf \(i\), define
\[
p_i=z[\{0,i\},i].
\]
Thus
\[
z[\{0,i\},0]=1-p_i.
\]

For distinct leaves \(i,j\), define
\[
y_{j,i}=z[\{0,i,j\},j].
\]
This is the first-hit probability that leaf \(j\) is first on the connected path set \(\{j,0,i\}\), contributing to the depth of leaf \(i\).

The projected center depth is
\[
D_0
=
\sum_{i=1}^d z[P(i,0),i]
=
\sum_{i=1}^d z[\{0,i\},i]
=
\sum_{i=1}^d p_i.
\]

The projected depth of leaf \(i\) is
\[
D_i
=
z[\{0,i\},0]
+
\sum_{j\ne i}z[\{0,i,j\},j],
\]
so
\[
D_i
=
(1-p_i)+\sum_{j\ne i}y_{j,i}.
\]

---

## 5. H1 triple constraints

Fix distinct leaves \(i,j\). In the connected triple \(\{0,i,j\}\), write
\[
y_i=z[\{0,i,j\},i]=y_{i,j},
\]
\[
y_j=z[\{0,i,j\},j]=y_{j,i},
\]
and
\[
c=z[\{0,i,j\},0].
\]

By simplex,
\[
y_i+y_j+c=1.
\]

By H1 heredity for the leaf roots,
\[
y_i\le p_i,
\]
and
\[
y_j\le p_j.
\]
By H1 heredity for the center root,
\[
c\le z[\{0,i\},0]=1-p_i,
\]
and
\[
c\le z[\{0,j\},0]=1-p_j.
\]
Since \(c=1-y_i-y_j\), these imply
\[
y_i+y_j\ge p_i
\]
and
\[
y_i+y_j\ge p_j.
\]
Therefore
\[
y_i+y_j\ge \max(p_i,p_j).
\]

These are the only H1 inequalities used below.

---

## 6. Pairwise lower bound

Assume \(i<j\), so \(a_i\ge a_j\). We prove:
\[
a_i y_{j,i}+a_j y_{i,j}
\ge
 a_jp_i+a_i(p_j-p_i)_+.
\]
Recall that \(y_{i,j}=y_i\) and \(y_{j,i}=y_j\).

If \(p_i\ge p_j\), then \(y_i+y_j\ge p_i\), and since \(a_i\ge a_j\),
\[
a_i y_j+a_j y_i
\ge
 a_j(y_i+y_j)
\ge
 a_jp_i.
\]
In this case \((p_j-p_i)_+=0\), so the desired inequality follows.

If \(p_j>p_i\), then \(y_i+y_j\ge p_j\) and \(y_i\le p_i\). Therefore
\[
a_i y_j+a_j y_i
=
 a_i(y_i+y_j)-(a_i-a_j)y_i
\]
\[
\ge
 a_i p_j-(a_i-a_j)p_i
=
 a_jp_i+a_i(p_j-p_i).
\]
This is the desired inequality.

Thus, for every \(i<j\),
\[
a_i y_{j,i}+a_j y_{i,j}
\ge
 a_jp_i+a_i(p_j-p_i)_+.
\]

---

## 7. Lower-bound the H1 weighted objective

Let
\[
L
=
\lambda D_0+
\sum_{i=1}^d a_iD_i
\]
be the weighted depth objective of the H1 point.

Using the depth formulas,
\[
L
=
\lambda\sum_i p_i
+
\sum_i a_i(1-p_i)
+
\sum_{i<j}\left(a_i y_{j,i}+a_j y_{i,j}\right).
\]

Applying the pairwise lower bound gives
\[
L\ge \Phi(p),
\]
where
\[
\Phi(p)
=
\sum_i a_i
+
\lambda\sum_i p_i
-
\sum_i a_i p_i
+
\sum_{i<j}a_jp_i
+
\sum_{i<j}a_i(p_j-p_i)_+.
\]

---

## 8. Layer-cake / threshold-set representation

For \(t\in[0,1]\), define the threshold set
\[
S_t=\{i:p_i\ge t\}.
\]
Then
\[
p_i=
\int_0^1 \mathbf 1_{\{i\in S_t\}}\,dt,
\]
and
\[
(p_j-p_i)_+
=
\int_0^1 \mathbf 1_{\{j\in S_t,\ i\notin S_t\}}\,dt.
\]

For each subset \(S\subseteq[d]\), let \(C(S)\) be the cost of the star STT that queries the leaves of \(S\) before the center, in increasing index order, then queries the center, after which all leaves outside \(S\) become singleton children of the center. Since indices are sorted by nonincreasing weight, this is the decreasing-weight order on \(S\).

For any \(S\subseteq[d]\), this STT has cost
\[
C(S)
=
\lambda |S|
+
\sum_{h\in S}(\operatorname{rank}_S(h)-1)a_h
+
(|S|+1)\sum_{h\notin S}a_h.
\]

Subtracting the baseline \(\sum_h a_h\), we get
\[
C(S)-\sum_h a_h
=
\lambda |S|
-
\sum_{h\in S}a_h
+
\sum_{\substack{i<j\\ i\in S}}a_j
+
\sum_{\substack{i<j\\ j\in S,\ i\notin S}}a_i.
\]

Indeed, if \(h\in S\), its coefficient above the baseline is
\[
(\operatorname{rank}_S(h)-1)-1
=
\#\{i\in S:i<h\}-1,
\]
which is produced by the term \(-a_h\) plus one copy of \(a_h\) for each selected earlier index. If \(h\notin S\), its coefficient above the baseline is \(|S|\), produced by one copy for each selected index either before or after \(h\) in the two double sums.

Using the layer-cake identities, this gives exactly
\[
\Phi(p)=\int_0^1 C(S_t)\,dt.
\]

For every \(t\), \(C(S_t)\) is the cost of a true star STT. Hence
\[
C(S_t)\ge \operatorname{OPT}_{\star}(\lambda,a)
\]
for every \(t\). Therefore
\[
L\ge \Phi(p)
=
\int_0^1 C(S_t)\,dt
\ge
\operatorname{OPT}_{\star}(\lambda,a).
\]

Thus no nonnegative weighted depth objective over H1 can beat the true star-STT optimum.

---

## 9. Dominant membership

Let
\[
\mathcal D_\star
=
\operatorname{conv}\{D(\tau):\tau\text{ a star STT}\}+\mathbb R_{\ge0}^{d+1}
\]
be the star STT depth dominant.

We have proved that for every nonnegative weight vector \(w=(\lambda,a_1,\ldots,a_d)\),
\[
w\cdot D(z)
\ge
\min_{x\in\mathcal D_\star}w\cdot x.
\]

If \(D(z)\notin\mathcal D_\star\), the separating hyperplane theorem gives a vector \(w\) and scalar \(\alpha\) such that
\[
w\cdot D(z)<\alpha\le w\cdot x
\]
for every \(x\in\mathcal D_\star\). Since \(\mathcal D_\star\) is upward closed, \(w\) must be componentwise nonnegative: otherwise, moving any point of \(\mathcal D_\star\) far enough in a coordinate with negative \(w\)-coefficient would violate the lower separation bound. This contradicts the nonnegative-objective inequality just proved.

Thus
\[
D(z)\in\mathcal D_\star.
\]

So H1 has exact depth projection on all stars, and therefore H2 and every stronger \(H_k\) relaxation have exact depth lower envelope on all stars. ∎

---

## 10. Frontier-note patch list

### Step-back assessment

Replace the unresolved star-depth bullet with:

> **Stars are depth-settled.** H1 already has exact depth projection on every star. Therefore H2 and all stronger \(H_k\) relaxations also have exact depth lower envelope on stars. This sharply separates the audited 4-leaf star full-\(z\) obstruction from depth-projection behavior.

Update the strategic conclusion to:

> H2 is useful but not generally exact in full \(z\)-space. However, its depth behavior is stronger on stars than previously known: the star depth projection is already exact at H1. The next depth frontier is not stars but almost-stars / edge-diameter-3 trees.

### Star section

After the audited 4-leaf star obstruction, add a new theorem subsection:

> **Star depth theorem.** Although the 4-leaf star kills H2 exactness in full first-hit space, it does not produce a depth obstruction. In fact, no star can: H1 has exact depth projection on every \(d\)-leaf star.

Insert the theorem and proof from this note.

Revise:

> The 4-leaf star obstruction is not a depth-projection obstruction.

into:

> The 4-leaf star obstruction is not a depth-projection obstruction, and the star depth theorem shows this is not an accident: every H1/H2 star depth vector lies in the STT dominant.

### Theorem target section

Remove “H2/Hk depth-projection behavior on stars” from provisional targets.

Replace it with:

> **Edge-diameter-3 / almost-star depth projection.** Since stars are H1-depth-exact but the SKZ long-star kills H1 generally, the next natural class is almost-stars / edge-diameter-3 trees. The key question is whether H2 supplies missing depth-level consistency beyond H1 on the first nontrivial branching/path hybrid classes.

Keep bounded-order \(H_k\) lower bounds on stars, but explicitly mark them as **full-\(z\)** lower bounds, not depth-projection lower bounds.

### Computational target section

Replace star-depth testing as theorem-scouting with regression only:

> **Star regression only.** Further star-depth random testing is unnecessary as evidence for the theorem. Keep small star tests as regression checks for code and as examples for the paper.

Promote:

> **Almost-star / edge-diameter-3 depth tests.** Test H1/H2 depth projection on double-stars, subdivided stars, and two-center stars with structured objectives.

### Paper outline

Update the paper outline to:

1. Public STT / Golinsky / SKZ context.
2. Connected first-hit hierarchy \(H_1,H_2,H_k,H_\infty\).
3. Complete \(Q(T)\) formulation: exact/integral but exponential.
4. Projection to \(X/Z/D\) and relationship to public path-variable constraints.
5. H2 exactness on paths.
6. **H1 depth exactness on stars.**
7. H2 exact-certified exclusion of the SKZ \(U(7,3)\) public fractional depth vector.
8. 4-leaf star full-\(z\) obstruction: H2 is not globally exact in first-hit space.
9. Open directions: almost-stars / edge-diameter-3 trees, bounded-order full-\(z\) hierarchy lower bounds, and depth projection beyond stars.

### Killed / demoted / stable claims

Add to stable theorem-level claims:

> H1 has exact depth projection on all stars. Consequently H2 and every \(H_k\) have exact depth lower envelope on stars.

Remove from provisional claims:

> H2/Hk depth-projection behavior on stars is unresolved.

Add to killed/demoted claims:

> Star-depth random testing as a frontier-pushing task: demoted to regression only. The theorem settles the star depth question.

Keep:

> H2 as globally exact full-\(z\): killed by the 4-leaf star.

Keep:

> H2 as globally exact depth relaxation: still open; not killed by stars.

---

## 11. What becomes unnecessary

Further star-depth random/objective testing is unnecessary except as code regression or paper-example generation. The symmetric star reduction remains useful as intuition and as a computational sanity check, but it is not the proof route for arbitrary weights because symmetrization does not preserve nonsymmetric objectives.

The next depth-focused frontier should move to almost-stars / edge-diameter-3 trees.

---

## 12. Next Codex task recommendation

```text
Create branch: stt-almost-star-depth-projection-v0

Context:
We now have a theorem: H1 already has exact depth projection on every star. Star-depth testing should be treated as regression only. The next depth-projection frontier is almost-stars / edge-diameter-3 trees.

Tasks:
1. Add regression tests for the star theorem:
   - for d-leaf stars in feasible ranges;
   - for structured and random nonnegative weights;
   - compare H1 and H2 depth optima against the closed-form ordered-prefix STT formula.
   These tests are regression checks, not theorem evidence.

2. Implement edge-diameter-3 / almost-star families:
   - double-stars: two centers joined by an edge, each with leaves;
   - subdivided stars with one extra layer;
   - small brooms and two-arm stars that interpolate between paths and stars.

3. For each topology, compute:
   - true STT optimum by enumeration / complete Q(T);
   - H1 depth optimum;
   - H2 depth optimum;
   - optionally H3 where feasible.

4. Use structured objectives first:
   - one heavy branch;
   - two heavy branches on same side;
   - two heavy branches on opposite sides;
   - center-heavy;
   - asymmetric heavy leaves;
   - sorted small-integer weights.

5. Produce exact rational certificates for any H1/H2 depth gap.

6. If H1 fails but H2 succeeds on a minimal almost-star, extract the active H2 inequalities and report a candidate theorem pattern.

7. Keep full-z failures separate from depth-projection failures.
```

---

## 13. Next theorem-pushing prompt

```text
We proved the star theorem: H1 already has exact depth projection on all stars, by a pairwise H1 inequality plus layer-cake decomposition into ordered-prefix star STTs.

Now attack the next depth-theorem frontier: almost-stars / edge-diameter-3 trees.

Do a theory-first attack, not a broad computation.

Goals:
1. Define a clean almost-star family, preferably double-stars: two centers joined by an edge, with leaves attached to each center.
2. Characterize exact STT depth vectors or at least derive a normal form for optimal STTs under nonnegative weights.
3. Determine whether the star layer-cake proof generalizes:
   - identify the analogues of p_i and pair/triple variables;
   - find the H1 inequalities that still suffice;
   - identify the first place where H1 fails and H2 may be needed.
4. Try to prove one of:
   A. H1 depth exactness for double-stars;
   B. H2 depth exactness for double-stars;
   C. a concrete H1 depth counterexample on a double-star that H2 plausibly fixes.
5. Do not stop at a first lemma. If a reduction is found, push it to a theorem or to a precise obstruction.
6. If a proof stalls, specify exactly what Codex should compute next: topology, weight family, variables to extract, and certificate type.
7. Keep full-z exactness separate from depth-projection exactness throughout.
```

---

## References

- Yaniv Sadeh, Haim Kaplan, Uri Zwick, *Search Trees on Trees via LP*, arXiv:2501.17563. https://arxiv.org/abs/2501.17563
- Ishay Golinsky, *A study on search trees on trees*, Master's thesis, Tel Aviv University, April 2023. Inspected in project as uploaded PDF.
- Internal project source: Frontier Note v4.4, `stt_first_hit_hierarchy_frontier_note_v4_4.md`.
- Internal project source: Codex report `stt_star_depth_projection_v0.md`.
