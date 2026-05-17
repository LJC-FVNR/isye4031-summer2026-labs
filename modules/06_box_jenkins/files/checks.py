# Small, non-intrusive checks for numerical notebook work.

import math

def check(condition, pass_message="PASS", fail_message="Check the preceding calculation."):
    return pass_message if bool(condition) else fail_message

def check_close(value, expected, tol=1e-6, label="value"):
    if value is None:
        return f"Check {label}: value is missing."
    if math.isfinite(float(value)) and abs(float(value) - expected) <= tol:
        return f"PASS: {label} is close to {expected}."
    return f"Check {label}: got {value}, expected about {expected}."

def check_between(value, low, high, label="value"):
    if low <= float(value) <= high:
        return f"PASS: {label} is between {low} and {high}."
    return f"Check {label}: got {value}, expected between {low} and {high}."

def check_columns(frame, expected):
    missing = [col for col in expected if col not in frame.columns]
    if not missing:
        return "PASS: expected columns are present."
    return "Missing columns: " + ", ".join(missing)
