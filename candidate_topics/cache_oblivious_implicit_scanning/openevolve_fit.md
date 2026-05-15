# OpenEvolve Fit

OpenEvolve suitability: 3/5.

Plausible evaluators:

- simulate candidate implicit layouts under many block sizes;
- score search locality and scan locality simultaneously;
- test rebuild schedules for amortized update bounds;
- search small permutation-layout gadgets.

Main caveat: asymptotic cache-oblivious proofs are delicate, and finite simulation can overfit to selected block sizes.
