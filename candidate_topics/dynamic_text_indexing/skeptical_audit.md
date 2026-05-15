# Skeptical Audit

Batch 002 adversarial audit, 2026-05-15:

- Open status: explicit in the older source, but stale and model-dependent now. Dynamic compressed self-indexing after 2007 appears to solve nearby goals in compressed-space measures, so the Batch 002 statement is too broad.
- Why might this not actually be open? Later dynamic compressed indexes, including signature-encoding based results, support updates and pattern searches under compressed or grammar-like space bounds. They may not equal `O(|T|)` bits for the exact single-text formulation, but they narrow or supersede the naive 2007 question.
- Why might it be too saturated? Dynamic string indexing, BWT/FM-indexing, grammar compression, and repetitive-text indexing are active subfields with many model variants. A broad "compact dynamic text indexing" candidate is a literature-review trap.
- Smallest meaningful subproblem: fix alphabet model, bit accounting, online substring insertion/deletion, worst-case vs amortized guarantees, and whether reporting time may include logarithmic factors per occurrence.
- Best use after audit: background context until a residual theorem is isolated. It is not ready as a theorem-project target.
- Weak-source flag: ResearchGate snippets are not enough. Use the ACM/TALG paper and later primary dynamic compressed-index papers.
- Why might automation fail or mislead? Exact small-string oracles test correctness of an index but not succinct bit-space or compressed-space asymptotics. An OpenEvolve evaluator would likely optimize an implementation toy, not the theorem gap.
- What would falsify interest? A modern dynamic self-index matching the exact linear-bit substring-update target, or evidence that the only open residuals are engineering constants.
- Primary sources to check next: Chan-Hon-Lam-Sadakane final paper; dynamic compressed self-index/signature-encoding papers; dynamic BWT/FM-index theory after 2010.
