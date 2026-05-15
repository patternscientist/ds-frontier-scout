# STT Diameter-3 Prediction Memo

Date: 2026-05-15

## Current Working Hypothesis

Public-source status: no checked public follow-up found so far settles the
edge-diameter-3 / almost-star residual after Sadeh-Kaplan-Zwick. The residual
appears legitimate enough for pilot work, but unpublished follow-up remains a
real uncertainty.

Working mathematical hypothesis: edge-diameter <= 3 may be lower-envelope exact
for `golinsky_stt_lp_v0`, but this should be treated as a falsification target
before becoming a proof target.

## Why Exactness Might Hold

- Edge-diameter <= 3 trees have very limited branch interaction under the
  line-graph convention.
- Paths and stars are already sanity baselines rather than warning examples.
- The known public barriers begin outside the narrow residual currently being
  targeted.
- Recursive root choices in these topologies may have enough local structure to
  force LP-depth optima onto the STT depth hull plus the nonnegative orthant.

## Why A Witness Might Still Exist

- The LP variables encode ancestry and loose LCA relations, not the full
  recursive decomposition.
- Small fractional effects can hide in objective directions that are rare under
  random sampling.
- The almost-star convention is still advisory; a convention mismatch could
  make the target either too broad or too narrow.
- Edge-diameter <= 3 may prevent the known examples without preventing a more
  delicate fractional depth projection.

## Evidence That Would Update Us

- A public or author-confirmed follow-up resolving the residual would dominate
  local inference.
- Exact LP enumeration over all edge-diameter <= 3 topologies through the next
  feasible `n` with no fractional depth witness would raise proof confidence,
  but would not prove the theorem.
- A single exact rational LP-depth vector separated from the STT depth hull
  would falsify the working hypothesis.
- A structural reduction from edge-diameter <= 3 trees to path/star-like
  components would shift effort toward proof-first.

## Next Computational Search Plan

1. Keep the combinatorial fixtures honest:
   `examples/stt/edge_diameter3_checker_only_7.json` is checker-only, while
   `examples/stt/skz_long_star_7_stt_optimum.json` is SKZ source-aligned for
   the STT optimum.
2. Do not add a full SKZ LP fixture until complete `X`/`Z`/`D` values are
   source-transcribed.
3. Add a small exact depth-hull exporter for enumerated STTs.
4. Add a separation check for supplied LP-depth vectors against
   `conv(STT depths) + R_{\ge 0}^n`.
5. Only then run an LP-backed search over edge-diameter <= 3 topologies.

## Choice

Use falsification-first before proof-first. The next pilot should try to break
the edge-diameter <= 3 lower-envelope hypothesis with exact small certificates
before investing heavily in a polished proof attempt.
