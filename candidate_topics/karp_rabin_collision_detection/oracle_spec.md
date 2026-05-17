# Tiny Brute-Force Oracle Spec

Purpose: exact small-instance checking only. Do not treat this as an attempted subquadratic algorithm.

## Inputs

- `S[0..n-1]`: integer string.
- `b`: fingerprint base, usually the alphabet size in the Dagstuhl formulation.
- `p`: prime modulus.

## Fingerprint

Use one fixed orientation:

```text
H_p(i, ell) = sum_{t=0}^{ell-1} S[i+t] b^(ell-1-t) mod p.
```

The reverse orientation is acceptable for experiments if every candidate algorithm and oracle uses the same convention.

## Exact Oracle

For every `ell = 1..n`:

1. Compute `H_p(i, ell)` for every start `i = 0..n-ell`.
2. Group starts by hash value.
3. Within each group, compare the actual substrings.
4. If two starts `i != j` have equal hash and unequal substring contents, return:

```yaml
answer: yes
witness:
  ell: <length>
  i: <start>
  j: <start>
  hash: <value mod p>
```

If no such pair exists, return:

```yaml
answer: no
```

## Edge Rules

- Equal substrings at different locations are not collision witnesses.
- Overlapping substrings are allowed.
- Length zero is excluded.
- The oracle should be deterministic and exhaustive for the chosen finite input.

## Exhaustive Fixture Mode

For tiny tests, enumerate all strings over alphabet `{0, ..., b-1}` up to a fixed `n_max` and all primes in a small list. Compare any candidate detector against the oracle on every `(S,b,p)`.

This fixture can validate definitions, catch off-by-one mistakes, and produce minimal witnesses. It cannot establish asymptotic progress.
