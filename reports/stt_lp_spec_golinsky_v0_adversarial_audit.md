# STT LP Specification Golinsky v0 Adversarial Audit

Date: 2026-05-15

Audited artifact: `reports/stt_lp_spec_golinsky_v0.md`

Verdict: merge-ready after minor wording fixes.

The spec is implementation-ready for exact rational feasibility checking of
the vanilla Sadeh-Kaplan-Zwick presentation/code version of Golinsky's STT LP.
It should not be described as independently verified against Golinsky's
original thesis until that thesis is obtained.

## Sources Checked

- Yaniv Sadeh, Haim Kaplan, Uri Zwick, "Search Trees on Trees via LP",
  arXiv:2501.17563, https://arxiv.org/abs/2501.17563.
- arXiv e-print/source archive downloaded 2026-05-15 from
  https://arxiv.org/e-print/2501.17563.
- Source files inspected: `section_preliminaries.tex`,
  `section_counter_example.tex`, `section_open_questions.tex`,
  `section_positive_results.tex`, `section_extra_results.tex`,
  `section_code.tex`, `reference.bib`, and
  `STTLP-sage-python3-source/`.
- Code files inspected: `STTLP-LPs.py`, `STTLP-GraphsAndSTT.py`,
  `STTLP-HardcodedValues.py`, and
  `example-logs/graph_7_3_1737401767.txt`.
- Repository context inspected: certificate schema, pilot plan, prior audits,
  frontier notes/sources, all `scripts/stt_checker/*.py`, and
  `docs/stt_checker_v0.md`.

## Findings

### Fixed: depth-projection dominance direction was reversed

The spec correctly says the vanilla LP projection is upward closed because the
source LP uses `D_i >= sum_j X_ji`, but one implementation sentence said to
test whether every feasible projected depth vector is "dominated by" a convex
combination of STT depths. That is backwards.

Correct condition:

```text
pi_D(P_U) = conv(STT LP-depth vectors) + R_{\ge 0}^n
```

Equivalently, every feasible projected LP-depth vector must dominate some
convex combination of STT LP-depth vectors.

Patch:

- Updated `reports/stt_lp_spec_golinsky_v0.md`.
- Updated `reports/stt_pilot_plan.md` so the theorem target and blind prompt
  use lower-envelope / nonnegative-orthant wording instead of literal bounded
  hull equality.

### Fixed: nonnegativity source wording was too blunt

The source paper's prose says the LP variables are relaxed to nonnegative real
values, but the displayed "Bounds" formula explicitly lists `X` and `Z`; `D`
nonnegativity follows from nonnegative `X` plus the depth inequality. The code
adds a nonnegative bound for every primal variable, including `D`.

Patch:

- Updated the spec's nonnegativity source note to distinguish the paper's
  display, the implication for `D`, and the code behavior.

This does not change the checker requirement: include and verify `D_i >= 0`
in v0, because the code path does and it is redundant but harmless.

### Fixed: Golinsky thesis trail needed a false-lead warning

The arXiv `reference.bib` cites Golinsky's Tel Aviv University 2023 master's
thesis without URL or DOI. It also has a commented DOI line near that entry,
`10.22028/D291-26671`, but that DOI is not Golinsky's thesis; it resolves to
Laszlo Kozma's 2016 thesis.

Patch:

- Updated the spec to record this false lead and keep the thesis as an
  unresolved source blocker for direct Golinsky-original claims.

### Fixed: schema/pilot examples used a non-source "long-star" topology

The paper's long star has source edges:

```text
(1,2),(2,3),(3,4),(4,5),(3,6),(6,7)
```

The matching repository 0-indexed edges are:

```text
(0,1),(1,2),(2,3),(3,4),(2,5),(5,6)
```

The schema and pilot examples used a different 7-node edge-diameter-3 topology:

```text
(0,1),(1,2),(2,3),(2,4),(4,5),(4,6)
```

