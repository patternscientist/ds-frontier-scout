# STT Star Depth Projection v0

## Scope

This report tests whether the connected first-hit H2 failure on the 4-leaf star is only a full-`z` phenomenon or also appears after projecting to root-depth-0 STT depth vectors.  It is finite exact computation plus theorem scouting, not an all-stars proof.

## Exact Model Definitions

- The `d`-leaf star has center `0`, leaves `1..d`, and edges `{0,i}`.
- Connected sets are exactly the singletons and the sets `{0} union S` with nonempty `S subseteq {1..d}`.
- Variables are first-hit values `z[I,r]` for connected `I` and `r in I`.
- H1 is simplex plus heredity.  Hk adds all union finite-difference inequalities through order `k`: `sum_B (-1)^|B| z[union_{i in B} A_i,r] >= 0`.
- Depth projection uses `D_v = sum_{u != v} z[P(u,v),u]` with root-depth-0 convention.
- The complete/`H_infty` baseline is exact STT enumeration.  On a star, an STT is an ordered prefix of leaves, followed by the center, then the remaining leaves as children.
- For nonnegative weights, the ordered-prefix formula sorts leaf weights `a_1 >= ... >= a_d` and minimizes `w_0 k + sum_{i=1..k} a_i (i-1) + (k+1) sum_{i=k+1..d} a_i` over `0 <= k <= d`.

## Theorem Discovered After Computation

- Finite computational evidence already run: this artifact found no H2/H3/H4 star depth-projection gap in the tested ranges, and the symmetric H2 reduction matched the full H2 LP for symmetric objectives through the checked full-LP range.
- Theorem now believed/proved externally: H1 has exact depth projection on all stars.  Since H2 contains H1 constraints, this also explains why the H2 star depth-projection gap search did not find a witness.
- Regression role of the code: the implementation now checks the ordered-prefix formula against exact H1 and H2 LP optima on feasible structured and deterministic pseudorandom nonnegative weights, and it keeps the audited 4-leaf full-`z` obstruction regression.  These tests guard the model and report machinery; they are not a proof of the theorem.

## Symmetric Star Reduction

Let `S subseteq {1..d}` be a set of leaves.  Under leaf symmetry, every center-containing first-hit variable belongs to one of two orbit types:

- `c_s = z[{0} union S, 0]` for `|S|=s`, with `0 <= s <= d`.
- `l_s = z[{0} union S, i]` for `i in S` and `|S|=s`, with `1 <= s <= d`.
- Singleton leaf values are constants: `z[{i}, i] = 1`.

The simplex equations reduce to:

- `c_0 = 1` for the singleton center set.
- `c_s + s l_s = 1` for every `s >= 1`, because `{0} union S` has one center root orbit and `s` identical leaf-root entries.

The H1 orbit inequalities are exactly the monotonicity rows obtained from a base connected set and a proper connected superset:

- Center-root rows: `c_s - c_t >= 0` for `0 <= s < t <= d`.
- Leaf-root rows inside center-containing sets: `l_s - l_t >= 0` for `1 <= s < t <= d`.
- Singleton-leaf base rows: `1 - l_t >= 0` for `1 <= t <= d`.

The H2 orbit inequalities are the two-extension finite differences after quotienting by leaf permutations.  For feasible union-size patterns with base size `s`, extension sizes `t` and `u`, and union size `v`, the generated rows have the forms `c_s - c_t - c_u + c_v >= 0`, `l_s - l_t - l_u + l_v >= 0`, and `1 - l_t - l_u + l_v >= 0` for center roots, center-containing leaf roots, and singleton-leaf bases respectively.  Feasible patterns are enumerated by distributing leaves among the Venn atoms of the two supersets, so the reduction depends only on orbit sizes rather than leaf labels.

Implementation note: the code generates rows directly in orbit variables for root types `center`, `leaf`, and `singleton_leaf`.  It stores rows in internal `<=` form and de-duplicates by the exact sparse coefficient vector plus exact right-hand side.  Swapping the two H2 extensions, repeated orbit-size patterns, and simplex/H1 duplicates therefore collapse to one row.  The only pre-insertion skip is for an empty row with a nonnegative pre-negation bound, so the filter cannot remove a nonempty orbit inequality.

## Evidence Types

### Exact Full-LP Tests

