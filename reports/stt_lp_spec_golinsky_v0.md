# STT LP Specification: Golinsky v0

Date: 2026-05-15

Internal relaxation name: `golinsky_stt_lp_v0`

## 1. Scope And Source Trail

This document specifies the first LP relaxation this repository should support
for search trees on trees (STTs). It is an implementation specification only.
It does not implement the checker and does not claim any theorem.

Primary sources consulted:

- Yaniv Sadeh, Haim Kaplan, Uri Zwick, "Search Trees on Trees via LP",
  arXiv:2501.17563, DOI `10.48550/arXiv.2501.17563`,
  https://arxiv.org/abs/2501.17563.
- The arXiv source archive for `2501.17563`, downloaded 2026-05-15 from
  https://arxiv.org/e-print/2501.17563. Files used:
  `section_preliminaries.tex`, `section_counter_example.tex`,
  `section_open_questions.tex`, `section_positive_results.tex`,
  `section_extra_results.tex`, `section_code.tex`, `reference.bib`, and the
  included `STTLP-sage-python3-source/` code.
- Source-code files inside that archive:
  `STTLP-LPs.py`, especially `construct_constraints_primal` and
  `modes_vanilla = []`; `STTLP-GraphsAndSTT.py`, especially
  `_construct_dictionaries_PRIMAL`, `betweenNodes`, `stt_to_XZD_vector`, and
  `round_to_STT`; `STTLP-HardcodedValues.py`, for hard-coded directions and
  non-integer vertices used by the paper's computational results.
- Golinsky original source: Sadeh-Kaplan-Zwick cite Ishay Golinsky,
  "A study on search trees on trees", master's thesis, Tel Aviv University,
  2023, as `GolinskyThesis`. I did not locate an accessible copy during this
  extraction. The arXiv `reference.bib` contains a commented DOI line
  `10.22028/D291-26671` adjacent to this entry, but that DOI resolves to
  Laszlo Kozma's 2016 thesis, not Golinsky's thesis. Independent verification
  against Golinsky's thesis remains a blocker before saying this is Golinsky's
  original text rather than the Sadeh-Kaplan-Zwick presentation of it.

Formulas used:

- `section_preliminaries.tex`, Definition `definition_LP_program`:
  variables, bounds, ancestry, loose-LCA, depth constraints, and objective.
- `section_preliminaries.tex`, Definition `definition_xzd_of_stt`: how an STT
  induces `(X,Z,D)`.
- `section_preliminaries.tex`, Remark `remark_depth_off_by_one`: `D_i` is one
  less than ordinary search depth.
- `section_preliminaries.tex`, Definition `definition_rounding_scheme`:
  root-rounding rule.
- `section_counter_example.tex`, Definition `definition_long_star` and Theorem
  `theorem_non_integer_optimum_long_star`: long-star topology, frequency
  vector `[3,2,0,2,3,3,10]/23`, and depth vector
  `[2,2,9/2,2,2,3/2,1/2]`.
- `section_code.tex`: the code archive is in the arXiv source, and Sage is
  required for LP/polytope operations.
- `STTLP-LPs.py`: confirms the vanilla code path and the exact inequality
  orientation used by the computational artifacts.
- `STTLP-GraphsAndSTT.py`: confirms variable indexing, strict path-between
  convention, 1-indexed source labels, and root-rounding score computation.

Completeness status:

- Complete enough to implement exact rational feasibility checking for the
  vanilla Sadeh-Kaplan-Zwick/Golinsky `X,Z,D` LP.
- Not complete enough to claim direct fidelity to Golinsky's original thesis
  until that thesis is obtained and checked.
- Not a spec for the paper's LP variants without `Z`, refined `Z`,
  exact-ancestry, exact-depth, path-monotonicity, ancestry-transitivity,
  LCA-separation, or upper-bound constraints.

## 2. LP Name And Version

Use:

```text
relaxation: "golinsky_stt_lp"
relaxation_version: "golinsky_stt_lp_v0"
```

Meaning:

- `golinsky_stt_lp_v0` is the vanilla LP in Sadeh-Kaplan-Zwick Definition
  `definition_LP_program`, with the separated `X`, `Z`, and `D` variables.
- In the arXiv source code this corresponds to `construct_constraints_primal`
  with `modes_vanilla = []`.
- It excludes all optional code modes in `ALL_PRIMAL_MODES`: `noZVariables`,
  `exactAncestryConstraints`, `exactDepthsConstraints`, `pathMonotonicity`,
  `AncestryTransitivity`, `LCAseparation`, `refinedZ`, and `upperBoundOf1`.

