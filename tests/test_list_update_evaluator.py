import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from fractions import Fraction
from itertools import product

from scripts.list_update.adversarial_traces import (
    build_adversarial_payload,
    enumerate_request_traces,
)
from scripts.list_update.cli import main as cli_main
from scripts.list_update.exact_evaluator import (
    competitive_ratio,
    kendall_tau_distance,
    offline_optimum,
    standard_transition_witnesses,
)
from scripts.list_update.model import (
    all_list_states,
    free_successors,
    initial_state_for_n,
)
from scripts.list_update.policies import (
    DETERMINISTIC_POLICIES,
    RANDOMIZED_POLICIES,
    evaluate_deterministic_policy,
    evaluate_randomized_policy,
)


class ListUpdateModelTests(unittest.TestCase):
    def test_free_successors_are_forward_moves_only(self):
        state = (0, 2, 1)
        self.assertEqual(
            free_successors(state, 1),
            ((1, 0, 2), (0, 1, 2), (0, 2, 1)),
        )
        self.assertEqual(free_successors(state, 0), (state,))

    def test_kendall_tau_distance_tiny_cases(self):
        self.assertEqual(kendall_tau_distance((0, 1, 2), (0, 1, 2)), 0)
        self.assertEqual(kendall_tau_distance((0, 1, 2), (1, 0, 2)), 1)
        self.assertEqual(kendall_tau_distance((0, 1, 2), (2, 1, 0)), 3)


class ListUpdatePolicyTests(unittest.TestCase):
    def test_hand_checked_two_item_trace(self):
        trace = (1, 0)
        offline = offline_optimum(trace, n=2)
        mtf = evaluate_deterministic_policy(DETERMINISTIC_POLICIES["mtf"], trace, n=2)
        static = evaluate_deterministic_policy(
            DETERMINISTIC_POLICIES["static"], trace, n=2
        )

        self.assertEqual(offline.cost, 3)
        self.assertEqual(static.cost, 3)
        self.assertEqual(mtf.cost, 4)
        self.assertEqual(competitive_ratio(mtf.cost, offline.cost), Fraction(4, 3))

    def test_mtf_and_transpose_costs_on_three_item_example(self):
        trace = (2, 1, 2)
        mtf = evaluate_deterministic_policy(DETERMINISTIC_POLICIES["mtf"], trace, n=3)
        transpose = evaluate_deterministic_policy(
            DETERMINISTIC_POLICIES["transpose"], trace, n=3
        )
        static = evaluate_deterministic_policy(
            DETERMINISTIC_POLICIES["static"], trace, n=3
        )

        self.assertEqual(mtf.cost, 8)
        self.assertEqual(tuple(step.access_cost for step in mtf.steps), (3, 3, 2))
        self.assertEqual(transpose.cost, 9)
        self.assertEqual(tuple(step.access_cost for step in transpose.steps), (3, 3, 3))
        self.assertEqual(static.cost, 8)

    def test_randomized_placeholder_uses_exact_rationals(self):
        trace = (2, 1, 2)
        evaluation = evaluate_randomized_policy(
            RANDOMIZED_POLICIES["half_mtf_half_transpose"],
            trace,
            n=3,
        )

        self.assertEqual(evaluation.expected_cost, Fraction(33, 4))
        self.assertEqual(sum(probability for _state, probability in evaluation.final_distribution), 1)
        self.assertTrue(all(isinstance(step.expected_access_cost, Fraction) for step in evaluation.steps))


