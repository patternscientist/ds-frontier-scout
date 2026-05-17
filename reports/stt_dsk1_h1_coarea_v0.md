# DS(k,1) H1/H2 Coarea Test v0

## Scope

This run tests `DS(k,1)` for `k=1..5` with exact rational Bellman optima and exact H1 dual certificates reconstructed from simplex bases. H2 values are exact by sandwich whenever H1 equals the true STT optimum; otherwise the H2 LP is solved directly.

The true optimum is computed by the DS(k,1) recurrence that either peels a left leaf from the component containing `a`, chooses `a`, chooses `b`, or chooses the right leaf `r`. The same recurrence gives `Phi(S)`, the optimum conditioned on exactly `S` being the left-leaf ancestors of `a`.

## Outcome

No H1 depth gap appeared in the tested DS(k,1) cases.
No H2 depth gap appeared; every reported H2 value is exact, mostly by H1/STT sandwiching.
`Phi(S)` was submodular for every tested weight vector.

JSON certificate artifacts are in `examples\stt_lp\dsk1_h1_coarea_v0_certificates.json`.

## Coverage

| k | cases | H1 gaps | H2 gaps | Phi failures | dual patterns |
|---:|---:|---:|---:|---:|---|
| 1 | 80 | 0 | 0 | 0 | `path exactness` |
| 2 | 161 | 0 | 0 | 0 | `DS(2,1)-style endpoint allocation, pure-star coarea` |
| 3 | 269 | 0 | 0 | 0 | `new global leaf-exchange/coarea lemma, pure-star coarea` |
| 4 | 9 | 0 | 0 | 0 | `new global leaf-exchange/coarea lemma` |
| 5 | 9 | 0 | 0 | 0 | `new global leaf-exchange/coarea lemma` |

## Dual Pattern Read

- `DS(2,1)-style endpoint allocation`: `151` tested objectives.
- `new global leaf-exchange/coarea lemma`: `259` tested objectives.
- `path exactness`: `80` tested objectives.
- `pure-star coarea`: `38` tested objectives.

Finite classification: `DS(1,1)` behaves as path exactness; the `k=2` rows line up with the existing endpoint-allocation story; larger `k` cases repeatedly need cross-component heredity rows, so the natural proof target is a global leaf-exchange/coarea lemma rather than a pure-star argument.

## Regressions

- Pure star regression: H1 `6` equals STT `6` with gap `0`.
- `U(7,3)` regression: H1 `59/2` versus true STT `30`, gap `-1/2`.
- DS(2,1) persistency caveat: DS(2,1) full depth objectives tested here are H1-tight, but prior normal-cone and pinned-boundary artifacts separate full-H1 depth exactness from reduced-functional persistency/coherence claims.

## Skeptical Audit

- This is finite evidence, not a theorem. The exhaustive part is only integer weights `0..2` modulo left-leaf symmetry for `k<=3`.
- For `k=4,5`, random cases are deliberately orbit-friendly two-block integer vectors so exact LP reconstruction remains tractable.
- H2 is often certified by sandwiching rather than separately solved; this is exact for the objective value but does not provide a separate H2 primal-dual basis in those cases.
- The repeated dual-pattern labels are heuristic proof-route classifications, not promoted symbolic lemmas.
