# Mixed-Support Public-Star Oracle Audit

## Stop Sign

This is an exact finite k=3 audit of the public-star support oracle. It does not claim public-LP exactness on `DS(k,1)`, does not close the b-root branch, and does not promote k=3 chamber data to an all-k theorem.

## Oracle Status

- corrected edge-cover max-flow/min-cut: `verified in recorded runs`
- min-cost support oracle: `implemented with exact Fraction arithmetic`
- direct LP cross-check for symmetric triangle: `verified`
- residual `ell_ij` formula: `implemented`
- residual `ell_ij` Farkas extraction: `not_certified`

## Symmetric Witness

- `Phi(1_12)`: `2`
- `Phi(1_13)`: `2`
- `Phi(1_23)`: `2`
- `Phi(1_12+1_13+1_23)`: `3`
- direct LP vertices: `18`

## Chamber Fan

The symmetric k=3 pair-antichain fan has `7` active min-cost forms.

| chamber | min-cost coefficients `(12,13,23)` | Phi coefficients `(12,13,23)` | witness lambda |
|---:|---:|---:|---:|
| 1 | `(0,2,2)` | `(2,0,0)` | `(1,0,0)` |
| 2 | `(1,1,1)` | `(1,1,1)` | `(1/3,1/3,1/3)` |
| 3 | `(1,1,2)` | `(1,1,0)` | `(1/2,1/2,0)` |
| 4 | `(1,2,1)` | `(1,0,1)` | `(1/2,0,1/2)` |
| 5 | `(2,0,2)` | `(0,2,0)` | `(0,1,0)` |
| 6 | `(2,1,1)` | `(0,1,1)` | `(0,1/2,1/2)` |
| 7 | `(2,2,0)` | `(0,0,2)` | `(0,0,1)` |

## Mode A

Root-comparisons-only mode: `failed_for_mixed_support_box_proxy`.

- violated proxy: `Phi(lambda_12+lambda_13+lambda_23) >= Phi(lambda_12)+Phi(lambda_13)+Phi(lambda_23)`
- lhs: `3`
- rhs: `6`
- slack: `-3`
- missing statistic: `s_min / equivalent min-cost support-flow statistic`

## Mode B

Vector proper-subset/mixed-support mode: `failed_for_individual_SUB_T_delta_proxy`; stronger residual `ell_ij` Farkas certificates were not extracted.

- violated proxy: `Phi(lambda) >= sum_ij lambda_ij delta_ij`
- lhs: `3`
- rhs: `6`
- slack: `-3`

## Regression Rays

- `existing_boundary_ray` weights `['0', '1', '1', '0', '1', '0']`: `F=1`, triangle `Phi=3`.
- `prompt_positive_interior_scalar_counterexample` weights `['1/2', '19/2', '20/3', '1/3', '5', '5']`: `F=26/3`, triangle `Phi=71/3`.

## Public Boundary

The scripts record only public `R,Q` row families and explicitly exclude H1/H2, refined-Z, path monotonicity, ancestry transitivity, LCA separation, non-public lifts, and grouped Bellman rays as public-dual extreme cuts.

## Artifacts

- `data\k3_pair_antichain_chambers.json`
- `data\mixed_support_certificates.json`
- `data\mixed_support_obstructions.json`
- `reports\mixed_support_oracle_report.md`

