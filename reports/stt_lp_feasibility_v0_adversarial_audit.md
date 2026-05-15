# STT LP Feasibility Checker v0 Adversarial Audit

Date: 2026-05-15

Audited artifact: exact rational primal feasibility checking for
`golinsky_stt_lp_v0` on branch `stt-lp-feasibility-v0`.

Verdict: merge-ready after the patches in this audit.

## Executive Summary

The checker matches the repository's source-backed
`golinsky_stt_lp_v0` specification for dense proof-mode primal feasibility:

- `D_i` exists for every topology vertex.
- `X_ij` exists exactly for ordered pairs `i != j`.
- `Z_kij` exists exactly for strict path-interior vertices `k` and normalized
  unordered endpoint keys `i < j`.
- Nonnegativity, ancestry, loose-LCA, and depth inequalities are generated with
  the specified quantification and directions.
- Objective replay is `sum_i f_i D_i` in LP strict-depth convention, with
  search-cost metadata reported as `sum_i f_i (D_i + 1)`.

I found one schema-drift risk rather than a mathematical inequality bug:
`lp_solution` silently ignored extra nested fields whenever `variables` was
present. That could let a stale or malformed certificate carry shadow
LP metadata without the checker objecting. I patched proof-mode parsing to
reject unsupported nested `lp_solution` fields and added regression coverage.

This checker is not an LP solver, not a root-rounding checker, not an
integrality-gap verifier, and not a theorem claim. A passing certificate means
only that one supplied rational primal point satisfies the v0 constraints
exactly.

## Files Audited

- `reports/stt_lp_spec_golinsky_v0.md`
- `reports/stt_lp_spec_golinsky_v0_adversarial_audit.md`
- `reports/stt_lp_certificate_schema.md`
- `reports/stt_lp_feasibility_v0_implementation_note.md`
- `docs/stt_lp_feasibility_v0.md`
- `docs/stt_checker_v0.md`
- `README.md`
- `scripts/stt_checker/lp_feasibility.py`
- `scripts/stt_checker/cli.py`
- `scripts/stt_checker/certificates.py`
- `scripts/stt_checker/enumerate_stts.py`
- `scripts/stt_checker/frontier_artifacts.py`
- `scripts/stt_checker/rationals.py`
- `scripts/stt_checker/stt.py`
- `scripts/stt_checker/topology.py`
- `scripts/stt_checker/topology_generation.py`
- `tests/test_stt_lp_feasibility.py`
- `tests/test_stt_checker.py`
- `examples/stt_lp/path_4_stt_induced_lp.json`
- `examples/stt_lp/star_4_stt_induced_lp.json`
- `examples/stt_lp/path_4_negative_d_invalid.json`
- `examples/stt/path_4_proof.json`
- `examples/stt/star_4_proof.json`
- `examples/stt/long_star_7.json`

## Source Fidelity

Status: confirmed for the implemented v0 scope.

`scripts/stt_checker/lp_feasibility.py` generates the same v0 variable families
specified in `reports/stt_lp_spec_golinsky_v0.md`:

- `D`: one variable per vertex.
- `X`: all ordered pairs `(i,j)` with `i != j`.
- `Z`: triples `(k,i,j)` only when `i < j` and `k` is strictly inside the
  base-tree path from `i` to `j`.

The checker correctly omits `Z` variables for adjacent endpoints and rejects
endpoint `Z` variables and reversed endpoint keys in proof mode.

Constraint directions match the spec:

- nonnegativity is checked as each variable `>= 0`;
- ancestry is checked once per unordered endpoint pair as
  `X_ij + X_ji + sum_k Z_kij >= 1`;
- loose-LCA is checked as `Z_kij <= X_ki` and `Z_kij <= X_kj`;
- depth is checked as `D_i >= sum_{j != i} X_ji`.

The checker accumulates all constraint violations after successful
parse/domain validation and reports family, indices, exact LHS/RHS, sense, and
slack.

## Issues Found And Patched

### Fixed: Nested `lp_solution` Schema Drift

