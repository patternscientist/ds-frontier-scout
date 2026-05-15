# Skeptical Audit

Why this might not actually be open:

- The incremental topological sort target is not open as written. Bhattacharya and Kulkarni give a randomized algorithm with `~O(m^(4/3))` total expected update time for incremental cycle detection and topological ordering.
- Dagstuhl's Fineman note appears to ask for a different combinatorial/density-regime bound, but the HTML drops the exact mathematical expression. Do not promote until the exact target is recovered.
- The dynamic connectivity level-elimination question is explicitly open in Dagstuhl, but it is a simplification of a sophisticated Monte Carlo framework.

Why this might be too saturated:

- Dynamic graph algorithms are highly active and competitive.
- The natural next steps may require deep familiarity with Kapron-King-Mountjoy, Gibb-Kapron-King-Mountjoy, Wang, and batch-dynamic variants.

Why automatic evaluation might fail:

- Adversarial edge-insertion generators do not certify total update-time upper bounds.
- Simulators may reward implementation heuristics rather than proof-relevant invariants.
- For connectivity, randomization and failure probability must be modeled exactly.

What would falsify interest:

- Fineman's intended topological-sort question is simply the already-known randomized `~O(m^(4/3))` result.
- Level-elimination is known impossible or already solved in unpublished follow-up.

Primary sources to check before promotion:

- Bhattacharya-Kulkarni 2020, "An Improved Algorithm for Incremental Cycle Detection and Topological Ordering in Sparse Graphs."
- Dagstuhl 25191 PDF or slides for Fineman's exact missing expression.
- Liu-King/Cann-King-Liu batch-dynamic connectivity manuscript.

Batch 002 adversarial addendum, 2026-05-15:

- `dynamic_stream_mincut_space` is explicit in ITCS 2025 as a streaming open question, but it is not a classic dynamic data-structure candidate.
- Best use is background/lower-bound context unless a communication game or finite sketch lower-bound task is isolated.
- Saturation risk remains high: dynamic min-cut, streaming cuts, and cut sketches are active areas.
- Automation warning: small sketch games may suggest hard distributions, but a credible result needs communication-complexity proof machinery.
