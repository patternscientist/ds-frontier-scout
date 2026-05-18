# Frontier v5.4 Repo Provenance Manifest

Generated: 2026-05-18

Branch: `frontier-v5-4-provenance-manifest-v0`

Base commit: `4dc1171298f7385a19df74003b4e613f99796ae3`

Scope: repository-local provenance for the AI and Data Structures / STT connected-first-hit project, intended as coordinator input for `frontier_note_v5_4_unified_project_overview.md`. This manifest uses checked-in files and fetched git history only. It does not add theorem claims and does not perform a literature search.

## Executive Summary

The stable theorem-level claim currently present in the repository is the internal connected-first-hit star theorem: H1 has exact depth projection on all pure stars. This is a theorem about the connected first-hit hierarchy, not public Golinsky/SKZ LP exactness.

The strongest recent finite certificate lane is DS(k,2), but it must be described at its actual finite scope. DS(2,2) has a full-objective H1 depth-vector certificate and a simplex-augmented packet-conic atlas closure. DS(3,2) and DS(4,2) have packet-window capacity certificates only for the declared finite weight universes. None of these artifacts proves all-k DS(k,2), DS(k,m), or public LP exactness.

The public-LP bridge lane currently contains obstruction/correction evidence, not closure. The proper-subset contraction audit demotes the scalar/proper-subset route under the audited interpretation. The mixed-support oracle audit certifies a finite k=3 public-star support-oracle/chamber/proxy obstruction analysis, while explicitly leaving b-root public-LP closure and the full residual `ell_ij` mixed-support theorem open.

The list-update/OpenEvolve materials are a side lane. Current `main` contains the deterministic evaluator milestone and older exact evaluator scaffold. Fetched history also contains wrapper/tiny-run/zero-money follow-up branches, but those artifacts are not present in the current checkout. They are infrastructure only; fixed-stub transport is not autonomous OpenEvolve policy discovery.

## Current Repo State

- Current branch after setup: `frontier-v5-4-provenance-manifest-v0`
- Starting `main` commit: `4dc1171298f7385a19df74003b4e613f99796ae3`
- Relevant recent merge path:
  - `9fd9045` merged `origin/ds22-simplex-augmented-packet-conic-v0`.
  - `e56c48a` merged `origin/ds32-ds42-packet-window-capacity-hardening-v0`.
  - `5313696` merged `origin/stt-public-lp-broot-mixed-support-oracle-v1` into `stt-public-lp-proper-subset-contraction-v0`.
  - `4dc1171` merged `origin/stt-public-lp-proper-subset-contraction-v0` to `main`.

## Major Artifacts And Status Labels

