# DS(k,1) H1 Coarea Scouting v1

## Stop Sign

**Finite evidence only / do not promote to theorem.** This report is a proof-scouting artifact for the conjecture that, for every `k`, H1 has exact depth projection on `DS(k,1)`. It does not prove that conjecture.

## Scope

This run tests `DS(k,1)` for `k=1..5` with exact rational Bellman optima and H1 LP objectives accepted only when exact primal-dual certificates are reconstructed from the floating simplex basis.

The true optimum is computed by the DS(k,1) recurrence that either peels a left leaf from the component containing `a`, chooses `a`, chooses `b`, or chooses the right leaf `r`. The same recurrence gives `Phi(S)`, the optimum conditioned on exactly `S` being the left-leaf ancestors of `a`.

H2 is kept separate: when H1 equals the true STT optimum, H2 is reported by the exact `H1 <= H2 <= STT` sandwich, not as a direct H2 primal-dual certificate.

## Exact Certificate Audit

Required H1 status: `verified_exact_primal_dual_after_floating_basis_reconstruction`.

Every reported H1 LP solve has the required verified exact primal-dual status.

| k | cases | H1 certificate statuses | H2 sandwich | direct H2 certificates | H2 statuses |
|---:|---:|---|---:|---:|---|
| 1 | 80 | verified_exact_primal_dual_after_floating_basis_reconstruction: 80 | 80 | 0 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal: 80 |
| 2 | 161 | verified_exact_primal_dual_after_floating_basis_reconstruction: 161 | 161 | 0 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal: 161 |
| 3 | 269 | verified_exact_primal_dual_after_floating_basis_reconstruction: 269 | 269 | 0 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal: 269 |
| 4 | 16 | verified_exact_primal_dual_after_floating_basis_reconstruction: 16 | 16 | 0 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal: 16 |
| 5 | 17 | verified_exact_primal_dual_after_floating_basis_reconstruction: 17 | 17 | 0 | exact_by_h1_equals_stt_sandwich_no_separate_h2_primal: 17 |

## Outcome

No H1 depth gap appeared in the tested DS(k,1) cases.
No H2 depth gap appeared. In this run every H2 value is a sandwich certificate, not a separate H2 LP basis.
`Phi(S)` was submodular for every tested weight vector.

JSON certificate and Phi proof-scouting artifacts are in `examples\stt_lp\dsk1_h1_coarea_v1_certificates.json`.

## Coverage And Runtime

Runtime for artifact generation: `356.703` seconds.

The exhaustive portion is exactly integer weights `0..2` modulo left-leaf symmetry for `k<=3`. The `k=4,5` portion is structured and orbit-friendly: all double-star templates, two-block split cases, fixed rational smoke cases, and seeded two-block random cases.

| k | cases | families | H1 gaps | H2 gaps | Phi failures | dual patterns |
|---:|---:|---|---:|---:|---:|---|
| 1 | 80 | small_int_leq_2: 80 | 0 | 0 | 0 | `path exactness` |
| 2 | 161 | small_int_leq_2: 161 | 0 | 0 | 0 | `DS(2,1)-style endpoint allocation, pure-star coarea` |
| 3 | 269 | small_int_leq_2: 269 | 0 | 0 | 0 | `new global leaf-exchange/coarea lemma, pure-star coarea` |
| 4 | 16 | all_left_leaves_heavy: 1, asym_left_center_right_leaf: 1, asym_right_center_left_leaf: 1, both_centers_heavy: 1, left_center_heavy: 1, one_heavy_leaf_each_side: 1, one_heavy_left_leaf: 1, one_heavy_right_leaf: 1, rational_two_block_left_heavy_right: 1, rational_two_block_left_light_center: 1, right_center_heavy: 1, two_block_left_split_1_center_tension: 1, two_block_left_split_2_center_tension: 1, two_block_left_split_3_center_tension: 1, two_block_random_seed_4105_0: 1, two_block_random_seed_4105_1: 1 | 0 | 0 | 0 | `new global leaf-exchange/coarea lemma` |
| 5 | 17 | all_left_leaves_heavy: 1, asym_left_center_right_leaf: 1, asym_right_center_left_leaf: 1, both_centers_heavy: 1, left_center_heavy: 1, one_heavy_leaf_each_side: 1, one_heavy_left_leaf: 1, one_heavy_right_leaf: 1, rational_two_block_left_heavy_right: 1, rational_two_block_left_light_center: 1, right_center_heavy: 1, two_block_left_split_1_center_tension: 1, two_block_left_split_2_center_tension: 1, two_block_left_split_3_center_tension: 1, two_block_left_split_4_center_tension: 1, two_block_random_seed_4106_0: 1, two_block_random_seed_4106_1: 1 | 0 | 0 | 0 | `new global leaf-exchange/coarea lemma` |

