# Frontier

Verified source:

- Kadria and Roditty, "Compact Routing Schemes in Undirected and Directed Graphs," DISC 2025 / arXiv:2503.13753.
- For undirected communication sessions, they obtain optimal `(2k-1)` roundtrip/handshake stretch with `~O(n^{1/k})` local storage.
- For directed graphs, previous general compact roundtrip routing achieved about `(4k+epsilon)` stretch.
- The paper improves the directed `k=3` case to 7 stretch using `~O(n^{1/3})` local storage.
- Problem 3 asks for the best stretch for directed weighted graphs with `~O(n^{1/k})` local storage.

Inferred frontier:

- The attractive residual is general directed `k`, especially whether the undirected-like `2k-1` target is possible or whether directed asymmetry enforces a larger constant.

TODO: verify source:

- Read arXiv v3 for any open-problem refinements beyond the proceedings text.
