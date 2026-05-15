# STT LP Pilot Plan

Date: 2026-05-15

## Pilot Objective

Start a one-week `search_trees_on_trees_lp` pilot that tests whether this repository can move from scouting into proof/certificate work. The pilot should not try to solve general optimal STT computation. It should build a trustworthy exact checker scaffold, reproduce at least one known small STT/LP-style artifact, and run a narrow theorem attempt on an edge-diameter-3 subclass target.

## Exact First Theorem Target

Target statement:

For every base tree `U` whose edge-diameter is at most 3, determine whether the depth-space projection of `golinsky_stt_lp_v0` has the same lower envelope as the convex hull of LP-depth vectors of valid static search trees on `U`; equivalently, determine whether the projection equals `conv(STT LP-depth vectors) + R_{\ge 0}^n`.

Accepted pilot outcomes:

- a proof of lower-envelope projection integrality for the edge-diameter-3 class;
- a minimal exact rational counterexample with topology, weights/objective, LP solution, and complete STT enumeration or dual certificate;
- a sharper reduction showing that the target must be narrowed, for example to a verified `almost-star` convention.

Baselines:

- paths are ordinary optimal BST baselines, not open exact-optimization cases;
- stars are LP-integral baselines, not open exact-optimization cases;
- `almost-star` is advisory until its exact convention is verified.

## Exact First Computational Target

Build a proof-mode checker scaffold for STT certificates before implementing guessed LP constraints.

Minimum first artifact:

- parse one JSON certificate;
- validate the base tree topology;
- validate weights and exact rationals;
- validate a recursive STT;
- recompute depths and weighted cost exactly;
- derive `path`, `star`, and edge-diameter subclass labels;
- enumerate all STTs for small `n` and verify the best integer cost against the supplied STT;
- emit a normalized certificate with stable key order and reduced rationals.

The first reproducibility target is a small Sadeh-Kaplan-Zwick-style instance such as the 7-node long-star topology and frequency vector recorded in the STT frontier. LP feasibility can stay in audit/unsupported mode until the relaxation details below are fixed.

## Certificate / Checker Requirements

The checker must be exact and replayable:

- use exact rational arithmetic only;
- reject floats in proof mode;
- recompute every derived value from primitive fields;
- separate proof mode from audit mode;
- never treat a digest as a proof unless the checker can independently enumerate the object behind it;
- make unsupported LP relaxation versions fail closed.

Checker-blocking clarifications from `reports/stt_lp_certificate_schema.md`:

- add a checker version and exact `relaxation_version`;
- specify LP variable domains for `X`, `Z`, and `D`, including index ordering, symmetry, and absent-variable defaults;
- implement a versioned machine-readable LP constraint set;
- define root-rounding score formulas by checker-known IDs, not free text;
- require complete enumeration, a supplied complete list, or exact dual certificates in proof mode;
- keep `almost-star` advisory until its exact convention is verified.

## Minimum Viable Data Formats

Use JSON as the checker input format. YAML can remain human-authored source material, but the first checker should normalize into JSON.

Required top-level fields for the first scaffold:

```json
{
  "schema_version": "stt-cert-v0",
  "certificate_id": "example-long-star-7",
  "mode": "proof",
  "topology": {
    "n": 7,
    "vertices": [0, 1, 2, 3, 4, 5, 6],
    "edges": [[0, 1], [1, 2], [2, 3], [3, 4], [2, 5], [5, 6]],
    "declared_subclass_labels": ["edge-diameter-3"]
  },
  "weights": {
    "type": "vertex_frequency",
    "normalization": "sum_1",
    "values": {
      "0": "3/23",
      "1": "2/23",
      "2": "0",
      "3": "2/23",
      "4": "3/23",
      "5": "3/23",
      "6": "10/23"
    }
  },
  "stt": {
    "component_roots": [
      {"component": [0, 1, 2, 3, 4, 5, 6], "root": 2}
    ]
  },
  "cost": {
    "depth_base": 1,
    "weighted_cost": "TODO"
  },
  "integer_optimum": {
    "certificate_type": "checker_enumerates_all_stts",
    "value": "TODO"
  }
}
```

Optional fields for later phases:

- `lp_solution`, accepted only when `relaxation_version` is supported;
- `root_rounding`, accepted only when the rounding formula ID is supported;
- `integrality_gap`, accepted only when both LP and integer certificates are proof-mode verifiable.

## First Blind No-Internet Prompt

Use this prompt before showing the model the frontier document or literature notes:

