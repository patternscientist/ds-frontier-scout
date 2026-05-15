# STT v0 Frontier Artifact

Generated for unlabeled tree topologies with `n <= 7`.

## Purpose And Scope

This artifact is a reproducible small-instance summary for the exact combinatorial STT checker scaffold v0. It generates tree topologies, deduplicates them up to isomorphism, derives checker-supported labels, enumerates valid recursive STTs when below the configured cap, and computes exact integer optima for simple rational vertex-frequency objectives.

**No LP feasibility is checked here.** This artifact does not implement, guess, or validate Golinsky LP constraints, LP variable domains, root rounding, or integrality-gap claims.

## Method

- Labeled trees are generated from Prufer codes on vertices `0..n-1`.
- Isomorphic duplicates are removed using an AHU-style canonical string: find the tree center or centers, compute sorted rooted subtree strings, and keep the lexicographically smallest center-rooted form.
- Derived labels use the existing checker: `path`, `star`, and exact `edge-diameter-k` under the line-graph edge-distance convention.
- Complete STT enumeration uses the checker cap `100000`. If a topology exceeds that cap, the record says so instead of failing the artifact build.

## Output Files

- `data/stt_frontier/topologies_n_leq_7.json`
- `data/stt_frontier/topology_summary_n_leq_7.csv`
- `reports/stt_v0_frontier_artifact.md`

## Unlabeled Tree Shapes By n

| n | shapes |
|---:|---:|
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |
| 4 | 2 |
| 5 | 3 |
| 6 | 6 |
| 7 | 11 |

## Edge-Diameter Class Counts By n

| n | edge-diameter-0 | edge-diameter-1 | edge-diameter-2 | edge-diameter-3 | edge-diameter-4 | edge-diameter-5 |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| 3 | 0 | 1 | 0 | 0 | 0 | 0 |
| 4 | 0 | 1 | 1 | 0 | 0 | 0 |
| 5 | 0 | 1 | 1 | 1 | 0 | 0 |
| 6 | 0 | 1 | 2 | 2 | 1 | 0 |
| 7 | 0 | 1 | 2 | 5 | 2 | 1 |

## Edge-Diameter-3 Topologies

| n | degree sequence | edges | STT count | uniform optimum |
|---:|---|---|---:|---:|
| 5 | 2 2 2 1 1 | `[[0,1],[0,3],[1,2],[2,4]]` | 42 | 11/5 |
| 6 | 3 2 2 1 1 1 | `[[0,1],[0,3],[0,4],[1,2],[2,5]]` | 166 | 13/6 |
| 6 | 3 2 2 1 1 1 | `[[0,1],[0,2],[0,3],[1,4],[2,5]]` | 176 | 13/6 |
| 7 | 4 2 2 1 1 1 1 | `[[0,1],[0,3],[0,4],[0,5],[1,2],[2,6]]` | 836 | 15/7 |
| 7 | 3 3 2 1 1 1 1 | `[[0,1],[0,3],[0,4],[1,2],[2,5],[2,6]]` | 721 | 16/7 |
| 7 | 3 3 2 1 1 1 1 | `[[0,1],[0,3],[0,4],[1,2],[1,5],[2,6]]` | 807 | 16/7 |
| 7 | 3 2 2 2 1 1 1 | `[[0,1],[0,4],[1,2],[1,3],[2,5],[3,6]]` | 662 | 16/7 |
| 7 | 4 2 2 1 1 1 1 | `[[0,1],[0,2],[0,3],[0,4],[1,5],[2,6]]` | 930 | 15/7 |

## Checker-Only Observations

- The generator found `25` unlabeled tree shapes for `n <= 7`.
- `21` of these shapes have checker-derived edge diameter at most 3.
- `8` shapes have checker-derived edge diameter exactly 3.
- Complete STT enumeration finished for `25` shapes and exceeded the configured cap for `0` shapes.
- Uniform and leaf-heavy objective values in the machine-readable files are exact integer optima only when `enumeration.completed` is true.

These observations are only statements about the exact checker output. They do not imply any LP integrality, LP feasibility, or theorem-level claim.

## Next Targets For The LP Phase

- Specify a versioned machine-readable Golinsky STT LP constraint set.
- Define exact variable domains and absent-variable defaults for all LP variable families.
- Add exact LP feasibility checking only after the constraint set is fixed.
- Compare future LP depth projections against the enumerated STT depth vectors for the edge-diameter-3 records listed above.
