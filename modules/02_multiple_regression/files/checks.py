import math

def check_close(value, target, tol=1e-3, label="value"):
    if not math.isfinite(float(value)):
        return f"{label} is not finite yet."
    if abs(float(value) - float(target)) <= tol:
        return f"Correct: {label} is approximately {target:.4g}."
    return f"{label} is {value:.4g}; check the model, data columns, or formula."

def check_interval_order(lower, center, upper, label="interval"):
    if lower <= center <= upper:
        return f"Correct: {label} contains the estimate in the expected order."
    return f"Recheck {label}: the lower bound should be <= estimate <= upper bound."

def check_positive(value, label="value"):
    if value > 0:
        return f"Correct: {label} is positive."
    return f"Recheck {label}; it should be positive for this model quantity."

def model_snapshot(model):
    return {
        "n": int(model.nobs),
        "df_resid": float(model.df_resid),
        "r_squared": float(model.rsquared),
        "adj_r_squared": float(model.rsquared_adj),
        "f_pvalue": float(model.f_pvalue),
    }
