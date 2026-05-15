# STT LP Certificate Schema

Date: 2026-05-15

Scope: minimal implementation-ready certificate/checker schema for `search_trees_on_trees_lp`. The goal is to support exact finite witnesses for STT enumeration, Golinsky-style LP solutions, root-rounding behavior, and integrality-gap examples before writing a checker.

## Design Principles

- Use JSON or YAML with the same logical fields; JSON is preferred for checker input.
- Every numeric value in a certificate is an exact rational, not a float.
- A certificate should be self-contained: topology, query weights, candidate STT/LP solution, objective value, and claimed property all live in one file.
- The checker should verify claims by recomputation from primitive fields, not by trusting derived costs.
- Labels are metadata unless the checker can derive them from topology.
- Include a `schema_version` and a checker-supported `relaxation_version` for every LP certificate. The name `golinsky_stt_lp` alone is not precise enough to identify constraints.

## Checker-Blocking Clarifications

The following items must be fixed before implementing a proof-mode checker:

- For the first intended LP relaxation, `reports/stt_lp_spec_golinsky_v0.md` now fixes the source-backed variable domains and constraint set under `relaxation_version: "golinsky_stt_lp_v0"`. A proof-mode checker still must implement that spec before accepting LP certificates.
- LP variable domains must be explicit for any selected relaxation: which ordered/unordered index tuples exist for `X`, `Z`, and `D`, which variables are symmetric, and which absent variables default to zero. For `golinsky_stt_lp_v0`, proof-mode certificates should be dense and missing defined variables should fail closed.
- LP constraints must be referenced by a versioned, machine-implemented constraint set. Free-text "Golinsky-style" constraints are not checkable; use `golinsky_stt_lp_v0` only for the vanilla Sadeh-Kaplan-Zwick/Golinsky `X,Z,D` LP.
- Root-rounding scores must name a checker-known formula or include enough primitive data for recomputation; a list of candidate scores is not a proof by itself.
- Enumeration digests are audit metadata unless the checker either enumerates all STTs itself below a configured threshold or verifies a complete supplied enumeration list.
- `almost-star` remains advisory until the exact Sadeh-Kaplan-Zwick convention is verified.
- Depth-projection claims for `golinsky_stt_lp_v0` must account for the source LP's `D_i >= sum_j X_ji` inequalities: compare lower envelopes, or compare against `conv(STT LP-depth vectors) + R_{\ge 0}^n`, not literal equality to the bounded STT depth hull.

## Rational Format

Represent every rational as either:

```json
{"num": 95, "den": 93}
```

or, for compact human-authored YAML only:

```yaml
"95/93"
```

Checker normalization requirements:

- denominator is positive;
- numerator and denominator are integers;
- fraction is reduced after parsing;
- integer `k` is accepted as `{"num": k, "den": 1}` only if the parser records that coercion.

## Base Tree Topology

```json
{
  "topology": {
    "n": 7,
    "vertices": [0, 1, 2, 3, 4, 5, 6],
    "edges": [[0, 1], [1, 2], [2, 3], [3, 4], [2, 5], [5, 6]],
    "root_label": null,
    "subclass_labels": ["edge-diameter-3"],
    "canonical_label": "optional-nauty-or-todo"
  }
}
```

Validation:

- `vertices` are exactly `0..n-1`;
- `edges` are unordered pairs of distinct vertices;
- there are `n-1` edges;
- the graph is connected and acyclic;
- `canonical_label` is advisory unless the checker has canonicalization enabled.

## Subclass Labels

Allowed labels:

- `path`: maximum degree at most 2.
- `star`: one center adjacent to all other vertices.
- `almost-star`: a tree obtained from a star by subdividing exactly one or more leaf edges once; use only after the repo fixes the exact Sadeh-Kaplan-Zwick convention.
- `edge-diameter-3`: maximum distance between edges is at most 3 under the line-graph distance convention.
- `edge-diameter-4`
- `edge-diameter-5-plus`
- `unknown`

The checker should compute `path`, `star`, and edge-diameter labels directly. `almost-star` may remain a declared label until its exact convention is verified.

## STT / Search Strategy

A static STT is a recursive root choice for each connected induced component of the base tree.

Minimal representation:

```json
{
  "stt": {
    "component_roots": [
      {"component": [0, 1, 2, 3, 4, 5, 6], "root": 2},
      {"component": [0, 1], "root": 1},
      {"component": [0], "root": 0},
      {"component": [3, 4], "root": 3},
      {"component": [4], "root": 4},
      {"component": [5, 6], "root": 5},
      {"component": [6], "root": 6}
    ]
  }
}
```

Derived representation accepted for convenience:

```json
{
  "stt_parent": [1, 2, null, 2, 2, 4, 4]
}
```

Validation:

- each listed `component` induces a connected subtree of the base tree;
- the first component is all vertices;
- removing the chosen `root` partitions the component into child components exactly matching the next recursive components;
- every vertex appears as a root exactly once;
- derived STT parent/depth arrays agree with the recursive representation.

## Query Weights

```json
{
  "weights": {
    "type": "vertex_frequency",
    "values": {
      "0": {"num": 3, "den": 23},
      "1": {"num": 2, "den": 23},
      "2": {"num": 0, "den": 1},
      "3": {"num": 2, "den": 23},
      "4": {"num": 3, "den": 23},
      "5": {"num": 3, "den": 23},
      "6": {"num": 10, "den": 23}
    },
    "normalization": "sum_1"
  }
}
```

