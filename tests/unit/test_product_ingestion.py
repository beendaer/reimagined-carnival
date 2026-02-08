"""
Unit tests for product ingestion utilities.
"""
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from services.product_ingestion import (
    parse_product_name,
    convert_normalized_product,
    evaluate_products
)


class TestProductIngestion(unittest.TestCase):
    """Test product ingestion helpers."""

    def test_parse_product_name(self):
        """Ensure product names split into make/model."""
        make, model = parse_product_name("Haier HWF75AW3")
        self.assertEqual(make, "Haier")
        self.assertEqual(model, "HWF75AW3")

    def test_convert_normalized_product(self):
        """Ensure normalized products convert into raw format."""
        normalized = {
            "name": "Haier HWF75AW3",
            "price": 454.0,
            "reliability": 0.94,
            "performance": 0.90,
            "efficiency": 0.90,
            "failure_rate": 0.03,
            "repair_cost": 350,
            "energy_cost": 45
        }
        raw = convert_normalized_product(normalized)
        self.assertEqual(raw["make"], "Haier")
        self.assertEqual(raw["model"], "HWF75AW3")
        self.assertEqual(raw["category"], "washing_machine")
        self.assertEqual(raw["price"], 454.0)
        self.assertEqual(raw["attributes"]["repair_cost"], 350)

    def test_evaluate_products(self):
        """Ensure BBFB evaluation returns scores and summary."""
        product = {
            "make": "Haier",
            "model": "HWF75AW3",
            "category": "washing_machine",
            "price": 454.0,
            "attributes": {
                "reliability": 0.94,
                "performance": 0.90,
                "efficiency": 0.90
            }
        }
        result = evaluate_products([product])
        self.assertEqual(result["summary"]["processed"], 1)
        self.assertEqual(result["summary"]["valid"], 1)
        self.assertAlmostEqual(result["results"][0]["bbfb_score"], 0.913, places=3)


if __name__ == "__main__":
    unittest.main()