The name is precise enough for checker use because it fixes the variable
families, index domains, symmetry convention for `Z`, inequality/equality
status, absence of upper bounds, and the depth-offset convention.

## 3. Objects And Indexing

### Base Tree

Input is an undirected tree topology

```text
U = (V, E)
```

with `V = {0, ..., n-1}` in this repository. Sadeh-Kaplan-Zwick's code uses
1-indexed vertices `{1, ..., n}`; checker implementation must translate
source examples by subtracting 1 from vertex labels.

The tree is labeled for certificate checking. Isomorphism/canonical labels are
metadata and are not part of the LP definition.

For vertices `i != j`, let:

- `path_U(i,j)` be the unique simple path from `i` to `j`, including endpoints.
- `between_U(i,j)` be the strict interior of that path, excluding `i` and `j`.
  This is the source notation `(i <-> j)`.
- `[u <-> v)` in root rounding means the path from `u` to `v`, including `u`
  and strict interior vertices, excluding `v`.

Empty sums are zero.

### Variable Families

All LP variables are real in the mathematical LP. Proof-mode certificates in
this repository must give exact rational values.

`D` variables:

```text
D_i for every i in V.
```

`D_i` is the LP depth, i.e. the number of strict ancestors for an STT-induced
point. It is not the checker's default search depth. For an STT with root depth
1, `search_depth_T(i) = D_i^T + 1`.

`X` variables:

```text
X_ij for every ordered pair (i,j) with i,j in V and i != j.
```

Intended integer meaning: `X_ij = 1` iff `i` is an ancestor of `j` in the STT.
There is no symmetry. `X_ij` and `X_ji` are distinct variables.

`Z` variables:

```text
Z_kij for every unordered endpoint pair {i,j}, i != j,
and every k in between_U(i,j).
```

Intended integer meaning: `Z_kij = 1` iff `k` is the LCA of `i` and `j` in the
STT. The endpoint order is symmetric:

```text
Z_kij = Z_kji.
```

Implementation convention: encode `Z` by the key `(k, min(i,j), max(i,j))`.
There are no `Z` variables when `i` and `j` are adjacent, and no endpoint `Z`
variables such as `Z_iij` or `Z_jij` in `golinsky_stt_lp_v0`.

Variable counts:

```text
|D| = n
|X| = n(n-1)
|Z| = sum_{unordered {i,j}} |between_U(i,j)|
    = sum_{unordered {i,j}} (dist_U(i,j) - 1)
```

Absent-variable convention for proof-mode v0:

- A defined variable missing from a dense proof-mode LP certificate is an error.
- An undefined variable, such as `X_ii`, `Z_iij`, or `Z_kij` with
  `k notin between_U(i,j)`, is an error if supplied.
- A future sparse encoding may allow absent `X`/`Z` values to default to zero,
  but that is not part of this v0 proof-mode spec.

## 4. Constraints

All constraints below are part of `golinsky_stt_lp_v0`.

### Nonnegativity

Human statement: all LP variables are nonnegative.

Formula:

```text
D_i >= 0                         for all i in V
X_ij >= 0                        for all ordered i != j
Z_kij >= 0                       for all defined Z_kij
```

Source:

- `section_preliminaries.tex`, exposition before Definition
  `definition_LP_program`, which relaxes the variables to nonnegative reals.
  The displayed "Bounds" line explicitly lists `X` and `Z`; `D_i >= 0` also
  follows from nonnegative `X` and the depth inequality.
- `STTLP-LPs.py`, `construct_constraints_primal`, "Bounds constraints", which
  adds `variable >= 0` for every variable in the primal dictionary.

Implementation notes:

- `D_i >= 0` is redundant if all `X >= 0` and the depth constraint is enforced,
  but the arXiv code adds nonnegativity bounds to all variables. Keep it.
- No upper bound `<= 1` is present in v0. The source code has an optional
  `upperBoundOf1` mode, but it is excluded.

### Ancestry

Human statement: for each pair of vertices, either one endpoint is an ancestor
of the other, or some strict interior vertex on the base-tree path is their
LCA.

Formula, for every unordered pair `{i,j}` with `i != j`:

```text
X_ij + X_ji + sum_{k in between_U(i,j)} Z_kij >= 1.
```

For adjacent vertices, this reduces to:

```text
X_ij + X_ji >= 1.
```

