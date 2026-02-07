"""Basic BBFB (Baseline Benefit & Flexibility) scoring utilities.

This module provides a small, dependency-free scoring toolkit composed of:
- Hard gate checks that immediately disqualify a product.
- Grace-curve penalty helpers (exponential, logistic, power).
- A weighted benefit calculator and a simple composite score helper.
"""

from __future__ import annotations

import math
from typing import Mapping


def _clamp01(value: float) -> float:
    """Clamp a numeric value to the inclusive range [0, 1]."""
    return max(0.0, min(1.0, float(value)))


# HARD GATES
def hard_gate_check(product: Mapping[str, object]) -> bool:
    """Return True only when all baseline capability gates are satisfied."""
    gates = [
        product.get("has_baseline_resolution", False),
        product.get("has_required_safety", False),
        product.get("has_required_hdr", False),
        product.get("has_basic_os_support", False),
    ]
    # Explicitly cast to bool to tolerate truthy values.
    return all(bool(flag) for flag in gates)


# GRACE CURVES
def exp_penalty(x: float, k: float = 10.0) -> float:
    """Exponential grace curve (historically named penalty). Higher ``x`` yields a higher factor."""
    x = _clamp01(x)
    return 1.0 - math.exp(-k * x)


def logistic_penalty(x: float, t: float = 0.05, k: float = 20.0) -> float:
    """Logistic grace curve centered at threshold ``t`` (named penalty for legacy compatibility)."""
    x = _clamp01(x)
    return 1.0 / (1.0 + math.exp(-k * (x - t)))


def power_penalty(x: float, alpha: float = 0.5) -> float:
    """Power-law grace curve/transform (legacy penalty name)."""
    x = _clamp01(x)
    if abs(alpha) < 1e-9:
        return 1.0
    return x**alpha


# WEIGHTED PRODUCT BENEFIT
def weighted_product_benefit(product: Mapping[str, object], weights: Mapping[str, float]) -> float:
    """
    Compute a normalized weighted benefit score in [0, 1].

    Only metrics that appear in ``weights`` are considered. Missing metrics
    default to 0. If all weights are zero, 0.0 is returned.
    """
    total_weight = 0.0
    weighted_sum = 0.0

    for metric, weight in weights.items():
        if abs(weight) < 1e-9:
            continue
        total_weight += weight
        weighted_sum += _clamp01(product.get(metric, 0.0)) * weight

    if total_weight == 0.0:
        return 0.0

    return weighted_sum / total_weight


def compute_final_score(
    product: Mapping[str, object],
    weights: Mapping[str, float],
    *,
    use_penalties: bool = True,
) -> float:
    """
    Compute a composite score using hard gates, weighted benefit, and optional penalties.

    If any hard gate fails, the score is 0. Otherwise, a weighted benefit is
    multiplied by the product of configured penalty factors derived from
    ``product.get("penalty_inputs", {})`` using the grace curve helpers. Penalty
    values are applied only when explicitly provided (missing or ``None`` values
    skip that penalty), and ``threshold`` may be provided as a legacy alias for
    ``logistic_threshold``.
    """
    if not hard_gate_check(product):
        return 0.0

    benefit = weighted_product_benefit(product, weights)

    if not use_penalties:
        return benefit

    penalty_inputs = dict(product.get("penalty_inputs", {}))
    penalty_factors = []

    if "exp" in penalty_inputs:
        exp_value = penalty_inputs.get("exp")
        if exp_value is not None:
            exp_k = penalty_inputs.get("exp_k", 10.0)
            penalty_factors.append(exp_penalty(exp_value, exp_k))

    if "logistic" in penalty_inputs:
        logistic_value = penalty_inputs.get("logistic")
        if logistic_value is not None:
            logistic_threshold = penalty_inputs.get(
                "logistic_threshold", penalty_inputs.get("threshold", 0.05)
            )
            logistic_k = penalty_inputs.get("logistic_k", 20.0)
            penalty_factors.append(logistic_penalty(logistic_value, logistic_threshold, logistic_k))

    if "power" in penalty_inputs:
        power_value = penalty_inputs.get("power")
        if power_value is not None:
            power_alpha = penalty_inputs.get("alpha", 0.5)
            penalty_factors.append(power_penalty(power_value, power_alpha))

    total_penalty = 1.0
    for factor in penalty_factors:
        total_penalty *= factor

    return benefit * total_penalty
