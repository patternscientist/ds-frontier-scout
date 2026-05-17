# Blind Prompt

You are given the following recurrence framework from a top-down analysis of path compression. Work without internet or literature context.

## Definitions

A rank forest is a rooted forest in which every node of rank `q` has, for each `0 <= i < q`, a child of rank `i`. Thus a rank forest with `n` nodes has maximum rank at most `floor(log_2 n)`.

Let `f(m,n,r)` be the maximum number of parent-pointer changes in any sequence of at most `m` non-rootpath compressions on a rank forest with at most `n` nodes and maximum rank at most `r`.

For a nondecreasing integer function `g` with `g(r) < r` for all `r > 0`, define:

```text
g*(r) =
  0                 if r <= 1,
  1 + g*(g(r))      if r > 1.

g^diamond(r) =
  g(r)                              if g(r) <= 1,
  1 + g^diamond(ceil(log_2 g(r)))   if g(r) > 1.
```

Assume the following shifting lemma:

```text
If f(m,n,r) <= k m + 2 n g(r) for all m,n,r,
then f(m,n,r) <= (k+1)m + 2 n g^diamond(r) for all m,n,r.
```

Define:

```text
J_0(r) = ceil((r - 1) / 2)
J_k(r) = (J_{k-1})^diamond(r)      for k > 0
S(m,n) = min { k in N : J_k(floor(log_2 n)) <= 1 + m/n }.
```

The recurrence already gives:

```text
f(m,n,r) <= k m + 2 n J_k(r),
f(m,n,r) <= (S(m,n) + 2)m + 2n.
```

Use this Ackermann normalization as the target:

```text
A(0,x) = 2x
A(i,0) = 0                         for i >= 1
A(i,1) = 2                         for i >= 1
A(i,x) = A(i-1, A(i,x-1))          for i >= 1 and x >= 2

alpha(m,n) = min { z >= 1 : A(z, 4 ceil(m/n)) > log_2 n }.
```

## Task

Give a simple direct proof that `S(m,n) = O(alpha(m,n))`, preferably with an explicit constant shift in the index. Conclude that path compression with linking by rank has total time `O(n + m alpha(m,n))`.

Do not introduce an unrelated fast-growing hierarchy unless you explicitly map it back to the `A(i,x)` normalization above. Do not assume the desired comparison between `J_k` and `A`; proving that comparison is the substance of the task.