Source:

- `section_preliminaries.tex`, Definition `definition_LP_program`, "Ancestry".
- `STTLP-LPs.py`, `construct_constraints_primal`, vanilla branch, loops over
  `i < j` and adds one inequality per unordered pair.

Implementation notes:

- The paper writes the quantification as `forall i,j`; the code generates one
  constraint for `i < j`, which is the nonduplicated symmetric form. Use the
  code convention.
- This is an inequality, not equality. The optional code mode
  `exactAncestryConstraints` is not in v0.

### Loose LCA

Human statement: if `k` contributes as an LCA witness for endpoints `i,j`, then
`k` must be an ancestor of both endpoints, fractionally.

Formula, for every defined `Z_kij`:

```text
Z_kij <= X_ki
Z_kij <= X_kj
```

Equivalently:

```text
X_ki - Z_kij >= 0
X_kj - Z_kij >= 0
```

Source:

- `section_preliminaries.tex`, Definition `definition_LP_program`,
  "Loosely LCA".
- `STTLP-LPs.py`, `construct_constraints_primal`, vanilla branch.

Implementation notes:

- The stronger inequality `Z_kij >= X_ki + X_kj - 1` is an optional
  `refinedZ` mode and is not in v0.
- No constraint forces `Z_kij` to equal `min(X_ki, X_kj)`.

### Depth

Human statement: `D_i` lower-bounds the total fractional ancestry into vertex
`i`.

Formula, for every `i in V`:

```text
D_i >= sum_{j in V, j != i} X_ji.
```

Equivalently:

```text
D_i - sum_{j != i} X_ji >= 0.
```

Source:

- `section_preliminaries.tex`, Definition `definition_LP_program`, "Depth".
- `STTLP-LPs.py`, `construct_constraints_primal`, "Depths constraints".

Implementation notes:

- This is an inequality, not equality. The optional code mode
  `exactDepthsConstraints` is not in v0.
- In any minimization with nonnegative weight on every `D_i`, optimal solutions
  can be assumed depth-tight for all positively weighted vertices, but proof
  checking must still evaluate the inequality as written.

## 5. Objective

For a nonnegative vertex-frequency or weight vector `f`, the LP minimizes:

```text
minimize f . D = sum_{i in V} f_i D_i.
```

Source:

- `section_preliminaries.tex`, Definition `definition_LP_program`,
  "Objective function".
- `STTLP-LPs.py`, `compute_gaps_or_vectors_for_direction`, which places the
  objective coefficients on the `D` coordinates for depth-only objectives.

Depth/cost convention:

- The LP objective uses strict-ancestor depths.
- The current checker's default STT cost uses root depth 1.
- If `f` is normalized so `sum_i f_i = 1`, then for an STT-induced point:

```text
search_cost(T,f) = 1 + f . D^T.
```

- For unnormalized nonnegative weights `w`:

```text
search_cost(T,w) = (sum_i w_i) + w . D^T.
```

Implementation convention:

- In an `lp_solution.objective`, store and verify `depth_objective_value =
  sum_i f_i D_i`.
- If comparing to existing checker costs with `depth_base: 1`, also compute
  `search_cost_value = depth_objective_value + sum_i f_i`.

The LP optimizes a given frequency vector. The feasible region itself is
frequency-independent. The "depth-space projection" questions are about the
frequency-independent projection of the feasible region onto `D`.

## 6. Depth-Space Projection

Let `P_U` be the feasible polyhedron in `(X,Z,D)` space defined by
`golinsky_stt_lp_v0`. The depth-space projection is:

```text
pi_D(P_U) = { D in R^V : exists X,Z such that (X,Z,D) in P_U }.
```

For a valid STT `T`, define its LP-depth vector:

```text
D^T_i = number of strict ancestors of i in T
      = checker_depth_base_1_T(i) - 1.
```

The STT depth hull is:

```text
H_U = conv { D^T : T is a valid recursive STT on U }.
```

Important implementation correction:

- Because `golinsky_stt_lp_v0` uses `D_i >= ...`, `pi_D(P_U)` is upward closed
  and unbounded. Literal equality `pi_D(P_U) = H_U` cannot hold as a bounded
  set comparison unless depth constraints are changed to equalities.
- The source paper handles objective-relevant comparisons through the lower
  envelope of the projected feasible region for nonnegative objectives.
- Therefore a checker should compare either:

```text
pi_D(P_U) lower envelope vs. H_U lower envelope
```

