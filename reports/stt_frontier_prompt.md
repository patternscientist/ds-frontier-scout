# STT Frontier Prompt

You are now allowed to use the project frontier context below. The goal is not
to solve all static search trees on trees, but to attack a narrow residual for
the versioned `golinsky_stt_lp_v0` relaxation and its depth projection.

Definitions:

- A static search tree on a base tree `U` is the recursive root-choice object
  defined in `reports/stt_true_blind_prompt.md`.
- The combinatorial checker uses root-depth-1 search costs.
- The LP uses strict-ancestor depths `D_i`; for normalized frequencies, base-1
  search cost is `1 + sum_i f_i D_i`.

Known frontier context:

- The relevant relaxation is `golinsky_stt_lp_v0`, the vanilla `X,Z,D` LP
  specified in `reports/stt_lp_spec_golinsky_v0.md`.
- Because the source LP has depth inequalities `D_i >= sum_j X_ji`, the right
  depth-space target is lower-envelope exactness:

```text
pi_D(P_U) = conv(STT LP-depth vectors) + R_{\ge 0}^n
```

- Equivalently, every feasible LP-depth vector should dominate some convex
  combination of valid STT LP-depth vectors.
- SKZ refutes full LP exactness with source long-star and path-5 barriers.
- The known SKZ source long-star fixture is source-aligned combinatorially in
  `examples/stt/skz_long_star_7_stt_optimum.json`, but a full LP fixture still
  requires complete source-transcribed `X`/`Z`/`D`.
- The remaining target is edge-diameter <= 3, with the almost-star convention
  still advisory until verified.

Task:

Try to prove or refute lower-envelope exactness for `golinsky_stt_lp_v0` on
edge-diameter <= 3 base trees. If the statement is too broad, isolate the
smallest precise subclass where a proof may work, or propose the smallest exact
rational witness that would falsify it.

Useful attack surfaces:

- characterize the structure of edge-diameter <= 3 trees under the line-graph
  convention;
- compare LP ancestry variables to recursive root choices;
- search for missing inequalities that are valid for all STT depth vectors;
- derive a separation problem for the STT depth hull;
- enumerate small topologies and depth vectors before attempting any proof;
- keep LP feasibility, depth-projection exactness, and root-rounding behavior
  separate.

Do not claim the residual is open unless a source check has been made. Treat
all almost-star wording as convention-sensitive.
