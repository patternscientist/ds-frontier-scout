import unittest
from itertools import product
from pathlib import Path

from scripts.karp_rabin_collision.fixed_length import CollisionWitness
from scripts.karp_rabin_collision.fixed_shift import (
    ShiftZeroEvent,
    compare_fixed_shift_enumeration_to_oracle,
    enumerate_zero_events,
    filter_true_substring_inequality,
    fixed_shift_delta_value,
    fixed_shift_deltas,
    group_zero_events_by_shift,
    load_counterexample_json,
    run_default_shift_searches,
    true_collision_witnesses_by_shift,
    validate_counterexample_record,
    validate_saved_fixed_shift_counterexamples,
)
from scripts.karp_rabin_collision.oracle import brute_force_oracle, verify_witness


class KarpRabinFixedShiftDeltaTests(unittest.TestCase):
    def test_delta_sequence_matches_prefix_hash_equality(self):
        symbols = [0, 1, 1, 0]
        records = fixed_shift_deltas(symbols, base=2, modulus=3, d=1)

        self.assertEqual(len(records), 6)
        self.assertEqual(
            fixed_shift_delta_value(symbols, base=2, modulus=3, i=0, d=1, length=1),
            2,
        )
        self.assertEqual(
            fixed_shift_delta_value(symbols, base=2, modulus=3, i=0, d=1, length=3),
            0,
        )

        zero_tuples = {
            (record.d, record.i, record.length, record.left_hash)
            for record in records
            if record.delta == 0
        }
        self.assertIn((1, 1, 1, 1), zero_tuples)
        self.assertIn((1, 0, 3, 0), zero_tuples)

    def test_zero_events_filter_by_true_substring_inequality(self):
        symbols = [0, 1, 1, 0]
        zero_events = enumerate_zero_events(symbols, base=2, modulus=3, d=1)
        true_events = filter_true_substring_inequality(symbols, zero_events)

        self.assertIn(ShiftZeroEvent(d=1, i=1, length=1, hash_value=1), zero_events)
        self.assertIn(ShiftZeroEvent(d=1, i=0, length=3, hash_value=0), true_events)
        self.assertNotIn(ShiftZeroEvent(d=1, i=1, length=1, hash_value=1), true_events)

    def test_group_zero_events_by_shift(self):
        groups = group_zero_events_by_shift([0, 1, 0, 1], base=2, modulus=3)

        self.assertEqual(set(groups), {1, 2})
        self.assertEqual(
            groups[1],
            (ShiftZeroEvent(d=1, i=0, length=3, hash_value=2),),
        )


class KarpRabinFixedShiftOracleAgreementTests(unittest.TestCase):
    def test_fixed_shift_enumeration_agrees_with_all_length_oracle(self):
        cases = ((2, 5, (2, 3, 5)), (3, 4, (2, 3, 5)))
        for alphabet_size, max_n, primes in cases:
            base = alphabet_size
            for n in range(max_n + 1):
                for symbols in product(range(alphabet_size), repeat=n):
                    for modulus in primes:
                        with self.subTest(
                            alphabet_size=alphabet_size,
                            n=n,
                            symbols=symbols,
                            modulus=modulus,
                        ):
                            comparison = compare_fixed_shift_enumeration_to_oracle(
                                symbols,
                                base,
                                modulus,
                            )
                            brute = brute_force_oracle(symbols, base, modulus)
                            self.assertTrue(comparison.agrees, comparison.to_dict())
                            self.assertEqual(comparison.oracle.witness, brute.witness)
                            self.assertEqual(
                                comparison.first_fixed_shift_witness,
                                brute.witness,
                            )

    def test_true_fixed_shift_witnesses_are_verifiable(self):
        symbols = [0, 2, 1, 0, 0, 0]
        witnesses = true_collision_witnesses_by_shift(symbols, base=3, modulus=5)

        self.assertIn(CollisionWitness(length=2, i=0, j=1, hash_value=2), witnesses)
        for witness in witnesses:
            self.assertTrue(verify_witness(symbols, 3, 5, witness))


class KarpRabinFixedShiftCounterexampleTests(unittest.TestCase):
    def test_default_shift_searches_return_valid_examples(self):
        outcomes = run_default_shift_searches()

        self.assertEqual(
            set(outcomes),
            {
                "first_last_zero_per_shift_gap",
                "minimal_zero_length_per_shift_gap",
                "arithmetic_progression_length_gap",
                "divisor_power_length_gap",
            },
        )
        for outcome in outcomes.values():
            self.assertTrue(outcome.found, outcome.to_dict())
            self.assertTrue(validate_counterexample_record(outcome.to_dict()))

    def test_saved_fixed_shift_counterexample_json_validates(self):
        root = Path(__file__).resolve().parents[1]
        payload = load_counterexample_json(
            root / "examples" / "karp_rabin_collision" / "fixed_shift_counterexamples_v0.json"
        )

        self.assertEqual(
            validate_saved_fixed_shift_counterexamples(payload),
            {
                "arithmetic_progression_length_gap": True,
                "divisor_power_length_gap": True,
                "first_last_zero_per_shift_gap": True,
                "minimal_zero_length_per_shift_gap": True,
            },
        )


if __name__ == "__main__":
    unittest.main()
