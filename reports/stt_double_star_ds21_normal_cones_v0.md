# DS(2,1) Reduced Normal-Cone Scan v0

## Scope

This audit uses the repository's exact reduced `LB_H1` extended LP for `DS(2,1)`.  The same-side `Psi` and cross `Gamma` terms are represented by rational endpoint-allocation variables and linear facets, not by sampled nonlinear surrogates.

The projected profile used for the coherence test is `a_i = A_left[x_i]` and `b_i = 1-r_i-A_left[x_i]`, with right split `S = A_right[y1]` and `T = 1-s_y-A_right[y1]`.  These are the center-orientation masses in the existing reduced LP.

## Outcome

No reduced `LB_H1 < OPT_DS` counterexample was found among the exposed incoherent faces discovered by the deterministic grid scan.

Exposed incoherent face certificates written to `examples\stt_lp\ds21_normal_cones_v0_certificates.json`.
Outcome counts: `{'exposed_incoherent_face_tied_with_coherent_deterministic_witness': 8}`.

## Exact Arrangement Data

- Backend variables: `18`.
- Feasibility rows before nonnegativity: `43`.
- Total halfspaces with nonnegativity: `61`.
- Naive basis patterns: `1312251244423350`.
- Included hyperplanes/facets: `p1=p2`, `A_left[xi]=A_right[y1] for i=1,2`, `B_left[xi]=B_right[y1] for i=1,2`, `r_i=p_i`, `A_left[xi]=0`, `A_left[xi]=theta`, `B_left[xi]=0`, `B_left[xi]=1-theta`, `same-side Psi endpoint caps/sum kinks`, `cross Gamma E=max(...) facets`, `cross Gamma endpoint caps/sum kinks`.

## Face Table

| face | weights | margin | incoherence | reduced | STT | normal cone | coherent witness | outcome |
|---|---:|---:|---|---:|---:|---|---|---|
| ds21-face-0001 | `(1, 0, 0, 0, 0)` | -1 | b1_minus_b2 | 0 | 0 | verified_exact_primal_from_basis | verified_exact_primal_from_basis | exposed_incoherent_face_tied_with_coherent_deterministic_witness |
| ds21-face-0002 | `(1, 0, 0, 0, 2)` | -1 | b1_minus_b2 | 1 | 1 | verified_exact_primal_from_basis | verified_exact_primal_from_basis | exposed_incoherent_face_tied_with_coherent_deterministic_witness |
| ds21-face-0003 | `(2, 0, 0, 0, 1)` | -1 | b1_minus_b2 | 1 | 1 | verified_exact_primal_from_basis | verified_exact_primal_from_basis | exposed_incoherent_face_tied_with_coherent_deterministic_witness |
| ds21-face-0004 | `(2, 0, 1, 0, 0)` | -1 | a1_minus_a2 | 1 | 1 | verified_exact_primal_from_basis | none | exposed_incoherent_face_tied_with_coherent_deterministic_witness |
| ds21-face-0005 | `(2, 0, 1, 0, 1)` | -1 | a1_minus_a2 | 3 | 3 | verified_exact_primal_from_basis | verified_exact_primal_from_basis | exposed_incoherent_face_tied_with_coherent_deterministic_witness |
| ds21-face-0006 | `(2, 0, 1, 0, 3)` | -1 | a1_minus_a2 | 4 | 4 | verified_exact_primal_from_basis | none | exposed_incoherent_face_tied_with_coherent_deterministic_witness |
| ds21-face-0007 | `(2, 1, 0, 1, 0)` | -1 | b1_minus_b2 | 3 | 3 | verified_exact_primal_from_basis | verified_exact_primal_from_basis | exposed_incoherent_face_tied_with_coherent_deterministic_witness |
| ds21-face-0008 | `(3, 0, 1, 0, 1)` | -1 | a1_minus_a2 | 3 | 3 | verified_exact_primal_from_basis | none | exposed_incoherent_face_tied_with_coherent_deterministic_witness |

## Unresolved

- `full_arrangement_face_enumeration_not_attempted`: `Naive exact basis enumeration would require C(61,18)=1312251244423350 patterns before rank pruning; this run certifies only exposed faces discovered by deterministic rational weight-grid solves.`

## Skeptical Audit

- This is not yet a proof of all arrangement faces: full active-face enumeration is explicitly unresolved above.
- Reduced `LB_H1` outcomes are kept separate from full H1/H2 depth-projection outcomes.
- Every saved discovered-face witness is rational and rechecked against the exact LP rows.
- The deterministic STT comparison uses normal-form `DS(2,1)` STT enumeration, not a reduced surrogate.
