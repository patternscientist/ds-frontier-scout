# Frontier Note v5.4.1: Patched Unified Overview of the Connected First-Hit STT Program

**Date:** 2026-05-18  
**Patch date:** 2026-05-18/19  
**Project:** AI and Data Structures / static search trees on trees  
**Intended repo path:** `reports/frontier_note_v5_4_1_unified_project_overview.md`  
**Audience:** mathematically mature AI and Lean club members who have not been following the STT/Golinsky-SKZ/connected-first-hit work.  
**Status:** club-facing synthesis and provenance overview, patched after Claude red-team audit v2. This document introduces no new theorem claims.

## TL;DR

The public problem is to optimize **static search trees on trees**: given a tree topology and nonnegative vertex weights, find a recursive search tree minimizing weighted depth. The public Golinsky/SKZ LP route does **not** give an exact global formulation, though public work leaves open stronger formulations, dual methods, and special topological regimes.

This project studies an internal **connected first-hit hierarchy**. The complete connected first-hit/Mobius formulation `Q(T)` is exact and integral for every tree, but exponential. The low-order relaxations H1, H2, ... are attempts to capture useful parts of that exact formulation.

Current theorem-level internal results:

1. `Q(T)` is exact and integral, but exponential.
2. H2 is exact in full first-hit space on paths.
3. H1/H2/Hk have exact depth projection on pure stars.
4. **v5.3 theorem:** H1 has exact depth projection on `DS(k,1)` for every `k >= 1`.

Current theorem-level obstruction guardrails:

1. H1 fails as a general depth relaxation on the public `U(7,3)` subdivided-star example.
2. H2 fails as a complete full-`z` first-hit formulation on the 4-leaf star, even though this is not a pure-star depth-projection obstruction.

Current certificate-backed finite results:

1. DS(2,2) H1 full-objective depth inclusion is checked over the six-vertex topology by a 943-blocker dual-certificate atlas.
2. DS(2,2) simplex-augmented packet-conic closure is checked over 302 leaf-swap atlas orbit representatives; the raw `Sigma` bookkeeping atoms are essential.
3. DS(3,2) packet-window closure is checked for all nonzero weights in `{0,1,2}^7`.
4. DS(4,2) packet-window closure is checked for all nonzero weights in `{0,1}^8`.

Current public-LP bridge status: **open, not closed**. The scalar/proper-subset and proxy routes have been killed or demoted in their audited scopes; the full residual `ell_ij` mixed-support theorem remains a live open target, and no checked artifact in this project closes or refutes that residual theorem.

Current OpenEvolve/list-update status: **side-lane infrastructure only**. List-update is the recommended zero-money local-model experiment because it has a small mutable policy object and cheap exact feedback, but no autonomous policy discovery has been achieved.

## 1. Public problem: static search trees on trees

Let `T=(V,E)` be a finite tree. A **static search tree on a tree** (STT) is defined recursively:

1. choose a root vertex `r` in the current connected tree;
2. delete `r`;
3. recurse independently on each connected component left after deleting `r`.

The resulting rooted search tree has the same vertex set `V`. For a search tree `tau`, let `d_tau(v)` be the number of strict ancestors of `v`; this project uses the **root-depth-0** convention. For nonnegative weights `w_v`, the weighted depth objective is

```math
\operatorname{cost}_w(\tau)=\sum_{v\in V} w_v d_\tau(v).
```

The exact optimization problem is:

> Given a tree `T` and weights `w >= 0`, find an STT `tau` minimizing `cost_w(tau)`.

This generalizes the classical binary-search-tree/BST setting from paths to arbitrary tree topologies. Paths are the one-dimensional case. Stars, spiders, and double-stars are the first meaningful families beyond paths.

## 2. Public frontier and why this project exists

The public Golinsky/SKZ line studies an LP relaxation for optimal STTs. Sadeh--Kaplan--Zwick refute Golinsky's conjecture that this LP gives an extended formulation for the convex hull of STT depth vectors, enumerate all tree topologies up to 8 vertices, and list directions toward the polynomial-time exact-optimization question [1]. Berendsohn's thesis records that no polynomial-time exact algorithm is known for optimal static search trees on graphs, even when the underlying graph is a tree [2]. Berendsohn--Golinsky--Kaplan--Kozma give centroid-tree approximation structure, not exact optimization [3].

