# Problem

Search trees on trees (STTs) generalize binary search trees from a path-ordered key space to an arbitrary tree topology. Given an underlying tree `U` and query frequencies on its vertices, a static STT recursively chooses a root vertex, then recurses on each connected component of `U` after that root is removed. The expected search cost is the frequency-weighted depth in the STT.

Core candidate problem:

Determine whether an optimal static STT for a weighted tree topology can be computed in polynomial time, and, if not yet, sharpen LP-based approximations and integrality-gap certificates around Golinsky's relaxation.

Patch-specific subproblems:

- understand Golinsky's LP relaxation and root-rounding method;
- reproduce and extend the 2025 Sadeh-Kaplan-Zwick counterexamples;
- characterize topologies where the LP or its projection to depth space is integral;
- prove or refute optimality on stars, paths, almost-stars / edge-diameter-3 trees, and other tiny topology classes;
- search for improved rounding schemes or stronger polynomial-size relaxations.

Open status: open for the polynomial-time optimal static STT question, as explicitly stated by Sadeh, Kaplan, and Zwick (2025): solving their Problem 1 by any tool/approach is still open. Exact status of specific LP subclasses remains uncertain unless listed as proved in the frontier.