| Area | Major artifact paths | Latest touching commit | Status label | Claim supported | Verification in this task | Guardrail |
|---|---|---:|---|---|---|---|
| Unified v4.4 baseline | `reports/stt_first_hit_hierarchy_frontier_note_v4_4.md` | `b846a62` | `candidate/conditional` | Prior frontier narrative for connected first-hit hierarchy. | Not run; narrative source. | Must be updated by v5.4 manifest; it predates recent DS(k,2) and public-LP audits. |
| Pure star theorem | `reports/stt_star_h1_depth_exactness_theorem_note.md` | `163377f` | `theorem-level` | H1 exact depth projection on every star; H2 and stronger hierarchy levels inherit the depth lower envelope on stars. | Regression tests passed via `tests.test_stt_star_depth_projection`. | Internal connected-first-hit theorem, not public Golinsky/SKZ LP exactness. |
| Pure star finite regressions | `reports/stt_star_depth_projection_v0.md`, `examples/stt_lp/star_symmetric_h2_d_leq_8_summary.json`, `tests/test_stt_star_depth_projection.py` | `329a500` / earlier | `certificate-backed finite` | Finite star H2/H3/H4 depth-projection no-gap tests plus regression role after the theorem note. | `python -m unittest tests.test_stt_star_depth_projection`: 13 tests passed. | Tests are regression/evidence only, not the all-star proof. |
| 4-leaf star full-z obstruction | `reports/stt_v4_star_audit_v0.md`, `tests/test_stt_v4_star_audit.py` | `666a25a` | `obstruction/refutation artifact` | Exact H2-feasible full-`z` system on 4-leaf star is not complete-Mobius representable, but its depth vector is dominated by a true STT. | `python -m unittest tests.test_stt_v4_star_audit`: 5 tests passed. | Not a depth-projection obstruction. |
| DS(k,1) H1/v5.3 coarea materials | `reports/stt_dsk1_h1_coarea_v1.md`, `examples/stt_lp/dsk1_h1_coarea_v1_certificates.json`, `tests/test_stt_dsk1_h1_coarea.py` | `d43296f` | `certificate-backed finite` | 543 finite DS(k,1) objectives with verified H1 primal-dual certificates, H2 by sandwich, and Phi submodularity checks. | `python -m unittest tests.test_stt_dsk1_h1_coarea`: 8 tests passed. | Does not prove all-k DS(k,1) H1 exactness or public LP exactness. |
| Double-star bridge/proof-route tests | `reports/stt_double_star_depth_projection_v0.md`, `reports/stt_double_star_coupling_functional_v0.md` | `9fe1373`, `55c3dff` | `candidate/conditional` | Finite no-gap tests for double-star depth projection and reduced coupling functional. | Double-star depth and coupling pytest files passed. | No double-star theorem; reduced counterexamples would attack a proof route, not automatically full H1. |
| DS(2,1) reduced/pinned coverage | `reports/stt_double_star_ds21_normal_cones_v1_coverage.md`, `reports/stt_double_star_ds21_pinned_boundary_v2.md` | `8ad56bf`, `784b6e1` | `certificate-backed finite` | Targeted exact coverage for named DS(2,1) normal-cone and pinned-boundary cells. | `tests/test_stt_ds21_normal_cones.py` and `tests/test_stt_ds21_pinned_boundary.py`: 5 tests passed. | Targeted cell coverage only, not full arrangement or full DS(2,1) proof. |
| DS(k,2) interface residual | `reports/dsk2_interface_residual_v0.md`, `certificates/dsk2_interface_residual_examples.json`, `scripts/check_dsk2_interface_identity.py` | `f78dcd3` | `certificate-backed finite` | Corrected symbolic H1 interface residual identity for `k=1,2,3` and bounded DS(2,2) no-gap search. | Script printed identity audits with `identity_holds=true`; pytest passed. | Does not claim DS(k,2) exactness. |
| DS(2,2) full objective H1 certificate | `reports/ds22_full_objective_depth_vector_cert_report.md`, `certificates/ds22_depth_inclusion_cert.json` | `bc36a2e` | `certificate-backed finite` | `D_H1 subset conv(D_RST)+R_+^V` for the six-vertex DS(2,2) tree. | Verifier passed: 214 schedules, 214 depth vectors, 943 blocker vertices, 943 dual certificates. | Not DS(k,2), arbitrary double-star, H2, public LP, or all-k exactness. |
| DS(2,2) packet-conic closure | `reports/ds22_simplex_augmented_packet_conic_report.md`, `data/ds22_blocker_orbits.json`, `data/ds22_simplex_augmented_packet_factorizations.json`, `data/ds22_simplex_augmented_packet_residuals.json` | `fdbed2e` / `4b55c6b` | `certificate-backed finite` | All 302 leaf-swap atlas representatives factor in the simplex-augmented `Sigma/Lambda/Gamma/Delta/Omega/Pi` basis with nonnegative residual. | Verifier passed; unittest passed. | Uses raw H1 simplex atoms; not conceptual packet-basis theorem, not DS(k,2), not DS(k,m), not public LP exactness. |
| DS(3,2)/DS(4,2) packet-window hardening | `reports/ds32_ds42_packet_window_capacity_hardening_report.md`, `data/ds32_packet_window_factorizations_ternary.json`, `data/ds42_packet_window_factorizations_binary.json`, `data/ds32_ds42_packet_window_gap_witnesses.json` | `a3a6c1b` | `certificate-backed finite` | Packet-window closure for exactly DS(3,2) ternary cube minus zero and DS(4,2) binary cube minus zero. | Verifier passed; pytest passed. | Not an all-k theorem, not DS(k,m), not public LP exactness. |
| Proper-subset contraction audit | `reports/proper_subset_contraction_report.md`, `data/proper_subset_contraction_k3.json`, `data/proper_subset_contraction_k4.json`, `scripts/check_proper_subset_contraction.py` | `78204dd` | `obstruction/refutation artifact` | Finite exact audit flags obstruction candidates for the corrected scalar/proper-subset source-deletion route. | Script passed with k3/k4 `obstruction_candidate_found`. | Scalar `D(S) >= delta(S)` / `SUB_S`-alone route should remain killed or demoted under this interpretation. |
| Mixed-support public-star oracle audit | `reports/mixed_support_oracle_report.md`, `data/k3_pair_antichain_chambers.json`, `data/mixed_support_certificates.json`, `data/mixed_support_obstructions.json` | `427aa56` | `certificate-backed finite` | Exact finite k=3 public-star support-oracle/chamber audit and proxy obstruction data. | Chamber checker, Farkas extractor, and support-oracle unittest passed. | Not b-root public-LP closure; not public LP exactness; residual `ell_ij` Farkas extraction is not certified. |
| Current list-update evaluator side lane | `reports/list_update_evaluator_milestone1.md`, `reports/list_update_eval_smoke.json`, `list_update_eval/*`, `tests/test_list_update_eval_milestone1.py` | `0cb917e` | `side-lane infrastructure` | Deterministic evaluator, offline oracle integration, baseline scoring, and smoke JSON for future OpenEvolve side experiment. | `tests/test_list_update_eval_milestone1.py` and `tests/test_list_update_evaluator.py`: 18 tests passed. | Not STT theorem lane and not policy discovery. |
| History-only OpenEvolve wrapper/tiny/zero-money side branches | `reports/list_update_openevolve_wrapper_milestone2.md`, `reports/list_update_openevolve_milestone3_tiny_run.md`, `reports/list_update_openevolve_milestone3z_zero_money.md` on fetched branch commits | `71ca111`, `41a37da`, `34b18c0` | `side-lane infrastructure` | Wrapper scaffold, blocked tiny run, and fixed-stub zero-money transport check exist in git history. | Not run in this task; files are not in current checkout. | Fixed-stub transport is non-autonomous, non-discovery plumbing evidence only. |