That existing checker fixture is valid as a checker-only topology, but it is
not the Sadeh-Kaplan-Zwick long star. Source-code log
`graph_7_3_1737401767.txt` reports 662 STT vertices for the source topology;
the existing checker fixture reports 807 STTs, confirming the mismatch.

Patch:

- Updated illustrative topology snippets in
  `reports/stt_lp_certificate_schema.md` and `reports/stt_pilot_plan.md`.
- Updated the schema's adjacent STT/depth/cost example to stay internally
  consistent with the corrected source topology.

No checked-in code or fixture certificate was changed.

## Checklist Audit

### 1. Source Trail

Status: acceptable after the Golinsky-thesis warning patch.

The arXiv source archive is real and contains the cited TeX files and
`STTLP-sage-python3-source/` directory. `section_code.tex` says the code is
included in the arXiv source as `STTLP-sage-python3-source.zip`; the downloaded
archive exposes it as a directory after extraction.

The cited code filenames are real:

- `STTLP-LPs.py`
- `STTLP-GraphsAndSTT.py`
- `STTLP-HardcodedValues.py`
- `STTLP-main-and-tests.py`
- `STTLP-BasicUtils.py`
- `main.sage`
- `parse_logs.py`

Golinsky's thesis remains inaccessible from this audit. The spec now
consistently limits its fidelity claim to the Sadeh-Kaplan-Zwick
presentation/code version.

### 2. Variable Families And Indexing

Status: confirmed.

- `D_i` exists for every vertex.
- `X_ij` exists for ordered pairs `i != j`.
- `Z_kij` exists only for strict path-interior `k` and unordered endpoint
  pair `{i,j}`.
- Source code stores `Z` as `(k, i, j)` only when `i < j`.
- `betweenNodes` removes both endpoints from the path, confirming the strict
  interior convention.
- Source labels are 1-indexed; repository labels are 0-indexed.
- Dense proof-mode missing/extra-variable behavior is our checker design
  choice, not a source convention; the spec says this explicitly.

### 3. Constraint Families

Status: confirmed for vanilla `modes_vanilla = []`.

- Nonnegativity: code adds `variable >= 0` for every primal variable. No upper
  bounds are in vanilla mode.
- Ancestry: source/code use
  `X_ij + X_ji + sum_{k in between(i,j)} Z_kij >= 1`; the code emits one
  nonduplicated constraint per `i < j`. Adjacent vertices have an empty `Z`
  sum, so the constraint reduces to `X_ij + X_ji >= 1`.
- Loose LCA: for every defined `Z_kij`, code emits `X_ki - Z_kij >= 0` and
  `X_kj - Z_kij >= 0`.
- Depth: code emits `D_i - sum_{j != i} X_ji >= 0`.
- Optional modes are correctly excluded: `noZVariables`,
  `exactAncestryConstraints`, `exactDepthsConstraints`, `pathMonotonicity`,
  `AncestryTransitivity`, `LCAseparation`, `refinedZ`, and `upperBoundOf1`.

### 4. Objective And Depth Convention

Status: confirmed.

The LP objective is `f . D`, not root-depth-1 checker cost.
`definition_xzd_of_stt`, `remark_depth_off_by_one`, and
`stt_to_XZD_vector` all use `D_i` as strict-ancestor depth / root depth 0.

For normalized frequencies:

```text
checker base-1 search cost = 1 + f . D
```

For unnormalized weights:

```text
checker base-1 search cost = sum_i w_i + w . D
```

### 5. Depth-Space Projection Correction

Status: confirmed and patched.

Literal equality `pi_D(P_U) = conv(STT depths)` cannot hold for the vanilla LP
as a bounded-set statement, because increasing any feasible `D_i` preserves
feasibility. The correct proof target is lower-envelope equality, equivalently
equality to the STT LP-depth hull plus the nonnegative orthant.

### 6. Root Rounding

Status: confirmed.

`definition_rounding_scheme` uses the half-open path condition:

```text
sum_{u : r in [u <-> v)} X_uv >= 1/2
```

