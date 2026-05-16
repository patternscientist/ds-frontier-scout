# Hereditary First-Hit LP Test On SKZ Long Star

## Question

Test the clean-room hereditary first-hit relaxation with variables `z_{A,r}` on the
source-aligned SKZ `U(7,3)` long-star instance:

- Edges: `[[0,1],[1,2],[2,3],[3,4],[2,5],[5,6]]`
- Unnormalized weights: `[3,2,0,2,3,3,10]`
- Known combinatorial STT optimum, depth base 1: `53`
- Therefore known combinatorial STT optimum, root-depth-0 objective: `30`

The LP objective is

```text
sum_v w_v d_v(z), where d_v(z) = sum_{u != v} z_{P(u,v),u}.
```

## Implementation

Implemented in `scripts/stt_checker/hereditary_lp.py`.

The model enumerates every nonempty connected subset of the input tree, creates
`z_{A,r}` for every `r in A`, adds one simplex equality per connected subset,
and adds every proper inclusion heredity inequality
`z_{A,r} <= z_{B,r}` for connected `B subset A` and `r in B`.

The solver used here is a pure-Python two-phase simplex fallback. Coefficients
are constructed exactly as `Fraction`s, then solved numerically in floating
point. Tolerance: `1e-9`.

The full numerical SKZ result, including all z variables, is saved at:

```text
examples/stt_lp/skz_long_star_7_hereditary_lp_result.json
```

## Counts

For the SKZ `U(7,3)` instance:

- Connected subsets: `36`
- z variables: `120`
- Simplex constraints: `36`
- Heredity inequalities: `681`

## Sanity Cases

All values below use the same root-depth-0 hereditary objective.

| Case | Weights | Hereditary LP value | True root-depth-0 STT optimum |
|---|---:|---:|---:|
| Edge `0-1` | `[1,1]` | `1` | `1` |
| P3 `0-1-2` | `[1,1,1]` | `2` | `2` |
| P3 `0-1-2` | `[2,0,3]` | `2` | `2` |
| P3 `0-1-2` | `[1,4,4]` | `5` | `5` |
| P3 `1-0-2`, center `0` | `[1,4,4]` | `6` | `6` |

Note: the earlier discrepancy was caused by a coordinate convention mismatch.
For the path topology `0-1-2`, weights `[1,4,4]` put weight `1` on an endpoint,
and exact enumeration gives optimum `5`. The intended good-root-failure sanity
case is instead the topology `1-0-2`, with vertex `0` as the center and weights
`[1,4,4]`; in that convention the true root-depth-0 STT optimum is `6`.

## SKZ Result

Solver status:

```text
status=0
message=optimal
solver=pure_python_two_phase_simplex
```

Numerical LP result:

```text
objective_value = 29.5
min_variable_value = 0
maximum_simplex_residual = 0
maximum_heredity_violation = 0
```

Comparison:

```text
hereditary LP value = 29.5
root-depth-0 STT optimum = 30
gap = -0.5
```

Thus the hereditary LP goes below the root-depth-0 STT optimum on the canonical
SKZ long-star weights.

## Rationalized Certificate

The numerical solution rationalizes exactly to values in `{0, 1/2, 1}`.
Exact checking of that rationalized primal point gives:

```text
exact objective = 59/2
minimum variable = 0
maximum simplex residual = 0
maximum heredity violation = 0
```

This exact primal certificate is included in
`examples/stt_lp/skz_long_star_7_hereditary_lp_result.json` under
`rationalized_certificate.nonzero_z_variables`.

This is stronger than a purely floating-point warning: the rationalized point is
feasible for the stated hereditary first-hit constraints and has objective
`59/2 < 30`. The simplex claim that `29.5` is the LP optimum is still numerical,
because no exact dual certificate is produced here.

## Conclusion

The clean-room hereditary first-hit conjecture `Q(U) subset D(U)` does not
survive this test as stated. On the SKZ `U(7,3)` topology with weights
`[3,2,0,2,3,3,10]`, the hereditary relaxation admits an exactly checkable
rational feasible point of root-depth-0 value `59/2`, below the exact STT
optimum `30`.

So the conjecture is killed for this relaxation, assuming the LP definition in
the clean-room note and the checked STT optimum fixture are the intended objects.
The remaining caveat is not numerical precision of the primal certificate, but
model interpretation: if some additional first-hit consistency constraint was
intended, it is not among the three constraints tested here.

## Reproduction

Run the standard sanity cases and SKZ solve:

```powershell
python -m scripts.stt_checker.hereditary_lp
```

Regenerate the saved SKZ result JSON:

```powershell
python -m scripts.stt_checker.hereditary_lp --write-skz-json examples\stt_lp\skz_long_star_7_hereditary_lp_result.json
```

Run the focused hereditary-LP tests:

```powershell
python -m unittest tests.test_stt_hereditary_lp -v
```

Run the full test suite:

```powershell
python -m unittest discover -v
```
