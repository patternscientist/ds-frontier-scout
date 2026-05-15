# Skeptical Audit

Why this might not actually be open:

- The historic open claim is no longer open in its original form. Kuszmaul and Xi prove a nontrivial positive result: constant expected insertion time for fixed-offset schemes at load factor at least `0.089`, with quadratic probing as a corollary.
- The remaining open problem is inferred: improve the load-factor regime, sharpen thresholds, extend models, or handle practical variants. Do not state "prove anything nontrivial" as current frontier.

Why this might be too saturated:

- After ICALP 2024 this may draw more attention. It is no longer an invisible folklore gap.
- The proof technique is specialized witness combinatorics; low-hanging improvements may already be in follow-up work or author notes.

Why automatic evaluation might fail:

- Finite-size simulations can badly overestimate high-load asymptotic behavior.
- Model choices matter: full randomness vs limited independence, fixed-offset sequence assumptions, chunking, table-size arithmetic, rebuild/deletion policy, and successful vs unsuccessful search.
- An evaluator should search for exact witness configurations or proof certificates, not just empirical average probe counts.

What would falsify interest:

- A post-2024 follow-up proves the natural high-load threshold or gives a broadly accepted tight analysis.
- The remaining constant-improvement problem reduces to tedious optimization of the existing witness enumeration without new structure.

Primary sources to check before promotion:

- Kuszmaul-Xi ICALP 2024 full paper, especially Theorems 1 and 2 and the exact assumptions on fixed-offset probing.
- Dagstuhl 25191 discussion for what Kuszmaul presents as still open.
- Any citations/follow-ups after ICALP 2024.