SKZ Section 6, Open Question 5(b) highlights edge-diameter-3 / almost-star families as a natural open region between paths, pure stars, and general trees. The `DS(k,1)` theorem below lives inside that region as the one-right-leaf subfamily; it should be read as a partial positive answer for that specific internal H1 hierarchy target, not as an all-almost-star theorem.

The public status imposes four guardrails:

1. We should **not** claim a polynomial-time exact STT algorithm.
2. We should **not** claim a compact exact extended formulation for all trees.
3. We should **not** treat star exactness or fixed topologies with at most 8 vertices as automatically new public territory.
4. We should **not** identify this project's internal H1/H2/Hk hierarchy with the public Golinsky/SKZ LP.

The project exists because the public LP failure does not rule out stronger or different formulations. The connected first-hit hierarchy is one such internal formulation family: it keeps track of which vertex is first hit inside connected vertex sets, then asks how much of the exact first-hit consistency structure can be recovered at low order.

## 3. Internal framework: connected first-hit variables and H1/H2/Hk

For a connected set `I` of vertices and an STT `tau`, define

```math
\rho_\tau(I)=\text{the first vertex of } I \text{ queried by } \tau.
```

For a distribution over STTs, define connected first-hit variables

```math
z[I,r]=\Pr(\rho_\tau(I)=r),\qquad I\in \operatorname{Conn}(T),\quad r\in I.
```

The depth projection is

```math
D_v(z)=\sum_{u\ne v} z[P(u,v),u],
```

where `P(u,v)` is the vertex set of the unique path from `u` to `v`. For a deterministic STT, `u` is an ancestor of `v` exactly when `u` is first on `P(u,v)`, so this projection recovers ordinary STT depths.

### H1

H1 consists of simplex/nonnegativity rows and heredity:

```math
z[I,r]\ge 0,
\qquad
\sum_{r\in I} z[I,r]=1
```

for each connected `I`, and

```math
z[A,r]\le z[B,r]
```

whenever `B subset A` are connected and `r in B`.

Intuition: if `r` is first in a larger connected set, then it is first in any connected subset containing `r`.

### H2

H2 adds a second-order consistency inequality. For connected `S,A,B,A union B`, with `S subset A`, `S subset B`, and `r in S`, H2 imposes

```math
z[S,r]-z[A,r]-z[B,r]+z[A\cup B,r]\ge 0.
```

Intuition: H2 is the first low-order attempt to remember intersection/union compatibility among first-hit events.

### Complete connected first-hit/Mobius formulation `Q(T)`

The complete formulation introduces Mobius variables `m[C,r] >= 0`, indexed by connected subproblems `C` and roots `r in C`, with

```math
z[I,r]=\sum_{C\supseteq I} m[C,r].
```

Substituting this into simplex gives an exact rooted-connected-subtree cover polytope `Q(T)`. This is exact and integral for every tree, but it has exponentially many connected subsets and therefore is not a polynomial-time algorithm by itself.

### Notation and terms used later in this overview

- `Conn(T)` is the family of nonempty connected vertex subsets of `T`.
- `DS(k,m)` is the double-star with centers `a,b`, edge `a-b`, `k` left leaves attached to `a`, and `m` right leaves attached to `b`. Thus `DS(k,1)` is the broom with one right leaf `r`, and `DS(2,2)` has two leaves on each side.
- `Sigma/Lambda/Gamma/Delta/Omega/Pi` denote the packet families used in the DS(2,2) simplex-augmented packet-conic atlas. They are exact rational factorization/bookkeeping atoms for a finite checked atlas; the raw `Sigma` atoms are essential bookkeeping, not a clean conceptual theorem by themselves.
- `ell_ij` denotes the residual mixed-support pair target in the public-LP bridge. The proxy modes around it have failed in audited scopes, but the actual residual `ell_ij` Farkas/certificate theorem has not been extracted or refuted.
- `SUB_T` denotes a public-LP subset/source-deletion style row indexed by a connected subset `T`; `D(S) >= delta(S)` is the scalar depth lower-bound form of the same tempting proper-subset route.
- A `b-root` branch is the public-LP Bellman/residual analysis branch in which the center `b` is the distinguished root/source case.
- `proper-subset contraction` is the audit that deletes/contracts a source and tests whether the scalar/proper-subset route survives. Its obstruction candidates demote that route; they are not public-LP counterexamples.
- `EVOLVE-block guards` are the OpenEvolve wrapper restrictions that allow mutations only inside explicitly marked code blocks, preventing generated code from changing evaluator scaffolding or tests.
- `leaf-swap atlas orbit representatives` are finite representatives after quotienting symmetric leaf swaps. Closure over these representatives is a finite certificate-backed atlas statement, not an all-`k` theorem.

