# List-Update OpenEvolve Milestone 3 Tiny Dry-Run

Branch: `openevolve-list-update-tiny-run-v0`

Starting commit: `71ca11120227292f6920d1477af9d50e10a21c90`

Status: blocked by missing LLM API credentials after installing OpenEvolve. No
evolutionary mutation ran, no candidate policy was generated, and no discovery
or novelty is claimed.

## Files Added Or Changed

- `examples/list_update_openevolve/config_tiny_milestone3.yaml`: tiny
  integration-only config using the installed OpenEvolve 0.2.x schema.
- `scripts/run_list_update_openevolve_tiny_milestone3.py`: guarded runner that
  checks for OpenEvolve, calls the `openevolve-run` CLI shape, records
  blocked/run artifacts, and re-evaluates generated Python candidates if a run
  succeeds.
- `tests/test_list_update_openevolve_milestone3.py`: config and graceful-blocker
  tests, plus a guarded generated-candidate interface check.
- `reports/list_update_openevolve_milestone3_initial_smoke.json`: fresh
  deterministic adapter evaluation for the initial program.
- `runs/list_update_openevolve_milestone3_tiny/`: local run artifact directory
  containing the copied config and blocked status JSON.
- `reports/list_update_openevolve_milestone3_tiny_run.md`: this report.

## Commands Run

```powershell
git switch -c openevolve-list-update-tiny-run-v0 71ca111
```

```powershell
python -c "import importlib.util; spec=importlib.util.find_spec('openevolve'); print(spec.origin if spec else 'NOT_FOUND')"
```

Initial observation before install: `NOT_FOUND`.

```powershell
python -m pip install openevolve
```

Observed: installed `openevolve-0.2.27` and dependencies into the Python user
site.

```powershell
python -c "import openevolve, pathlib; print(pathlib.Path(openevolve.__file__).resolve())"
```

Observed outside the filesystem sandbox:
`C:\Users\poin\AppData\Roaming\Python\Python314\site-packages\openevolve\__init__.py`.

```powershell
& "C:\Users\poin\AppData\Roaming\Python\Python314\Scripts\openevolve-run.exe" --help
```

Observed: installed CLI accepts:

```text
openevolve-run initial_program evaluation_file --config CONFIG --output OUTPUT --iterations ITERATIONS
```

```powershell
python scripts/run_list_update_openevolve_tiny_milestone3.py
```

Observed result after install: blocked because `OPENAI_API_KEY` is not set. The runner wrote
`runs/list_update_openevolve_milestone3_tiny/milestone3_tiny_run_status.json`.

```powershell
$env:OPENAI_API_KEY='dummy-for-config-parse-only'; python -c "from openevolve.config import Config; c=Config.from_yaml('examples/list_update_openevolve/config_tiny_milestone3.yaml'); print(f'max_iterations={c.max_iterations} population_size={c.database.population_size} evaluator_timeout={c.evaluator.timeout} model={c.llm.models[0].name}')"
```

Observed: `max_iterations=1 population_size=2 evaluator_timeout=10 model=gpt-5-mini`.

```powershell
python -m list_update_eval.openevolve_adapter --policy examples/list_update_openevolve/initial_program.py --suite smoke --out reports/list_update_openevolve_milestone3_initial_smoke.json
```

```powershell
python -m pytest tests/test_list_update_eval_milestone1.py tests/test_list_update_openevolve_adapter_milestone2.py tests/test_list_update_openevolve_milestone3.py
```

Observed summary after the install-aware runner update:
`19 passed, 1 skipped in 8.55s`.

```powershell
python -m pytest
```

Observed summary after the install-aware runner update:
`160 passed, 1 skipped in 196.72s (0:03:16)`.

## OpenEvolve Availability

OpenEvolve was downloaded and installed successfully via pip:
`openevolve-0.2.27`.

The installed package is visible outside the filesystem sandbox, and the
installed CLI is:

```text
C:\Users\poin\AppData\Roaming\Python\Python314\Scripts\openevolve-run.exe
```

The tiny run is still blocked because `OPENAI_API_KEY` is not set in the
environment, so OpenEvolve cannot request the one intended mutation.

Blocked status JSON:

```text
runs/list_update_openevolve_milestone3_tiny/milestone3_tiny_run_status.json
```

Recorded blockers:

- `OPENAI_API_KEY is not set; OpenEvolve can be imported but cannot request the one tiny mutation`

