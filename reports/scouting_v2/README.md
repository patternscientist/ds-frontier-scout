# Scouting v2 Framework

Status: framework only; subruns not started.

Purpose: define a source-diverse background scouting lane that avoids the prior failure mode where one broad run prematurely inferred saturation. This lane prepares candidate search, source logging, synthesis, and adversarial audit templates. It does not execute any subrun by itself.

## Background-Lane Boundary

STT / DS(k,1) remains the active foreground theorem project. Scouting v2 is background candidate search only. It must not overwrite, supersede, or re-rank the current STT proof work by itself. Any possible pivot must wait for later control-panel review of the synthesis and adversarial audit.

## Subruns

- `subrun_2A_geometry.md`: computational geometry and geometric data-structure source pool.
- `subrun_2B_cell_probe_lower_bounds.md`: cell-probe and adjacent lower-bound source pool.
- `subrun_2F_author_problem_pages.md`: author-maintained problem pages, course notes, and personal open-problem lists.
- `subrun_2I_openevolve_objects.md`: evaluator/object-first search for OpenEvolve-compatible candidates.
- `subrun_2R_v1_area_remining.md`: re-mining previously scouted areas for source-diverse updates, duplicates, and rejected-but-revivable leads.

## Methodology Rules

1. Scouting v2 is a background lane. It does not supersede STT / DS(k,1) without explicit later control-panel decision.
2. Scouting v2 has a 5-calendar-day budget from the first subrun. If the deadline arrives, synthesize completed subruns and stop.
3. Each subrun searches only its assigned source pool.
4. Each subrun may return fewer than five candidates. Do not pad.
5. Before proposing a candidate, check existing slugs in `candidate_topics/` and `reports/top_20_shortlist.md`.
6. If a candidate duplicates an existing slug, do not create a new entry; record only the new source/update.
7. For every candidate, do a freshness check for progress or closure in the last 24 months.
8. Mark `open_status = explicit / inferred / uncertain / likely_solved`.
9. Record exact source URLs/DOIs/arXiv IDs/titles, search terms, and date searched for each candidate and serious rejected candidate.
10. Maintain a rejection ledger for every subrun.
11. Use anchored literal-under-attendedness scores:
    - 5 = fewer than 5 citations of the open question by name in the past 10 years, no AI-collab work, one specialist/small group.
    - 4 = 5--20 citations, one or two active researchers, no AI attention.
    - 3 = specialist subfield, regular but slow work, no AI attention.
    - 2 = active specialist area, ongoing work, some AI attention.
    - 1 = high-traffic conjecture with multiple AI-collab efforts or major community focus.
12. Feasibility gate runs before lexicographic ranking.
13. Synthesis must re-rank from scratch. STT's current rank is informational only and must not anchor the new ranking.
14. Primary theorem ranking is lexicographic among feasibility-gated candidates:
    - literal under-attendedness;
    - AI-collaboration fit;
    - theorem-project suitability.
15. Pilot-readiness ranking is separate and informational.
16. OpenEvolve suitability must include a specific evolvable object, not just a generic evaluator.
17. After Scouting v2 and its audit, the output is a recommendation only. It does not cause a pivot unless the control-panel chat explicitly accepts it.
18. Synthesis and audit must explicitly check whether any recommendation would prematurely interrupt the current DS(k,1) proof lane.

## Candidate Record Template

Use this shape inside a subrun only after duplicate checks and source logging are complete.

```yaml
slug: TODO
title: TODO
subrun: TODO
open_status: uncertain
source_pool: TODO
primary_sources:
  - title: TODO
    url_or_doi_or_arxiv: TODO
    source_type: paper/preprint/lecture_note/problem_page/author_page/conference_page
    date_searched: TODO
freshness_check_24_months:
  search_terms:
    - TODO
  sources_checked:
    - TODO
  result: TODO
literal_under_attendedness: TODO
theorem_project_suitability: TODO
openevolve_suitability: TODO
intellectual_interest: TODO
ai_collaboration_fit: TODO
feasibility_gate: pass/fail/uncertain
specific_evolvable_object: TODO
duplicate_check:
  candidate_topics_slugs_checked: true
  top_20_shortlist_checked: true
  duplicate_of: null
scouting_hypothesis: TODO
source_says: TODO
inference_from_sources: TODO
skeptical_audit_hooks:
  not_open_risk: TODO
  saturation_risk: TODO
  auto_evaluation_risk: TODO
  falsifier: TODO
  primary_sources_before_promotion:
    - TODO
```

## Serious Rejection Record Template

Every serious rejected lead needs enough provenance to be recoverable later.

```yaml
title_or_slug: TODO
subrun: TODO
reason_rejected: TODO
source_urls_or_ids:
  - TODO
search_terms:
  - TODO
date_searched: TODO
freshness_or_closure_signal: TODO
could_revisit_if: TODO
```

