# STT v4 Star Audit v0

## Definitions Used

- Base tree for the obstruction: center `0` and leaves `1,2,3,4`.
- Connected-subset first-hit variables are `z[I,r]`, with `r in I`.
- H1 constraints checked exactly: simplex `sum_{r in I} z[I,r] = 1` and heredity `z[A,r] <= z[S,r]` for connected `S subset A` and `r in S`.
- H2 extension rectangles checked exactly: `z[S,r] - z[A,r] - z[B,r] + z[A union B,r] >= 0` whenever all four sets are connected, `S subset A`, `S subset B`, and `r in S`.
- Complete-form masses use the connected-set zeta inversion `z[I,r] = sum_{C superset I} m[C,r]`, over connected supersets containing `r`.
- Depths use the strict-ancestor/root-depth-0 projection `d_v = sum_{u != v} z[P(u,v),u]`.

## 4-Leaf Star H2 Feasibility

| case | simplex | z vars | H1 | H2 ordered | H2 canonical | simplex residual | min H1 | min H2 ordered | min H2 canonical |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4-leaf star | 20 | 52 | 173 | 1449 | 181 | 0 | 0 | 0 | 0 |

All simplex, H1 heredity, and H2 extension rectangle inequalities pass exactly over `Fraction` arithmetic.

## Complete-Mobius Inversion

- Center-root mass `m[{0},0]`: `-1/3`.
- Negative recovered masses: `5`.
- `m[[0],0] = -1/3`
- `m[[0, 1],1] = -1/12`
- `m[[0, 2],2] = -1/12`
- `m[[0, 3],3] = -1/12`
- `m[[0, 4],4] = -1/12`

There are four additional negative leaf-root masses, so the center-root obstruction is not the only negative recovered mass.

## Depth Projection

- Depth vector `(0,1,2,3,4)`: `(8/3, 11/6, 11/6, 11/6, 11/6)`.
- This is `d_0 = 8/3` and `d_i = 11/6` for each leaf `i`.

## STT Dominant Status

- Enumerated STT depth vectors on the 4-leaf star: `65`.
- Dominant membership: `yes`.
- Exact convex-combination certificate:
  - weight `1` on depth vector `(0, 1, 1, 1, 1)`.
  - component roots `[([0, 1, 2, 3, 4], 0), ([1], 1), ([2], 2), ([3], 3), ([4], 4)]`.

Thus this exact z-system is a full first-hit-space obstruction, but not a depth-projection obstruction under root-depth-0 dominant convention.

## Degree-4 Embedding Samples

| branch lengths | n | connected | z vars | H1 | H2 ordered | H2 canonical | simplex residual | min H1 | min H2 ordered | min H2 canonical | center mass | negative masses |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [1, 1, 1, 1] | 5 | 20 | 52 | 173 | 1449 | 181 | 0 | 0 | 0 | 0 | -1/3 | 5 |
| [2, 1, 1, 1] | 6 | 30 | 91 | 426 | 4643 | 713 | 0 | 0 | 0 | 0 | -1/3 | 5 |
| [2, 2, 1, 1] | 7 | 44 | 154 | 988 | 14202 | 2586 | 0 | 0 | 0 | 0 | -1/3 | 5 |
| [2, 2, 2, 2] | 9 | 93 | 421 | 4895 | 126452 | 29912 | 0 | 0 | 0 | 0 | -1/3 | 5 |
| [3, 2, 1, 1] | 8 | 59 | 232 | 1905 | 34289 | 6837 | 0 | 0 | 0 | 0 | -1/3 | 5 |

The sampled subdivided-star embeddings all satisfy H1/H2 exactly and keep `m[{0},0] = -1/3` as a nonrepresentability witness. These finite samples support the v4 embedding proof, but they are not by themselves a complete proof of the degree-at-least-4 theorem.

## Recommendation

- Promote: the 4-leaf star z-system is exactly H2-feasible and not complete-Mobius representable.
- Promote with precision: the complete-Mobius obstruction includes `m[{0},0] = -1/3` plus four leaf-root negatives `-1/12`.
- Weaken or qualify: do not call this example a depth-projection obstruction; its depth vector is already dominated by the integral center-root STT depth vector `(0,1,1,1,1)`.
- Promote only as computational support: the sampled degree-4 embeddings pass exact H1/H2 checks and preserve a negative center-root mass, but finite samples do not prove the full theorem.
