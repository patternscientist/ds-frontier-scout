# b-root Residual Cut Extraction Report

## 1. Summary verdict

- k=2: projection `aborted_row_limit_after_eliminating_R[a,b]`, cuts `4717`, genuine subset-level cuts `4614`, residual-selection audit `not_attempted_projection_incomplete`.
- k=3: projection `aborted_row_limit_after_eliminating_R[a,b]`, cuts `251`, genuine subset-level cuts `218`, residual-selection audit `not_attempted_projection_incomplete`.

## 2. Exact commands run and outputs

- `python scripts/check_ds11_broot_envelope.py` writes `data/ds11_broot_envelope_audit.json` and `reports/ds11_broot_envelope_audit.md`.
- `python scripts/generate_public_dual_dsk1.py --k 1 --self-test` writes `data/public_dual_dsk1_k1.json`.
- `python scripts/extract_broot_residual_cuts.py --k 2` writes `data/broot_residual_cuts_k2.json`.
- `python scripts/extract_broot_residual_cuts.py --k 3` writes `data/broot_residual_cuts_k3.json`.

## 3. DS(1,1) envelope hardening result

Reconstructed-envelope verdict: `True`; source 12-envelope certificate loaded: `False`.

## 4. Public-dual model generator audit

DS(1,1) model counts: `{'capping': 4, 'frequency': 12}`; self-test passed: `True`.
DS(2,1) model counts: `{'capping': 8, 'frequency': 20}`; variables `26`.
DS(3,1) model counts: `{'capping': 13, 'frequency': 30}`; variables `41`.

## 5. k=2 residual-cut families

- Star residual cases: `5`.
- Augmentation projection status: `aborted_row_limit_after_eliminating_R[a,b]`.
- Extracted cuts: `4717`.
- Classification counts: `{'genuine subset-level': 4614, 'global a/r Bellman-like': 101, 'singleton': 2}`.
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 11/5*gamma + 3/5*s1 + 2/5*s2 + 11/10*u1 + 3/5*u2`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 11/5*gamma + 3/5*s1 + 2/5*s2 + 13/10*u1 + 3/5*u2`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 11/5*gamma + 3/5*s1 + 2/5*s2 + 7/10*u1 + 3/5*u2`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 11/5*gamma + 3/5*s1 + 2/5*s2 + 9/10*u1 + 3/5*u2`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 11/6*gamma + 1/2*s1 + 1/3*s2 + 2/3*u1 + 2/3*u2`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 11/6*gamma + 1/2*s1 + 1/3*s2 + 4/3*u1 + 2/3*u2`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 11/6*gamma + 1/2*s1 + 1/3*s2 + 5/6*u1 + 2/3*u2`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 11/6*gamma + 1/2*s1 + 1/3*s2 + 7/6*u1 + 2/3*u2`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 11/6*gamma + 1/2*s1 + 1/3*s2 + u1 + 2/3*u2`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 11/6*gamma + 2/3*s1 + 1/3*s2 + 2/3*u1 + 2/3*u2`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 11/6*gamma + 2/3*s1 + 1/3*s2 + 5/6*u1 + 2/3*u2`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 11/6*gamma + 2/3*s1 + 1/3*s2 + 7/6*u1 + 2/3*u2`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 11/6*gamma + 2/3*s1 + 1/3*s2 + u1 + 2/3*u2`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 13/6*gamma + 1/2*s1 + 1/3*s2 + 2/3*u1 + 2/3*u2`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 13/6*gamma + 1/2*s1 + 1/3*s2 + 4/3*u1 + 2/3*u2`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 13/6*gamma + 1/2*s1 + 1/3*s2 + 5/6*u1 + 2/3*u2`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 13/6*gamma + 1/2*s1 + 1/3*s2 + 7/6*u1 + 2/3*u2`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 13/6*gamma + 1/2*s1 + 1/3*s2 + u1 + 2/3*u2`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 13/6*gamma + 2/3*s1 + 1/3*s2 + 2/3*u1 + 2/3*u2`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 13/6*gamma + 2/3*s1 + 1/3*s2 + 5/6*u1 + 2/3*u2`
  - additional cuts are in the JSON artifact.

