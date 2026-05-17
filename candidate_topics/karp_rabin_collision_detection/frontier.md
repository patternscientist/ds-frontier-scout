# Frontier

Status: hardened for future review, not promoted over the current STT / DS(k,1) lane.

## Source Anchor

Martin Farach-Colton posed the problem "Detecting collisions in Karp-Rabin fingerprinting" in Dagstuhl 25191. The report asks how quickly one can take a string and a prime and determine whether any two distinct same-length substrings have equal Karp-Rabin fingerprints. It records the straightforward quadratic-time route via suffix trees.

Primary source: Dagstuhl Seminar 25191 report, section 5.5.

## Working Notation

Let `S[0..n-1]` be a string over an integer alphabet. Let `b` be the fingerprint base; in the Dagstuhl wording this is the alphabet size. Let `p` be the given prime modulus. For a substring of length `ell` starting at `i`, fix one polynomial orientation and use it consistently, for example:

```text
H_p(i, ell) = sum_{t=0}^{ell-1} S[i+t] b^(ell-1-t) mod p.
```

A collision witness is a triple `(ell, i, j)` with `i != j`, `0 <= i,j <= n-ell`, such that:

```text
H_p(i, ell) = H_p(j, ell)
S[i..i+ell-1] != S[j..j+ell-1].
```

Equal substrings at different positions are not collision witnesses; their fingerprints agree for semantic reasons, not because the modulus created a false equality. Overlapping substrings are allowed.

## Variant Note

### Deterministic Exact Collision Detection

Input: `(S, b, p)`. Output `YES` iff a collision witness exists, and `NO` otherwise. A witness-finding version additionally returns `(ell, i, j)`.

This is the clean theorem-pilot variant. It has an exact small-instance oracle and no probabilistic escape hatch.

### Randomized One-Sided Rejection Variant

The Dagstuhl-source trail and local v2 audit record a relaxed certification variant in which an algorithm may reject some good moduli/polynomials with small probability. Keep this separate from exact detection.

For this folder, interpret the relaxed variant as a safety-certification problem with possible outputs:

```text
BAD(witness)     a real collision witness was found;
GOOD             the modulus/base is accepted as collision-free for S;
REJECT/UNKNOWN   the algorithm declines to certify this instance.
```

One-sidedness should mean that `GOOD` is never returned on a truly colliding instance, except within the explicitly stated error model, while `REJECT/UNKNOWN` may occur on truly collision-free instances. A future proof attempt must restate the exact probability space: over algorithmic randomness, over a random base/modulus choice, or over both.

### Witness-Finding Versus Decision

Decision asks only whether a witness exists. Witness-finding returns a checkable certificate `(ell, i, j)`. For future AI-assisted attacks, witness-finding is preferable because certificates are easy to verify and make small-instance regressions unambiguous.

Do not conflate:

- finding one collision witness;
- deciding whether any witness exists;
- certifying that no witness exists;
- rejecting a good modulus in a randomized certification routine.

## Small-Instance Oracle Hook

See `oracle_spec.md` for the deliberately tiny brute-force oracle specification. It is intended for test fixtures and counterexample mining only, not as an algorithmic-search implementation.
