# DS(2,1) Pinned Boundary Coverage v2

## Scope

This is a targeted exact rational coverage run for only the remaining A-pinned and B-pinned endpoint/cross-kink cells.  It does not use an unconstrained weight-grid scan as evidence.

The run imposes the pinned equations and strict profile inequalities, splits the listed endpoint/cross-kink facets, and tests the relevant normal cones under the requested slope restrictions.

## Outcome

No bad exposed pinned endpoint/cross-kink cell remains: every targeted cell is empty/no-relative-interior, has no pinned-slope normal cone, or is tied by a coherent reduced or deterministic STT witness.

Coverage certificates written to `examples\stt_lp\ds21_pinned_boundary_v2_certificates.json`.
Outcome counts: `{'no_pinned_relative_interior': 5888, 'normal_cone_infeasible_for_pinned_slope': 448}`.

## Coverage Summary

- Pinned cells considered: `6336`.
- Nonempty cells with normal-cone work recorded: `448`.
- Coherent-reduced and deterministic-STT-only witnesses are separated in the JSON via `witness_class`.

## Unresolved Cells

No unresolved pinned cells remain.

## Skeptical Audit

- This v2 artifact covers only the frontier-listed pinned endpoint/cross-kink families, not the full DS(2,1) arrangement.
- Strict profile and slope restrictions are represented by exact positive-margin LPs with normalized objective scale.
- Normal-cone witnesses, reduced objectives, STT comparisons, and coherent-face checks are reconstructed and reported as rational data.
- Infeasible normal cones are reported per exact active cell; promoted cells require either a rational counterexample or an explicit equality-witness classification.
