# Skeptical Audit

Why this might not actually be open:

- It is not open as a data-structure bound: path compression already has inverse-Ackermann analyses.
- The open part is a proof-exposition request: derive the classical inverse-Ackermann bound directly from the Seidel-Sharir top-down recurrence using a classical Ackermann definition.
- A simple proof may exist in lecture notes or unpublished course material.

Why this might be too saturated:

- Union-find analysis is classic, but this exact recurrence-comparison problem is niche rather than saturated.

Why automatic evaluation might fail:

- There is no meaningful OpenEvolve evaluator for the proof. Numeric recurrence experiments can suggest mappings but cannot certify the asymptotic proof.
- A blind prompt without the exact recurrence risks solving a different problem.

What would falsify interest:

- The recurrence-to-Ackermann translation is already written cleanly in Seidel's SWAT notes, Stanford/Princeton lecture notes, or Tarjan's unpublished notes.
- The resulting proof is not simpler than the existing Seidel-Sharir exposition.

Primary sources to check before promotion:

- Seidel-Sharir, "Top-Down Analysis of Path Compression," SIAM J. Comput. 2005.
- Tarjan's Dagstuhl 25191 problem statement.
- Seidel's SWAT 2006 invited abstract/notes if available.

Required prompt fix:

- Copy the exact recurrence and define the exact Ackermann/inverse-Ackermann normalization before using `blind_prompt.md`.
