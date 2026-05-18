# Proper-Subset Source-Deletion Contraction Audit v0

## Stop Sign

Finite exact small-k evidence only. This report does not claim public LP exactness on `DS(k,1)`, does not promote the b-root branch to a theorem, and does not prove the all-k proper-subset contraction lemma.

## Scope

The scripts implement the corrected source-deletion formula `F^{(-S)}(L)=min_A U((L\A)\S)+kappa(A)` with `kappa(A)=sum_{i in A} min(alpha,u_i)+sum_{pairs intersect A} min(u_i,u_j)`. The public-LP side records only the SKZ/Golinsky dual skeleton with unordered `R` and ordered collinear-triplet `Q` variables, capping rows, and frequency rows.

## Exact Status

| k | integer rays | b-root rays | positive b-root rays | proper subsets | status |
|---:|---:|---:|---:|---:|---|
| 3 | 3969 | 789 | 23 | 3 | `obstruction_candidate_found` |
| 4 | 2059 | 289 | 0 | 10 | `obstruction_candidate_found` |

The corrected `F(L)` formula was cross-checked against direct star-STT enumeration on the small star grids used by the script; no formula mismatch was found in the recorded runs.

## Floating Evidence

None. The generated JSON values are exact `Fraction` computations serialized as reduced rational strings. The only limitation is finite coverage, not floating-point reconstruction.

## First Proper-Subset Cut

The natural `D(S)` interpretation as the best S-first-b Bellman gap has an exact boundary obstruction candidate. This is not an all-k counterexample to any theorem unless this is confirmed as the intended `D(S)` definition, but it is a real architecture warning for this formulation.

- support: `['l2', 'l3']`
- weights: `{'l1': '0', 'l2': '1', 'l3': '1', 'a': '0', 'b': '1', 'r': '0'}`
- `F`: `1`
- `F_deleted`: `0`
- `delta(S)`: `1`
- `D(S)`: `0`
- slack `D(S)-delta(S)`: `-1`
- b-root cost: `3`
- true Bellman optimum: `3`
- b-root Bellman-optimal: `True`
- strictly positive weights: `False`

## Public Dual Skeleton

- k=3: `R` variables `15`, `Q` variables `26`, capping rows `13`, frequency rows `30`.
- k=4: `R` variables `21`, `Q` variables `38`, capping rows `19`, frequency rows `42`.

No H1/H2, refined-Z, path-monotonicity, ancestry-transitivity, or LCA-separation rows are generated.

## Corrected A_b(s) Families

The JSON groups normalized b-root Bellman rays by the corrected active `F(L)` branch `s`; these are the finite `A_b(s)` cut families extracted by the scripts. Proper non-singleton supports are then audited as `SUB_S` rows against exact `delta(S)` and `D(S)` values.

- k=3: {l1,l2,l3}: 703, {l1,l2}: 346, {l1,l3}: 346, {l1}: 220, {l2,l3}: 346, {l2}: 220, {l3}: 220, {}: 249
- k=4: {l1,l2,l3,l4}: 266, {l1,l2,l3}: 159, {l1,l2,l4}: 159, {l1,l2}: 98, {l1,l3,l4}: 159, {l1,l3}: 98, {l1,l4}: 98, {l1}: 75, {l2,l3,l4}: 159, {l2,l3}: 98, {l2,l4}: 98, {l2}: 75, {l3,l4}: 98, {l3}: 75, {l4}: 75, {}: 83

## Proper-Subset Summary

### k=3

| S | checked b-root rays | min slack | failures | positive failures | certificate status |
|---|---:|---:|---:|---:|---|
| `['l1', 'l2']` | 789 | `-3` | 11 | 0 | `failed_for_checked_rays` |
| `['l1', 'l3']` | 789 | `-3` | 11 | 0 | `failed_for_checked_rays` |
| `['l2', 'l3']` | 789 | `-3` | 11 | 0 | `failed_for_checked_rays` |

### k=4

| S | checked b-root rays | min slack | failures | positive failures | certificate status |
|---|---:|---:|---:|---:|---|
| `['l1', 'l2']` | 289 | `-2` | 2 | 0 | `failed_for_checked_rays` |
| `['l1', 'l3']` | 289 | `-2` | 2 | 0 | `failed_for_checked_rays` |
| `['l1', 'l4']` | 289 | `-2` | 2 | 0 | `failed_for_checked_rays` |
| `['l2', 'l3']` | 289 | `-2` | 2 | 0 | `failed_for_checked_rays` |
| `['l2', 'l4']` | 289 | `-2` | 2 | 0 | `failed_for_checked_rays` |
| `['l3', 'l4']` | 289 | `-2` | 2 | 0 | `failed_for_checked_rays` |
| `['l1', 'l2', 'l3']` | 289 | `0` | 0 | 0 | `certified_on_checked_rays` |
| `['l1', 'l2', 'l4']` | 289 | `0` | 0 | 0 | `certified_on_checked_rays` |
| `['l1', 'l3', 'l4']` | 289 | `0` | 0 | 0 | `certified_on_checked_rays` |
| `['l2', 'l3', 'l4']` | 289 | `0` | 0 | 0 | `certified_on_checked_rays` |

## Interpretation

This points to an architecture correction or at least a degeneracy patch before a proof pass: the S-first deletion bound must either be stronger than the audited Bellman interpretation, or the proof must route boundary faces through `B/a`, `B/r`, singleton rows, or explicit capacity/nonnegativity rows.

## Artifacts

- `data\proper_subset_contraction_k3.json`
- `data\proper_subset_contraction_k4.json`
- `reports\proper_subset_contraction_report.md`

