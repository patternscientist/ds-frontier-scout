# Blind Prompt

You are studying the following self-contained problem.

A splay tree is a binary search tree. To access a key `x`, search from the root to `x`, then repeatedly rotate `x` upward until it becomes the root, using the standard zig, zig-zig, and zig-zag splay steps. The cost of an access is the number of nodes on the search path, or equivalently within constant factors the number of rotations plus one.

For a binary search tree `T` on keys `{1,...,n}`, let `preorder(T)` be the sequence obtained by visiting the root, then recursively the left subtree, then recursively the right subtree. Equivalently, these are the permutations avoiding the pattern `(2,3,1)`: there are no indices `i < j < k` whose values have the same relative order as middle, largest, smallest.

Problem: study how much of the preorder traversal phenomenon survives when the initial tree is arbitrary.

Version A, warm-up / benchmark, not the main open target: Starting from the empty tree, insert the keys of a 231-avoiding permutation by ordinary BST search followed by splaying the inserted key. Prove total cost `O(n)`. This case is known or expected from the cited frontier and should be used to test definitions, potentials, and simulations before attacking the real target.

Version B, main research target: Starting from an arbitrary initial BST on `{1,...,n}`, access a 231-avoiding permutation by splaying after every access. Seek total cost `O(n)`. If that is out of reach, seek any `o(n log n)` upper bound, or prove linearity for a meaningful subclass of arbitrary-initial-tree preorder access.

Try to find:

- a potential function whose amortized access cost telescopes over the recursive preorder structure;
- a decomposition of 231-avoiding permutations into left and right recursive blocks that controls future access paths;
- a falsifiable invariant about nodes that can lie on many access paths;
- or a small explicit obstruction showing why the arbitrary-initial-tree version is harder than the empty or aligned version.

Do not use literature or web search. State every assumption precisely.
