import unittest

import bbfb_engine as engine


class TestBBFBEngine(unittest.TestCase):
    def test_hard_gate_check(self):
        product = {
            "has_baseline_resolution": True,
            "has_required_safety": True,
            "has_required_hdr": True,
            "has_basic_os_support": True,
        }
        self.assertTrue(engine.hard_gate_check(product))

        product["has_required_hdr"] = False
        self.assertFalse(engine.hard_gate_check(product))

    def test_grace_curve_clamping(self):
        # Values outside [0, 1] should be clamped before evaluation.
        self.assertAlmostEqual(engine.exp_penalty(2.0), engine.exp_penalty(1.0))
        self.assertAlmostEqual(engine.power_penalty(-0.5), 0.0)
        self.assertGreater(engine.logistic_penalty(0.5), engine.logistic_penalty(0.0))

    def test_weighted_product_benefit(self):
        product = {"reliability": 0.8, "performance": 0.6}
        weights = {"reliability": 0.6, "performance": 0.4}
        expected = (0.8 * 0.6 + 0.6 * 0.4) / (0.6 + 0.4)
        self.assertAlmostEqual(engine.weighted_product_benefit(product, weights), expected)

    def test_weighted_product_benefit_handles_zero_weight(self):
        self.assertEqual(engine.weighted_product_benefit({}, {"unused": 0.0}), 0.0)

    def test_compute_final_score_with_penalties(self):
        product = {
            "has_baseline_resolution": True,
            "has_required_safety": True,
            "has_required_hdr": True,
            "has_basic_os_support": True,
            "reliability": 0.8,
            "performance": 0.6,
            "penalty_inputs": {"exp": 0.1, "logistic": 0.05, "power": 0.25, "alpha": 0.5},
        }
        weights = {"reliability": 0.6, "performance": 0.4}

        benefit = engine.weighted_product_benefit(product, weights)
        penalties = (
            engine.exp_penalty(0.1)
            * engine.logistic_penalty(0.05)
            * engine.power_penalty(0.25, 0.5)
        )
        self.assertAlmostEqual(engine.compute_final_score(product, weights), benefit * penalties)

    def test_compute_final_score_without_penalty_inputs(self):
        product = {
            "has_baseline_resolution": True,
            "has_required_safety": True,
            "has_required_hdr": True,
            "has_basic_os_support": True,
            "reliability": 0.9,
            "performance": 0.7,
        }
        weights = {"reliability": 0.5, "performance": 0.5}
        benefit = engine.weighted_product_benefit(product, weights)
        self.assertAlmostEqual(engine.compute_final_score(product, weights), benefit)

    def test_compute_final_score_blocks_on_gates(self):
        product = {"has_baseline_resolution": False}
        score = engine.compute_final_score(product, {"metric": 1.0})
        self.assertEqual(score, 0.0)


if __name__ == "__main__":
    unittest.main()
