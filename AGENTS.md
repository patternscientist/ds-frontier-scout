# ds-frontier-scout Agent Instructions

This repository is for scouting under-attended open problems in data-structure theory and nearby algorithmic theory. The goal is infrastructure and careful research triage, not solving problems yet.

## Research Standards

- Prefer primary sources: papers, preprints, lecture notes by domain experts, conference problem lists, and author-maintained pages.
- Do not invent citations, theorem names, folklore claims, dates, venues, or open-problem status.
- If a source has not been checked, write `TODO: verify source` or mark `open_status: uncertain`.
- Distinguish clearly between:
  - what a source explicitly says;
  - what we infer from the literature;
  - our own scouting hypothesis.
- Preserve uncertainty. A candidate being uncertain is acceptable; a fake certainty is not.

## Candidate Philosophy

- Under-attended can mean extremely niche. A topic may be worthwhile even if only a small specialist community cares.
- Do not optimize for fame, popularity, or benchmark glamour.
- Avoid saturated flagship problems unless the candidate is a narrow, under-attended subproblem with a distinct attack surface.
- The theorem-project candidate and the OpenEvolve/evolutionary-search candidate do not need to be the same.
- It is acceptable, and often desirable, to scout weird corners of data structures, online algorithms, combinatorics of access sequences, external memory, succinct structures, geometry, hashing, kinetic structures, and dynamic graph maintenance.

## Required Separation Of Scores

For each candidate, keep separate judgments for:

- `theorem_project_suitability`: fit for AI-assisted proof search using staged prompting.
- `openevolve_suitability`: fit for automated search, candidate generation, counterexample mining, or evaluator-driven optimization.
- `intellectual_interest`: general mathematical or algorithmic appeal.

Do not collapse these into one vibe score.

## Theorem-Project Workflow

Each theorem candidate should support this staged attack whenever possible:

1. Blind prompt: self-contained problem statement, no internet, no literature context, maximum reasoning effort.
2. Frontier document: curated known results, definitions, obstacles, and plausible lemmas.
3. Literature mode: broader source access after blind and frontier attempts stall.

The `blind_prompt.md` file must avoid accidentally smuggling in too much frontier knowledge unless explicitly marked as a non-blind variant.

## OpenEvolve Workflow

OpenEvolve candidates should identify an automated evaluator when possible, such as:

- exact small-instance oracle;
- exhaustive counterexample search;
- LP, SAT, SMT, or integer-programming relaxation;
- simulator with adversarial trace generation;
- potential-function inequality checker;
- benchmark against known lower bounds or certified constructions.

If no plausible evaluator exists yet, say so directly.

## Skeptical Audit Requirements

Every candidate needs an adversarial audit:

- Why might this not actually be open?
- Why might it be too saturated?
- Why might it be impossible to evaluate automatically?
- What would falsify our interest in it?
- Which primary sources must be checked before promoting it?

The audit is not decorative. It should be strong enough to downgrade or reject the candidate.

## File Conventions

- Use TODO markers instead of fabricated content.
- Keep source metadata in YAML files when possible.
- Prefer stable identifiers: DOI, arXiv, conference page, author page, or publisher URL.
- Record access dates for web sources once verified.
- Keep speculative ideas separate from sourced facts.