- Structural STT enumeration checked against generic recursive enumeration for `d=1..5`: `{'1': True, '2': True, '3': True, '4': True, '5': True}`.
- Full H2 LP objectives: 122 objectives; smallest H-STT gap `0`.
- Full objective families include center-heavy, one/two/three/four-heavy leaves, symmetric leaf weights, convex heavy-count patterns, and all small integer weights up to `2` modulo leaf symmetry through `d=4`.
- Reported families: `1_leaf_heavy`, `2_leaf_heavy`, `3_leaf_heavy`, `4_leaf_heavy`, `center_heavy`, `convex_heavy_count_0`, `convex_heavy_count_1`, `convex_heavy_count_2`, `convex_heavy_count_3`, `convex_heavy_count_4`, `small_int_leq_2`, `symmetric_leaf_weights`.
- Certificate status: each no-gap optimum is reconstructed from a floating simplex basis, independently verified after reconstruction by exact primal and dual checks, and checked during report generation only.  Full-LP basis data and per-objective certificates are not saved as JSON.
- Tightest full H2 case: d=1, H2, family=center_heavy, weights=(10, 1), H=1, STT=1.

### Exact Symmetric-Reduction Tests

- Symmetric H2 objectives: 40 objectives; smallest H-STT gap `0`.
- Symmetric objectives use `(center, leaf)` weights `(0,1)`, `(1,1)`, `(4,1)`, `(10,1)`, and `(1,4)` through `d=8`.
- For symmetric weights and `d<=4`, the orbit-variable H2 LP was compared against the full H2 LP.  All compared optima matched exactly.
- Reported families: `symmetric_0_1`, `symmetric_10_1`, `symmetric_1_1`, `symmetric_1_4`, `symmetric_4_1`.
- Certificate status: each no-gap optimum is reconstructed from a floating simplex basis and independently verified after reconstruction.  A compact JSON summary is saved at `examples\stt_lp\star_symmetric_h2_d_leq_8_summary.json`; it records optima, gaps, weights, and verification status, but not basis data or full variable assignments.
- Tightest symmetric H2 case: d=1, H2, family=symmetric_0_1, weights=(0, 1), H=0, STT=0.

### H3/H4 Probes

- Full H3/H4 probe objectives: 22 objectives; smallest H-STT gap `0`.
- Probe families are center-heavy, symmetric leaf weights, and two-heavy-leaf objectives where defined.
- Reported families: `center_heavy`, `symmetric_leaf_weights`, `two_leaf_heavy`.
- Certificate status: each no-gap optimum is reconstructed from a floating simplex basis, independently verified after reconstruction, and checked during report generation only.  H3/H4 probe certificates are not saved as JSON.
- Tightest H3/H4 probe case: d=1, H3, family=center_heavy, weights=(10, 1), H=1, STT=1.

### Random/Secondary Scouting

- No random objective sampling is reported as scouting evidence in this artifact.  The secondary scouting is deterministic: structured heavy-leaf families, convex heavy-count families, and small nondecreasing integer weights modulo leaf symmetry.
- Separately, the regression tests include deterministic pseudorandom nonnegative weights to check the H1/H2 implementation against the ordered-prefix theorem formula.

### Limitations

- No finite test proves all-star exactness.
- A nonsymmetric separating weight vector with larger support or larger coefficients could still exist.
- H3/H4 were only probed where the full finite-difference generator was computationally modest.
- The compact symmetric JSON artifact intentionally omits basis data; rerun the generator to reconstruct and reverify certificates.

## Depth-Projection Gap Search

No H2/H3/H4 star depth-projection gap was found in the tested ranges.
- For every reported objective, the H-STT gap is nonnegative and the exact primal/dual certificate verification passes.

## 4-Leaf z-Obstruction Regression

- Audited 4-leaf obstruction H2-feasible in full `z`-space: `True`.
- Complete Mobius negative masses: `5`, including center mass `-1/3`.
- Depth vector: `('8/3', '11/6', '11/6', '11/6', '11/6')`.
- Dominated by center-root STT vector `(0,1,1,1,1)`: `True`.

## Candidate Theorem Extracted

The computation originally suggested: **H2 depth projection may be exact for all stars.**  After the computation, the stronger theorem now believed/proved externally is: **H1 has exact depth projection on all stars.**  The code did not prove this theorem; it now serves as a regression harness for the formula and the LP implementations.

What remains before this repository should promote the theorem as a proof artifact:

- A checked-in proof note or source reference for the external proof.
- An analytic characterization of the star STT dominant.
- An analytic derivation showing why H1 attains exactly the ordered-prefix formula for every nonnegative weight vector.
- Optional: a dual pattern explaining the exact LP optimum symbolically rather than by per-instance certificates.

## Skeptical Audit

- The tests do not prove all-star exactness; by themselves they only rule out witnesses in the enumerated objective families and sizes.
- Without the external H1 theorem, a nonsymmetric separating weight vector with larger support or larger coefficients would remain a possible finite-test escape.
- H3/H4 were only probed where the full finite-difference generator was computationally modest.
- The 4-leaf full-`z` obstruction remains real; the evidence here says it does not project to a depth obstruction.
- Before proof-level promotion inside this repository, the external theorem should be recorded in a proof note or tied to a primary source.
