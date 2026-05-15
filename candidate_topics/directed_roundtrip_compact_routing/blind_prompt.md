# Blind Prompt

Given a weighted strongly connected directed graph, build a compact labeled routing scheme for roundtrip distance.

Each vertex stores `~O(n^{1/k})` local information. Routing from a source to a destination must be local: each hop can inspect only the current vertex's routing table, the destination label, and a small packet header.

For general `k`, improve the known `4k+epsilon`-style roundtrip stretch, or prove a lower bound showing that stretch close to `2k-1` is impossible in directed graphs.
