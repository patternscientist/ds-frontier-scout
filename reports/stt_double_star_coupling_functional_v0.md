# STT Double-Star Coupling Functional v0

## Scope

This is a targeted proof-route test of the reduced global coupling functional `LB_H1(theta,p,q,r,s)` on double-stars. It is not a broad almost-star sweep and it does not test H3/H4.

The tested topologies are `DS(1,1)`, `DS(2,1)`, `DS(2,2)`, `DS(3,1)`, `DS(3,2)`. Structured nonnegative weights reuse the previous double-star families, including all small integer weights through the configured bound on `DS(1,1)`.

## Outcome

No reduced `LB_H1 < STT` counterexample was found in the tested cases.

No full H1 depth-projection gap appeared in the same tested cases.
No full H2 depth-projection gap appeared; when H1 matched STT, H2 was certified by sandwiching.

## Solve Table

| topology | family | weights | STT | reduced LB_H1 min | gap | full H1 | full H2 |
|---|---|---:|---:|---:|---:|---:|---:|
| DS(1,1) | one_heavy_left_leaf | `(x1=8, a=1, b=1, y1=1)` | 5 | 5 | 0 | 5 | 5 |
| DS(1,1) | one_heavy_right_leaf | `(x1=1, a=1, b=1, y1=8)` | 5 | 5 | 0 | 5 | 5 |
| DS(1,1) | one_heavy_leaf_each_side | `(x1=8, a=1, b=1, y1=8)` | 13 | 13 | 0 | 13 | 13 |
| DS(1,1) | left_center_heavy | `(x1=1, a=8, b=1, y1=1)` | 4 | 4 | 0 | 4 | 4 |
| DS(1,1) | right_center_heavy | `(x1=1, a=1, b=8, y1=1)` | 4 | 4 | 0 | 4 | 4 |
| DS(1,1) | both_centers_heavy | `(x1=1, a=8, b=8, y1=1)` | 11 | 11 | 0 | 11 | 11 |
| DS(1,1) | asym_left_center_right_leaf | `(x1=1, a=6, b=1, y1=9)` | 10 | 10 | 0 | 10 | 10 |
| DS(1,1) | asym_right_center_left_leaf | `(x1=9, a=1, b=6, y1=1)` | 10 | 10 | 0 | 10 | 10 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=0, b=0, y1=1)` | 0 | 0 | 0 | 0 | 0 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=0, b=0, y1=2)` | 0 | 0 | 0 | 0 | 0 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=0, b=1, y1=0)` | 0 | 0 | 0 | 0 | 0 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=0, b=1, y1=1)` | 1 | 1 | 0 | 1 | 1 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=0, b=1, y1=2)` | 1 | 1 | 0 | 1 | 1 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=0, b=2, y1=0)` | 0 | 0 | 0 | 0 | 0 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=0, b=2, y1=1)` | 1 | 1 | 0 | 1 | 1 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=0, b=2, y1=2)` | 2 | 2 | 0 | 2 | 2 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=1, b=0, y1=0)` | 0 | 0 | 0 | 0 | 0 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=1, b=0, y1=1)` | 1 | 1 | 0 | 1 | 1 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=1, b=0, y1=2)` | 1 | 1 | 0 | 1 | 1 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=1, b=1, y1=0)` | 1 | 1 | 0 | 1 | 1 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=1, b=1, y1=1)` | 2 | 2 | 0 | 2 | 2 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=1, b=1, y1=2)` | 3 | 3 | 0 | 3 | 3 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=1, b=2, y1=0)` | 1 | 1 | 0 | 1 | 1 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=1, b=2, y1=1)` | 2 | 2 | 0 | 2 | 2 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=1, b=2, y1=2)` | 3 | 3 | 0 | 3 | 3 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=2, b=0, y1=0)` | 0 | 0 | 0 | 0 | 0 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=2, b=0, y1=1)` | 1 | 1 | 0 | 1 | 1 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=2, b=0, y1=2)` | 2 | 2 | 0 | 2 | 2 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=2, b=1, y1=0)` | 1 | 1 | 0 | 1 | 1 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=2, b=1, y1=1)` | 3 | 3 | 0 | 3 | 3 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=2, b=1, y1=2)` | 4 | 4 | 0 | 4 | 4 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=2, b=2, y1=0)` | 2 | 2 | 0 | 2 | 2 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=2, b=2, y1=1)` | 3 | 3 | 0 | 3 | 3 |
| DS(1,1) | small_int_leq_2 | `(x1=0, a=2, b=2, y1=2)` | 4 | 4 | 0 | 4 | 4 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=0, b=0, y1=0)` | 0 | 0 | 0 | 0 | 0 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=0, b=0, y1=1)` | 1 | 1 | 0 | 1 | 1 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=0, b=0, y1=2)` | 1 | 1 | 0 | 1 | 1 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=0, b=1, y1=0)` | 1 | 1 | 0 | 1 | 1 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=0, b=1, y1=1)` | 2 | 2 | 0 | 2 | 2 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=0, b=1, y1=2)` | 3 | 3 | 0 | 3 | 3 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=0, b=2, y1=0)` | 1 | 1 | 0 | 1 | 1 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=0, b=2, y1=1)` | 2 | 2 | 0 | 2 | 2 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=0, b=2, y1=2)` | 3 | 3 | 0 | 3 | 3 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=1, b=0, y1=0)` | 1 | 1 | 0 | 1 | 1 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=1, b=0, y1=1)` | 2 | 2 | 0 | 2 | 2 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=1, b=0, y1=2)` | 3 | 3 | 0 | 3 | 3 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=1, b=1, y1=0)` | 2 | 2 | 0 | 2 | 2 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=1, b=1, y1=1)` | 4 | 4 | 0 | 4 | 4 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=1, b=1, y1=2)` | 5 | 5 | 0 | 5 | 5 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=1, b=2, y1=0)` | 3 | 3 | 0 | 3 | 3 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=1, b=2, y1=1)` | 4 | 4 | 0 | 4 | 4 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=1, b=2, y1=2)` | 5 | 5 | 0 | 5 | 5 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=2, b=0, y1=0)` | 1 | 1 | 0 | 1 | 1 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=2, b=0, y1=1)` | 2 | 2 | 0 | 2 | 2 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=2, b=0, y1=2)` | 3 | 3 | 0 | 3 | 3 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=2, b=1, y1=0)` | 2 | 2 | 0 | 2 | 2 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=2, b=1, y1=1)` | 4 | 4 | 0 | 4 | 4 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=2, b=1, y1=2)` | 5 | 5 | 0 | 5 | 5 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=2, b=2, y1=0)` | 3 | 3 | 0 | 3 | 3 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=2, b=2, y1=1)` | 5 | 5 | 0 | 5 | 5 |
| DS(1,1) | small_int_leq_2 | `(x1=1, a=2, b=2, y1=2)` | 6 | 6 | 0 | 6 | 6 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=0, b=0, y1=0)` | 0 | 0 | 0 | 0 | 0 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=0, b=0, y1=1)` | 1 | 1 | 0 | 1 | 1 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=0, b=0, y1=2)` | 2 | 2 | 0 | 2 | 2 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=0, b=1, y1=0)` | 1 | 1 | 0 | 1 | 1 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=0, b=1, y1=1)` | 3 | 3 | 0 | 3 | 3 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=0, b=1, y1=2)` | 4 | 4 | 0 | 4 | 4 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=0, b=2, y1=0)` | 2 | 2 | 0 | 2 | 2 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=0, b=2, y1=1)` | 3 | 3 | 0 | 3 | 3 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=0, b=2, y1=2)` | 4 | 4 | 0 | 4 | 4 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=1, b=0, y1=0)` | 1 | 1 | 0 | 1 | 1 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=1, b=0, y1=1)` | 3 | 3 | 0 | 3 | 3 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=1, b=0, y1=2)` | 4 | 4 | 0 | 4 | 4 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=1, b=1, y1=0)` | 3 | 3 | 0 | 3 | 3 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=1, b=1, y1=1)` | 5 | 5 | 0 | 5 | 5 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=1, b=1, y1=2)` | 6 | 6 | 0 | 6 | 6 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=1, b=2, y1=0)` | 4 | 4 | 0 | 4 | 4 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=1, b=2, y1=1)` | 5 | 5 | 0 | 5 | 5 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=1, b=2, y1=2)` | 6 | 6 | 0 | 6 | 6 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=2, b=0, y1=0)` | 2 | 2 | 0 | 2 | 2 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=2, b=0, y1=1)` | 3 | 3 | 0 | 3 | 3 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=2, b=0, y1=2)` | 4 | 4 | 0 | 4 | 4 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=2, b=1, y1=0)` | 3 | 3 | 0 | 3 | 3 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=2, b=1, y1=1)` | 5 | 5 | 0 | 5 | 5 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=2, b=1, y1=2)` | 6 | 6 | 0 | 6 | 6 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=2, b=2, y1=0)` | 4 | 4 | 0 | 4 | 4 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=2, b=2, y1=1)` | 6 | 6 | 0 | 6 | 6 |
| DS(1,1) | small_int_leq_2 | `(x1=2, a=2, b=2, y1=2)` | 8 | 8 | 0 | 8 | 8 |
| DS(2,1) | one_heavy_left_leaf | `(x1=8, x2=1, a=1, b=1, y1=1)` | 8 | 8 | 0 | 8 | 8 |
| DS(2,1) | one_heavy_right_leaf | `(x1=1, x2=1, a=1, b=1, y1=8)` | 7 | 7 | 0 | 7 | 7 |
| DS(2,1) | one_heavy_leaf_each_side | `(x1=8, x2=1, a=1, b=1, y1=8)` | 16 | 16 | 0 | 16 | 16 |
| DS(2,1) | all_left_leaves_heavy | `(x1=8, x2=8, a=1, b=1, y1=1)` | 16 | 16 | 0 | 16 | 16 |
| DS(2,1) | left_center_heavy | `(x1=1, x2=1, a=8, b=1, y1=1)` | 5 | 5 | 0 | 5 | 5 |
| DS(2,1) | right_center_heavy | `(x1=1, x2=1, a=1, b=8, y1=1)` | 6 | 6 | 0 | 6 | 6 |
| DS(2,1) | both_centers_heavy | `(x1=1, x2=1, a=8, b=8, y1=1)` | 12 | 12 | 0 | 12 | 12 |
| DS(2,1) | asym_left_center_right_leaf | `(x1=1, x2=1, a=6, b=1, y1=9)` | 12 | 12 | 0 | 12 | 12 |
| DS(2,1) | asym_right_center_left_leaf | `(x1=9, x2=1, a=1, b=6, y1=1)` | 13 | 13 | 0 | 13 | 13 |
| DS(2,2) | one_heavy_left_leaf | `(x1=8, x2=1, a=1, b=1, y1=1, y2=1)` | 10 | 10 | 0 | 10 | 10 |
| DS(2,2) | one_heavy_right_leaf | `(x1=1, x2=1, a=1, b=1, y1=8, y2=1)` | 10 | 10 | 0 | 10 | 10 |
| DS(2,2) | one_heavy_leaf_each_side | `(x1=8, x2=1, a=1, b=1, y1=8, y2=1)` | 20 | 20 | 0 | 20 | 20 |
| DS(2,2) | all_left_leaves_heavy | `(x1=8, x2=8, a=1, b=1, y1=1, y2=1)` | 19 | 19 | 0 | 19 | 19 |
| DS(2,2) | all_right_leaves_heavy | `(x1=1, x2=1, a=1, b=1, y1=8, y2=8)` | 19 | 19 | 0 | 19 | 19 |
| DS(2,2) | left_center_heavy | `(x1=1, x2=1, a=8, b=1, y1=1, y2=1)` | 7 | 7 | 0 | 7 | 7 |
| DS(2,2) | right_center_heavy | `(x1=1, x2=1, a=1, b=8, y1=1, y2=1)` | 7 | 7 | 0 | 7 | 7 |
| DS(2,2) | both_centers_heavy | `(x1=1, x2=1, a=8, b=8, y1=1, y2=1)` | 14 | 14 | 0 | 14 | 14 |
| DS(2,2) | asym_left_center_right_leaf | `(x1=1, x2=1, a=6, b=1, y1=9, y2=1)` | 15 | 15 | 0 | 15 | 15 |
| DS(2,2) | asym_right_center_left_leaf | `(x1=9, x2=1, a=1, b=6, y1=1, y2=1)` | 15 | 15 | 0 | 15 | 15 |
| DS(3,1) | one_heavy_left_leaf | `(x1=8, x2=1, x3=1, a=1, b=1, y1=1)` | 10 | 10 | 0 | 10 | 10 |
| DS(3,1) | one_heavy_right_leaf | `(x1=1, x2=1, x3=1, a=1, b=1, y1=8)` | 9 | 9 | 0 | 9 | 9 |
| DS(3,1) | one_heavy_leaf_each_side | `(x1=8, x2=1, x3=1, a=1, b=1, y1=8)` | 19 | 19 | 0 | 19 | 19 |
| DS(3,1) | all_left_leaves_heavy | `(x1=8, x2=8, x3=8, a=1, b=1, y1=1)` | 27 | 27 | 0 | 27 | 27 |
| DS(3,1) | left_center_heavy | `(x1=1, x2=1, x3=1, a=8, b=1, y1=1)` | 6 | 6 | 0 | 6 | 6 |
| DS(3,1) | right_center_heavy | `(x1=1, x2=1, x3=1, a=1, b=8, y1=1)` | 8 | 8 | 0 | 8 | 8 |
| DS(3,1) | both_centers_heavy | `(x1=1, x2=1, x3=1, a=8, b=8, y1=1)` | 13 | 13 | 0 | 13 | 13 |
| DS(3,1) | asym_left_center_right_leaf | `(x1=1, x2=1, x3=1, a=6, b=1, y1=9)` | 14 | 14 | 0 | 14 | 14 |
| DS(3,1) | asym_right_center_left_leaf | `(x1=9, x2=1, x3=1, a=1, b=6, y1=1)` | 16 | 16 | 0 | 16 | 16 |
| DS(3,2) | one_heavy_left_leaf | `(x1=8, x2=1, x3=1, a=1, b=1, y1=1, y2=1)` | 13 | 13 | 0 | 13 | 13 |
| DS(3,2) | one_heavy_right_leaf | `(x1=1, x2=1, x3=1, a=1, b=1, y1=8, y2=1)` | 12 | 12 | 0 | 12 | 12 |
| DS(3,2) | one_heavy_leaf_each_side | `(x1=8, x2=1, x3=1, a=1, b=1, y1=8, y2=1)` | 23 | 23 | 0 | 23 | 23 |
| DS(3,2) | all_left_leaves_heavy | `(x1=8, x2=8, x3=8, a=1, b=1, y1=1, y2=1)` | 29 | 29 | 0 | 29 | 29 |
| DS(3,2) | all_right_leaves_heavy | `(x1=1, x2=1, x3=1, a=1, b=1, y1=8, y2=8)` | 22 | 22 | 0 | 22 | 22 |
| DS(3,2) | left_center_heavy | `(x1=1, x2=1, x3=1, a=8, b=1, y1=1, y2=1)` | 8 | 8 | 0 | 8 | 8 |
| DS(3,2) | right_center_heavy | `(x1=1, x2=1, x3=1, a=1, b=8, y1=1, y2=1)` | 9 | 9 | 0 | 9 | 9 |
| DS(3,2) | both_centers_heavy | `(x1=1, x2=1, x3=1, a=8, b=8, y1=1, y2=1)` | 15 | 15 | 0 | 15 | 15 |
| DS(3,2) | asym_left_center_right_leaf | `(x1=1, x2=1, x3=1, a=6, b=1, y1=9, y2=1)` | 17 | 17 | 0 | 17 | 17 |
| DS(3,2) | asym_right_center_left_leaf | `(x1=9, x2=1, x3=1, a=1, b=6, y1=1, y2=1)` | 18 | 18 | 0 | 18 | 18 |

## Reduced LP Encoding

- Variables are `theta`, `p_x`, `q_y`, `r_x`, `s_y`, interval variables `A_left[x]`, `A_right[y]`, same-side endpoint variables for `Psi`, and cross-side `E_xy`, `Vx_xy`, `Vy_xy` variables for `Gamma`.
- The interval constraints encode exactly `I_x = [max(0, theta-r_x), min(1-p_x, theta, 1-r_x)]` and `J_y = [max(0, q_y-s_y, theta-s_y), min(theta, 1-s_y)]`; nonnegativity is supplied by the standard LP form.
- `Gamma` is represented by endpoint allocation constraints `0 <= Vx <= r_x`, `0 <= Vy <= s_y`, `Vx + Vy >= E`, with `E` lower-bounding the four expressions in the prompt.

## Candidate Proof Pattern

- `DS(1,1)` / `one_heavy_left_leaf` active reduced dual rows, first few nonzero multipliers: `({'row_index': 2, 'value': '6', 'row': {'kind': 'upper_unit', 'var': ['r', 0]}}, {'row_index': 6, 'value': '7', 'row': {'kind': 'left_interval_upper_one_minus_p', 'x': 'x1'}}, {'row_index': 7, 'value': '1', 'row': {'kind': 'left_interval_upper_theta', 'x': 'x1'}}, {'row_index': 14, 'value': '1', 'row': {'kind': 'right_interval_lower_theta_minus_s', 'y': 'y1'}}, {'row_index': 17, 'value': '1', 'row': {'kind': 'cross_e_ge_r', 'x': 'x1', 'y': 'y1'}}, {'row_index': 23, 'value': '1', 'row': {'kind': 'gamma_vsum_ge_e', 'x': 'x1', 'y': 'y1'}})`.
- `DS(2,1)` / `one_heavy_left_leaf` active reduced dual rows, first few nonzero multipliers: `({'row_index': 4, 'value': '6', 'row': {'kind': 'reduced_h1_r_le_p', 'x': 'x1'}}, {'row_index': 6, 'value': '12', 'row': {'kind': 'left_interval_upper_one_minus_p', 'x': 'x1'}}, {'row_index': 15, 'value': '1', 'row': {'kind': 'left_interval_upper_theta', 'x': 'x2'}}, {'row_index': 22, 'value': '1', 'row': {'kind': 'right_interval_lower_theta_minus_s', 'y': 'y1'}}, {'row_index': 27, 'value': '1', 'row': {'kind': 'psi_sum_ge_first_mass', 'side': 'left', 'first': 'x1', 'second': 'x2'}}, {'row_index': 29, 'value': '1', 'row': {'kind': 'cross_e_ge_r', 'x': 'x1', 'y': 'y1'}}, {'row_index': 35, 'value': '1', 'row': {'kind': 'gamma_vsum_ge_e', 'x': 'x1', 'y': 'y1'}})`.
- `DS(2,2)` / `one_heavy_left_leaf` active reduced dual rows, first few nonzero multipliers: `({'row_index': 1, 'value': '4', 'row': {'kind': 'upper_unit', 'var': ['p', 0]}}, {'row_index': 4, 'value': '5', 'row': {'kind': 'reduced_h1_r_le_p', 'x': 'x1'}}, {'row_index': 6, 'value': '7', 'row': {'kind': 'left_interval_upper_one_minus_p', 'x': 'x1'}}, {'row_index': 7, 'value': '1', 'row': {'kind': 'left_interval_upper_theta', 'x': 'x1'}}, {'row_index': 15, 'value': '1', 'row': {'kind': 'left_interval_upper_theta', 'x': 'x2'}}, {'row_index': 22, 'value': '1', 'row': {'kind': 'right_interval_lower_theta_minus_s', 'y': 'y1'}}, {'row_index': 30, 'value': '1', 'row': {'kind': 'right_interval_lower_theta_minus_s', 'y': 'y2'}}, {'row_index': 35, 'value': '1', 'row': {'kind': 'psi_sum_ge_first_mass', 'side': 'left', 'first': 'x1', 'second': 'x2'}})`.
- `DS(3,1)` / `one_heavy_left_leaf` active reduced dual rows, first few nonzero multipliers: `({'row_index': 4, 'value': '6', 'row': {'kind': 'reduced_h1_r_le_p', 'x': 'x1'}}, {'row_index': 6, 'value': '11', 'row': {'kind': 'left_interval_upper_one_minus_p', 'x': 'x1'}}, {'row_index': 15, 'value': '1', 'row': {'kind': 'left_interval_upper_theta', 'x': 'x2'}}, {'row_index': 19, 'value': '1', 'row': {'kind': 'upper_unit', 'var': ['A_left', 2]}}, {'row_index': 30, 'value': '1', 'row': {'kind': 'right_interval_lower_theta_minus_s', 'y': 'y1'}}, {'row_index': 35, 'value': '1', 'row': {'kind': 'psi_sum_ge_first_mass', 'side': 'left', 'first': 'x1', 'second': 'x2'}}, {'row_index': 39, 'value': '1', 'row': {'kind': 'psi_sum_ge_first_mass', 'side': 'left', 'first': 'x1', 'second': 'x3'}}, {'row_index': 45, 'value': '1', 'row': {'kind': 'cross_e_ge_r', 'x': 'x1', 'y': 'y1'}})`.
- `DS(3,2)` / `one_heavy_left_leaf` active reduced dual rows, first few nonzero multipliers: `({'row_index': 4, 'value': '5', 'row': {'kind': 'reduced_h1_r_le_p', 'x': 'x1'}}, {'row_index': 6, 'value': '10', 'row': {'kind': 'left_interval_upper_one_minus_p', 'x': 'x1'}}, {'row_index': 15, 'value': '1', 'row': {'kind': 'left_interval_upper_theta', 'x': 'x2'}}, {'row_index': 23, 'value': '1', 'row': {'kind': 'left_interval_upper_theta', 'x': 'x3'}}, {'row_index': 30, 'value': '1', 'row': {'kind': 'right_interval_lower_theta_minus_s', 'y': 'y1'}}, {'row_index': 38, 'value': '1', 'row': {'kind': 'right_interval_lower_theta_minus_s', 'y': 'y2'}}, {'row_index': 43, 'value': '1', 'row': {'kind': 'psi_sum_ge_first_mass', 'side': 'left', 'first': 'x1', 'second': 'x2'}}, {'row_index': 47, 'value': '1', 'row': {'kind': 'psi_sum_ge_first_mass', 'side': 'left', 'first': 'x1', 'second': 'x3'}})`.

Finite pattern: the reduced duals use interval upper/lower rows together with the `Gamma` endpoint caps and same-side `Psi` sum rows. This is only a candidate symbolic pattern, not a promoted proof.

## Skeptical Audit

- A reduced-functional counterexample only attacks this global coupling lemma route, not full H1 exactness.
- A no-gap finite run would still not prove the inequality for all reduced H1-feasible data.
- The reduced feasible region is exactly the one encoded here; any stronger formalization should be added as explicit constraints and rerun.
- The full H1/H2 comparisons are depth-projection checks from the previous machinery and are kept separate from the reduced-functional result.
