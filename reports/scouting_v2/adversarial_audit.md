# Scouting v2 Adversarial Audit

Status: not started; run after synthesis draft.

Purpose: hostile review of Scouting v2 candidates, rankings, duplicate handling, source provenance, freshness checks, and the risk of prematurely disrupting the current STT / DS(k,1) proof lane.

## Non-Interruption Audit

STT / DS(k,1) remains the active foreground theorem project. This audit must explicitly check whether any synthesis recommendation would prematurely interrupt the current DS(k,1) proof lane.

Audit questions:

- Does the synthesis claim or imply that Scouting v2 supersedes STT without a later control-panel decision?
- Does it re-rank from scratch while treating STT's current rank as informational only?
- Does it recommend a pivot, pause, or resource shift that would interrupt DS(k,1)?
- If it recommends later review, is that clearly framed as a control-panel decision rather than an automatic outcome?

Default audit verdict unless proven otherwise: no Scouting v2 result causes a pivot by itself.

## Source-Provenance Audit

For each promoted candidate:

- Are exact titles, URLs/DOIs/arXiv IDs, search terms, and dates searched recorded?
- Is the open status marked as `explicit`, `inferred`, `uncertain`, or `likely_solved`?
- Is the distinction clear between what the source says, what is inferred, and what is a scouting hypothesis?
- Was the last-24-month freshness check actually performed and logged?
- Were primary sources preferred over secondary summaries?

## Duplicate And Saturation Audit

For each promoted candidate:

- Were existing slugs in `candidate_topics/` checked?
- Was `reports/top_20_shortlist.md` checked?
- If duplicate, was only a source/update recorded rather than a new candidate?
- Does the synthesis mistake repeated coverage of the same area for independent evidence of saturation?
- Does any subrun overgeneralize from a narrow source pool to a broad area-level conclusion?

## Candidate Audit Template

Use one section per promoted candidate.

### TODO Candidate Slug

- synthesis rank: TODO
- source-supported open status: TODO
- strongest evidence for promotion: TODO
- strongest reason it might not actually be open: TODO
- strongest reason it might be too saturated: TODO
- strongest reason automatic evaluation might fail: TODO
- what would falsify interest: TODO
- primary sources that must be checked before promotion: TODO
- score corrections:
  - literal under-attendedness: TODO
  - AI-collaboration fit: TODO
  - theorem-project suitability: TODO
  - OpenEvolve suitability: TODO
  - intellectual interest: TODO
- audit verdict: TODO

## Serious Rejection Audit

Check whether the rejection ledgers are strong enough to prevent future re-litigation without source changes.

| Lead | Subrun | Rejection ledger adequate? | Missing provenance | Revisit condition |
| --- | --- | --- | --- | --- |
| TODO | TODO | TODO | TODO | TODO |

## Final Verdict

TODO after synthesis draft.

The final verdict must say one of:

- no recommendation should affect the active DS(k,1) proof lane;
- recommendation should be reviewed later by the control panel, with no automatic pivot;
- synthesis is too weak or source-fragile to support any control-panel review.