class ListUpdateOfflineOptimumTests(unittest.TestCase):
    def test_offline_optimum_can_use_standard_paid_rearrangement(self):
        offline = offline_optimum((2,), n=3)

        self.assertEqual(offline.cost, 3)
        self.assertEqual(len(offline.steps), 1)
        self.assertEqual(
            offline.steps[0].paid_exchange_cost + offline.steps[0].access_cost,
            3,
        )

    def test_hand_checked_offline_witnesses_use_paid_exchanges_before_access(self):
        cases = (
            (
                3,
                (2, 1, 1, 2),
                8,
                (
                    ((0, 1, 2), (1, 0, 2), 1, 3, (1, 2, 0)),
                    ((1, 2, 0), (1, 2, 0), 0, 1, (1, 2, 0)),
                    ((1, 2, 0), (1, 2, 0), 0, 1, (1, 2, 0)),
                    ((1, 2, 0), (1, 2, 0), 0, 2, (1, 2, 0)),
                ),
            ),
            (
                3,
                (2, 1, 2, 1),
                8,
                (
                    ((0, 1, 2), (1, 0, 2), 1, 3, (1, 2, 0)),
                    ((1, 2, 0), (1, 2, 0), 0, 1, (1, 2, 0)),
                    ((1, 2, 0), (1, 2, 0), 0, 2, (1, 2, 0)),
                    ((1, 2, 0), (1, 2, 0), 0, 1, (1, 2, 0)),
                ),
            ),
            (
                4,
                (3, 2, 2, 3),
                10,
                (
                    ((0, 1, 2, 3), (2, 0, 1, 3), 2, 4, (2, 3, 0, 1)),
                    ((2, 3, 0, 1), (2, 3, 0, 1), 0, 1, (2, 3, 0, 1)),
                    ((2, 3, 0, 1), (2, 3, 0, 1), 0, 1, (2, 3, 0, 1)),
                    ((2, 3, 0, 1), (2, 3, 0, 1), 0, 2, (2, 3, 0, 1)),
                ),
            ),
        )

        for n, trace, expected_cost, expected_steps in cases:
            with self.subTest(n=n, trace=trace):
                offline = offline_optimum(trace, n=n)
                observed_steps = tuple(
                    (
                        step.state_before,
                        step.access_state,
                        step.paid_exchange_cost,
                        step.access_cost,
                        step.state_after,
                    )
                    for step in offline.steps
                )

                self.assertEqual(offline.cost, expected_cost)
                self.assertEqual(observed_steps, expected_steps)
                self.assertTrue(
                    any(step.paid_exchange_cost > 0 for step in offline.steps)
                )

    def test_transition_witnesses_match_independent_exhaustive_enumeration(self):
        start = (0, 2, 1)
        request = 1
        expected = _independent_transition_costs(start, request)
        actual = {
            witness.post_state: witness.total_cost
            for witness in standard_transition_witnesses(start, request)
        }
        self.assertEqual(actual, expected)

    def test_dp_matches_recursive_exhaustive_transition_enumeration(self):
        n = 3
        for length in range(4):
            for trace in product(range(n), repeat=length):
                offline = offline_optimum(trace, n=n)
                brute = _brute_force_standard_optimum(initial_state_for_n(n), trace)
                self.assertEqual(offline.cost, brute, msg=f"trace={trace}")


class ListUpdateAdversarialTraceTests(unittest.TestCase):
    def test_enumerates_all_nonempty_traces_up_to_bound_for_n2(self):
        traces = enumerate_request_traces(n=2, max_length=2)

        self.assertEqual(
            traces,
            ((0,), (1,), (0, 0), (0, 1), (1, 0), (1, 1)),
        )

    def test_adversarial_payload_scores_each_deterministic_policy_for_n2(self):
        payload = build_adversarial_payload(n=2, max_length=2, top_k=1)

        self.assertEqual(payload["trace_count"], 6)
        self.assertEqual(set(payload["policies"]), set(DETERMINISTIC_POLICIES))
        self.assertEqual(
            payload["policies"]["mtf"][0],
            {
                "trace": [1, 0],
                "policy_cost": "4",
                "offline_cost": "3",
                "ratio_to_offline": "4/3",
                "final_state": [0, 1],
                "offline_final_state": [0, 1],
            },
        )
        self.assertEqual(payload["policies"]["static"][0]["trace"], [1, 1])
        self.assertEqual(
            payload["policies"]["static"][0]["ratio_to_offline"],
            "4/3",
        )


class ListUpdateCliTests(unittest.TestCase):
    def test_empty_trace_is_rejected_without_partial_json_output(self):
        stdout = io.StringIO()
        stderr = io.StringIO()

        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = cli_main(["--n", "3", "--trace", ""])

        self.assertEqual(status, 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("--trace must contain at least one request", stderr.getvalue())


def _independent_transition_costs(state, request):
    best_by_post = {}
    for access_state in all_list_states(len(state)):
        paid_cost = kendall_tau_distance(state, access_state)
        access_cost = access_state.index(request) + 1
        for post_state in free_successors(access_state, request):
            total = paid_cost + access_cost
            best_by_post[post_state] = min(best_by_post.get(post_state, total), total)
    return best_by_post


def _brute_force_standard_optimum(state, trace):
    if not trace:
        return 0
    request = trace[0]
    best = None
    for access_state in all_list_states(len(state)):
        paid_cost = kendall_tau_distance(state, access_state)
        access_cost = access_state.index(request) + 1
        for post_state in free_successors(access_state, request):
            cost = paid_cost + access_cost + _brute_force_standard_optimum(
                post_state,
                trace[1:],
            )
            if best is None or cost < best:
                best = cost
    if best is None:
        raise AssertionError("no transition found")
    return best


if __name__ == "__main__":
    unittest.main()