## 4. Stable theorem-level internal results

These are the facts that should be carried forward as stable within the internal connected-first-hit framework. The table separates validity facts, positive exactness theorems, and obstruction theorems because conflating these is the easiest way to overclaim.

| Result | Status | Meaning | Guardrail |
|---|---|---|---|
| Every true STT induces H1 and H2 variables | Validity / definitional | H1/H2 are legitimate relaxations of true STT first-hit behavior. | Does not imply exactness of either relaxation. |
| Complete `Q(T)` formulation is exact and integral | Theorem-level | The complete connected first-hit/Mobius object captures exactly convex combinations of true STTs. | Exponential; not a compact algorithm. |
| H2 exactness on paths | Theorem-level | On paths, H2 recovers the complete first-hit space. | Path/BST case only. |
| H1/H2/Hk depth exactness on pure stars | Theorem-level | On stars, H1 already has exact depth projection; higher Hk inherit this. | Full first-hit-space exactness still differs from depth-projection exactness. |
| H1 depth exactness on `DS(k,1)` for every `k >= 1` | Theorem-level, v5.3 | First parametric positive theorem beyond paths and pure stars in this internal hierarchy. | Not public LP exactness; not DS(k,2), all double-stars, all spiders, or all max-degree-3 trees. |
| H1 failure on public `U(7,3)` | Theorem-level obstruction carried from v4.5/v5.3 | H1 is not a general depth relaxation for subdivided stars/spiders/max-degree-3 trees. | Does not refute the `DS(k,1)` theorem and does not decide H2 on spiders. |
| 4-leaf star full-`z` obstruction | Theorem-level obstruction carried from v4.5/v5.3 | H2 is not exact as a complete full first-hit-space formulation on stars. | This is not a depth-projection obstruction for pure stars. |

The key conceptual split is between **full first-hit-space exactness** and **depth-projection exactness**. H2 can fail in full `z`-space on a 4-leaf star while H1 still has exact depth projection on every pure star. In the 4-leaf-star obstruction, the complete-Mobius inverse has five negative masses:

```math
m[\{0\},0]=-1/3,
\qquad
m[\{0,i\},i]=-1/12\quad\text{for }i=1,2,3,4.
```

The `U(7,3)` obstruction is the corresponding warning on the H1 side: the positive `DS(k,1)` theorem sits next to a known H1 failure for general subdivided-star/spider/max-degree-3 behavior. This is why the theorem is valuable but narrow.

## 5. Main v5.3 theorem: `DS(k,1)` H1 depth exactness

`DS(k,1)` is the double-star broom with centers `a,b`, edge `a-b`, left leaves `l_1,...,l_k` attached to `a`, and one right leaf `r` attached to `b`.

The v5.3 theorem says:

```math
\text{For every } k\ge 1,\text{ every H1-feasible depth vector on }DS(k,1)
\text{ lies in }
\operatorname{conv}(\mathrm{STTDepth}(DS(k,1)))+\mathbb R_{\ge0}^V.
```

Equivalently, for every nonnegative weight vector,

```math
\min_{z\in H1(DS(k,1))} w\cdot D(z)
=
\min_{\tau\in STT(DS(k,1))} w\cdot D(\tau).
```

The equivalence between the dominance form and the cost-equality form is by separating hyperplanes for the closed dominant

```math
\operatorname{conv}(\mathrm{STTDepth}(DS(k,1)))+\mathbb R_{\ge0}^V.
```

If a relaxed depth vector lay outside this dominant, a nonnegative weight vector would separate it from all true STT depth vectors, contradicting weighted-objective equality.

This is a theorem-level internal connected-first-hit result. It is not a theorem about the public Golinsky/SKZ LP. It is best framed as a partial positive result on the one-right-leaf subfamily of the edge-diameter-3 / almost-star region highlighted in SKZ Open Question 5(b), not as an all-almost-star or all-double-star theorem.

