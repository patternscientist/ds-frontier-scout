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

- Done in `frontier.md` and `blind_prompt.md` for this hardened version: the main dissection lemma, shifting lemma, `J_k` hierarchy, and Tarjan-style Ackermann normalization are now explicit.

## Lecture-Note Direct-Proof Audit

Checked on 2026-05-17:

- Seidel's Princeton/COS 423 path-compression slides give the top-down recurrence and an inverse-Ackermann-style interpretation, but the checked slides do not appear to provide the requested direct comparison from the paper's `J` hierarchy to Tarjan's classical Ackermann function.
- Stanford CS166 2025 disjoint-set slides give a recent pedagogical recurrence exposition and an iterated-log-style inverse-Ackermann definition. This is useful context, but it is not the direct `J_k`-to-classical-`A(i,x)` proof requested in Dagstuhl 25191.
- Search snippets for other union-find lecture notes mostly expose standard Tarjan/CLRS-style analyses or Seidel-Sharir recurrences. No checked public note was found that cleanly closes the exact proof-translation gap.

Audit consequence: keep `open_status: open_proof_problem`, but do not claim novelty beyond Tarjan's 2025 problem statement. Before any theorem-pilot promotion, recheck author-maintained lecture notes and ask whether Seidel's SWAT 2006 invited material contains an unpublished fuller comparison.