The runner's setup instructions are intentionally conservative: verify that
either `python -c "import openevolve"` succeeds or `openevolve-run --help` is
available, set `OPENAI_API_KEY`, then rerun
`python scripts/run_list_update_openevolve_tiny_milestone3.py`.

## Run Status

Run status: blocked.

OpenEvolve available: yes.

Actual command prepared by the runner:

```text
C:\Users\poin\AppData\Roaming\Python\Python314\Scripts\openevolve-run.exe C:\Users\poin\Documents\ds-frontier-scout\examples\list_update_openevolve\initial_program.py C:\Users\poin\Documents\ds-frontier-scout\examples\list_update_openevolve\evaluator.py --config C:\Users\poin\Documents\ds-frontier-scout\examples\list_update_openevolve\config_tiny_milestone3.yaml --output C:\Users\poin\Documents\ds-frontier-scout\runs\list_update_openevolve_milestone3_tiny --iterations 1 --log-level INFO
```

Artifact directory:

```text
runs/list_update_openevolve_milestone3_tiny/
```

Artifacts written:

- `runs/list_update_openevolve_milestone3_tiny/config_tiny_milestone3.yaml`
- `runs/list_update_openevolve_milestone3_tiny/milestone3_tiny_run_status.json`

Generated candidate path: none.

Independent generated-candidate re-evaluation JSON path: none.

## Initial Program Re-Evaluation

Fresh initial-program adapter report:

```text
reports/list_update_openevolve_milestone3_initial_smoke.json
```

Metrics:

```text
combined_score=980.210526
valid=True
invalid_policy=False
timeout=False
nondeterminism=False
total_cost=42
ratio_vs_mtf=1.0
offline_oracle_ratio=1.105263157894737
offline_oracle_regret=4
```

Generated-candidate comparison: not available because OpenEvolve did not run
and no generated candidate exists.

## Invalid, Timeout, And Nondeterminism Observations

- Initial program: valid, no timeout, no nondeterminism detected.
- OpenEvolve run: not executed because `OPENAI_API_KEY` was unavailable.
- Generated candidates: none, so no invalid generated policies are hidden.

## Known Limitations

- The tiny config was parsed successfully by the installed OpenEvolve config
  loader using a dummy API key, but no LLM request was made.
- The runner can verify EVOLVE-block-only changes for discovered Python
  candidates, but no generated candidates were present to check.
- No OpenEvolve artifact recovery beyond the blocked status was exercised.
- No policy-quality conclusion is possible from this milestone.

## Milestone 4 Readiness

Milestone 4 is not safe to plan as a search or policy-discovery milestone yet.
First, set `OPENAI_API_KEY` for the OpenEvolve mutation call, then rerun this
exact tiny Milestone 3 integration dry-run. Milestone 4 should wait until the
run completes with at least one generated candidate that is independently
re-evaluated by `list_update_eval.openevolve_adapter`.

## Addendum: Cost-Effective Paths Forward

Research date: May 18, 2026.

Question: can we proceed without spending OpenAI API credits, and what is the
best cost/validity tradeoff for finishing the tiny Milestone 3 dry-run?

### Source Notes

- OpenEvolve 0.2.27 is the installed package version in this environment. PyPI
  lists `openevolve-0.2.27` as uploaded on March 18, 2026:
  <https://pypi.org/project/openevolve/>.
- The OpenEvolve README says it requires LLM access through an
  OpenAI-compatible API, supports direct OpenAI, Google Gemini,
  local Ollama/vLLM endpoints, and custom `api_base` providers:
  <https://github.com/algorithmicsuperintelligence/openevolve>.
- The installed OpenEvolve 0.2.27 code also has `llm.manual_mode`, which writes
  prompt tasks to a filesystem queue and waits for answer JSON files. This is
  useful for plumbing, but the generated patch is human-assisted rather than an
  autonomous LLM/API mutation.
- OpenAI's current model docs recommend smaller variants such as
  `gpt-5.4-mini` or `gpt-5.4-nano` for latency/cost-sensitive workloads:
  <https://developers.openai.com/api/docs/models>.
- `gpt-5.4-nano` is documented at `$0.20 / 1M` input tokens and
  `$1.25 / 1M` output tokens, with Chat Completions support:
  <https://developers.openai.com/api/docs/models/gpt-5.4-nano>.
