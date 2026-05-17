# Karp-Rabin Oracle and Fixed-Length Explorer v0

Date: 2026-05-17

Branch: `karp-rabin-oracle-fixed-length-v0`

Scope: exact finite infrastructure for the deterministic all-length fixed-base,
fixed-prime Karp-Rabin collision problem. This is side work only and does not
supersede the STT / DS(k,1) lane.

## Source Frontier Used

Used the existing local topic notes, `reports/scouting_v2/closeout.md`, and the
attached 2026-05-17 frontier packet / oracle spec v2. No new broad literature
scouting was performed.

## Implementation

- `candidate_topics/karp_rabin_collision_detection/oracle_spec.md` now records
  the v2 exact finite oracle semantics.
- `scripts/karp_rabin_collision/oracle.py` implements the all-length oracle,
  witness verification, collision-length enumeration, and an independent brute
  force all-length enumerator for tests.
- `scripts/karp_rabin_collision/fixed_length.py` implements prefix hashes,
  fixed-length hash buckets, direct true-substring verification inside buckets,
  and an independent brute force fixed-length checker.
- `scripts/karp_rabin_collision/search_counterexamples.py` searches finite
  instances for false reductions and stores validated saved examples.
- `tests/test_karp_rabin_collision.py` covers oracle semantics, brute-force
  agreement, fixed-length agreement, and counterexample-search outcomes.

## Search Bounds

Default counterexample command:

```powershell
python -m scripts.karp_rabin_collision.search_counterexamples --alphabet-size 2 --max-n 6 --base 2 --moduli 3,5,7 --restricted-lengths 1,2
```

Bounds:

- alphabet: `{0,1}`;
- string lengths: `1 <= n <= 6`;
- base: fixed `2`;
- prime moduli: fixed list `[3,5,7]`;
- restricted-length test set: `[1,2]`;
- powers-of-two test set: all powers of two at most `n`;
- search order: increasing `n`, lexicographic string order, listed modulus
  order.

The test suite also exhaustively compared optimized and brute force all-length
oracles for:

- binary strings with `0 <= n <= 5`, base `2`, primes `[2,3,5]`;
- ternary strings with `0 <= n <= 4`, base `3`, primes `[2,3,5]`.

Fixed-length detector tests compared every length for:

- alphabets `{0,1}` and `{0,1,2}`;
- `1 <= n <= 4`;
- base equal to alphabet size;
- primes `[2,3,5]`.

## Saved Counterexamples

All three default searches found the same minimal example in the stated search
order:

```text
S = [0, 1, 0, 1]
base = 2
modulus = 3
```

Length-3 substrings:

- `S[0:3] = [0,1,0]`, hash `2 mod 3`;
- `S[1:4] = [1,0,1]`, hash `5 mod 3 = 2`;
- substrings differ and overlap, so `(length=3, i=0, j=1, hash=2)` is a real
  collision witness.

Verified reductions killed within the finite bounds:

- powers-of-two-only check fails: lengths `[1,2,4]` are collision-free, but
  length `3` collides;
- restricted set `[1,2]` fails for the same witness;
- the minimal collision length is `3`; proper divisor `[1]` and halving lengths
  `[1,2]` are collision-free.

These are counterexamples to tempting finite reductions only. They are not
lower bounds and do not rule out subtler all-length batching.

## Commands Run

```powershell
git switch -c karp-rabin-oracle-fixed-length-v0
```

Succeeded.

```powershell
python -m pytest tests\test_karp_rabin_collision.py -q
```

Failed because `pytest` is not installed in this environment:
`No module named pytest`.

```powershell
python -m unittest tests.test_karp_rabin_collision -v
```

Succeeded: 9 tests run, all OK.

```powershell
python -m scripts.karp_rabin_collision.search_counterexamples --alphabet-size 2 --max-n 6 --base 2 --moduli 3,5,7 --restricted-lengths 1,2
```

Succeeded and emitted the saved examples above.

```powershell
python -m unittest discover -v
```

Timed out after about 820.5 seconds while running the pre-existing STT-heavy
suite. No failure was printed before timeout; this is not a complete full-suite
pass.

```powershell
python -m compileall scripts\karp_rabin_collision tests\test_karp_rabin_collision.py
```

Succeeded.

```powershell
git add candidate_topics\karp_rabin_collision_detection\oracle_spec.md reports\karp_rabin_oracle_fixed_length_v0.md scripts\karp_rabin_collision\__init__.py scripts\karp_rabin_collision\fixed_length.py scripts\karp_rabin_collision\oracle.py scripts\karp_rabin_collision\search_counterexamples.py tests\test_karp_rabin_collision.py
```

Failed with `Unable to create ... .git/index.lock: Permission denied`. No commit
was attempted.

## No Theorem Claims

This artifact only supplies exact finite infrastructure and small
counterexamples to naive reductions. It does not claim an all-length algorithm,
a lower bound, closure of the Dagstuhl problem, or any probabilistic rejection
guarantee.

## Best Next Proof-Work Target

The best next target is a fixed-shift batching lemma or obstruction. For a
fixed offset `d = j-i`, study the sequence of differences
`H_p(i, ell) - H_p(i+d, ell)` across lengths `ell`, with true equality filtered
by LCE/direct equality. The proof task is to determine whether zero events over
many lengths can be batched without paying for all `(i, ell)` pairs, or to find
minimal finite obstructions showing why a proposed batching rule still hides
quadratic work.
