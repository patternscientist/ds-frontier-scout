# DS(k,2) Interface Residual v0

## Scope

This is a finite exact-rational audit of the corrected DS(k,2) H1 interface residual for `k=1,2,3`, plus a bounded DS(2,2) H1 gap search. It does not claim DS(k,2) exactness.

The checked residual keeps the per-left-leaf, per-right-vertex variables `eta_{i,x}` and `epsilon_{i,x}` for `x in {b,r,s}`. No H2, refined-Z, path monotonicity, or mixed-second-difference rows are used.

## Algebraic Identity

| topology | connected subsets | z variables | simplex rows | heredity rows | identity |
|---|---:|---:|---:|---:|---|
| DS(1,2) | 17 | 42 | 17 | 124 | True |
| DS(2,2) | 28 | 84 | 28 | 380 | True |
| DS(3,2) | 49 | 177 | 49 | 1220 | True |

The symbolic coefficient check verifies

`H1Obj = RightObj_{alpha+U}(z|_{R*}) + U + sum_i R_i + LeftLeft(z)`

where `LeftLeft(z) = sum_i u_i sum_{j != i} z[P(l_j,l_i),l_j]`. The JSON records every residual and `LeftLeft` term.

## DS(2,2) Search

No exact rational H1 depth gap was found in the bounded tested DS(2,2) objectives.

- Cases run: `128`.
- H1 certificate statuses: `{'verified_exact_primal_dual_after_floating_basis_reconstruction': 128}`.
- Solver failures: `0`.
- Runtime seconds: `75.171`.

## Dangerous-Chamber Certificates

Representative exact primal-dual certificates are saved in `certificates\dsk2_interface_residual_examples.json` and grouped by interface gap rows, promotion rows, left-left coarea rows, right-star defect rows, simplex rows, and other H1 rows.

| family | weights | H1 gap | dangerous score | active dual row groups |
|---|---|---:|---:|---|
| dangerous_left_heavy | `{'u_1': '8', 'u_2': '8', 'alpha': '0', 'beta': '0', 'w_r': '0', 'w_s': '1'}` | 0 | 4 | `{'interface_gap_rows_epsilon': 0, 'promotion_rows_eta_le_y': 0, 'left_left_coarea_rows': 1, 'right_star_defect_rows': 0, 'simplex_rows': 2, 'other_rows': 2}` |
| dangerous_left_heavy | `{'u_1': '10', 'u_2': '10', 'alpha': '0', 'beta': '0', 'w_r': '0', 'w_s': '1'}` | 0 | 4 | `{'interface_gap_rows_epsilon': 0, 'promotion_rows_eta_le_y': 0, 'left_left_coarea_rows': 1, 'right_star_defect_rows': 0, 'simplex_rows': 2, 'other_rows': 2}` |
| dangerous_left_heavy | `{'u_1': '10', 'u_2': '10', 'alpha': '0', 'beta': '0', 'w_r': '1', 'w_s': '1'}` | 0 | 4 | `{'interface_gap_rows_epsilon': 0, 'promotion_rows_eta_le_y': 0, 'left_left_coarea_rows': 1, 'right_star_defect_rows': 1, 'simplex_rows': 3, 'other_rows': 3}` |
| dangerous_left_heavy | `{'u_1': '9', 'u_2': '9', 'alpha': '2', 'beta': '0', 'w_r': '2', 'w_s': '1'}` | 0 | 4 | `{'interface_gap_rows_epsilon': 0, 'promotion_rows_eta_le_y': 1, 'left_left_coarea_rows': 1, 'right_star_defect_rows': 3, 'simplex_rows': 9, 'other_rows': 5}` |
| dangerous_left_heavy | `{'u_1': '10', 'u_2': '9', 'alpha': '0', 'beta': '0', 'w_r': '1', 'w_s': '1'}` | 0 | 4 | `{'interface_gap_rows_epsilon': 0, 'promotion_rows_eta_le_y': 0, 'left_left_coarea_rows': 2, 'right_star_defect_rows': 1, 'simplex_rows': 4, 'other_rows': 4}` |
| dangerous_left_heavy | `{'u_1': '10', 'u_2': '9', 'alpha': '1', 'beta': '1', 'w_r': '1', 'w_s': '1'}` | 0 | 4 | `{'interface_gap_rows_epsilon': 0, 'promotion_rows_eta_le_y': 0, 'left_left_coarea_rows': 2, 'right_star_defect_rows': 6, 'simplex_rows': 12, 'other_rows': 6}` |

## Skeptical Audit

- Finite no-gap results are not evidence of all-weights DS(2,2), DS(k,2), or double-star exactness.
- The local dangerous pattern is only a chamber heuristic; a simplex optimum can tie to another primal face and miss the displayed half-integral coordinates.
- The right marginal is not treated as a convex mixture of true right-star states. The residual explicitly keeps `eta` and `epsilon` interface variables.
- Dual-row grouping is diagnostic, not a symbolic proof generator.
