"""
Product data ingestion utilities for BBFB processing.
"""
from typing import Dict, Any, List, Tuple, Optional

REQUIRED_RAW_FIELDS = ("make", "model", "category", "price")
SCORE_FIELDS = ("reliability", "performance", "efficiency")
ATTRIBUTE_FIELDS = (
    "reliability",
    "performance",
    "efficiency",
    "failure_rate",
    "repair_cost",
    "energy_cost",
)


def parse_product_name(name: str) -> Tuple[str, str]:
    """Split a product name into make and model."""
    if not isinstance(name, str):
        raise ValueError("Product name must be a string")

    cleaned = name.strip()
    if not cleaned:
        raise ValueError("Product name cannot be empty")

    parts = cleaned.split()
    make = parts[0]
    model = " ".join(parts[1:]).strip() if len(parts) > 1 else ""
    return make, model


def convert_normalized_product(
    product: Dict[str, Any],
    category: str = "washing_machine"
) -> Dict[str, Any]:
    """Convert a normalized product entry into RawProductData format."""
    if not isinstance(product, dict):
        raise ValueError("Product must be a dictionary")

    if "name" not in product:
        raise ValueError("Product name is required")

    if "price" not in product:
        raise ValueError("Product price is required")

    make, model = parse_product_name(product["name"])
    if not model:
        raise ValueError("Product model is required")
    attributes = {key: product[key] for key in ATTRIBUTE_FIELDS if key in product}

    return {
        "make": make,
        "model": model,
        "category": category,
        "price": product["price"],
        "attributes": attributes,
    }


def convert_normalized_products(
    products: List[Dict[str, Any]],
    category: str = "washing_machine"
) -> List[Dict[str, Any]]:
    """Convert a list of normalized products into RawProductData format."""
    if not isinstance(products, list):
        raise ValueError("Products payload must be a list")
    return [convert_normalized_product(product, category=category) for product in products]


def validate_raw_product(product: Dict[str, Any]) -> List[str]:
    """Return missing required fields for a RawProductData entry."""
    if not isinstance(product, dict):
        return list(REQUIRED_RAW_FIELDS)

    missing = []
    for field in REQUIRED_RAW_FIELDS:
        value = product.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(field)
    return missing


def calculate_bbfb_score(product: Dict[str, Any]) -> Optional[float]:
    """Calculate a basic BBFB score from available normalized metrics."""
    if not isinstance(product, dict):
        return None

    attributes = product.get("attributes")
    if not isinstance(attributes, dict):
        return None

    scores = [
        attributes.get(field)
        for field in SCORE_FIELDS
        if isinstance(attributes.get(field), (int, float))
    ]
    if not scores:
        return None
    return round(sum(scores) / len(scores), 3)


def evaluate_products(products: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Evaluate RawProductData entries for BBFB processing."""
    results = []
    valid_count = 0
    for product in products:
        missing = validate_raw_product(product)
        if not missing:
            valid_count += 1

        results.append({
            "product": product,
            "missing_fields": missing,
            "bbfb_score": calculate_bbfb_score(product),
        })

    return {
        "summary": {
            "processed": len(products),
            "valid": valid_count,
            "invalid": len(products) - valid_count,
        },
        "results": results,
    }
