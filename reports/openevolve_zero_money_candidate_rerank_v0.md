# OpenEvolve Zero-Money Candidate Rerank v0

Generated: 2026-05-18T15:33:07-07:00

Branch: `openevolve-zero-money-strategy-audit-v0`

Base commit: `9fd90458e76c5a545c0d0e064211bbe0201f19ae`

## Executive Summary

This is not broad scouting. It is a repo-grounded reranking audit of already-scouted OpenEvolve/evaluator candidates under a zero-money, local-model-only constraint.

Verdict: continue `list_update` first as the immediate zero-money OpenEvolve side lane. It wins the normal weighted ranking and still wins when the `existing_infrastructure` score is removed. The recommendation is therefore not just sunk-cost momentum.

`search_trees_on_trees_lp` should remain the main theorem/certificate lane. It is still the best certificate-heavy STT project in the repo, but tiny local coding models are less likely to autonomously improve STT LP inequality, rounding, or topology-search code without heavier context, dependencies, and proof guidance.

Optional parallel scaffold: if one tiny extra lane is allowed, use `karp_rabin_collision_detection`, but only after fixing the mutable object as a fixed-shift batching selector or witness-generator scaffold. Do not treat its exact oracle alone as an OpenEvolve success condition.

## Scope And Provenance

This audit used checked-in repository files and `git show` output only. No external web or literature search was performed.

Primary ranking files inspected:

- `README.md`
- `reports/fixed_point_recommendation.md`
- `reports/candidate_matrix.md`
- `reports/top_20_shortlist.md`
- `reports/search_space_gaps.md`
- `reports/list_update_openevolve_scaffold_v0.md`
- `reports/scouting_v2/subrun_2I_openevolve_objects.md`
- `reports/scouting_v2/synthesis.md`
- `reports/karp_rabin_oracle_fixed_length_v0.md`
- `reports/karp_rabin_fixed_shift_batching_v0.md`

Candidate files inspected for all seven ranked candidates:

- `candidate_topics/*/problem.md`
- `candidate_topics/*/openevolve_fit.md`
- `candidate_topics/*/score.yaml`

List-update side-lane commits inspected:

| Commit | Report inspected | Availability | Audit finding |
| --- | --- | --- | --- |
| `0cb917e` | `reports/list_update_evaluator_milestone1.md` | available | Deterministic evaluator scaffold accepted; no OpenEvolve wrapper or policy evolution. |
| `71ca11120227292f6920d1477af9d50e10a21c90` | `reports/list_update_openevolve_wrapper_milestone2.md` | available | OpenEvolve-compatible adapter/wrapper scaffold accepted; dry-run uses hand-written candidates only. |
| `41a37da3ba8bbf6c82fefaeaf8e64286688f3c9c` | `reports/list_update_openevolve_milestone3_tiny_run.md` | available | Tiny OpenEvolve run was blocked by missing API credentials; no generated policy. |
| `34b18c0ea8da80037f52fda79b538d4f4f044d16` | `reports/list_update_openevolve_milestone3z_zero_money.md` | available | Real local-model path blocked because no local endpoint was available; fixed-stub transport succeeded but was non-autonomous and non-discovery. |

Repo tension to preserve: `reports/fixed_point_recommendation.md` says STT LP is the incumbent entering source-diverse Scouting v2 and should not be treated as final pilot authorization, while `reports/search_space_gaps.md` says the repo is saturated enough to begin the STT LP pilot. This audit does not resolve that theorem-pilot tension. It only reranks zero-money local-model OpenEvolve side-lane priorities.

## Zero-Money Criteria

Scores are 1 to 5. `risk_of_local_llm_noise` and `generalization_risk` are reverse-scored: 5 means lower risk, 1 means higher risk.

Normal weights:

| Criterion | Weight |
| --- | ---: |
| `local_model_editability` | 1.5 |
| `cheap_evaluation_loop` | 1.3 |
| `dense_feedback` | 1.2 |
| `artifact_value_if_no_breakthrough` | 1.3 |
| `existing_infrastructure` | 1.2 |
| `theorem_relevance` | 1.2 |
| `risk_of_local_llm_noise` | 1.0 |
| `dependency_lightness` | 1.0 |
| `scope_clarity` | 1.0 |
| `generalization_risk` | 1.0 |

Infrastructure-discounted weights are identical except `existing_infrastructure = 0.0`.

## Candidate Comparison

Legend: LME = local model editability, CEL = cheap evaluation loop, DF = dense feedback, AV = artifact value without breakthrough, INF = existing infrastructure, THM = theorem relevance, NOISE = low risk of local LLM noise, DEP = dependency lightness, SCOPE = next-milestone clarity, GEN = low generalization risk.

