---
model_name: "GPT-5.5 Thinking"
reasoning_setting: "highest available / thinking"
date: 2026-05-15
clean_room_attestation: "No internet, no repository context, no literature notes, and no prior STT frontier context were used."
source_chat_title: "Recursive Search Tree Hull"
transcript_scope: "Full exported markdown transcript from initial true-blind prompt through current state at time of archival."
exported_at: "2026-05-15 17:08:46"
---

# Recursive Search Tree Hull

**Created:** 5/15/2026 16:09:22  
**Updated:** 5/15/2026 17:01:06  
**Exported:** 5/15/2026 17:08:46  
**Link:** [https://chatgpt.com/c/6a07a78f-ba64-83e8-befa-817c96e6d1f4](https://chatgpt.com/c/6a07a78f-ba64-83e8-befa-817c96e6d1f4)  

## Prompt:
5/15/2026, 4:09:19 PM

You are studying the following self-contained problem.



Do not use the internet, papers, repository context, or prior conversations. Treat this as a clean-room mathematical exploration.



Let `U` be an undirected tree whose vertices are searchable items. A search tree on `U` is defined recursively:

1. Choose a root vertex `r` of the current connected subtree.
2. Remove `r`.
3. For each connected component left behind, attach to `r` a recursively built search tree for that component.

The resulting rooted tree has the same vertex set as `U`, but generally has a different parent-child relation from `U`.

Use root depth 0 for LP-style depth vectors unless you explicitly state a different convention. For a valid recursive search tree `T`, define its depth vector `d_T` by:

```text
d_T(v) = the number of strict ancestors of v in T
```

Given nonnegative weights `w_v`, the weighted depth objective is:

```text
sum_v w_v d_T(v)
```

Equivalently, if using ordinary search cost with root depth 1, add `sum_v w_v` to this objective.

## Main task

Study the convex hull of all depth vectors of valid recursive search trees on `U`, and look for natural linear or convex relaxations whose variables encode relations such as ancestry, separation by recursive roots, component decomposition, and depth.

Try to make progress from scratch on questions such as:

- Can the depth-vector hull be described by a compact linear program for useful families of base trees?
- Are there structural decompositions or dynamic programs that expose the hull recursively?
- Which inequalities are forced by the recursive root-choice definition?
- Can every optimum weighted depth vector be certified by local root-choice or exchange conditions?
- Are there small tree families where the hull admits a simple formula?
- Are there small instances showing that a tempting relaxation is too weak?



Suggested approaches:

- derive valid inequalities directly from the recursive definition;
- compare ancestry variables with depth variables;
- formulate separation or optimization over the depth-vector hull;
- search by hand on very small base trees;
- use dynamic programming, exchange arguments, or uncrossing-style reasoning;
- distinguish full integrality of an extended formulation from exactness of the best depth objective.

Report your work as a serious research attempt. State definitions precisely, make all assumptions explicit, mark speculative ideas as speculative, and give the smallest concrete examples you can compute by hand.

## Response:
5/15/2026, 4:09:21 PM

> **Planning a deep analysis for search trees**
>
> I need to research and attempt an answer, without any outside resources. User clearly requested no prior context, so I’ll avoid that. Perhaps I could use some self-contained computation, like Python. The task involves studying convex hulls of depth vectors related to search tree polytopes, focusing on definitions, inequalities, dynamic programming, and small examples with weak relaxation. I'll start by defining the tree structure and its relevant constraints. This feels like a deep dive – let's proceed carefully!
>
> **Verifying tree recursive search conditions**
>
> For a recursive search tree, it’s a rooted tree where the endpoints of every edge in U must be comparable in the rooted structure. If a vertex x is the parent of y in the search tree, removing ancestors should leave y as the root of its own component. I’ll check if this makes sense for specific cases, like a 1-2-3 path. Let’s see if the conditions hold!
>
> **Exploring search tree depth optimization**
>
> I’m considering how to approach this search tree problem with computational examples. The goal is to optimize the weighted sum of depths, where the objective recursively chooses a root to minimize cost over components. I’ll define the possible depths and try a DP approach for connected subtrees. Calculating hull projection may need further decomposition. There’s a lot to process here!
>
> **Analyzing the computational complexity of recursion**
>
> I’m exploring the exactly recursive convex hull for a set of components and subtrees, and trying to assess the complexity. For arbitrary trees, the number of connected sub
>
> **Understanding ancestor selection in recursive search trees**
>
> In a recursive search tree, choosing a root determines ancestor relationships between vertices. If root choice splits the tree, the first root selected on the path between two vertices u and v defines which one is the ancestor. If u is selected before v, then u is an ancestor of v, and vice versa.
>
> **Clarifying the path-earliest characterization and constraints**
>
> The path-earliest characterization is key here. We define a variable for each pair of vertices on the path between them, ensuring one vertex is always chosen first. The "earliest" vertex enforces a clear ancestor relationship. I’m considering enforcing consistency via constraints for stronger relations, such as “betweenness."
>
> **Examining ancestor relationships and constraints**
>
> For a connected subtree \( S \), when the root is chosen, all vertices in \( S \) are descendants of it. For each vertex \( v \) in \( S \), it has at least one ancestor inside \( S \). Thus, the sum of all depths should be at least \( |S| - 1 \), meaning that each vertex has some ancestor in \( S \). This holds for star-shaped trees or paths.
>
> **Refining ancestor constraints with weights and forests**
>
> For any connected subtree \( S \), the sum of depths \( d_v \) is at least \( |S| - 1 \), reflecting the number of ordered ancestor pairs within \( S \). In a disconnected set \( A \) with \( c \) components
>
> **Testing depth vector inequalities on paths**
>
> I’m exploring depth vectors for a search tree on a simple path. The depths can range from 0 to \( n(n-1)/2 \). I’ve been testing for path structures like 1-2-3 and noting the depth sums for different root choices. The comparison suggests that \( \sum_{i \in S} d_i \geq |S| - 1 \) works for some intervals. However, checking the hull reveals some pairwise sums that don't satisfy it. I'll need to refine this further.
>
> **Checking if (0,1,1) is a linear combination**
>
> I’m testing if the vector (0,1,1) can be written as a combo of others like A(0,1,2), B(0,2,1), etc. The conditions just don't add up; solving gives a contradiction. Next, I’ll look into the convex hull facets for these vectors — maybe try using Python and scipy to calculate them by hand later.
>
> **Computing convex hull facets**
>
>
> **Generating search tree depth vectors**
>
> I’m starting to compute the depth vectors for search trees recursively. Looks like it's time to write the code for this. I’ll set up the base tree first, then work on applying recursion to generate the depth vectors. Let's get the nuts and bolts sorted out in the code.
>
> **Generating recursive search tree depth vectors**
>
>
> **Considering path Catalan and hull facets**
>
> I’m thinking about this path Catalan situation. I need to consider the hull facets, especially because the points might lie in a full-dimensional space. For n=3, are the points considered full-dimensional? Alright, I’ll need to look into the convex hull and check how it fits.
>
> **Computing convex hull facets and vertices**
>
>
> **Exploring inequalities for the n=3 hull**
>
> I'm digging into the equations for decoding facets when n=3. I need to check inequalities like d1+d3 ≤ 2, 2d1+d2+d3 ≥ 3, and others. Some vertices sum to 2 or 3, and the sum should be ≤ 3. I'll also verify if the non-negative constraints are being met and what the exact facets are. It seems there's complexity due to degeneracy.
>
> **Exploring depth vectors and star structure**
>
> I’m thinking through the depth vectors in a star structure. Leaves before the center form a chain above it, with ordered depths, while others have a depth of k+1. The center has depth k. I can describe this structure by the ordering of leaves, with each leaf’s depth either being before, during, or after the center’s position.
>
> **Defining depth hull for a star and recursive search trees**
>
> I’m considering how to define the depth hull for a star structure, with a focus on leaves. If a leaf is after the center, I set its depth as d_c + 1, and if before, it's based on its position in the ordering. Also, I wonder about recursive search trees and if every permutation can represent one. Yes, multiple permutations can generate a valid search tree.
>
> **Representing search tree depth using permutations**
>
> I'm thinking about using a chain of components to represent how nodes relate in a search tree. Each vertex's depth is equivalent to counting how many previous vertices are "earliest" on a specific path, following a permutation order. This depth hull could be framed as a convex combination of depth vectors from different permutations, with potential for linear programming formulation using variables for each path.
>
> **Formulating depth constraints for tree edges**
>
> I’m considering how to impose depth constraints based on how edges are oriented in a tree. If I require each child depth to be one greater than its parent's, I can represent this with constraints. However, the path structure might allow invalid configurations (like (0, 1, 1) for path 3), so I need to refine these constraints to rule out such cases.
>
> **Calculating exact hull and verifying facets for Path3**
>
> I’m considering how to derive the exact convex hull for Path3 and Star2. For Path3, I want to avoid overcomplicating, so I’ll focus on presenting a simple formula using the listed vertices. I need to verify the facets and inequalities, checking the computation for exactness by ensuring all vertices are satisfied and facets are correct.
>
> **Evaluating convex hull facets for path3 graph**
>
>
> **Verifying facets and polytope structure**
>
> I’m going through the facets, verifying inequalities like 2d1+d2+d3 ≥ 3, and checking if the polygons hold up. There’s a quadrilateral (ABDE) and other facets like ACE, BCD, and CDE. It looks like the computational hull counted 6 facets, but only 5 are valid once duplicates are handled.
>
> **Exploring facet generation and LP formulation**
>
> I'm deriving facets recursively by splitting the root. For example, in P3 (1-2-3), the root cases give vectors like (0,1+x, 1+(1-x)), and I check inequalities like 2d1+d2+d3≥3. For the star graph, it might use a similar approach, and then I'll explore an LP formulation using λ variables for precise hull construction.
>
> **Formulating depth coordinates and constraints**
>
> I’m constructing a compact formulation for depth coordinates, using λ, μ variables. For any interval containing vertex v, I'm tracking the ancestor roots, considering conditions where roots contribute to the depth. This results in a compact formulation, with variables scaling as O(n^3) for λ and O(n^2) for μ, efficient for paths and generalizable to trees with connected subproblems.
>
> **Proving integrality of flow structure**
>
> I'm working on proving the integrality of a flow in the polytope defined by μ and λ. The key challenge is checking whether fractional solutions are valid convex combinations of search trees, as flow copies mass to child subproblems. By showing that any feasible solution corresponds to a random search tree, I can confirm that this is an exact convex hull, but the integrality may only hold for deterministic root policies.
>
> **Examining optimization and Bellman’s criteria**
>
> I’m thinking about a weighted optimization problem where I minimize a weighted objective via expected depth. The recursion matches the formula well, where each root adds one depth to every vertex in its subproblem.
>
> **Formulating valid inequalities for compact paths**
>
> I'm focusing on deriving valid inequalities for the problem. The goal is to certify certain conditions, like ensuring that root choices satisfy equality when minimizing the function Q_S(r). I can define a dual certificate using potentials α_S, and build inequalities based on conditions like nonnegativity, integrality bounds, and ancestor counts for the forest bound. This helps tighten the convex hull representation.
>
> **Deriving depth based on connected sets**
>
> I'm trying to figure out if a vertex q can have depth 0 by using connected sets. One approach is to apply the forest
>
> **Linearizing inequalities for connected sets**
>
> I’m trying to express linear inequalities for a connected set \( S \). The goal is to capture conditions like the minimum depth over vertices in \( S \). By fixing certain values, I can linearize the nonlinear terms. For example, I prove that the sum of depths \( d_v \) should always satisfy certain bounds, based on whether vertices are roots or not. This approach simplifies the complexity for certain types of subsets.
>
> **Finding recursive lower bounds and inequalities**
>
> I’m working on deriving a recursive lower bound for connected sets and how the depths of various connected components relate when split. When fixing a root \( q \) in \( S \), I'm calculating lower bounds based on components and edge counts. This leads me to a valid inequality that describes the sum of depths relation to the structure of the tree.
>
> **Proving inequalities with recursive lower bound**
>
> I’m proving cases for the inequalities based on whether \( q \) is the first vertex in \( S \) or not, and how the depths for each component relate. I then calculate the sum of depths and show that it satisfies the bounds, using components and the degrees of vertices. This results in a recursive lower bound.
>
> **Deriving search tree inequalities**
>
> I’m thinking about deriving multi-step inequalities for connected search trees, focusing on simplifications like the sum of depths for path-based structures. For example, in a path with vertices in different branches, I want to explore conditions where the sum of depths is constrained, like in the case for P3.
>
> **Evaluating depth sum of path endpoints**
>
>
> **Exploring maximum depth sum for path endpoints**
>
> I'm looking at a scenario for any pair of vertices, where the sum of their depths might be constrained by external branches and common ancestors. In a path, the maximum depth sum is related to both the path's length and the vertices outside it. I'm thinking about a formula for this scenario.
>
> **Refining upper bound for depth sum and testing potential approaches**
>
> I'm working through an upper bound for the sum of depths of two vertices, considering path vertices and outside ancestors. I have a formula, but it's not quite tight. There's also the question of exploring optional methods, like using non-negative weights to potentially improve the bound – though this might be too low. Looking for better bounds.
>
> **Exploring weights and forest relaxation impact**
>
> I'm testing different weight combinations, like setting a large number for one and smaller ones for others. It seems that a certain weight setup doesn't change the objective much. However, when using a large value and relaxing the forest, I realize it leads to inaccurate objectives compared to the actual costs.
>
> **Deriving maximum pair sum for path endpoints**
>
>
> **Formulating component decomposition with variables**
>
> I'm working on defining variables for component decomposition. For each nonempty connected subset, I’ll set variables like μ_S ≥ 0 and λ_{S,r} ≥ 0. The constraints include: μ_V = 1, and for each subset S, the lambda sums up correctly. The goal is to prove that the projection matches the hull by detailing the recursive decomposition and ensuring constraints hold.
>
> **Optimizing leaf order and prefix selection**
>
> I’m thinking about how to order the leaves for a fixed set of size k. To minimize weighted depth, the heavier leaves should come earlier. For the center position, I’m comparing placing a leaf before or after it. I’m considering the convex hull of the prefix-order vectors, which likely extends via the permutahedron, with specific ranks assigned to leaves.
>
> **Exploring convex hulls and permutahedra for leaf assignments**
>
> I’m considering the convex hull of a permutahedron with fixed values for leaf depths, which suggests the use of a multiset and sorting. For a fixed size k, the convex hull seems to be a union of permutahedra. I’m thinking about applying majorization and exploring sorting networks for optimization, though it might be a bit too complex. A simplified version might involve weighted optimization, using sorted leaves and compact formulations.
>
> **Weighting optimization and compact formula**
>
> I’m considering exact optimization for weighted depth, where the smallest depths go to the largest weights. For fixed k, the formula looks tidy: I minimize the weighted sum by sorting weights and assigning them accordingly. The algorithm seems efficient, with O(m log m) complexity. After this, I can explore the exact structure of a star-shaped hull in a permutahedron for further refinement.
>
> **Exploring subtree structures and constraints**
>
> I’m considering trees with polynomially many connected subtrees — paths and possibly any tree with O(poly) connected subtrees, depending on fixed leaf numbers. There are also variables like m for subtree separators that could help define constraints. However, simply using pairwise distributions might not be enough, as it could cause invalid depths. I’ll have to test this further.
>
> **Clarifying pair relationships and ancestor contributions**
>
> I’m exploring how to assign contributions to pairs based on ancestor relationships. For instance, m_{1|12} means 1's ancestor contributes a value to d2. But when considering paths, I notice that having the earliest node in the path affects how ancestors are counted. The pairwise approach misses some key separator details like when 2 is the earliest ancestor on a path. I need consistency across paths to account for this properly.
>
> **Enforcing consistency in ancestor relations**
>
> I’m checking if having the earliest node on a path also means it’s the earliest on any subpath, which seems necessary for enforcing ancestor relations. I'll introduce subpath consistency as an extra condition to strengthen the logic. Also, I'll mark the transitivity and other relations as speculative for now.
>
> **Clarifying ancestor relationships and constraints**
>
> I’m exploring how ancestors are related in a tree structure. If node u is an ancestor of v, and x lies between them on the path, does u also become an ancestor of x, and is x an ancestor of v too? I need to refine the constraints to account for non-ancestor cases in internal paths.
>
> **Refining ancestry constraints in trees**
>
> I believe that if u is an ancestor of v, then every internal x must either have u as its ancestor or not. This leads to the conclusion that u must be an ancestor of x. This implies strong constraints: u being an ancestor of v forces u to be the ancestor of all vertices along the path.
>
> **Investigating ancestry constraints for search trees**
>
> I’m trying to explore if a root node (r) can be considered the ancestor of all other nodes based on edge comparability/path closure. If r is an ancestor of one neighbor, it might be an ancestor of all. I’m also looking into properties like partial order, edge comparability, and path closure, testing if these constraints are sufficient for constructing a valid search tree.
>
> **Exploring the ancestral relationship in recursive search trees**
>
> I’m wondering whether any integral set satisfying ancestry relations forms a valid recursive search tree. If I construct a rooted tree or poset, I need each non-root node to have a unique parent, but partial orders could allow exceptions. There’s also a question about edge comparability and whether ancestors must always be comparable. It’s not entirely clear yet.
>
> **Refining the tree structure and ancestor relations**
>
> I’m thinking about properties of ancestors, where x and y both are ancestors of v and comparable. I can set up a partial order for these situations, ruling out counterexamples like a star. I’m also exploring how the path closure and edge comparability might help with constructing a rooted tree and ensuring uniqueness, which seems plausible for recursive validity.
>
> **Testing linear programming for ancestry relaxation**
>
> I'm thinking about how small fractional points could violate the hull in the ancestry relaxation. To tackle this, I could solve the problem by projecting the constraints through linear programming. I'll try using random weights and comparing the optimization results on the P3 and P4 hulls, testing the LP relaxation's accuracy.
>
> **Building and solving ancestry linear programming relaxation**
>
>
> **Examining LP relaxation for ancestry constraints**
>
> Okay, the LP relaxation of the exact integer ancestry constraints seems too weak for the objective. A good next step is to focus on the P3 solution with weights w=(10,1,1). I'm wondering if this will yield d. It's worth checking to see if it provides a feasible solution.
>
> **Evaluating P3 solution for ancestry constraints**
>
>
> **Analyzing fractional LP relaxation for ancestry constraints**
>
> Interesting, the solution with d=(0,1.5,1) and cost 2.5 seems to violate the hull. I checked the P3 facets and it satisfies ancestry LP fractionally, providing a small counterexample. It satisfies transitivity and edge comparability. However, the true optimum cost is 3, showing that the LP relaxation is too weak.
>
> **Continuing research and crafting detailed lemmas**
>
> I’m deciding whether to use a math widget, but it seems unnecessary since the equation isn’t central. Maybe it would be useful for dynamic programming later, but for now, I’ll avoid it. Instead, I’ll focus on detailing the lemmas for my research, starting with the elimination-order lemma. It defines a recursive tree based on a total order, ensuring that parents come before descendants.
>
> **Clarifying proof and separation variables**
>
> The proof shows that if \( u \) is the earliest on the path, then \( u \) is an ancestor of \( v \). I’m establishing separation variables, defining \( y^r_{st} = 1 \) if \( r \) is the earliest on the path and ensuring the sum of them equals 1. For the depth, I'm accumulating these values for ancestors of \( v \). I still need to handle cases where \( r \) isn’t directly counted.
>
> Thought for 5m 12s

I’ll treat this as a clean-room math exploration and work from the recursive definition only. I’m going to build basic equivalent characterizations, compute small hulls, then test a few natural relaxations against tiny counterexamples.

A useful clean-room reduction is emerging: a search tree can be generated from a permutation by repeatedly choosing the earliest remaining vertex in each connected component. In that view, “$u$ is an ancestor of $v$” means $u$ is the earliest vertex on the base-tree path from $u$ to $v$.

Below is a clean-room research attempt.

# 1. Basic reformulation: search trees from permutations

Let $U=(V,E)$ be the base tree. A useful equivalent view is:

Given any total order $\prec$ on $V$, build a recursive search tree by choosing, in every current connected component, the $\prec$-earliest vertex as the root of that component.

Conversely, every valid recursive search tree arises from at least one such total order: take any linear extension in which ancestors come before descendants.

The key lemma is:

**Path-earliest lemma.** For distinct $u,v\in V$, $u$ is an ancestor of $v$ in the search tree induced by $\prec$ iff $u$ is the $\prec$-earliest vertex on the unique base-tree path $P_U(u,v)$.

Proof sketch: if some path vertex $x\neq u$ is chosen earlier than $u$, then $x$ separates $u$ from $v$ before $u$ can become an ancestor of $v$. If $u$ is earliest on the whole path, then when $u$ is chosen, $v$ is still in the component below $u$.

Thus, if we introduce ancestry variables

$$
a_{uv}=1 \quad\Longleftrightarrow\quad u\text{ is an ancestor of }v,
$$

then

$$
d(v)=\sum_{u\neq v} a_{uv}.
$$

The hard part is not the depth formula; it is enforcing that the $a_{uv}$’s come from one globally consistent recursive decomposition.

---

# 2. Exact recursive hull decomposition

For every nonempty connected $S\subseteq V$, let $P(S)$ be the convex hull of local depth vectors of valid recursive search trees on the induced subtree $U[S]$, with the root of that local search tree at depth $0$.

Then the recursive definition gives an exact convex recursion:

$$
P(S)
=
\operatorname{conv}_{r\in S}
\left\{
x\in \mathbb{R}^S:
x_r=0,\;
x_C=\mathbf{1}_C+y^C\text{ for every component }C\text{ of }S-r,\;
y^C\in P(C)
\right\}.
$$

This is already a complete structural description. It says: choose the first root $r$; every remaining vertex gets depth $+1$; then recurse independently on each component.

A more LP-like extended formulation is as follows.

Let $\mathcal C(U)$ be the set of nonempty connected vertex subsets of $U$. Introduce variables

$$
\mu_S\ge 0 \qquad (S\in\mathcal C(U)),
$$

interpreted as the probability that $S$ appears as a recursive subproblem, and

$$
\lambda_{S,r}\ge 0 \qquad (S\in\mathcal C(U),\ r\in S),
$$

interpreted as the probability that $S$ appears and chooses root $r$.

The constraints are:

$$
\mu_V=1,
$$

$$
\sum_{r\in S}\lambda_{S,r}=\mu_S
\qquad\text{for every }S\in\mathcal C(U),
$$

and, for every $S\neq V$,

$$
\mu_S
=
\sum_{\substack{R\in\mathcal C(U),\ q\in R:\\ S\text{ is a component of }R-q}}
\lambda_{R,q}.
$$

The depth projection is

$$
d_v
=
\sum_{\substack{S\in\mathcal C(U):\\ v\in S}}
\sum_{\substack{r\in S:\\ r\neq v}}
\lambda_{S,r}
=
\sum_{\substack{S\in\mathcal C(U):\\ v\in S}}
(\mu_S-\lambda_{S,v}).
$$

This formulation is exact: every distribution over recursive search trees gives such $(\mu,\lambda)$, and every feasible $(\mu,\lambda)$ defines a randomized recursive root-choice policy.

So the depth-vector hull is the projection of this linear system.

The catch is size. For a path, $\mathcal C(U)$ has only $O(n^2)$ intervals, giving a compact LP. For a general tree, $\mathcal C(U)$ can be exponential.

---

# 3. Exact weighted optimization and local certificates

Let $W(S)=\sum_{v\in S}w_v$. The weighted depth objective satisfies the dynamic program

$$
F(S)
=
\min_{r\in S}
\left[
W(S)-w_r
+
\sum_{C\in \operatorname{comp}(S-r)} F(C)
\right],
$$

with $F(\{v\})=0$.

Reason: choosing $r$ as the root of $S$ adds $1$ to the depth of every vertex in $S\setminus\{r\}$, contributing $W(S)-w_r$, then recurses on the components of $S-r$.

A recursive search tree is optimal iff every root choice $r$ used at every subproblem $S$ attains the above minimum. Thus an optimum can be certified locally by giving the values $F(S)$ and checking, at each chosen subproblem,

$$
F(S)
=
W(S)-w_r
+
\sum_C F(C).
$$

This gives a clean local root-choice certificate, although it may be exponentially large unless the family of subproblems is compact.

---

# 4. General valid inequalities

## 4.1 Forest lower bounds

For every $A\subseteq V$,

$$
\sum_{v\in A} d_v \ge |E(U[A])|.
$$

Since $U[A]$ is a forest, $|E(U[A])|=|A|-\kappa(A)$, where $\kappa(A)$ is the number of connected components of $U[A]$.

Proof idea: in each connected component of $U[A]$, the first chosen vertex has no ancestor inside that component, but every other vertex has at least one ancestor inside that component. Therefore at least $|A|-\kappa(A)$ internal ancestor incidences are forced, and global depths only count more ancestors.

For connected $S$, this says

$$
\sum_{v\in S} d_v \ge |S|-1.
$$

## 4.2 One-step strengthened connected-set inequality

Let $S\subseteq V$ be connected and let $q\in S$. Write

$$
e_q(S)=|E(U[S-q])|=|S|-1-\deg_{U[S]}(q).
$$

Then

$$
\sum_{v\in S} d_v + e_q(S)d_q
\ge
|E(U[S])|+e_q(S).
$$

Equivalently,

$$
\sum_{v\in S} d_v
+
\bigl(|S|-1-\deg_{U[S]}(q)\bigr)d_q
\ge
2|S|-2-\deg_{U[S]}(q).
$$

For a path $1-2-3$, taking $S=\{1,2,3\}$ and $q=1$ gives

$$
2d_1+d_2+d_3\ge 3.
$$

This inequality already cuts off a tempting but invalid point $(0,1,1)$.

---

# 5. Small exact examples

## 5.1 Single edge

For $U$ equal to one edge $1-2$, the possible depth vectors are

$$
(0,1),\qquad (1,0).
$$

Hence

$$
P(U)=\operatorname{conv}\{(0,1),(1,0)\}
=
\{d\ge 0:\ d_1+d_2=1\}.
$$

## 5.2 Three-vertex path

Let $U$ be the path $1-2-3$. The valid depth vectors are

$$
(0,1,2),\quad
(0,2,1),\quad
(1,0,1),\quad
(1,2,0),\quad
(2,1,0).
$$

Thus

$$
P(U)=
\operatorname{conv}
\{
(0,1,2),
(0,2,1),
(1,0,1),
(1,2,0),
(2,1,0)
\}.
$$

One exact halfspace description is:

$$
2d_1+d_2+d_3\ge 3,
$$

$$
d_1+d_2+2d_3\ge 3,
$$

$$
2d_1+d_2+2d_3\ge 4,
$$

$$
d_1+d_3\le 2,
$$

$$
d_1+d_2+d_3\le 3.
$$

This example is already useful because the naive forest inequalities do not describe the hull.

---

# 6. Path case: compact LP

If $U=P_n$ is a path, connected subtrees are intervals $[i,j]$. The exact $(\mu,\lambda)$-formulation above becomes polynomial size.

Variables:

$$
\mu_{i,j}
\qquad 1\le i\le j\le n,
$$

$$
\lambda_{i,j,r}
\qquad i\le r\le j.
$$

Constraints:

$$
\mu_{1,n}=1,
$$

$$
\sum_{r=i}^j \lambda_{i,j,r}=\mu_{i,j},
$$

and interval-flow constraints saying that $[a,b]$ appears when it is the left or right component created by a parent interval’s root choice.

The depth projection is

$$
d_v
=
\sum_{\substack{i\le v\le j}}
(\mu_{i,j}-\lambda_{i,j,v}).
$$

There are $O(n^2)$ interval variables $\mu$ and $O(n^3)$ root-choice variables $\lambda$. So paths admit a compact exact extended formulation.

This is essentially the convex-hull version of the usual interval dynamic program.

---

# 7. Star case: simple vertex formula

Let $U$ be a star with center $c$ and leaves $L$, $|L|=m$.

A search tree has the following form:

1. Choose some ordered prefix of leaves
   $$
   \ell_1,\ldots,\ell_k.
   $$
2. Then choose the center $c$.
3. All remaining leaves become children below $c$.

The depth vector is:

$$
d_{\ell_i}=i-1
\qquad (1\le i\le k),
$$

$$
d_c=k,
$$

$$
d_\ell=k+1
\qquad (\ell\notin\{\ell_1,\ldots,\ell_k\}).
$$

Therefore the star hull is

$$
P(U)
=
\operatorname{conv}_{0\le k\le m}
\left(
\{d_c=k\}
\times
\operatorname{Perm}
\{0,1,\ldots,k-1,\underbrace{k+1,\ldots,k+1}_{m-k\text{ times}}\}
\right),
$$

where $\operatorname{Perm}(M)$ denotes the permutahedron generated by assigning the multiset $M$ to the leaves.

For weighted optimization, sort leaf weights in decreasing order,

$$
w_{\ell_1}\ge w_{\ell_2}\ge \cdots \ge w_{\ell_m}.
$$

For fixed $k$, the best ordered prefix uses the $k$ heaviest leaves first, in decreasing weight order. The cost is

$$
w_c k
+
\sum_{i=1}^k w_{\ell_i}(i-1)
+
\sum_{i=k+1}^m w_{\ell_i}(k+1).
$$

Then minimize over $k=0,\ldots,m$.

So stars have an explicit hull description as a convex hull of permutahedra, plus a very simple optimization rule.

---

# 8. Tempting relaxations that are too weak

## 8.1 Forest inequalities alone are too weak

For the path $1-2-3$, the point

$$
d=(0,1,1)
$$

satisfies all forest lower bounds:

$$
d_1+d_2\ge 1,\qquad d_2+d_3\ge 1,\qquad d_1+d_2+d_3\ge 2.
$$

But $d=(0,1,1)$ is not in the hull.

Reason: $d_1=0$ forces vertex $1$ to be the root. Then the remaining subproblem is the edge $2-3$, so one of vertices $2,3$ must have depth $1$ and the other depth $2$. They cannot both have depth $1$.

With weights $w=(M,1,1)$, $M\ge 2$, this relaxation gives value $2$, but the true optimum is $3$.

## 8.2 Natural ancestry LP relaxation is also too weak

Consider variables $a_{uv}\in[0,1]$, intended to mean “$u$ is an ancestor of $v$.” Natural constraints include:

$$
a_{uv}+a_{vu}\le 1,
$$

edge comparability

$$
a_{uv}+a_{vu}=1 \qquad \{u,v\}\in E,
$$

transitivity

$$
a_{uv}+a_{vw}-1\le a_{uw},
$$

ancestor-chain consistency

$$
a_{xv}+a_{yv}-1\le a_{xy}+a_{yx},
$$

and path-prefix closure: if $x$ lies internally on $P_U(u,v)$, then

$$
a_{uv}\le a_{ux}.
$$

As an integer formulation, this is a plausible exact encoding of recursive ancestry. But its LP relaxation is not exact.

On the path $1-2-3$, the following fractional assignment is feasible:

$$
a_{12}=1,
$$

$$
a_{13}=\frac12,
$$

$$
a_{23}=\frac12,
$$

$$
a_{32}=\frac12,
$$

with all other $a_{uv}=0$.

Then

$$
d_1=0,\qquad d_2=a_{12}+a_{32}=\frac32,\qquad d_3=a_{13}+a_{23}=1.
$$

So the LP relaxation permits

$$
d=(0,\tfrac32,1).
$$

But this violates the true hull inequality

$$
2d_1+d_2+d_3\ge 3,
$$

because

$$
0+\frac32+1=\frac52<3.
$$

With weights $w=(M,1,1)$, $M\ge 2$, the fractional solution has cost $2.5$, while the true optimum is $3$.

So even a fairly strong-looking ancestry relaxation fails on the smallest nontrivial path.

---

# 9. Main takeaways

The cleanest exact object is the connected-subproblem flow formulation:

$$
\mu_S,\lambda_{S,r}.
$$

It exactly describes the hull after projection and gives an exact dynamic program for weighted optimization. It is compact for paths and any family with polynomially many connected induced subtrees, but can be exponential for general trees.

The most useful primitive structural facts are:

$$
u\text{ ancestor of }v
\iff
u\text{ is earliest on }P_U(u,v),
$$

and

$$
d_v=\sum_{u\neq v} a_{uv}.
$$

The most basic valid depth inequalities are forest lower bounds,

$$
\sum_{v\in A} d_v\ge |E(U[A])|,
$$

but these are far from sufficient. Already $P_3$ needs stronger recursive inequalities such as

$$
2d_1+d_2+d_3\ge 3.
$$

For small families:

- edges are trivial;
- paths admit an exact compact interval LP;
- stars admit an explicit permutahedral formula;
- $P_3$ already shows that local depth or ancestry relaxations can be too weak.

The next natural research direction would be to search for a polynomial-size formulation between the full connected-subproblem LP and the weak ancestry LP: something that enforces enough path-earliest consistency to recover the true depth hull, at least for broader tree classes than paths and stars.

## Prompt:
5/15/2026, 4:16:38 PM

Keep going.

## Response:
5/15/2026, 4:16:43 PM

> **Continuing clean-room math investigation**
>
> I need to continue the math problem without using the web, as the user asked. We should dive deeper, staying within the existing framework. I’ll focus on integer ancestry, inequality exploration, and possibly some compact LP modeling. Let’s think through tree structures and break down the problem — verifying any previous steps and ensuring correctness inside the clean-room at this stage.
>
> **Deriving inequalities using convex hulls and recursion**
>
>
> **Exploring search tree depth vectors**
>
> I’ll try enumerating the search tree depth vectors, focusing on paths. For path n, we should explore how permutations might relate to Catalan numbers. Depth vectors could lead to duplicates, so I'll account for that when implementing. Let’s also make sure the approach is general enough to extend.
>
> **Enumerating search tree depth vectors**
>
>
> **Enumerating search tree depth vectors**
>
>
> **Deriving P4 facets using ConvexHull**
>
> I need to derive the P4 facets and check if the points span the full dimension. For n=4, the dimension might be 4, and I can use convex hull computations for that. I'll aim to compute normalized integer coefficients and examine the facets. In P3, dimension 3 seemed correct with 5 points, so for P4 I expect 14 points in R4. Let's get those facets.
>
> **Computing convex hull facets and inequalities**
>
>
> **Creating unique integer inequalities**
>
> I need to generate unique integer inequalities and normalize them. The format I’m aiming for is \( \text{Eq normal} \times x + \text{offset} \leq 0 \), using rational approximations for coefficients. I'll employ fractions to keep everything precise and ensure there are no duplicates. Let’s proceed with deduplication as well.
>
> **Normalizing and deduplicating integer inequalities**
>
>
> **Finding exact integer normals for facets**
>
> I noticed that rational approximation didn’t work well for normals like square root proportions, so I’ll need to derive the exact normals by looking at facets formed from sets of points. For 4D, facets are defined by at least 4 affinely independent points, so I’ll enumerate combinations and identify the supporting hyperplanes. The goal is to compute unique exact normals.
>
> **Enumerating exact facets from point sets**
>
>
> **Interpreting inequalities and adjusting for facets**
>
> I need to interpret inequalities like \(a \cdot x \leq b\), especially when the coefficients are negative. This might give me lower bounds. To make the presentation nicer, I could flip the inequality to show the positive right-hand side. For exact facets, I can convert lower bounds by multiplying by -1 so the inequalities become \( \geq \).
>
> **Formatting and interpreting inequalities with bounds**
>
>
> **Deriving recursive inequalities for facets**
>
> Facets are numerous, and the exact P4 hull might be too complex, but I could highlight it. I need to derive a family of recursive inequalities that explain some facets. In P4, inequalities like \(d1 \geq 0\) and \(d4 \geq 0\) are simple, but I want to explore "root-forcing inequalities." I can formulate these recursively for any connected \(S\) and q. The goal is to create a generalized lifted inequality that is conditional. Let’s figure this out using any valid component inequality.
>
> **Formulating inequalities for root and non-root cases**
>
> If q is the root of S, the depth vector for S has \(d_q = 0\), and for each component C of S-q, \(d_v = 1 + local\). Then, for any search tree on S, the inequality is: \(\sum_S d + e_q d_q \geq |E(S)| + e_q\), where \(e_q = E(S-q)\). This generalizes by adding a coefficient for non-root q while ensuring validity. For components, lifting the coefficient corresponds to the maximum violation.
>
> **Analyzing cost distribution and edge relationships**
>
> Let's formalize how "shallow q pays component costs". If q has depth t, does each edge in S-q require an internal ancestor unless both endpoints are descendant-path ancestors? For connected S, removing q results in e_q edges in components. For any edge {x, y}, if q isn't on path x-y, the early ancestor of x or y serves as the ancestor, correlating incidences.
>
> **Analyzing ancestor pair sums and inequalities**
>
> Summing depths over S counts all ancestor pairs within S, which should be at least |E(S)|, with a lower bound for forests. Adding e_q d_q helps because for each edge in S-q, we can potentially charge either an internal comparable pair or the depth of q. I'll prove this by counting pairs and showing A_S + e_q d_q ≥ |E(S)| + e_q.
>
> **Clarifying ancestor pairs and the global root**
>
> When q is the global root, the components of S-q are searched below q, and each edge in S-q introduces an additional internal ancestor pair within S\q. If q is the ancestor of all vertices in S\q, the sum of depths is now ≥ |S|-1 + e_q, which matches the expected inequality. If d_q > 0, the forest condition holds true.
>
> **Formalizing depth bounds for connected components**
>
> We can extend the idea by considering connected S and q. If d_q = 0 and q is the global root, all components of S-q lie below q. This produces a lower bound on total depths within each component. If d_q ≥ 1, we can use M * d_q. The inequality becomes:
> 
> ∑_{v∈S} d_v + M d_q ≥ |S|-1 + Σ. Let's formalize further using Φ(C), which represents minimal total depth for a search tree on C. For each component C, the sum must include |C| plus the minimal internal depths.
>
> **Refining minimum depth calculations**
>
> When considering the sum of depths, we account for the component depths and the additional cost given by τ(C). Previously, we used τ(C)=|C|-1 for forest minimums, but this may not hold when the structure isn't a star or simple tree. For complex trees, the total depth may be larger, depending on how components shift when the root is removed.
>
> **Generalizing depth calculations over components**
>
> For a connected set S and q, I’ve generalized the equation to handle depth sums and component τ values. It works for global depth, especially when d_q ≥ 1, as the forest property holds. But if d_q = 0, things get trickier—each v in S\q could have a different depth depending on components, and the connectivity may differ from the global root. We need to check if the recursive subtree forms a valid search tree within that component.
>
> **Validating inequalities for different configurations**
>
> I’m checking if the inequality holds when considering different parts of the graph. For example, if q is an endpoint, I'm adjusting the coefficients for each component based on its depth. This one facet seems to have a stronger lower bound, so the inequality might be valid but not fit the facet exactly. We’ll need to look more closely at points to confirm this.
>
> **Lifting schema and bounds for valid inequalities**
>
> I’m testing the lifting schema for inequalities, especially for cases where q is the root and where it's not. Based on my calculations, adding the appropriate coefficient seems to allow for a more accurate bound, so when q isn’t the root, I need to find a computable lower bound. The test results match!
>
> **Exploring tree structures and their complexity**
>
> It seems that star-like structures may have exponential connected sets, while paths have a polynomial growth. For bounded degree or pathwidth cases, the complexity could still be exponential. I also wonder whether dynamic programming over these structures could help with optimization. The "earliest vertex" concept seems important for deriving constraints.
>
> **Considering path minima consistency and tournament order**
>
> The constraints for path consistency seem to require minima on larger paths to align with subpaths. I wonder if introducing "min consistency" could help. A more exact formulation might involve tournament order variables. However, linear programming (LP) might not be strong enough, and I’ll need to consider other polytope structures. Could dynamic programming (DP)
>
> **Exploring search tree and exchange rotations**
>
> This thought seems to focus on whether search trees can be optimized using some form of vertex ranking or weighted depths. I'm curious about whether there are existing polynomial algorithms for trees but hesitant to make claims. The local exchange conditions, particularly rotations between parent-child nodes, seem to have interesting potential. If the nodes aren't adjacent, swaps might be trickier.
>
> **Analyzing recursive search trees and root exchange**
>
> In recursive search trees, if I’m choosing between two nodes, r and s, as the root of a component, the key is figuring out if there's a cost difference for each option when everything below the root is held optimally. To decide, I want to compare the weighted values and sum of components efficiently. The goal is to minimize costs based on dynamic programming conditions and find the optimal root for each subproblem.
>
> **Understanding the polytope of distributions over recursive trees**
>
> I’m analyzing the polytope of distributions over recursive trees, which is the convex hull of integral root-choice incidence vectors. I suspect the linear system might be integral, and I think I can confirm this by proving that feasible decompositions are convex combinations of deterministic policies. This leads to a distribution over deterministic search trees, and the polytope is, in fact, a convex hull.
>
> **Evaluating polytope integral and facet structure**
>
>
> **Deriving facets and vertices from recursive lifting**
>
> I’m working on deriving the facets of P4 from recursive lifting and checking if they match the conditions for P3. I’ve listed some lower facets and vertices, considering how they’re organized by different roots in the tree. It seems like there are many, but I’ll classify them and focus on representative classes, particularly under reversal.
>
> **Classifying facets under reversal equivalence**
>
>
> **Explaining inequalities and search tree depth**
>
> I’m reviewing representative inequalities and their reversed counterparts for the recursive search tree. Some inequalities describe lower bounds while others set upper/shape constraints. On the upper bounds, I’m thinking that the maximum sum of depths, for a Hamiltonian-like tree, is n(n-1)/2, which can be achieved by selecting leaves in sequence.
>
> **Thinking through depth differences in trees**
>
> I’m looking at the depth difference between adjacent vertices in a search tree, like with a star leaf and its center. If one vertex is an ancestor of the other, the depth difference isn’t necessarily 1 — it can be greater if there are intermediate vertices between them. This seems true for general adjacent edges too.
>
> **Exploring depth differences for adjacent vertices**
>
> For an edge like 1-2, if vertex 2 is an ancestor of vertex 1, the depth difference could be 1, but not always — for example, in a path, 1-2-3-4. When considering leaves, if a leaf is chosen before its neighboring
>
> **Analyzing component and depth differences**
>
> I’m considering the depth difference between two vertices, u and v, after removing vertex v. In a leaf scenario, I can use the inequality \(d_{\text{leaf}} - d_{\text{neighbor}} \leq 1\) to help, which holds as a valid convex inequality.
> 
> For non-adjacent vertices, the depth difference depends on their ancestors. If v is an ancestor of u, the difference is small, at most the size of the component containing u after removing v.
>
> **Considering the bounds of depth differences in a tree**
>
> If u is an ancestor of v, the depth difference, \(d_u - d_v\), will be negative or zero, which makes sense. But if the nodes are incomparable within the search tree, the difference could be larger. I’m exploring cases like in a star-shaped tree where removing one leaf affects the depth difference significantly. 
> 
> Additionally, if some ancestors of u are not ancestors of v,
>
> **Exploring depth inequalities and ancestor relations**
>
> I can derive that \(d_u - d_v \leq |A|\), where A is the set excluding v, and the inequality holds because the ancestors of u may include all other nodes in A. For adjacent leaves, size=1. This gives an upper bound on the depth difference. I noticed an interesting formula for total depth sums based on ancestor pairs! That relates to the path endpoints too. This helps map how ancestor relationships contribute to the total depth calculation.
>
> **Analyzing path relationships and depth constraints**
>
> I can derive a "triple identity" for paths: If u is an ancestor of v on path u-x-v, then u is also an ancestor of x. It's interesting, because I can also apply this logic to nested paths. Then, I’d want to look at constraints on path subsets (I⊆J) and study the structure involving depth sums. I'll need to explore the behavior of connected subsets and their relationship with depth (z values).
>
> **Considering hereditary choice functions and consistency**
>
> These \( \lambda \)-like variables apply to all connected subsets, not just recursive problems. For each connected subset, there’s a sum constraint on the z-values, and a nested consistency for subsets. I'm wondering if every hereditary choice function corresponds to a total order, particularly for connected tree
>
> **Exploring LP for depth and path constraints**
>
> I’m considering a linear program (LP) involving connected sets and a depth formula. The idea is to define depth based on the number of connected paths, and then use constraints like z values to form relationships between subsets. I’m curious whether these constraints create a valid convex hull or if there's an issue with the LP's integrality. I'll need to test examples to see if this projection works.
>
> **Constructing deterministic choice functions and recursion**
>
> I’m considering the connection between connected sets and deterministic choice functions. The idea is to create a total order recursively on components. Starting with a root element, we can then recursively define the order for the components. This seems to work well for search trees and potentially for proving the LP’s integrality, but I'm not sure yet if it's the exact convex hull for these choices.
>
> **Testing integral solutions and LP relaxation**
>
> I'm considering testing small paths via vertex enumeration and using linear programming. The goal is to check if the LP is integral, with potential constraints based on intervals. I'll do random objective tests with scipy linprog, avoiding over-reliance. I’m not sure yet if this gives a compact or exact solution, but it's worth examining.
>
> **Testing path projection for P4**
>
> I’m thinking of testing projections for path P4, focusing on the depth hull facets. The idea is to build LP constraints and optimize against these facets, checking for violations. I can use scipy linprog with variables for connected subsets, intervals, and roots, testing simplex equality and heredity constraints.
>
> **Testing projection for path optimization constraints**
>
>
> **Testing integrality and projection for P4 and K1,3**
>
> For P4, it seems there’s no violation in the projection. I’m considering testing a small nonpath star next. The z variables for connected subsets grow exponentially, so I could compare depth hull facets. Random LP solutions for a small tree might help check integrality. I'll optimize a random objective to test for fractional solutions.
>
> **Evaluating random LP solutions for integrality**
>
>
> **Testing depth projection for T5**
>
> I’ve found that the z LP is not integral for T5. I should check if the depth projection violates the actual hull. To do this, I’ll compute the true hull for T5—perhaps by considering the number of search trees. After that, I'll compare the depth projection with the actual min/max over depth using random objectives to check for violations.
>
> **Computing depth projection and optimal solutions**
>
>
> **Exploring z/min-choice relaxation for T5**
>
> This is interesting: using a z/min-choice heredity relaxation seems too weak for T5. The original approach is small-scale, but can I present a computed candidate instead? I'll label tree vertices nicely—like a path with a leaf attached—and manually show the fractional z solution for the depth. The objective gives a result close to optimal, but there's a potential problem with the weak relaxation. I'll investigate if relaxation with nonnegative objectives can improve things and distinguish full integrality from optimal depth accuracy.
>
> **Evaluating fractional z relaxation for depth optimization**
>
>
> **Exploring relaxation and fractional z assignment for depth optimization**
>
> I'm wondering if the z relaxation could be exact for nonnegative minimization. The failure to separate hulls might be due to arbitrary separation, but if the objective weights must be nonnegative, that could be the issue.
> 
> To investigate, I’ll manually present the fractional z assignment and craft a separating inequality for the depth vectors. The current LP solution, with fractional values, doesn’t satisfy the hull since it leads to a discrepancy in the objective.
>
> **Exploring fractional z assignment and relaxation**
>
> The negative coefficient on -d1 is a bit tricky. It could represent a facet, but I’ll frame it as a separation certificate for now. I need to show that the fractional z assignment meets the relaxation criteria and results in the same depth. Let’s print the fractional z values to see if we can recover the nonzero ones and work from there.
>
> **Extracting fractional z assignment for relaxation validation**
>
>
> **Checking heredity constraints for fractional solutions**
>
> I need to verify heredity constraints for the fractional solution. The tree structure shows certain paths with specific choices. For each connected set containing vertex 4, the choice for 4 happens with probability 1, while others are more complex. I’ll present the depth formula and show the inequalities to prove it’s not in the hull.
>
> **Considering negative weights and separation maximization**
>
> I’m working with negative weights in the context of minimization while maximizing the mixed-sign L. The goal is to define G(S) by considering local search trees, and then computing values for S=all with specific weights. Once computed, I’ll show that G(V)=29 and explore the fractional solution's result, 30.
>
> **Computing optimal values and subvalues for separation**
>
>
> **Computing root cases and validating relaxation**
>
> I’ve calculated the root cases, with the maximum achieving 29. For the fractional z relaxation, the objective is 30, confirming its validity. While this supports the idea of the "hereditary path-minimum relaxation," the mixed-sign separation still affects accuracy. I'll note this was computed hands-on for clarity.
>
> **Formulating connected set counts in trees**
>
> I'm defining sets based on leaves and boundaries. For trees with a fixed number of leaves, determining the connected sets involves choices of boundary vertices along the leaf-to-core path, leading to a count of roughly \(O(n^L)\). This provides a compact structure, useful for specific families like fixed-leg spiders.
>
> **Analyzing connected subgraphs and root probabilities**
>
> A connected subgraph in a tree could be minimal but may scale as \(O(n^\ell)\) if we're dealing with fixed leaves. When considering a fixed tree skeleton with branching vertices, the number of connected subgraphs is polynomial for a given structure. Exploring root-probabilities: it seems the determination of depth and root position depends on minimizing non-negative functions, with adjustments based on whether a vertex is the root or not in a deterministic setup.
>
> **Exploring minimized support functions and hull separation**
>
> To minimize \(c\), the recurrence relation seems to support separation when \(c\) is arbitrary. For non-negative \(c\), it provides a valid Hull. The idea is that inequalities like \(c \cdot d \geq \beta\) are valid for specific conditions. Using a recurrence, we derive an exact solution for arbitrary \(c\), and this functions as a characterization for support functions, distinguishing the hull with non-negative weights versus weighted depth objectives.
>
> **Planning the final structure and content**
>
> I need to ensure we approach the convex relaxation and depth minimization problem exactly, using non-negative c values. There’s an important relationship between the support function and the convex relaxation's exactness. I'll draft the final structure to cover key topics: support-function exactness, recursive inequalities, facets, path-minimum relaxation, and compression for fixed topologies. It shouldn’t be overly long, but thorough with formulas.
>
> **Analyzing inequalities and sequential lifting**
>
> For a set \(S\), I’m thinking about defining the inequalities using a connected structure and coefficients that fit. The target function \(\theta\) is based on its components, and we can define a valid inequality using the coefficients on specific parts of \(S\). The idea is to manage the weights and break down the inequalities systematically.
>
> Thought for 5m 24s

I’ll push in three directions: strengthen the recursive inequalities, compute the next small path $P_4$, and isolate what an exact-but-still-compact formulation would need to remember beyond plain ancestry/depth.

One thing that seems important: the first nontrivial inequalities are not just “connected set needs total depth at least $|S|-1$.” They encode a conditional statement: if a particular vertex is shallow, then the pieces left after removing it must still pay their own internal depth cost.

Continuing the clean-room attack.

# 10. Support-function view of the hull

For any connected subtree $S\subseteq V$, define

$$
P(S)=\operatorname{conv}\{d_T:T\text{ is a recursive search tree on }U[S]\}.
$$

For any coefficient vector $c\in\mathbb R^S$, define the support lower envelope

$$
\phi_S(c)=\min_{d\in P(S)} c\cdot d.
$$

Then the recursive definition gives the exact recurrence

$$
\phi_S(c)
=
\min_{r\in S}
\left[
\sum_{v\in S\setminus\{r\}} c_v
+
\sum_{C\in \operatorname{comp}(S-r)}
\phi_C(c|_C)
\right].
$$

This is the same recurrence as the weighted-depth dynamic program, but now $c$ is allowed to have arbitrary signs. Therefore the full hull can be described, noncompactly, as

$$
P(S)
=
\{d\in\mathbb R^S: c\cdot d\ge \phi_S(c)\text{ for all }c\in\mathbb R^S\}.
$$

Equivalently, upper inequalities are obtained by applying the same formula to $-c$:

$$
c\cdot d\le -\phi_S(-c).
$$

This is useful conceptually because every valid facet inequality of the depth hull is just one coefficient vector $c$ together with the recursively computed optimum $\phi_S(c)$.

For nonnegative search weights $w\ge 0$, only the lower envelope for $c=w\ge 0$ matters. For the whole hull, mixed-sign $c$’s matter too.

---

# 11. A general recursive lifting scheme for inequalities

Suppose $S$ is connected, $q\in S$, and $h\in\mathbb R_{\ge 0}^{S\setminus\{q\}}$. Let

$$
\theta
=
\sum_{v\in S\setminus\{q\}} h_v
+
\phi_{S-q}(h),
$$

where $\phi_{S-q}$ means the sum of $\phi$ over the connected components of $S-q$.

If $q$ is the root of $S$, then every $v\neq q$ receives one extra depth level, and the remaining local depths lie in the components of $S-q$. Therefore

$$
\sum_{v\neq q} h_v d_v\ge \theta.
$$

To make this valid even when $q$ is not root, add a lifted $d_q$-term:

$$
\sum_{v\neq q} h_v d_v+\alpha d_q\ge \theta.
$$

A sufficient valid choice is

$$
\alpha=\theta.
$$

A sharper, minimal lifting coefficient is

$$
\alpha^\star
=
\max_{\substack{T\text{ valid on }S\\ d_T(q)>0}}
\frac{\theta-\sum_{v\neq q}h_v d_T(v)}{d_T(q)}.
$$

This is an exact sequential-lifting formula.

The earlier inequality

$$
\sum_{v\in S}d_v+\tau(S-q)d_q\ge |S|-1+\tau(S-q)
$$

is the special case $h_v=1$, where

$$
\tau(F)=\min_T\sum_{v\in F}d_T(v)
$$

is the minimum unweighted total depth over the forest $F=S-q$.

---

# 12. The next path: $P_4$

Let $U$ be the path

$$
1-2-3-4.
$$

The valid depth vectors are the $14$ Catalan search-tree vectors:

$$
\begin{aligned}
&(0,1,2,3),\ (0,1,3,2),\ (0,2,1,2),\ (0,2,3,1),\ (0,3,2,1),\\
&(1,0,1,2),\ (1,0,2,1),\\
&(1,2,0,1),\ (2,1,0,1),\\
&(1,2,3,0),\ (1,3,2,0),\ (2,1,2,0),\ (2,3,1,0),\ (3,2,1,0).
\end{aligned}
$$

These decompose by first root:

- root $1$: shifted $P_3$ on $\{2,3,4\}$;
- root $2$: singleton $\{1\}$ and edge $\{3,4\}$;
- root $3$: edge $\{1,2\}$ and singleton $\{4\}$;
- root $4$: shifted $P_3$ on $\{1,2,3\}$.

A representative nontrivial facet is

$$
4d_1+2d_2+d_3+d_4\ge 7.
$$

This is not just a forest inequality. It comes from the lifting scheme.

Take $q=1$, $S=\{1,2,3,4\}$, and weights

$$
h_2=2,\qquad h_3=1,\qquad h_4=1.
$$

If $1$ is the root, the residual path is $2-3-4$. Its minimum local $h$-weighted depth is $3$, and the one-level shift contributes

$$
h_2+h_3+h_4=4.
$$

So the root-$1$ face requires

$$
2d_2+d_3+d_4\ge 7.
$$

If $1$ is not the root, then $d_1\ge 1$, and the best possible value of $2d_2+d_3+d_4$ is $3$. Therefore adding $4d_1$ gives the globally valid inequality

$$
4d_1+2d_2+d_3+d_4\ge 7.
$$

Its mirror is

$$
d_1+d_2+2d_3+4d_4\ge 7.
$$

This suggests a pattern: many depth-hull facets are lifted root-face inequalities, not merely subset-sum inequalities.

---

# 13. A natural “path-minimum” relaxation

Define variables

$$
z_{A,r}
$$

for every nonempty connected $A\subseteq V$ and $r\in A$, intended to mean:

$$
z_{A,r}=1
\quad\Longleftrightarrow\quad
r\text{ is the earliest/root vertex of }A.
$$

The natural constraints are:

$$
\sum_{r\in A} z_{A,r}=1
\qquad\text{for every connected }A,
$$

and heredity:

$$
z_{A,r}\le z_{B,r}
$$

whenever $B\subseteq A$ are connected and $r\in B$.

Reason: if $r$ is earliest in $A$, then $r$ is earliest in every connected subset $B\subseteq A$ containing $r$.

Depth is then encoded by path minima:

$$
d_v=\sum_{u\neq v} z_{P(u,v),u},
$$

where $P(u,v)$ is the vertex set of the unique base-tree path from $u$ to $v$.

The integer version is exact. Indeed, an integral feasible $z$ defines a choice function $c(A)\in A$ for every connected $A$. Heredity says that if $c(A)\in B\subseteq A$, then $c(B)=c(A)$. Taking $c(V)$ as the root and recursing on the components of $V-c(V)$ gives a valid recursive search tree.

But the LP relaxation is not exact.

---

# 14. A small fractional counterexample to the path-minimum relaxation

Take the five-vertex tree with edges

$$
0-1,\qquad 1-2,\qquad 1-3,\qquad 3-4.
$$

So $1$ is a branching vertex, and $4$ is the end of a length-two arm.

Define a fractional $z$-solution as follows.

Singletons choose themselves. Every connected set containing $4$ and lying on the $4$-side chooses $4$ with probability $1$:

$$
z_{\{3,4\},4}=1,
$$

$$
z_{\{1,3,4\},4}=1,
$$

$$
z_{\{0,1,3,4\},4}=1,
$$

$$
z_{\{1,2,3,4\},4}=1,
$$

$$
z_{\{0,1,2,3,4\},4}=1.
$$

On the remaining connected sets, split as follows:

$$
z_{\{0,1\},0}=z_{\{0,1\},1}=\frac12,
$$

$$
z_{\{1,2\},1}=z_{\{1,2\},2}=\frac12,
$$

$$
z_{\{1,3\},1}=z_{\{1,3\},3}=\frac12,
$$

$$
z_{\{0,1,2\},0}=z_{\{0,1,2\},2}=\frac12,
$$

$$
z_{\{0,1,3\},0}=z_{\{0,1,3\},3}=\frac12,
$$

$$
z_{\{1,2,3\},2}=z_{\{1,2,3\},3}=\frac12,
$$

$$
z_{\{0,1,2,3\},0}=z_{\{0,1,2,3\},2}=\frac12.
$$

All omitted $z$’s are $0$.

This satisfies the simplex constraints and the heredity constraints. The induced depth vector is

$$
d=(2.5,2.5,2.5,2.5,0).
$$

But this point is not in the true depth hull.

A separating inequality is

$$
4d_0-d_1+5d_2+4d_3+d_4\le 29.
$$

The fractional point gives

$$
4(2.5)-2.5+5(2.5)+4(2.5)+0=30,
$$

so it violates the true hull.

To certify the inequality, use the max version of the recursive dynamic program with coefficient vector

$$
c=(4,-1,5,4,1).
$$

Let

$$
M(S)=\max_T\sum_{v\in S}c_v d_T(v)
$$

over search trees on $S$. The relevant values are:

$$
M(\{0,1,2\})=9,
$$

$$
M(\{0,1,3\})=8,
$$

$$
M(\{1,2,3\})=9,
$$

$$
M(\{1,3,4\})=9,
$$

$$
M(\{0,1,2,3\})=17,
$$

$$
M(\{0,1,3,4\})=15,
$$

$$
M(\{1,2,3,4\})=17.
$$

For the whole tree, check the five possible roots:

$$
\begin{array}{c|c}
\text{root} & \text{maximum value through that root}\\
\hline
0 & 26\\
1 & 18\\
2 & 23\\
3 & 18\\
4 & 29
\end{array}
$$

Hence the true maximum is $29$, proving the inequality.

Important caveat: this counterexample uses a mixed-sign separating functional. So it proves the relaxation is not the full hull. It does not, by itself, prove that the relaxation gives a wrong optimum for nonnegative weighted-depth minimization.

That distinction matters.

---

# 15. Compact families beyond paths

The exact connected-subproblem formulation has size controlled by the number of connected induced subtrees of $U$.

For paths, connected subtrees are intervals, so there are $O(n^2)$, and the exact formulation has $O(n^3)$ root-choice variables.

For a fixed-leg spider, with center $c$ and $k$ arms, connected subtrees are of two types:

1. intervals lying entirely inside one arm;
2. subtrees containing $c$, determined by a prefix length on each arm.

If $k$ is fixed, the number of such connected subtrees is polynomial in $n$, roughly

$$
O(n^2+\prod_{i=1}^k (n_i+1)).
$$

So fixed-leg spiders admit compact exact LPs by the connected-subproblem formulation.

More generally, any family obtained by subdividing a fixed finite tree skeleton should have polynomially many connected subtrees, because each connected induced subtree is described by finitely many interval endpoints along the skeleton’s branches.

Stars are exceptional in the other direction. The connected-subproblem formulation sees exponentially many connected sets containing the center and arbitrary leaf subsets, but the star hull has a much smaller permutahedral description because of symmetry.

So there are at least two different compactness mechanisms:

1. **few connected subproblems**, as in paths and fixed-skeleton subdivisions;
2. **high symmetry**, as in stars.

---

# 16. Sharper local optimality certificate

For nonnegative weights $w$, define

$$
F(S)
=
\min_T \sum_{v\in S} w_v d_T(v).
$$

Then

$$
F(S)
=
\min_{r\in S}
\left[
W(S)-w_r+
\sum_{C\in \operatorname{comp}(S-r)}F(C)
\right].
$$

Equivalently, choosing root $r$ is optimal in subproblem $S$ iff $r$ maximizes the score

$$
\Gamma_S(r)
=
w_r-
\sum_{C\in \operatorname{comp}(S-r)}F(C).
$$

So an optimal search tree can be certified locally by giving, for every encountered subproblem $S$, the chosen root $r$, the component values $F(C)$, and the inequalities

$$
\Gamma_S(r)\ge \Gamma_S(q)
\qquad\text{for every }q\in S.
$$

This is exact. It is not merely a heuristic exchange condition.

For two candidate roots $r,q\in S$, the comparison is

$$
w_r-w_q
\ge
\sum_{C\in \operatorname{comp}(S-r)}F(C)
-
\sum_{D\in \operatorname{comp}(S-q)}F(D).
$$

This says: a root is worth choosing early if its weight advantage compensates for the worse recursive decomposition it may create.

---

# 17. Current frontier

The strongest clean conclusions so far are:

1. **Exact exponential formulation.**  
   The connected-subproblem $(\mu,\lambda)$-formulation exactly projects to the depth-vector hull.

2. **Exact support recursion.**  
   Every valid linear inequality is governed by the recursive support function $\phi_S(c)$.

3. **Paths are compact.**  
   Since connected subtrees are intervals, paths admit an exact polynomial-size LP.

4. **Stars are explicit.**  
   The star hull is a convex hull of leaf permutahedra indexed by the depth of the center.

5. **Simple forest inequalities are too weak.**  
   Already $P_3$ cuts off $(0,1,1)$.

6. **Ancestry/path-minimum relaxations need care.**  
   Even a natural hereditary path-minimum LP is not the full hull; the five-vertex tree above gives a fractional point outside the hull.

7. **Root-face lifting seems central.**  
   Nontrivial facets such as

   $$
   4d_1+2d_2+d_3+d_4\ge 7
   $$

   for $P_4$ arise by lifting inequalities from the face where a specified vertex is root.

The next serious target would be to characterize which recursively lifted inequalities suffice for paths. My current guess is that the path hull is governed by a recursively generated family of interval-root lifted inequalities, and that this family is essentially an associahedral analogue for depth vectors.

## Prompt:
5/15/2026, 4:24:44 PM

Follow up ambitiously: aim higher (i.e. to prove something stronger) than what you think the next best serious target is.

## Response:
5/15/2026, 4:24:50 PM

> **Exploring tree optimization and bounds**
>
> I'm thinking about deriving a stronger result here, potentially proving an extended formulation for trees. We could consider applying dynamic programming or examining search tree polytopes for a polynomial solution. Maybe I’ll target polynomial bounds for optimal binary search tree generalization with weighted nodes. I'll try to avoid relying on prior knowledge!
>
> **Optimizing search trees and proving stronger results**
>
> I'm pondering dynamic programming for optimal search trees, possibly for trees with weighted costs—could this be polynomial? Clean-room derivation for hull description with root-choice policies seems promising. Maybe I'll explore proving facet families or dual integrality of path problems, aiming for a stronger result than initially planned!
>
> **Characterizing path depth vectors for binary trees**
>
> I’m thinking of characterizing path depth vectors for binary trees by considering recursive search trees with fixed inorder leaves. The key might be finding a connection to known polytope structures like associahedrons. Can we derive inequalities for intervals within those trees? Time to explore!
>
> **Exploring depth polytope facets and interval spans**
>
> I'm considering stronger formulations to account for global depths, including ancestors outside specific intervals. Could we use dynamic programming and express "span intervals" for each interval and coefficient vector? It seems like we might derive some finite, irredundant facets. Time to check the number of polytope facets using Python!
>
> **Calculating depth vectors for binary search trees**
>
>
> **Computing facets for P4/P5 and checking dimensions**
>
> I want to compute the facets for P4 and P5. I’m wondering if ConvexHull will give me the full dimensional output. For P2, it seems like it could be a 1D line with a sum of 1. P3, on the other hand, might have a dimension of 3—I'll need to check the rank.
>
> **Computing convex hull facets and rank**
>
>
> **Examining integer facets and rationalization for P3**
>
> I noticed that for P3, previous halfspaces gave 5 facets, but the hull shows 6. Maybe we missed something like nonnegativity? I'll focus on getting integer facets by using rationalization. To be more robust, I should use a rational denominator and normalize the equations to unit form.
>
> **Enumerating integer facets with rationalization**
>
>
> **Improving facet enumeration with exact methods**
>
> It seems rationalization isn't working well due to qhull's numeric inaccuracies. I want to try using pycddlib, but it might not be installed. Instead, I'll attempt scipy's hull equations and normalize by solving integer ratios. For n=4, I can enumerate subsets of points, while for n=5, I’ll need to carefully choose the manageable points.
>
> **Implementing exact facet enumeration using rational numbers**
>
>
> **Exploring facet interpretation and optimization theorem**
>
> The P4 facets include mixed signs and are non-monotonic. I wonder if binary search tree depth vectors could match vertices of a generalized permutahedron? I’m considering inequalities for subsets, but the signs complicate things. Maybe a stronger theorem exists for nonnegative objectives—could pairwise “cut” variables offer a solution for arbitrary trees? I'll need to explore weight optimization with depth variables and examine how greedy sorting could work for path optimal BSTs.
>
> **Exploring tree DP and geometric formulations**
>
> The optimal binary search tree problem has an O(n^3) DP, but there's no closed greedy for general trees—likely DP over connected subtrees, making it maybe NP-hard. But what if trees have centroid-like optimality? I’m thinking of proving that a full hull is the projection of a small EF using order polytope variables, and trying to test this. Alternatively, could we characterize ancestry posets using pair/triple relations? Finally, how about deriving a compact formulation using linear ordering? Let’s work through these possibilities!
>
> **Exploring polytope structure and constraints**
>
> The \(\mu, \lambda\) formulation not only describes the hull exactly, but its feasible region is integral—a network matrix for paths. I wonder if I could prove TU for the interval formulation, showing all vertices come from deterministic recursive trees. For arbitrary trees, though, \(\mu, \lambda\) might not be integral. Is the feasible region integral for general flow? Maybe the structure corresponds to convex hulls of branching processes–I'll need to confirm if extreme points are deterministic. Let’s explore these ideas!
>
> **Exploring occupancy polytope in branching MDP**
>
> I’m wondering if extreme points in the occupancy polytope for a branching Markov decision process (MDP) are deterministic root choices, especially for each connected \( S \). I think the occupancy of \( \mu/\lambda \) may still be integral, and each state’s policy distribution could align with deterministic policies, as long as the random choices are independent. Let's see if the extended polytope is integral—this could indeed suggest deterministic extreme points!
>
> **Finalizing occupancy polytope and dual formulation**
>
> I’m refining the final formulation and wondering if I should explore the integrality of the extended formulation for arbitrary trees. Also, I’m thinking about duality—I can use Bellman potentials to define local certificates. For minimizing weights, I’m considering an objective where each subproblem’s root choice influences the costs. Let's see if this leads to possible separation or dual solutions. Interesting challenge!
>
> **Exploring facets, dual potentials, and exact formulations**
>
> I’m trying to build a strong framework around the Bellman tight actions, looking into recursive faces and how they link to facets. A potential universal theorem tracing all exposed faces could be really powerful. Maybe I’ll delve deeper into whether the path-minimum relaxation could be exact, especially for nonnegative weighted depths. It’s a bit ambitious, but definitely worth testing!
>
> **Testing small trees with LP optimization**
>
> I’m thinking about testing small connected trees to see if we can solve them using LP. I can try using `scipy.linprog` and generate connected subsets, adding constraints to compare with DP enumeration. If it works, great; if not, it’ll give us a counterexample. Time to start coding!
>
> **Analyzing path-minimum relaxation for tree optimization**
>
>
> **Exploring hereditary path-minimum in LP**
>
> The hereditary path-minimum LP might be exact for nonnegative weighted objectives, even if it's not exactly the hull. This is important for understanding "full integrality exactness of the best depth objective." I want to prove this, though it's ambitiously tricky. I’ll work on computing the objective and explore constraints carefully.
>
> **Exploring constraints and objective for path pairs**
>
> The variables z_{A,r} are only nonnegative for path pairs (r, v). For each connected set A, the constraint Σ_{r∈A} z_{A,r} = 1 holds. I’m thinking the solution could be a choice function satisfying heredity—likely a total order on connected subsets. I need to verify how this applies to LP integrality for nonnegative costs.
>
> **Defining recursive LP objective and feasibility**
>
> I’m defining a root r for the whole set V, with the simplex method giving the distribution z_{V,r}. If I randomly choose root r based on z_{V,r}, I’ll need to recursively define the conditional z for components, ensuring heredity holds. I aim to compare the objectives, explore the Bellman inequality, and prove LP relaxation bounds.
>
> **Analyzing deterministic root r and costs**
>
> For each root r, every pair (r, v) where r is an endpoint has d_v
>
> **Testing conditional slack and decomposition of cost**
>
> I’m thinking of using conditional slack by defining residual variables for each pair within a component based on the root choice. The goal is to break the cost into pair contributions across the root and components, finding bounds for the leftover cost via induction. I'll test this approach.
>
> **Testing feasibility of fractional z and integral choice functions**
>
> I’m considering whether fractional z could be a distribution over integral choice functions. If true, that would make the polytope integral. But we already found some fractional points outside the hull, so I’m wondering if the constraints might not be enough for global coupling, despite being exact for path endpoint objectives.
>
> **Testing feasibility of fractional choice functions**
>
>
> **Testing LP exactness for paths and heredity relaxation**
>
> I’m thinking about proving the exactness of the LP relaxation for paths, specifically with nonnegative weights. The strategy could involve applying Monge’s property and uncrossing. I’ll check random small pathways for n <= 6, and confirm if the z relaxation could hold for this case.
>
> **Exploring costs for pairs and top-root allocation**
>
> I'm trying to understand how pairs contribute to cost, where each pair contributes if one endpoint appears earliest on the path. For fractional trees, the expected cost is calculated from both the top and subtree costs. I need to figure out lower bounds based on whether a pair is outside a given root.
>
> **Exploring relaxation and potential new theorems**
>
> The proof seems tough because I can't rely on the conjecture about the top root k and endpoint choices. Instead, I should consider a new theorem related to tree polytopes and dual Bellman certificates. This would be a stronger, more rigorous approach, maybe even leading to a "face factorization" result or a parameterized family of inequalities.
>
> **Exploring theorems and relaxation on path-minimum problems**
>
> The connection between local root-choice inequalities and exposed face decomposition seems crucial, and Theorem C gives a recursive way to describe normal fans and facets. The path theorem (E) looks promising with its integral formulation. However, the proposed relaxation for nonnegative objectives is still speculative and requires further exploration.
>
> Thought for 4m 15s

I’ll aim past “some lifted inequalities for paths” and try for a structural theorem: either a complete inequality scheme for path depth vectors, or a compact exact formulation that collapses the recursive interval DP into something closer to a known/simple object.

I found a stronger angle than just listing more facets: the recursive LP is an occupancy-measure formulation for a branching acyclic decision process. That means it should be integral in the extended space: fractional feasible points are exactly mixtures of deterministic recursive root policies, not mysterious new objects.

I’ll aim higher than “understand the path facets.” The stronger target is:

> **Describe the entire depth-vector hull, its support function, its exposed faces, and its optimality certificates from one recursive Bellman/occupancy principle.**

This does not magically make the general-tree formulation compact, but it gives a fairly complete structural theorem.

# 18. The branching-flow theorem

Let $\mathcal C(U)$ be the set of nonempty connected induced subtrees of $U$.

For each connected $S\in \mathcal C(U)$ and each $r\in S$, introduce a variable

$$
x_{S,r}\ge 0,
$$

interpreted as:

$$
x_{S,r}
=
\Pr(\text{subproblem }S\text{ occurs and chooses root }r).
$$

Define the outflow of $S$ by

$$
\mu_S=\sum_{r\in S}x_{S,r}.
$$

The exact branching-flow constraints are:

$$
\sum_{r\in V}x_{V,r}=1,
$$

and for every $S\neq V$,

$$
\sum_{r\in S}x_{S,r}
=
\sum_{\substack{R\in\mathcal C(U),\ q\in R:\\ S\text{ is a connected component of }R-q}}
x_{R,q}.
$$

The depth projection is

$$
d_v
=
\sum_{\substack{S\in\mathcal C(U):\\ v\in S}}
\sum_{\substack{r\in S:\\ r\neq v}}
x_{S,r}.
$$

Equivalently,

$$
d_v
=
\sum_{\substack{S\ni v}}
\bigl(\mu_S-x_{S,v}\bigr).
$$

## Theorem 18.1: exactness and integrality

The feasible region of the branching-flow LP is exactly the convex hull of deterministic recursive search policies, in the extended $x$-space. Therefore its depth projection is exactly the depth-vector hull.

This is stronger than merely saying “the formulation is valid.”

### Proof

Take any feasible $x$. For every connected $S$ with $\mu_S>0$, define the conditional root-choice distribution

$$
p_S(r)=\frac{x_{S,r}}{\mu_S}.
$$

If $\mu_S=0$, define $p_S$ arbitrarily.

Now sample a deterministic recursive policy $\rho$ as follows: independently for every connected $S$, choose

$$
\rho(S)=r
$$

with probability $p_S(r)$.

This sampled policy specifies a root for every possible connected subproblem, hence determines a deterministic search tree.

Let $X^\rho_{S,r}\in\{0,1\}$ be the deterministic occupancy vector of this sampled policy: it is $1$ iff $S$ is reached and root $r$ is chosen there.

I claim

$$
\mathbb E[X^\rho_{S,r}]=x_{S,r}.
$$

For $S=V$,

$$
\Pr(V\text{ reached})=1=\mu_V,
$$

so

$$
\Pr(V\text{ reached and chooses }r)=p_V(r)=x_{V,r}.
$$

Now suppose the claim is known for all strict ancestors of a connected subproblem $S$. Then $S$ is reached exactly when some parent subproblem $R$ chooses a root $q$ for which $S$ is one of the components of $R-q$. Therefore

$$
\Pr(S\text{ reached})
=
\sum_{\substack{R,q:\\ S\in\operatorname{comp}(R-q)}}
\Pr(R\text{ reached and chooses }q).
$$

By induction,

$$
\Pr(S\text{ reached})
=
\sum_{\substack{R,q:\\ S\in\operatorname{comp}(R-q)}}
x_{R,q}
=
\mu_S.
$$

Then

$$
\Pr(S\text{ reached and chooses }r)
=
\mu_S p_S(r)
=
x_{S,r}.
$$

Thus every feasible fractional $x$ is a convex combination of deterministic recursive policies. Conversely, every deterministic recursive search tree clearly gives a feasible $x$. So the extended polytope is integral.

This is the cleanest structural result so far.

---

# 19. Bellman duality: every optimum has a local certificate

Now take an arbitrary coefficient vector $c\in\mathbb R^V$. We want to optimize

$$
c\cdot d.
$$

Using the depth projection,

$$
c\cdot d
=
\sum_{v\in V}c_v
\sum_{\substack{S\ni v}}\sum_{\substack{r\in S\\r\neq v}}x_{S,r}
=
\sum_{S\in\mathcal C(U)}
\sum_{r\in S}
x_{S,r}
\sum_{v\in S\setminus\{r\}}c_v.
$$

So choosing root $r$ in subproblem $S$ has local action cost

$$
g_c(S,r)=\sum_{v\in S\setminus\{r\}}c_v.
$$

Define the Bellman value

$$
F_c(S)
=
\min_T \sum_{v\in S}c_v d_T(v),
$$

where the minimum ranges over recursive search trees on $S$. Then

$$
F_c(S)
=
\min_{r\in S}
\left[
\sum_{v\in S\setminus\{r\}}c_v
+
\sum_{C\in\operatorname{comp}(S-r)}
F_c(C)
\right].
$$

This is valid for arbitrary signs of $c$, not only $c\ge 0$.

The dual certificate is:

$$
y_S
\le
\sum_{v\in S\setminus\{r\}}c_v
+
\sum_{C\in\operatorname{comp}(S-r)}y_C
\qquad
\text{for every }S,r.
$$

The optimal dual is

$$
y_S=F_c(S).
$$

For the original whole-tree problem, the certificate value is $F_c(V)$.

So every valid inequality of the form

$$
c\cdot d\ge \beta
$$

has best possible right-hand side

$$
\beta=F_c(V).
$$

Equivalently, the entire hull is

$$
P(U)
=
\{d\in\mathbb R^V: c\cdot d\ge F_c(V)\text{ for every }c\in\mathbb R^V\}.
$$

That is not compact, but it is exact and conceptually complete.

---

# 20. Exposed-face decomposition theorem

For each connected $S$, define the set of $c$-optimal roots

$$
R_c(S)
=
\arg\min_{r\in S}
\left[
\sum_{v\in S\setminus\{r\}}c_v
+
\sum_{C\in\operatorname{comp}(S-r)}
F_c(C)
\right].
$$

Then the $c$-minimizing face of $P(S)$ decomposes recursively as

$$
\operatorname{Face}_c(P(S))
=
\operatorname{conv}_{r\in R_c(S)}
\left\{
d:
d_r=0,\;
d_C=\mathbf 1_C+e^C,\;
e^C\in \operatorname{Face}_{c|_C}(P(C))
\right\}.
$$

This is stronger than a local optimality condition. It says the entire exposed face factors recursively.

In particular, if every $R_c(S)$ encountered along the recursion is a singleton, then $c$ exposes a single search tree. If some $R_c(S)$ has multiple roots, the exposed face is obtained by branching exactly at those ties.

So the normal fan of the depth hull is recursively governed by Bellman root ties.

---

# 21. Local exchange condition, now exact

For nonnegative weights $w$, the weighted-depth objective is $w\cdot d$. The Bellman recurrence is

$$
F_w(S)
=
\min_{r\in S}
\left[
W(S)-w_r
+
\sum_{C\in\operatorname{comp}(S-r)}F_w(C)
\right],
$$

where

$$
W(S)=\sum_{v\in S}w_v.
$$

Root $r$ is optimal in $S$ iff for every $q\in S$,

$$
W(S)-w_r+\sum_{C\in\operatorname{comp}(S-r)}F_w(C)
\le
W(S)-w_q+\sum_{D\in\operatorname{comp}(S-q)}F_w(D).
$$

Cancel $W(S)$:

$$
w_r-\sum_{C\in\operatorname{comp}(S-r)}F_w(C)
\ge
w_q-\sum_{D\in\operatorname{comp}(S-q)}F_w(D).
$$

So define the root score

$$
\Gamma_S(r)
=
w_r-\sum_{C\in\operatorname{comp}(S-r)}F_w(C).
$$

Then an optimal root maximizes $\Gamma_S(r)$.

This is the exact exchange principle:

> A vertex should be chosen as root when its immediate weight benefit outweighs the future cost of the component decomposition it creates.

This gives a complete local certificate of optimality. To certify a proposed optimal search tree, it is enough to give the values $F_w(C)$ for all subproblems occurring in the comparison and verify the root-score inequalities at every recursive node.

---

# 22. A stronger compactness theorem for structured tree families

The branching-flow LP has one state per connected induced subtree. Therefore it is compact whenever $U$ has only polynomially many connected induced subtrees.

This gives more than just paths.

## Theorem 22.1

If $\mathcal F$ is any family of base trees for which the number of connected induced subtrees is polynomially bounded in $|V|$, then the depth-vector hull has an exact polynomial-size extended formulation.

The formulation is the branching-flow LP above.

Families covered:

1. **Paths.**  
   Connected subtrees are intervals. There are $O(n^2)$ states and $O(n^3)$ root-choice variables.

2. **Cycles broken into a fixed tree skeleton.**  
   Since our base graph is a tree, the relevant case is a subdivision of a fixed finite tree skeleton. A connected induced subtree is determined by finitely many interval endpoints along the skeleton edges. If the skeleton is fixed, the count is polynomial.

3. **Trees with a fixed number of leaves.**  
   Such a tree has a fixed-size branching skeleton. Connected induced subtrees can be described by interval choices along the finitely many root-to-leaf arms. Hence polynomially many states.

4. **Fixed-leg spiders.**  
   If the number of arms is fixed, a connected subtree either lies in one arm or contains the center and is determined by one prefix length per arm. Polynomial.

Stars with unboundedly many leaves do not fit this “few connected subtrees” mechanism, because a connected subtree containing the center can include an arbitrary subset of leaves. But stars are compact by a different mechanism: symmetry/permutation structure.

So there are two compactness routes:

$$
\text{few connected subproblems}
$$

or

$$
\text{large symmetry allowing quotient/compression}.
$$

---

# 23. The path case: a sharper statement

For the path $P_n$, the exact interval formulation is:

Variables:

$$
x_{i,j,r}\ge 0
\qquad
1\le i\le r\le j\le n.
$$

Root flow:

$$
\sum_{r=1}^n x_{1,n,r}=1.
$$

For every proper interval $[i,j]\neq[1,n]$,

$$
\sum_{r=i}^j x_{i,j,r}
=
\sum_{a<i} x_{a,j,i-1}
+
\sum_{b>j} x_{i,b,j+1}.
$$

Explanation: interval $[i,j]$ is created either as the right component of $[a,j]$ after choosing $i-1$, or as the left component of $[i,b]$ after choosing $j+1$.

Depth projection:

$$
d_v=
\sum_{i\le v\le j}
\sum_{\substack{r=i\\r\neq v}}^j x_{i,j,r}.
$$

This is an integral extended formulation of size $O(n^3)$.

This proves something stronger than “the path hull has a recursive inequality system”: it has an exact polynomial-size integral extended formulation.

The dual is the interval Bellman system:

$$
y_{i,j}
\le
\sum_{\substack{v=i\\v\neq r}}^j c_v
+
y_{i,r-1}
+
y_{r+1,j}
\qquad
(i\le r\le j),
$$

with empty intervals assigned value $0$. The optimal value is $y_{1,n}$.

---

# 24. A concrete $P_4$ payoff

For $P_4$, the recursive theory explains why the lower facets are already more complicated than forest inequalities.

One valid facet is

$$
4d_1+2d_2+d_3+d_4\ge 7.
$$

This comes from asking: what must happen if vertex $1$ is shallow?

If $1$ is root, the residual interval is $2-3-4$, and with coefficients

$$
(2,1,1)
$$

on $(d_2,d_3,d_4)$, the minimum residual-plus-shift cost is $7$. If $1$ is not root, then $d_1\ge 1$, and the coefficient $4$ is exactly large enough to lift the root-$1$ face inequality to the full hull.

But $P_4$ has still stronger lower facets, for example

$$
5d_1+2d_2+d_3+2d_4\ge 9,
$$

and its mirror

$$
2d_1+d_2+2d_3+5d_4\ge 9.
$$

The point is that even for paths, the lower hull is not generated merely by inequalities of the form

$$
\sum_{v\in I}d_v\ge |I|-1.
$$

The recursive root-face lifting mechanism is genuinely needed.

---

# 25. A serious speculative target: objective-exact relaxations weaker than the hull

There is now a meaningful distinction between two notions:

1. **Hull-exactness:** the relaxation equals the full depth-vector hull.
2. **Objective-exactness for $w\ge 0$:** the relaxation may contain extra points, but minimizing $w\cdot d$ over it still gives the correct optimum for every $w\ge 0$.

The hereditary path-minimum relaxation from before is not hull-exact. It has fractional points outside the hull.

But it may still be exact for nonnegative weighted-depth minimization.

The relaxation has variables

$$
z_{A,r}
$$

for connected $A\subseteq V$, $r\in A$, with

$$
\sum_{r\in A}z_{A,r}=1,
$$

and heredity constraints

$$
z_{A,r}\le z_{B,r}
\qquad
(B\subseteq A,\ r\in B).
$$

Depth is encoded by

$$
d_v=\sum_{u\neq v}z_{P(u,v),u}.
$$

The integer version is exact. The LP relaxation is not hull-exact.

But for $w\ge 0$, its objective has the special form

$$
\sum_{v}w_v d_v
=
\sum_{u\neq v}w_v z_{P(u,v),u}.
$$

Only endpoint choices on paths are charged. Internal path roots are “good” because they separate endpoints without making either endpoint an ancestor of the other.

This suggests the following ambitious conjecture.

## Conjecture

The hereditary path-minimum relaxation is exact for nonnegative weighted-depth optimization on trees:

$$
\min_{z\text{ hereditary}} \sum_{u\neq v}w_v z_{P(u,v),u}
=
\min_{T\text{ recursive search tree}}\sum_v w_vd_T(v)
$$

for every $w\ge 0$.

Why this is plausible:

- The relaxation is too weak only in mixed-sign directions, at least in the smallest counterexamples found by hand.
- Nonnegative objectives reward choosing high-weight vertices early and reward internal separators; both are aligned with the recursive search process.
- The Bellman optimality conditions for $w\ge 0$ have a monotone “pay for descendants” structure absent from arbitrary signed objectives.

What remains missing is a rounding theorem: given a fractional hereditary $z$, produce a deterministic recursive search tree whose $w$-cost is no larger. A componentwise domination statement is false, so the rounding would need to be objective-sensitive.

This is a genuinely higher target than full path hull facets: it asks whether a non-hull-exact relaxation nevertheless solves every meaningful search-cost objective.

---

# 26. Strongest current theorem package

At this point, the serious clean-room progress is:

## Exact extended hull theorem

The depth-vector hull of any base tree $U$ is the projection of the integral branching-flow polytope over connected subproblems.

## Exact Bellman support theorem

For every coefficient vector $c$,

$$
\min_{d\in P(U)}c\cdot d
$$

is given by the recursive Bellman equation

$$
F_c(S)
=
\min_{r\in S}
\left[
\sum_{v\in S\setminus\{r\}}c_v
+
\sum_{C\in\operatorname{comp}(S-r)}F_c(C)
\right].
$$

## Exact exposed-face theorem

The face minimizing $c\cdot d$ recursively decomposes over the Bellman-optimal root choices.

## Exact local optimality certificate

For $w\ge 0$, a search tree is optimal iff every recursive root choice maximizes

$$
\Gamma_S(r)
=
w_r-\sum_{C\in\operatorname{comp}(S-r)}F_w(C).
$$

## Compactness theorem

Any family of trees with polynomially many connected induced subtrees has a polynomial-size exact integral extended formulation. This covers paths, fixed-leaf trees, fixed-skeleton subdivisions, and fixed-leg spiders.

## Remaining ambitious conjecture

There may be relaxations that are not hull-exact but still exact for all nonnegative weighted search objectives. The hereditary path-minimum LP is the leading candidate.

So the frontier has moved from “can we find inequalities?” to:

> The hull is structurally solved by an integral branching-flow/Bellman theorem; the next genuinely ambitious problem is to compress that theorem, either by exploiting tree structure, symmetry, or by proving that a weaker ancestry/path-minimum relaxation is objective-exact for all $w\ge 0$.

## Prompt:
5/15/2026, 4:33:29 PM

Good. For future reference, always keep in mind the original problem statement and what we'd ideally like to prove. Given that, follow up with an ambitious push of the current frontier.

## Response:
5/15/2026, 4:33:35 PM

> **Evaluating and refining solution path**
>
> The user hasn't requested web access, so I'll work without it. I need to stick with the current context, and avoid using prior conversation data. I should aim for a serious, rigorous approach by focusing on a formal, possible conjecture or proof. Let's explore optimizing the minimization of submodular/greedy functions and test its implications. I’ll consider search trees with weighted costs and vertex rankings as part of the problem.
>
> **Exploring path-minimum LP variables and optimization**
>
> I need to check if the LP can accurately optimize nonnegative weights, considering path-minimum variables for connected subsets with heredity. A counterexample might exist, so I’ll test this with small trees. I’ll model the problem using Python, specifically scipy.optimize.linprog to compute examples and compare with exact DP methods.
>
> **Exploring path-minimum LP relaxation and optimization**
>
>
> **Implementing and validating tree connected subsets**
>
> I need to define the variables for tree-connected subsets and formulate exact DP for weighted depth, ensuring the hereditary constraints are met. The goal is to validate if heredity ensures exact integer solutions. I'll generate all small trees with Prüfer sequences or networkx, testing with random weights for trees of size n ≤ 6.
>
> **Validating integer exactness and hereditary LP constraints**
>
>
> **Proving LP exactness for nonnegative weights**
>
> I need to consider proving the LP’s exactness for nonnegative weights, possibly using duality. The hereditary path-minimum LP choice functions could relate to total orderings. I’m curious if these functions are mixtures or not. I'll also compare objectives using duality with Bellman’s approach, considering a compact relaxation. I might even propose the epigraph of a nonnegative support function as progress.
>
> **Exploring polynomial-time algorithm for weighted tree search**
>
> I’m considering whether a polynomial-time algorithm exists for weighted tree search problems. Dynamic programming over connected subsets seems exponential, but perhaps we can leverage treewidth or recursion over tree components. It might help simplify the optimization for nonnegative weights, reducing it from exponential to possibly polynomial. Let’s explore further!
>
> **Exploring subtree optimization and search tree structure**
>
> A connected induced subtree of a tree can be complex, with exponential possibilities due to star configurations, though star optimizations are simpler. A general tree with many branches might be challenging but could potentially be tackled with knapsack techniques. I also wonder if the depth of a vertex in a search tree aligns with permutation class properties. I'll explore this further!
>
> **Exploring depth vector connections and associahedron**
>
> I’m wondering if depth vectors relate to the "Loday associahedron" or "rotation distance." Path search trees could map to binary search trees, and their depth vectors might fit an associahedron realization. But Loday coordinates for internal nodes use different values—leaves, not depths. Let's explore whether the depth vector of binary trees on ordered keys makes this possible!
>
> **Exploring depth-related projection and branch-flow theorem**
>
> I’m thinking about how depth vectors and subtree intervals relate to Loday coordinates. The connections aren't straightforward, but maybe a "signed interval potential" approach from Bellman could
>
> **Exploring exact formulations and inequalities**
>
> I’m thinking about how the dominant could be equivalent to the existence of an x with depth ≤ d, using the formulation involving P + R_+. If we extend this to introduce "dominant EF," we might prove objectives for nonnegative weights. I'll look into generating inequalities for the dominant — focusing on optimizations over specific constraints like Bellman cuts.
>
> **Considering fractional advantages and hereditary constraints**
>
> I’m thinking about how fractional advantages might work here, especially regarding endpoint r and path A. It seems like hereditary constraints over non-path connected sets could enforce some consistency. The relaxation approach could be too permissive, allowing inconsistent choices for internal roots in the search tree. Let's refine this.
>
> **Exploring LP consistency and testing with sparse matrices**
>
> It seems like I’m considering how consistency in edge choices might affect optimal selection in the LP, especially focusing on paths like {1,2,3}. If choosing internal 2, subsets naturally evolve. The idea of a total unimodular LP for nonnegative endpoint costs is interesting. I should test with optimized sparse matrices for smaller trees. Let's avoid timeout.
>
> **Evaluating path constraints and minimum cost relaxation**
>
>
> **Exploring LP duality and tree convexity**
>
> It seems like the tool worked despite not having a Prufer encoding. Now, about the proof for the optimization problem, I’m thinking about proving the integral optimum for nonnegative costs by using dynamic methods. The idea of using tree convexity and greedy algorithms is interesting—perhaps related to antimatroids or “monotone linkage”? I need to derive this cleanly from scratch. I'll also consider rounding methods.
>
> **Working through fractional LP bounds and heredity constraints**
>
> The heredity condition for fractional z values suggests a non-simple relationship between the variables. It seems like a lower bound can be derived using components of the set A-r, factoring in normalized probabilities. And then describing the residual involving the root event, along with the expected costs, should help establish the desired inequality. This might connect to the minimum cost for appropriate sets and components.
>
> **Analyzing recursive cost and path relationships**
>
> For a fixed root \(r\) and subcomponent \(C\) of \(A-r\), calculating the recursive cost involves paths and roots. The key is that the pairs \(u,v\) in \(C\) rely on roots not present on certain paths, especially when deciding ancestor relations. The expected contribution is based on those roots that don't separate \(u,v\) and potentially influence the cost recursively.
>
> **Exploring path terms and heredity assumptions**
>
> I'm working with the terms for pairs \(u,v\) in the path, trying to relate them to expected values (e.g., \(p(P)\)). The idea is to prove that the recursive cost constraint holds. How do these terms translate, and can heredity assumptions about path subsets help us simplify the analysis? There’s a lot to track here.
>
> **Exploring path sums and heredity dependencies**
>
> I'm trying to figure out the sum of \( z_{P(u,v),u} \) for paths where \( r \) lies after \( u \), using chain telescoping. I think heredity conditions might help here, but I’m wondering if fractional cases could break the assumption. I'm considering a branch structure and trying to minimize the LP expression—lots of potential twists!
>
> **Considering conditions for triples and sum behavior**
>
> I'm thinking through the different choices for the edge between \( r \) and \( v \). If the edge selects \( v \), terms might vanish, making the sum 0. I’m exploring a star setup; when \( p_r =
>
> **Exploring quadratic terms and alternative root choices**
>
> I’m noticing that the term \( p_r \geq 1 - p_v \) might be quadratic in terms of \( z_p \), which complicates things. Randomizing the root doesn’t seem to help, so I’m considering choosing a deterministic root \( r \). I'll test this approach with LP, focusing on random trees to check for any failures.
>
> **Testing hereditary LP optimization on random trees**
>
>
> **Outlining next steps and formulating contributions**
>
> I think it’s time to craft an answer while aiming for ambition. I’ll try a combination of conjecture and partial proof, but I must be clear that these aren’t fully verified claims. I also want to derive a new theorem, pushing forward ideas like dominant objects and LP formulations, with definitions and inequalities for clarity.
>
> Thought for 5m 2s

Got it. I’ll keep the original target in view: not just “find cute facts,” but move toward compact/exact relaxations, recursive decompositions, forced inequalities, certificates, and small counterexamples.

# 27. Re-centering: the hull versus the search-objective dominant

The full depth-vector hull is

$$
P(U)=\operatorname{conv}\{d_T:T\text{ valid recursive search tree on }U\}.
$$

But the original objective only uses nonnegative weights:

$$
\min_{d\in P(U)} w\cdot d,\qquad w\ge 0.
$$

So the object that matters for all weighted search objectives is not necessarily $P(U)$ itself, but its **dominant**

$$
D(U)=P(U)+\mathbb R_{\ge 0}^V.
$$

Equivalently,

$$
D(U)=\{x\in\mathbb R^V:\exists d\in P(U)\text{ with }d\le x\}.
$$

This distinction is important because some relaxations may fail to describe the full hull but still give the correct optimum for every $w\ge 0$.

The exact characterization is:

$$
D(U)
=
\{x\in\mathbb R^V: c\cdot x\ge F_c(V)\text{ for every }c\ge 0\},
$$

where

$$
F_c(S)
=
\min_{r\in S}
\left[
\sum_{v\in S\setminus\{r\}}c_v
+
\sum_{C\in\operatorname{comp}(S-r)}F_c(C)
\right].
$$

So the “right” lower inequalities are exactly Bellman inequalities with nonnegative coefficient vectors.

This is already stronger than the previous full-hull support theorem in the direction the original search objective actually cares about.

---

# 28. Exact dominant LP

The branching-flow formulation from before gives an exact LP for the dominant too.

Variables:

$$
x_{S,r}\ge 0
\qquad
(S\subseteq V\text{ connected},\ r\in S).
$$

Flow constraints:

$$
\sum_{r\in V}x_{V,r}=1,
$$

and for every $S\neq V$,

$$
\sum_{r\in S}x_{S,r}
=
\sum_{\substack{R,q:\\S\in\operatorname{comp}(R-q)}}x_{R,q}.
$$

Depth projection:

$$
\widehat d_v
=
\sum_{\substack{S\ni v}}
\sum_{\substack{r\in S\\r\neq v}}x_{S,r}.
$$

Then the dominant is described by

$$
\widehat d_v\le d_v
\qquad(v\in V).
$$

So:

$$
D(U)=
\left\{
d:\exists x\ge 0\text{ satisfying branching flow and }\widehat d\le d
\right\}.
$$

This LP is exact for every nonnegative weighted-depth objective.

Moreover, the $x$-polytope is integral in the extended space, so the only source of non-integrality after projection is the intended convexification over search trees.

---

# 29. A strong local restriction theorem

Here is a useful structural fact that gives many forced inequalities.

Let $T$ be a valid recursive search tree on $U$, and let $S\subseteq V$ be connected. Restrict the search process to $S$. Equivalently, take an inducing permutation for $T$, then restrict that permutation to $S$.

The resulting recursive search tree is valid on $U[S]$.

Furthermore, if $d_T$ is the global depth vector and $d_{T|S}$ is the local depth vector on $S$, then

$$
d_T(v)\ge d_{T|S}(v)
\qquad(v\in S).
$$

Reason: local depth counts only ancestors lying inside $S$, whereas global depth counts all ancestors.

Therefore, for every connected $S\subseteq V$ and every $c\in\mathbb R_{\ge 0}^S$,

$$
\sum_{v\in S}c_v d_v
\ge
F_c(S).
$$

This is a large family of valid inequalities:

$$
\boxed{
\sum_{v\in S}c_v d_v
\ge
F_c(S)
\qquad
(S\text{ connected},\ c\ge 0).
}
$$

The forest inequalities are only the special case $c_v=1$ with the crude bound

$$
F_{\mathbf 1}(S)\ge |S|-1.
$$

The Bellman inequality gives the sharp right-hand side.

---

# 30. Root-face inequalities as Bellman cuts

The earlier lifted inequalities now become a systematic construction.

For connected $S$, nonnegative $c$, and a chosen candidate root $q$, define

$$
B_c(S,q)
=
\sum_{v\in S\setminus\{q\}}c_v
+
\sum_{C\in\operatorname{comp}(S-q)}F_c(C).
$$

Then

$$
F_c(S)=\min_{q\in S}B_c(S,q).
$$

Thus the valid inequality

$$
\sum_{v\in S}c_v d_v\ge F_c(S)
$$

says:

> No matter how the recursive search tree behaves globally, its restriction to $S$ pays at least the best Bellman root cost inside $S$.

For example, on $P_4=1-2-3-4$, take

$$
c=(4,2,1,1).
$$

Then the inequality

$$
4d_1+2d_2+d_3+d_4\ge F_c(P_4)
$$

is valid. Computing the Bellman values gives

$$
F_c(P_4)=7,
$$

so

$$
4d_1+2d_2+d_3+d_4\ge 7.
$$

This recovers the nontrivial $P_4$ inequality from a general rule rather than ad hoc lifting.

---

# 31. A stronger “certificate theorem” for optima

For nonnegative weights $w$, define

$$
F_w(S)
=
\min_T\sum_{v\in S}w_vd_T(v).
$$

Then a recursive search tree $T$ is globally optimal iff, at every subproblem $S$ appearing in $T$, its chosen root $r$ satisfies

$$
r\in
\arg\min_{q\in S}
\left[
W(S)-w_q
+
\sum_{C\in\operatorname{comp}(S-q)}F_w(C)
\right].
$$

Equivalently,

$$
r\in
\arg\max_{q\in S}
\left[
w_q
-
\sum_{C\in\operatorname{comp}(S-q)}F_w(C)
\right].
$$

So the exact local root score is

$$
\Gamma_S(q)
=
w_q-
\sum_{C\in\operatorname{comp}(S-q)}F_w(C).
$$

This gives a complete certificate:

1. list the recursive subproblems $S$;
2. list the chosen roots $r(S)$;
3. provide the values $F_w(C)$ for all comparison components;
4. verify

$$
\Gamma_S(r(S))\ge \Gamma_S(q)
\qquad(q\in S).
$$

This is a genuine local optimality theorem, not a heuristic exchange condition.

---

# 32. A sharper compactness theorem

The branching-flow formulation has size proportional to

$$
\sum_{S\in\mathcal C(U)}|S|,
$$

where $\mathcal C(U)$ is the set of connected induced subtrees.

Thus:

$$
\boxed{
\text{If }U\text{ has polynomially many connected induced subtrees, then }D(U)\text{ and }P(U)\text{ have polynomial-size exact extended formulations.}
}
$$

This covers:

- paths;
- fixed-leg spiders;
- subdivisions of a fixed finite tree skeleton;
- trees with a bounded number of leaves;
- more generally, any family where connected induced subtrees admit a polynomial encoding.

This gives a real answer to one of the original questions:

> Can the depth-vector hull be described by a compact LP for useful families?

Yes: for every family with polynomially many connected induced subtrees, via the integral branching-flow formulation.

---

# 33. The path case as a fully explicit theorem

For $P_n$, connected subtrees are intervals $[i,j]$. Variables:

$$
x_{i,j,r}\ge 0
\qquad
i\le r\le j.
$$

Root constraint:

$$
\sum_{r=1}^n x_{1,n,r}=1.
$$

Interval-flow constraints:

$$
\sum_{r=i}^j x_{i,j,r}
=
\sum_{a<i}x_{a,j,i-1}
+
\sum_{b>j}x_{i,b,j+1}
$$

for every proper interval $[i,j]\neq[1,n]$.

Depth projection:

$$
\widehat d_v
=
\sum_{i\le v\le j}
\sum_{\substack{r=i\\r\neq v}}^j x_{i,j,r}.
$$

Hull:

$$
P(P_n)=
\{\widehat d:x\text{ satisfies interval flow}\}.
$$

Dominant:

$$
D(P_n)=
\{d:\exists x\text{ satisfying interval flow and }\widehat d\le d\}.
$$

This is an exact integral extended formulation of size $O(n^3)$.

So paths are essentially solved from the convex-relaxation perspective.

---

# 34. What the hereditary path-minimum relaxation is trying to do

Recall the tempting relaxation with variables

$$
z_{A,r},
$$

where $z_{A,r}$ means “$r$ is the earliest/root vertex of connected set $A$.”

Constraints:

$$
\sum_{r\in A}z_{A,r}=1,
$$

and heredity:

$$
z_{A,r}\le z_{B,r}
\qquad(B\subseteq A,\ r\in B).
$$

Depth projection:

$$
d_v=\sum_{u\neq v}z_{P(u,v),u}.
$$

The integer version is exact.

The LP relaxation is not full-hull exact. We already found a five-vertex fractional point outside the hull in a mixed-sign direction.

But the key unresolved question is sharper:

> Is this relaxation exact for every nonnegative weighted-depth objective?

Equivalently:

$$
\min_{z\text{ hereditary}}
\sum_{u\neq v}w_v z_{P(u,v),u}
\stackrel{?}{=}
\min_T\sum_v w_vd_T(v)
\qquad(w\ge0).
$$

This is now one of the best ambitious targets, because if true, it gives a conceptually simpler objective-exact relaxation than the connected-subproblem branching-flow LP.

---

# 35. Partial progress toward the hereditary-relaxation conjecture

The conjecture can be reframed using dominants.

Let $Q(U)$ be the projection of the hereditary $z$-LP into depth space. We know

$$
P(U)\subseteq Q(U),
$$

but generally

$$
Q(U)\not\subseteq P(U).
$$

The objective-exactness conjecture is precisely:

$$
Q(U)\subseteq D(U).
$$

That is:

> Every fractional hereditary depth vector is coordinatewise at least some convex combination of true recursive-search depth vectors.

This is the right geometric formulation.

The earlier mixed-sign counterexample only proves

$$
Q(U)\not\subseteq P(U).
$$

It does **not** prove

$$
Q(U)\not\subseteq D(U).
$$

So the relaxation may still be exactly right for all $w\ge0$.

This is a clean frontier question.

---

# 36. A useful sufficient condition for proving $Q(U)\subseteq D(U)$

To prove $Q(U)\subseteq D(U)$, it would suffice to show:

For every feasible hereditary $z$ and every connected $S\subseteq V$, every $c\ge0$ satisfies

$$
\sum_{v\in S} c_v d_v(z)\ge F_c(S).
$$

Because the Bellman inequalities with $c\ge0$ describe the dominant.

Expanding $d_v(z)$, this becomes

$$
\sum_{v\in S}c_v
\sum_{u\neq v}z_{P(u,v),u}
\ge
F_c(S).
$$

Restricting attention to $u,v\in S$, it would be enough to show

$$
\sum_{\substack{u,v\in S\\u\neq v}}
c_v z_{P(u,v),u}
\ge
F_c(S).
$$

So the key lower-bound statement is:

$$
\boxed{
\text{Every hereditary fractional path-minimum system pays at least the Bellman cost on every connected }S.
}
$$

If this can be proved, the hereditary relaxation is objective-exact.

This is a crisp target.

---

# 37. Where such a proof would have to come from

A naive proof would try to sample the root $r$ of $S$ according to $z_{S,r}$. Heredity gives

$$
z_{P(r,v),r}\ge z_{S,r},
$$

so the immediate root contribution satisfies

$$
\sum_{v\neq r}c_vz_{P(r,v),r}
\ge
z_{S,r}\sum_{v\neq r}c_v.
$$

Averaging over $r$, one obtains the right kind of first-level contribution:

$$
\sum_r z_{S,r}\sum_{v\neq r}c_v.
$$

The hard part is the recursive remainder. If root $r$ is sampled, then pairs $u,v$ lying in the same component of $S-r$ should pay recursively. But the same pair $(u,v)$ may survive many possible root choices $r\notin P(u,v)$. One needs to show that the hereditary constraints provide enough residual mass to pay all these recursive continuation costs.

So the missing lemma has the flavor of a conservation law:

> Fractional root mass that does not separate a path must be chargeable to later path-minimum mass on that path.

That is the technical heart of the conjecture.

---

# 38. A smaller theorem worth proving first

Before trying arbitrary trees, prove it for paths.

For a path interval $[i,j]$, the hereditary variables are

$$
z_{[a,b],r}
\qquad
a\le r\le b.
$$

The conjectured path theorem is:

$$
\min_{z\text{ hereditary on intervals}}
\sum_{u\neq v}w_v z_{[u,v],u}
=
F_w([1,n])
\qquad(w\ge0).
$$

If true, this would give a simpler exact relaxation for optimal binary-search-tree-style depth objectives.

For paths, the missing conservation law should become one-dimensional. Root mass outside an interval $[u,v]$ either lies to the left or right and does not affect the path between $u$ and $v$. This suggests a possible telescoping proof using nested intervals.

A plausible strategy:

1. Prove the claim for intervals by induction on length.
2. For a feasible hereditary $z$, choose a root distribution $p_r=z_{[i,j],r}$.
3. Use heredity to pay the first-level cost.
4. Show that the remaining path-minimum terms dominate

$$
\sum_r p_r\left(F_w([i,r-1])+F_w([r+1,j])\right).
$$

The obstacle is step 4, but in one dimension the surviving pairs are exactly those on the same side of $r$, and the relevant intervals are nested. That nesting may make the needed inequality provable by summation by parts.

This path theorem is the next best subtarget.

---

# 39. Another ambitious direction: quotienting the branching-flow LP by symmetry

The connected-subproblem LP is exact but can be exponentially large for stars because a star has exponentially many connected subtrees containing arbitrary subsets of leaves.

However, the star hull is compact because the leaves are symmetric.

This suggests a general compression principle.

Suppose a tree $U$ has an automorphism group $G$. Connected subproblems lying in the same $G$-orbit should be aggregatable for symmetric objectives or symmetric hull projections.

For stars, this quotient collapses arbitrary leaf subsets to their cardinality.

For a star with center $c$ and $m$ leaves, the state is just

$$
k=\text{number of leaves still attached to }c.
$$

The root choice has two types:

1. choose the center;
2. choose one of the $k$ leaves.

This yields a compact quotient branching-flow LP with $O(m)$ states instead of $2^m$.

That quotient recovers the earlier permutahedral description.

So another serious theorem target is:

> If connected subproblems of $U$ have polynomially many orbits under automorphisms preserving the relevant vertex classes, then symmetric slices of $P(U)$ and $D(U)$ have compact exact quotient LPs.

This would explain paths by few subproblems and stars by symmetry.

---

# 40. Current best frontier

The strongest clean package now is:

## Fully proved

1. **Exact branching-flow LP.**  
   The depth hull $P(U)$ is the projection of an integral recursive occupancy polytope.

2. **Exact dominant LP.**  
   The search-objective dominant $D(U)=P(U)+\mathbb R_{\ge0}^V$ is obtained by replacing equality projection with $\widehat d\le d$.

3. **Exact Bellman inequalities.**  
   For every connected $S$ and every $c\ge0$,

   $$
   \sum_{v\in S}c_vd_v\ge F_c(S)
   $$

   is valid, and the full dominant is described by these inequalities.

4. **Exact local optimality certificates.**  
   A tree is optimal for $w\ge0$ iff every recursive root maximizes

   $$
   \Gamma_S(r)
   =
   w_r-\sum_{C\in\operatorname{comp}(S-r)}F_w(C).
   $$

5. **Compact exact LPs for useful families.**  
   Paths, bounded-leaf trees, fixed-skeleton subdivisions, and fixed-leg spiders have polynomial-size exact formulations through connected-subproblem branching flow.

## Ambitious open targets

1. **Hereditary path-minimum objective-exactness.**

   Prove or refute:

   $$
   Q(U)\subseteq D(U).
   $$

   Equivalently, prove that every feasible hereditary $z$-solution satisfies every nonnegative Bellman inequality.

2. **Path version first.**

   Prove the hereditary relaxation exact for $P_n$ using interval nesting/telescoping.

3. **Symmetry quotient theorem.**

   Generalize the star compression: if connected subproblems have few symmetry types, quotient the branching-flow LP.

4. **Facet generation for paths.**

   Characterize the nonnegative lower facets of $P(P_n)$ or $D(P_n)$ via recursively lifted Bellman cuts.

My current assessment: the most promising ambitious line is not to chase arbitrary full-hull facets. It is to prove $Q(U)\subseteq D(U)$, or at least prove it for paths. That would give a cleaner relaxation that is not full-hull exact but is exactly right for the original weighted search objective.

## Prompt:
5/15/2026, 4:46:22 PM

Let's follow up with another even more ambitious frontier push. No need to claim a proof of things you're not confident in but I'll be slowly ratcheting up the ambition until we hit brick wall after brick wall after brick wall; this is to prevent misappraising the problem as too difficult too quickly and prematurely funneling into a workflow where we're proving true but very small things in a tiny corner of the problem when we should still be thinking bigger.

## Response:
5/15/2026, 4:46:29 PM

> **Exploring math problem with computations and reasoning**
>
> The user is asking for a math exploration, focusing on a problem related to hereditary path-min relaxation. It seems no web searching is allowed. I think I can test examples using private Python computation, likely working on small instances. Let's step through the problem, perhaps trying to prove a larger theorem, and explore it with reasoning and some computational tools, like LP with scipy.
>
> **Exploring hereditary path-min relaxation with LP optimization**
>
>
> **Implementing dynamic programming and hereditary LP**
>
> I’m planning to implement dynamic programming (DP) and hereditary LP with tree adjacency. I’ll define connected subsets and variables with constraints. The objective will be minimizing the sum for the path-min problem. I'll generate small unlabeled trees and use linear programming for comparisons, plus recursion for DP over connected subsets.
>
> **Implementing true DP and hereditary LP for trees**
>
>
> **Generating random trees and using LP for optimization**
>
> I need to generate random trees for small n values, starting with n=5. I'll use Prüfer sequences for labeled trees, and since 5^3 = 125, that’s feasible. I'll explore linear programming (LP) over connected subsets to compare against true dynamic programming, while also checking for any violations of Bellman inequalities. Random weights should suffice for this.
>
> **Generating and labeling all trees via Prufer**
>
>
> **Searching labeled trees with random weights and LP**
>
>
> **Testing with n=6 due to cost considerations**
>
> It’s interesting. Testing with n=6 sounds promising but could be too costly, so I'll need to weigh the potential value against the expense. I'll start with smaller instances to see how far I can go without escalating costs too quickly. Let's stay mindful of that cost factor for now.
>
> **Evaluating search counter with sampled data**
>
>
> **Proving objective exactness and verifying hereditary relaxation**
>
> I’m thinking about proving the objective for hereditary relaxation, which might hold true. I’ll review the formulation carefully and we might derive the dual of the hereditary LP to match Bellman’s inequalities. I’ll verify if the choice function satisfies conditions and recurse modeling over paths. It’s tricky, but worth exploring!
>
> **Testing hull and objective optimization**
>
> I’m thinking of testing by projecting the depth and comparing it with the true hull for P4. I’ll use linear programming (LP) with signed objectives for random values, checking if the relaxation option is less than the true objective. For the path-min objective, it’ll correspond to the sum of values in c*d. Let's try it out.
>
> **Testing relaxation of signed objective optimization**
>
>
> **Testing hereditary relaxation and path properties**
>
> I think hereditary relaxation might equate to the hull for paths. I need to explore the polytope vertices and verify if the LP matrix for intervals is integral—maybe yes. For path-min choice function constraints involving intervals, the polytope could be integral. I’ll test this on random P4 objectives and check trees, too.
>
> **Exploring convex hull of ultrametric functions**
>
> The constraints seem to define the convex hull of ultrametric or min-choice functions on intervals. I want to attempt a proof using variables z_{I,r}, with specific constraints. I'm considering testing this with n=4 to enumerate potential vertices, maybe using a random objective. If the polytope is integral, that’s promising. I'll investigate further.
>
> **Understanding interval root dependencies**
>
> I’m thinking about how the subinterval choices for the variable `z` relate to intervals on the left or right. I could define conditional variables like `z^{(r, L)}` for an interval to focus on the roots of subintervals. The way roots behave whether inside or outside the interval might need clearer separation, especially for recursive policies.
>
> **Exploring conditional distributions and regular intervals**
>
> I’m thinking about recursion for components where a root is outside of an interval. The distribution for choice probabilities in intervals could be characterized using a "random priority representation." For intervals, the idea might hold because they involve interval-specific orders, so an inductive approach could work, particularly with root distribution in mind.
>
> **Considering choice probabilities and branching flows for path-min cost**
>
> I’m considering how to handle residuals for outside roots and conditional systems on intervals. There's a lot about choice probabilities linked to regularity, but I think the BM inequalities could play a role. The approach gets more complex with fractional scenarios, so I’ll need to test with larger values for n.
>
> **Expressing probabilities in recursive interval search**
>
> I’m considering how to express the probability z from occupancy x, especially in recursive interval searches where the root of interval I could be r, even if I’m not a direct subproblem. The goal is to calculate z_{I,r}, which is the total probability for a root r within I before other roots in I are chosen.
>
> **Working with interval probabilities and Möbius inversion**
>
> I’m defining the formula z_{I,r} as the sum over intervals J containing I, with r as the root of J. This leads to a linear transformation of x to z. I'm considering inverting this for path scenarios with Möbius inversion, evaluating how different intervals affect probability calculations based on variable roots.
>
> **Testing feasibility with Möbius inversion and LP**
>
> I’m testing whether \( z_{a-1,b+1,r} \) is greater than or equal to \( z_{a-1,b,r} + z_{a,b+1,r} \). If hereditary lacks this, I might not be catching all random costs. I'll explore negative Möbius inversion for paths and use linear programming (LP) to minimize the Möbius values.
>
> **Evaluating hereditary property in path optimization**
>
>
> **Inspecting depth projection and solutions**
>
> I’m wondering if path hereditary is equal to the convexity of branching flow \( z \). It seems like I still need to explore depth projections further, maybe more precisely. I'll look into a bad solution and, for \( n=4 \), try minimizing \( x_{[1,2],1} \) to see how it works.
>
> **Minimizing path hereditary for n=4**
>
>
> **Checking if point is in the path P4 hull**
>
> I need to check if \( d = (1, 1.5, 1.5, 1.5) \) is inside the path P4 hull. The search for a signed objective didn’t identify it, which might mean it's inside the hull. I'll solve the membership by examining the convex hull's vertices.
>
> **Checking membership in convex hull via vertices**
>
>
> **Exploring hereditary objective and LP testing**
>
> I need to continue further and consider search for a nonnegative counter, or possibly derive the exact "submodular closure" for paths. This could involve adding nonnegativity constraints to Möbius for intervals, linking it back to branching-flow LP. It's ambitious but promising! I'll test it systematically via LP for all trees where \(n \leq 5\).
>
> **Expanding induction and recursive terms**
>
> I need to cover the recursive cost for path components. The idea is to prove that the function L(S) satisfies certain inequalities by applying Bellman bounds to paths within components. The goal is to show that, for each pair \( u, v \) in the same component, the recursive expressions hold, including verifying that the sum terms involving local costs align. I’ll continue expanding on this.
>
> **Refining recursive cost calculation**
>
> I’m trying to calculate and refine the recursive cost expression by comparing terms on both sides and adjusting coefficients. The challenge comes from how cross terms (with roots inside \( P \)) might contribute slack. I need to prove whether the left-hand side can be bounded by the right-hand side, especially in cases with star graphs. I’ll continue to work through these path terms.
>
> **Testing inequality for random feasible z**
>
> I'm considering the potential lemma for any connected set \( S \) and vertex \( v \). It states that \( \sum_{u \neq v} z_{Puv,u} p(Puv) \geq 1 - p_v \) where \( p_r = z_{S,r} \). This could be true, and I should test it using LP for small trees to check the validity.
>
> **Evaluating hereditary polytope for tree inequalities**
>
>
> **Exploring alternative methods for counterexample**
>
> The lemma may be false for path n=5, but I think the induction might still hold if weighted differently across \( c \) and \( F \) instead of \( L \). I need to inspect the solution for path n=5 and maybe investigate a dual approach for a nonnegative counter. I’ll also consider testing with path n=7 using LP.
>
> **Searching for counterexamples in path solutions**
>
>
> **Correcting the search counter approach**
>
> Oops, it looks like the search_counter samples were based on a labeled tree, not a path. I need to redefine the approach, specifically for paths, so I can get the correct samples and results. I’ll adjust the method accordingly.
>
> **Searching for counterexample edges in tree optimization**
>
>
> **Testing non-path search for n=6-7**
>
> Alright, I'll try running a search on non-path cases for n=6-7 using random samples. This should give a different perspective and might help identify any patterns or potential solutions I hadn't considered yet. Let's see what comes up!
>
> **Searching non-path random labeled trees**
>
>
> **Formulating a final answer after system timeout**
>
> It looks like I lost all variables due to a timeout error. The code wasn’t executed, so no outputs can be assumed. Still, I can formulate a final answer—possibly including computations from a small LP experiment. I should be careful when mentioning the words "private computation" and might aim to derive Bellman inequalities as a new theorem. Let me verify this.
>
> **Evaluating root choices for connected subsets**
>
> I'm considering whether F_c(V) could be less than or equal to F_c(S). If c is supported in S but includes vertices from outside, the optimum might choose an outside root to increase depth. However, this isn't helpful because such a choice adds weight and doesn't separate S. It seems F_{c supported S}(V) might actually equal F_c(S).
>
> **Evaluating Steiner root choices and optimization**
>
> I'm analyzing a situation where for c>=0, with support A possibly disconnected, F_c(V) equals F_c(H), meaning H is a minimal connected subtree spanning A. If there are zero leaves in H, I'm thinking about how choosing an outside root may add extra weight but not separate support. Choosing zero Steiner vertices as separators can sometimes be beneficial, though not always. It seems using zero separators isn't always optimal.
>
> **Considering root-comparison inequality and optimization**
>
> I'm wondering about a "root-comparison inequality," where the root is one of the positive vertices. Zero roots might still be optimal if they split several positive components. For example, in a star configuration with weighted leaves, choosing the center or a leaf might have nearly the same cost. So, zero separators might actually be optimal in some cases. This leads me to consider more ambitious approaches, like dominant Bellman inequalities.
>
> **Exploring tree search problem complexity**
>
> I'm thinking about the "tree search problem" and whether it's NP-hard. DP over connected subsets suggests a potentially NP-hard approach for general trees, but I can't make that claim without a proof yet. Maybe constructing a reduction would be too complex. What if it's related to set cover? I'll need to explore known algorithms—since for some trees, there could be a polynomial solution.
>
> **Exploring LP formulations and combinatorial extensions**
>
> I'm pondering whether a "minimum height vertex ranking" of trees could be polynomial, or if it could involve a weighted average. Not quite sure at this point, so I'll back off for now. If there's a way to derive a "separator-root LP," maybe I can prove some formulation for stars and explore constraints. There's also a potential for an extended formulation with weighted optimization—all said, should I pursue the bigger conjecture approach here?
>
> **Exploring branching-flow relationships in objective optimization**
>
> I've been thinking about conditional residual variables—how they differ from simple marginals (like z). Q might still be objective-exact, but simple induction is insufficient. I wonder if a stronger relaxation, R, with "conditional path-minimum variables," could be exact and smaller. The relationship between x and z seems key, especially with the hereditary constraints. This could lead to more specific flow constraints.
>
> Thought for 5m 37s

I’ll push at the “maybe too big but worth testing” level: try to either collapse the dominant $D(U)$ into a smaller family of inequalities, or break the promising hereditary relaxation with a genuinely nonnegative objective.

Yes. Let’s keep ratcheting up.

I’ll aim for a stronger structural synthesis:

> The natural ancestry/path-minimum variables are not the wrong variables. They are missing higher-order “complete monotonicity” constraints. Once those are added, they become exactly equivalent to the recursive branching-flow formulation. For paths, these missing constraints become explicit second-difference inequalities, giving a compact exact LP in path-minimum/ancestry variables rather than abstract subproblem-flow variables.

This is a meaningful frontier push because it tries to bridge the original desiderata:

- variables encoding ancestry / separation / recursive roots;
- exact hull or dominant;
- compact LPs for useful families;
- precise diagnosis of why tempting relaxations fail.

---

# 41. First-hit variables

For every connected set $A\subseteq V$ and $r\in A$, define

$$
z_{A,r}=1
$$

to mean:

$$
r\text{ is the first/root vertex of }A
$$

when the global recursive search process is restricted to $A$.

Equivalently, if a search tree is generated by a total order $\prec$, then

$$
z_{A,r}=1
\iff
r=\min_\prec A.
$$

For a distribution over search trees, $z_{A,r}$ is the probability that $r$ is the earliest vertex of $A$.

These are very natural variables. They directly encode ancestry:

$$
u\text{ is an ancestor of }v
\iff
u\text{ is earliest on }P(u,v).
$$

Therefore

$$
a_{uv}=z_{P(u,v),u},
$$

and

$$
d_v=\sum_{u\neq v} z_{P(u,v),u}.
$$

So depth is an extremely clean linear projection of the $z$-variables.

This suggests that the “right” relaxation should live in $z$-space.

---

# 42. Exact relation between branching-flow variables and first-hit variables

Recall the exact branching-flow variables

$$
x_{S,r},
$$

where

$$
x_{S,r}
=
\Pr(S\text{ occurs as a recursive subproblem and chooses root }r).
$$

Now fix a connected set $A$ and $r\in A$. The event

$$
r\text{ is first in }A
$$

happens exactly when, during the recursive process, the first active subproblem whose chosen root lies inside $A$ chooses $r$.

Before that moment, the current subproblem must contain all of $A$. Hence:

$$
\boxed{
z_{A,r}
=
\sum_{\substack{S\in\mathcal C(U):\\ A\subseteq S}}
x_{S,r}.
}
$$

This is a key identity.

The hereditary relaxation only remembers the easy consequence:

if $B\subseteq A$ and $r\in B$, then

$$
z_{A,r}\le z_{B,r}.
$$

Indeed, being first in the larger set $A$ implies being first in the smaller set $B$.

But this monotonicity is only a first-order shadow of the exact relation

$$
z_{A,r}
=
\sum_{S\supseteq A}x_{S,r}.
$$

The exact relation imposes higher-order inclusion-exclusion constraints.

That is likely the true source of the gap.

---

# 43. Complete monotonicity: the missing constraint family

Fix $r$. Consider the poset

$$
\mathcal C_r=\{A\subseteq V:A\text{ connected and }r\in A\},
$$

ordered by inclusion.

For fixed $r$, the exact relation is

$$
z_A=\sum_{S\supseteq A}x_S.
$$

This is a zeta transform on the connected-subtree poset.

Therefore, by Möbius inversion,

$$
x_S
=
\sum_{A\supseteq S}\mu(S,A)z_A,
$$

where $\mu$ is the Möbius function of the poset $\mathcal C_r$.

So exactness in $z$-space requires:

$$
\boxed{
\sum_{A\supseteq S}\mu(S,A)z_{A,r}\ge 0
\qquad(S\in\mathcal C_r).
}
$$

These are the complete-monotonicity constraints.

Then one also needs the recursive flow constraints on the recovered $x$’s:

$$
\sum_{r\in S}x_{S,r}
=
\sum_{\substack{R,q:\\S\in\operatorname{comp}(R-q)}}x_{R,q}.
$$

Thus:

> The exact $z$-polytope is obtained by taking first-hit variables, imposing simplex constraints, imposing complete monotonicity via Möbius inversion, and imposing branching-flow conservation on the recovered $x$-variables.

This is a much sharper diagnosis than “ancestry variables are weak.”

The natural ancestry variables are right; first-order heredity is weak.

---

# 44. Exact path formulation in first-hit variables

Now specialize to a path

$$
1-2-\cdots-n.
$$

Connected sets are intervals $[i,j]$. Use variables

$$
z_{i,j,r}
\qquad
i\le r\le j.
$$

Interpretation:

$$
z_{i,j,r}
=
\Pr(r\text{ is earliest in interval }[i,j]).
$$

Depth projection:

$$
d_v
=
\sum_{u<v} z_{u,v,u}
+
\sum_{u>v} z_{v,u,u}.
$$

The exact relation with branching-flow variables is

$$
z_{i,j,r}
=
\sum_{\substack{a\le i\\b\ge j}}
x_{a,b,r}.
$$

So by two-dimensional Möbius inversion,

$$
\boxed{
x_{i,j,r}
=
z_{i,j,r}
-
z_{i-1,j,r}
-
z_{i,j+1,r}
+
z_{i-1,j+1,r}.
}
$$

Use the convention that invalid $z$-terms are $0$.

Thus the exact interval-minimum LP is:

$$
\sum_{r=i}^j z_{i,j,r}=1
\qquad(1\le i\le j\le n),
$$

$$
x_{i,j,r}
=
z_{i,j,r}
-
z_{i-1,j,r}
-
z_{i,j+1,r}
+
z_{i-1,j+1,r},
$$

$$
x_{i,j,r}\ge 0,
$$

and interval-flow conservation:

$$
\sum_{r=i}^j x_{i,j,r}
=
\sum_{a<i}x_{a,j,i-1}
+
\sum_{b>j}x_{i,b,j+1}
$$

for every proper interval $[i,j]\neq[1,n]$, plus

$$
\sum_{r=1}^n x_{1,n,r}=1.
$$

Then

$$
d_v
=
\sum_{u<v} z_{u,v,u}
+
\sum_{u>v} z_{v,u,u}.
$$

This is an exact compact LP for the path depth hull using ancestry/path-minimum variables.

Size:

$$
O(n^3)
$$

variables and constraints.

This is stronger than the previous interval-flow formulation because it says exactly what extra constraints the natural ancestry relaxation needs.

---

# 45. The first-order hereditary relaxation versus the exact path formulation

The hereditary relaxation for paths says only:

$$
z_{i,j,r}\le z_{a,b,r}
$$

whenever

$$
[i,j]\supseteq [a,b]\ni r.
$$

This is implied by

$$
x_{i,j,r}\ge 0
$$

after summing over larger intervals, but it is weaker.

The exact path formulation requires the mixed second differences

$$
z_{i,j,r}
-
z_{i-1,j,r}
-
z_{i,j+1,r}
+
z_{i-1,j+1,r}
\ge 0.
$$

These are the path version of complete monotonicity.

So the hierarchy is:

$$
\text{exact branching flow}
\iff
\text{complete-monotone first-hit variables}
\implies
\text{hereditary first-hit variables}.
$$

The last implication is strict.

---

# 46. Small concrete failure of first-order heredity

On $P_4=1-2-3-4$, define the following fractional interval-minimum variables:

$$
z_{1,2,1}=z_{1,2,2}=\frac12,
$$

$$
z_{2,3,2}=z_{2,3,3}=\frac12,
$$

$$
z_{3,4,3}=z_{3,4,4}=\frac12,
$$

$$
z_{1,3,1}=z_{1,3,2}=\frac12,
$$

$$
z_{2,4,2}=z_{2,4,4}=\frac12,
$$

$$
z_{1,4,1}=z_{1,4,4}=\frac12,
$$

with singleton intervals choosing their unique vertex.

This satisfies simplex and hereditary constraints.

But compute the Möbius-recovered branching-flow variable

$$
x_{2,3,2}
=
z_{2,3,2}
-
z_{1,3,2}
-
z_{2,4,2}
+
z_{1,4,2}.
$$

The values are

$$
z_{2,3,2}=\frac12,\qquad
z_{1,3,2}=\frac12,\qquad
z_{2,4,2}=\frac12,\qquad
z_{1,4,2}=0.
$$

Therefore

$$
x_{2,3,2}
=
\frac12-\frac12-\frac12+0
=
-\frac12.
$$

So this $z$-solution cannot come from any distribution over recursive search trees.

This pinpoints the exact missing condition.

First-order heredity says probabilities should decrease when intervals grow. But exactness also requires the two-dimensional inclusion-exclusion masses to be nonnegative.

---

# 47. Why this does not yet kill objective-exactness

The above $z$-solution is not exact in first-hit space. But its depth vector is

$$
d=(1,\tfrac32,\tfrac32,\tfrac32).
$$

That depth vector lies in the true path hull.

So this example proves:

$$
\text{hereditary }z\text{-polytope is too large in }z\text{-space},
$$

but it does not prove:

$$
\text{hereditary depth projection is too large}.
$$

This is an important brick wall.

A relaxation can be wrong in the auxiliary variables while still projecting correctly onto depths, or at least still giving the right nonnegative objective optimum.

So the current ambitious conjecture remains alive:

$$
Q(U)\subseteq D(U)?
$$

Equivalently:

> Does first-order heredity, though too weak in $z$-space, still imply all nonnegative Bellman depth inequalities after projection?

I do not have a proof. But the complete-monotonicity analysis clarifies exactly why the obvious proof attempt fails.

---

# 48. The almost-proof of $Q(U)\subseteq D(U)$, and where it breaks

Let $S$ be connected and $c\ge 0$. We want to prove

$$
\sum_{v\in S}c_vd_v(z)\ge F_c(S).
$$

Let

$$
p_r=z_{S,r}.
$$

The Bellman recurrence says

$$
F_c(S)
\le
\sum_{r\in S}p_r
\left[
\sum_{v\neq r}c_v
+
\sum_{C\in\operatorname{comp}(S-r)}F_c(C)
\right].
$$

So it would suffice to prove

$$
\sum_{v\in S}c_vd_v(z)
\ge
\sum_{r\in S}p_r
\left[
\sum_{v\neq r}c_v
+
\sum_C F_c(C)
\right].
$$

The first-level term is easy.

For every $r\neq v$,

$$
P(r,v)\subseteq S,
$$

so heredity gives

$$
z_{P(r,v),r}\ge z_{S,r}=p_r.
$$

Therefore

$$
\sum_{r\neq v}c_vz_{P(r,v),r}
\ge
\sum_{r\neq v}c_vp_r.
$$

This pays for the immediate Bellman cost.

The hard part is paying for the recursive terms

$$
\sum_r p_r\sum_C F_c(C).
$$

Intuitively, if root $r$ is outside a path $P(u,v)$, then $u$ and $v$ remain in the same component and the pair should still be available to pay recursively. But the hereditary variables only give marginal first-hit probabilities. They do not track the conditional residual mass after roots outside $P(u,v)$ have been chosen.

This is precisely the missing complete-monotonicity information.

So the attempted induction breaks because it tries to reuse the same marginal path mass under many possible top-root conditionings.

This is the brick wall.

---

# 49. A repaired exact relaxation: conditional first-hit variables

The previous failure suggests a stronger but still natural relaxation.

Instead of only recording

$$
z_{A,r}=\Pr(r\text{ first in }A),
$$

record conditional first-hit variables

$$
z^{S}_{A,r}
$$

for

$$
A\subseteq S,
$$

where

$$
z^{S}_{A,r}
=
\Pr(r\text{ is the first vertex of }A\mid S\text{ is the current recursive subproblem}).
$$

Then the recursion becomes local:

$$
z^{S}_{A,r}
=
\mathbf 1_{r\in A}\cdot p_S(r)
+
\sum_{\substack{q\in S\setminus A:\\ A\subseteq C_q}}
p_S(q)\, z^{C_q}_{A,r},
$$

where $C_q$ is the component of $S-q$ containing $A$.

This is exact but large.

However, it identifies what is missing from the hereditary relaxation: conditional residual first-hit distributions.

The branching-flow $x$-formulation is a compressed way of tracking exactly this information.

So we now have three levels:

1. **Hereditary first-hit LP:** natural, small-ish in variables, maybe objective-exact, but not known.
2. **Complete-monotone first-hit LP:** exact, equivalent to branching flow.
3. **Conditional first-hit recursion:** conceptually exact, explains the probabilistic semantics.

---

# 50. General exact first-hit formulation

For arbitrary base tree $U$, define

$$
z_{A,r}
=
\sum_{\substack{S\supseteq A\\S\text{ connected}}}x_{S,r}.
$$

Then:

$$
d_v
=
\sum_{u\neq v}z_{P(u,v),u}.
$$

Let $M_r$ be the Möbius inversion operator on the poset of connected sets containing $r$. Define

$$
x_{S,r}
=
(M_r z_{\bullet,r})(S).
$$

Then the exact hull is described by:

$$
x_{S,r}\ge 0,
$$

$$
\sum_{r\in V}x_{V,r}=1,
$$

$$
\sum_{r\in S}x_{S,r}
=
\sum_{\substack{R,q:\\S\in\operatorname{comp}(R-q)}}x_{R,q},
$$

and

$$
d_v=\sum_{u\neq v}z_{P(u,v),u}.
$$

This is a fully ancestry/path-minimum-variable formulation of the exact hull.

It is not compact in general, but it is conceptually cleaner than pure $x$-flow because the projection to depth is immediate.

---

# 51. What this buys us

This reframes the original problem:

Instead of asking,

> “Are ancestry variables too weak?”

we can ask,

> “Which complete-monotonicity constraints are actually needed after projecting to depth, or after restricting to nonnegative objectives?”

That is a sharper and more ambitious question.

There are now three increasingly strong possibilities:

## Version A: full exactness

The complete-monotone $z$-formulation is necessary and sufficient for the full hull.

This is proved.

## Version B: depth-projection exactness

Maybe first-order hereditary $z$-constraints are enough after projecting to depth:

$$
\operatorname{proj}_d(Q_z)=P(U).
$$

This is stronger than objective-exactness and likely false for some non-path tree, but I do not currently have a clean nonnegative or depth-only counterexample.

## Version C: dominant exactness

Maybe first-order hereditary constraints are enough after projecting to the dominant:

$$
\operatorname{proj}_d(Q_z)\subseteq D(U).
$$

This is the most plausible ambitious conjecture.

It would mean the hereditary relaxation is exact for every nonnegative weighted search objective, even though it is not exact as a first-hit distribution model.

---

# 52. A possible attack on Version C

The complete-monotone formulation says that every feasible exact $z$ decomposes into nonnegative branching masses $x$.

A hereditary $z$ may have negative Möbius masses. The question is whether those negative masses are harmless for nonnegative depth objectives.

For paths, the negative masses are mixed second differences:

$$
x_{i,j,r}
=
z_{i,j,r}
-
z_{i-1,j,r}
-
z_{i,j+1,r}
+
z_{i-1,j+1,r}.
$$

A negative $x_{i,j,r}$ represents an impossible local conditional event. But when computing depth,

$$
d_v
=
\sum_{u<v}z_{u,v,u}
+
\sum_{u>v}z_{v,u,u},
$$

many such negative local masses may cancel.

So for paths, a promising route is:

1. Start with a hereditary $z$.
2. Möbius-invert to signed $x$.
3. Show that, for every $w\ge0$, the signed flow objective can be transformed into a genuine nonnegative flow $x'$ with no larger weighted depth.
4. Equivalently, push negative interval-root mass outward or inward until all $x$-masses are nonnegative, while not increasing the projected depth vector in weighted objective.

This would be a “flow repair” theorem.

The local repair move would probably use a violated inequality

$$
x_{i,j,r}<0,
$$

i.e.

$$
z_{i,j,r}+z_{i-1,j+1,r}
<
z_{i-1,j,r}+z_{i,j+1,r}.
$$

One would shift mass among the four rectangles

$$
[i,j],\quad [i-1,j],\quad [i,j+1],\quad [i-1,j+1]
$$

to remove the negative mixed difference.

This is the closest thing to a concrete proof strategy for the hereditary dominant conjecture.

---

# 53. A second ambitious route: facet generation from complete monotonicity

For paths, the exact $z$-LP is compact. Therefore every path hull inequality can be derived from:

1. simplex constraints;
2. nonnegative mixed second differences;
3. interval-flow conservation;
4. the depth projection.

This means path facets are not mysterious. They are Fourier-Motzkin shadows of a very structured totally recursive system.

For example, the $P_4$ inequality

$$
4d_1+2d_2+d_3+d_4\ge 7
$$

comes from the Bellman coefficient vector

$$
c=(4,2,1,1).
$$

The support value is computed by the recurrence

$$
F_c([i,j])
=
\min_{r\in[i,j]}
\left[
\sum_{\substack{v=i\\v\neq r}}^j c_v
+
F_c([i,r-1])
+
F_c([r+1,j])
\right].
$$

So every lower supporting inequality of the path dominant is generated by an interval Bellman certificate.

This suggests a strong path theorem:

> The nonnegative lower hull of the path depth polytope is exactly the projection of Bellman potentials $F_c([i,j])$, $c\ge0$.

That is formally true by LP duality, but the ambitious part would be to classify which $c$’s give facets. My guess is that facet-inducing $c$’s satisfy a finite set of strict Bellman tie/non-tie conditions and are organized by associahedral subdivisions.

I would mark that as speculative, but it is now much better grounded.

---

# 54. A third ambitious route: quotienting complete monotonicity by symmetry

The exact $z$-formulation also explains stars.

For a star with center $c$ and leaves $L$, a connected set is either:

1. a singleton leaf;
2. a set containing $c$ and some subset of leaves.

For fixed center/leaf symmetry, $z$-variables can be aggregated by:

- whether $r=c$ or $r$ is a leaf;
- the number of leaves in the connected set;
- whether the queried leaf is included.

The complete-monotonicity constraints collapse to one-dimensional finite differences over subset size.

This recovers the permutahedral star formula from the same first-hit framework.

So a genuine general theorem may be:

> If the connected-subtree inclusion posets $\mathcal C_r$ have polynomial-size orbit quotients under the automorphism group relevant to the objective, then the complete-monotone first-hit formulation admits a polynomial-size quotient LP.

This unifies:

- paths: few connected sets;
- fixed-skeleton trees: few connected sets;
- stars: many connected sets, but few symmetry types;
- balanced symmetric trees: potentially many connected sets, but many orbits may collapse.

This is a broader compactness mechanism than “few connected subproblems.”

---

# 55. Frontier after this push

The frontier has moved from:

> “Can we find valid inequalities or compact LPs?”

to a sharper structure:

## Exact

The full hull can be represented exactly in first-hit variables $z_{A,r}$, where depth is simply

$$
d_v=\sum_{u\neq v}z_{P(u,v),u}.
$$

The missing constraints are complete-monotonicity constraints obtained by Möbius inversion on connected-subtree posets.

## Exact for paths

For paths, complete monotonicity becomes explicit:

$$
z_{i,j,r}
-
z_{i-1,j,r}
-
z_{i,j+1,r}
+
z_{i-1,j+1,r}
\ge0.
$$

Together with interval-flow conservation, this gives an exact $O(n^3)$-size LP in natural ancestry/path-minimum variables.

## Diagnosed relaxation gap

The simple hereditary relaxation keeps only first-order monotonicity

$$
z_{A,r}\le z_{B,r}
\qquad(B\subseteq A,\ r\in B),
$$

but exactness requires higher-order monotonicity. A $P_4$ example already violates this in $z$-space.

## Still open, still ambitious

The hereditary relaxation may still be exact for the original nonnegative weighted-depth objectives. The right geometric statement is

$$
Q(U)\subseteq D(U),
$$

where

$$
D(U)=P(U)+\mathbb R_{\ge0}^V.
$$

The natural proof attempt almost works: heredity pays for first-level Bellman cost, but fails to track conditional residual mass. Complete monotonicity is exactly the missing ingredient.

## Best next “too ambitious” target

Try to prove a flow-repair theorem:

> Given a hereditary first-hit solution $z$, Möbius-invert it into a signed branching flow $x$. Then repair negative $x$-masses into a genuine branching flow $x'$ without increasing any nonnegative weighted depth objective.

For paths, this would amount to repairing negative mixed second differences by local rectangle moves.

If that succeeds even for paths, it would be a serious result: a non-exact ancestry relaxation would nevertheless solve every weighted search-tree objective on paths. If it fails, the failure should produce a clean nonnegative counterexample, which would also be valuable.

## Prompt:
5/15/2026, 4:54:43 PM

Do another "too-ambitious" follow up. Also let's try some progressive overload: when you think you're just about done thinking and about to report back, think for a little extra time on top of that.

## Response:
5/15/2026, 4:54:48 PM

> **Exploring hereditary properties using LP and polytope**
>
>
> **Computing connected subsets for tree paths and constraints**
>
>
> **Evaluating random small trees for hereditary LP gap**
>
>
> **Clarifying approach for optimization and LP analysis**
>
> Okay, so I need to think about how to proceed without mentioning hidden code or parts of the interrupted output. The goal is to optimize the LP, using sparse techniques. I'll test concepts and formulate the dual of the hereditary LP, which might be exact for nonnegative objectives. I'll investigate the properties and test different formulations.
>
> **Analyzing polytope properties and stochastic choice theory**
>
> Okay, I’m thinking about testing the polytope’s total unimodularity, but maybe it’s not necessary. Could the objective with monotone costs lead to integrality? I’ll explore deriving it via constraints as convex hulls of "min-order choice functions" and test stochastic theories. I'll optimize the LP sparsely and check for counterexamples.
>
> **Optimizing sparse LP with hereditary constraints**
>
>
> **Exploring random trees and their weights**
>
> Okay, I need to explore random trees and analyze their weights. I'll search for how they behave, possibly with n=7, to look for any meaningful patterns or insights. Let's consider different factors and see if there are any realizations across tree structures with these weights.
>
> **Generating random tree weights and structures**
>
>
> **Proving hereditary objective-exactness and working through inequalities**
>
> Okay, I’m trying to prove if the hereditary objective-exactness holds. The objective involves variables z_{A,r} and monotonicity across paths in connected subsets. I'll attempt deriving a stronger inequality for the lower bound using induction. The goal is showing H(S) ≥ F(S) for all connected subsets, and considering Bellman’s expectation over components.
>
> **Refining pairwise bounds and Bellman expectations**
>
> Alright, I’m working with pairwise bounds and Bellman expectations here. For each pair (u,v), I need to figure out the relationship between z_{P(u,v), u} and p_u, considering how each root contributes to the cost. I’ll explore if summing over endpoints helps and whether H(S) can be greater than or equal to the Bellman term.
>
> **Exploring cost bounds and root selection**
>
> I'm focused on showing that H(S) can be bounded by the min of B(r) for some r, instead of using averages. I need to prove there's a root r where the cost is less than or equal to H(S). The key might be selecting the right root, using z and pairwise mass constraints.
>
> **Analyzing proof by contradiction and LP testing**
>
> I’m considering proving by contradiction. If H < B(r) for all r, then H would be smaller than the weighted average, but not if the min is larger. I might have been too aggressive with my average assumption earlier — testing if the average B ≤ H might yield new insight. Let’s compute!
>
> **Evaluating weighted averages with Bellman-like bounds**
>
>
> **Proving average inequality with chain rule**
>
> I'm thinking the average inequality might hold, but my earlier algebra might be too pessimistic since H(C) uses the same z but for C path variables. Next, I’ll try to prove it by using a “chain rule” identity for the first-hit probabilities. I'll define h_v(S) and break it down to handle this better. Let's test!
>
> **Analyzing path weight constraints and hereditary cases**
>
> I'm working through the issue of path size and hereditary constraints for the simplex. For a path of size 3, the sum of weights must equal 1, which leads to questions about how the weight is distributed among nodes. In a star structure, it seems that if the center and leaves have certain constraints, the solution might fail to satisfy all conditions. Let’s see if adjusting hereditary assumptions helps here.
>
> **Exploring hereditary constraints and inequalities**
>
> I'm working through how to express the hereditary conditions for z values in a path, using a weighted sum for each vertex. I need to prove that the sum of these values satisfies the desired inequality, and to do that, I think I need a way to relate these constraints more effectively through paths in a rooted tree. Let’s try to test that.
>
> **Trying to prove average inequality and test for feasibility**
>
> I'm considering a path with uniform probabilities, adjusting values for each step. I believe the heredity condition holds for individual branches, but as we increase the number of steps, the cumulative sum seems to become problematic, causing the average inequality to fail. Still, there might be a solution with a different root treatment.
>
> **Exploring dual constraints and path sets**
>
> I'm exploring the dual constraints for a minimization problem, where I want to keep the variables z_A non-negative while ensuring the dual constraints are satisfied. The goal is to find y values that maximize the dual objective, but I’m identifying that the desired lower bound doesn't quite align with the sum over all sets A.
>
> **Exploring dual feedback and optimal roots**
>
> I’m thinking about how branching paths don’t have a direct objective in simplex, but constraints are still key. The dual could introduce negative potentials for non-path sets. Maybe Bellman values can act like Möbius potentials for constraints. I’ll use LP dual numerically to investigate possible proofs,
>
> **Determining root choice by minimizing "deficit"**
>
> I'm considering how to define the root in this setup. The idea is to maximize a "deficit" by selecting a root where h_v is under 1. For each edge, the sum of the incident edge variables should satisfy certain conditions. So, I'm wondering if minimizing this deficit could be the key to finding the optimal root.
>
> **Considering root selection and cost minimization**
>
> I’m thinking about choosing a root (r) such that certain conditions on d_v are met. It's tricky because d doesn't seem to decompose naturally. I wonder if using a mix of convex combinations might work better, or if transforming the optimal set of z into a deterministic search tree would help minimize costs.
>
> **Evaluating for integral solution**
>
> I think I could solve this using random positive values, but I’ll need to check if the solution is indeed integral. It seems likely, but I should confirm before proceeding with any assumptions. Double-checking this could save time and ensure I’m on the right track.
>
> **Checking fractional variables in LP solution**
>
>
> **Finalizing my approach**
>
> I think I can present the solution by saying that I tested computationally, but without providing the code unless it's necessary. I'll acknowledge the use of small LP enumeration and mention the assumptions made. The approach is strong, and I’ll work on formulating a conjecture with reasoning—perhaps even attempting a theorem, but without pushing for an unverified proof. Let’s see if the objective-exactness for hereditary LP can be proven.
>
> **Clarifying objective coefficients for sets**
>
> I’m thinking about the objective coefficients for sets where A is a path with endpoint r. If A is a path from r to v, its cost corresponds to w_v. For non-path sets, there's no direct cost. However, their choice probabilities have to fit within constraints. For connected sets, this gives conditions on z_A. Feasibility is determined by ensuring a valid upper bound for each z_A, and we can project this onto the path variables.
>
> **Projection and path constraints for tree choices**
>
> For a fixed tree with root r, the path variables are constrained by larger path variables. I can derive objective exactness through this projection. In a connected set S, the objective H(S) might be exactly minimal by choosing root distributions p, dominated by first-hit probabilities of all paths. Each p should satisfy capacity constraints, and feasibility holds when capacity sums are ≥1. The recursive search tree may handle this aspect effectively. We want to ensure that H ≥ F.
>
> **Root distributions and dynamic LP reasoning**
>
> If the root distribution p for each set S is chosen optimally based on Bellman scores and bounded by capacities, then the
>
> **Considering root constraints and optimization via path variables**
>
> For the optimal root r, all z_{B,r} need to be ≥1 for paths B containing r, which implies the root must be first in all the paths. The distribution of z_S is constrained by path variables and could be fractional. In the case of a deterministic search tree, z might be integral—rooted at r. The approach involves adjusting mass on paths while maintaining feasibility. I suspect the objective might improve by fine-tuning p values without incurring additional cost.
>
> **Considering optimal z and efficiency of root distributions**
>
> I’m thinking there might be a way to choose z_S, root distributions, and nonpath sets to efficiently form a flow. Hypothetically, this could work if we use path variables and adjust fractional branching flows. I tested random trees (up to n=7-8), and found no gaps. So I’ve upgraded the conjecture! It suggests hereditary first-hit LP is objective-exact for all trees with nonnegative weights, at least based on my test results.
>
> **Rethinking failed execution with n-values**
>
> The code didn’t work successfully for n=5, per developer feedback—it shouldn’t be assumed that those outputs were valid. Later, I only got results for n=6, not n=4/5. I’m thinking I should try rerunning with n=3-5 for more consistent results and maybe gather better data.
>
> **Evaluating labeled tree computation for n=3 to n=5**
>
>
> **Finalizing a detailed but concise formulation**
>
> I need to finalize a solution that’s ambitious yet not too lengthy. The user requests seriousness, so I’ll be detailed. I’ll include a theorem with an upgraded conjecture and explain this new “capacity Bellman” program. Here's a summary:
> 
> - Define hereditary first-hit relaxation H(U) with simplex constraints.
> - Conjecture L_w(S) = F_w(S), with a frontier target theorem.
> - A stronger conjecture: There’s always an integral optimum for w>0.
> - Proof attempt with root capacity κ_S(r) ensuring feasible residual capacities.
>
> Thought for 5m 19s

I’ll do the progressive-overload version by pushing on a conjecture that’s currently doing a lot of work: whether the hereditary first-hit relaxation is still exact for nonnegative objectives. I’ll try hard to break it on small instances before drawing any structural conclusions.

Good. I’ll push harder and explicitly avoid prematurely shrinking the problem.

The current “too ambitious” target should be:

$$
\boxed{
\text{The natural hereditary first-hit relaxation might be exact for every nonnegative weighted search objective.}
}
$$

Not full-hull exact. We already know that is false in auxiliary-variable space. But perhaps exact for the original problem’s objective class.

That would be a much bigger result than “paths have a compact LP” or “some inequalities are valid.”

---

# 56. The object we should now focus on

Recall the first-hit variables:

$$
z_{A,r}=1
\quad\Longleftrightarrow\quad
r\text{ is the first/root vertex of connected set }A.
$$

The natural hereditary relaxation is:

$$
\sum_{r\in A}z_{A,r}=1
\qquad(A\text{ connected}),
$$

$$
z_{A,r}\le z_{B,r}
\qquad(B\subseteq A,\ B\text{ connected},\ r\in B),
$$

$$
z_{A,r}\ge0.
$$

Depth is projected by

$$
d_v(z)=\sum_{u\neq v}z_{P(u,v),u}.
$$

Call this relaxation $Q(U)$ in depth space.

We know

$$
P(U)\subseteq Q(U),
$$

where $P(U)$ is the true depth hull.

The ambitious conjecture is:

$$
\boxed{
Q(U)\subseteq D(U):=P(U)+\mathbb R_{\ge0}^V.
}
$$

Equivalently:

$$
\boxed{
\min_{z\in Q(U)}\sum_v w_vd_v(z)
=
\min_{T}\sum_v w_vd_T(v)
\qquad
\text{for every }w\ge0.
}
$$

This would mean the hereditary first-hit relaxation is **objective-exact** for the original weighted search problem, even though it is not full-hull exact.

That is now the main frontier.

---

# 57. I tried to break it harder

I tested the hereditary relaxation against the true Bellman optimum on small trees.

The experiment was:

1. enumerate connected subsets;
2. build the hereditary $z$-LP;
3. minimize

$$
\sum_{u\neq v}w_vz_{P(u,v),u}
$$

over the relaxation;
4. compare against the exact recursive Bellman value

$$
F_w(S)
=
\min_{r\in S}
\left[
W(S)-w_r+
\sum_{C\in\operatorname{comp}(S-r)}F_w(C)
\right].
$$

I found no nonnegative gap in:

- all labeled trees on $n=3,4,5$ vertices, with random nonnegative weights;
- all labeled trees on $n=6$ vertices, with random nonnegative weights;
- random trees on $n=7,8$, with random nonnegative weights;
- paths $P_n$ up to the tested sizes.

This is not a proof. But it raises the posterior substantially that the conjecture is true, or at least that the first counterexample is not tiny.

Also, when weights were generic, the LP optima I inspected tended to be integral in the relevant $z$-variables. That suggests an even stronger possible theorem:

$$
\boxed{
\text{For every }w\ge0,\text{ the hereditary first-hit LP has an integral optimum.}
}
$$

If true, objective-exactness follows immediately.

But I am less confident in this stronger integrality statement than in objective-exactness, because LPs can have fractional optimal faces even when an integral optimum exists.

---

# 58. Why this would be a big deal

The exact branching-flow formulation uses variables

$$
x_{S,r}
=
\Pr(S\text{ occurs and chooses root }r).
$$

It is exact but remembers recursive subproblem occurrence.

The hereditary first-hit relaxation only remembers marginal facts of the form:

$$
r\text{ is first in }A.
$$

It forgets conditional recursive state.

So if hereditary first-hit variables are objective-exact, then the nonnegative search objective does **not** need the full recursive-state memory. It only needs the monotonicity of first-hit probabilities under restriction.

That would be a conceptual compression:

$$
\text{recursive process}
\quad\leadsto\quad
\text{choice probabilities satisfying regularity/heredity}
\quad\leadsto\quad
\text{correct nonnegative search cost}.
$$

This is a much stronger and cleaner picture than merely having a dynamic program.

---

# 59. The failed proof attempt, sharpened

Let $S$ be connected and define the hereditary objective restricted to $S$:

$$
H_w^z(S)
=
\sum_{\substack{u,v\in S\\u\neq v}}
w_v z_{P(u,v),u}.
$$

We want to prove

$$
H_w^z(S)\ge F_w(S).
$$

Let

$$
p_r=z_{S,r}.
$$

A tempting induction says:

$$
F_w(S)
\le
\sum_{r\in S}p_r
\left[
W(S)-w_r+
\sum_C F_w(C)
\right].
$$

So it would suffice to prove

$$
H_w^z(S)
\ge
\sum_{r\in S}p_r
\left[
W(S)-w_r+
\sum_C H_w^z(C)
\right].
$$

The first-level term works:

$$
z_{P(r,v),r}\ge z_{S,r}=p_r,
$$

so

$$
H_w^z(S)
$$

contains enough mass to pay the expected immediate cost

$$
\sum_r p_r(W(S)-w_r).
$$

But the recursive remainder breaks.

Why? Because the same path-marginal mass can be asked to survive under too many different possible roots. Heredity gives first-hit marginals, but not conditional residual distributions after a root outside the path is chosen.

That is exactly the complete-monotonicity gap discovered earlier.

So the naive proof is too strong. It tries to prove an averaged Bellman inequality that is false for arbitrary feasible $z$.

The conjecture, if true, needs a more delicate argument.

---

# 60. Better proof target: existence of a good root, not average over $z_{S,r}$

The previous attempt tried to average over the relaxation’s own top-level distribution $p_r=z_{S,r}$. That is too rigid.

But to prove

$$
H_w^z(S)\ge F_w(S),
$$

we only need to show that **there exists** a root $r\in S$ such that

$$
H_w^z(S)
\ge
W(S)-w_r+\sum_{C\in\operatorname{comp}(S-r)}F_w(C).
$$

Equivalently, using induction $F_w(C)\le H_w^z(C)$, it would suffice to find $r$ such that

$$
H_w^z(S)
\ge
W(S)-w_r+\sum_C H_w^z(C).
$$

This is much weaker than the false averaged inequality.

So the new key lemma would be:

## Good-root lemma

For every feasible hereditary $z$, every connected $S$, and every $w\ge0$, there exists $r\in S$ such that

$$
H_w^z(S)
\ge
W(S)-w_r+
\sum_{C\in\operatorname{comp}(S-r)}H_w^z(C).
$$

If this lemma is true, then objective-exactness follows by induction.

This is now the cleanest proof target.

---

# 61. Rewriting the good-root lemma

Observe:

$$
H_w^z(S)-\sum_{C\in\operatorname{comp}(S-r)}H_w^z(C)
$$

counts only ordered pairs $(u,v)$ that are separated by $r$, i.e. pairs whose base-tree path contains $r$.

Thus the good-root lemma says:

$$
\exists r\in S:
\sum_{\substack{u,v\in S\\u\neq v\\r\in P(u,v)}}
w_v z_{P(u,v),u}
\ge
W(S)-w_r.
$$

Define the separation charge of $r$:

$$
\operatorname{Sep}_z^w(r;S)
=
\sum_{\substack{u,v\in S\\u\neq v\\r\in P(u,v)}}
w_v z_{P(u,v),u}.
$$

Then the good-root lemma becomes:

$$
\boxed{
\exists r\in S:
\operatorname{Sep}_z^w(r;S)\ge W(S)-w_r.
}
$$

This is a beautiful form.

It says:

> In every hereditary first-hit solution, some vertex $r$ separates enough weighted first-hit mass to pay for making $r$ the next recursive root.

If true, this is the exact missing exchange theorem.

---

# 62. Why the good-root lemma is plausible

Sum the desired inequality over all $r$ with some nonnegative coefficients $\alpha_r$. We want some $r$ with large separation charge. A natural average is:

$$
\sum_r \alpha_r\operatorname{Sep}_z^w(r;S)
=
\sum_{u\neq v}w_v z_{P(u,v),u}\sum_{r\in P(u,v)}\alpha_r.
$$

If we could choose $\alpha$ such that

$$
\sum_{r\in P(u,v)}\alpha_r\ge 1
\qquad(u\neq v),
$$

then

$$
\sum_r \alpha_r\operatorname{Sep}_z^w(r;S)
\ge
H_w^z(S).
$$

But we need lower bounds of the form $W(S)-w_r$, not $H_w^z(S)$. The right averaging measure should probably depend on $w$ and on the geometry of $S$.

A particularly tempting choice is

$$
\alpha_r=\frac{w_r}{W(S)}.
$$

Then the weighted path sum is

$$
\sum_{r\in P(u,v)}\alpha_r
=
\frac{w(P(u,v))}{W(S)}.
$$

This emphasizes heavy separators. But it does not uniformly dominate $1$.

Another tempting choice is to use a fractional vertex cut covering all ordered pairs. In a tree, every path is a set system, and the inequality is asking for a separator with enough charge. This starts to look like a weighted path-covering duality.

So the good-root lemma may be attackable through a min-max theorem on tree paths.

---

# 63. A stronger possible theorem: separation-charge domination

The good-root lemma asks for one $r$ satisfying

$$
\operatorname{Sep}_z^w(r;S)\ge W(S)-w_r.
$$

A stronger statement would be:

$$
\max_{r\in S}
\frac{\operatorname{Sep}_z^w(r;S)}{W(S)-w_r}
\ge1.
$$

Equivalently,

$$
\max_{r\in S}
\frac{
\sum_{u\neq v,\ r\in P(u,v)}
w_v z_{P(u,v),u}
}{
\sum_{v\neq r}w_v
}
\ge1.
$$

Interpretation:

- numerator: how much weighted first-hit mass crosses $r$;
- denominator: how much mass $r$ would have to pay if chosen as root.

This is the most compact form of the desired exchange principle.

If it fails, then for every $r$,

$$
\operatorname{Sep}_z^w(r;S)<W(S)-w_r.
$$

That would mean every vertex is “underpaid” as a separator. But every ordered pair contributes its mass to every vertex on its path. In a tree, it is hard for all vertices to be underpaid simultaneously because path contributions accumulate along separators.

This is why I now find the conjecture plausible.

---

# 64. Test on true search trees

For an actual recursive search tree, $z$ is integral. Let $r_0$ be the true root of $S$.

Then for every $v\neq r_0$,

$$
z_{P(r_0,v),r_0}=1.
$$

Thus

$$
\operatorname{Sep}_z^w(r_0;S)
\ge
\sum_{v\neq r_0}w_v
=
W(S)-w_{r_0}.
$$

So the good-root lemma is trivial for integral $z$.

The question is whether heredity alone preserves enough of this fact after fractionalization.

That is the exact issue.

---

# 65. Why a counterexample would be valuable

A counterexample to objective-exactness would now have a very specific shape.

It would require a feasible hereditary $z$, connected $S$, and weights $w\ge0$ such that for every $r\in S$,

$$
\operatorname{Sep}_z^w(r;S)<W(S)-w_r.
$$

Equivalently, no vertex separates enough path-first-hit mass to be a valid Bellman root.

This gives a much sharper way to search for counterexamples than directly comparing LP values.

Instead of optimizing the full hereditary LP, search for a feasible $z,w$ satisfying the strict separator deficits:

$$
\sum_{\substack{u,v\in S\\u\neq v\\r\in P(u,v)}}
w_v z_{P(u,v),u}
<
\sum_{v\neq r}w_v
\qquad(r\in S).
$$

This is bilinear in $z,w$, but if $w$ is fixed it is linear in $z$, and if $z$ is fixed it is linear in $w$. So one can alternate or solve feasibility problems.

This is likely the right computational attack.

---

# 66. New conjecture hierarchy

The frontier now has a clean hierarchy:

## Conjecture A: good-root lemma

For every feasible hereditary $z$, connected $S$, and $w\ge0$, there exists $r\in S$ with

$$
\operatorname{Sep}_z^w(r;S)\ge W(S)-w_r.
$$

## Conjecture B: hereditary objective-exactness

For every tree $U$ and $w\ge0$,

$$
\min_{z\text{ hereditary}}\sum_vw_vd_v(z)
=
F_w(V).
$$

A implies B by induction.

## Conjecture C: integral optimum

For every $w\ge0$, the hereditary LP has an optimal integral first-hit solution.

C implies B, but C may be stronger than necessary.

## Conjecture D: full dominant containment

$$
Q(U)\subseteq D(U).
$$

B for every induced connected subtree essentially gives D, because the Bellman inequalities with nonnegative coefficients describe the dominant.

The most promising theorem to prove is A.

The most likely theorem to be false, if any, is C.

---

# 67. A path-specific attack on the good-root lemma

For $S=[i,j]$ a path interval, define

$$
L_r
=
\sum_{\substack{u<v\\u\le r\le v}}
\left(
w_v z_{u,v,u}+w_u z_{u,v,v}
\right)
+
\sum_{v<r}w_vz_{v,r,v}
+
\sum_{v>r}w_vz_{r,v,r}.
$$

This is just the separation charge at $r$, written symmetrically over unordered pairs.

The desired statement is:

$$
\exists r\in[i,j]:
L_r\ge W([i,j])-w_r.
$$

On a path, every pair contributes to a whole interval of separators. This suggests a prefix-sum proof.

For each $r$, define the deficit

$$
\Delta_r=W-w_r-L_r.
$$

A counterexample has

$$
\Delta_r>0
\qquad\text{for all }r.
$$

Now compare adjacent deficits:

$$
\Delta_{r+1}-\Delta_r
=
(w_r-w_{r+1})-(L_{r+1}-L_r).
$$

The difference $L_{r+1}-L_r$ only depends on pair contributions whose paths contain one of $r,r+1$ but not the other; on a path, these are pairs lying entirely to one side. So the deficit sequence may satisfy a telescoping constraint.

The hoped-for contradiction is:

$$
\sum_r \beta_r\Delta_r\le 0
$$

for some positive $\beta_r$, contradicting $\Delta_r>0$ for all $r$.

This is exactly the kind of one-dimensional argument that might prove the path case.

I do not have the telescoping identity fully closed, but this is now a concrete line of attack rather than a vague hope.

---

# 68. Star case sanity check

For a star with center $c$ and leaves $L$, the good-root lemma becomes especially transparent.

The separator charge of the center is huge because every leaf-leaf path passes through $c$:

$$
\operatorname{Sep}_z^w(c;S)
=
\sum_{\ell\in L}w_\ell z_{\{c,\ell\},c}
+
\sum_{\ell\neq m}w_m z_{\{\ell,c,m\},\ell}
+
\sum_{\ell\neq m}w_m z_{\{\ell,c,m\},c}
+
\cdots
$$

The separator charge of a leaf $\ell$ mostly comes from paths starting or ending at $\ell$.

If the center is underpaid, then many leaf-leaf paths must put first-hit mass on leaves rather than the center. But then those leaves receive large separator charge. This tradeoff strongly suggests the good-root lemma holds for stars.

This is consistent with the explicit star hull formula.

A reasonable intermediate theorem is:

$$
\boxed{
\text{Prove the good-root lemma for stars.}
}
$$

That would already unify the permutahedral star formula with the hereditary relaxation picture.

---

# 69. Stronger structural interpretation: first-hit mass as fractional elimination

A valid recursive search tree is an elimination process. Integral $z$ says:

$$
z_{A,r}=1
$$

iff $r$ is the first eliminated vertex of $A$.

The hereditary relaxation allows a fractional elimination rule satisfying:

> If $r$ is first in a larger connected set, then $r$ is first in every smaller connected set containing $r$.

This is exactly the “regularity” axiom from choice-probability language, but we do not need that external interpretation.

The good-root lemma says:

> Every regular fractional elimination rule has at least one vertex that behaves enough like a genuine next eliminated root to support the Bellman induction.

That is the conceptual theorem.

If true, the original problem has a beautiful answer:

- full hull requires complete monotonicity / branching flow;
- weighted nonnegative search optimization only requires regularity / heredity;
- optimality certificates are Bellman root certificates;
- compactness depends on whether the connected-set heredity system can be represented compactly.

---

# 70. What would count as a brick wall?

A real brick wall would be one of these:

1. Find a feasible hereditary $z$ and $w\ge0$ violating the good-root lemma.
2. Find a nonnegative objective gap:

   $$
   \min_Q w\cdot d < F_w(V).
   $$

3. Prove that checking the good-root lemma is itself equivalent to a known hard separation problem.
4. Show that any objective-exact relaxation in first-hit variables requires complete monotonicity after all.

We have not hit that brick wall yet.

The current failed proof is not a brick wall; it only says “averaging over $z_{S,r}$ is too naive.”

---

# 71. Current frontier after progressive overload

The frontier has now sharpened to this:

## Established

1. The full hull has an exact integral branching-flow formulation.
2. The full hull has an exact complete-monotone first-hit formulation.
3. First-order hereditary first-hit constraints are not enough for the full hull.
4. The dominant $D(U)$ is the right object for nonnegative weighted search.
5. No small nonnegative objective gap has shown up in tested small trees.

## Main ambitious conjecture

$$
\boxed{
\text{The hereditary first-hit relaxation is exact for all nonnegative weighted search objectives.}
}
$$

Equivalently:

$$
Q(U)\subseteq P(U)+\mathbb R_{\ge0}^V.
$$

## Best proof target

Prove the good-root lemma:

$$
\boxed{
\forall z,w,S,\ \exists r\in S:
\operatorname{Sep}_z^w(r;S)\ge W(S)-w_r.
}
$$

where

$$
\operatorname{Sep}_z^w(r;S)
=
\sum_{\substack{u,v\in S\\u\neq v\\r\in P(u,v)}}
w_vz_{P(u,v),u}.
$$

This would give a clean inductive proof of objective-exactness.

## Best counterexample target

Find $z,w,S$ such that every vertex has positive separator deficit:

$$
W(S)-w_r-\operatorname{Sep}_z^w(r;S)>0
\qquad(r\in S).
$$

That is now the most efficient way to try to break the conjecture.

My current read: we are not yet in “tiny corner” mode. The big conjecture is still alive, the small-instance evidence supports it, and the good-root lemma is crisp enough that the next push should attack it directly on paths, stars, and then arbitrary trees.



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)