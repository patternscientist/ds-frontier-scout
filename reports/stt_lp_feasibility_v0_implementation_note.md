# STT LP Feasibility v0 Implementation Note

Date: 2026-05-15

## Implemented

- Added `scripts/stt_checker/lp_feasibility.py`.
- Added dense proof-mode domain generation for `golinsky_stt_lp_v0`:
  `D_i`, ordered `X_ij` for `i != j`, and `Z_kij` for strict base-tree path
  interiors with endpoint convention `i < j`.
- Added exact rational parsing through the existing rational parser, including
  rejection of floats and decimal strings.
- Added duplicate, missing, and unknown variable rejection for dense variable
  arrays.
- Added exact checks for nonnegativity, ancestry, loose-LCA, and depth
  constraints.
- Added optional exact objective recomputation in LP strict-depth convention.
- Added STT-induced `(D,X,Z)` construction for tests and fixtures.
- Added `python -m scripts.stt_checker.cli check-lp`.
- Added small path/star induced LP examples under `examples/stt_lp/`.
- Added tests in `tests/test_stt_lp_feasibility.py`.
- Added documentation in `docs/stt_lp_feasibility_v0.md`.

## Unsupported

This implementation does not provide:

- LP solving;
- root rounding;
- integrality-gap checking;
- depth projection or lower-envelope testing;
- exact dual certificates;
- optional LP variants beyond the vanilla `golinsky_stt_lp_v0` specification.

Unsupported `root_rounding` and `integrality_gap` fields remain rejected in
proof-mode LP certificates.

## Commands Run During Implementation

```text
python -m unittest -v tests.test_stt_lp_feasibility
python -m unittest discover -v
python -m scripts.stt_checker.cli check examples/stt/path_4_proof.json
python -m scripts.stt_checker.cli check examples/stt/star_4_proof.json
python -m scripts.stt_checker.cli check examples/stt/long_star_7.json
python -m scripts.stt_checker.frontier_artifacts --max-n 7 --max-enumeration 100000
python -m scripts.stt_checker.cli check-lp examples/stt_lp/path_4_stt_induced_lp.json
python -m scripts.stt_checker.cli check-lp examples/stt_lp/star_4_stt_induced_lp.json
```

## Known Limitations

The checker is a proof replay tool for one supplied rational primal point. It
does not search for a feasible point, prove optimality, prove non-integrality,
or establish any theorem about STT depth hulls. A passing certificate means only
that the topology is valid, the dense domains match the spec, and the supplied
rational point satisfies the vanilla constraints exactly.