| Candidate | LME | CEL | DF | AV | INF | THM | NOISE | DEP | SCOPE | GEN | Normal | Infra-discounted |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `list_update` | 5 | 5 | 5 | 5 | 5 | 4 | 4 | 5 | 5 | 2 | 53.3 | 47.3 |
| `karp_rabin_collision_detection` | 3 | 5 | 4 | 5 | 4 | 4 | 3 | 5 | 4 | 3 | 46.9 | 42.1 |
| `search_trees_on_trees_lp` | 3 | 2 | 5 | 5 | 5 | 5 | 3 | 2 | 3 | 4 | 43.6 | 37.6 |
| `imprecise_comparison_sorting` | 4 | 4 | 5 | 4 | 1 | 4 | 3 | 4 | 3 | 3 | 41.4 | 40.2 |
| `quadratic_probing` | 4 | 5 | 4 | 4 | 1 | 3 | 3 | 5 | 3 | 2 | 40.3 | 39.1 |
| `range_mode_queries` | 4 | 4 | 4 | 4 | 1 | 3 | 3 | 5 | 3 | 2 | 39.0 | 37.8 |
| `pairing_heaps` | 3 | 3 | 4 | 4 | 1 | 4 | 2 | 4 | 3 | 2 | 35.4 | 34.2 |

## Why The Local-Model Constraint Changes The Ranking

The original repo-level OpenEvolve ordering is about evaluator promise in the abstract. The zero-money version asks a different operational question: can a small local coding model mutate the object, stay inside the interface, and receive cheap dense feedback without paid API calls or heavyweight solvers?

`list_update` improves under this lens because the mutable object is tiny: a policy function or finite-state table over current list state, request, and history. The evaluator is exact for small traces, gives ratios/regret/validity diagnostics, and already has a wrapper path in side branches. Its main weakness is theorem lift: finite-state wins may not generalize to arbitrary list size.

`search_trees_on_trees_lp` moves down for immediate zero-money OpenEvolve work because its best artifacts are LP/certificate/proof artifacts, not small autonomous code edits. It still has excellent theorem relevance and checked-in infrastructure, but the useful mutations involve inequality templates, root-rounding logic, topology families, and sometimes Sage/polytope or exact LP context.

`karp_rabin_collision_detection` rises as a possible tiny parallel scaffold because the current repo already has exact finite oracle and fixed-shift batching infrastructure. Its limiter is object clarity: an oracle is not enough. A local-model loop needs a precise mutable object such as a selector rule, batching heuristic, or witness generator.

## Normal Weighted Ranking

1. `list_update` - 53.3
2. `karp_rabin_collision_detection` - 46.9
3. `search_trees_on_trees_lp` - 43.6
4. `imprecise_comparison_sorting` - 41.4
5. `quadratic_probing` - 40.3
6. `range_mode_queries` - 39.0
7. `pairing_heaps` - 35.4

## Infrastructure-Discounted Ranking

1. `list_update` - 47.3
2. `karp_rabin_collision_detection` - 42.1
3. `imprecise_comparison_sorting` - 40.2
4. `quadratic_probing` - 39.1
5. `range_mode_queries` - 37.8
6. `search_trees_on_trees_lp` - 37.6
7. `pairing_heaps` - 34.2

## Sunk-Cost Audit

`list_update` remains first in both rankings. Existing infrastructure helps it, but it is not the decisive reason.

Structural reasons it survives the infrastructure discount:

- smallest and clearest mutable object among the seven candidates;
- exact small-instance evaluator with dense numeric diagnostics;
- no need for Sage, LP solvers, paid services, or long-running theorem context for the next milestone;
- OpenEvolve wrapper target is one Python policy file with a guarded interface;
- failure artifacts are still useful: invalid mutations, adversarial traces, baseline regressions, and exact finite ratios.

Rank changes after infrastructure discount:

- `search_trees_on_trees_lp` drops because its checked-in infrastructure is strong but its local-model dependency and editability profile are heavier.
- `imprecise_comparison_sorting`, `quadratic_probing`, and `range_mode_queries` move relatively upward because they are dependency-light finite-game or brute-force-oracle ideas, even though they lack current scaffolding.
- `karp_rabin_collision_detection` remains second because it combines cheap exact checks with useful checked-in oracle infrastructure, but it still lacks `list_update`'s clean policy object.

Final robustness verdict: the recommendation to continue `list_update` first is robust, not mainly driven by sunk cost.

## Final Recommended Ordering

For immediate zero-money local-model OpenEvolve work:

1. `list_update`
2. `karp_rabin_collision_detection`
3. `imprecise_comparison_sorting`
4. `quadratic_probing`
5. `range_mode_queries`
6. `search_trees_on_trees_lp`
7. `pairing_heaps`

This role-aware order differs slightly from the normal weighted order because `search_trees_on_trees_lp` is better preserved as the main theorem/certificate lane than as a tiny local-model side experiment.

## Decision Answers

1. Should we continue `list_update` first under a zero-money/local-model constraint?

