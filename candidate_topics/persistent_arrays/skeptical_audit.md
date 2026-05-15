# Skeptical Audit

Batch 002 adversarial audit, 2026-05-15:

- Open status: likely solved or stale as stated. The cited Straka paper is itself titled "Fully persistent arrays with optimal worst-case access and update time" and its abstract presents the first worst-case optimal implementation. That is evidence against the Batch 002 open claim, not evidence for it.
- Why might this not actually be open? The exact target in the problem file, `O(n+m)` space and worst-case `O(log log m)` lookup/update, appears to be the result claimed by Straka's primary source. The Batch 002 reliance on secondary summaries likely inverted the citation.
- Why might it be too saturated? Saturation is not the main issue; the main issue is that the promoted question is probably already answered in the source folder.
- Smallest meaningful subproblem: extract the exact Dietz/Straka model assumptions and, only if a stricter model is found, restate a residual problem such as purely functional persistence, pointer-machine restrictions, cache-oblivious layout, or deamortization under a narrower operation set.
- Best use after audit: background context or Lean/formalization of known results. Discard as an open theorem target until a primary source states a residual gap.
- Blind-prompt warning: the current blind prompt asks for a known-or-likely-known result as if open.
- Why might automation fail or mislead? Small version-tree experiments cannot rediscover or refute the word-RAM layout theorem; they would mostly test implementation choices.
- What would falsify renewed interest? Direct confirmation from Straka's thesis/paper that the exact linear-space worst-case target is achieved, with no stricter unresolved model identified.
- Primary sources to check next: Straka 2009 PDF, Straka 2013 thesis persistent-array chapter, Dietz WADS 1989.
