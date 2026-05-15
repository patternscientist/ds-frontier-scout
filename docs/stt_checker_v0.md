# STT Checker Scaffold v0

This document describes the first trusted checker scaffold for static search
trees on trees (STTs). It is intentionally narrower than the LP certificate
schema: v0 checks exact combinatorial STTs, exact costs, topology labels, and
small complete enumerations. It does not check Golinsky LP feasibility.

## Supported Certificate Subset

The checker accepts JSON certificates with:

- `schema_version: "stt-cert-v0"`;
- `mode: "proof"` or `mode: "audit"`;
- a base-tree `topology`;
- `vertex_frequency` weights using exact rationals;
- an `stt.component_roots` recursive root map;
- an optional `cost` block with `depth_base`, `vertex_depths`, and
  `weighted_cost`;
- an optional `integer_optimum` block whose `certificate_type` is
  `checker_enumerates_all_stts`.

In proof mode, any `lp_solution`, `root_rounding`, or `integrality_gap` field
is rejected. In audit mode, these fields are preserved as unsupported metadata
but are not verified.

## Exact Rationals

Rationals may be written as:

```json
"0"
"3"
"-2/5"
"10/23"
{"num": 10, "den": 23}
```

JSON integers are also accepted. JSON floats and decimal strings such as
`0.5` are rejected. Normalized output uses reduced rational strings, with
integers printed without `/1`.

## Topology Format

```json
{
  "topology": {
    "n": 4,
    "vertices": [0, 1, 2, 3],
    "edges": [[0, 1], [1, 2], [2, 3]],
    "declared_subclass_labels": ["path", "edge-diameter-2"]
  }
}
```

The checker validates that edges are unordered pairs of distinct valid
vertices, rejects duplicate edges, and checks that the graph is a connected
tree with `n - 1` edges.

Derived labels in v0 are:

- `path`, when maximum degree is at most 2;
- `star`, when some vertex is adjacent to every other vertex;
- `edge-diameter-k`, where `k` is the maximum line-graph distance between
  two base-tree edges. A one-vertex tree and a one-edge tree have
  `edge-diameter-0`.

The `almost-star` label is advisory and unsupported for now. If declared, it
does not prove anything and is not checked.

## STT Format

The supported STT representation is the flat recursive root map:

```json
{
  "stt": {
    "component_roots": [
      {"component": [0, 1, 2, 3], "root": 1},
      {"component": [2, 3], "root": 2}
    ]
  }
}
```

Validation starts at the full vertex set. For each connected component, the
checker removes the declared root and recurses on the connected components
left behind. Singleton components may be omitted and are inferred. Every
non-singleton recursive component must have exactly one root entry, and every
declared component must be reached by the recursion.

The checker derives:

- the STT parent map;
- vertex depths under `depth_base` 0 or 1;
- a normalized complete recursive component list, including inferred
  singletons.

## Cost Checking

Only `weights.type: "vertex_frequency"` is supported. Each topology vertex must
have one nonnegative rational weight. If `normalization` is `sum_1`, weights
must sum exactly to 1.

The weighted cost is recomputed exactly:

```text
sum_v weight[v] * depth[v]
```

If `cost.weighted_cost` or `cost.vertex_depths` is supplied, it must match the
checker-derived value.

## Enumeration

For small topologies, v0 recursively enumerates every valid STT. The safety cap
defaults to 100,000 and can be changed from the CLI with `--max-enumeration`.

Proof-mode integer optima are currently supported only through:

```json
{
  "integer_optimum": {
    "certificate_type": "checker_enumerates_all_stts",
    "value": "48/23",
    "stt_count": 807
  }
}
```

The checker recomputes the complete enumeration and verifies the exact optimum
and, if supplied, the STT count.

## CLI Examples

From the repository root:

```sh
python -m scripts.stt_checker.cli check examples/stt/long_star_7.json
python -m scripts.stt_checker.cli check examples/stt/path_4_proof.json --normalized-json
python -m scripts.stt_checker.cli enumerate examples/stt/long_star_7.json
```

To enumerate a standalone topology JSON object:

```sh
python -m scripts.stt_checker.cli enumerate-topology path/to/topology.json
```

The CLI prints `PASS` on valid inputs, `FAIL` on invalid inputs, and exits
nonzero on failure.

## Unsupported LP Fields

The following fields are deliberately unsupported in proof mode:

- `lp_solution`;
- `root_rounding`;
- `integrality_gap`.

No `relaxation_version` is supported yet. This checker does not implement
Golinsky LP constraints, does not infer LP variable domains, and does not claim
to reproduce Sadeh-Kaplan-Zwick LP results.

## Known Limitations

- Enumeration is exponential and intended only for small topologies.
- The `edge-diameter-k` label follows the line-graph distance convention from
  the pilot target, not ordinary vertex-tree diameter.
- `almost-star` is not formalized.
- Only vertex-frequency objectives are supported.
- There is no canonical unlabeled tree isomorphism support.
- No LP, SAT, SMT, or dual-certificate backend exists in v0.

## Next Steps

- Add a versioned machine-readable LP relaxation only after variable domains
  and constraints are specified.
- Add complete-enumeration import or exact dual certificates for larger
  integer optimality proofs.
- Add topology generation up to small `n` for edge-diameter subclass audits.
- Formalize the exact `almost-star` convention before using that label in
  proof mode.