## 6. High-level proof idea for the `DS(k,1)` theorem

At a glance: the proof decomposes the right path `a-b-r` into five H1 atoms, uses pure-star coarea to turn left-leaf fractional data into threshold sets, couples the two by a Monge/slope-chain transport rule, compresses the only remaining overlap terms to a three-cap leaf-local inequality, and closes that inequality by a finite symbolic certificate. The final envelope is then explicitly refined into a finite convex average of true `DS(k,1)` schedules.

The proof is best understood as an optimal-transport/coarea argument glued to a finite cap certificate.

### 6.1 Right-path atoms

The right side `a-b-r` has a small H1 path system. Its behavior can be decomposed into five nonnegative atom masses:

```text
B, sB, RBs, qB, ABq.
```

These atoms are local right-path atoms. They are not automatically full global schedule states once left leaves are present; the proof uses them through an H1-certified transport envelope.

### 6.2 Fixed-right-atom schedule formula

For each right atom `T` and each left-leaf set `S`, let `f_T(S)` be the minimum true STT cost among schedules with right atom `T` and exactly the leaves in `S` ancestral to `a`. The audited fixed-atom formula is

```math
f_T(S)=c_T+\sum_{i\in S}d_i^T-\sum_{\{i,j\}\subseteq S}\max(u_i,u_j).
```

The important point is that the pair correction is independent of the right atom. The right atom only changes the empty cost `c_T` and singleton increments `d_i^T`.

### 6.3 Pure-star coarea on the left leaves

For each left leaf, H1 gives a threshold variable `y_i`. Define

```math
S_t=\{i:y_i\ge t\},\qquad 0\le t\le 1.
```

As in the pure-star theorem, integrating over these threshold sets converts a fractional left-leaf profile into a convex average over honest leaf-prefix configurations.

### 6.4 Slope-chain / Monge transport

The singleton increments across the five right atoms have a monotone slope order:

```text
sB <= B <= RBs <= qB = ABq.
```

This gives a Monge uncrossing principle: lower-slope atoms should be paired with larger threshold sets. Hence the optimal right-atom/left-threshold coupling is comonotone.

This is the transport heart of the proof. It prevents the right-path fractional data and the left-leaf coarea data from being coupled adversarially in a way that would beat all true schedules.

### 6.5 Three-cap basis and four cap regions

After comonotone coupling, all singleton-overlap terms can be written using three cap basis functions:

```text
min(y_i, s-B),   min(y_i, s),   min(y_i, R+B).
```

The five right-path atoms collapse to this three-cap basis because the singleton increments `d_i^{qB}` and `d_i^{ABq}` are equal for every leaf, so the `qB`/`ABq` split cancels from the singleton-overlap formula. The three cap thresholds `s-B`, `s`, and `R+B` cut `[0,1]` into four cap regions; the leaf-local certificate verifies the residual inequality separately in those four regions. Thus “four-cap identities” below refers to the four regions, not to a fourth basis function.

This is the point at which a high-dimensional-looking fractional problem collapses to a leaf-local inequality with a small set of cap statistics.

### 6.6 Leaf-local cap certificate

The remaining residual inequality is reduced to a universal one-leaf inequality. This is certified in v5.3 by a finite fan/ray table and primitive-ray/four-region identities, with a companion checker:

```powershell
python scripts/dsk1_leaf_local_cap_certificate_check.py
```

Expected output:

```text
ok: corrected fan and primitive-ray certificates verified
```

The checker requires `sympy`; if needed, run:

```powershell
python -m pip install sympy
```

The cap lemma has a human proof in v5.3 §9. The script is a regression check for the finite symbolic certificate, not a replacement for that proof.

### 6.7 Finite convex-average close

The final step shows that the optimal-transport envelope is literally a finite convex average of true `DS(k,1)` schedules. The thresholds `S_t` change only at finitely many values `y_i`, and the right-atom intervals are finite. Refining these partitions gives cells `J_{T,S}`. On each positive cell choose a true schedule realizing `f_T(S)`. Therefore the envelope cost is

```math
\sum_{T,S} |J_{T,S}|\,\operatorname{cost}_w(\tau_{T,S}),
```

with nonnegative coefficients summing to 1. This proves the H1 objective is at least the true optimum; the opposite inequality is automatic because every true STT induces H1 variables.

