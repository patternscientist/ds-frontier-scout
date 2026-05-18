# List-Update OpenEvolve Milestone 3z Zero-Money Follow-Up

Branch: `openevolve-list-update-zero-money-tiny-run-v0`

Starting commit: `41a37da3ba8bbf6c82fefaeaf8e64286688f3c9c`

Status: partial infrastructure success. The real zero-money local-model path is
blocked because no Ollama executable or local OpenAI-compatible endpoint is
available. A fixed-stub OpenAI-compatible transport check succeeded and
exercised OpenEvolve's HTTP/evaluator plumbing, but it is explicitly
non-autonomous and non-discovery.

## Files Added Or Changed

- `examples/list_update_openevolve/config_tiny_milestone3_ollama.yaml`: local
  Ollama/OpenAI-compatible zero-money config, one iteration, population 2, no
  paid key, no LLM feedback, conservative token cap.
- `scripts/run_list_update_openevolve_zero_money_milestone3.py`: local endpoint
  probe, Ollama probe, OpenEvolve invocation, candidate extraction from
  OpenEvolve JSON records, SHA256 hashing, EVOLVE-block classification, and
  independent adapter re-evaluation.
- `scripts/run_list_update_openevolve_fixed_stub_transport_milestone3.py`:
  optional fixed-response OpenAI-compatible HTTP stub. Label:
  `Stubbed OpenAI-compatible transport test; fixed response, no model inference, no autonomous mutation, no policy discovery.`
- `tests/test_list_update_openevolve_milestone3.py`: added zero-money config,
  graceful-blocking, hashing/classification, JSON-candidate extraction, and
  generated-candidate checks.
- `runs/list_update_openevolve_milestone3z_zero_money/`: blocked real local
  endpoint status and copied Ollama config.
- `runs/list_update_openevolve_milestone3z_fixed_stub/`: fixed-stub transport
  run artifacts, extracted OpenEvolve program JSON candidates, and candidate
  adapter reports.
- `reports/list_update_openevolve_milestone3z_initial_smoke.json`: fresh
  initial-program adapter report.
- `reports/list_update_openevolve_milestone3z_fixed_stub_changed_smoke.json`:
  independent adapter report for the stub-generated changed candidate.
- `reports/list_update_openevolve_milestone3z_zero_money.md`: this report.

## Local Endpoint Probes

Real Ollama/local-model path:

```text
api_base=http://localhost:11434/v1
model=qwen2.5-coder:1.5b
ollama installed=false
endpoint available=false
endpoint reason=URLError: <urlopen error timed out>
OpenEvolve available=true
status=blocked
```

Chocolatey setup attempt:

```powershell
choco search ollama --exact
```

Observed: `Ollama 0.24.0 [Approved]`.

```powershell
choco install ollama -y
```

Observed: failed from the non-admin shell with Chocolatey lock/permission
errors under `C:\ProgramData\chocolatey\lib` / `lib-bad`. No Ollama install was
completed by this run.

Fixed-stub transport path:

```text
api_base=http://127.0.0.1:61407/v1
model=fixed-stub-list-update-v0
endpoint available=true
status=succeeded
stubbed_transport=true
real_local_llm_run_attempted=false
real_local_llm_mutation_obtained=false
```

## Commands Run

```powershell
git switch -c openevolve-list-update-zero-money-tiny-run-v0 41a37da3ba8bbf6c82fefaeaf8e64286688f3c9c
```

```powershell
python -m pip install openevolve
```

Observed: `openevolve 0.2.27` already present in the user site. The sandboxed
Python import did not see it, but the unsandboxed runner found the user-site
`openevolve-run.exe`.

```powershell
python scripts/run_list_update_openevolve_zero_money_milestone3.py
```

Observed: blocked. Wrote
`runs/list_update_openevolve_milestone3z_zero_money/milestone3z_zero_money_status.json`.

```powershell
python scripts/run_list_update_openevolve_fixed_stub_transport_milestone3.py
```