- `gpt-5-nano` is documented at `$0.05 / 1M` input tokens and `$0.40 / 1M`
  output tokens, also with Chat Completions support:
  <https://developers.openai.com/api/docs/models/gpt-5-nano>. OpenAI's docs
  describe it as cheaper, while recommending `gpt-5.4-nano` for most new
  speed/cost-sensitive workloads.
- OpenAI's cost optimization guide recommends reducing request count, reducing
  input/output tokens, and selecting smaller models. It also points to Batch
  API and flex processing for asynchronous/lower-priority work:
  <https://developers.openai.com/api/docs/guides/cost-optimization>.
- Batch API gives a 50% discount but has asynchronous turnaround, so it is not
  directly compatible with the synchronous `openevolve-run` loop without an
  adapter or proxy:
  <https://developers.openai.com/api/docs/guides/batch>.
- Flex processing can reduce Chat Completions cost for lower-priority tasks,
  but OpenEvolve's stock client does not expose `service_tier`, so using it
  would require a small OpenEvolve patch or OpenAI-compatible proxy:
  <https://developers.openai.com/api/docs/guides/flex-processing>.
- Ollama documents an OpenAI-compatible `/v1/chat/completions` endpoint at
  `http://localhost:11434/v1/`, with an API key value required but ignored:
  <https://docs.ollama.com/api/openai-compatibility>.
- vLLM documents an OpenAI-compatible server with `vllm serve` and a
  `http://localhost:8000/v1` base URL:
  <https://docs.vllm.ai/en/latest/serving/openai_compatible_server/>.
- LM Studio documents a local API server with OpenAI-compatible endpoints:
  <https://lmstudio.ai/docs/developer/core/server>.

### Ranked Options

1. **Cheapest honest OpenAI-backed Milestone 3 completion**

   Use a single `openevolve-run` iteration with `gpt-5-nano` or
   `gpt-5.4-nano`, `retries: 0`, `population_size: 2`, `max_iterations: 1`,
   `llm.max_tokens` capped at 512 or 1024, and prompt artifact bytes capped or
   omitted.

   Estimated cost for a carefully bounded one-iteration dry-run is likely
   well under one cent. For example, a deliberately pessimistic 20k input-token
   prompt plus 1k output tokens would cost about `$0.0014` on `gpt-5-nano`, or
   about `$0.00525` on `gpt-5.4-nano`, before any taxes/regional uplift. The
   real cost could be higher if OpenEvolve makes more than one generation call
   or if large artifacts are included in prompts, so the run should still be
   treated as metered.

   Best model choice:

   - `gpt-5-nano`: lowest listed OpenAI token cost; best for a plumbing-only
     dry-run where mutation quality is secondary.
   - `gpt-5.4-nano`: still very cheap and the current recommended
     speed/cost-sensitive starting point in OpenAI docs; better default if we
     want the dry-run to reflect the current model family.

   Recommended if the goal is to satisfy the original Milestone 3 success
   criteria with the least engineering work and minimal spend.

2. **Zero OpenAI credits, still a real OpenEvolve LLM run**

   Point OpenEvolve at a local or non-OpenAI OpenAI-compatible endpoint, such
   as Ollama, vLLM, or LM Studio. Example shape:

   ```yaml
   llm:
     api_base: "http://localhost:11434/v1"
     api_key: "ollama"
     primary_model: "gpt-oss:20b"
   ```

   This can satisfy "OpenEvolve generated the candidate" if the local endpoint
   actually returns the mutation. It avoids OpenAI API credits, but it is not
   free in engineering time: we must install/start a local server, choose a
   model that follows SEARCH/REPLACE diffs reliably, and capture the endpoint
   details in the report. Quality and latency may be worse than the OpenAI
   nano path.

   Recommended if spending any OpenAI credits is unacceptable and a local model
   server is already available or easy to start.

3. **Manual-mode plumbing dry-run**

   Use OpenEvolve's installed `llm.manual_mode` to enqueue the mutation prompt,
   then have a human or Codex supply an answer JSON file. This should exercise
   much of the OpenEvolve controller/evaluator/artifact pipeline without API
   credits.

   This is not an autonomous evolution result. The report must label any
   candidate as manual-mode assisted, not as an API-generated OpenEvolve
   discovery. It is useful if the near-term goal is debugging run artifacts and
   adapter compatibility, but it does not fully satisfy the original Milestone
   3 criterion that OpenEvolve itself obtains a mutation from its configured
   LLM path.