Before this audit, `parse_dense_assignment` accepted:

```json
{
  "lp_solution": {
    "variables": { "...": "..." },
    "relaxation_version": "shadowed_or_stale_value"
  }
}
```

and ignored the extra nested field. The authoritative relaxation fields are
top-level in `stt-lp-cert-v0`, but silently accepting stale nested metadata is
bad proof-infrastructure hygiene.

Patch:

- `scripts/stt_checker/lp_feasibility.py` now rejects unsupported nested
  `lp_solution` fields when `variables` is present.
- `docs/stt_lp_feasibility_v0.md` documents the fail-closed behavior.
- `tests/test_stt_lp_feasibility.py` includes a regression test.

## Tests Added Or Strengthened

Strengthened `tests/test_stt_lp_feasibility.py` with coverage for:

- `n=1` and `n=2` variable-domain edge cases.
- Exact schema enforcement for `schema_version`, `mode`, `relaxation`, and
  `relaxation_version`.
- Rejection of top-level `root_rounding` and `integrality_gap` in proof mode.
- Rejection of unsupported nested `lp_solution` fields.
- Exact violation metadata for LHS/RHS/sense/slack.
- Multiple simultaneous constraint violations being collected.
- Unnormalized rational objective replay.
- Missing and extra objective frequency keys.
- STT-induced LP construction on a non-path, non-star tree.
- A feasible fractional point on a two-vertex tree that is not STT-induced.
- `check-lp --verbose --normalized-json` output behavior.

Existing tests already covered:

- missing, unknown, and duplicate variables;
- float and decimal-string rejection;
- one violation in each constraint family;
- objective mismatch rejection;
- checked-in path and star LP fixtures;
- pass/fail CLI exit behavior.

## Remaining Limitations

- No LP solving is implemented.
- No root rounding is implemented.
- No integrality-gap checking is implemented.
- No projection or lower-envelope testing is implemented.
- No exact dual certificate support exists.
- No optional LP variants are supported.
- Dense proof-mode certificates are required; sparse zero-default encodings
  remain a future schema decision.
- The long-star integrality-gap smoke target still lacks a checked-in full
  source-transcribed `(X,Z,D)` certificate. The current LP fixtures are
  STT-induced path and star examples plus one negative example.
- Direct fidelity to Golinsky's original thesis remains blocked by source
  access, as noted in the LP spec audit. The implemented target is the
  Sadeh-Kaplan-Zwick presentation/code version captured by
  `golinsky_stt_lp_v0`.

## Commands Run

All commands were run from repository root on 2026-05-15.

```text
python -m unittest -v tests.test_stt_lp_feasibility
```

Result: passed, 15 tests.

```text
python -m unittest discover -v
```

Result: passed, 43 tests.

```text
python -m scripts.stt_checker.cli check examples/stt/path_4_proof.json
```

Result: passed, `weighted_cost=2`.

```text
python -m scripts.stt_checker.cli check examples/stt/star_4_proof.json
```

Result: passed, `weighted_cost=7/4`.

```text
python -m scripts.stt_checker.cli check examples/stt/long_star_7.json
```

Result: passed, `weighted_cost=48/23`.

```text
python -m scripts.stt_checker.frontier_artifacts --max-n 7 --max-enumeration 100000
```

Result: passed. It rewrote the expected frontier artifact paths with no
content diff observed afterward.

```text
python -m scripts.stt_checker.cli check-lp examples/stt_lp/path_4_stt_induced_lp.json
```

Result: passed, `depth_objective=1`.

```text
python -m scripts.stt_checker.cli check-lp examples/stt_lp/star_4_stt_induced_lp.json
```

Result: passed, `depth_objective=3/4`.

## Merge Recommendation

Merge-ready.

The only patched implementation behavior is a fail-closed schema check for
nested `lp_solution` fields. The mathematical LP constraint implementation
appears faithful to the checked v0 spec, and the test suite now covers the
main indexing, inequality-direction, objective-convention, edge-case, and CLI
failure modes that would be most likely to cause false positives or false
negatives in later proof-infrastructure use.