### 6.8 Forbidden-tool audit and endpoint warning

The proof uses only H1 nonnegativity/simplex/heredity, true STT schedule enumeration for fixed right atoms, pure-star coarea available at H1 level, slope-chain Monge uncrossing, and the explicit leaf-local Farkas certificate. It does **not** use H2, refined-Z, path-monotonicity, mixed second differences, `Delta_B >= 0`, or public small-topology enumeration as a proof step.

The architecture does not obviously generalize to `DS(k,m)` with `m > 1`: a longer or bushier right side introduces a larger atom fan and likely more cap statistics. Thus `DS(k,1)` is best read as a meaningful endpoint and proof mechanism, not as a trivial template for all double-stars.

## 7. Certificate-backed finite double-star / packet-window results

These are strong checked finite artifacts, but they must not be promoted into all-`k` theorems.

### 7.1 DS(2,2) depth inclusion and packet-conic closure

The DS(2,2) lane has two important finite/certificate-backed components.

First, the depth-inclusion certificate verifies the H1 depth-vector inclusion over the checked six-vertex DS(2,2) topology. The provenance manifest records:

```text
214 true schedules
214 depth vectors
943 blocker vertices
943 dual certificates
```

Second, the simplex-augmented packet-conic closure report shows that all 302 leaf-swap atlas orbit representatives factor exactly into the augmented packet basis

```text
Sigma / Lambda / Gamma / Delta / Omega / Pi
```

plus a nonnegative residual. The factorization data are exact rational artifacts; floating-point simplex was used only to locate candidate LP bases.

Guardrail: the raw `Sigma` atoms are bookkeeping. The five-packet basis without `Sigma` fails on 287 of the 302 representatives. Therefore the result is an exact finite DS(2,2) atlas/certificate, not a clean conceptual all-`k` packet theorem.

Verification commands:

```powershell
python -m src.ds22_simplex_augmented_packet_conic --verify
python -m unittest tests.test_ds22_simplex_augmented_packet_conic
```

### 7.2 DS(3,2) and DS(4,2) packet-window hardening

The packet-window hardening report checks finite weight universes:

```text
DS(3,2): all nonzero weights in {0,1,2}^7
DS(4,2): all nonzero weights in {0,1}^8
```

Recorded counts:

```text
DS(3,2): 2186 closed weights, 1135 true schedules/depth vectors, 228 packet atoms, failures 0.
DS(4,2): 255 closed weights, 7284 true schedules/depth vectors, 456 packet atoms, failures 0.
```

Verification commands:

```powershell
python -m src.ds32_ds42_packet_window_capacity --verify
python -m pytest tests/test_ds32_ds42_packet_window_capacity.py
```

Guardrail: this does not prove DS(k,2), DS(2,m), DS(k,m), public Golinsky/SKZ LP exactness, or general STT exactness. It is finite certificate-backed evidence in exactly the declared universes.

## 8. Public-LP bridge: what was tried, what was killed, and what remains open

The public-LP bridge is not closed. The current artifacts are obstruction/correction audits, not a proof of public LP exactness.

### 8.1 Proper-subset contraction audit

The proper-subset source-deletion audit implements a corrected source-deletion formula and checks finite small-`k` b-root rays. It records obstruction candidates for the scalar/proper-subset route.

Important status:

```text
k=3: obstruction_candidate_found
k=4: obstruction_candidate_found
```

The string `obstruction_candidate_found` is the checker/report classification for the audited scalar/proper-subset route. It should not be read as “the public LP is refuted on `DS(k,1)`” or “the b-root branch is closed.” The interpretation is:

> the audited scalar/proper-subset route is not a stable proof route without an architecture correction or a stronger definition.

This demotes the `D(S) >= delta(S)` / `SUB_S`-alone route under the audited Bellman interpretation.

Verification command:

```powershell
python scripts/check_proper_subset_contraction.py
```

### 8.2 Mixed-support public-star oracle audit

The mixed-support oracle audit is an exact finite `k=3` public-star support-oracle/proxy-obstruction audit. It verifies the corrected edge-cover support oracle and finds failures for proxy modes:

```text
Mode A: root-comparisons-only mixed-support box proxy failed.
Mode B: individual SUB_T delta proxy failed.
```