4. **Codex-authored candidate outside OpenEvolve**

   Codex can hand-write one or more policy candidates and re-evaluate them with
   `list_update_eval.openevolve_adapter`. This costs no OpenAI API credits
   beyond the current Codex session, and it is useful for evaluator hardening.

   It is not an OpenEvolve integration run and should not be used to claim
   Milestone 3 success.

5. **Batch/Flex optimization**

   Batch and flex are attractive for larger, asynchronous campaigns. For the
   tiny Milestone 3 run they are not the first move, because stock OpenEvolve
   expects synchronous Chat Completions. Use them later only if we patch
   OpenEvolve, add an OpenAI-compatible proxy, or run many queued mutation
   requests where asynchronous turnaround is acceptable.

### Recommended Next Step

Best practical path: run exactly one tiny OpenEvolve iteration using an OpenAI
nano-class model, after tightening the config to minimize prompt/output size.
Use `gpt-5-nano` if pure cost minimization is the priority, or
`gpt-5.4-nano` if we prefer the current recommended speed/cost-sensitive model
family. Keep all deterministic evaluator semantics unchanged.

Recommended config adjustments before rerun:

- change `llm.primary_model` from `gpt-5-mini` to either `gpt-5-nano` or
  `gpt-5.4-nano`;
- reduce `llm.max_tokens` to `512` for the dry-run;
- keep `llm.retries: 0`;
- set `prompt.max_artifact_bytes` to a small cap such as `2048`, or set
  `prompt.include_artifacts: false` for this plumbing-only run;
- keep `evaluator.use_llm_feedback: false`;
- keep `max_iterations: 1`, `database.population_size: 2`, and
  `database.num_islands: 1`;
- preserve the runner's independent EVOLVE-block-only check and deterministic
  post-run re-evaluation requirement.

If the user wants zero OpenAI API credits, the best next path is to add a
second tiny config for an explicit local endpoint, probably Ollama first
because its OpenAI-compatible URL and ignored dummy key are simple:
`api_base: "http://localhost:11434/v1"` and `api_key: "ollama"`. That route
should be reported as a local-model OpenEvolve run, with model name, server
version, and any failed/invalid candidates preserved.

Milestone 4 should still wait. The next milestone-worthy event is one completed
tiny run, with a generated candidate path and independent adapter
re-evaluation JSON.

### Zero-Money Path, Strict Version

Additional check date: May 18, 2026.

Interpretation: "do not spend any money at all" means no OpenAI API credits, no
paid hosted-model credits, no rented GPU, and no paid subscription dependency.
It may still require local CPU/GPU time, disk space, electricity, and free
downloads unless we choose a manual/stubbed path.

Current local availability probe:

```text
ollama: not found on PATH
lms: not found on PATH
nvidia-smi: not found on PATH
python import vllm: false
python import llama_cpp: false
```

So this checkout cannot run a local OpenEvolve LLM mutation immediately. A
zero-money run needs one of the following.

#### Option A: Free Local LLM, Real OpenEvolve Mutation

This is the only zero-money path that can honestly preserve the statement
"OpenEvolve obtained a mutation from an LLM." Use free local inference on
existing hardware.

Most practical stack:

1. Install the free Ollama desktop/CLI locally.
2. Pull a free code-capable model.
3. Configure OpenEvolve with Ollama's OpenAI-compatible endpoint:

```yaml
llm:
  api_base: "http://localhost:11434/v1"
  api_key: "ollama"
  primary_model: "qwen2.5-coder:1.5b"
```

Possible models:

- `qwen2.5-coder:1.5b` or `qwen2.5-coder:3b`: small enough to try on modest
  local hardware; likely adequate for a one-line EVOLVE-block mutation, but
  may fail to follow SEARCH/REPLACE format.
- `qwen2.5-coder:7b`: better chance of coherent diffs, more memory/latency.
- `gpt-oss:20b`: OpenAI open-weight model; stronger reasoning but much heavier.
  OpenAI states `gpt-oss-20b` can run with about 16 GB of memory and that the
  weights are freely available. See:
  <https://openai.com/open-models/> and
  <https://openai.com/index/introducing-gpt-oss/>.

Primary sources supporting this path:

