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

## Ranges Tested

- Structural STT enumeration checked against generic recursive enumeration for `d=1..5`: `{'1': True, '2': True, '3': True, '4': True, '5': True}`.
- Full H2 LP objectives: 122 objectives; smallest H-STT gap `0`.
- Full H3/H4 probe objectives: 22 objectives; smallest H-STT gap `0`.
- Symmetric H2 objectives: 40 objectives; smallest H-STT gap `0`.
- Full objective families include center-heavy, one/two/three/four-heavy leaves, symmetric leaf weights, convex heavy-count patterns, and all small integer weights up to `2` modulo leaf symmetry through `d=4`.
- Symmetric objectives use `(center, leaf)` weights `(0,1)`, `(1,1)`, `(4,1)`, `(10,1)`, and `(1,4)` through `d=8`.

## Full vs Symmetric Reduction

For symmetric weights and `d<=4`, the orbit-variable H2 LP was compared against the full H2 LP.  All compared optima matched exactly.  The reduced variables are `c_s` for the center root on a center-containing set with `s` leaves and `l_s` for a leaf root in such a set; singleton leaf first-hit values are constants equal to `1`.

## Depth-Projection Gap Search

No depth-projection gap was found in the tested range.
- Tightest full H2 case: d=1, H2, family=center_heavy, weights=(10, 1), H=1, STT=1.
- Tightest H3/H4 probe case: d=1, H3, family=center_heavy, weights=(10, 1), H=1, STT=1.
- Tightest symmetric H2 case: d=1, H2, family=symmetric_0_1, weights=(0, 1), H=0, STT=0.
- For every reported objective, an exact primal/dual certificate was reconstructed from the LP basis with zero primal violation, zero dual deficit, and matching objective value.

## 4-Leaf z-Obstruction Regression

- Audited 4-leaf obstruction H2-feasible in full `z`-space: `True`.
- Complete Mobius negative masses: `5`, including center mass `-1/3`.
- Depth vector: `('8/3', '11/6', '11/6', '11/6', '11/6')`.
- Dominated by center-root STT vector `(0,1,1,1,1)`: `True`.

## Candidate Theorem Statements

1. Conservative candidate: For every fixed nonnegative weight vector tested here, the H2 depth optimum on a star equals the exact STT optimum.  This is only a finite computational statement.
2. Structural candidate: The leaf-symmetrized H2 constraints may already imply the lower envelope of ordered-prefix STT depth vectors for symmetric weights on all stars.
3. Strong candidate to audit: H2 has exact depth projection on all stars, even though H2 is not exact in full first-hit `z`-space.

## Skeptical Audit

- The tests do not prove all-star exactness; they only rule out witnesses in the enumerated objective families and sizes.
- A nonsymmetric separating weight vector with larger support or larger coefficients could still exist.
- H3/H4 were only probed where the full finite-difference generator was computationally modest.
- The 4-leaf full-`z` obstruction remains real; the evidence here says it does not project to a depth obstruction.
- Before promotion, the symmetric reduction should be independently reviewed and a hand-checkable dual pattern should be extracted from the exact multipliers.