The stronger residual `ell_ij` Farkas certificate was **not** extracted. Hence the full residual `ell_ij` mixed-support theorem remains open.

Verification commands:

```powershell
python scripts/check_k3_pair_antichain_chambers.py
python scripts/extract_mixed_lambda_farkas.py
python -m unittest tests.test_star_support_oracle
```

### 8.3 Current honest status of the public-LP bridge

What is known in this project:

- scalar/proper-subset routes are demoted/killed in their audited scopes;
- proxy mixed-support routes are demoted/killed in their audited finite `k=3` scope;
- the public-star support-oracle implementation is useful finite infrastructure;
- no checked artifact proves public LP exactness on `DS(k,1)`;
- no checked artifact refutes the full residual `ell_ij` theorem.

The next public-LP attempt should either attack the full residual `ell_ij` theorem directly or produce a formal no-go theorem for that residual architecture. It should not return to the killed scalar/proxy routes without a genuinely new definition.

## 9. List-update / OpenEvolve side lane

The list-update/OpenEvolve lane is not part of the STT theorem lane. It exists because the broader project also wants cheap, zero-money experiments in automated data-structure search.

The zero-money rerank asks a practical question:

> Under local-model-only constraints, where can a small coding model mutate a compact object, stay inside a guarded interface, and receive cheap dense evaluator feedback?

The current audit recommends `list_update` first because it has:

- a small mutable policy object;
- exact finite trace evaluation;
- dense ratios/regret/validity diagnostics;
- low dependency burden;
- side-branch evaluator/wrapper scaffolding already built.

The current-main strategy report says `list_update` wins both the normal weighted ranking and the infrastructure-discounted ranking, so the recommendation is not just sunk-cost momentum.

Here “non-autonomous” means the candidate was fixed or stubbed by the experimenter rather than discovered by the model; “non-discovery” means the run tested plumbing rather than producing a new policy.

What has been built in side-branch history:

| Milestone | Status |
|---|---|
| Milestone 1 | deterministic list-update evaluator scaffold accepted. |
| Milestone 2 | OpenEvolve-compatible adapter/wrapper scaffold accepted. |
| Milestone 3 | tiny run blocked by missing API credentials; no generated policy. |
| Milestone 3z | fixed-stub transport succeeded as plumbing, but was non-autonomous and non-discovery. |

What has not been achieved:

- no autonomous local-model OpenEvolve success;
- no discovered list-update policy;
- no theorem-level competitive-ratio progress;
- no reason to demote STT as the main theorem/certificate lane.

The honest next side-lane step is one real local OpenAI-compatible run through Ollama or LM Studio, preserving EVOLVE-block guards and independently re-evaluating any generated candidate.

## 10. What is beyond the public frontier

The internal contribution is not “we solved STTs.” It is more specific:

1. **Connected-first-hit formulation architecture.** The project gives an exact but exponential `Q(T)` formulation and studies principled low-order truncations.
2. **Full-space vs depth-projection separation.** The 4-leaf star shows H2 can fail in full first-hit space even though pure-star depth projection is exact already at H1.
3. **Pure-star H1 depth theorem.** H1 exactness on pure stars gives a clean coarea proof and removes pure stars as the next depth battleground.
4. **Parametric `DS(k,1)` theorem.** The v5.3 result is an all-`k` theorem for a nontrivial infinite double-star/broom family beyond paths and pure stars. It is the one-right-leaf subfamily inside the edge-diameter-3 / almost-star region highlighted by SKZ Open Question 5(b), so it is a partial positive answer there, not an all-almost-star theorem.
5. **New proof mechanism.** The `DS(k,1)` proof combines right-path atoms, pure-star coarea, Monge transport, three-cap reduction, and a finite leaf-local certificate. The proof mechanism is meaningful precisely because it does not obviously scale by rote to `DS(k,m)` with `m>1`.
6. **Finite packet-window infrastructure.** DS(2,2), DS(3,2), and DS(4,2) artifacts create a serious certificate-backed platform for testing all-`k` double-star conjectures.
7. **Sharper public-LP obstruction story.** The public-LP branch is not closed, but the project has killed or demoted several tempting scalar/proxy shortcuts and isolated the real residual mixed-support target.

## 11. What is not claimed

