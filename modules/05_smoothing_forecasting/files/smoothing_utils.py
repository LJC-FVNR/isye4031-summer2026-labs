import numpy as np
import pandas as pd
from scipy.optimize import minimize, minimize_scalar
from scipy.stats import norm


def accuracy_measures(actual, fitted):
    actual = np.asarray(actual, dtype=float)
    fitted = np.asarray(fitted, dtype=float)
    mask = np.isfinite(actual) & np.isfinite(fitted)
    actual = actual[mask]
    fitted = fitted[mask]
    errors = actual - fitted
    out = {
        "SSE": float(np.sum(errors ** 2)),
        "MAD": float(np.mean(np.abs(errors))),
        "MSE": float(np.mean(errors ** 2)),
    }
    nonzero = actual != 0
    out["MAPE"] = float(np.mean(np.abs(errors[nonzero] / actual[nonzero])) * 100) if np.any(nonzero) else np.nan
    return out


def initial_level_mean(y, n=None):
    y = np.asarray(y, dtype=float)
    n = max(1, len(y) // 2) if n is None else n
    return float(np.mean(y[:n]))


def initial_line(y, n=None):
    y = np.asarray(y, dtype=float)
    n = len(y) if n is None else n
    t = np.arange(1, n + 1, dtype=float)
    x = np.column_stack([np.ones(n), t])
    intercept, slope = np.linalg.lstsq(x, y[:n], rcond=None)[0]
    return float(intercept), float(slope)


def simple_es(y, alpha, l0=None):
    y = np.asarray(y, dtype=float)
    l0 = initial_level_mean(y) if l0 is None else float(l0)
    level = np.empty(len(y), dtype=float)
    fitted = np.empty(len(y), dtype=float)
    previous_level = l0
    for i, obs in enumerate(y):
        fitted[i] = previous_level
        level[i] = alpha * obs + (1 - alpha) * previous_level
        previous_level = level[i]
    out = pd.DataFrame({"Time": np.arange(1, len(y) + 1), "y": y, "yhat_one_step": fitted, "level": level})
    out["error"] = out["y"] - out["yhat_one_step"]
    out["squared_error"] = out["error"] ** 2
    return out


def optimize_simple_es(y, l0=None):
    y = np.asarray(y, dtype=float)
    l0 = initial_level_mean(y) if l0 is None else float(l0)

    def objective(alpha):
        return accuracy_measures(y, simple_es(y, alpha, l0)["yhat_one_step"])["SSE"]

    res = minimize_scalar(objective, bounds=(0, 1), method="bounded", options={"xatol": 1e-10})
    alpha = float(res.x)
    fit = simple_es(y, alpha, l0)
    return alpha, fit, accuracy_measures(y, fit["yhat_one_step"])


def holt_trend(y, alpha, gamma, l0, b0):
    y = np.asarray(y, dtype=float)
    level = np.empty(len(y), dtype=float)
    trend = np.empty(len(y), dtype=float)
    fitted = np.empty(len(y), dtype=float)
    previous_level = float(l0)
    previous_trend = float(b0)
    for i, obs in enumerate(y):
        fitted[i] = previous_level + previous_trend
        level[i] = alpha * obs + (1 - alpha) * (previous_level + previous_trend)
        trend[i] = gamma * (level[i] - previous_level) + (1 - gamma) * previous_trend
        previous_level = level[i]
        previous_trend = trend[i]
    out = pd.DataFrame({"Time": np.arange(1, len(y) + 1), "y": y, "yhat_one_step": fitted, "level": level, "trend": trend})
    out["error"] = out["y"] - out["yhat_one_step"]
    out["squared_error"] = out["error"] ** 2
    return out


def optimize_holt(y, l0, b0):
    y = np.asarray(y, dtype=float)

    def objective(params):
        alpha, gamma = params
        if alpha < 0 or alpha > 1 or gamma < 0 or gamma > 1:
            return 1e100
        fit = holt_trend(y, alpha, gamma, l0, b0)
        return accuracy_measures(y, fit["yhat_one_step"])["SSE"]

    starts = ([0.2, 0.1], [0.05, 0.0], [0.5, 0.1], [0.2, 0.5], [0.8, 0.2])
    results = [minimize(objective, x0=start, bounds=[(0, 1), (0, 1)], method="L-BFGS-B") for start in starts]
    best = min(results, key=lambda result: result.fun)
    alpha, gamma = [float(v) for v in best.x]
    fit = holt_trend(y, alpha, gamma, l0, b0)
    return alpha, gamma, fit, accuracy_measures(y, fit["yhat_one_step"])


def holt_forecast_table(fit, alpha, gamma, h, level=0.95):
    lT = float(fit["level"].iloc[-1])
    bT = float(fit["trend"].iloc[-1])
    T = len(fit)
    SSE = float(fit["squared_error"].sum())
    s = np.sqrt(SSE / max(T - 2, 1))
    z = norm.ppf(0.5 + level / 2)
    rows = []
    for tau in range(1, h + 1):
        mean = lT + tau * bT
        multiplier = np.sqrt(1 + sum((alpha ** 2) * ((1 + j * gamma) ** 2) for j in range(1, tau)))
        half_width = z * s * multiplier
        rows.append({"tau": tau, "forecast": mean, "lower_95_PI": mean - half_width, "upper_95_PI": mean + half_width})
    return pd.DataFrame(rows)


def _initial_seasonal_factors(y, period, kind="additive"):
    y = np.asarray(y, dtype=float)
    l0, b0 = initial_line(y, len(y))
    t = np.arange(1, len(y) + 1, dtype=float)
    trend_line = l0 + b0 * t
    factors = []
    for season in range(period):
        values = y[season::period]
        trend_values = trend_line[season::period]
        if kind == "additive":
            factors.append(float(np.mean(values - trend_values)))
        else:
            factors.append(float(np.mean(values / trend_values)))
    factors = np.asarray(factors, dtype=float)
    if kind == "additive":
        factors = factors - factors.mean()
    else:
        factors = factors / factors.mean()
    return l0, b0, factors


def holt_winters(y, period, alpha, gamma, delta, kind="additive"):
    y = np.asarray(y, dtype=float)
    l0, b0, seasonal = _initial_seasonal_factors(y, period, kind=kind)
    level = np.empty(len(y), dtype=float)
    trend = np.empty(len(y), dtype=float)
    seasonal_used = np.empty(len(y), dtype=float)
    fitted = np.empty(len(y), dtype=float)
    seasonal = seasonal.copy()
    previous_level = float(l0)
    previous_trend = float(b0)
    for i, obs in enumerate(y):
        season = i % period
        prior_seasonal = float(seasonal[season])
        seasonal_used[i] = prior_seasonal
        if kind == "additive":
            fitted[i] = previous_level + previous_trend + prior_seasonal
            level[i] = alpha * (obs - prior_seasonal) + (1 - alpha) * (previous_level + previous_trend)
            trend[i] = gamma * (level[i] - previous_level) + (1 - gamma) * previous_trend
            seasonal[season] = delta * (obs - level[i]) + (1 - delta) * prior_seasonal
        else:
            fitted[i] = (previous_level + previous_trend) * prior_seasonal
            level[i] = alpha * (obs / prior_seasonal) + (1 - alpha) * (previous_level + previous_trend)
            trend[i] = gamma * (level[i] - previous_level) + (1 - gamma) * previous_trend
            seasonal[season] = delta * (obs / level[i]) + (1 - delta) * prior_seasonal
        previous_level = level[i]
        previous_trend = trend[i]
    out = pd.DataFrame({"Time": np.arange(1, len(y) + 1), "y": y, "yhat_one_step": fitted, "level": level, "trend": trend, "seasonal_factor_used": seasonal_used})
    out["error"] = out["y"] - out["yhat_one_step"]
    out["squared_error"] = out["error"] ** 2
    out.attrs["final_seasonal_factors"] = seasonal
    out.attrs["period"] = period
    out.attrs["kind"] = kind
    return out


def optimize_holt_winters(y, period, kind="additive"):
    y = np.asarray(y, dtype=float)

    def objective(params):
        alpha, gamma, delta = params
        if np.any(np.asarray(params) < 0) or np.any(np.asarray(params) > 1):
            return 1e100
        fit = holt_winters(y, period, alpha, gamma, delta, kind=kind)
        return accuracy_measures(y, fit["yhat_one_step"])["SSE"]

    starts = ([0.2, 0.1, 0.1], [0.4, 0.1, 0.2], [0.1, 0.1, 0.5], [0.6, 0.2, 0.2])
    results = [minimize(objective, x0=start, bounds=[(0, 1), (0, 1), (0, 1)], method="L-BFGS-B") for start in starts]
    best = min(results, key=lambda result: result.fun)
    alpha, gamma, delta = [float(v) for v in best.x]
    fit = holt_winters(y, period, alpha, gamma, delta, kind=kind)
    return alpha, gamma, delta, fit, accuracy_measures(y, fit["yhat_one_step"])


def holt_winters_forecast(fit, h):
    period = int(fit.attrs["period"])
    kind = fit.attrs["kind"]
    lT = float(fit["level"].iloc[-1])
    bT = float(fit["trend"].iloc[-1])
    seasonal = np.asarray(fit.attrs["final_seasonal_factors"], dtype=float)
    rows = []
    for tau in range(1, h + 1):
        season = (len(fit) + tau - 1) % period
        seasonal_factor = seasonal[season]
        base = lT + tau * bT
        forecast = base + seasonal_factor if kind == "additive" else base * seasonal_factor
        rows.append({"tau": tau, "season": season + 1, "forecast": forecast, "seasonal_factor": seasonal_factor})
    return pd.DataFrame(rows)