where the path includes `u` and excludes `v`. `round_to_STT` matches this by
summing `x_variables[(u,v)]` when `r == u` or `r in betweenNodes(u,v)`.

Future checker data needed:

- full topology and full `X` values;
- current recursive component at each step;
- recomputed admissible-root inequalities;
- chosen root;
- deterministic tie-breaking only if a certificate claims one chosen rounded
  STT rather than the set of all possible roundings.

### 7. Long-Star Smoke Target

Status: source-backed as a target, but no proof fixture should be added yet.

Confirmed source facts:

- topology edges are `(1,2),(2,3),(3,4),(4,5),(3,6),(6,7)`;
- repository 0-indexed edges are `(0,1),(1,2),(2,3),(3,4),(2,5),(5,6)`;
- frequency vector is `[3,2,0,2,3,3,10]/23`;
- LP-depth vector is `[2,2,9/2,2,2,3/2,1/2]`;
- unnormalized fractional LP-depth objective is `59/2`;
- unnormalized best STT LP-depth objective is `30`;
- LP-depth-objective gap is `60/59`.

These three numbers are in the LP-depth-objective convention, not base-1
search-cost convention. With normalized frequencies, the best STT base-1 cost
is `53/23`.

Local checker cross-check for the source topology:

```text
STT count: 662
base-1 optimum: 53/23
```

Do not add a long-star LP proof fixture until full `(X,Z,D)` coordinates are
transcribed from Figure `figure_explicit_counter_example` or from
`MAPPER_INDEX_TO_FULL_VERTEX` and replayed through the exact checker.

### 8. Certificate Schema Consistency

Status: acceptable after example-topology patch.

The schema now agrees with the spec on:

- exact rational values;
- 0-indexed repository labels;
- dense proof-mode domains for `D`, ordered `X`, and strict-interior unordered
  endpoint `Z`;
- lower-envelope / nonnegative-orthant depth-projection claims;
- unsupported LP/root-rounding/integrality-gap proof mode until implemented.

Residual note: root-rounding still has no implemented checker-known ID. The
spec gives enough formula detail to create `golinsky_root_rounding_v0` later,
but this audit did not add unsupported checker semantics.

### 9. Implementation Readiness

Minimal first LP checker task after this audit:

1. Add domain generation for `D`, ordered `X`, and strict-interior unordered
   endpoint `Z` from a 0-indexed topology.
2. Add dense exact rational parsing for `lp_solution.variables`.
3. Reject missing defined variables and reject undefined variables in proof
   mode.
4. Evaluate only primal feasibility for `golinsky_stt_lp_v0` exactly:
   nonnegativity, ancestry, loose-LCA, and depth.
5. Recompute `depth_objective_value = sum_i f_i D_i`.
6. Report violations with constraint family and indices.

Blockers before broader theorem/projection implementation:

- direct Golinsky thesis verification if we want to claim fidelity to the
  original thesis rather than SKZ/code;
- full source-checked long-star `(X,Z,D)` coordinates for a proof fixture;
- exact lower-envelope comparison method, separation oracle, or dual/facet
  certificate format;
- root-rounding replay ID and deterministic tie-breaking policy.

## Commands Run

```text
Invoke-WebRequest -Uri https://arxiv.org/e-print/2501.17563 -OutFile arxiv-2501.17563-src.tar.gz
tar -tf arxiv-2501.17563-src.tar.gz
tar -xzf arxiv-2501.17563-src.tar.gz -C .audit_arxiv_2501_17563
rg ... .audit_arxiv_2501_17563
python -m scripts.stt_checker.cli check examples/stt/edge_diameter3_checker_only_7.json
```

Result for the checked-in `examples/stt/edge_diameter3_checker_only_7.json`: valid checker-only
certificate, but not the source long-star topology.

Additional source-topology check:

```text
@' ... inline source-topology checker call ... '@ | python -
```

Result:

```text
662
53/23
```

No checker code was changed.
