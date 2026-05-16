# H2 Exact Dual Certificate Audit For SKZ U(7,3)

## Instance

Topology: SKZ `U(7,3)` long star with edges
`[[0,1],[1,2],[2,3],[3,4],[2,5],[5,6]]`.

Weights: `[3,2,0,2,3,3,10]`.

Comparison target: exact root-depth-0 STT optimum `30`.

## Model Audit

The H2 model is the clean-room hereditary first-hit LP from
`scripts/stt_checker/hereditary_lp.py`.

Variables are `z_{A,r}` for every nonempty connected subset `A` and every
`r in A`. H1 includes nonnegativity, one simplex equality
`sum_{r in A} z_{A,r} = 1` for each connected `A`, and heredity
`z_{A,r} <= z_{B,r}` whenever `B subset A`, `B` is connected, and `r in B`.

H2 adds

```text
z_{S,r} - z_{A,r} - z_{B,r} + z_{A union B,r} >= 0
```

whenever `S`, `A`, `B`, and `A union B` are connected, `S subset A`,
`S subset B`, and `r in S`.

The audit enumerates all ordered candidate triples `(S,A,B)` and simplifies
each row exactly. Rows with zero reduced expression are true tautologies. Rows
with one positive and one negative term are already H1 heredity rows. The
remaining four-term rows are canonicalized by sorting the symmetric `A,B` pair.

For the SKZ instance the audit gives:

```text
connected_subsets = 36
z_variables = 120
ordered_candidates = 8435
tautologies = 1482
h1_duplicates = 4439
nontrivial_ordered = 2514
symmetric_or_exact_duplicates = 1257
canonical_nontrivial = 1257
implemented_rectangles = 1257
missing_nontrivial_rows = 0
extra_rows = 0
```

Thus every intended nontrivial H2 rectangle inequality is present, and every
omitted candidate is a tautology, an H1 duplicate, or the symmetric duplicate of
an included rectangle row.

## Reconstruction From Numerical Basis

Exact certificate produced:

```text
examples/stt_lp/skz_long_star_7_h2_dual_certificate.json
```

The certificate was reconstructed from the saved numerical simplex result in
`examples/stt_lp/skz_long_star_7_h2_result.json`. The reconstruction uses only
the saved topology, weights, rationalized primal point, and simplex basis to
solve an exact reduced linear system for the dual multipliers.

The saved numerical basis reconstructs cleanly. There are `117` basic original
variables and `117` nonbasic slack rows; solving the reduced exact system yields
an integral nonnegative dual. The checked certificate has `89` nonzero dual
rows.

This reconstruction step is not the verifier. It is the provenance of the
checked-in certificate.

## Independent Certificate Verification

The saved certificate is independently verified by:

```powershell
python -m scripts.stt_checker.h2_dual_certificate verify examples\stt_lp\skz_long_star_7_h2_dual_certificate.json
```

Verifier output:

```text
verified H2 certificate: primal=30 dual_max=-30 lower_bound=30
```

This verifier does not read `examples/stt_lp/skz_long_star_7_h2_result.json`
and does not rely on the saved numerical basis or the certificate's
`basis_reconstruction` metadata. It rebuilds the H2 standard form exactly from
the certificate's topology and weights as
`max -objective subject to Ax <= b, x >= 0`, with simplex equalities represented
by both signs. It then checks:

- primal dimensions and all exact H2 constraints;
- primal objective `30`;
- dual dimensions, row descriptors, signs, and exact dual feasibility
  `A^T y >= c`;
- dual objective `b^T y = -30`, giving original minimization lower bound `30`;
- matching primal and dual values.

Conclusion: H2 closes the SKZ `U(7,3)` objective gap exactly for this weight
vector. This is now an exact, independently checkable LP certificate, not only a
numerical simplex observation.

## Primal Objective

The primal certificate is the rationalized H2 feasible point from the saved
solve. It is exact:

```text
objective = 30
min z = 0
simplex residual = 0
heredity violation = 0
H2 rectangle violation = 0
```

## Dual Objective

The dual certificate is exact in the standard max-`-objective` convention:

```text
dual max objective = -30
original minimization lower bound = 30
```

Together with the exact primal value `30`, this certifies the H2 optimum exactly.

## Fixed-D Infeasibility

Depth vector tested:

```text
D = (2, 2, 9/2, 2, 2, 3/2, 1/2)
```

Saved result:

```text
examples/stt_lp/skz_long_star_7_h2_fixed_d_result.json
```

Command:

```powershell
python -m scripts.stt_checker.h2_dual_certificate fixed-d --certificate examples\stt_lp\skz_long_star_7_h2_dual_certificate.json --output examples\stt_lp\skz_long_star_7_h2_fixed_d_result.json --run-numerical
```

Output:

```text
fixed-D feasible=False fixed_objective=59/2 h2_lower_bound=30 farkas_rhs=-1/2
numerical_simplex status=2 message=infeasible in simplex phase I
```

The exact infeasibility certificate uses the same H2 dual bound. The fixed
depth vector forces the weighted objective to

```text
3*2 + 2*2 + 0*(9/2) + 2*2 + 3*2 + 3*(3/2) + 10*(1/2) = 59/2.
```

The exact H2 dual proves every H2 feasible point has objective at least `30`.
Equivalently, combining the H2 dual multipliers with the fixed-D equality
multipliers gives a Farkas-style contradiction with right-hand side `-1/2`.
So the public SKZ fractional depth vector does not lift to H2.

The optional full public SKZ `X/Z` path-variable lift was not run; the complete
public point is not checked in as data in this repository.

## Full Public X/Z Lift Status

The full public SKZ `X/Z` lift remains untested in this repository. The result
above only rules out the listed fixed depth vector under H2. It should not be
read as a certificate about every possible public path-variable assignment
unless that full public point is added and checked separately.

## Reproduction

Audit the rectangle enumeration:

```powershell
python -m scripts.stt_checker.h2_dual_certificate audit-rectangles
```

Reconstruct the certificate from the saved numerical basis:

```powershell
python -m scripts.stt_checker.h2_dual_certificate reconstruct --result-json examples\stt_lp\skz_long_star_7_h2_result.json --certificate examples\stt_lp\skz_long_star_7_h2_dual_certificate.json
```

Verify the certificate:

```powershell
python -m scripts.stt_checker.h2_dual_certificate verify examples\stt_lp\skz_long_star_7_h2_dual_certificate.json
```

Run the fixed-D test:

```powershell
python -m scripts.stt_checker.h2_dual_certificate fixed-d --certificate examples\stt_lp\skz_long_star_7_h2_dual_certificate.json --output examples\stt_lp\skz_long_star_7_h2_fixed_d_result.json --run-numerical
```

Run tests:

```powershell
python -m unittest discover -v
```