- Ollama documents OpenAI-compatible `/v1/chat/completions` at
  `http://localhost:11434/v1/`, with a required-but-ignored local API key:
  <https://docs.ollama.com/api/openai-compatibility>.
- Ollama's docs list gpt-oss, Gemma, DeepSeek-R1, Qwen3, and other local model
  families as supported examples: <https://docs.ollama.com/>.
- OpenEvolve documents local Ollama/vLLM configuration through `api_base`:
  <https://github.com/algorithmicsuperintelligence/openevolve>.

Pros:

- No API credits and no hosted-model bill.
- Still a genuine OpenEvolve LLM integration run if the local model returns the
  mutation.
- Local artifacts remain reproducible if model name/version and server details
  are recorded.

Cons:

- Requires free installation/downloads.
- Large model files may consume several GB to tens of GB of disk.
- CPU-only inference may be slow.
- Small local models may produce malformed diffs, change outside the EVOLVE
  block, or fail to generate useful code. The runner's EVOLVE-block guard and
  deterministic adapter re-evaluation are therefore mandatory.

#### Option B: Free Local LLM Through vLLM Or LM Studio

This is equivalent in principle to Ollama but currently less convenient on this
machine because neither `vllm` nor `lms` is installed.

- vLLM documents an OpenAI-compatible server using `vllm serve` and
  `http://localhost:8000/v1`:
  <https://docs.vllm.ai/en/latest/serving/openai_compatible_server/>.
- LM Studio documents a local server with OpenAI-compatible endpoints:
  <https://lmstudio.ai/docs/developer/core/server>.

Recommended only if one of these tools is already installed or preferred by the
user. Otherwise Ollama has the lowest setup friction for a zero-money attempt.

#### Option C: Manual Mode, No Model Cost

OpenEvolve 0.2.27 has `llm.manual_mode`, which enqueues the mutation prompt to a
local directory and waits for a manually written answer JSON. This costs no API
credits and no model download, and it exercises much of the OpenEvolve
controller/evaluator/artifact flow.

However, the candidate is manual-assisted. It should be reported as:

```text
OpenEvolve manual-mode integration dry-run; mutation text supplied manually.
No autonomous LLM/API generation occurred.
```

This is useful for debugging artifact recovery and candidate re-evaluation, but
it does not fully satisfy the original autonomous OpenEvolve dry-run criterion.

#### Option D: Fixed Local OpenAI-Compatible Stub

We can write a tiny local HTTP server using only Python's standard library that
implements enough of `/v1/chat/completions` to return one fixed SEARCH/REPLACE
diff inside the EVOLVE block. Then OpenEvolve can call a "local API" without
API credits, paid services, or model downloads.

This is the strictest zero-money, zero-model-download path. It would verify:

- OpenEvolve can call an OpenAI-compatible endpoint;
- OpenEvolve can apply a returned diff;
- the evaluator adapter receives and scores the candidate;
- artifacts and independent re-evaluation are written.

But it is not an LLM run. It must be labeled:

```text
Stubbed OpenAI-compatible transport test; fixed response, no model inference,
no autonomous mutation, no policy discovery.
```

This is not enough for Milestone 4 readiness unless the milestone definition is
explicitly relaxed to allow a stubbed transport smoke test before a true local
or hosted LLM run.

#### Zero-Money Recommendation

If the user wants no spending at all, the best honest sequence is:

1. Add a separate `config_tiny_milestone3_ollama.yaml` and keep the current
   OpenAI-key config untouched.
2. Try Ollama with a small free model first, probably `qwen2.5-coder:1.5b` or
   `qwen2.5-coder:3b`, because the mutation target is tiny and output quality
   only needs to clear the SEARCH/REPLACE and policy-interface bars.
3. If the small model fails formatting, try a stronger local model such as
   `qwen2.5-coder:7b` or `gpt-oss:20b`, assuming the machine has enough memory.
4. Keep the same guardrails: one iteration, population 2, no LLM feedback, small
   output cap, no evaluator semantic changes, EVOLVE-block-only check, and
   independent deterministic re-evaluation.
5. If local model setup is not acceptable, do a manual-mode or fixed-stub
   transport test and explicitly mark it as a non-autonomous, non-discovery
   plumbing test.

Under a strict zero-money constraint, Milestone 4 should only be planned after
Option A or B succeeds with an actual local model response. Manual/stubbed
success is useful engineering evidence, but not evidence that OpenEvolve can
autonomously produce candidate policies in this repository.
