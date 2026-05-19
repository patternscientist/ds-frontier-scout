# Frontier v5.4 Repo Provenance Manifest

Generated: 2026-05-18T18:33:21-07:00

Branch: `frontier-v5-4-provenance-manifest-refresh-v1`

Base/current repo commit: `145a34c21d861efbbdb43ff36951307cd6b83c0f` (`origin/main`, subject: `Add frontier notes`)

Scope: repository-local provenance for a coordinator-written `frontier_note_v5_4_unified_project_overview.md`. This is a status/provenance audit only. It introduces no new theorem claims, performs no literature search, and treats current checked-in files plus fetched git history as the source of truth.

## Executive Summary

The prior provenance manifest from `origin/frontier-v5-4-provenance-manifest-v0` is stale for `DS(k,1)`: it was based at `110825f614ff8cf53040ea1449cc3a787884a7cd`, before commit `145a34c` checked in the v4.5-v5.3 frontier-note sequence and the leaf-local cap checker. The refreshed status is that `reports/frontier_note_v5_3_dsk1_h1_exactness_2026_05_17.md` is the canonical checked-in project-level artifact for the internal connected-first-hit theorem:

> H1 has exact depth projection on `DS(k,1)` for every `k >= 1`.

This is theorem-level only within the internal connected first-hit hierarchy. It is not public Golinsky/SKZ LP exactness, not a polynomial-time exact STT algorithm, and not an exactness theorem for `DS(k,2)`, `DS(k,m)`, all double-stars, all spiders, or all max-degree-3 trees.

The v4.5 pure-star result remains theorem-level: H1 has exact depth projection on pure stars, and therefore H2/Hk inherit exact depth projection there. The v4.5 guardrails also remain live: H1 fails as a general depth relaxation on the public `U(7,3)` subdivided-star example; H2 full-`z` exactness is killed by the 4-leaf star obstruction; and that 4-leaf star obstruction is not a depth-projection obstruction.

The DS(2,2), DS(3,2), and DS(4,2) packet artifacts are certificate-backed finite results over exactly their checked atlases/weight universes. The public-LP artifacts are finite obstruction/correction audits, not public-LP closure. The list-update/OpenEvolve files are side-lane infrastructure and strategy audits, not STT theorem-lane evidence and not OpenEvolve policy discovery.

## Current Repo Commit

- Current branch after setup: `frontier-v5-4-provenance-manifest-refresh-v1`
- Current commit: `145a34c21d861efbbdb43ff36951307cd6b83c0f`
- Recent base evidence:
  - `145a34c` adds the v4.5-v5.3 frontier notes and `scripts/dsk1_leaf_local_cap_certificate_check.py`.
  - `110825f` merged the zero-money OpenEvolve strategy audit.
  - `4dc1171`, `5313696`, `e56c48a`, `9fd9045`, `78204dd`, `427aa56`, `a3a6c1b`, `fdbed2e`, and `4b55c6b` carry the finite STT/public-LP certificate and audit lanes listed below.

## Adversarial Audit Of Prior Manifest

Prior draft inspected:

- `git show origin/frontier-v5-4-provenance-manifest-v0:reports/frontier_v5_4_repo_provenance_manifest.md`
- `git show origin/frontier-v5-4-provenance-manifest-v0:data/frontier_v5_4_repo_provenance_manifest.json`

Findings and corrections:

