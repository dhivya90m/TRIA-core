import unittest

from tria_core import decide_release, gate_action, score_reply, LensResult


def judge_pass(*args):
    return 0.9, "Pass."


def judge_fail_policy(customer_request, sop_policy, agent_reply, lens):
    if lens["name"] == "Policy Compliance":
        return 0.0, "Fail."
    return 0.9, "Pass."


class TestReleaseDecision(unittest.TestCase):
    def test_all_clear(self):
        results = [LensResult("A", 0.9, "PASS"), LensResult("B", 0.85, "PASS")]
        self.assertEqual(decide_release(results, "S2"), "CLEARS THIS SCENARIO")

    def test_all_pass_but_borderline(self):
        results = [LensResult("A", 0.9, "PASS"), LensResult("B", 0.72, "PASS")]
        self.assertEqual(decide_release(results, "S2"), "CLEARS WITH REVIEW")

    def test_s1_fail_blocks_shipping(self):
        results = [LensResult("A", 0.0, "FAIL")]
        self.assertEqual(decide_release(results, "S1"), "DO NOT SHIP")

    def test_s2_fail_holds(self):
        results = [LensResult("A", 0.0, "FAIL")]
        self.assertEqual(decide_release(results, "S2"), "HOLD FOR FIX")

    def test_s3_fail_ships_only_with_tracked_fix(self):
        results = [LensResult("A", 0.0, "FAIL")]
        self.assertEqual(decide_release(results, "S3"), "SHIP ONLY WITH A TRACKED FIX")

    def test_error_is_incomplete(self):
        results = [LensResult("A", 0.0, "ERROR")]
        self.assertEqual(decide_release(results, "S2"), "INCOMPLETE")


class TestGate(unittest.TestCase):
    def test_clears_is_sent(self):
        self.assertEqual(gate_action("CLEARS THIS SCENARIO"), "SENT to customer")

    def test_clears_with_review_is_held(self):
        self.assertEqual(
            gate_action("CLEARS WITH REVIEW"),
            "HELD for human spot-check, not sent yet",
        )

    def test_hold_is_blocked(self):
        self.assertEqual(
            gate_action("HOLD FOR FIX"), "BLOCKED, routed to a human, not sent"
        )


class TestScoreReply(unittest.TestCase):
    def test_trap_blocks(self):
        card = score_reply("Req", "Policy", "60 days reply", judge_fail_policy, severity="S2")
        self.assertEqual(card.release_decision, "HOLD FOR FIX")
        self.assertEqual(card.failed_lenses, ["Policy Compliance"])
        self.assertIn("BLOCKED", card.gate_action)

    def test_custom_lens_alone_can_block(self):
        custom = [{
            "name": "Financial Risk",
            "pass_looks_like": "No money risk.",
            "fail_looks_like": "Money risk.",
            "needs_policy": True,
        }]
        card = score_reply(
            "Req", "Policy", "Reply", judge_pass, lenses=custom, severity="S2"
        )
        self.assertEqual(card.release_decision, "CLEARS THIS SCENARIO")
        card2 = score_reply(
            "Req", "Policy", "Reply",
            lambda *a: (0.0, "Fail."),
            lenses=custom, severity="S2",
        )
        self.assertEqual(card2.release_decision, "HOLD FOR FIX")
        self.assertEqual(card2.failed_lenses, ["Financial Risk"])


if __name__ == "__main__":
    unittest.main()
