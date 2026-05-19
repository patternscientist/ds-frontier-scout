# v5.4.1 unified overview patch audit

**Date:** 2026-05-19  
**Branch:** `frontier-v5-4-1-overview-patch`  
**Installed overview:** `reports/frontier_note_v5_4_1_unified_project_overview.md`  
**Audit scope:** focused prose/provenance sanity audit against Claude red-team audit v2 and the Codex starter prompt. This audit did not attempt a new proof pass or broad certificate-suite rebuild.

## Summary verdict

The patched overview is installed and passes the focused starter checks. The four red-team must-fixes and the main should-fixes requested in the starter prompt are present in the installed Markdown. The file keeps the patched overview's explicit claim boundary: no new theorem claims are introduced by this integration document.

## Must-fix checklist

- Public references/citations for SKZ, Berendsohn, and BGKK: verified present in Section 2 and Appendix B.
- Five right atoms / three cap basis / four cap regions, including `qB`/`ABq` cancellation: verified present in Section 6.5.
- Explicit `U(7,3)` H1 failure guardrail: verified present in the TL;DR, Section 4, and Section 11 motivation.
- Notation and terms subsection: verified present after Section 3, defining `Conn(T)`, `DS(k,m)`, packet basis names, `ell_ij`, `SUB_T`, `D(S) >= delta(S)`, `b-root`, proper-subset contraction, `EVOLVE-block guards`, and leaf-swap atlas orbit representatives.

## Main should-fix checklist

- SKZ Open Question 5(b) framing for `DS(k,1)`: verified present in Sections 2, 5, and 10.
- Meaningful-endpoint / not-template warning for `DS(k,1)`: verified present in Section 6.8 and Section 10.
- Forbidden-tool audit paragraph for the v5.3 proof: verified present in Section 6.8.
- TL;DR warning that no checked artifact closes or refutes residual `ell_ij`: verified present.
- Dominance-form vs cost-equality bridge: verified present in Section 5.
- `sympy` requirement for the leaf-local checker: verified present in Section 6.6 and Appendix A.
- DS(2,2) full-objective depth inclusion and simplex-augmented packet-conic closure separated: verified present in the TL;DR and Section 7.1.

## Overclaim/status audit

The installed overview uses separate status buckets for theorem-level internal results, theorem-level obstruction guardrails, certificate-backed finite results, open/candidate public-LP bridge status, killed/demoted routes, and side-lane infrastructure. The "What is not claimed" section explicitly rules out:

- public Golinsky/SKZ LP exactness;
- all-`k` `DS(k,2)`;
- all `DS(k,m)`;
- all double-stars, spiders, or max-degree-3 trees;
- a polynomial-time exact STT algorithm;
- OpenEvolve/list-update policy discovery.

I did not find a new theorem claim introduced by the patch. The additions are citation/provenance framing, notation, explicit guardrails, or clearer labels for already referenced repo artifacts.

## Appendix A path check

All 35 unique repo paths parsed from Appendix A exist in the current checkout. No history-only paths appear in Appendix A of the patched overview.

## Commands run

```powershell
git status --short --branch
git log --oneline --decorate --max-count=10
```

Result: current branch was created from clean `main` at `e6e98a6`, which is after the expected `145a34c`.

```powershell
python - <<'PY'
from pathlib import Path
import re
p = Path('reports/frontier_note_v5_4_1_unified_project_overview.md')
text = p.read_text(encoding='utf-8')
assert text.count('```') % 2 == 0
# Required phrase, notation, status-label, and Appendix A path checks.
PY
```

Result: passed; reported balanced fences, required phrases present, required terms present, and 35 Appendix A paths existing.

```powershell
python scripts/dsk1_leaf_local_cap_certificate_check.py
```

Initial sandbox result: failed with `ModuleNotFoundError: No module named 'sympy'`.

```powershell
python -m pip install --user --force-reinstall sympy
python scripts/dsk1_leaf_local_cap_certificate_check.py
```

Result after installing `sympy` and running with access to the active user Python environment: `ok: corrected fan and primitive-ray certificates verified`.

```powershell
git diff --check
```

Result: passed.

## Remaining caveats

- I did not rerun broad DS(2,2), DS(3,2), DS(4,2), public-LP, or list-update certificate/test suites. The overview reports those from existing repo artifacts and the v5.4 provenance manifest.
- The default workspace sandbox could not see the user-site `sympy` installation, so the leaf-local checker's successful run required permission to use the active user Python environment.
