# Blind Prompt

You are given a string `S[0..n-1]` over an integer alphabet, a fingerprint base `b`, and a prime modulus `p`. For a substring of length `ell` starting at `i`, define:

```text
H_p(i, ell) = sum_{t=0}^{ell-1} S[i+t] b^(ell-1-t) mod p.
```

A Karp-Rabin collision witness is a triple `(ell, i, j)` with `i != j`, `0 <= i,j <= n-ell`, such that:

```text
H_p(i, ell) = H_p(j, ell)
S[i..i+ell-1] != S[j..j+ell-1].
```

Equal substrings at different positions do not count as collisions. Overlapping substrings are allowed.

## Main Task

Design a deterministic algorithm asymptotically faster than the straightforward quadratic-time approach for deciding whether a collision witness exists. Ideally, return a witness when the answer is `YES`.

If you cannot give such an algorithm, identify a natural restricted variant, reduction, barrier, or fixed-length subproblem that clarifies why the all-length problem is difficult.

## Optional Relaxed Variant

After treating the deterministic exact problem, you may consider a randomized one-sided certification variant in which the algorithm is allowed to return `REJECT/UNKNOWN` on some collision-free instances with small probability. Keep this separate from exact decision. State the probability space and guarantee precisely.
