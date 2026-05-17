# DS(2,2) Full-Objective Depth-Vector Certificate

## Result

certificate-backed DS(2,2) full-objective H1 exactness.

This is only a finite DS(2,2) H1 depth-vector statement. It does not claim DS(k,2), H2, refined-Z, path monotonicity, mixed second differences, endpointwise kappa payment, or any true-right-star-mixture fact.

## Counts

- H1 connected subsets: `28`.
- H1 variables: `84`.
- H1 simplex rows: `28`.
- H1 heredity rows: `380`.
- Standard-form rows checked by dual certificates: `436`.
- True schedules: `214`.
- Deduplicated true depth vectors: `214`.
- Blocking-cell facet normals: `943`.
- H1 exact dual certificates: `943`.

## Exact Inclusion Certificate

The certificate enumerates the exact vertices of the blocking polyhedron `{w >= 0 : w dot d(T) >= 1 for every true recursive search tree T}`. For every listed nonnegative blocker vertex `w`, the JSON stores an exact H1 dual certificate proving `min_{z in H1} w dot d(z) >= 1`. Since each blocker is normalized so that `min_T w dot d(T) = 1`, every lower facet of `conv(D_RST)+R_+^V` is valid for `D_H1`.

The coordinate facets `q_x >= 0` are covered directly because every H1 depth coordinate is a sum of nonnegative first-hit variables.

## Artifacts

- Certificate: `certificates\ds22_depth_inclusion_cert.json`.
- Verifier: `src/ds22_depth_inclusion_check.py`.
- Builder: `src/ds22_h1_depth_polytope.py`.
- True schedule enumerator: `src/ds22_true_schedules.py`.
- Report: `reports\ds22_full_objective_depth_vector_cert_report.md`.

## Commands

```powershell
python -m src.ds22_h1_depth_polytope --progress
python -m src.ds22_depth_inclusion_check certificates/ds22_depth_inclusion_cert.json
python -m unittest tests.test_ds22_depth_inclusion
```

Expected verifier output:

```text
verified ds22 depth inclusion certificate: true_schedules=214 depth_vectors=214 blocker_vertices=943 dual_certificates=943 h1_rows=436
```

## Overclaim-Safe Interpretation

The certificate proves `D_H1 subset conv(D_RST)+R_{>=0}^V` for the six-vertex DS(2,2) tree only. It is a full-objective nonnegative-weight certificate, not a bounded-weight search, but it should not be promoted to DS(k,2) or arbitrary double-star exactness.

## Best Next Proof-Work Prompt

Use the DS(2,2) blocker-vertex dual certificates as a finite atlas. Cluster the 943 nonnegative facet normals by graph automorphism and active H1 heredity rows, then ask for a symbolic proof template that derives the recurring dual patterns using only H1 simplex and heredity rows.
