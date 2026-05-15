# ds-frontier-scout

`ds-frontier-scout` is a research-scouting repository for systematically finding, verifying, comparing, and adversarially auditing under-attended open problems in data-structure theory and nearby algorithmic theory.

The repo is deliberately pre-solution. Its purpose is to build a reliable map of candidate projects before attempting proofs, experiments, or computational search.

## What Counts As A Candidate?

A candidate may be famous, obscure, or hyper-niche. The key requirement is that it could matter to a real specialist community if resolved. The initial spark came from splay trees and dynamic optimality, but this scouting process is intentionally broader than dynamic optimality.

Candidates should be marked honestly:

- `open`: supported by checked sources.
- `uncertain`: plausible, but source verification is incomplete.
- `closed`: no longer a candidate, retained only for audit history.

## Scouting Workflow

1. Collect seed sources and open-problem mentions in `sources/`.
2. Create one folder per candidate topic in `candidate_topics/`.
3. For each candidate, write:
   - a self-contained problem statement;
   - a frontier summary from verified sources;
   - a blind prompt suitable for no-internet theorem exploration;
   - a skeptical audit;
   - separate fit assessments for theorem discovery and OpenEvolve-style search.
4. Compare candidates in `reports/candidate_matrix.md`.
5. Promote the most promising items into `reports/top_20_shortlist.md`.
6. Maintain the current best recommendation in `reports/fixed_point_recommendation.md`.

## Evaluation Axes

The repo separates three questions that are often conflated:

- Is this a good AI-assisted theorem project?
- Is this a good OpenEvolve or evaluator-driven computational-search project?
- Is this intellectually interesting in general?

A topic can score high on one axis and low on another. For example, a problem may be mathematically beautiful but hard to automate, or highly searchable by exhaustive small-instance methods but not especially promising as a proof project.

## Rendering Scores

To refresh `data/scores.csv` and `reports/candidate_matrix.md`, run:

```sh
python scripts/scoring/render_scores.py
```

## STT Checker v0

The first proof-mode checker scaffold for the `search_trees_on_trees_lp` pilot
lives in `scripts/stt_checker/`. It validates exact base-tree topologies,
recursive STTs, rational vertex-frequency costs, and small complete
enumerations, while rejecting unsupported LP fields in proof mode.

See `docs/stt_checker_v0.md` for the supported certificate subset and CLI
examples. A quick smoke test from the repo root is:

```sh
python -m scripts.stt_checker.cli check examples/stt/long_star_7.json
```

The first reproducible small-topology frontier artifact is generated in
`reports/stt_v0_frontier_artifact.md`, with companion machine-readable files in
`data/stt_frontier/`.

The LP feasibility checker v0 replays dense exact rational certificates for
`golinsky_stt_lp_v0` only. It lives beside the STT checker and is documented in
`docs/stt_lp_feasibility_v0.md`:

```sh
python -m scripts.stt_checker.cli check-lp examples/stt_lp/path_4_stt_induced_lp.json
```

It is not an LP solver and does not check root rounding, integrality gaps, or
projection/lower-envelope claims.

## Source Discipline

Do not invent citations or open-problem claims. Use TODO markers until sources are checked. Primary sources are preferred over survey summaries, and every promoted candidate should include a skeptical audit explaining why the claimed open status might be wrong.

## Current Status

This repository now contains the initial scaffold; Batch 001 scouting; targeted high-priority patches; the Batch 001 adversarial audit; scoring infrastructure; the Batch 002 saturation pass and adversarial audit; cross-batch fixed-point synthesis; Batch 003 mini-frontier scouting; the STT LP certificate schema; the Batch 003 adversarial audit; and exact rational LP feasibility checking for `golinsky_stt_lp_v0`. The current leading pilot remains `search_trees_on_trees_lp`, especially as a combined theorem/certificate/OpenEvolve project.

Batch 003 added candidates in dynamic-stream min-cut, directed compact roundtrip routing, concurrent history-independent hash-table cell capacity, connected geometric circle-segment queries, and cache-oblivious implicit dictionary scans. Its adversarial audit downgraded several evaluator claims, especially the concurrent SHI and cache-oblivious scan formulations, and left checker-blocking clarifications for the STT LP certificate schema before implementation.
