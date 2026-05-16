# STT Double-Star Depth Projection v0

## Scope

This is finite theorem-driven computation for double-stars `DS(m,n)`, not a broad arbitrary-tree sweep.  The complete baseline is exact root-depth-0 STT enumeration; H1 is connected first-hit heredity; H2 adds connected two-extension rectangle inequalities.

The tested topologies are `DS(1,1)`, `DS(2,1)`, `DS(2,2)`, `DS(3,1)`, `DS(3,2)`, `DS(3,3)`.
Normal-form STT enumeration agrees with generic recursive enumeration on small checks: `{'DS(1,1)': True, 'DS(2,1)': True, 'DS(2,2)': True}`.

## Outcome

No H1 depth-projection gap was found in the tested double-star objectives.
No H2 depth-projection gap was found; H2 optima were certified by the H1/STT sandwich whenever H1 was already tight.

This is finite evidence only.  It does not claim double-star exactness.

## Solve Table

| topology | family | weights | STT | H1 | H1 cert | H2 | H2 cert |
|---|---|---:|---:|---:|---|---:|---|
| DS(1,1) | one_heavy_left_leaf | `(8, 1, 1, 1)` | 5 | 5 | verified_exact_primal_dual_after_floating_basis_reconstruction | 5 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | one_heavy_right_leaf | `(1, 1, 1, 8)` | 5 | 5 | verified_exact_primal_dual_after_floating_basis_reconstruction | 5 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | one_heavy_leaf_each_side | `(8, 1, 1, 8)` | 13 | 13 | verified_exact_primal_dual_after_floating_basis_reconstruction | 13 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | left_center_heavy | `(1, 8, 1, 1)` | 4 | 4 | verified_exact_primal_dual_after_floating_basis_reconstruction | 4 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | right_center_heavy | `(1, 1, 8, 1)` | 4 | 4 | verified_exact_primal_dual_after_floating_basis_reconstruction | 4 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | both_centers_heavy | `(1, 8, 8, 1)` | 11 | 11 | verified_exact_primal_dual_after_floating_basis_reconstruction | 11 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | asym_left_center_right_leaf | `(1, 6, 1, 9)` | 10 | 10 | verified_exact_primal_dual_after_floating_basis_reconstruction | 10 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | asym_right_center_left_leaf | `(9, 1, 6, 1)` | 10 | 10 | verified_exact_primal_dual_after_floating_basis_reconstruction | 10 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 0, 0, 1)` | 0 | 0 | verified_exact_primal_dual_after_floating_basis_reconstruction | 0 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 0, 0, 2)` | 0 | 0 | verified_exact_primal_dual_after_floating_basis_reconstruction | 0 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 0, 1, 0)` | 0 | 0 | verified_exact_primal_dual_after_floating_basis_reconstruction | 0 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 0, 1, 1)` | 1 | 1 | verified_exact_primal_dual_after_floating_basis_reconstruction | 1 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 0, 1, 2)` | 1 | 1 | verified_exact_primal_dual_after_floating_basis_reconstruction | 1 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 0, 2, 0)` | 0 | 0 | verified_exact_primal_dual_after_floating_basis_reconstruction | 0 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 0, 2, 1)` | 1 | 1 | verified_exact_primal_dual_after_floating_basis_reconstruction | 1 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 0, 2, 2)` | 2 | 2 | verified_exact_primal_dual_after_floating_basis_reconstruction | 2 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 1, 0, 0)` | 0 | 0 | verified_exact_primal_dual_after_floating_basis_reconstruction | 0 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 1, 0, 1)` | 1 | 1 | verified_exact_primal_dual_after_floating_basis_reconstruction | 1 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 1, 0, 2)` | 1 | 1 | verified_exact_primal_dual_after_floating_basis_reconstruction | 1 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 1, 1, 0)` | 1 | 1 | verified_exact_primal_dual_after_floating_basis_reconstruction | 1 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 1, 1, 1)` | 2 | 2 | verified_exact_primal_dual_after_floating_basis_reconstruction | 2 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 1, 1, 2)` | 3 | 3 | verified_exact_primal_dual_after_floating_basis_reconstruction | 3 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 1, 2, 0)` | 1 | 1 | verified_exact_primal_dual_after_floating_basis_reconstruction | 1 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 1, 2, 1)` | 2 | 2 | verified_exact_primal_dual_after_floating_basis_reconstruction | 2 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 1, 2, 2)` | 3 | 3 | verified_exact_primal_dual_after_floating_basis_reconstruction | 3 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 2, 0, 0)` | 0 | 0 | verified_exact_primal_dual_after_floating_basis_reconstruction | 0 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 2, 0, 1)` | 1 | 1 | verified_exact_primal_dual_after_floating_basis_reconstruction | 1 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 2, 0, 2)` | 2 | 2 | verified_exact_primal_dual_after_floating_basis_reconstruction | 2 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 2, 1, 0)` | 1 | 1 | verified_exact_primal_dual_after_floating_basis_reconstruction | 1 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 2, 1, 1)` | 3 | 3 | verified_exact_primal_dual_after_floating_basis_reconstruction | 3 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 2, 1, 2)` | 4 | 4 | verified_exact_primal_dual_after_floating_basis_reconstruction | 4 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 2, 2, 0)` | 2 | 2 | verified_exact_primal_dual_after_floating_basis_reconstruction | 2 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 2, 2, 1)` | 3 | 3 | verified_exact_primal_dual_after_floating_basis_reconstruction | 3 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(0, 2, 2, 2)` | 4 | 4 | verified_exact_primal_dual_after_floating_basis_reconstruction | 4 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 0, 0, 0)` | 0 | 0 | verified_exact_primal_dual_after_floating_basis_reconstruction | 0 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 0, 0, 1)` | 1 | 1 | verified_exact_primal_dual_after_floating_basis_reconstruction | 1 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 0, 0, 2)` | 1 | 1 | verified_exact_primal_dual_after_floating_basis_reconstruction | 1 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 0, 1, 0)` | 1 | 1 | verified_exact_primal_dual_after_floating_basis_reconstruction | 1 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 0, 1, 1)` | 2 | 2 | verified_exact_primal_dual_after_floating_basis_reconstruction | 2 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 0, 1, 2)` | 3 | 3 | verified_exact_primal_dual_after_floating_basis_reconstruction | 3 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 0, 2, 0)` | 1 | 1 | verified_exact_primal_dual_after_floating_basis_reconstruction | 1 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 0, 2, 1)` | 2 | 2 | verified_exact_primal_dual_after_floating_basis_reconstruction | 2 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 0, 2, 2)` | 3 | 3 | verified_exact_primal_dual_after_floating_basis_reconstruction | 3 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 1, 0, 0)` | 1 | 1 | verified_exact_primal_dual_after_floating_basis_reconstruction | 1 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 1, 0, 1)` | 2 | 2 | verified_exact_primal_dual_after_floating_basis_reconstruction | 2 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 1, 0, 2)` | 3 | 3 | verified_exact_primal_dual_after_floating_basis_reconstruction | 3 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 1, 1, 0)` | 2 | 2 | verified_exact_primal_dual_after_floating_basis_reconstruction | 2 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 1, 1, 1)` | 4 | 4 | verified_exact_primal_dual_after_floating_basis_reconstruction | 4 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 1, 1, 2)` | 5 | 5 | verified_exact_primal_dual_after_floating_basis_reconstruction | 5 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 1, 2, 0)` | 3 | 3 | verified_exact_primal_dual_after_floating_basis_reconstruction | 3 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 1, 2, 1)` | 4 | 4 | verified_exact_primal_dual_after_floating_basis_reconstruction | 4 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 1, 2, 2)` | 5 | 5 | verified_exact_primal_dual_after_floating_basis_reconstruction | 5 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 2, 0, 0)` | 1 | 1 | verified_exact_primal_dual_after_floating_basis_reconstruction | 1 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 2, 0, 1)` | 2 | 2 | verified_exact_primal_dual_after_floating_basis_reconstruction | 2 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 2, 0, 2)` | 3 | 3 | verified_exact_primal_dual_after_floating_basis_reconstruction | 3 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 2, 1, 0)` | 2 | 2 | verified_exact_primal_dual_after_floating_basis_reconstruction | 2 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 2, 1, 1)` | 4 | 4 | verified_exact_primal_dual_after_floating_basis_reconstruction | 4 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 2, 1, 2)` | 5 | 5 | verified_exact_primal_dual_after_floating_basis_reconstruction | 5 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 2, 2, 0)` | 3 | 3 | verified_exact_primal_dual_after_floating_basis_reconstruction | 3 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 2, 2, 1)` | 5 | 5 | verified_exact_primal_dual_after_floating_basis_reconstruction | 5 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(1, 2, 2, 2)` | 6 | 6 | verified_exact_primal_dual_after_floating_basis_reconstruction | 6 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 0, 0, 0)` | 0 | 0 | verified_exact_primal_dual_after_floating_basis_reconstruction | 0 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 0, 0, 1)` | 1 | 1 | verified_exact_primal_dual_after_floating_basis_reconstruction | 1 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 0, 0, 2)` | 2 | 2 | verified_exact_primal_dual_after_floating_basis_reconstruction | 2 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 0, 1, 0)` | 1 | 1 | verified_exact_primal_dual_after_floating_basis_reconstruction | 1 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 0, 1, 1)` | 3 | 3 | verified_exact_primal_dual_after_floating_basis_reconstruction | 3 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 0, 1, 2)` | 4 | 4 | verified_exact_primal_dual_after_floating_basis_reconstruction | 4 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 0, 2, 0)` | 2 | 2 | verified_exact_primal_dual_after_floating_basis_reconstruction | 2 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 0, 2, 1)` | 3 | 3 | verified_exact_primal_dual_after_floating_basis_reconstruction | 3 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 0, 2, 2)` | 4 | 4 | verified_exact_primal_dual_after_floating_basis_reconstruction | 4 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 1, 0, 0)` | 1 | 1 | verified_exact_primal_dual_after_floating_basis_reconstruction | 1 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 1, 0, 1)` | 3 | 3 | verified_exact_primal_dual_after_floating_basis_reconstruction | 3 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 1, 0, 2)` | 4 | 4 | verified_exact_primal_dual_after_floating_basis_reconstruction | 4 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 1, 1, 0)` | 3 | 3 | verified_exact_primal_dual_after_floating_basis_reconstruction | 3 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 1, 1, 1)` | 5 | 5 | verified_exact_primal_dual_after_floating_basis_reconstruction | 5 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 1, 1, 2)` | 6 | 6 | verified_exact_primal_dual_after_floating_basis_reconstruction | 6 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 1, 2, 0)` | 4 | 4 | verified_exact_primal_dual_after_floating_basis_reconstruction | 4 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 1, 2, 1)` | 5 | 5 | verified_exact_primal_dual_after_floating_basis_reconstruction | 5 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 1, 2, 2)` | 6 | 6 | verified_exact_primal_dual_after_floating_basis_reconstruction | 6 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 2, 0, 0)` | 2 | 2 | verified_exact_primal_dual_after_floating_basis_reconstruction | 2 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 2, 0, 1)` | 3 | 3 | verified_exact_primal_dual_after_floating_basis_reconstruction | 3 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 2, 0, 2)` | 4 | 4 | verified_exact_primal_dual_after_floating_basis_reconstruction | 4 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 2, 1, 0)` | 3 | 3 | verified_exact_primal_dual_after_floating_basis_reconstruction | 3 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 2, 1, 1)` | 5 | 5 | verified_exact_primal_dual_after_floating_basis_reconstruction | 5 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 2, 1, 2)` | 6 | 6 | verified_exact_primal_dual_after_floating_basis_reconstruction | 6 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 2, 2, 0)` | 4 | 4 | verified_exact_primal_dual_after_floating_basis_reconstruction | 4 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 2, 2, 1)` | 6 | 6 | verified_exact_primal_dual_after_floating_basis_reconstruction | 6 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(1,1) | small_int_leq_2 | `(2, 2, 2, 2)` | 8 | 8 | verified_exact_primal_dual_after_floating_basis_reconstruction | 8 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(2,1) | one_heavy_left_leaf | `(8, 1, 1, 1, 1)` | 8 | 8 | verified_exact_primal_dual_after_floating_basis_reconstruction | 8 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(2,1) | one_heavy_right_leaf | `(1, 1, 1, 1, 8)` | 7 | 7 | verified_exact_primal_dual_after_floating_basis_reconstruction | 7 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(2,1) | one_heavy_leaf_each_side | `(8, 1, 1, 1, 8)` | 16 | 16 | verified_exact_primal_dual_after_floating_basis_reconstruction | 16 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(2,1) | all_left_leaves_heavy | `(8, 8, 1, 1, 1)` | 16 | 16 | verified_exact_primal_dual_after_floating_basis_reconstruction | 16 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(2,1) | left_center_heavy | `(1, 1, 8, 1, 1)` | 5 | 5 | verified_exact_primal_dual_after_floating_basis_reconstruction | 5 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(2,1) | right_center_heavy | `(1, 1, 1, 8, 1)` | 6 | 6 | verified_exact_primal_dual_after_floating_basis_reconstruction | 6 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(2,1) | both_centers_heavy | `(1, 1, 8, 8, 1)` | 12 | 12 | verified_exact_primal_dual_after_floating_basis_reconstruction | 12 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(2,1) | asym_left_center_right_leaf | `(1, 1, 6, 1, 9)` | 12 | 12 | verified_exact_primal_dual_after_floating_basis_reconstruction | 12 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(2,1) | asym_right_center_left_leaf | `(9, 1, 1, 6, 1)` | 13 | 13 | verified_exact_primal_dual_after_floating_basis_reconstruction | 13 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(2,2) | one_heavy_left_leaf | `(8, 1, 1, 1, 1, 1)` | 10 | 10 | verified_exact_primal_dual_after_floating_basis_reconstruction | 10 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(2,2) | one_heavy_right_leaf | `(1, 1, 1, 1, 8, 1)` | 10 | 10 | verified_exact_primal_dual_after_floating_basis_reconstruction | 10 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(2,2) | one_heavy_leaf_each_side | `(8, 1, 1, 1, 8, 1)` | 20 | 20 | verified_exact_primal_dual_after_floating_basis_reconstruction | 20 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(2,2) | all_left_leaves_heavy | `(8, 8, 1, 1, 1, 1)` | 19 | 19 | verified_exact_primal_dual_after_floating_basis_reconstruction | 19 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(2,2) | all_right_leaves_heavy | `(1, 1, 1, 1, 8, 8)` | 19 | 19 | verified_exact_primal_dual_after_floating_basis_reconstruction | 19 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(2,2) | left_center_heavy | `(1, 1, 8, 1, 1, 1)` | 7 | 7 | verified_exact_primal_dual_after_floating_basis_reconstruction | 7 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(2,2) | right_center_heavy | `(1, 1, 1, 8, 1, 1)` | 7 | 7 | verified_exact_primal_dual_after_floating_basis_reconstruction | 7 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(2,2) | both_centers_heavy | `(1, 1, 8, 8, 1, 1)` | 14 | 14 | verified_exact_primal_dual_after_floating_basis_reconstruction | 14 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(2,2) | asym_left_center_right_leaf | `(1, 1, 6, 1, 9, 1)` | 15 | 15 | verified_exact_primal_dual_after_floating_basis_reconstruction | 15 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(2,2) | asym_right_center_left_leaf | `(9, 1, 1, 6, 1, 1)` | 15 | 15 | verified_exact_primal_dual_after_floating_basis_reconstruction | 15 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,1) | one_heavy_left_leaf | `(8, 1, 1, 1, 1, 1)` | 10 | 10 | verified_exact_primal_dual_after_floating_basis_reconstruction | 10 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,1) | one_heavy_right_leaf | `(1, 1, 1, 1, 1, 8)` | 9 | 9 | verified_exact_primal_dual_after_floating_basis_reconstruction | 9 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,1) | one_heavy_leaf_each_side | `(8, 1, 1, 1, 1, 8)` | 19 | 19 | verified_exact_primal_dual_after_floating_basis_reconstruction | 19 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,1) | all_left_leaves_heavy | `(8, 8, 8, 1, 1, 1)` | 27 | 27 | verified_exact_primal_dual_after_floating_basis_reconstruction | 27 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,1) | left_center_heavy | `(1, 1, 1, 8, 1, 1)` | 6 | 6 | verified_exact_primal_dual_after_floating_basis_reconstruction | 6 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,1) | right_center_heavy | `(1, 1, 1, 1, 8, 1)` | 8 | 8 | verified_exact_primal_dual_after_floating_basis_reconstruction | 8 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,1) | both_centers_heavy | `(1, 1, 1, 8, 8, 1)` | 13 | 13 | verified_exact_primal_dual_after_floating_basis_reconstruction | 13 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,1) | asym_left_center_right_leaf | `(1, 1, 1, 6, 1, 9)` | 14 | 14 | verified_exact_primal_dual_after_floating_basis_reconstruction | 14 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,1) | asym_right_center_left_leaf | `(9, 1, 1, 1, 6, 1)` | 16 | 16 | verified_exact_primal_dual_after_floating_basis_reconstruction | 16 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,2) | one_heavy_left_leaf | `(8, 1, 1, 1, 1, 1, 1)` | 13 | 13 | verified_exact_primal_dual_after_floating_basis_reconstruction | 13 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,2) | one_heavy_right_leaf | `(1, 1, 1, 1, 1, 8, 1)` | 12 | 12 | verified_exact_primal_dual_after_floating_basis_reconstruction | 12 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,2) | one_heavy_leaf_each_side | `(8, 1, 1, 1, 1, 8, 1)` | 23 | 23 | verified_exact_primal_dual_after_floating_basis_reconstruction | 23 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,2) | all_left_leaves_heavy | `(8, 8, 8, 1, 1, 1, 1)` | 29 | 29 | verified_exact_primal_dual_after_floating_basis_reconstruction | 29 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,2) | all_right_leaves_heavy | `(1, 1, 1, 1, 1, 8, 8)` | 22 | 22 | verified_exact_primal_dual_after_floating_basis_reconstruction | 22 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,2) | left_center_heavy | `(1, 1, 1, 8, 1, 1, 1)` | 8 | 8 | verified_exact_primal_dual_after_floating_basis_reconstruction | 8 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,2) | right_center_heavy | `(1, 1, 1, 1, 8, 1, 1)` | 9 | 9 | verified_exact_primal_dual_after_floating_basis_reconstruction | 9 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,2) | both_centers_heavy | `(1, 1, 1, 8, 8, 1, 1)` | 15 | 15 | verified_exact_primal_dual_after_floating_basis_reconstruction | 15 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,2) | asym_left_center_right_leaf | `(1, 1, 1, 6, 1, 9, 1)` | 17 | 17 | verified_exact_primal_dual_after_floating_basis_reconstruction | 17 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,2) | asym_right_center_left_leaf | `(9, 1, 1, 1, 6, 1, 1)` | 18 | 18 | verified_exact_primal_dual_after_floating_basis_reconstruction | 18 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,3) | one_heavy_left_leaf | `(8, 1, 1, 1, 1, 1, 1, 1)` | 15 | 15 | verified_exact_primal_dual_after_floating_basis_reconstruction | 15 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,3) | one_heavy_right_leaf | `(1, 1, 1, 1, 1, 8, 1, 1)` | 15 | 15 | verified_exact_primal_dual_after_floating_basis_reconstruction | 15 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,3) | one_heavy_leaf_each_side | `(8, 1, 1, 1, 1, 8, 1, 1)` | 26 | 26 | verified_exact_primal_dual_after_floating_basis_reconstruction | 26 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,3) | all_left_leaves_heavy | `(8, 8, 8, 1, 1, 1, 1, 1)` | 31 | 31 | verified_exact_primal_dual_after_floating_basis_reconstruction | 31 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,3) | all_right_leaves_heavy | `(1, 1, 1, 1, 1, 8, 8, 8)` | 31 | 31 | verified_exact_primal_dual_after_floating_basis_reconstruction | 31 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,3) | left_center_heavy | `(1, 1, 1, 8, 1, 1, 1, 1)` | 10 | 10 | verified_exact_primal_dual_after_floating_basis_reconstruction | 10 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,3) | right_center_heavy | `(1, 1, 1, 1, 8, 1, 1, 1)` | 10 | 10 | verified_exact_primal_dual_after_floating_basis_reconstruction | 10 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,3) | both_centers_heavy | `(1, 1, 1, 8, 8, 1, 1, 1)` | 17 | 17 | verified_exact_primal_dual_after_floating_basis_reconstruction | 17 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,3) | asym_left_center_right_leaf | `(1, 1, 1, 6, 1, 9, 1, 1)` | 20 | 20 | verified_exact_primal_dual_after_floating_basis_reconstruction | 20 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |
| DS(3,3) | asym_right_center_left_leaf | `(9, 1, 1, 1, 6, 1, 1, 1)` | 20 | 20 | verified_exact_primal_dual_after_floating_basis_reconstruction | 20 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal |

## Representative Reduced Variables

### DS(1,1) / one_heavy_left_leaf

- `theta = z[{a,b},a]`: `0`
- left leaf variables: `[{'leaf': 'x1', 'p_x': '1', 'r_x': '1', 'A_x': '0', 'B_x': '0'}]`
- right leaf variables: `[{'leaf': 'y1', 'q_y': '0', 's_y': '0', 'A_y': '0', 'B_y': '1'}]`
- four-set values: `[{'x': 'x1', 'y': 'y1', 'z_x': '1', 'z_a': '0', 'z_b': '0', 'z_y': '0'}]`

### DS(2,1) / one_heavy_left_leaf

- `theta = z[{a,b},a]`: `1`
- left leaf variables: `[{'leaf': 'x1', 'p_x': '1', 'r_x': '1', 'A_x': '0', 'B_x': '0'}, {'leaf': 'x2', 'p_x': '0', 'r_x': '0', 'A_x': '1', 'B_x': '0'}]`
- right leaf variables: `[{'leaf': 'y1', 'q_y': '0', 's_y': '0', 'A_y': '1', 'B_y': '0'}]`
- four-set values: `[{'x': 'x1', 'y': 'y1', 'z_x': '1', 'z_a': '0', 'z_b': '0', 'z_y': '0'}, {'x': 'x2', 'y': 'y1', 'z_x': '0', 'z_a': '1', 'z_b': '0', 'z_y': '0'}]`

### DS(2,2) / one_heavy_left_leaf

- `theta = z[{a,b},a]`: `0`
- left leaf variables: `[{'leaf': 'x1', 'p_x': '1', 'r_x': '1', 'A_x': '0', 'B_x': '0'}, {'leaf': 'x2', 'p_x': '1', 'r_x': '0', 'A_x': '0', 'B_x': '1'}]`
- right leaf variables: `[{'leaf': 'y1', 'q_y': '0', 's_y': '0', 'A_y': '0', 'B_y': '1'}, {'leaf': 'y2', 'q_y': '0', 's_y': '0', 'A_y': '0', 'B_y': '1'}]`
- four-set values: `[{'x': 'x1', 'y': 'y1', 'z_x': '1', 'z_a': '0', 'z_b': '0', 'z_y': '0'}, {'x': 'x1', 'y': 'y2', 'z_x': '1', 'z_a': '0', 'z_b': '0', 'z_y': '0'}, {'x': 'x2', 'y': 'y1', 'z_x': '0', 'z_a': '0', 'z_b': '1', 'z_y': '0'}, {'x': 'x2', 'y': 'y2', 'z_x': '0', 'z_a': '0', 'z_b': '1', 'z_y': '0'}]`

### DS(3,1) / one_heavy_left_leaf

- `theta = z[{a,b},a]`: `1`
- left leaf variables: `[{'leaf': 'x1', 'p_x': '1', 'r_x': '1', 'A_x': '0', 'B_x': '0'}, {'leaf': 'x2', 'p_x': '0', 'r_x': '0', 'A_x': '1', 'B_x': '0'}, {'leaf': 'x3', 'p_x': '0', 'r_x': '0', 'A_x': '1', 'B_x': '0'}]`
- right leaf variables: `[{'leaf': 'y1', 'q_y': '0', 's_y': '0', 'A_y': '1', 'B_y': '0'}]`
- four-set values: `[{'x': 'x1', 'y': 'y1', 'z_x': '1', 'z_a': '0', 'z_b': '0', 'z_y': '0'}, {'x': 'x2', 'y': 'y1', 'z_x': '0', 'z_a': '1', 'z_b': '0', 'z_y': '0'}, {'x': 'x3', 'y': 'y1', 'z_x': '0', 'z_a': '1', 'z_b': '0', 'z_y': '0'}]`

### DS(3,2) / one_heavy_left_leaf

- `theta = z[{a,b},a]`: `0`
- left leaf variables: `[{'leaf': 'x1', 'p_x': '1', 'r_x': '1', 'A_x': '0', 'B_x': '0'}, {'leaf': 'x2', 'p_x': '0', 'r_x': '0', 'A_x': '0', 'B_x': '1'}, {'leaf': 'x3', 'p_x': '0', 'r_x': '0', 'A_x': '0', 'B_x': '1'}]`
- right leaf variables: `[{'leaf': 'y1', 'q_y': '0', 's_y': '0', 'A_y': '0', 'B_y': '1'}, {'leaf': 'y2', 'q_y': '0', 's_y': '0', 'A_y': '0', 'B_y': '1'}]`
- four-set values: `[{'x': 'x1', 'y': 'y1', 'z_x': '1', 'z_a': '0', 'z_b': '0', 'z_y': '0'}, {'x': 'x1', 'y': 'y2', 'z_x': '1', 'z_a': '0', 'z_b': '0', 'z_y': '0'}, {'x': 'x2', 'y': 'y1', 'z_x': '0', 'z_a': '0', 'z_b': '1', 'z_y': '0'}, {'x': 'x2', 'y': 'y2', 'z_x': '0', 'z_a': '0', 'z_b': '1', 'z_y': '0'}, {'x': 'x3', 'y': 'y1', 'z_x': '0', 'z_a': '0', 'z_b': '1', 'z_y': '0'}, {'x': 'x3', 'y': 'y2', 'z_x': '0', 'z_a': '0', 'z_b': '1', 'z_y': '0'}]`

### DS(3,3) / one_heavy_left_leaf

- `theta = z[{a,b},a]`: `0`
- left leaf variables: `[{'leaf': 'x1', 'p_x': '1', 'r_x': '1', 'A_x': '0', 'B_x': '0'}, {'leaf': 'x2', 'p_x': '0', 'r_x': '0', 'A_x': '0', 'B_x': '1'}, {'leaf': 'x3', 'p_x': '0', 'r_x': '0', 'A_x': '0', 'B_x': '1'}]`
- right leaf variables: `[{'leaf': 'y1', 'q_y': '0', 's_y': '0', 'A_y': '0', 'B_y': '1'}, {'leaf': 'y2', 'q_y': '0', 's_y': '0', 'A_y': '0', 'B_y': '1'}, {'leaf': 'y3', 'q_y': '0', 's_y': '0', 'A_y': '0', 'B_y': '1'}]`
- four-set values: `[{'x': 'x1', 'y': 'y1', 'z_x': '1', 'z_a': '0', 'z_b': '0', 'z_y': '0'}, {'x': 'x1', 'y': 'y2', 'z_x': '1', 'z_a': '0', 'z_b': '0', 'z_y': '0'}, {'x': 'x1', 'y': 'y3', 'z_x': '1', 'z_a': '0', 'z_b': '0', 'z_y': '0'}, {'x': 'x2', 'y': 'y1', 'z_x': '0', 'z_a': '0', 'z_b': '1', 'z_y': '0'}, {'x': 'x2', 'y': 'y2', 'z_x': '0', 'z_a': '0', 'z_b': '1', 'z_y': '0'}, {'x': 'x2', 'y': 'y3', 'z_x': '0', 'z_a': '0', 'z_b': '1', 'z_y': '0'}, {'x': 'x3', 'y': 'y1', 'z_x': '0', 'z_a': '0', 'z_b': '1', 'z_y': '0'}, {'x': 'x3', 'y': 'y2', 'z_x': '0', 'z_a': '0', 'z_b': '1', 'z_y': '0'}, {'x': 'x3', 'y': 'y3', 'z_x': '0', 'z_a': '0', 'z_b': '1', 'z_y': '0'}]`

## Representative H1 Dual Rows

Because every H1 optimum matched the STT baseline, H2 optima are certified by the `H1 <= H2 <= STT` sandwich.  The reduced H1 proof-pattern fitting attempt therefore starts from exact H1 dual multipliers rather than H2 repair rows.

- `DS(1,1)` / `one_heavy_left_leaf` active H1 dual rows, first few nonzero multipliers: `[{'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [0, 1]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [2, 3]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [0, 1, 2]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [1, 2, 3]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [0, 1, 2, 3]}}, {'value': '1', 'orbit_size': 1, 'kind': 'heredity', 'row': {'kind': 'heredity', 'superset': [0, 1, 2], 'subset': [0, 1], 'root': 1}}, {'value': '1', 'orbit_size': 1, 'kind': 'heredity', 'row': {'kind': 'heredity', 'superset': [1, 2, 3], 'subset': [1, 2], 'root': 2}}, {'value': '1', 'orbit_size': 1, 'kind': 'heredity', 'row': {'kind': 'heredity', 'superset': [0, 1, 2, 3], 'subset': [0, 1], 'root': 1}}]`.
- `DS(2,1)` / `one_heavy_left_leaf` active H1 dual rows, first few nonzero multipliers: `[{'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [0, 2]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [1, 2]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [3, 4]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [0, 1, 2]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [0, 2, 3]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [1, 2, 3]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [2, 3, 4]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [0, 2, 3, 4]}}]`.
- `DS(2,2)` / `one_heavy_left_leaf` active H1 dual rows, first few nonzero multipliers: `[{'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [0, 2]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [1, 2]}}, {'value': '1', 'orbit_size': 2, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [3, 4]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [0, 1, 2]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [0, 2, 3]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [1, 2, 3]}}, {'value': '1', 'orbit_size': 2, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [2, 3, 4]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [3, 4, 5]}}]`.
- `DS(3,1)` / `one_heavy_left_leaf` active H1 dual rows, first few nonzero multipliers: `[{'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [0, 3]}}, {'value': '2', 'orbit_size': 2, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [1, 3]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_upper', 'row': {'kind': 'simplex_upper', 'component': [3, 4]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [4, 5]}}, {'value': '2', 'orbit_size': 2, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [0, 1, 3]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [0, 3, 4]}}, {'value': '2', 'orbit_size': 2, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [1, 3, 4]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [3, 4, 5]}}]`.
- `DS(3,2)` / `one_heavy_left_leaf` active H1 dual rows, first few nonzero multipliers: `[{'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [0, 3]}}, {'value': '2', 'orbit_size': 2, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [1, 3]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [3, 4]}}, {'value': '1', 'orbit_size': 2, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [4, 5]}}, {'value': '2', 'orbit_size': 2, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [0, 1, 3]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [0, 3, 4]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [4, 5, 6]}}, {'value': '2', 'orbit_size': 2, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [0, 3, 4, 5]}}]`.
- `DS(3,3)` / `one_heavy_left_leaf` active H1 dual rows, first few nonzero multipliers: `[{'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [0, 3]}}, {'value': '2', 'orbit_size': 2, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [1, 3]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [3, 4]}}, {'value': '3', 'orbit_size': 3, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [4, 5]}}, {'value': '2', 'orbit_size': 2, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [0, 1, 3]}}, {'value': '1', 'orbit_size': 1, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [0, 3, 4]}}, {'value': '3', 'orbit_size': 3, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [0, 3, 4, 5]}}, {'value': '2', 'orbit_size': 6, 'kind': 'simplex_lower', 'row': {'kind': 'simplex_lower', 'component': [1, 3, 4, 5]}}]`.

Observed finite pattern: after quotienting by weight-preserving left/right leaf permutations, nonzero H1 dual rows are simplex rows plus heredity rows on path components touching the center edge or the heavy side.  This is a useful target for the reduced H1 proof pattern, but it is not a checked symbolic proof and is not promoted as double-star exactness.

## Four-Set H2 Rectangles

- `DS(1,1)` relevant four-set rectangles on `{x,a,b,y}`, grouped by root: `{'a': 3, 'b': 3}`.
- `DS(2,1)` relevant four-set rectangles on `{x,a,b,y}`, grouped by root: `{'a': 6, 'b': 6}`.
- `DS(2,2)` relevant four-set rectangles on `{x,a,b,y}`, grouped by root: `{'a': 12, 'b': 12}`.
- `DS(3,1)` relevant four-set rectangles on `{x,a,b,y}`, grouped by root: `{'a': 9, 'b': 9}`.
- `DS(3,2)` relevant four-set rectangles on `{x,a,b,y}`, grouped by root: `{'a': 18, 'b': 18}`.
- `DS(3,3)` relevant four-set rectangles on `{x,a,b,y}`, grouped by root: `{'a': 27, 'b': 27}`.

No H2 repair was needed in these runs because no H1 depth gap was found; consequently there are no active H2 repair rectangles to list.

## Skeptical Audit

- A no-gap finite run is not a proof of double-star exactness.
- DS(3,3) H2 is feasible here only because the structured objectives permit weight-preserving symmetry reduction; arbitrary asymmetric objectives remain out of scope.
- Full-`z` failure and depth-projection failure are kept separate: this report only compares projected weighted depth objectives.
- Before promoting any theorem claim, the reduced H1 proof pattern from the theory note still has to be fitted symbolically.
