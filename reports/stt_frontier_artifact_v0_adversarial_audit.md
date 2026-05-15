# STT Frontier Artifact v0 Adversarial Audit

Date: 2026-05-15

Scope: adversarial audit of the `stt-frontier-artifact-v0` branch's topology
generation and reproducible checker-only frontier artifact. This audit covers
topology generation, AHU-style canonicalization, edge-diameter labels, STT
enumeration, exact checker-only optima, output files, docs, and tests.

This audit does not implement LP constraints, does not infer Golinsky LP
variables, and does not claim any LP theorem.

## Executive Status

The artifact is merge-ready for its stated v0 purpose: a reproducible
checker-only small-instance frontier summary for unlabeled trees with `n <= 7`.

No blocking mathematical-correctness or reproducibility bugs were found. The
artifact is not LP evidence. It correctly says that no Golinsky LP constraints,
LP variable domains, root rounding, or integrality-gap claims are checked.

This audit added tests for previously under-tested risks:

- labeled Prufer generation covers Cayley counts for `n <= 5`;
- unlabeled topology counts match the requested sequence through `n = 7`:
  `1, 1, 1, 2, 3, 6, 11`;
- canonical forms agree under one-center and two-center relabelings;
- canonical forms separate a path and star on four vertices;
- complete STT counts match an independent count-only recurrence for all
  generated unlabeled topologies through `n = 6`;
- frontier artifact cap behavior records incomplete enumeration without
  publishing optima;
- frontier artifact JSON, CSV, and Markdown outputs are deterministic across
  reruns in temporary output directories.

## Findings

### No Blocking Finding: topology generation is correct for v0 range

Prufer decoding uses the standard degree-and-smallest-leaf algorithm. Tiny
examples now pin down:

- `n = 1`, empty code -> no edges;
- `n = 2`, empty code -> one edge;
- `[0, 0]` on `n = 4` -> a 4-vertex star centered at `0`;
- `[1, 2]` on `n = 4` -> the path edges
  `[(0, 1), (1, 2), (2, 3)]`.

Labeled generation iterates all codes in `[0, n-1]^(n-2)`, and every decoded
tree is passed through `TreeTopology.from_dict`, so representatives have
vertices `0..n-1`, exactly `n - 1` edges, no duplicate undirected edges, and
connected tree structure. The new Cayley-count test checks that labeled tree
generation produces exactly `n^(n-2)` distinct edge sets for `n <= 5`.

Residual risk: generation above `n = 7` is intentionally refused by
`DEFAULT_MAX_N`. That is appropriate for this artifact but should not be
presented as a scalable unlabeled-tree generator.

### No Blocking Finding: AHU-style deduplication is adequate

The canonicalization finds the center or centers of the tree, computes sorted
rooted subtree strings, and keeps the lexicographically smallest rooted form.
For one-center trees, this is the standard rooted-at-center invariant. For
two-center trees, the multiset of the two center-rooted full-tree forms is
isomorphism invariant; choosing its minimum remains a valid discriminator for
small tree deduplication because equality of a rooted full-tree form gives a
rooted isomorphism and therefore an unrooted isomorphism.

The new tests cover both one-center and two-center relabelings, plus a
non-isomorphic path/star separation case.

Residual risk: this is a small-purpose AHU string, not a general graph
canonical labeling tool. That limitation is already documented.

### No Blocking Finding: edge-diameter labels use the intended convention

The artifact consistently uses line-graph edge distance through
`TreeTopology.diameter_edges`, not ordinary vertex-tree diameter. Boundary
cases are documented and tested:

- a one-vertex tree has `edge-diameter-0`;
- a one-edge tree also has `edge-diameter-0`;
- a 4-vertex path has `edge-diameter-2`;
- a 4-vertex star has `edge-diameter-1`;
- the 7-node long-star fixture has `edge-diameter-3`.

The `n = 2` `edge-diameter-0` convention may surprise readers expecting a
vertex diameter, but it is correct under line-graph diameter: the line graph
has one vertex and diameter zero. I did not change it.

### No Blocking Finding: STT enumeration uses the trusted checker path

`frontier_artifacts.py` computes objective optima through
`integer_optimum_by_enumeration` from `scripts/stt_checker/enumerate_stts.py`.
It does not contain an independent ad hoc STT enumerator.

The audit added a count-only recurrence test:

```text
count(C) = sum over roots r in C of product over components C_i of C-r count(C_i)
```

That recurrence agrees with `enumerate_stts` for every generated unlabeled
topology through `n = 6`.

Repeated enumeration for uniform and leaf-heavy objectives is guarded:
`frontier_artifacts.py` raises an internal error if the two enumeration counts
differ, so mismatched counts cannot be silently published.

Residual risk: enumeration materializes recursive option lists and is still
exponential. The cap is a correctness boundary for the artifact, not a memory
or scalability proof.