Validation:

- every vertex has one nonnegative rational weight;
- if `normalization` is `sum_1`, weights sum to 1;
- if `normalization` is `unnormalized`, costs are checked against the unnormalized sum.

## Cost Format

Depth convention must be explicit:

```json
{
  "cost": {
    "depth_base": 1,
    "vertex_depths": {
      "0": 3,
      "1": 2,
      "2": 1,
      "3": 2,
      "4": 3,
      "5": 2,
      "6": 3
    },
    "weighted_cost": {"num": 62, "den": 23}
  }
}
```

Validation:

- `depth_base` is either 0 or 1;
- depths are recomputed from the STT;
- weighted cost equals `sum_v weight[v] * depth[v]`.

## LP Solution / Counterexample Format

```json
{
  "lp_solution": {
    "relaxation": "golinsky_stt_lp",
    "relaxation_version": "golinsky_stt_lp_v0",
    "variable_domains": {
      "X": "ordered_pairs_i_j_i_ne_j",
      "Z": "triples_k_i_j_with_i_lt_j_and_k_strictly_between_i_j",
      "D": "vertices",
      "encoding": "dense_required_in_proof_mode"
    },
    "variables": {
      "X": [{"i": 0, "j": 1, "value": "1/2"}],
      "Z": [{"i": 0, "j": 1, "k": 2, "value": "1/3"}],
      "D": [{"i": 0, "value": "5/3"}]
    },
    "objective": {
      "weights_ref": "weights",
      "value": "95/93"
    },
    "claim": "feasible_fractional_better_than_any_stt"
  }
}
```

Validation:

- `relaxation_version` is one of the checker-supported exact constraint sets;
- all required LP variables for the declared relaxation and variable domains are present, or absent variables have a schema-level default of 0 for that exact variable family;
- every variable is rational and in its allowed range;
- all LP constraints are checked exactly;
- objective value is recomputed from `D` and weights;
- if the claim compares against STTs, the certificate must also include either a complete STT enumeration digest or a separate optimality certificate.

## Root-Rounding Certificate Format

```json
{
  "root_rounding": {
    "lp_solution_ref": "lp_solution",
    "tie_break": {
      "rule": "lexicographic_min_vertex"
    },
    "rounding_rule": {
      "id": "TODO-root-rounding-formula",
      "version": "TODO"
    },
    "rounding_steps": [
      {
        "component": [0, 1, 2, 3, 4, 5, 6],
        "candidate_root_scores": [
          {"root": 2, "score": "7/5"},
          {"root": 4, "score": "7/5"}
        ],
        "chosen_root": 2
      }
    ],
    "rounded_stt_ref": "stt",
    "rounded_cost": "263/190"
  }
}
```

Validation:

- each rounding step refers to a connected current component;
- candidate root scores match the declared machine-readable root-rounding rule and the referenced LP solution;
- tie-breaking is deterministic and replayable;
- the produced STT validates under the STT schema;
- rounded cost is recomputed exactly.

## Integrality-Gap Witness Format

```json
{
  "integrality_gap": {
    "lp_solution_ref": "lp_solution",
    "integer_optimum": {
      "value": "1",
      "certificate_type": "complete_enumeration",
      "stt_count": 144,
      "sha256_of_enumeration": "TODO"
    },
    "lp_value": "93/95",
    "gap_ratio": "95/93",
    "minimization": true
  }
}
```

Validation:

- `gap_ratio = integer_optimum.value / lp_value` for minimization;
- `lp_value` equals the LP objective;
- integer optimum is justified by one of:
  - `complete_enumeration`: checker enumerates all STTs for `n` below a configured threshold;
  - `dual_bound`: certificate includes exact dual variables proving the lower bound;
  - `external_verified_digest`: accepted only in audit mode, not proof mode.

## Validation Checks

Minimum checker phases:

1. Parse and normalize rationals.
2. Validate base tree topology.
3. Derive subclass labels and compare to declared labels.
4. Validate query weights.
5. Validate STT recursion and compute depths.
6. Recompute exact STT cost.
7. Validate LP variable domains and constraints.
8. Recompute LP objective.
9. Replay root rounding, including tie-breaking.
10. Verify integrality-gap arithmetic.
11. Emit a canonical normalized certificate with stable key order and reduced rationals.

Recommended rejection modes:

- `invalid_topology`
- `invalid_stt_recursion`
- `invalid_rational`
- `constraint_violation`
- `objective_mismatch`
- `rounding_mismatch`
- `gap_arithmetic_mismatch`
- `unverified_external_digest`

## Lean Verification Path

This schema can support Lean later by keeping the trusted core small:

- define finite trees as vertex sets plus edge relation with proof of connected acyclic structure;
- define STTs inductively as recursive root decompositions over connected subtrees;
- define rational arithmetic using Lean's `Rat`;
- formalize depth and weighted cost as finite sums;
- formalize Golinsky LP constraints as predicates over finite maps of rational variables;
- prove checker soundness: if Lean accepts a certificate, then the claimed LP feasibility, STT cost, or gap arithmetic holds;
- keep enumeration outside Lean initially, but import enumeration results as lists plus a proof/check that every listed recursive decomposition is valid and complete for small `n`.

First Lean target: prove that a single certificate's rounded STT cost and LP objective arithmetic are correct. Full polytope completeness can wait.
