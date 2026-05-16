"""Small feedback helpers for ISYE 4031 executable tutorials."""

from __future__ import annotations

import math
from typing import Iterable


def _status(ok: bool, success: str, failure: str) -> str:
    label = "PASS" if ok else "CHECK"
    detail = success if ok else failure
    return f"{label}: {detail}"


def check(condition: bool, success: str, failure: str) -> str:
    """Return a readable pass/check message for notebook exercises."""
    return _status(bool(condition), success, failure)


def check_close(
    name: str,
    value: float,
    expected: float,
    tolerance: float,
    hint: str | None = None,
) -> str:
    """Check that a numeric answer is within an absolute tolerance."""
    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return f"CHECK: {name} should be numeric. {hint or ''}".strip()

    ok = math.isclose(numeric_value, expected, abs_tol=tolerance)
    success = f"{name} is close enough: {numeric_value:.4g}."
    failure = (
        f"{name} is {numeric_value:.4g}, but it should be within "
        f"{tolerance:g} of {expected:.4g}."
    )
    if hint:
        failure += f" Hint: {hint}"
    return _status(ok, success, failure)


def check_columns(df, required: Iterable[str]) -> str:
    """Check that a dataframe contains required columns."""
    required = list(required)
    missing = [col for col in required if col not in df.columns]
    return _status(
        len(missing) == 0,
        f"Found the required columns: {', '.join(required)}.",
        f"Missing columns: {', '.join(missing)}.",
    )


def check_sign(name: str, value: float, expected: str) -> str:
    """Check whether a numeric value has the expected sign."""
    numeric_value = float(value)
    if expected == "positive":
        ok = numeric_value > 0
    elif expected == "negative":
        ok = numeric_value < 0
    elif expected == "zero":
        ok = abs(numeric_value) < 1e-12
    else:
        raise ValueError("expected must be positive, negative, or zero")

    return _status(
        ok,
        f"{name} has the expected {expected} sign.",
        f"{name} does not have the expected {expected} sign. Recheck the model formula and variable order.",
    )


def check_interval_order(lower: float, estimate: float, upper: float, name: str) -> str:
    """Check that an interval lower bound, estimate, and upper bound are ordered."""
    ok = float(lower) < float(estimate) < float(upper)
    return _status(
        ok,
        f"{name} is ordered correctly: lower < estimate < upper.",
        f"{name} should satisfy lower < estimate < upper.",
    )


def model_snapshot(model) -> dict[str, float]:
    """Return core simple-regression quantities with stable names."""
    predictor_names = [name for name in model.params.index if name != "Intercept"]
    predictor = predictor_names[0] if predictor_names else model.params.index[-1]
    return {
        "intercept": float(model.params["Intercept"]),
        "slope": float(model.params[predictor]),
        "r_squared": float(model.rsquared),
        "slope_p_value": float(model.pvalues[predictor]),
        "rmse": float((model.resid.pow(2).mean()) ** 0.5),
    }
