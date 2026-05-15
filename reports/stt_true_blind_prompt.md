# STT True Blind Prompt

You are studying the following self-contained problem. Do not use the internet,
papers, repository context, or prior conversations. Treat this as a clean-room
mathematical exploration.

Let `U` be an undirected tree whose vertices are searchable items. A search
tree on `U` is defined recursively:

1. Choose a root vertex `r` of the current connected subtree.
2. Remove `r`.
3. For each connected component left behind, attach to `r` a recursively built
   search tree for that component.

The resulting rooted tree has the same vertex set as `U`, but generally has a
different parent-child relation from `U`. Use root depth 0 for LP-style depth
vectors unless you explicitly state a different convention.

For a valid recursive search tree `T`, define its depth vector `d_T` by
`d_T(v) =` the number of strict ancestors of `v` in `T`. Given nonnegative
weights `w_v`, the weighted depth objective is

```text
sum_v w_v d_T(v)
```

Equivalently, if using ordinary search cost with root depth 1, add
`sum_v w_v` to this objective.

Main task:

Study the convex hull of all depth vectors of valid recursive search trees on
`U`, and look for natural linear or convex relaxations whose variables encode
relations such as ancestry, separation by recursive roots, component
decomposition, and depth.

Try to make progress from scratch on questions such as:

- Can the depth-vector hull be described by a compact linear program for
  useful families of base trees?
- Are there structural decompositions or dynamic programs that expose the hull
  recursively?
- Which inequalities are forced by the recursive root-choice definition?
- Can every optimum weighted depth vector be certified by local root-choice or
  exchange conditions?
- Are there small tree families where the hull admits a simple formula?
- Are there small instances showing that a tempting relaxation is too weak?

Suggested approaches:

- derive valid inequalities directly from the recursive definition;
- compare ancestry variables with depth variables;
- formulate separation or optimization over the depth-vector hull;
- search by hand on very small base trees;
- use dynamic programming, exchange arguments, or uncrossing-style reasoning;
- distinguish full integrality of an extended formulation from exactness of
  the best depth objective.

Report your work as a serious research attempt. State definitions precisely,
make all assumptions explicit, mark speculative ideas as speculative, and give
the smallest concrete examples you can compute by hand.