### No Blocking Finding: exact optima are exact rationals and honestly gated

Uniform weights are `Fraction(1, n)` for each vertex. Leaf-heavy weights are
`Fraction(1, number_of_leaves)` on leaves and zero elsewhere, with the
one-vertex tree treated as leaf-supported. Both objectives are normalized to
sum to one exactly.

Optima are stringified exact `Fraction` values only after enumeration completes.
If enumeration exceeds the cap, the artifact leaves both optima as `null`,
sets `enumeration.completed` to `false`, sets `exceeded_cap` to `true`, and
records the cap message. A new smoke test covers this behavior with a low cap.

### No Blocking Finding: output files are machine-readable and deterministic

The JSON file has a stable top-level schema marker:
`stt-frontier-artifact-v0`. JSON output uses sorted keys and indentation.

The CSV is written with Python's `csv.DictWriter`, newline control, and JSON
encoding for the nested edge list field, so commas in edge lists are quoted
properly and the file parses as one logical record per row.

The Markdown report is readable and avoids theorem overclaiming. Its
observations are explicitly scoped to exact checker output and say they do not
imply LP integrality, LP feasibility, or theorem-level claims.

Regenerating with

```text
python -m scripts.stt_checker.frontier_artifacts --max-n 7 --max-enumeration 100000
```

produced no diffs in the checked-in JSON, CSV, or Markdown artifact files.
The new deterministic-rerun test also compares two temporary output trees.

### No Blocking Finding: docs and README describe the artifact accurately

`docs/stt_checker_v0.md` documents the frontier generation command, the output
paths, the Prufer/AHU/checker-enumeration method, and the unsupported LP
fields. `README.md` points to the checker docs and describes the artifact as a
small-topology frontier artifact with companion machine-readable files.

No scouting scores, candidate rankings, or candidate reports were changed.

## Skeptical Audit

Why might this not actually be correct?

- The canonicalizer is custom. The known unlabeled counts through `n = 7`,
  relabeling tests, and path/star separation reduce this risk for v0, but a
  stronger future audit could compare against a separate tree-isomorphism
  implementation.
- The enumerator and the independent recurrence both rely on
  `connected_components_after_removing`; a bug there could affect both. The
  topology validator and fixture counts reduce the risk, but this is still the
  shared trusted primitive.
- The artifact records one representative per unlabeled shape. It should not be
  used to infer labeled-frequency statistics.

Why might this be too saturated or misleading?

- The artifact is infrastructure, not a frontier theorem. Its value is as a
  reproducible small-instance map for later theorem and LP work.
- Edge-diameter-3 records should not be promoted as evidence for projection
  integrality until a versioned LP checker exists.

Why might it be impossible to evaluate automatically?

- Integer STT enumeration is automatic only while the cap is feasible. Larger
  instances will need exact dual certificates, complete imported enumerations,
  or a future LP/SAT/SMT backend.

What would falsify interest in the artifact?

- A mismatch with known unlabeled tree counts in the supported range;
- an isomorphism collision that merges non-isomorphic shapes;
- a repeated-run diff in generated files without an intentional schema change;
- a discovered convention mismatch between STT recursion here and primary STT
  definitions;
- any report wording that treats checker-only integer enumeration as LP proof.

Primary sources or references still needed before theorem promotion:

- primary STT/search-trees-on-trees definitions for the recursive model;
- the exact Golinsky LP variable domains and constraints, by version;
- the exact Sadeh-Kaplan-Zwick long-star or almost-star convention before using
  that label in proof-mode claims.

## Patches Made

- Strengthened `tests/test_stt_checker.py` for Prufer validation, labeled and
  unlabeled topology generation, canonicalization, independent STT count
  recurrence, cap behavior, and deterministic artifact reruns.
- Added this audit report.

No code changes were needed in `scripts/stt_checker/`, and no generated data
changes were produced by rerunning the frontier artifact command.

## Commands Run

```text
python -m unittest discover -v
```

Result: passed, 28 tests.

```text
python -m scripts.stt_checker.cli check examples/stt/path_4_proof.json
```

Result: `PASS examples/stt/path_4_proof.json: weighted_cost=2`

```text
python -m scripts.stt_checker.cli check examples/stt/star_4_proof.json
```

Result: `PASS examples/stt/star_4_proof.json: weighted_cost=7/4`

```text
python -m scripts.stt_checker.cli check examples/stt/long_star_7.json
```

Result: `PASS examples/stt/long_star_7.json: weighted_cost=48/23`

```text
python -m scripts.stt_checker.frontier_artifacts --max-n 7 --max-enumeration 100000
```

Result: regenerated
`data/stt_frontier/topologies_n_leq_7.json`,
`data/stt_frontier/topology_summary_n_leq_7.csv`, and
`reports/stt_v0_frontier_artifact.md` with no diff.