| Audit question | Prior-draft issue | Refresh action |
|---|---|---|
| Stale from missing v5.3 notes? | Yes. The draft predates `145a34c` and does not include `frontier_note_v4_5...` through `frontier_note_v5_3...` or the leaf-local cap checker. | Added v4.5-v5.3 artifacts and made v5.3 the canonical DS(k,1) status source. |
| DS(k,1) status label? | Stale and overconservative. It labels DS(k,1) as finite coarea evidence/conjectural outside v1 data. | Corrected to theorem-level internal connected-first-hit H1 exactness for every `k >= 1`, supported by v5.3. |
| Verification commands current? | Missing `python scripts/dsk1_leaf_local_cap_certificate_check.py`. | Added and ran the checker. First sandboxed run missed `sympy`; after `python -m pip install sympy`, the successful rerun printed the expected `ok:` line. |
| Finite DS(k,2) accidentally all-k? | Prior draft was mostly careful. | Preserved finite-only labels for DS(2,2), DS(3,2), and DS(4,2). |
| Internal hierarchy confused with public LP? | Prior draft was mostly careful. | Strengthened warnings that v4.5/v5.3 are not public Golinsky/SKZ LP exactness. |
| Public-LP proxy obstruction confused with closure? | Prior draft was mostly careful. | Preserved obstruction/refutation labels for proper-subset and mixed-support proxy routes. |
| List-update confused with policy discovery? | Prior draft was careful. | Preserved side-lane infrastructure label and fixed-stub warning. |
| Killed/demoted routes separated from live candidates? | Mostly yes, but DS(k,1) was still listed as a candidate/conjectural route. | Moved DS(k,1) out of candidate/conditional and into theorem-level claims; left DS(k,2), spider H2, residual `ell_ij`, and b-root closure as candidates/open. |
| Missing repo artifacts? | Missing v4.5-v5.3 frontier notes and `scripts/dsk1_leaf_local_cap_certificate_check.py`. | Added them to the artifact table and JSON manifest. |
| Status changed by v5.3? | Yes. | Explicitly records this as the main status-label correction. |

No checked report/test disagreement was found that needed silent resolution. Where a finite checker and report have different roles, this manifest records the distinction instead of promoting either beyond its scope.

## Major Artifacts And Status Labels

