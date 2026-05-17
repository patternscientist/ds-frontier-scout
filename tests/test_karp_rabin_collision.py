import unittest
from itertools import product

from scripts.karp_rabin_collision.fixed_length import (
    brute_force_fixed_length_collision,
    find_fixed_length_collision,
)
from scripts.karp_rabin_collision.oracle import (
    all_length_oracle,
    brute_force_oracle,
    verify_witness,
)
from scripts.karp_rabin_collision.search_counterexamples import (
    find_powers_of_two_gap,
    run_default_searches,
    validate_saved_counterexamples,
)


class KarpRabinOracleTests(unittest.TestCase):
    def test_equal_repeated_substrings_are_not_collisions(self):
        result = all_length_oracle("aaaa", base=257, modulus=101)

        self.assertFalse(result.has_collision)
        self.assertIsNone(result.witness)

    def test_overlapping_real_collisions_count(self):
        result = all_length_oracle([0, 1, 1, 0], base=2, modulus=3)

        self.assertTrue(result.has_collision)
        self.assertEqual(result.witness.as_tuple(), (3, 0, 1))
        self.assertTrue(verify_witness([0, 1, 1, 0], 2, 3, result.witness))

    def test_collision_at_length_one_is_detected(self):
        result = all_length_oracle([0, 2], base=3, modulus=2)

        self.assertTrue(result.has_collision)
        self.assertEqual(result.witness.as_tuple(), (1, 0, 1))

    def test_no_collision_instance_returns_false(self):
        result = all_length_oracle([0, 1, 2], base=3, modulus=101)

        self.assertFalse(result.has_collision)
        self.assertEqual(result.checked_lengths, 3)

    def test_brute_force_pair_enumeration_agrees_with_optimized_oracle(self):
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
                            optimized = all_length_oracle(symbols, base, modulus)
                            brute = brute_force_oracle(symbols, base, modulus)
                            self.assertEqual(optimized.witness, brute.witness)
                            self.assertEqual(
                                optimized.has_collision,
                                brute.has_collision,
                            )

    def test_fixed_length_detector_agrees_with_brute_force(self):
        for alphabet_size in (2, 3):
            base = alphabet_size
            for n in range(1, 5):
                for symbols in product(range(alphabet_size), repeat=n):
                    for modulus in (2, 3, 5):
                        for length in range(1, n + 1):
                            with self.subTest(
                                alphabet_size=alphabet_size,
                                symbols=symbols,
                                modulus=modulus,
                                length=length,
                            ):
                                self.assertEqual(
                                    find_fixed_length_collision(
                                        symbols, base, modulus, length
                                    ),
                                    brute_force_fixed_length_collision(
                                        symbols, base, modulus, length
                                    ),
                                )


class KarpRabinCounterexampleSearchTests(unittest.TestCase):
    def test_default_searches_return_checkable_examples(self):
        outcomes = run_default_searches(max_n=6)

        self.assertEqual(
            set(outcomes),
            {
                "powers_of_two_gap",
                "restricted_length_gap",
                "minimal_length_structure_gap",
            },
        )
        for outcome in outcomes.values():
            self.assertTrue(outcome.found, outcome.to_dict())
            example = outcome.example
            witness = example["missed_witness"]
            self.assertNotIn(witness["length"], example["restricted_lengths"])
            result = all_length_oracle(
                example["S"],
                example["base"],
                example["modulus"],
            )
            self.assertEqual(result.witness.to_dict(), witness)

    def test_saved_counterexamples_validate(self):
        self.assertEqual(
            validate_saved_counterexamples(),
            {
                "powers_of_two_gap": True,
                "restricted_prefix_gap": True,
                "minimal_length_structure_gap": True,
            },
        )

    def test_none_found_outcome_records_bounds(self):
        outcome = find_powers_of_two_gap(max_n=3)

        self.assertFalse(outcome.found)
        self.assertIsNone(outcome.example)
        self.assertEqual(outcome.bounds["max_n"], 3)
        self.assertIn("none found", " ".join(outcome.notes))


if __name__ == "__main__":
    unittest.main()