This section is deliberately blunt because the positive `DS(k,1)` theorem sits near genuine negative evidence: H1 already fails on the public `U(7,3)` subdivided-star example, and H2 already fails as a full first-hit-space formulation on the 4-leaf star. The point of the project is a sharp internal positive theorem plus certificate-backed finite infrastructure, not a blanket solution of neighboring graph classes.

The project does **not** claim:

1. a polynomial-time exact STT algorithm;
2. a compact exact extended formulation for all STTs;
3. public Golinsky/SKZ LP exactness on `DS(k,1)`;
4. that H1/H2/Hk are the public Golinsky/SKZ LP;
5. all-`k` DS(k,2) exactness;
6. all DS(k,m) exactness;
7. all double-stars, all spiders, or all max-degree-3 trees are solved;
8. finite DS(3,2)/DS(4,2) packet-window evidence is an all-`k` theorem;
9. proper-subset or mixed-support proxy obstruction artifacts close the public-LP bridge;
10. residual `ell_ij` mixed-support theorem is proved;
11. list-update/OpenEvolve discovered a policy;
12. list-update infrastructure is evidence for any STT theorem.

## 12. Current best next moves

### 12.1 Before club sharing

Red-team this v5.4 overview for:

- outsider readability;
- status-label discipline;
- whether “public frontier” is explained enough without turning into a literature review;
- whether the internal/public LP boundary is clear;
- whether DS(k,2) finite evidence is stated carefully enough.

### 12.2 Main theorem/certificate lane

1. Package the v5.3 leaf-local cap certificate into stable JSON/Lean-ready data, if the goal is reproducible formalization.
2. Continue DS(k,2) only with the finite-vs-all-`k` boundary explicit. The natural target is the all-`k` packet-window gluing conjecture using H1 capacity and embedded DS(2,2) atoms.
3. For public-LP, attack the full residual `ell_ij` mixed-support theorem directly, or prove a formal no-go theorem for that residual architecture. Do not spend time reanimating killed scalar/proxy routes.

### 12.3 Side-lane OpenEvolve work

Continue list-update only as side-lane infrastructure:

1. run one real local OpenAI-compatible endpoint experiment through Ollama or LM Studio;
2. reject fixed-stub transport as policy discovery;
3. preserve EVOLVE-block-only guards;
4. independently re-evaluate any generated candidate;
5. report exact model/server details, candidate classification, and test results.

## Appendix A. Provenance table

