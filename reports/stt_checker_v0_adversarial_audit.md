# STT Checker v0 Adversarial Audit

Date: 2026-05-15

Scope: adversarial audit of the exact combinatorial checker scaffold for
`search_trees_on_trees_lp`. This audit covers the v0 proof-mode STT checker
only. It does not audit or implement Golinsky LP constraints.

## Executive Status

The checker is merge-ready for the v0 combinatorial proof scaffold after the
patches described below. It is not LP-proof-ready, and it correctly keeps
`lp_solution`, `root_rounding`, and `integrality_gap` unsupported in proof
mode.

The branch state already included these prior fixes before this report was
written:

- topology vertices are required to be exactly `0..n-1`;
- `edge-diameter-k` uses line-graph edge distance, not ordinary vertex-tree
  diameter;
- path, star, and the checker-only 7-node edge-diameter-3 fixture use the
  corrected edge-diameter labels;
- docs describe the corrected edge-diameter convention;
- CLI `--max-enumeration` works after subcommands as well as before them;
- tests cover rational rejection, topology boundary labels, and the
  enumeration safety cap.

This audit added the following additional hardening:

- proof and audit certificates must explicitly provide `mode`;
- arbitrary declared subclass labels are rejected instead of silently ignored;
- `tests/__init__.py` was added so `python -m unittest discover -v` actually
  discovers the test suite from the repository root.

## Findings And Patches

### Fixed: missing `mode` was accepted

`check_certificate` previously defaulted absent `mode` to `"proof"`. The v0
certificate subset and examples require an explicit `"proof"` or `"audit"`
mode, and the audit target explicitly includes checking `mode`.

Impact: a malformed certificate could be accepted as proof-mode input.

Patch:

- `scripts/stt_checker/certificates.py` now raises `ValueError("mode: missing")`
  when `mode` is absent.
- `tests/test_stt_checker.py` includes `test_missing_mode_fails`.

### Fixed: arbitrary declared subclass labels were accepted

`TreeTopology.validate_declared_labels` checked derived labels when a declared
label looked like `path`, `star`, or `edge-diameter-*`, but ignored arbitrary
strings. Since the schema has a finite declared-label vocabulary, accepting
`"not-a-schema-label"` was schema drift.

Impact: malformed topology metadata could pass validation and appear in the
normalized certificate.

Patch:

- unsupported labels now fail closed;
- `unknown` and `almost-star` remain accepted as advisory labels;
- `tests/test_stt_checker.py` covers unsupported-label rejection and advisory
  label acceptance.

### Fixed: root test discovery ran zero tests

The required command `python -m unittest discover -v` initially ran zero tests
from the repository root until `tests/__init__.py` was present.

Impact: CI or a human following the audit command could get a false sense of
coverage.

Patch:

- added `tests/__init__.py`;
- verified the required discovery command now runs 18 tests.

## Audit By Target

### 1. Exact Rational Parsing

Status: acceptable for v0.

Checked behavior:

- rejects JSON floats;
- rejects decimal strings such as `"0.5"`;
- rejects zero denominators in strings and rational objects;
- rejects malformed rational objects with extra keys;
- normalizes fractions through `fractions.Fraction`;
- rejects booleans as integers.

Residual note: strings are stripped before parsing, so `" 1/2 "` is accepted.
This is not mathematically dangerous, but if the schema wants strict lexical
JSON values, add a follow-up test and reject surrounding whitespace.

### 2. Topology Validation

Status: acceptable for v0 after the existing branch fixes and this audit's
label hardening.

Checked behavior:

- enforces `vertices == [0, ..., n-1]`;
- rejects loops, duplicate undirected edges, invalid endpoints, and wrong edge
  count;
- checks connectivity;
- computes path and star labels;
- computes edge diameter by line-graph distance;
- handles `n=1` and `n=2` as `path`, `star`, and `edge-diameter-0`.

Important correction already present in branch baseline: a 4-vertex path has
`edge-diameter-2`, a 4-vertex star has `edge-diameter-1`, and the 7-node
long-star fixture has `edge-diameter-3` under the line-graph convention.

Residual note: `almost-star` is accepted only as advisory metadata and is not
checked. That matches v0 docs.

### 3. Recursive STT Validation

Status: acceptable for v0.

Checked behavior:

- validates that declared components are nonempty connected induced subtrees;
- starts recursion from the full topology vertex set;
- requires every reached non-singleton component to have exactly one declared
  root;