or equivalently:

```text
pi_D(P_U) vs. H_U + R_{\ge 0}^V.
```

For the pilot theorem target, this means the implementation should not test
literal bounded-polytope equality for the vanilla LP. It should test whether
every feasible projected depth vector dominates some convex combination of
valid STT LP-depth vectors, or search for a non-STT lower-envelope projected
vertex that improves some nonnegative objective.

Existing checker support:

- The v0 checker can enumerate STTs and compute root-depth-1 vectors.
- A future LP comparison must convert those to LP-depth vectors by subtracting
  1 from every coordinate.

## 7. Root-Rounding And Gap Certificate Hooks

### Root Rounding

Source rule, from Definition `definition_rounding_scheme`:

For a current connected component `C` and a feasible LP solution `P=(X,Z,D)`,
a vertex `r in C` is an admissible root if for every `v in C`, `v != r`,

```text
sum_{u in C : u != v and r in [u <-> v)} X_uv >= 1/2.
```

Then root the current STT component at `r`, delete `r`, and recurse on each
connected component of `C \ {r}` using the same `X` values restricted to that
component.

Source-code confirmation:

- `STTLP-GraphsAndSTT.py`, `round_to_STT`, computes `R[v]` by summing
  `x_variables[(u,v)]` when `r == u` or `r in betweenNodes(u,v)`, exactly the
  half-open path condition.

Certificate data needed:

- The topology and full `X` values.
- For each recursive component, the candidate root set or enough data for the
  checker to recompute it.
- The chosen root and deterministic tie-breaking rule if multiple roots are
  admissible.
- The rounded STT, represented in the existing `component_roots` format.

Already checkable by v0:

- Topology validity.
- Recursive rounded STT validity.
- Rounded STT depths and weighted cost.
- Integer optimum by complete enumeration for small `n`.

Needs new LP code:

- Validate `X` domains and values.
- Validate all LP constraints.
- Recompute admissible-root inequalities exactly.
- Replay tie-breaking exactly.

### Integrality-Gap Witness

A proof-mode witness needs:

- A topology.
- A nonnegative weight/frequency vector.
- A full rational `(X,Z,D)` LP solution for `golinsky_stt_lp_v0`.
- Exact LP depth objective `sum_i f_i D_i`.
- Integer optimum in matching LP-depth convention, or an existing
  root-depth-1 optimum plus exact conversion by subtracting `sum_i f_i`.
- A proof that the supplied integer optimum is exact: for small `n`, checker
  enumeration is enough; otherwise a future exact dual/integer certificate is
  needed.

The Sadeh-Kaplan-Zwick long-star example gives a source-backed smoke target:

- Source topology uses 1-indexed edges `(1,2),(2,3),(3,4),(4,5),(3,6),(6,7)`.
- Repository 0-indexed edges are
  `(0,1),(1,2),(2,3),(3,4),(2,5),(5,6)`.
- Source frequency vector is `[3,2,0,2,3,3,10]/23`.
- Source LP-depth vector is `[2,2,9/2,2,2,3/2,1/2]`.
- Source best STT LP-depth value for unnormalized weights is `30`; the
  fractional LP-depth value is `59/2`, giving LP-depth-objective gap `60/59`
  for this example. These are not root-depth-1 search-cost values; with
  normalized frequencies, the corresponding base-1 search costs add `1` to
  both objectives.

## 8. Edge-Diameter-3 Pilot Relevance

Sadeh-Kaplan-Zwick list as open whether the LP/root-rounding approach is
optimal on subclasses beyond stars, especially paths and edge-diameter-3
topologies, which they call "almost stars" informally. They also state that:

- the LP is known non-integer for edge-diameter 4 and above by the path on 5
  nodes;
- the `D`-space projection is non-integer for edge-diameter 5 and above by the
  long-star example.

Repository convention:

- Use the checker's line-graph edge distance label `edge-diameter-k`.
- Keep `almost-star` advisory until independently formalized.
- The edge-diameter-3 target should be phrased in `D`-projection/lower-envelope
  terms for `golinsky_stt_lp_v0`, not in literal bounded-polytope equality
  terms.

Before testing the target, implement:

- Dense exact parsing of `X`, `Z`, and `D` variables for
  `relaxation_version: "golinsky_stt_lp_v0"`.
