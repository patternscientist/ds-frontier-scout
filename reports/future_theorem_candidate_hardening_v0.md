# Future-Theorem Candidate Hardening v0

Date: 2026-05-17.

Branch: `future-theorem-candidate-hardening-v0`.

Boundary: this hardens two later theorem-pilot options for future review. It is not a recommendation to replace or interrupt STT / DS(k,1).

## Files Patched

`path_compression_topdown`:

- `frontier.md`: added Seidel-Sharir's main dissection recurrence, rank-forest conventions, shifting lemma, `J_k` hierarchy, `S(m,n)`, and the Tarjan-style Ackermann normalization to compare against.
- `blind_prompt.md`: replaced the underspecified prompt with a self-contained recurrence-plus-Ackermann prompt that withholds the intended comparison proof.
- `sources.yaml`: added source metadata and a 24-month targeted freshness/search log.
- `skeptical_audit.md`: added a lecture-note audit covering Seidel/Princeton slides and Stanford CS166 2025 materials.

`karp_rabin_collision_detection`:

- `frontier.md`: added a precise variant note separating deterministic exact detection, randomized one-sided rejection/certification, and witness-finding versus decision.
- `blind_prompt.md`: restated the exact deterministic problem first, with randomized rejection only as an optional separate variant.
- `sources.yaml`: added source metadata and a 24-month targeted freshness/search log.
- `oracle_spec.md`: added a tiny brute-force oracle specification for small strings, bases, and prime moduli.
- `openevolve_fit.md` and `skeptical_audit.md`: clarified that the exact oracle is useful, but object-first OpenEvolve promotion still needs a concrete mutable object.

## Source/Freshness Summary

Path compression:

- Primary recurrence source checked: Seidel-Sharir 2005, DOI `10.1137/S0097539703439088`.
- Problem source checked: Tarjan's Dagstuhl 25191 note, section 5.3.
- Ackermann target source checked: Tarjan 1975, DOI `10.1145/321879.321884`.
- Recent/public lecture-note audit: Seidel/Princeton slides and Stanford CS166 2025 slides explain the top-down recurrence and inverse-Ackermann-style bounds, but the checked materials do not appear to contain the direct `J_k`-to-classical-Ackermann proof requested by Tarjan.

Karp-Rabin:

- Problem source checked: Farach-Colton's Dagstuhl 25191 note, section 5.5.
- Background fingerprint metadata checked: Karp-Rabin 1987, DOI `10.1147/rd.312.0249`.
- Targeted search did not find a closure of the exact all-length, fixed-prime collision-detection problem, but the terminology risk remains high enough to require a proper stringology sweep before any future promotion.

## Deferred Work

- No recurrence-table or inequality-checker script was added. The path-compression artifact is proof-comparison-shaped, and a tiny numeric table would be useful only after a candidate comparison lemma exists.
- No Karp-Rabin algorithmic search was implemented. The oracle spec is deliberately small and exact.
- Neither candidate is recommended as a replacement for the foreground STT / DS(k,1) proof lane.
