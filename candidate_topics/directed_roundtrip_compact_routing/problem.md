# Problem

For weighted strongly connected directed graphs, determine the best roundtrip stretch achievable by compact routing schemes with about `~O(n^{1/k})` local storage per vertex.

Roundtrip distance is `d(u,v)+d(v,u)`. A routing scheme stores local tables and labels, then routes using only local table information, destination labels, and packet headers.

Open status: explicit as Problem 3 in Kadria and Roditty (DISC 2025).
