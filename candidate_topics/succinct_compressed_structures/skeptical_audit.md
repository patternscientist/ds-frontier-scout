# Skeptical Audit

Why this might not actually be open:

- Dagstuhl states explicit questions, but the HTML omits key asymptotic notation.
- Compressed indexing is large; similar LZ random-access or pattern-matching tradeoffs may have been solved under a slightly different compression model.

Why this might be too saturated:

- String compression/indexing has a substantial active literature.
- Without a narrow formal model, the candidate risks becoming a literature-review sink.

Why automatic evaluation might fail:

- Tiny LZ/grammar instances do not reveal space lower bounds.
- An evaluator may reward parse-specific tricks that do not work for worst-case compressed representations.

What would falsify interest:

- The desired `O(n)`-space, `O(log N)` LZ indexing target is already known for the exact parse model.
- The grammar expansion-length overhead problem reduces to a known DAG labeling/sampling theorem.

Primary sources to check before promotion:

- Gawrychowski Dagstuhl 25191 PDF/slides for exact LZ notation.
- Navarro Dagstuhl 25191 PDF/slides for exact DAG problem.
- Recent compressed-index surveys and papers citing those questions.