## Theorem-Level Stable Claims

- H1 has exact depth projection on all pure stars, in the internal connected-first-hit hierarchy. This is supported by `reports/stt_star_h1_depth_exactness_theorem_note.md`.
- The pure-star theorem also implies that H2 and stronger connected-first-hit hierarchy levels have the same exact depth lower envelope on stars, because they add constraints to H1.

Do not translate this into a public Golinsky/SKZ LP theorem. The theorem note itself says the public path-variable LP boundary is separate.

## Certificate-Backed Finite Claims

- DS(2,2) full-objective H1 depth exactness over the checked six-vertex double-star: `certificates/ds22_depth_inclusion_cert.json` verified with 943 exact dual certificates.
- DS(2,2) simplex-augmented packet-conic closure over the checked leaf-swap atlas: 302 orbit representatives, 76 packet atoms, 0 augmented-basis failures, and 287 five-packet failures without `Sigma`.
- DS(3,2)/DS(4,2) packet-window closure only over the declared finite weight universes: DS(3,2) ternary cube minus zero with 2186 factorizations, and DS(4,2) binary cube minus zero with 255 factorizations.
- DS(k,1) v1 coarea scouting data: 543 finite objectives with verified H1 certificates and no tested Phi submodularity failures.
- DS(k,2) interface residual identity: exact symbolic identity audits for DS(1,2), DS(2,2), and DS(3,2).
- Mixed-support k=3 public-star support-oracle/chamber artifacts: 7 active chamber forms and proxy obstructions as recorded, with residual `ell_ij` Farkas extraction explicitly not certified.
- DS(2,1) normal-cone and pinned-boundary reports are finite targeted coverage certificates for named cells only.

