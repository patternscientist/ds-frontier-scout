# Skeptical Audit

Why this might not actually be open:

- The Lazy B-Trees paper explicitly flags the external biased-search-tree gap, but "fully satisfactory" is not itself a theorem statement.
- A specialized external biased structure may exist under different terminology in external-memory search-tree literature.

Why this might be too saturated:

- Low broad saturation, but the target is recent and likely being pursued by the authors or adjacent experts.

Why automatic evaluation might fail:

- Small B-tree simulations do not certify weighted I/O bounds or linear block-space guarantees.
- Update-heavy versions may hide the simpler static weighted-search obstruction.

What would falsify interest:

- A known external biased search tree already achieves `O(n/B)` blocks and `O(log_B(W/w)+1)` I/Os with suitable updates.
- The remaining issue is an implementation detail internal to Lazy B-Trees rather than a standalone theorem.

Primary sources to check before promotion:

- Rysgaard-Wild MFCS 2025 full version.
- External-memory biased search tree and biased skip tree literature.
- Any follow-up notes from Wild/Rysgaard after MFCS 2025.
