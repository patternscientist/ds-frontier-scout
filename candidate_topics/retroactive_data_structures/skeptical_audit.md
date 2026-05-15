# Skeptical Audit

Batch 002 adversarial audit, 2026-05-15:

- Open status: inferred/uncertain. `retroactive_lower_bounds` is an attractive lower-bound direction, but Batch 002 did not find a primary source explicitly posing the exact unconditional or cell-probe strengthening as open.
- Why might this not actually be open? Demaine-Iacono-Langerman give classical retroactive transformations and examples; Chung-Demaine-Hendrickson-Lynch give strong conditional lower bounds. The apparent residual may be an artifact of wanting a cleaner theorem than the literature claims.
- Why might it be too saturated? Retroactivity is not saturated, but lower-bound strengthening is hard and may be dominated by fine-grained conjectures rather than finite certificates.
- Smallest meaningful subproblem: an explicit separation for one named dynamic problem, retroactivity type, update/query set, and model: unconditional cell-probe, OMv/3SUM-style conditional, or finite communication game.
- Best use after audit: background context until an exact residual is sourced.
- Why might automation fail or mislead? Operation-sequence search can find suggestive hard instances but cannot produce unconditional cell-probe lower bounds without a reduction framework.
- Weak-source flag: do not claim an "unconditional retroactive lower-bound strengthening" is explicitly open until a source says so.
- What would falsify interest? The cleanest residual is already implied by the 2022 lower-bound paper, or all plausible variants require assumptions outside this scouting project.
