# Karp-Rabin Fixed-Shift Batching Explorer v0

Date: 2026-05-17

Branch: `karp-rabin-fixed-shift-batching-v0`

Starting commit: `35f21cfc08a00008e53c27cc0862659d09f3368a`

Scope: exact finite proof-scouting infrastructure for equal-length
Karp-Rabin collision events grouped by fixed offset `d = j - i`. This is not a
theorem claim, not a subquadratic algorithm, and not a lower bound.

## Delta Formulation

For the fixed orientation already used by the oracle,

```text
H(i, ell) = sum_{t=0}^{ell-1} S[i+t] b^(ell-1-t) mod p.
```

For a fixed positive shift `d`, define

```text
Delta_{i,d}(ell) = H(i, ell) - H(i+d, ell) mod p.
```

The valid range is `1 <= d < n`, `1 <= ell <= n-d`, and
`0 <= i <= n-d-ell`. A zero event means the two fixed-shift substrings have the
same fingerprint. It is a real deterministic collision witness only after
directly checking

```text
S[i : i+ell] != S[i+d : i+d+ell].
```

Using prefix hashes `P[k] = H(0,k)` and powers `B[ell] = b^ell mod p`, the
computed formula is

```text
H(i, ell) = P[i+ell] - P[i] * B[ell] mod p
Delta_{i,d}(ell)
  = P[i+ell] - P[i] * B[ell]
    - P[i+d+ell] + P[i+d] * B[ell] mod p.
```

Equivalently, for fixed `i,d`,

```text
Delta_{i,d}(ell+1)
  = b * Delta_{i,d}(ell) + S[i+ell] - S[i+d+ell] mod p,
```

but the implementation uses the prefix-hash formula to stay aligned with the
existing oracle.

## Implementation

- `scripts/karp_rabin_collision/fixed_shift.py` implements:
  - `fixed_shift_deltas`;
  - `fixed_shift_delta_value`;
  - `enumerate_zero_events`;
  - `filter_true_substring_inequality`;
  - `group_zero_events_by_shift`;
  - `true_collision_witnesses_by_shift`;
  - `compare_fixed_shift_enumeration_to_oracle`;
  - finite counterexample searches for several tempting batching rules.
- `examples/karp_rabin_collision/fixed_shift_counterexamples_v0.json` stores
  checkable saved examples emitted by the fixed-shift CLI.
- `tests/test_karp_rabin_fixed_shift.py` compares fixed-shift enumeration with
  the all-length oracle on small exhaustive fixtures and validates the saved
  JSON.

The canonical event order is increasing `(ell, i, j)`. For a fixed shift this
is increasing length, then increasing start. The "first/last zero" rule tested
below refers only to this explicit order.

## Search Bounds

Default command:

```powershell
python -m scripts.karp_rabin_collision.fixed_shift --output examples\karp_rabin_collision\fixed_shift_counterexamples_v0.json
```

Bounds:

- alphabet: `{0,1,2}`;
- string lengths: `1 <= n <= 6`;
- base: fixed `3`;
- prime moduli: fixed list `[2,3,5,7]`;
- arithmetic progressions tested: `(start, step)` in
  `[(1,2), (2,2), (1,3), (2,3), (3,3)]`;
- search order: increasing `n`, lexicographic string order, listed modulus
  order.

## Saved Counterexamples

All examples below are minimal only in the stated finite search order.

### First/Last Zero Per Shift

```text
S = [0, 2, 1, 0, 0, 0]
base = 3
modulus = 5
missed witness = {length=2, i=0, j=1, hash=2}
```

For `d = 1`, the zero events in canonical order include equal-substring events
at `(ell=1,i=3)`, `(ell=1,i=4)`, the true collision at `(ell=2,i=0)`, and an
equal-substring event at `(ell=2,i=3)`. Checking only the first and last zero
events for each shift checks no true collision and misses the middle event.

### Minimal Zero Length Per Shift

```text
S = [0, 1, 1]
base = 3
modulus = 3
missed witness = {length=2, i=0, j=1, hash=1}
```

For `d = 1`, the minimum zero length is `1`, witnessed by equal substrings at
positions `1` and `2`. The real collision is at length `2`.

### Arithmetic Progression Lengths

```text
S = [0, 1, 0]
base = 3
modulus = 2
progression = 1, 3, 5, ...
missed witness = {length=2, i=0, j=1, hash=1}
```

Checking only odd lengths selects the equal length-1 zero event at shift `2`
and misses the length-2 collision at shift `1`.

### Divisors / Powers Of Two Lengths

```text
S = [0, 1, 0, 1]
base = 3
modulus = 7
checked global lengths = {1, 2, 4}
missed witness = {length=3, i=0, j=1, hash=3}
```

The selected zero events at lengths `1` and `2` are equal-substring events at
shift `2`; the real collision occurs at length `3`.

## Audit And Limits

- These are finite counterexamples to specific selectors only.
- The first/last result depends on the explicitly stated canonical order; it
  does not refute every possible endpoint-style batching scheme.
- The arithmetic-progression search covers only the listed progressions.
- The divisor/power search uses global string length `n`; it does not cover
  every possible per-shift length generator.
- Equal-substring zero events are deliberately retained in the audit trail,
  because a batching rule can spend work on them while still missing the first
  true collision.
- No randomized rejection model is used here. Base and modulus are fixed inputs.

## Commands Run

```powershell
git switch -c karp-rabin-fixed-shift-batching-v0 35f21cfc08a00008e53c27cc0862659d09f3368a
```

Succeeded.

```powershell
python -m scripts.karp_rabin_collision.fixed_shift --output examples\karp_rabin_collision\fixed_shift_counterexamples_v0.json
```

Succeeded and wrote the saved JSON artifact.

```powershell
python -m unittest tests.test_karp_rabin_fixed_shift -v
python -m unittest tests.test_karp_rabin_collision -v
```

Succeeded: 7 fixed-shift tests and 9 existing Karp-Rabin tests all OK.

## No Theorem Claims

This artifact supplies exact finite infrastructure and concrete small misses
for naive fixed-shift batching rules. It does not claim an all-length
subquadratic algorithm, a lower bound, closure of any open problem, or any
probabilistic rejection guarantee.
