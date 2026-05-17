# List-Update Exact Evaluator Scaffold v0

Status: scaffold implemented for a future OpenEvolve side experiment.

Scope boundary: this report records an exact finite-game oracle and sanity examples only. It does not run an evolutionary search, does not report sampled scores, and does not make theorem claims.

## Inputs Read

- `reports/scouting_v2/subrun_2I_openevolve_objects.md`
- `reports/scouting_v2/synthesis.md`
- `candidate_topics/list_update/*`

Relevant local synthesis: `list_update` is the preferred OpenEvolve side experiment because it has a clean finite policy object and an exact offline optimum/work-function-style evaluator for small lists. The candidate folder still marks post-2012 open-status checks as required before theorem promotion.

## Model

The scaffold uses the full-cost standard list-update model, recorded in `scripts/list_update/MODEL.md`.

- List states are permutations of `0..n-1`.
- Accessing an item at 0-based rank `r` costs `r + 1`.
- Free exchanges after access are allowed: the accessed item can move to any earlier position for free, including staying put.
- The offline optimum may use the standard unit-cost adjacent paid exchange operation.
- The DP canonicalizes paid rearrangements before the access. Paid rearrangements after an access are charged before the next access.
- No paid-exchange variants are mixed in: no partial-cost accounting, no non-adjacent paid swaps, no discounted exchanges, and no free moves of non-requested items.

## Implemented Files

- `scripts/list_update/model.py`: model constants, validation, permutation states, free successors.
- `scripts/list_update/exact_evaluator.py`: Kendall tau paid-exchange distance, exhaustive standard transition witnesses, offline optimum DP over permutations, exact ratios.
- `scripts/list_update/policies.py`: MTF, transpose, static do-nothing, and an exact `1/2` MTF + `1/2` transpose randomized placeholder.
- `scripts/list_update/cli.py`: small JSON table emitter for fixed traces.
- `scripts/list_update/adversarial_traces.py`: exhaustive nonempty trace enumeration up to a small length bound, with per-deterministic-policy top-k finite ratios as JSON. The default is `n = 4`, and this enumerator rejects `n > 4`.
- `tests/test_list_update_evaluator.py`: hand checks, policy costs, randomized rational output, transition enumeration, and DP-vs-brute-force tests.

Supported size: `n <= 5`, with fixed small request traces. All deterministic costs are integers. Randomized-policy expectations and ratios use exact rational arithmetic.

## Hardening v1 Additions

- Empty CLI traces are rejected with `FAIL: --trace must contain at least one request`; no partial JSON payload is emitted.
- The offline witness tests now include hand-derived traces where the optimal witness uses paid exchanges before an access, including traces over `n = 3` and `n = 4`.
- The adversarial trace enumerator is a scorer only: it enumerates finite traces and emits exact JSON summaries for existing deterministic policies. It does not implement OpenEvolve.

## Exact Example Table

Initial state is `[0, 1]`.

Trace `[1, 0]`:

| object | exact cost | ratio to offline |
| --- | ---: | ---: |
| offline optimum | 3 | 1 |
| static do-nothing | 3 | 1 |
| MTF | 4 | 4/3 |
| transpose | 4 | 4/3 |

Initial state is `[0, 1, 2]`.

Trace `[2, 1, 2]`:

| object | access-cost trace | exact cost | ratio to offline |
| --- | --- | ---: | ---: |
| offline optimum | witness costs `4, 1, 2` | 7 | 1 |
| MTF | `3, 3, 2` | 8 | 8/7 |
| transpose | `3, 3, 3` | 9 | 9/7 |
| static do-nothing | `3, 2, 3` | 8 | 8/7 |
| `1/2` MTF + `1/2` transpose | exact expectation | 33/4 | 33/28 |

These are tiny trace audits only. They are not evidence about asymptotic competitive ratios.

## Verification Log

Commands run on branch `list-update-evaluator-hardening-v1`:

| command | observed status |
| --- | --- |
| `python -m unittest tests.test_list_update_evaluator` | exit code `0`; `Ran 12 tests`; `OK` |
| `python -m scripts.list_update.cli --n 3 --trace 2,1,2` | exit code `0`; JSON emitted with offline optimum cost `7`, deterministic ratios `8/7`, `9/7`, `8/7`, and randomized placeholder ratio `33/28` |
| `python -m scripts.list_update.adversarial_traces --n 2 --max-length 2 --top-k 1` | exit code `0`; JSON emitted with `trace_count: 6` and top ratio `4/3` for each deterministic policy |

## Offline Oracle

For each request and current permutation, the transition enumerator considers every access permutation. It charges Kendall tau distance from the current state to that access permutation, charges full access cost for the requested item, then enumerates all free forward moves of the requested item. The DP keeps the cheapest prefix cost for every post-access permutation.

The tests compare this DP against an independent recursive exhaustive transition enumeration for all traces of length at most `3` over `n = 3`.

## OpenEvolve Readiness

Ready for a later loop:

- candidate policy tables can call the deterministic or randomized policy evaluators;
- adversarial fixed traces can be scored against the exact offline optimum;
- exact finite ratios can be emitted as rational values;
- transition witnesses expose the offline move sequence for trace audits.

Still intentionally absent:

- no evolutionary search loop;
- no LP/minimax adversary over trace distributions;
- no COMB/projective-algorithm encoding;
- no sampled benchmarks;
- no theorem-level conclusion.

## Skeptical Audit

Why this scaffold might mislead if overread:

- `n <= 5` finite behavior may reward policies that do not scale or factor to arbitrary list sizes.
- The randomized placeholder is only a rational evaluator smoke test, not a known optimal randomized list-update policy.
- Exact finite ratios over handpicked traces are trace audits, not competitive-ratio estimates.
- The candidate folder still requires a post-2012 source sweep before any theorem-promotion claim.

What would falsify the side-experiment value:

- the exact oracle fails on independent transition checks;
- policy encodings cannot be made expressive enough to represent known baselines;
- evolved policies overfit tiny traces without producing auditable policy tables or adversarial trace families.
