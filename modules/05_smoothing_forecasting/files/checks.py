def check_between(value, low, high, label="value"):
    if low <= value <= high:
        return f"OK: {label} = {value:.4g} is between {low} and {high}."
    return f"Check this: {label} = {value:.4g} is outside [{low}, {high}]."


def check_close(value, target, tol=1e-6, label="value"):
    if abs(value - target) <= tol:
        return f"OK: {label} is close to {target}."
    return f"Check this: {label} = {value:.6g}, expected about {target:.6g}."


def check_columns(frame, columns):
    missing = [column for column in columns if column not in frame.columns]
    if not missing:
        return "OK: required columns are present."
    return "Missing columns: " + ", ".join(missing)