```text
You are studying the following self-contained problem. Do not use the internet or any literature context.

Let U be an undirected tree whose vertices are searchable items. A search tree on U is defined recursively: choose a root vertex r; remove r from U; for each connected component of U - r, attach as a child of r a search tree recursively built on that component. Thus the search tree has the same vertices as U, but a different rooted tree structure. The depth of the root is 1.

Each valid search tree T has a depth vector d_T, where d_T(v) is the depth of vertex v. Given nonnegative weights w_v, the static cost is sum_v w_v d_T(v).

Paths and stars are baseline sanity checks, not the target: paths should behave like ordinary optimal binary search trees, and stars should be treated as a simple highly symmetric case.

Focus on base trees whose edge-diameter is at most 3, meaning that in the line graph of U, every two edges have distance at most 3. Consider linear relaxations whose variables are intended to encode ancestry, lowest-common-ancestor, and depth information for recursive search trees.

Main target, corrected for the vanilla LP's depth inequalities: prove or refute that every feasible LP-depth vector dominates a convex combination of valid recursive-search-tree LP-depth vectors, equivalently that the projected feasible region is the STT LP-depth hull plus the nonnegative orthant. If the target is too broad, isolate the smallest precise subclass where the statement can be proved, or construct a concrete lower-envelope counterexample with rational weights/objective.

Try dynamic programming, exchange arguments, root-choice characterizations, or valid inequalities. State every definition you use, distinguish full LP integrality from depth-projection integrality, and list failure modes clearly.
```

## First Codex Implementation Prompt

Use this prompt for the first implementation pass:

```text
Implement the first STT LP certificate/checker scaffold in this repository.

Read AGENTS.md and reports/stt_lp_certificate_schema.md. Do not fetch the internet and do not implement guessed Golinsky LP constraints. Treat LP proof-mode checking as unsupported until relaxation_version, variable domains for X/Z/D, and the exact constraint set are specified.

Create a small Python checker package and tests that support:

1. exact rational parsing and normalization for integers, "a/b" strings, and {"num": a, "den": b} objects, rejecting floats in proof mode;
2. base-tree validation: vertices are 0..n-1, edges are unordered distinct pairs, the graph is connected and acyclic;
3. computed subclass labels for path, star, and edge-diameter-k buckets using line-graph distance;
4. weight validation for nonnegative vertex weights and optional sum_1 normalization;
5. recursive STT validation from component_roots, including connected induced components, root removal partition checks, and every vertex used exactly once as a root;
6. derived parent/depth computation with depth_base 0 or 1;
7. exact weighted-cost recomputation;
8. complete STT enumeration for small n, with a configurable safety threshold;
9. proof-mode integer optimum checking by checker enumeration for small n;
10. canonical normalized JSON output with stable key order and reduced rationals.

Add fixture certificates for a path, a star, and one 7-node STT topology using the frequency vector [3,2,0,2,3,3,10]/23 from candidate_topics/search_trees_on_trees_lp/frontier.md. Include tests for invalid topology, invalid STT recursion, rational normalization, cost mismatch, and unsupported lp_solution rejection.

Keep the implementation conservative and documented. Do not rewrite candidate folders. Do not claim LP feasibility checking is complete until the checker-blocking clarifications are resolved.
```

## First OpenEvolve-Style Evaluator Idea

After the scaffold exists, define an evaluator that scores candidate finite certificates and conjectures by exact checker output:

- generate tree topologies up to a small `n`;
- filter by computed edge-diameter;
- enumerate all recursive STTs and depth vectors;
- sample or enumerate rational objectives with small denominators;
- call an LP backend only after a supported `relaxation_version` exists;
- reward candidates that either prove integer optimum by enumeration or find a fractional depth vector separated from the integer hull;
- penalize certificates that rely on advisory labels, digests, floats, or unsupported LP fields.

Until LP constraints are versioned, the evaluator should search only integer STT structure, depth-vector hull data, and certificate-shape robustness.

## One-Week Success Criteria

Success after one week means:

- the checker scaffold runs in proof mode on path, star, and one nontrivial 7-node fixture;
- exact rational costs and complete small-`n` STT enumeration are tested;
- `reports/stt_lp_certificate_schema.md` has no unresolved ambiguity for the implemented non-LP phases;
- the first blind theorem attempt has been run and summarized;
- the next LP-blocking clarification is isolated as a short checklist, not a vague TODO.

Stretch success:

- a verified certificate reproduces one known integer optimum or root-rounded STT cost;
- edge-diameter-3 topologies up to a small `n` are enumerated and summarized;
- the code can ingest a future LP certificate while safely rejecting unsupported relaxations.

## Failure / Pivot Signals

Pivot or pause if any of these happen:

- the STT recursion or enumeration model in the checker conflicts with the primary STT definitions;
- the Sadeh-Kaplan-Zwick artifacts cannot be reproduced or mapped into the schema after reasonable source extraction;
- `almost-star` or edge-diameter-3 conventions remain too ambiguous to target safely;
- exact enumeration explodes before producing useful small certificates and no fallback dual/cut approach is clear;
- a post-2025 source closes the edge-diameter-3 projection-integrality question or makes the pilot target obsolete;
- the first week produces only literature notes and no runnable checker artifact.
