# DS(2,1) Strict-Heavy Normal-Cone Coverage v1

## Scope

This v1 run is a coverage certificate for the remaining smooth strict-heavy kink family, not another unconstrained weight-grid scan.  It uses the exact reduced `LB_H1` extended LP and enumerates the relevant `Psi/Gamma` kink cells after imposing `p1=p2`, `a1=S`, `a1>a2`, `b_i>c_i`, and the split cells `c_i<T` / `c_i>T`.

The profile convention is `a_i=A_left[x_i]`, `b_i=1-r_i-A_left[x_i]`, `c_i=1-p_i-A_left[x_i]`, `S=A_right[y1]`, and `T=1-s_y-A_right[y1]`.  Thus `b_i>c_i` is the smooth condition `p_i>r_i` already visible in the reduced LP.

## Outcome

No bad exposed strict-heavy smooth cell remains in this exact coverage run: every strict cell either has no strict-heavy normal cone or is tied by a coherent reduced witness or deterministic STT equality.

Coverage certificates written to `examples\stt_lp\ds21_normal_cones_v1_coverage_certificates.json`.
Outcome counts: `{'normal_cone_infeasible_for_strict_heavy_weights': 91, 'no_strict_interior': 485}`.

## Coverage Summary

- Kink cells considered after strict-heavy pruning: `576`.
- Nonempty strict cells with normal-cone work recorded: `91`.
- V0 discovered grid faces retained with structural classifications: `8`.

## Unresolved Strict-Heavy Cells

No unresolved strict-heavy cells remain.

## Skeptical Audit

- This certificate targets the named smooth strict-heavy blocker only; it does not claim full 61-halfspace arrangement enumeration.
- Strictness is modeled by exact positive interior margins under normalized objective scale, not by floating tolerances.
- The v0 deterministic grid scan is retained only as context and now carries structural classifications for each discovered face.
- Coherent-reduced witnesses and deterministic-STT-only ties are reported separately in the JSON.
