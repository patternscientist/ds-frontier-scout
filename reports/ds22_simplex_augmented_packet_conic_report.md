# DS(2,2) Simplex-Augmented Packet-Conic Closure

## Result

All 302 leaf-swap atlas orbit representatives factor exactly into the simplex-augmented packet basis `Sigma/Lambda/Gamma/Delta/Omega/Pi` plus a nonnegative coordinate residual. Each stored factorization has total packet mass exactly `1`.

Floating-point simplex was used only to identify candidate LP bases. The checked artifacts store exact rational coefficients, exact rational residuals, and exact rational dual upper-bound certificates for the five-packet optima.

## Counts

- H1 variables: `84` over `28` connected subsets.
- Certificate blocker vertices: `943`.
- Leaf-swap orbit representatives: `302`.
- Simplex-augmented packet atoms: `76` with kind counts `{'Sigma': 28, 'Lambda': 2, 'Gamma': 2, 'Delta': 4, 'Omega': 4, 'Pi': 36}`.
- Five-packet atoms without `Sigma`: `48`.
- Augmented-basis failures: `0`.
- Five-packet failures without `Sigma`: `287` of `302`.

## Correction Note

`Lambda/Gamma/Delta/Omega/Pi` alone are insufficient. In the exact LP audit without `Sigma`, 287 of the 302 orbit representatives have maximum packet mass below `1`; the raw simplex atoms supply the missing mass.

`Sigma_S = sigma_S` is a raw H1 simplex-row atom, not a new packet type with independent structural content. The augmented closure is therefore best read as an exact DS(2,2) computational atlas and a bookkeeping decomposition for the packet deficit, not as a conceptual packet-basis theorem.

Special representatives requested in the task:

- `o011`: five-packet maximum mass `10/11`, deficit `1/11`.
- `o055`: five-packet maximum mass `47/56`, deficit `9/56`.
- `o057`: five-packet maximum mass `41/50`, deficit `9/50`.
- `o058`: five-packet maximum mass `6/7`, deficit `1/7`.
- `o069`: five-packet maximum mass `32/39`, deficit `7/39`.
- `o080`: five-packet maximum mass `31/36`, deficit `5/36`.

## Exact Objects

- `Sigma_S = sigma_S` for each connected `S`.
- `Lambda`, `Gamma`, `Delta`, `Omega`, and `Pi` atoms are represented as exact H1 coordinate vectors in the factorization JSON.
- For each representative, `w dot d` is reconstructed from the blocker weights and the H1 path-depth objective.
- The residual vector is `w dot d - packet_combination`, checked coordinatewise nonnegative over all 84 H1 coordinates.

## Scope Guardrails

This branch uses only H1 first-hit coordinates, raw simplex rows, and packet-coordinate arithmetic. It does not use H2, refined-Z, path-monotonicity, ancestry-transitivity, LCA-separation, or mixed-second-difference rows.

The result is a finite DS(2,2) packet-closure certificate over this atlas. It does not imply DS(k,2), DS(2,m), or DS(k,m) exactness, and it should not be promoted as a standalone conceptual closure until the role of the simplex atoms is explained by a non-tautological proof template.

## Artifacts

- Orbit atlas: `data\ds22_blocker_orbits.json`.
- Factorizations: `data\ds22_simplex_augmented_packet_factorizations.json`.
- Residuals and five-packet deficits: `data\ds22_simplex_augmented_packet_residuals.json`.
- Verifier/test entry point: `tests/test_ds22_simplex_augmented_packet_conic.py`.

## Verification Commands

```powershell
python -m src.ds22_simplex_augmented_packet_conic --verify
python -m unittest tests.test_ds22_simplex_augmented_packet_conic
```