| Area | Repo artifact(s) | Status supported | Verification / guardrail |
|---|---|---|---|
| v5.4 provenance manifest | `reports/frontier_v5_4_repo_provenance_manifest.md`; `data/frontier_v5_4_repo_provenance_manifest.json` | Current source map and strict labels for v5.4 synthesis | Manifest introduces no new theorem claims; it records artifact status. |
| Baseline connected-first-hit frontier | `reports/frontier_note_v4_5_patched_connected_first_hit_hierarchy.md` | `Q(T)` exact/integral; H2 paths; pure-star H1/H2/Hk depth exactness; H1 spider obstruction; H2 full-`z` star obstruction | Guardrails: not public LP exactness; pure stars are not the spider/double-star frontier. |
| Main `DS(k,1)` theorem | `reports/frontier_note_v5_3_dsk1_h1_exactness_2026_05_17.md` | H1 depth exactness on `DS(k,1)` for every `k >= 1` | Internal connected-first-hit theorem only; not public LP exactness; not DS(k,2) or all double-stars. |
| Leaf-local cap certificate | `scripts/dsk1_leaf_local_cap_certificate_check.py` | finite symbolic support for v5.3 leaf-local cap lemma | `python scripts/dsk1_leaf_local_cap_certificate_check.py`; expected `ok: corrected fan and primitive-ray certificates verified`; requires `sympy`; regression check, not a replacement for the v5.3 human proof. |
| DS(2,2) depth inclusion | `reports/ds22_full_objective_depth_vector_cert_report.md`; `certificates/ds22_depth_inclusion_cert.json`; `src/ds22_depth_inclusion_check.py`; `tests/test_ds22_depth_inclusion.py` | finite DS(2,2) H1 depth-vector inclusion | 214 schedules, 214 depth vectors, 943 blockers/dual certificates. |
| DS(2,2) packet-conic closure | `reports/ds22_simplex_augmented_packet_conic_report.md`; `data/ds22_blocker_orbits.json`; `data/ds22_simplex_augmented_packet_factorizations.json`; `data/ds22_simplex_augmented_packet_residuals.json`; `src/ds22_simplex_augmented_packet_conic.py`; `tests/test_ds22_simplex_augmented_packet_conic.py` | finite simplex-augmented packet-conic atlas closure | 302 orbit representatives; raw `Sigma` bookkeeping essential; not all-`k`. |
| DS(3,2)/DS(4,2) packet-window hardening | `reports/ds32_ds42_packet_window_capacity_hardening_report.md`; `data/ds32_packet_window_factorizations_ternary.json`; `data/ds42_packet_window_factorizations_binary.json`; `data/ds32_ds42_packet_window_gap_witnesses.json`; `src/ds32_ds42_packet_window_capacity.py`; `tests/test_ds32_ds42_packet_window_capacity.py` | finite packet-window closure for declared weight universes | DS(3,2) `{0,1,2}^7 \setminus {0}`; DS(4,2) `{0,1}^8 \setminus {0}`; not all-`k`. |
| Proper-subset public-LP audit | `reports/proper_subset_contraction_report.md`; `data/proper_subset_contraction_k3.json`; `data/proper_subset_contraction_k4.json`; `scripts/check_proper_subset_contraction.py` | scalar/proper-subset route killed/demoted in audited finite scope | Obstruction candidates found; not public-LP closure. |
| Mixed-support public-star oracle audit | `reports/mixed_support_oracle_report.md`; `data/k3_pair_antichain_chambers.json`; `data/mixed_support_certificates.json`; `data/mixed_support_obstructions.json`; `scripts/star_support_oracle.py`; `scripts/check_k3_pair_antichain_chambers.py`; `scripts/extract_mixed_lambda_farkas.py`; `tests/test_star_support_oracle.py` | finite `k=3` support-oracle/proxy obstruction audit | Proxy routes fail; residual `ell_ij` Farkas extraction not certified; bridge remains open. |
| OpenEvolve zero-money side lane | `reports/openevolve_zero_money_candidate_rerank_v0.md`; `reports/openevolve_zero_money_candidate_rerank_v0.json` | list-update recommended as immediate local-model side lane; STT remains main theorem/certificate lane | Not policy discovery; fixed-stub is not autonomous success. |


## Appendix B. References

[1] Yaniv Sadeh, Haim Kaplan, Uri Zwick, *Search Trees on Trees via LP*, arXiv:2501.17563, 2025.

[2] Benjamin Aram Berendsohn, *Search trees on graphs*, PhD thesis, Freie Universität Berlin, 2024.

[3] Benjamin Aram Berendsohn, Ishay Golinsky, Haim Kaplan, László Kozma, *Fast Approximation of Search Trees on Trees with Centroid Trees*, ICALP 2023 / arXiv:2209.08024.

[4] Frontier Note v5.3: `reports/frontier_note_v5_3_dsk1_h1_exactness_2026_05_17.md`.

[5] Frontier v5.4 provenance manifest: `reports/frontier_v5_4_repo_provenance_manifest.md`.

## Appendix C. Suggested red-team prompt

```text
Audit the attached v5.4.1 patched unified overview for the STT connected-first-hit project.

Main task:
Check outsider readability and overclaim discipline. The document is meant for mathematically mature AI/Lean club members who do not already know STTs, Golinsky/SKZ, or the connected first-hit hierarchy.

Audit requirements:
1. Identify any place where theorem-level, certificate-backed finite, candidate/open, killed/demoted, or side-lane infrastructure status is ambiguous.
2. Check that the document does not claim public Golinsky/SKZ LP exactness, all-k DS(k,2), all DS(k,m), all double-stars, all spiders, all max-degree-3 trees, a polynomial-time exact STT algorithm, or OpenEvolve policy discovery.
3. Check whether the public problem and public frontier are clear enough for a club-facing overview without becoming a literature review.
4. Check whether the DS(k,1) proof idea is understandable at a high level without proof-dump overload.
5. Suggest minimal edits only; do not rewrite the document from scratch unless a major structural issue appears.

Return:
- major status-label risks, if any;
- readability blockers, if any;
- concrete patch suggestions;
- a final verdict: safe to share with club / safe after minor edits / needs major revision.
```