## Candidate Or Conditional Architectures

- DS(k,1) H1 exactness via Phi submodularity/coarea remains conjectural outside the finite v1 data.
- Double-star depth projection and reduced coupling-functional proof routes remain candidate architectures. Existing no-gap computations are finite and structured.
- DS(k,2) all-k packet-window gluing remains a proof target. DS(3,2)/DS(4,2) packet-window certificates are finite evidence only.
- The v4.4 frontier note remains useful as narrative context but should be patched with the newer status distinctions before reuse.

## Killed Or Demoted Routes

- H2 as globally exact full first-hit `z`-space is refuted by the 4-leaf star full-`z` obstruction.
- Star-depth random/objective testing is demoted to regression, because the star depth question is settled by the H1 theorem note.
- The scalar/proper-subset `D(S) >= delta(S)` / `SUB_S`-alone route should remain killed or demoted under the audited Bellman interpretation in `proper_subset_contraction_report.md`.
- Root-comparisons-only mixed support and individual `SUB_T` delta proxy routes are demoted/killed only to the extent recorded in the mixed-support report/data. Do not generalize this to residual `ell_ij` or b-root closure.

## Side-Lane Infrastructure

- Current `main` contains the list-update evaluator milestone and exact evaluator scaffold. These support a future OpenEvolve side experiment and are not part of the STT theorem lane.
- Fetched branch `openevolve-list-update-wrapper-v0` (`71ca111`) adds an OpenEvolve-compatible adapter scaffold, but those files are not present in this checkout.
- Fetched branch `openevolve-list-update-tiny-run-v0` (`41a37da`) records a blocked tiny dry-run due to missing API credentials.
- Fetched branch `openevolve-list-update-zero-money-tiny-run-v0` (`34b18c0`) records a blocked real local-model path and a successful fixed-stub transport check. The stub path is explicitly non-autonomous and produced no valid policy discovery.

## Verification Commands And Results

| Command | Result in this task |
|---|---|
| `git fetch --all --prune --tags` | First sandboxed attempt failed with shared git metadata permission error; approved retry succeeded. |
| `git status --short` | Clean before edits. |
| `git branch --show-current` | Empty before branch setup because worktree was detached at `main`; branch then created as `frontier-v5-4-provenance-manifest-v0`. |
| `git log --oneline --decorate --max-count=30` | Head was `4dc1171 (origin/main, origin/HEAD, main)`. |
| `python -m src.ds22_simplex_augmented_packet_conic --verify` | Passed: 302 orbit representatives, 76 packet atoms, 287 five-packet failures. |
| `python -m unittest tests.test_ds22_simplex_augmented_packet_conic` | Passed: 9 tests in about 409 seconds. |
| `python -m src.ds32_ds42_packet_window_capacity --verify` | Passed: DS32 factorizations 2186, DS42 factorizations 255, gap witnesses 0. |
| `python -m pytest tests/test_ds32_ds42_packet_window_capacity.py` | Passed: 5 tests. |
| `python scripts/check_proper_subset_contraction.py` | Passed: k3 and k4 `obstruction_candidate_found`. |
| `python scripts/check_k3_pair_antichain_chambers.py` | Passed: 7 chambers, witness verified. |
| `python scripts/extract_mixed_lambda_farkas.py` | Passed with explicit non-certification: root-only and individual proxy failures recorded; stronger residual `ell` Farkas certificate not extracted. |
| `python -m unittest tests.test_star_support_oracle` | Passed: 5 tests. |
| `python -m src.ds22_depth_inclusion_check certificates/ds22_depth_inclusion_cert.json` | Passed: 214 schedules, 214 depth vectors, 943 blocker vertices, 943 dual certificates. |
| `python -m unittest tests.test_ds22_depth_inclusion` | Passed: 4 tests. |
| `python -m unittest tests.test_stt_dsk1_h1_coarea` | Passed: 8 tests. |
| `python scripts/check_dsk2_interface_identity.py` | Passed; printed identity audits for DS(1,2), DS(2,2), DS(3,2) with `identity_holds=true`. |
| `python -m unittest tests.test_stt_star_depth_projection` | Passed: 13 tests. |
| `python -m unittest tests.test_stt_v4_star_audit` | Passed: 5 tests. |
| `python -m pytest tests/test_list_update_eval_milestone1.py tests/test_list_update_evaluator.py` | Passed: 18 tests. |
| `python -m pytest tests/test_stt_dsk2_interface_residual.py` | Passed: 3 tests. |
| `python -m pytest tests/test_stt_double_star_depth_projection.py` | Passed: 6 tests. |
| `python -m pytest tests/test_stt_double_star_coupling_functional.py` | Passed: 8 tests. |
| `python -m pytest tests/test_stt_ds21_normal_cones.py tests/test_stt_ds21_pinned_boundary.py` | Passed: 5 tests. |

