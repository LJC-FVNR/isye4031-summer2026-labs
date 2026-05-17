
# Utility functions for ISYE 4031 Box-Jenkins notebooks.

from __future__ import annotations

import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.stats.diagnostic import acorr_ljungbox


def first_difference(series):
    s = pd.Series(series).astype(float)
    return s.diff().dropna().reset_index(drop=True)


def second_difference(series):
    s = pd.Series(series).astype(float)
    return s.diff().diff().dropna().reset_index(drop=True)


def seasonal_difference(series, lag):
    s = pd.Series(series).astype(float)
    return s.diff(lag).dropna().reset_index(drop=True)


def regular_then_seasonal_difference(series, seasonal_lag):
    return seasonal_difference(first_difference(series), seasonal_lag)


def acf_pacf_table(series, nlags=12):
    s = pd.Series(series).astype(float).dropna()
    nlags = min(nlags, max(1, len(s) // 2 - 1))
    acf_vals = acf(s, nlags=nlags, fft=False)
    pacf_vals = pacf(s, nlags=nlags, method="ywmle")
    n = len(s)
    acf_se = np.empty(nlags + 1, dtype=float)
    acf_se[0] = np.nan
    for k in range(1, nlags + 1):
        # Bartlett-style standard error used in the lecture notes:
        # se(r_k) = sqrt(1 + 2 * sum_{j=1}^{k-1} r_j^2) / sqrt(N).
        acf_se[k] = np.sqrt(1 + 2 * np.sum(acf_vals[1:k] ** 2)) / np.sqrt(n)
    pacf_se = np.repeat(1 / np.sqrt(n), nlags + 1)
    pacf_se[0] = np.nan
    acf_t = acf_vals / acf_se
    pacf_t = pacf_vals / pacf_se
    acf_sig = np.abs(acf_t) > 2
    pacf_sig = np.abs(pacf_t) > 2
    acf_sig[0] = False
    pacf_sig[0] = False
    return pd.DataFrame({
        "lag": np.arange(nlags + 1),
        "ACF": acf_vals,
        "ACF_se": acf_se,
        "ACF_t": acf_t,
        "PACF": pacf_vals,
        "PACF_se": pacf_se,
        "PACF_t": pacf_t,
        "approx_significant_ACF": acf_sig,
        "approx_significant_PACF": pacf_sig,
    })


def mean_zero_t_test(series):
    s = pd.Series(series).astype(float).dropna()
    n = len(s)
    mean = float(s.mean())
    sd = float(s.std(ddof=1))
    se = sd / np.sqrt(n)
    t_value = mean / se if se > 0 else np.nan
    p_value = 2 * stats.t.sf(abs(t_value), df=n - 1) if n > 1 and se > 0 else np.nan
    return pd.Series({"n": n, "mean": mean, "sd": sd, "se": se, "t": t_value, "p_value": p_value})


def fit_arima(series, order, trend="n"):
    s = pd.Series(series).astype(float).dropna()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = ARIMA(s, order=order, trend=trend).fit()
    return result


def fit_sarima(series, order, seasonal_order, trend="n"):
    s = pd.Series(series).astype(float).dropna()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = SARIMAX(
            s,
            order=order,
            seasonal_order=seasonal_order,
            trend=trend,
            enforce_stationarity=False,
            enforce_invertibility=False,
        ).fit(disp=False, maxiter=100)
    return result


def parameter_table(result):
    params = result.params
    bse = result.bse
    zvalues = params / bse
    pvalues = 2 * stats.norm.sf(np.abs(zvalues))
    return pd.DataFrame({
        "estimate": params,
        "std_error": bse,
        "z_or_t": zvalues,
        "p_value": pvalues,
    })


def forecast_table(result, steps=6, alpha=0.05):
    fc = result.get_forecast(steps=steps)
    out = pd.DataFrame({"forecast": fc.predicted_mean})
    ci = pd.DataFrame(fc.conf_int(alpha=alpha))
    if ci.shape[1] >= 2:
        out["lower"] = ci.iloc[:, 0].to_numpy()
        out["upper"] = ci.iloc[:, 1].to_numpy()
    out.index = np.arange(1, steps + 1)
    out.index.name = "step"
    return out


def ljung_box_table(residuals, lags=(6, 12, 18)):
    r = pd.Series(residuals).astype(float).dropna()
    valid_lags = [lag for lag in lags if lag < len(r)]
    if not valid_lags:
        valid_lags = [min(5, len(r) - 1)]
    return acorr_ljungbox(r, lags=valid_lags, return_df=True)


def arima_grid_search(series, p_values=(0, 1, 2), d_values=(0, 1), q_values=(0, 1, 2), trend_options=("n",), max_results=10):
    rows = []
    for p in p_values:
        for d in d_values:
            for q in q_values:
                for trend in trend_options:
                    if d > 0 and trend == "c":
                        continue
                    try:
                        result = fit_arima(series, order=(p, d, q), trend=trend)
                        rows.append({
                            "order": (p, d, q),
                            "trend": trend,
                            "aic": result.aic,
                            "bic": result.bic,
                            "converged": bool(result.mle_retvals.get("converged", True)),
                        })
                    except Exception:
                        continue
    table = pd.DataFrame(rows)
    if table.empty:
        return table
    return table.sort_values("aic").head(max_results).reset_index(drop=True)


def plot_series(series, x=None, title="Time series", ylabel="value", ax=None, marker="o"):
    s = pd.Series(series).astype(float)
    if x is None:
        x = np.arange(1, len(s) + 1)
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, s, marker=marker)
    ax.set_title(title)
    ax.set_xlabel("time")
    ax.set_ylabel(ylabel)
    return ax


def plot_acf_pacf_pair(series, lags=24, title="Series"):
    s = pd.Series(series).astype(float).dropna()
    lags = min(lags, max(1, len(s) // 2 - 1))
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    plot_acf(s, lags=lags, ax=axes[0], title=f"ACF: {title}")
    plot_pacf(s, lags=lags, ax=axes[1], title=f"PACF: {title}", method="ywmle")
    plt.tight_layout()
    return fig, axes


def plot_forecast(original, result, steps=6, title="Forecast", ylabel="value"):
    y = pd.Series(original).astype(float).reset_index(drop=True)
    fc = forecast_table(result, steps=steps)
    history_x = np.arange(1, len(y) + 1)
    forecast_x = np.arange(len(y) + 1, len(y) + steps + 1)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(history_x, y, marker="o", label="Observed")
    ax.plot(forecast_x, fc["forecast"], marker="o", label="Forecast")
    if {"lower", "upper"}.issubset(fc.columns):
        ax.fill_between(forecast_x, fc["lower"].to_numpy(), fc["upper"].to_numpy(), alpha=0.2, label="95% interval")
    ax.set_title(title)
    ax.set_xlabel("time")
    ax.set_ylabel(ylabel)
    ax.legend()
    plt.tight_layout()
    return fig, ax