- infers omitted singleton roots;
- accepts explicit singleton roots only when they match the singleton vertex;
- rejects unreached declared components;
- derives parent and depth maps;
- supports `depth_base` 0 and 1 through the same recursive derivation.

Residual design choice: `component_roots` is treated as an order-insensitive
flat map. The broader schema says the first component is all vertices, but the
v0 docs describe a flat recursive root map. I did not change this because it is
ambiguous rather than mathematically wrong. If order is intended to be part of
the proof format, add a schema rule and a test.

### 4. Enumeration

Status: acceptable for v0 small instances.

Checked behavior:

- recursively enumerates one root choice per connected recursive component;
- tiny counts match tests: path on 4 vertices has 14 STTs, star on 4 vertices
  has 16 STTs, the checker-only 7-node edge-diameter-3 fixture has 807 STTs,
  and the SKZ source-aligned long-star fixture has 662 STTs;
- exact weighted optimum is computed with rational costs;
- safety cap raises `EnumerationLimitExceeded` once a complete enumeration
  would exceed the cap.

Residual note: enumeration materializes child option lists recursively, so the
cap is not a memory guard for very large components. This is acceptable for
v0's small-instance role but should be revisited before using enumeration as a
general proof backend.

### 5. Certificate Checking

Status: acceptable for v0 combinatorial certificates.

Checked behavior:

- validates `schema_version`;
- now requires explicit `mode`;
- validates topology, weights, STT, cost, and optional integer optimum;
- rejects proof-mode `lp_solution`, `root_rounding`, and `integrality_gap`;
- preserves unsupported LP metadata in audit mode without verifying it;
- normalized JSON uses stable sorted keys and reduced rational strings.

Residual note: `integer_optimum` is optional. A certificate without it can prove
"this STT has this cost" but not "this STT is optimal." That distinction should
stay visible in downstream reporting.

### 6. CLI

Status: acceptable for v0.

Checked behavior:

- `check` prints `PASS` and exits 0 for valid certificates;
- failures print `FAIL` and exit 1;
- `enumerate` reports STT count and exact integer optimum when weights exist;
- `enumerate-topology` accepts either a bare topology object or a certificate
  wrapper;
- documented examples run.

### 7. Tests

Status: materially improved and now discoverable from the required command.

Coverage now includes:

- rational normalization and malformed rational rejection;
- invalid topology cases, non-contiguous labels, path/star/edge-diameter labels,
  and `n=1`/`n=2`;
- STT singleton inference and unreached component rejection;
- enumeration counts, optimum computation, and safety cap behavior;
- certificate cost mismatch, missing mode, proof-mode LP rejection, audit-mode
  unsupported metadata preservation;
- CLI pass/fail exit codes and subcommand-local `--max-enumeration`.

Remaining useful tests:

- explicit `depth_base: 0` certificate cost check;
- `stt_parent` mismatch rejection;
- `cost.vertex_depths` mismatch rejection;
- proof-mode rejection of `root_rounding` and `integrality_gap` separately;
- normalization stability snapshot for one fixture.

## Commands Run

```text
python -m unittest discover -v
```

Result: passed, 18 tests.

```text
python -m scripts.stt_checker.cli check examples/stt/path_4_proof.json
```

Result: `PASS examples/stt/path_4_proof.json: weighted_cost=2`

```text
python -m scripts.stt_checker.cli check examples/stt/star_4_proof.json
```

Result: `PASS examples/stt/star_4_proof.json: weighted_cost=7/4`

```text
python -m scripts.stt_checker.cli check examples/stt/edge_diameter3_checker_only_7.json
```

Result: `PASS examples/stt/edge_diameter3_checker_only_7.json: weighted_cost=48/23`

```text
python -m scripts.stt_checker.cli check examples/stt/skz_long_star_7_stt_optimum.json
```

Result: `PASS examples/stt/skz_long_star_7_stt_optimum.json: weighted_cost=53/23`

Additional documented examples checked:

```text
python -m scripts.stt_checker.cli check examples/stt/path_4_proof.json --normalized-json
python -m scripts.stt_checker.cli enumerate examples/stt/edge_diameter3_checker_only_7.json
python -m scripts.stt_checker.cli enumerate-topology examples/stt/path_4_proof.json
```

All exited 0.

## Merge Readiness

Merge-ready for the v0 exact combinatorial checker scaffold, with the explicit
qualification that LP fields remain unsupported and unverified outside audit
metadata preservation. Do not present this as a Golinsky LP checker.
