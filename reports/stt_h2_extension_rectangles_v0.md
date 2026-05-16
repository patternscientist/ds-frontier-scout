# H2 Extension-Rectangle LP Test On SKZ Long Star

## Question

Test the next clean-room hereditary first-hit relaxation on the source-aligned
SKZ `U(7,3)` long-star instance:

- Edges: `[[0,1],[1,2],[2,3],[3,4],[2,5],[5,6]]`
- Unnormalized weights: `[3,2,0,2,3,3,10]`
- Comparison target: exact root-depth-0 STT optimum `30`

Do not use the root-depth-1 value `53` for this LP comparison.

## H2 Definition

For every nonempty connected set `A` in the base tree and every `r in A`, H1 has
a variable `z_{A,r}`. H1 constraints are:

```text
z_{A,r} >= 0
sum_{r in A} z_{A,r} = 1
z_{A,r} <= z_{B,r} whenever B subset A, B connected, and r in B
```

H2 is H1 plus the connected-set extension rectangle inequalities

```text
z_{S,r} - z_{A,r} - z_{B,r} + z_{A union B,r} >= 0
```

whenever `S`, `A`, `B`, and `A union B` are connected, `S subset A`,
`S subset B`, and `r in S`.

The implementation enumerates one orientation of the symmetric `A,B` pair and
omits rectangle rows that collapse to a tautology or to an already-present H1
heredity row. This does not change the feasible region.

## Implementation

Implemented in `scripts/stt_checker/hereditary_lp.py`.

The command-line option is:

```powershell
python -m scripts.stt_checker.hereditary_lp --relaxation h1
python -m scripts.stt_checker.hereditary_lp --relaxation h2
```

The solver is still the repository's pure-Python two-phase simplex routine.
Coefficients are built exactly as `Fraction`s and then solved in floating point.
Tolerance: `1e-9`.

The H2 SKZ result is saved at:

```text
examples/stt_lp/skz_long_star_7_h2_result.json
```

That JSON includes the numerical primal solution, a rationalized primal check,
and final simplex basis/nonbasis indices for later exact-dual reconstruction.

## Counts

For the SKZ long-star instance:

```text
connected_subsets = 36
z_variables = 120
simplex_constraints = 36
heredity_inequalities = 681
h2_rectangle_inequalities = 1257
```

The standard-form simplex solve has `2010` inequality rows after representing
the simplex equalities by both signs.

## H1 Comparison

The prior H1 run found an exactly checkable rational feasible point with

```text
objective = 59/2 = 29.5 < 30
```

The saved H1 certificate violates the H2 rectangle

```text
S = {2,3,4}
A = {1,2,3,4}
B = {2,3,4,5}
A union B = {1,2,3,4,5}
r = 3
```

by

```text
1/2 - 1/2 - 1/2 + 0 = -1/2
```

The focused tests check this exact violation and check that H2 includes a row
cutting this certificate.

## H2 Result

Solver status:

```text
status = 0
message = optimal
solver = pure_python_two_phase_simplex
```

Numerical result:

```text
objective_value = 30.000000000000057
objective_recomputed = 30.000000000000064
min_variable_value = 0
max_simplex_residual = 2.9976021664879227e-15
max_heredity_violation = 1.3322676295500569e-15
max_h2_rectangle_violation = 2.8865798640254827e-15
```

The numerical H2 optimum is therefore `30` to solver tolerance. It does not
produce a new objective below `30` on this instance.

The numerical primal solution rationalizes to an exactly feasible H2 point with
objective `30`:

```text
exact rationalized primal objective = 30
maximum simplex residual = 0
maximum heredity violation = 0
maximum H2 rectangle violation = 0
```

This exact primal point proves feasibility at value `30`, but not optimality.
The closure claim for the H2 relaxation on this instance remains numerical and
provisional until an exact dual certificate is produced. The saved basis data in
`examples/stt_lp/skz_long_star_7_h2_result.json` is intended to support that
next exact-certification step.

## Answer

Does H2 still have objective below `30`?

No, not in the numerical solve.

Does H2 close the known H1 gap to `30`?

Numerically yes on the 7-node SKZ long-star instance. The old H1 certificate is
cut by an H2 rectangle inequality, and the H2 solve returns value `30` up to
roundoff.

Is the result exact?

The feasible primal value `30` is exact after rationalization. The optimality
claim is not exact yet, because no exact dual certificate has been produced.

## Reproduction

Run the H1 sanity cases:

```powershell
python -m scripts.stt_checker.hereditary_lp
```

Regenerate the H2 SKZ result JSON:

```powershell
python -m scripts.stt_checker.hereditary_lp --relaxation h2 --write-skz-json examples\stt_lp\skz_long_star_7_h2_result.json
```

Run the focused tests:

```powershell
python -m unittest tests.test_stt_hereditary_lp -v
```

Run the full test suite:

```powershell
python -m unittest discover -v
```