## 6. k=3 residual-cut families

- Star residual cases: `16`.
- Augmentation projection status: `aborted_row_limit_after_eliminating_R[a,b]`.
- Extracted cuts: `251`.
- Classification counts: `{'genuine subset-level': 218, 'global a/r Bellman-like': 33}`.
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 2*gamma + 1/2*s1 + 1/2*s2 + 1/2*s3 + 1/2*u1 + 1/2*u2 + 1/2*u3`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 2*gamma + 1/2*s1 + 1/2*s2 + 1/2*s3 + 1/2*u1 + 1/2*u2 + 2*u3`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 2*gamma + 1/2*s1 + 1/2*s2 + 1/2*s3 + 1/2*u1 + 1/2*u2 + 3/2*u3`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 2*gamma + 1/2*s1 + 1/2*s2 + 1/2*s3 + 1/2*u1 + 1/2*u2 + u3`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 2*gamma + 1/2*s1 + 1/2*s2 + s3 + 1/2*u1 + 1/2*u2 + 1/2*u3`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 2*gamma + 1/2*s1 + 1/2*s2 + s3 + 1/2*u1 + 1/2*u2 + 3/2*u3`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 2*gamma + 1/2*s1 + 1/2*s2 + s3 + 1/2*u1 + 1/2*u2 + u3`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 2*gamma + 1/2*s1 + 1/2*s3 + 1/2*u1 + u2 + 1/2*u3`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 2*gamma + 1/2*s1 + 1/2*s3 + 1/2*u1 + u2 + 2*u3`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 2*gamma + 1/2*s1 + 1/2*s3 + 1/2*u1 + u2 + 3/2*u3`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 2*gamma + 1/2*s1 + 1/2*s3 + 1/2*u1 + u2 + u3`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 2*gamma + 1/2*s1 + s3 + 1/2*u1 + u2 + 1/2*u3`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 2*gamma + 1/2*s1 + s3 + 1/2*u1 + u2 + 3/2*u3`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 2*gamma + 1/2*s1 + s3 + 1/2*u1 + u2 + u3`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 2*gamma + 1/2*s2 + 1/2*s3 + u1 + 1/2*u2 + 1/2*u3`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 2*gamma + 1/2*s2 + 1/2*s3 + u1 + 1/2*u2 + 2*u3`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 2*gamma + 1/2*s2 + 1/2*s3 + u1 + 1/2*u2 + 3/2*u3`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 2*gamma + 1/2*s2 + 1/2*s3 + u1 + 1/2*u2 + u3`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 2*gamma + 1/2*s2 + s3 + u1 + 1/2*u2 + 1/2*u3`
  - `genuine subset-level`: `t <= 1/2*alpha + 1/2*beta + 2*gamma + 1/2*s2 + s3 + u1 + 1/2*u2 + 3/2*u3`
  - additional cuts are in the JSON artifact.

## 7. First genuine subset-level obstruction/cut family

First extracted genuine subset-level cut appears at k=2: `t <= 1/2*alpha + 1/2*beta + 11/5*gamma + 3/5*s1 + 2/5*s2 + 11/10*u1 + 3/5*u2`.

## 8. Exact certificate/counterexample artifacts produced

- `data/ds11_broot_envelope_audit.json`
- `data/public_dual_dsk1_k1.json`
- `data/broot_residual_cuts_k2.json`
- `data/broot_residual_cuts_k3.json`
- exact matrix fallback sections inside each `broot_residual_cuts_k*.json`

## 9. Recommended next manual proof prompt

Use the first non-singleton extracted cut, or the exact matrix fallback if k=3 projection aborted, as the next manual proof target. Prove or refute that the cut is dominated on every b-root Bellman chamber by the projected public-dual star residual system. Treat missing per-cut domination certificates as proof obligations, not theorem counterexamples.

## 10. Explicit overclaim checklist

- Does not claim public LP exactness on DS(k,1).
- Does not claim the b-root residual-selection theorem for arbitrary k.
- Does not treat k=2,3 evidence as an all-k theorem.
- Does not use H1/H2/refined-Z/path-monotonicity/ancestry-transitivity/LCA-separation constraints.
- Does not present floating-point output as exact.
