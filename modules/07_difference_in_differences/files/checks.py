import math


def _as_float(value):
    try:
        return float(value)
    except Exception:
        return math.nan


def check_close(value, target, tol=1e-3, label="value"):
    value_float = _as_float(value)
    target_float = _as_float(target)
    if not math.isfinite(value_float):
        return f"Recheck: {label} is not numeric yet."
    if abs(value_float - target_float) <= tol:
        return f"Correct: {label} is approximately {target_float:.4g}."
    return f"Recheck: {label} is {value_float:.4g}; expected about {target_float:.4g}."


def check_columns(df, required):
    missing = [col for col in required if col not in df.columns]
    if not missing:
        return "Correct: all required columns are present."
    return "Recheck: missing columns: " + ", ".join(missing)


def check_did_binary(df, did_col="did"):
    values = set(df[did_col].dropna().unique())
    if values.issubset({0, 1}):
        return f"Correct: {did_col} is binary."
    return f"Recheck: {did_col} should contain only 0 and 1."


def check_same_estimate(a, b, tol=1e-6, label="estimate"):
    return check_close(_as_float(a) - _as_float(b), 0.0, tol=tol, label=label + " difference")


def check_pretrend_small(value, threshold=1.0, label="pre-trend coefficient"):
    value_float = _as_float(value)
    if not math.isfinite(value_float):
        return f"Recheck: {label} is not numeric yet."
    if abs(value_float) <= threshold:
        return f"Correct: {label} is small in magnitude."
    return f"Recheck: {label} is not small; discuss this as a warning sign."


def check_sign(value, expected="positive", label="estimate"):
    value_float = _as_float(value)
    if not math.isfinite(value_float):
        return f"Recheck: {label} is not numeric yet."
    if expected == "positive" and value_float > 0:
        return f"Correct: {label} is positive."
    if expected == "negative" and value_float < 0:
        return f"Correct: {label} is negative."
    return f"Recheck: {label} does not have the expected {expected} sign."


def model_snapshot(model):
    return {
        "n": int(model.nobs),
        "df_resid": float(model.df_resid),
        "r_squared": float(model.rsquared),
        "adj_r_squared": float(model.rsquared_adj),
        "f_pvalue": float(model.f_pvalue),
    }
