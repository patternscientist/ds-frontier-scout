# Subrun 2I: OpenEvolve Object-First Source Pool

Status: not started.

Role: search for candidates by starting from concrete evolvable objects and evaluators, then tracing backward to source-supported open problems. This subrun is not allowed to promote generic "could simulate it" claims without a specific object.

## Assigned Source Pool

Allowed sources:

- Primary papers and expert notes that define finite objects, traces, layouts, policies, potentials, formulas, certificates, or search spaces tied to open data-structure questions.
- Existing candidate folders only for duplicate checks and for identifying object types that should not be duplicated.
- Reproducible artifacts, benchmark definitions, exact small-instance oracles, SAT/SMT/LP formulations, or formal checker descriptions attached to primary sources.

Out of scope:

- Candidates with only a vague evaluator and no evolvable object.
- Pure benchmarking or engineering optimization without a source-supported theorem question.
- Broad web/source exploration not anchored to an object or evaluator.

## Required Checks Before Promotion

- Check `candidate_topics/` slugs and `reports/top_20_shortlist.md`.
- Name the specific evolvable object before scoring OpenEvolve suitability.
- Identify the evaluator or oracle and what it can falsify, certify, or optimize.
- Run a last-24-month freshness check for every candidate.
- Record exact source URLs, DOI/arXiv IDs, titles, search terms, and date searched.
- Keep theorem-project suitability, OpenEvolve suitability, and intellectual interest separate.
- Do not promote more than five candidates; fewer is acceptable.

## Candidate Findings

No subrun performed yet.

## Rejection Ledger

No subrun performed yet.

## Evolvable Object Checklist

For every promoted or seriously rejected lead, record:

- object type: trace, access sequence, graph family, memory layout, policy, potential function, certificate, formula, distribution, or other precise object;
- mutation operators or generation scheme;
- evaluator/oracle;
- smallest exact instance size where the evaluator is meaningful;
- what success would and would not imply mathematically.

## Notes For Synthesis

Pilot-readiness ranking is informational only. A strong OpenEvolve object does not automatically outrank a better theorem candidate after the feasibility gate and lexicographic theorem ranking.

