# Frontier

Status: hardened for future review, not promoted over the current STT / DS(k,1) lane.

## Source Anchor

Robert E. Tarjan's Dagstuhl 25191 note asks for a simple direct proof that the Seidel-Sharir top-down path-compression recurrence implies the inverse-Ackermann upper bound when inverse Ackermann is defined via the classical Ackermann function.

Primary recurrence source: Raimund Seidel and Micha Sharir, "Top-Down Analysis of Path Compression," SIAM J. Comput. 34(3):515-525, 2005, DOI `10.1137/S0097539703439088`.

## Parameter Conventions

Seidel and Sharir reduce union-by-rank plus path compression to sequences of generalized path-compression operations on a fixed rank-balanced forest.

- A compression sequence `C` has length `|C|`, counting non-rootpath compressions only.
- `cost(C)` is the number of parent-pointer changes caused by all compressions in `C`.
- A rank forest is a rooted forest in which a node of rank `q` has, for every `0 <= i < q`, a child of rank `i`. Hence a rank forest on `n` nodes has maximum rank at most `floor(log_2 n)`.
- `f(m,n,r)` is the maximum possible `cost(C)` over compression sequences of length `m` in a rank forest with `n` nodes and maximum rank `r`.

This differs from the operational union-find input only by the standard reduction: after all union operations are fixed, find operations induce a sequence of path compressions. The final theorem adds the `O(m+n)` operational overhead.

## Main Dissection Recurrence

For a forest `F` with node set `X`, a dissection is a partition `(X_b, X_t)` such that `X_t` is upward closed. Seidel-Sharir's main lemma says that any compression sequence `C` on `F` induces compression sequences `C_b` and `C_t` on the bottom and top induced forests with

```text
|C_b| + |C_t| <= |C|
cost(C) <= cost(C_b) + cost(C_t) + |X_b| + |C_t|.
```

For rank forests, choose a separating rank `s`, let `X_{<=s}` be the bottom and `X_{>s}` be the top. Then:

```text
F(X_{<=s}) has maximum rank at most s,
F(X_{>s}) has maximum rank at most r - s - 1,
|X_{>s}| <= |X| / 2^(s+1).
```

This is the top-down recurrence skeleton. The later `J_k` hierarchy is a way to iterate it with a carefully chosen `s`.

## Shifting Lemma And `J_k`

Let `g: N -> N` be nondecreasing with `g(r) < r` for every `r > 0`. Define:

```text
g*(r) =
  0                 if r <= 1,
  1 + g*(g(r))      if r > 1.

g^diamond(r) =
  g(r)                              if g(r) <= 1,
  1 + g^diamond(ceil(log_2 g(r)))   if g(r) > 1.
```

The paper notes that `g^diamond` is essentially `(ceil(log_2) o g)*`.

Shifting lemma:

```text
If f(m,n,r) <= k m + 2 n g(r) for all m,n,r,
then f(m,n,r) <= (k+1)m + 2 n g^diamond(r) for all m,n,r.
```

The `J` hierarchy is:

```text
J_0(r) = ceil((r - 1) / 2)
J_k(r) = (J_{k-1})^diamond(r)      for k > 0.
```

Corollary:

```text
f(m,n,r) <= k m + 2 n J_k(r)       for all k,m,n,r.
```

Define:

```text
S(m,n) = min { k in N : J_k(floor(log_2 n)) <= 1 + m/n }.
```

Then Seidel-Sharir obtain:

```text
f(m,n,r) <= (S(m,n) + 2)m + 2n,
```

and therefore a union-find sequence with `m` find operations on `n` elements takes `O(n + m S(m,n))` time.

## Classical Ackermann Normalization For This Folder

For the future proof attempt, use Tarjan's 1975 Ackermann variant as the classical target unless a control-panel review chooses another normalization:

```text
A(0,x) = 2x
A(i,0) = 0                         for i >= 1
A(i,1) = 2                         for i >= 1
A(i,x) = A(i-1, A(i,x-1))          for i >= 1 and x >= 2
```

Tarjan's two-parameter inverse is recorded as:

```text
alpha(m,n) = min { z >= 1 : A(z, 4 ceil(m/n)) > log_2 n }.
```

The future theorem task is not to reprove Seidel-Sharir's `J`-based bound. It is to give a simple comparison proof that `S(m,n)` is bounded by a constant shift of this `alpha(m,n)` normalization, or to choose and justify an equivalent classical Ackermann normalization and prove the comparison cleanly.

## Current Proof-State Notes

- The exact data-structure theorem is not open; the open item is proof translation and exposition.
- The prompt should include the recurrence and the Ackermann target above, but should not include a proposed comparison map between `J_k` and `A`.
- A small recurrence table may be useful later, but it should only be used as a sanity check for candidate inequalities, not as evidence of the asymptotic proof.