| Area | Major artifact paths | Latest touching commit | Status label | Claim supported | Verification status | Guardrail |
|---|---|---:|---|---|---|---|
| v4.5 frontier note | `reports/frontier_note_v4_5_patched_connected_first_hit_hierarchy.md` | `145a34c` | `theorem-level` plus `obstruction/refutation` and `candidate/conditional` context | Pure-star H1/H2/Hk depth-projection exactness; H1 failure on `U(7,3)`; 4-leaf star full-`z` obstruction is not a depth obstruction. | Narrative/theorem note inspected; pure-star and v4 star tests passed. | Not public LP exactness; H2 spider/double-star remains open in v4.5. |
| v5-v5.3 DS(k,1) frontier notes | `reports/frontier_note_v5_dsk1_h1_exactness_2026_05_17.md`, `reports/frontier_note_v5_1_dsk1_h1_exactness_2026_05_17.md`, `reports/frontier_note_v5_2_dsk1_h1_exactness_2026_05_17.md`, `reports/frontier_note_v5_3_dsk1_h1_exactness_2026_05_17.md` | `145a34c` | `theorem-level` | H1 has exact depth projection on `DS(k,1)` for every `k >= 1`; v5.3 is canonical checked-in artifact. | v5.3 inspected; leaf-local checker passed. | Internal connected-first-hit H1 only; not public LP, not DS(k,2), not all double-stars/spiders/max-degree-3. |
| DS(k,1) leaf-local checker | `scripts/dsk1_leaf_local_cap_certificate_check.py` | `145a34c` | `certificate-backed finite` supporting theorem architecture | Verifies corrected fan table and primitive-ray/four-cap identities for the v5.3 leaf-local cap lemma. | `ok: corrected fan and primitive-ray certificates verified`. | Regression for finite symbolic certificate, not a replacement for the v5.3 proof. Requires `sympy`. |
| Older DS(k,1) coarea finite scaffold | `reports/stt_dsk1_h1_coarea_v1.md`, `examples/stt_lp/dsk1_h1_coarea_v1_certificates.json`, `tests/test_stt_dsk1_h1_coarea.py` | `d43296f` | `certificate-backed finite`, now superseded as status source | 543 finite DS(k,1) objectives with checked H1 certificates and no tested Phi failures. | `python -m unittest tests.test_stt_dsk1_h1_coarea`: 8 passed. | No longer the canonical DS(k,1) status source; v5.3 theorem supersedes the conjectural framing. |
| DS(2,2) full objective depth inclusion | `reports/ds22_full_objective_depth_vector_cert_report.md`, `certificates/ds22_depth_inclusion_cert.json`, `src/ds22_depth_inclusion_check.py`, `tests/test_ds22_depth_inclusion.py` | `bc36a2e` | `certificate-backed finite` | DS(2,2) H1 depth-vector inclusion over the six-vertex checked topology. | Verifier passed: 214 schedules, 214 depth vectors, 943 blocker vertices, 943 dual certificates; unittest 4 passed. | Not DS(k,2), not H2, not public LP, not arbitrary double-star. |
| DS(2,2) simplex-augmented packet conic | `reports/ds22_simplex_augmented_packet_conic_report.md`, `data/ds22_blocker_orbits.json`, `data/ds22_simplex_augmented_packet_factorizations.json`, `data/ds22_simplex_augmented_packet_residuals.json`, `src/ds22_simplex_augmented_packet_conic.py`, `tests/test_ds22_simplex_augmented_packet_conic.py` | `fdbed2e` / `4b55c6b` | `certificate-backed finite` | 302 leaf-swap atlas representatives factor in the simplex-augmented `Sigma/Lambda/Gamma/Delta/Omega/Pi` basis with nonnegative residual. | Verifier passed; unittest 9 passed. | `Sigma` atoms are bookkeeping; not conceptual all-k packet theorem, not DS(k,m), not public LP. |
| DS(3,2)/DS(4,2) packet-window hardening | `reports/ds32_ds42_packet_window_capacity_hardening_report.md`, `data/ds32_packet_window_factorizations_ternary.json`, `data/ds42_packet_window_factorizations_binary.json`, `data/ds32_ds42_packet_window_gap_witnesses.json`, `src/ds32_ds42_packet_window_capacity.py`, `tests/test_ds32_ds42_packet_window_capacity.py` | `a3a6c1b` | `certificate-backed finite` | Packet-window closure for exactly DS(3,2) nonzero weights in `{0,1,2}^7` and DS(4,2) nonzero weights in `{0,1}^8`. | Verifier passed: 2186 DS32, 255 DS42, 0 gap witnesses; pytest 5 passed. | Not all-k DS(k,2), not DS(k,m), not public Golinsky/SKZ LP exactness. |
| Proper-subset contraction audit | `reports/proper_subset_contraction_report.md`, `data/proper_subset_contraction_k3.json`, `data/proper_subset_contraction_k4.json`, `scripts/check_proper_subset_contraction.py` | `78204dd` | `obstruction/refutation artifact`; route `killed/demoted` | Finite exact audit flags obstruction candidates for the corrected scalar/proper-subset source-deletion route. | Script passed: k3/k4 `obstruction_candidate_found`. | Does not prove public LP exactness; scalar `D(S) >= delta(S)` / `SUB_S`-alone route should stay demoted under audited interpretation. |
| Mixed-support public-star oracle audit | `reports/mixed_support_oracle_report.md`, `data/k3_pair_antichain_chambers.json`, `data/mixed_support_certificates.json`, `data/mixed_support_obstructions.json`, `scripts/star_support_oracle.py`, `scripts/check_k3_pair_antichain_chambers.py`, `scripts/extract_mixed_lambda_farkas.py`, `tests/test_star_support_oracle.py` | `427aa56` | `certificate-backed finite` plus `obstruction/refutation artifact` | Exact finite k=3 support-oracle/chamber/proxy obstruction audit. | Chamber checker passed; Farkas extractor records proxy failures and no residual `ell` certificate; unittest 5 passed. | Not b-root closure, not public LP exactness on DS(k,1), not an all-k theorem. |
| List-update zero-money strategy | `reports/openevolve_zero_money_candidate_rerank_v0.md`, `reports/openevolve_zero_money_candidate_rerank_v0.json` | `3fef3fe` | `side-lane infrastructure` | Repo-grounded rerank under zero-money/local-model constraints; `list_update` remains first side lane, STT remains theorem/certificate lane. | JSON syntax validation passed; focused list-update tests passed. | Not policy discovery and not STT theorem evidence. |
| History-only list-update OpenEvolve milestones | `git:0cb917e:reports/list_update_evaluator_milestone1.md`, `git:71ca111...:reports/list_update_openevolve_wrapper_milestone2.md`, `git:41a37da...:reports/list_update_openevolve_milestone3_tiny_run.md`, `git:34b18c0...:reports/list_update_openevolve_milestone3z_zero_money.md` | `0cb917e`, `71ca111`, `41a37da`, `34b18c0` | `side-lane infrastructure` | Evaluator scaffold, wrapper scaffold, blocked tiny run, and fixed-stub transport evidence exist in history. | Inspected with `git show`; current checkout focused tests passed. | Fixed-stub transport is non-autonomous plumbing and not policy discovery. |