Yes. Continue `list_update` first. It wins both rankings and has the cleanest next operational move.

2. Is Ollama/LM Studio local OpenAI-compatible execution still the right next operational move?

Yes. A real local OpenAI-compatible endpoint is the right next move. The side-lane report at `34b18c0` says the real Ollama/local-model path was blocked only because no endpoint was available, while the fixed-stub transport succeeded but was not an LLM run. The next attempt should use Ollama or LM Studio if available, record model/server details, and reject fixed-stub success as policy discovery.

3. Is there any existing candidate clearly better than `list_update` for small local-model code evolution?

No. `karp_rabin_collision_detection` is the closest competitor, but it does not beat `list_update` because the mutable object is less natural and more likely to drift into algorithm-grammar or witness-generator work. It is useful as a tiny parallel scaffold, not as a pivot.

4. Is there any candidate worth one tiny parallel Milestone 1 scaffold while `list_update` continues?

Yes, conditionally: `karp_rabin_collision_detection`. The scaffold should be very small and object-fixing: define a fixed-shift batching selector or adversarial witness-generator grammar, wrap it against the existing oracle, and report counterexamples or invalid selectors. Do not broaden it into a new literature pass.

5. What exact next Codex prompt should be run after this audit?

Use the prompt below.

## Role-Separation Verdict

| Role | Candidate | Verdict |
| --- | --- | --- |
| Main theorem/certificate lane | `search_trees_on_trees_lp` | Keep as the main theorem/certificate project. Its finite artifacts and exact rational certificates remain the strongest theorem-facing infrastructure. |
| Immediate zero-money OpenEvolve side lane | `list_update` | Continue first. It is the best cheap local-model evolution target. |
| Optional parallel scaffold | `karp_rabin_collision_detection` | Worth one tiny scaffold only if it fixes the mutable object and does not delay list-update. |

## Warnings

- Do not claim OpenEvolve has discovered a list-update policy. The inspected side-lane commits do not show policy discovery.
- Do not count the fixed-stub transport run as autonomous OpenEvolve success. It was explicitly non-autonomous and non-discovery.
- Do not treat finite list-update improvements as theorem-level competitive-ratio progress without generalization or finite-game certificate analysis.
- Do not demote `search_trees_on_trees_lp` as the main theorem/certificate lane merely because it is less convenient for tiny local-model code evolution.
- Do not claim modern open status was reverified here. This audit intentionally did not perform new external source checks.
- Do not let exact oracles alone promote a candidate to OpenEvolve readiness. A mutable object and evaluator objective must both be explicit.

## Next Codex Prompt

```text
Codex task: list-update Milestone 3-real-local OpenEvolve run under strict zero-money constraints

Branch:
openevolve-list-update-real-local-milestone3-v0

Starting point:
Start from branch `openevolve-list-update-zero-money-tiny-run-v0` at commit `34b18c0ea8da80037f52fda79b538d4f4f044d16`.

Before editing, run:
git fetch --all --prune --tags
git status --short
git branch --show-current
git log -1 --oneline

Goal:
Complete the next honest zero-money list-update OpenEvolve integration milestone. Use a real local OpenAI-compatible LLM endpoint only, such as Ollama or LM Studio. Do not use paid API credits. Do not count manual mode or a fixed-stub response as autonomous LLM success.

Required checks:
1. Probe for an available local OpenAI-compatible endpoint, starting with `http://localhost:11434/v1` for Ollama and then a locally configured LM Studio endpoint if present.
2. If a local endpoint is available, run exactly one tiny OpenEvolve iteration against `examples/list_update_openevolve/initial_program.py` and `examples/list_update_openevolve/evaluator.py`.
3. Keep the run tiny: one iteration, population 2, no LLM feedback, bounded output tokens, unchanged deterministic evaluator semantics, and independent post-run re-evaluation.
4. Preserve the EVOLVE-block-only guard. Classify generated candidates as identical, changed inside EVOLVE block only, changed outside allowed block, invalid, timeout, nondeterministic, or valid.
5. If no real local endpoint is available, do not install paid services and do not fake success. Write a blocked report with exact probes and next setup instructions.
6. If a generated candidate appears, independently re-evaluate it with `list_update_eval.openevolve_adapter` and save the JSON report.
7. Update or create a Markdown report under `reports/` and machine-readable run status under `runs/`.
8. Run the focused list-update tests. Run full `python -m pytest` only if cheap in the environment; otherwise record why it was skipped or blocked.

Non-goals:
- No theorem claims.
- No new literature scouting.
- No policy-discovery claim unless a real local model produced a saved changed candidate and the adapter independently re-evaluated it.
- No Milestone 4 planning unless the real local-model run succeeds.

Final response should report:
- branch name;
- final commit SHA if committed;
- local endpoint and model used, or exact blocker;
- generated candidate classification;
- adapter re-evaluation result;
- tests run and results;
- files created or modified.
```
