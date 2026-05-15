# OpenEvolve Fit

OpenEvolve suitability: 5/5.

Plausible automated evaluators:

- enumerate unlabeled tree topologies up to `n`;
- enumerate all STTs for a topology and compute depth vectors;
- solve Golinsky's LP for random and facet-normal objectives;
- compare LP optimum against best STT optimum to certify gaps;
- run root rounding under best-case and worst-case tie-breaking;
- test candidate valid inequalities against all enumerated STT points and known fractional vertices;
- search for new fractional vertices in paths, almost-stars, and edge-diameter-2/3/4 topologies.

Certificate opportunities:

- exact rational LP certificates for integrality gaps;
- facet normals for false facets of the STT depth polytope;
- minimal topologies witnessing failure of candidate inequalities;
- proof-assistant-friendly enumeration logs for small `n`.

Immediate implementation path:

1. Extract `STTLP-sage-python3-source.zip` from the arXiv source.
2. Reproduce Sadeh-Kaplan-Zwick Tables 1, 2, 3, 6, and 7.
3. Add search modes for edge-diameter-3 topologies and paths.
4. Add a candidate-inequality generator and a falsifier over enumerated STTs plus known fractional LP vertices.

Main caveat: Sage/polytope enumeration may dominate runtime. A pure-Python layer should handle topology/STT enumeration, with Sage reserved for LP/polytope calls.
