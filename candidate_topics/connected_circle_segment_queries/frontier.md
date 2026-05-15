# Frontier

Verified source:

- Afshani, Bosch, and Storandt, "Circle-Segment Intersection Queries in Connected Geometric Graphs," ISAAC 2025.
- The paper exploits connectivity of the segment graph via an edge partition tree whose nodes induce connected subgraphs.
- Each node gets a circle-graph intersection oracle using transformed endpoints, convex hulls, and segment Voronoi diagrams.
- The future-work section suggests bottom-up construction, fractional-cascading-style improvements over nested convex hulls, and lower bounds for data-size/query-time tradeoffs.

Inferred frontier:

- The cleanest theorem target is not implementation speed but a lower-bound or tradeoff model for connected segment graphs.
- The cleanest evaluator target is finite connected graph families where many partition-tree oracle calls are forced while output is small.

TODO: verify source:

- Recover exact asymptotic formulas from the PDF or source because the HTML rendering drops symbols.
