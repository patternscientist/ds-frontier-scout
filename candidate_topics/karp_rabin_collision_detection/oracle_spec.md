# Exact Oracle Spec v2

Purpose: exact finite checking only. Do not treat this as an attempted
subquadratic algorithm or as evidence that a restricted length set solves the
all-length problem.

## Inputs

```json
{
  "S": [integer characters],
  "base": "fixed integer base",
  "modulus": "fixed prime modulus"
}
```

`S` may also be supplied to the local Python oracle as an ASCII string, in which
case characters are converted with `ord`.

## Fingerprint

Use one fixed orientation:

```text
H_p(i, ell) = sum_{t=0}^{ell-1} S[i+t] b^(ell-1-t) mod p.
```

The reverse orientation is acceptable for experiments if every candidate algorithm and oracle uses the same convention.

## Exact Oracle

For every `ell = 1..n`, in increasing order:

1. Use prefix hashes and powers of `base mod modulus` to compute `H_p(i, ell)`
   for every start `i = 0..n-ell`.
2. Group starts by hash value.
3. Within each bucket, compare the actual substrings directly.
4. If two starts `i != j` have equal hash and unequal substring contents,
   return:

```json
{
  "has_collision": true,
  "witness": {"length": "ell", "i": "start", "j": "start", "hash": "value mod p"},
  "checked_lengths": "number of lengths inspected before returning",
  "notes": []
}
```

If no such pair exists, return:

```json
{
  "has_collision": false,
  "witness": null,
  "checked_lengths": "n",
  "notes": []
}
```

## Edge Rules

- Equal substrings at different locations are not collision witnesses.
- Overlapping substrings are allowed.
- Length zero is excluded.
- The oracle should be deterministic and exhaustive for the chosen finite input.
- A fixed input base and fixed input prime modulus are part of the instance; do
  not replace them with a fresh random choice.

## Exhaustive Fixture Mode

For tiny tests, enumerate all strings over alphabet `{0, ..., b-1}` up to a fixed `n_max` and all primes in a small list. Compare any candidate detector against the oracle on every `(S,b,p)`.

This fixture can validate definitions, catch off-by-one mistakes, and produce minimal witnesses. It cannot establish asymptotic progress.

## Local Implementation

- `scripts/karp_rabin_collision/oracle.py`: all-length oracle and independent
  brute-force pair enumerator for tests.
- `scripts/karp_rabin_collision/fixed_length.py`: fixed-length bucket detector
  using prefix hashes, with direct true-substring verification.
- `scripts/karp_rabin_collision/search_counterexamples.py`: finite searches for
  false reductions such as powers-of-two-only checks or small restricted length
  sets.
