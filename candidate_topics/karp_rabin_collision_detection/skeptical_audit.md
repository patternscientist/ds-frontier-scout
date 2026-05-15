# Skeptical Audit

Why this might not actually be open:

- The Dagstuhl statement is explicit, but the problem may appear in stringology under names such as collision-free fingerprint certification, bad modulus detection, or substring polynomial hash collision checking.
- A solution may exist for fixed length, random modulus, or restricted alphabets without settling the all-length deterministic problem.

Why this might be too saturated:

- Karp-Rabin hashing is ubiquitous, but this exact certification problem looks narrower than mainstream compressed-indexing/fingerprinting work.

Why automatic evaluation might fail:

- The problem statement allows rejecting some non-colliding primes/polynomials with small probability. This is not the same as exact collision detection.
- Exhaustive small strings and moduli are useful for algorithm testing, but may bias search toward arithmetic tricks that do not scale.
- Equal-length substrings must be enforced; mixing different lengths creates false witnesses.

What would falsify interest:

- A known suffix-array/number-theoretic algorithm already gives near-linear all-length detection for the exact same fixed-prime model.
- The only viable algorithms depend on bit-complexity assumptions not acceptable in the intended RAM model.

Primary sources to check before promotion:

- Martin Farach-Colton's Dagstuhl 25191 problem statement.
- Recent stringology papers using collision-free Karp-Rabin fingerprints, especially those that certify or derandomize the chosen modulus/base.
- Any notes/slides from the Dagstuhl talk with the omitted asymptotic target in the HTML.