- Exact generation of all variable domains from topology.
- Exact evaluation of all constraints in this spec.
- Exact objective recomputation in LP-depth convention.
- Conversion between checker root-depth-1 vectors and LP-depth vectors.
- A finite comparison method for `pi_D(P_U)` lower envelope versus enumerated
  STT depth hull, such as rational LP separation or exact vertex/facet data.

## 9. Implementation Plan

Minimal parser additions:

- Accept `lp_solution.relaxation == "golinsky_stt_lp"` and
  `lp_solution.relaxation_version == "golinsky_stt_lp_v0"`.
- Add dense `variables.D`, `variables.X`, and `variables.Z` blocks.
- Use 0-indexed repository labels in certificates.
- Reject undefined variable keys and missing defined variables in proof mode.
- Reject floats and decimal strings, reusing the exact rational parser.

Suggested JSON key shape:

```json
{
  "variables": {
    "D": [{"i": 0, "value": "2"}],
    "X": [{"i": 0, "j": 1, "value": "1"}],
    "Z": [{"k": 1, "i": 0, "j": 2, "value": "1/2"}]
  }
}
```

For `Z`, the checker should normalize endpoints internally to
`i < j`. If a certificate supplies `i > j`, either normalize with a warning in
audit mode or reject in proof mode. The conservative proof-mode choice is to
require `i < j`.

LP feasibility checker requirements:

- Build the variable domain from topology.
- Store rationals as `fractions.Fraction`.
- Represent a linear expression as a sparse map from variable key to rational
  coefficient plus a rational constant.
- Evaluate each inequality exactly as `lhs >= rhs`, or normalized as
  `expr >= 0`.
- Return machine-readable violations naming the constraint family and indices.

Exact rational linear-expression representation:

```text
LinearExpr = {constant: Fraction, terms: dict[VariableKey, Fraction]}
```

Proof mode versus search mode:

- Proof mode should be a custom exact checker for a supplied rational solution.
  It does not need to solve LPs.
- Floating solvers such as `scipy.optimize.linprog`, PuLP/CBC, or Sage numeric
  outputs may be useful in audit/search mode, but they are not proof objects.
- If a floating solver is used to find candidates, the candidate must be
  rationalized and then replayed through the exact checker.
- Exact dual certificates can be added later for objective optimality. They are
  not required for first feasibility checking.

Recommended first implementation path:

1. Implement domain generation and dense rational parsing.
2. Implement exact primal feasibility checking only.
3. Implement exact objective recomputation.
4. Add a long-star audit fixture from the Sadeh-Kaplan-Zwick source only after
   the full `(X,Z,D)` coordinates are transcribed from the figure/code archive.
5. Add root-rounding replay.
6. Add exact separation or dual certificates for projection/hull claims.

## 10. Ambiguities And Blockers

Golinsky thesis:

- Blocker: obtain and inspect Ishay Golinsky, "A study on search trees on
  trees", master's thesis, Tel Aviv University, 2023.
- Until then, cite `golinsky_stt_lp_v0` as the Sadeh-Kaplan-Zwick presentation
  and code version of Golinsky's relaxation.

Full long-star `(X,Z,D)` coordinates:

- The paper's text gives the long-star `D` vector and says the full point is in
  a figure. Before adding a proof fixture, extract every `X` and `Z` value from
  the figure or from the hard-coded full vertex representation in the source
  archive, then verify it against this spec.

Projection-integrality wording:

- The current pilot wording says "depth-space projection equals the convex hull
  of STT depth vectors." For `golinsky_stt_lp_v0` with depth inequalities, the
  literal projection is unbounded upward. The source-relevant comparison is
  lower-envelope equality, or equality to `conv(STT depths) + R_{\ge 0}^n`.
  Future theorem statements should use that exact convention.

Almost-star convention:

- Sadeh-Kaplan-Zwick informally connect edge-diameter 3 and "almost stars" in
  open-question text. The checker should continue deriving only
  `edge-diameter-k` until a precise `almost-star` definition is source-checked.

Dense versus sparse LP certificates:

- This spec chooses dense proof-mode LP variables to fail closed. Sparse
  zero-default certificates are attractive but should be a separate schema
  version or an explicit `encoding` field.

LP variants:

- The arXiv code contains several optional modes and a no-`Z` formulation.
  None are included in `golinsky_stt_lp_v0`. Supporting them requires separate
  names and separate specs.

Numerical source code:

- The arXiv code uses Sage for LP/polytope work and includes hard-coded
  computational data. The implementation should not treat Sage output, logs, or
  hard-coded arrays as proof unless replayed by exact checker logic.
