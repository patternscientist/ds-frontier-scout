# OpenEvolve Fit

OpenEvolve suitability: 4/5 for counterexample mining and lemma search; 2/5 for full theorem discovery.

Plausible automated evaluators:

- exact Splay simulator for all 231-avoiding permutations up to `n`;
- exact Greedy/geometric-BST simulator for the same access classes;
- Catalan generator for all preorder permutations;
- fixed-pattern-avoidance generator for arbitrary small forbidden patterns;
- offline optimum oracle for small `n` via dynamic programming, geometric BST integer programming, or exhaustive rotation schedules;
- feature extractor for access paths: depth changes, ancestor exposure, dynamic-finger jump sizes, and potential deltas.

Search targets:

- candidate potential functions with nonpositive amortized drift on all 231-avoiding traces up to a bound;
- small counterexamples to naive Splay-on-pattern-avoidance lemmas;
- minimal restricted classes where Splay appears linear from arbitrary initial trees;
- empirical separation between empty-initial, aligned-initial, balanced-target, and arbitrary-initial regimes.

Evaluator caveat: exact OPT for dynamic BSTs grows fast. Keep the first phase to Splay-cost certification and candidate lemma falsification, not full dynamic-optimality benchmarking.
