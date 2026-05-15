# Skeptical Audit

Batch 002 adversarial audit, 2026-05-15:

- Open status: stale as stated. Naor-Teague explicitly left variable-size allocation open in 2001, but Kuszmaul's FOCS 2023 paper "Strongly History-Independent Storage Allocation: New Upper and Lower Bounds" (DOI:10.1109/FOCS57990.2023.00111) directly addresses strongly history-independent allocation of variable-sized memory blocks.
- Why might this not actually be open? The 2023 storage-allocation paper appears to be a direct modern answer/narrowing of the exact historical problem. The Batch 002 claim should not be promoted from the 2001 source alone.
- Why might it be too saturated? The niche is small, but this exact historical gap has direct recent attention. Any residual problem is probably technical and model-specific.
- Smallest meaningful subproblem: after reading the 2023 paper, isolate a residual such as worst-case rather than amortized overhead, deterministic rather than randomized allocation, tighter fragmentation, or a restricted RAM/block model not covered there.
- Best use after audit: background context. Do not use as theorem project until residual tradeoffs are sourced.
- Blind-prompt warning: the current blind prompt likely presents a solved/narrowed problem as open.
- Why might automation fail or mislead? Exhaustive state-layout checks scale poorly and can miss distributional equality issues; they are useful only after a tiny formal allocator model is fixed.
- What would falsify interest? The 2023 paper fully handles the low-overhead variable-size strong-history-independence model that Batch 002 intended.
- Primary sources to check next: Naor-Teague 2001 for the historical statement; Kuszmaul et al. FOCS 2023 for the modern storage-allocation result; any 2024/2025 follow-up.