## Commands Not Run

- `python -m src.ds22_h1_depth_polytope --progress`: not run because it is a certificate builder/rebuilder, not needed to verify existing manifest claims.
- Full `python -m pytest`: not run because targeted verification already exercised the relevant artifacts and some certificate tests are long.
- `python -m list_update_eval.evaluate --suite smoke --all-baselines --out reports/list_update_eval_smoke.json`: not run to avoid rewriting the existing smoke provenance artifact.
- History-only OpenEvolve wrapper/tiny/zero-money branch commands were not run because those files are not present in the current checkout and the lane is infrastructure-only.

## Missing Or Ambiguous Artifacts

- No `frontier_note_v5_4_unified_project_overview.md` exists yet; this manifest is an input for it.
- The wrapper/tiny-run/zero-money OpenEvolve files from `71ca111`, `41a37da`, and `34b18c0` are available in fetched branch history but are not present in current `main`.
- No checked artifact proves b-root public-LP closure or public LP exactness on DS(k,1).
- No checked artifact extracts residual `ell_ij` mixed-support Farkas certificates.
- No checked artifact proves all-k DS(k,2), DS(k,m), or arbitrary double-star exactness.
- The status of DS(k,1) H1 exactness remains conjectural outside finite v1 evidence.

## Overclaim Warnings

- Do not treat finite DS(2,2), DS(3,2), or DS(4,2) certificates as all-k DS(k,2) or DS(k,m) proof.
- Do not treat internal H1 star exactness as public Golinsky/SKZ LP exactness.
- Do not treat public-LP obstruction artifacts as public-LP closure artifacts.
- Do not describe mixed-support proxy obstructions as a proof that the full residual `ell_ij` mixed-support theorem fails.
- Do not describe list-update infrastructure or fixed-stub transport as autonomous OpenEvolve policy discovery.
- Do not reuse v4.4 narrative without updating the status of pure stars, DS(k,2) packet evidence, and public-LP obstructions.

## Recommended Inputs For v5.4 Frontier Note

1. Lead with the source separation: theorem-level pure-star result, finite DS(k,2) certificates, public-LP obstruction audits, and list-update side lane.
2. State the pure-star result as an internal connected-first-hit theorem only.
3. Present DS(2,2) as two finite certificate layers: full-objective H1 depth-vector inclusion and simplex-augmented packet-conic atlas closure.
4. Present DS(3,2)/DS(4,2) as finite packet-window capacity hardening over declared weight universes, not as all-k evidence beyond its scope.
5. Present public-LP artifacts as correction/demotion work: proper-subset scalar route obstructed; mixed-support k=3 proxy routes obstructed; residual `ell_ij` and b-root closure open.
6. Keep DS(k,1) H1/coarea and double-star coupling as candidate proof architectures supported by finite certificates, not theorem-level claims.
7. Put list-update/OpenEvolve in a clearly separate side-lane appendix or infrastructure paragraph.
