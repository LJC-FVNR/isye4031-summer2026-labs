import math


def check_close(value, target, tol=1e-3, label="value"):
    if not math.isfinite(float(value)):
        return f"{label} is not finite yet."
    if abs(float(value) - float(target)) <= tol:
        return f"Correct: {label} is approximately {target:.4g}."
    return f"{label} is {float(value):.4g}; check the model, data columns, or formula."


def check_columns(frame, expected):
    missing = [col for col in expected if col not in frame.columns]
    if not missing:
        return "Correct: all required columns are present."
    return "Missing columns: " + ", ".join(missing)


def check_interval_width(conf_low, conf_high, pred_low, pred_high):
    ci_width = conf_high - conf_low
    pi_width = pred_high - pred_low
    if pi_width > ci_width > 0:
        return "Correct: the prediction interval is wider than the confidence interval."
    return "Recheck the intervals: the prediction interval should be wider."


def check_positive(value, label="value"):
    if float(value) > 0:
        return f"Correct: {label} is positive."
    return f"Recheck {label}; it should be positive."


def check_nonempty(items, label="selection"):
    if len(items) > 0:
        return f"Correct: {label} contains at least one item."
    return f"Recheck {label}; it is empty."


def model_snapshot(model):
    return {
        "n": int(model.nobs),
        "df_resid": float(model.df_resid),
        "r_squared": float(model.rsquared),
        "adj_r_squared": float(model.rsquared_adj),
        "f_pvalue": float(model.f_pvalue) if model.f_pvalue == model.f_pvalue else None,
    }
