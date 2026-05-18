# DS(3,2)/DS(4,2) Packet-Window Capacity Hardening

## Result

No packet-window gap was found in either required finite universe.

The closure claim here is finite and certificate-backed only for the declared weight universes. It does not prove DS(k,2), DS(2,m), DS(k,m), public Golinsky/SKZ LP exactness, or general STT exactness.

Packet-window closure is also separate from full H1 exactness: by the prompt-provided implications, a mass-`OPT` packet-window certificate gives `Pkt_{k,2}(w)=OPT_{k,2}(w)` for that tested weight, and then H1 is exact for that weight.

## Finite Universes

- `DS(3,2)`: `2186` closed weights in `DS(3,2) full ternary cube {0,1,2}^7 minus zero`; true schedules `1135`, deduplicated depth vectors `1135`, packet atoms `228`, canonical LP solves `539`, max denominator `3`, failures `0`.
- `DS(4,2)`: `255` closed weights in `DS(4,2) full binary cube {0,1}^8 minus zero`; true schedules `7284`, deduplicated depth vectors `7284`, packet atoms `456`, canonical LP solves `59`, max denominator `2`, failures `0`.

## Construction

- Coordinates are H1 first-hit variables `z[S,v]` for connected `S` and `v in S`.
- Capacities are exact strict-path coefficients `cap_w(S,v)=sum_{x != v : P(x,v)=S} w_x`.
- True `OPT` values come from exact recursive-search-tree depth-vector enumeration.
- Packet atoms are the DS(2,2) `Sigma/Lambda/Gamma/Delta/Omega/Pi` atoms embedded into every two-left window.
- Floating-point simplex is used only to locate candidate LP bases; stored coefficients are exact rationals and are verified coordinatewise.

## Scope Guardrails

This hardening uses only H1 coordinate capacities and embedded DS(2,2) packet atoms. It does not use H2, refined-Z, path-monotonicity, ancestry-transitivity, LCA-separation, or mixed-second-difference rows.

Raw `Sigma` atoms remain essential certificate bookkeeping inherited from DS(2,2); this report does not promote them to a conceptual all-k theorem.

## Artifacts

- DS(3,2) ternary factorizations: `data\ds32_packet_window_factorizations_ternary.json`.
- DS(4,2) binary factorizations: `data\ds42_packet_window_factorizations_binary.json`.
- Gap witnesses: `data\ds32_ds42_packet_window_gap_witnesses.json`.
- Tests: `tests/test_ds32_ds42_packet_window_capacity.py`.

## Verification Commands

```powershell
python -m src.ds22_simplex_augmented_packet_conic --verify
python -m unittest tests.test_ds22_simplex_augmented_packet_conic
python -m src.ds32_ds42_packet_window_capacity --verify
python -m pytest tests/test_ds32_ds42_packet_window_capacity.py
```

## Next Proof-Work Prompt

Try to prove or refute the all-k DS(k,2) packet-window gluing conjecture using only the H1 capacity LP and the embedded DS(2,2) `Sigma/Lambda/Gamma/Delta/Omega/Pi` atoms. Treat the DS(3,2) ternary and DS(4,2) binary certificates as finite evidence, not as theorem proof.