Status vocabulary is intentionally strict. No major checked artifact in this manifest is promoted under a `scratch/provisional` label; older exploratory material is either omitted from the major table or explicitly treated as candidate/conditional, killed/demoted, or side-lane infrastructure.

## Theorem-Level Stable Claims

- Complete connected first-hit/Mobius `Q(T)` is exact/integral but exponential, as carried in v4.5/v5.3 frontier notes.
- H2 is exact in full first-hit space on paths, as carried in v4.5/v5.3.
- H1/H2/Hk have exact depth projection on pure stars. Canonical project-level note for this baseline: `reports/frontier_note_v4_5_patched_connected_first_hit_hierarchy.md`.
- H1 has exact depth projection on `DS(k,1)` for every `k >= 1`. Canonical artifact: `reports/frontier_note_v5_3_dsk1_h1_exactness_2026_05_17.md`.

The `DS(k,1)` proof architecture to carry into v5.4 is: fixed-right-atom enumeration; pure-star coarea split; slope-chain/Monge transport; three-cap basis; residual decomposition; universal leaf-local cap certificate; and the finite convex-average argument in Theorem 10.3.

## Certificate-Backed Finite Claims

- DS(k,1) leaf-local cap certificate: the checker verifies the corrected fan and primitive-ray/four-cap identities supporting the v5.3 leaf-local lemma.
- DS(2,2) H1 depth-vector inclusion over the checked six-vertex topology: 943 blocker dual certificates verified.
- DS(2,2) simplex-augmented packet-conic closure over the 302-representative checked atlas.
- DS(3,2)/DS(4,2) packet-window closure exactly for DS(3,2) nonzero weights in `{0,1,2}^7` and DS(4,2) nonzero weights in `{0,1}^8`.
- Mixed-support k=3 public-star support-oracle/chamber artifacts and proxy obstruction records.
- Older finite DS(k,1), DS(k,2), double-star, and DS(2,1) tests remain useful regression/certificate evidence, but they do not supersede the v5.3 theorem note or broaden finite scopes.

## Candidate/Conditional Architectures

- DS(k,2) all-k packet-window gluing remains a live proof target. The DS(3,2)/DS(4,2) hardening artifacts are finite evidence only.
- Spider/subdivided-star H2 depth projection remains open in the checked notes. H1 is killed as a general spider route by `U(7,3)`.
- Public-LP b-root closure remains open. The proper-subset and mixed-support artifacts audit/demote proxy routes; they do not close the public LP.
- Residual `ell_ij` mixed-support Farkas extraction remains open/not certified.
- Formal packaging of the v5.3 leaf-local certificate into stable JSON/Lean-ready data is optional infrastructure, not a new theorem task.

## Killed/Demoted Routes

- H1 as a general depth relaxation for all spiders/subdivided stars or all max-degree-3 trees is killed by the public `U(7,3)` subdivided-star example recorded in v4.5/v5.3.
- H2 as globally exact full first-hit `z`-space is killed by the 4-leaf star full-`z` obstruction.
- The 4-leaf star full-`z` obstruction as a depth-projection obstruction is killed/demoted; v4.5 records that its depth vector is dominated by a true STT depth vector, and pure-star H1 depth exactness is theorem-level.
- The scalar/proper-subset `D(S) >= delta(S)` / `SUB_S`-alone public-LP route is demoted under the audited Bellman interpretation in `proper_subset_contraction_report.md`.
- Root-comparisons-only mixed-support box proxy and individual `SUB_T` delta proxy routes are demoted/killed only within the audited k=3 proxy scope.
- DS(2,1) persistency as all-double-star exactness is false/overstrong per v4.5/v5.3 notes.
- The five-packet DS(2,2) basis without raw `Sigma` atoms is insufficient for the checked atlas.
- List-update evaluator/wrapper/fixed-stub materials are demoted from any "policy discovery" reading; they are infrastructure only.

## Obstruction/Refutation Artifacts

