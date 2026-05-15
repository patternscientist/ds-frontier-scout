# STT LP Feasibility Checker v0

This document describes the proof-mode feasibility checker for
`golinsky_stt_lp_v0`.

## Supported Relaxation

Supported exactly:

- `relaxation: "golinsky_stt_lp"`
- `relaxation_version: "golinsky_stt_lp_v0"`
- `schema_version: "stt-lp-cert-v0"`
- `mode: "proof"`

The checker implements the vanilla `X,Z,D` primal feasibility constraints from
`reports/stt_lp_spec_golinsky_v0.md`. That report is authoritative for the
formulas and indexing conventions.

## Certificate Format

LP certificates are separate from combinatorial STT certificates:

```json
{
  "schema_version": "stt-lp-cert-v0",
  "certificate_id": "example-path-4-proof-induced-lp",
  "mode": "proof",
  "relaxation": "golinsky_stt_lp",
  "relaxation_version": "golinsky_stt_lp_v0",
  "topology": {
    "n": 4,
    "vertices": [0, 1, 2, 3],
    "edges": [[0, 1], [1, 2], [2, 3]],
    "declared_subclass_labels": ["path", "edge-diameter-2"]
  },
  "lp_solution": {
    "variables": {
      "D": [{"i": 0, "value": "1"}],
      "X": [{"i": 0, "j": 1, "value": "0"}],
      "Z": [{"k": 1, "i": 0, "j": 2, "value": "1"}]
    }
  },
  "objective": {
    "frequency": {"0": "1/4", "1": "1/4", "2": "1/4", "3": "1/4"},
    "value": "1"
  }
}
```

The displayed variable arrays are abbreviated. Proof mode requires every
defined variable exactly once. In proof mode, `lp_solution` may contain only
the `variables` object; unsupported nested fields are rejected instead of
being ignored.

## Variable Keys

`D` entries use:

```json
{"i": 0, "value": "1"}
```

`X` entries use ordered pairs with `i != j`:

```json
{"i": 0, "j": 1, "value": "0"}
```

`Z` entries use strict base-tree path interior vertices and normalized
endpoints `i < j`:

```json
{"k": 1, "i": 0, "j": 2, "value": "1"}
```

There is no `Z` variable for adjacent endpoints, no endpoint `Z_iij`, and no
`X_ii`.

All values are exact rationals accepted by `scripts/stt_checker/rationals.py`:
integers, strings like `"3/5"`, or objects like `{"num": 3, "den": 5}`.
Floats and decimal strings are rejected.

## Checked

The checker validates:

- topology with the existing `TreeTopology` checker;
- exact dense domains for `D`, ordered `X`, and strict-interior `Z`;
- duplicate, missing, and unknown variable rejection;
- nonnegativity of all `D`, `X`, and `Z`;
- ancestry constraints;
- loose-LCA constraints;
- depth constraints;
- optional objective recomputation as `sum_i f_i D_i`.

On failure, the CLI reports constraint family, indices, left-hand side,
right-hand side, sense, and exact slack for representative violations.

## Not Checked

This v0 does not implement:

- LP solving;
- root rounding;
- integrality-gap checking;
- lower-envelope or projection testing;
- exact dual certificates;
- optional LP variants such as no-`Z`, refined-`Z`, exact-depth, exact-ancestry,
  path-monotonicity, ancestry-transitivity, LCA-separation, or upper-bound
  constraints.

Unsupported `root_rounding` and `integrality_gap` fields are rejected in proof
mode.

## CLI

From the repository root:

```sh
python -m scripts.stt_checker.cli check-lp examples/stt_lp/path_4_stt_induced_lp.json
python -m scripts.stt_checker.cli check-lp examples/stt_lp/star_4_stt_induced_lp.json --verbose
python -m scripts.stt_checker.cli check-lp examples/stt_lp/path_4_stt_induced_lp.json --normalized-json
```

The command prints `PASS` on valid certificates and exits nonzero on invalid
certificates.

## Depth Convention

The LP variable `D_i` is strict-ancestor depth. The combinatorial checker's
default search depth is root-depth-1, so for an STT-induced point:

```text
checker_search_depth(i) = D_i + 1
```

For normalized frequencies, the base-1 search cost equals:

```text
1 + sum_i f_i D_i
```

For unnormalized weights, add `sum_i f_i` instead of `1`.

## Known Limitations

The checker only replays a supplied rational primal point. A passing LP
certificate says the point satisfies the specified inequalities exactly; it
does not prove optimality, non-integrality, a rounding guarantee, or any theorem
about the depth projection.
