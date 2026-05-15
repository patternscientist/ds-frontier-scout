# Skeptical Audit

Why this might not actually be open:

- The 2025 paper explicitly says solving static STT by any tool/approach is still open, but a 2026 preprint or thesis update could have solved a subclass.
- Paths and stars must not be presented as open exact-optimization cases: paths reduce to ordinary optimal BSTs, and stars are proved LP-integral with a polynomial-time optimal algorithm.
- "Paths open" in this folder means LP/root-rounding/projection behavior for the STT LP, not the existence of an exact polynomial-time optimal search tree for path topology.
- Golinsky's original LP source still needs direct verification; Sadeh-Kaplan-Zwick's description is a strong secondary primary-ish account but not the original conjecture text.

Why this might be too saturated:

- Not globally saturated, but the small active STT community includes the people who introduced, approximated, and refuted the LP conjectures.
- The obvious computational enumeration route has already been pushed through all topologies up to 8 nodes in the tested regime.

Why automatic evaluation might fail:

- Polytope enumeration scales badly and can produce misleading "all small cases pass" evidence.
- Random objective sampling can miss rare fractional vertices.
- New inequalities may hold on all small topologies and fail under simple topology composition.

What would falsify interest:

- Reproducing the arXiv source code fails or reveals the examples are too brittle to extend.
- Almost-stars / edge-diameter-3 LP integrality is already settled in unpublished notes.
- The only next step is generic polyhedral optimization without a data-structure-specific insight.

Primary sources to check before promotion:

- Sadeh-Kaplan-Zwick arXiv v2 and source archive.
- Golinsky's original thesis/manuscript for the LP and conjecture.
- Berendsohn's 2024 thesis chapters on static STT and k-cut dynamic programming.
- Citations of arXiv:2501.17563 after 2025-08-01.

Smallest acceptable project:

- Reproduce the normals/counterexample pipeline, then attack edge-diameter-3/almost-star LP integrality or D-space projection integrality with certified scripts.