- `U(7,3)` H1 gap in v4.5/v5.3: refutes H1 as a general depth relaxation for spiders/subdivided stars/max-degree-3 trees, but does not address double-stars.
- 4-leaf star full-`z` obstruction in v4.5: refutes H2 full first-hit-space exactness on stars, but not depth projection.
- Proper-subset contraction data: exact finite obstruction candidates for the audited scalar/proper-subset route.
- Mixed-support data: exact finite k=3 proxy failures for root-comparisons-only and individual `SUB_T` delta proxy modes; residual `ell_ij` is not refuted by these proxy failures.
- DS22 packet residual data: records that five packet atoms without `Sigma` fail on 287 of 302 representatives, warning against a clean five-packet conceptual theorem.

## Side-Lane Infrastructure

- Current main includes `reports/openevolve_zero_money_candidate_rerank_v0.md` and `.json`. This is a strategy/rerank audit, not an experiment result.
- The immediate side lane is `list_update`, because it has a small mutable policy object and cheap exact finite evaluation.
- `search_trees_on_trees_lp` remains the main theorem/certificate lane, not the immediate zero-money OpenEvolve target.
- History-only side-branch milestones show evaluator scaffold (`0cb917e`), wrapper scaffold (`71ca111...`), blocked API-key tiny run (`41a37da...`), and fixed-stub transport (`34b18c0...`). The fixed-stub path is explicitly non-autonomous and non-discovery.

## Verification Commands And Results

| Command | Result |
|---|---|
| `git fetch --all --prune --tags` | Initial sandbox attempt failed on shared git metadata permission; approved retry succeeded. |
| `git status --short` | Clean before edits. |
| `git branch --show-current` | Empty before setup because checkout was detached at `145a34c`; branch created as `frontier-v5-4-provenance-manifest-refresh-v1`. |
| `git log --oneline --decorate --max-count=40` | Head was `145a34c (origin/main, origin/HEAD, main) Add frontier notes`. |
| `python scripts/dsk1_leaf_local_cap_certificate_check.py` | First run failed with missing `sympy`; after `python -m pip install sympy`, rerun outside sandbox passed with `ok: corrected fan and primitive-ray certificates verified`. |
| `python -m src.ds22_simplex_augmented_packet_conic --verify` | Passed: `orbit_representatives=302`, `packet_atoms=76`, `five_packet_failures=287`. |
| `python -m unittest tests.test_ds22_simplex_augmented_packet_conic` | Passed: 9 tests. |
| `python -m src.ds32_ds42_packet_window_capacity --verify` | Passed: `ds32_factorizations=2186`, `ds42_factorizations=255`, `gap_witnesses=0`, max denominators 3 and 2. |
| `python -m pytest tests/test_ds32_ds42_packet_window_capacity.py` | Passed: 5 tests. |
| `python scripts/check_proper_subset_contraction.py` | First 120s run timed out; rerun with longer timeout passed: k3/k4 `obstruction_candidate_found`. |
| `python scripts/check_k3_pair_antichain_chambers.py` | Passed: 7 chambers, witness verified. |
| `python scripts/extract_mixed_lambda_farkas.py` | Passed with expected non-certification: root-only and vector proxies failed; stronger residual `ell` Farkas certificate not extracted. |
| `python -m unittest tests.test_star_support_oracle` | Passed: 5 tests. |
| `python -m src.ds22_depth_inclusion_check certificates/ds22_depth_inclusion_cert.json` | Passed: 214 true schedules, 214 depth vectors, 943 blocker vertices, 943 dual certificates. |
| `python -m unittest tests.test_ds22_depth_inclusion` | Passed: 4 tests. |
| `python -m unittest tests.test_stt_star_depth_projection` | Passed: 13 tests. |
| `python -m unittest tests.test_stt_v4_star_audit` | Passed: 5 tests. |
| `python -m unittest tests.test_stt_dsk1_h1_coarea` | Passed: 8 tests. |
| `python scripts/check_dsk2_interface_identity.py` | Passed; printed identity audits with `identity_holds=true` for DS(1,2), DS(2,2), and DS(3,2). |
| `python -m pytest tests/test_stt_dsk2_interface_residual.py` | Passed: 3 tests. |
| `python -m pytest tests/test_stt_double_star_depth_projection.py` | Passed: 6 tests. |
| `python -m pytest tests/test_stt_double_star_coupling_functional.py` | Passed: 8 tests. |
| `python -m pytest tests/test_stt_ds21_normal_cones.py tests/test_stt_ds21_pinned_boundary.py` | Passed: 5 tests. |
| `python -m pytest tests/test_list_update_eval_milestone1.py tests/test_list_update_evaluator.py` | Passed: 18 tests. |
| `python -m json.tool reports/openevolve_zero_money_candidate_rerank_v0.json` | Passed. |

