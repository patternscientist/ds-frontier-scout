# AI Collaboration Fit

Theorem-project suitability: 4/5 for a narrowed subproblem; 2/5 for the full traversal conjecture.

Good staged workflow:

1. Blind prompt: define Splay, preorder / 231-avoidance, and one restricted initial-tree regime. Ask for a potential or structural invariant without literature context.
2. Frontier document: introduce known Splay special cases, Greedy forbidden-submatrix bounds, offline OPT on fixed-pattern-avoiding sequences, and the arbitrary-initial-tree obstruction.
3. Literature mode: bring in the geometric BST model, Greedy execution logs, subsequence property, and product-pattern extremal bounds.

AI is likely useful for:

- generating candidate potentials for 231-avoiding insertion/access sequences;
- translating between tree recursion and permutation-pattern recursion;
- searching for minimal statements that survive exact simulation;
- comparing Splay and Greedy traces on Catalan-size families;
- proposing falsifiable lemmas about access paths, exposed ancestors, or "hidden" nodes.

Main danger: the model may hallucinate folklore around dynamic optimality. Every lemma should be tested against small exact simulations before being promoted.
