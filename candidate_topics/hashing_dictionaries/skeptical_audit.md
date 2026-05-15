# Skeptical Audit

Batch 002 adversarial audit, 2026-05-15:

- Open status: uncertain/residual, not promotion-ready. The `all_purpose_hashing_residual` lead has no single explicit unsolved theorem after All-Purpose Hashing/Iceberg hashing and follow-up optimal time/space tradeoff work.
- Why might this not actually be open? "All desirable hash-table properties at once" was historical motivation before Iceberg hashing, not necessarily a current open claim. Later tradeoff papers may already settle the natural succinct-waste/time variants under their models.
- Why might it be too saturated? Recent hash-table theory is active and technical. A vague residual tradeoff is likely to duplicate ongoing work or propose a solved variant.
- Smallest meaningful subproblem: choose one model-specific tradeoff, such as stable addresses plus succinct wasted space plus very-high-probability operations under a named hashing/randomness model.
- Best use after audit: background context. Do not promote until an explicit residual statement is extracted from primary sources.
- Why might automation fail or mislead? Simulations can optimize load factors and displacement distributions, but they do not prove high-probability, cache, stability, or succinct-space guarantees.
- Weak-source flag: All-Purpose Hashing and optimal tradeoff papers are solution/frontier papers; they should not be mined for broad open claims without exact residual text.
- What would falsify interest? A primary paper already proves the chosen combination of properties, or the remaining gap depends only on implementation engineering constants.