## Commands Not Run

- Full `python -m pytest`: not run because the targeted verification suite covered the requested/current artifacts and some certificate tests are moderately expensive.
- Certificate builders/rebuilders, such as broad DS22 builder commands: not run because checked certificates were verified in place.
- `python -m list_update_eval.evaluate --suite smoke --all-baselines --out reports/list_update_eval_smoke.json`: not run because it would rewrite a checked-in side-lane smoke artifact; focused list-update tests passed instead.
- History-only OpenEvolve wrapper/tiny-run branch tests: not run in this checkout because those files are not present on current main. The reports were inspected with `git show`.
- New literature searches: intentionally not run per task constraints.

## Missing Or Ambiguous Artifacts

- `reports/frontier_note_v5_4_unified_project_overview.md` does not exist yet; this manifest is intended as input for it.
- The v5.3 DS(k,1) theorem has a checked frontier note and a Python checker for the leaf-local cap certificate, but no standalone JSON/Lean certificate package is checked in.
- `scripts/dsk1_leaf_local_cap_certificate_check.py` depends on `sympy`; this environment needed `python -m pip install sympy` before the checker could run successfully outside the sandbox.
- The OpenEvolve wrapper/tiny-run reports from `71ca111`, `41a37da`, and `34b18c0` are available in fetched history but not present in the current checkout.
- No checked artifact proves all-k DS(k,2), DS(k,m), arbitrary double-star exactness, b-root public-LP closure, public LP exactness on DS(k,1), or residual `ell_ij` mixed-support Farkas certificates.

## Overclaim Warnings

- Do not describe v5.3 as public Golinsky/SKZ LP exactness.
- Do not describe v5.3 as a polynomial-time exact STT algorithm.
- Do not extend `DS(k,1)` to `DS(k,2)`, `DS(k,m)`, all double-stars, all spiders, or all max-degree-3 trees.
- Do not treat finite DS(2,2), DS(3,2), or DS(4,2) certificates as all-k theorem proof.
- Do not treat public-LP proxy obstructions as public-LP closure.
- Do not treat mixed-support proxy failures as a refutation of the full residual `ell_ij` route.
- Do not treat list-update infrastructure, reranking, or fixed-stub transport as OpenEvolve policy discovery.
- Do not use finite fixed-`k <= 5` public enumeration as the proof of the all-k DS(k,1) theorem; v5.3 claims a structural proof.

## Recommended Inputs For The Coordinator's v5.4 Unified Frontier Note

1. Lead with the status correction: after `145a34c`, v5.3 is the canonical DS(k,1) theorem-level frontier artifact.
2. State the DS(k,1) theorem exactly: H1 has exact depth projection on `DS(k,1)` for every `k >= 1` in the internal connected first-hit hierarchy.
3. Summarize the v5.3 architecture: fixed-right atoms, pure-star coarea split, slope-chain/Monge transport, three-cap basis, residual decomposition, leaf-local cap certificate, and Theorem 10.3 finite convex average.
4. Carry v4.5 as the baseline: pure-star H1/H2/Hk depth exactness, `U(7,3)` H1 failure for spiders/max-degree-3, and 4-leaf star full-`z` obstruction that is not a depth obstruction.
5. Present DS(2,2) and DS(3,2)/DS(4,2) as finite certificate lanes only, with exact scopes and verification counts.
6. Present public-LP work as obstruction/correction evidence: proper-subset scalar route demoted, k=3 mixed-support proxies demoted, residual `ell_ij` and b-root closure open.
7. Put list-update/OpenEvolve in a separate side-lane section or appendix: infrastructure and strategy only, no policy-discovery claim.
8. Include a small verification appendix with the commands above, especially the DS(k,1) checker dependency note.