Observed: fixed-stub transport succeeded. Wrote
`runs/list_update_openevolve_milestone3z_fixed_stub/milestone3z_zero_money_status.json`.

```powershell
python -m list_update_eval.openevolve_adapter --policy examples/list_update_openevolve/initial_program.py --suite smoke --out reports/list_update_openevolve_milestone3z_initial_smoke.json
```

Observed:

```text
combined_score=980.210526
valid=true
invalid_policy=false
timeout=false
nondeterminism=false
total_cost=42
ratio_vs_mtf=1.0
offline_oracle_ratio=1.105263157894737
offline_oracle_regret=4
```

```powershell
python -m list_update_eval.openevolve_adapter --policy runs/list_update_openevolve_milestone3z_fixed_stub/extracted_candidates/014ebc2b-7d23-4897-9b4f-a58434c62d81.py --suite smoke --out reports/list_update_openevolve_milestone3z_fixed_stub_changed_smoke.json
```

Observed:

```text
combined_score=-12000.0
valid=false
invalid_policy=true
timeout=false
nondeterminism=false
total_cost=None
ratio_vs_mtf=None
offline_oracle_ratio=None
offline_oracle_regret=None
```

```powershell
python -m pytest tests/test_list_update_eval_milestone1.py tests/test_list_update_openevolve_adapter_milestone2.py tests/test_list_update_openevolve_milestone3.py
```

Observed: `24 passed, 2 skipped in 8.86s`.

```powershell
python -m pytest
```

Observed: `165 passed, 2 skipped in 217.21s (0:03:37)`.

## Candidate Classification

Initial program SHA256:

```text
69204972702316ffb6a660890cdbc95fcfc680e7eb0977cee4743971991681e6
```

The real Ollama/local-model run produced no generated changed candidate because
the endpoint was unavailable and OpenEvolve was not started.

The fixed-stub run produced one extracted changed candidate from OpenEvolve's
JSON database:

```text
runs/list_update_openevolve_milestone3z_fixed_stub/extracted_candidates/014ebc2b-7d23-4897-9b4f-a58434c62d81.py
candidate_sha256=04e3fd1c9f10b6db354f200b182cca868ce8ebe665fac8ab4bcbcd23bdf0ed8c
classification=generated_candidate_changed_evolve_block_only
final_class=invalid_candidate
```

The stub-generated candidate changes:

```python
target_index = len(state) - 1
```

inside the EVOLVE block. The adapter rejects it honestly because for a request
already at index `0`, returning `len(state) - 1` can move the requested item
later, outside the allowed free-move range.

OpenEvolve also saved incumbent `best_program.py` snapshots. Their raw hashes
changed because OpenEvolve rewrote line endings, but normalized text matched
the initial program; the runner classifies them as
`generated_candidate_identical_to_initial`, not as generated changed
candidates.

No best valid changed-candidate report was copied to
`reports/list_update_openevolve_milestone3z_best_smoke.json`, because the only
changed candidate observed in the fixed-stub path was invalid.

## Limitations

- No real local LLM mutation ran. Ollama was not on PATH, and
  `http://localhost:11434/v1/models` timed out.
- The Chocolatey Ollama package could not be installed from this non-admin
  shell because of Windows permission/lock errors.
- The fixed-stub run is useful plumbing evidence only. It used a fixed response,
  no model inference, no autonomous mutation, and no policy discovery.
- The stub-generated changed candidate was invalid, though it was preserved and
  independently re-evaluated.
- The real local-model success criterion still needs an installed/running free
  local model endpoint, such as Ollama with `qwen2.5-coder:1.5b`.

## Milestone Status

Original Milestone 3 is not complete under the stated success criteria. A real
local LLM endpoint did not produce a mutation.

Milestone 4 is not safe to plan as an autonomous OpenEvolve search milestone
yet. It becomes safe to plan only after a real local model endpoint produces at
least one saved changed candidate and that candidate is independently
re-evaluated by `list_update_eval.openevolve_adapter`, whether valid or invalid.
