# List-Update OpenEvolve Wrapper Milestone 2

Branch: `openevolve-list-update-wrapper-v0`

Status: deterministic OpenEvolve-compatible wrapper/adapter scaffold added. No
OpenEvolve evolutionary search was run, no LLM was called to evolve policies,
and no novelty or discovery is claimed.

## Files Added Or Changed

- `list_update_eval/openevolve_adapter.py`: adapter API, scoring formula, JSON
  report writer, and dry-run CLI.
- `examples/list_update_openevolve/evaluator.py`: OpenEvolve-style
  `evaluate(program_path)` entry point.
- `examples/list_update_openevolve/initial_program.py`: conservative initial
  Move-To-Front-like candidate with `# EVOLVE-BLOCK-START` and
  `# EVOLVE-BLOCK-END`.
- `examples/list_update_openevolve/config.yaml`: future-run config stub; not
  for Milestone 2 execution.
- `examples/list_update_openevolve/candidates/*.py`: hand-written valid,
  invalid, timeout, and nondeterministic test candidates.
- `tests/test_list_update_openevolve_adapter_milestone2.py`: adapter tests.
- `reports/list_update_openevolve_adapter_smoke.json`: dry-run adapter report.
- `reports/list_update_openevolve_wrapper_milestone2.md`: this report.

## Adapter API

Primary function:

```python
from list_update_eval.openevolve_adapter import evaluate_candidate

report = evaluate_candidate(
    policy_path="examples/list_update_openevolve/initial_program.py",
    suite="smoke",
    out_path="reports/list_update_openevolve_adapter_smoke.json",
)
```

The returned dictionary includes top-level and nested `metrics` fields for:

- `combined_score` / `fitness`
- `valid`, `invalid_policy`, `timeout`, `nondeterminism`
- `total_cost`
- `ratio_vs_mtf`
- `offline_oracle_ratio`
- `offline_oracle_regret`
- `policy_complexity`
- `movement_aggressiveness`
- `suite`
- `report_path`

It also includes `artifacts.evaluator_diagnostics`, which embeds the Milestone 1
evaluator report used for scoring.

## OpenEvolve Evaluator Shape

`examples/list_update_openevolve/evaluator.py` exposes:

```python
def evaluate(program_path):
    ...
```

It calls `evaluate_candidate(program_path, suite="smoke")`. If
`openevolve.evaluation_result.EvaluationResult` is importable, it returns
`EvaluationResult(metrics=..., artifacts=...)`; otherwise it returns a plain
dictionary:

```python
{"metrics": metrics, "artifacts": artifacts}
```

OpenEvolve is therefore not a hard dependency for local tests.

## Fitness Formula

Formula version: `transparent_penalty_v0`

Higher is better:

```text
combined_score = 1000 - total_penalties
```

Penalties:

```text
invalid_policy:                 10000 if true
timeout:                         5000 if true
nondeterminism:                  2500 if detected
missing_ratio_vs_mtf:            1000 if unavailable
ratio_vs_mtf:                     200 * max(0, ratio_vs_mtf - 1)
missing_offline_oracle_ratio:    1000 if unavailable
offline_oracle_ratio:             150 * max(0, offline_oracle_ratio - 1)
missing_offline_oracle_regret:   1000 if unavailable
offline_oracle_regret:              1 * max(0, offline_oracle_regret)
source_length:                    max(0, source_length - 1200) / 100
ast_node_count:                   max(0, ast_node_count - 200) / 20
movement_aggressiveness:           25 * max(0, avg_position_shift - 1.25)
```

This is intentionally transparent and conservative. It shapes future search
toward valid, deterministic, small policies that are not much worse than
Move-To-Front and not far from the small-suite offline oracle. It is not tuned
as a leaderboard objective.

## Dry Run

Command:

```powershell
python -m list_update_eval.openevolve_adapter --policy examples/list_update_openevolve/initial_program.py --suite smoke --out reports/list_update_openevolve_adapter_smoke.json
```

Observed summary:

```text
policy=initial_program suite=smoke combined_score=980.210526 valid=true invalid=false timeout=false nondeterminism=false total_cost=42 ratio_vs_mtf=1.0 offline_oracle_ratio=1.105263157894737 wrote C:\Users\poin\Documents\ds-frontier-scout\reports\list_update_openevolve_adapter_smoke.json
```

Output report:

```text
reports/list_update_openevolve_adapter_smoke.json
```

Key dry-run metrics:

```text
schema_version=list_update_eval.openevolve_adapter.milestone2.v0
policy_name=initial_program
combined_score=980.210526
valid=True
total_cost=42
ratio_vs_mtf=1.0
offline_oracle_ratio=1.105263157894737
offline_oracle_regret=4
fitness_formula_version=transparent_penalty_v0
```

## Tests

Required paired command:

```powershell
python -m pytest tests/test_list_update_eval_milestone1.py tests/test_list_update_openevolve_adapter_milestone2.py
```

Observed summary:

```text
collected 16 items
tests\test_list_update_eval_milestone1.py ......                         [ 37%]
tests\test_list_update_openevolve_adapter_milestone2.py ..........       [100%]
16 passed in 8.75s
```

Full suite command:

```powershell
python -m pytest
```

Observed summary:

```text
collected 157 items
157 passed in 261.61s (0:04:21)
```

Note: the sandboxed `python -m pytest` initially could not read the already
installed user-site `pytest` package, so pytest commands were run outside the
filesystem sandbox after approval. The commands above are the commands that
were executed.

## Known Limitations

- The adapter inherits Milestone 1 process isolation and timeout behavior; it is
  not a security sandbox for malicious Python.
- Nondeterminism detection is still repeated isolated evaluation. It catches
  obvious instability, not all hidden state or environment-dependent behavior.
- The smoke suite is intentionally tiny. The score is a wrapper sanity metric,
  not evidence of a strong policy.
- The exact offline oracle remains limited to the small deterministic suites
  supported by Milestone 1.
- The config file is a schema-shaped future-run stub only. It has not been
  validated against a real OpenEvolve installation.
- The fitness constants are conservative placeholders and should be reviewed in
  Milestone 3 before any real search budget is spent.

## Milestone 3 / Do Not Run Yet

Future command, clearly not executed in Milestone 2:

```powershell
openevolve run --config examples/list_update_openevolve/config.yaml
```

Before running this, Milestone 3 should confirm the installed OpenEvolve CLI
schema, decide whether `smoke` is still the right first suite, and add explicit
run-output handling for evolved candidates.