## Phi(S) Proof-Scouting Data

For each tested instance, the JSON records all `Phi(S)` values, all attaining top roots, one canonical Bellman normal-form trace for each `S`, all nontrivial tight submodularity inequalities, and marginal profiles for adding each left leaf to the ancestor set of `a`.

- Tested instances with Phi data: `543`.
- Phi submodularity failures: `0`.
- Cases with marginal diminishing-return violations: `0`.
- Nontrivial tight submodularity inequalities by k: `{'1': 0, '2': 24, '3': 309, '4': 0, '5': 5}`.
- Attaining top-root role counts over all Phi sets: `{'a': 446, 'b': 1805, 'left_leaf_in_S': 2073, 'r': 566}`.

Observed pattern, still heuristic: the marginal cost of forcing one more left leaf above `a` appears to diminish as more left leaves are already forced above `a`. The tight incomparable inequalities are the best finite handles for an exchange proof.

## Candidate DS(k,1) theorem suggested by v1

Definition of `Phi(S)`: for a fixed nonnegative vertex-weight vector `w` on `DS(k,1)`, `Phi_w(S)` is the minimum weighted root-depth objective over all STTs in which the set of left leaves that are strict ancestors of `a` is exactly `S`.

Clean conjectural submodularity lemma: for every `A,B` contained in the left leaves, `Phi_w(A) + Phi_w(B) >= Phi_w(A cap B) + Phi_w(A cup B)`. Equivalently, the marginal penalty for adding a left leaf to the ancestor set of `a` has diminishing returns.

Clean conjectural H1-to-Lovasz/coarea target: express the H1 dual lower bound as a coarea-style integral or Lovasz-extension lower bound over threshold sets of the fractional left-leaf ancestor indicators, with `Phi_w` supplying the submodular set function. This would turn finite dual-pattern labels into a symbolic leaf-exchange certificate.

Minimal special cases that appear theorem-ready: `k=1` reduces to path exactness; one-active-left-leaf and all-left-leaves-equal regimes look closest to a direct exchange argument; the `DS(2,1)` endpoint-allocation pattern remains useful as a sanity check but is not promoted here to a persistency theorem.

Exact blockers: no symbolic proof yet identifies the exchange map behind all tight Phi inequalities; the H1 dual rows are certified instance-by-instance but not generated by a closed formula; rational smoke cases are finite reliability checks only; the H2 entries are sandwich certificates rather than direct H2 certificates.

## Dual Pattern Read

- `DS(2,1)-style endpoint allocation`: `151` tested objectives.
- `new global leaf-exchange/coarea lemma`: `274` tested objectives.
- `path exactness`: `80` tested objectives.
- `pure-star coarea`: `38` tested objectives.

Finite classification: `DS(1,1)` behaves as path exactness; the `k=2` rows line up with the existing endpoint-allocation story; larger `k` cases repeatedly need cross-component heredity rows, so the natural proof target is a global leaf-exchange/coarea lemma rather than a pure-star argument.

## Regressions

- Pure star regression: H1 `6` equals STT `6` with gap `0`.
- `U(7,3)` regression: H1 `59/2` versus true STT `30`, gap `-1/2`.
- DS(2,1) persistency caveat: DS(2,1) full depth objectives tested here are H1-tight, but prior normal-cone and pinned-boundary artifacts separate full-H1 depth exactness from reduced-functional persistency/coherence claims.

## Skeptical Audit

- This is finite evidence, not a theorem. The exhaustive part is only integer weights `0..2` modulo left-leaf symmetry for `k<=3`.
- For `k=4,5`, cases are deliberately orbit-friendly structured, two-block, rational-smoke, and seeded random vectors so exact LP reconstruction remains tractable.
- H2 is often certified by sandwiching rather than separately solved; this is exact for the objective value but does not provide a separate H2 primal-dual basis in those cases.
- The repeated dual-pattern labels are heuristic proof-route classifications, not promoted symbolic lemmas.
- This report does not claim DS(k,1) exactness, all-double-star exactness, DS(2,1) persistency theorem status, or H2 spider exactness.

## Final Summary

Verified exactly: `543` finite DS(k,1) objectives have Bellman STT optima, no H1 depth gaps, no H2 sandwich gaps, Phi submodularity, and H1 status counts `{'verified_exact_primal_dual_after_floating_basis_reconstruction': 543}`.

Still conjectural: the all-`k` DS(k,1) H1 exactness statement, the submodular Phi lemma outside the tested finite set, and the proposed Lovasz/coarea representation of the H1 lower bound.

Next proof-work prompt: prove the Phi submodularity exchange lemma first, then derive an H1 coarea lower bound from the Lovasz extension of Phi; use the v1 JSON tight inequalities and canonical Bellman traces as lemma-mining data, not as theorem evidence by themselves.
