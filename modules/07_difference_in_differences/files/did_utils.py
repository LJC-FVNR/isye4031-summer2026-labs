import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def did_2x2_table(df, outcome, treated_col="treated", post_col="post"):
    table = (
        df.groupby([treated_col, post_col], as_index=False)[outcome]
        .mean()
        .rename(columns={outcome: "mean_outcome"})
    )
    table["cell"] = table[treated_col].map({0: "control", 1: "treated"}) + "_" + table[post_col].map({0: "pre", 1: "post"})
    return table[[treated_col, post_col, "cell", "mean_outcome"]]


def manual_did(df, outcome, treated_col="treated", post_col="post"):
    means = df.groupby([treated_col, post_col])[outcome].mean()
    treated_change = means.loc[(1, 1)] - means.loc[(1, 0)]
    control_change = means.loc[(0, 1)] - means.loc[(0, 0)]
    return float(treated_change - control_change)


def predicted_values_2x2(model):
    grid = pd.DataFrame(
        {
            "treated": [0, 0, 1, 1],
            "post": [0, 1, 0, 1],
        }
    )
    grid["did"] = grid["treated"] * grid["post"]
    grid["cell"] = grid["treated"].map({0: "control", 1: "treated"}) + "_" + grid["post"].map({0: "pre", 1: "post"})
    grid["predicted"] = model.predict(grid)
    return grid[["treated", "post", "did", "cell", "predicted"]]


def plot_group_trends(df, outcome, time_col, treated_col, title=None):
    trend = (
        df.groupby([time_col, treated_col], as_index=False)[outcome]
        .mean()
        .sort_values([treated_col, time_col])
    )
    fig, ax = plt.subplots()
    for treated_value, part in trend.groupby(treated_col):
        label = "Treated" if int(treated_value) == 1 else "Control"
        ax.plot(part[time_col], part[outcome], marker="o", label=label)
    ax.set_xlabel(time_col)
    ax.set_ylabel(outcome)
    ax.set_title(title or "Group average trends")
    ax.legend()
    return ax


def plot_did_counterfactual(df, outcome, time_col, treated_col="treated", post_col="post", title=None):
    means = (
        df.groupby([time_col, treated_col], as_index=False)[outcome]
        .mean()
        .sort_values([treated_col, time_col])
    )
    fig, ax = plt.subplots()
    styles = {0: {"label": "Control observed", "marker": "o"}, 1: {"label": "Treated observed", "marker": "o"}}
    for treated_value, part in means.groupby(treated_col):
        style = styles.get(int(treated_value), {"label": str(treated_value), "marker": "o"})
        ax.plot(part[time_col], part[outcome], linewidth=2, **style)

    pre_times = sorted(df.loc[df[post_col] == 0, time_col].unique())
    if pre_times:
        reference_time = pre_times[-1]
        control_ref = means.query(f"{time_col} == @reference_time and {treated_col} == 0")[outcome].iloc[0]
        treated_ref = means.query(f"{time_col} == @reference_time and {treated_col} == 1")[outcome].iloc[0]
        counterfactual_rows = []
        for t in sorted(df[time_col].unique()):
            control_t = means.query(f"{time_col} == @t and {treated_col} == 0")[outcome].iloc[0]
            counterfactual_rows.append({time_col: t, "counterfactual": treated_ref + (control_t - control_ref)})
        counterfactual = pd.DataFrame(counterfactual_rows)
        ax.plot(
            counterfactual[time_col],
            counterfactual["counterfactual"],
            linestyle="--",
            linewidth=2,
            marker="s",
            label="Treated counterfactual from control trend",
        )

    post_times = sorted(df.loc[df[post_col] == 1, time_col].unique())
    if post_times:
        ax.axvline(post_times[0], color="gray", linestyle=":", linewidth=1.5, label="Post period starts")
    ax.set_xlabel(time_col)
    ax.set_ylabel(outcome)
    ax.set_title(title or "Observed outcomes and DiD counterfactual")
    ax.legend()
    return ax


def _event_name(k, prefix):
    return f"{prefix}m{abs(int(k))}" if int(k) < 0 else f"{prefix}p{int(k)}"


def make_event_dummies(df, rel_time_col, treated_col, omit=-1, window=(-4, 4), prefix="event_"):
    out = df.copy()
    cols = []
    for k in range(window[0], window[1] + 1):
        if k == omit:
            continue
        name = _event_name(k, prefix)
        out[name] = ((out[rel_time_col] == k) & (out[treated_col] == 1)).astype(int)
        cols.append(name)
    return out, cols


def extract_event_study_results(model, prefix="event_"):
    rows = []
    for name in model.params.index:
        if not name.startswith(prefix):
            continue
        suffix = name[len(prefix):]
        if suffix.startswith("m"):
            relative_time = -int(suffix[1:])
        elif suffix.startswith("p"):
            relative_time = int(suffix[1:])
        else:
            continue
        rows.append(
            {
                "relative_time": relative_time,
                "estimate": float(model.params[name]),
                "std_error": float(model.bse[name]),
            }
        )
    return pd.DataFrame(rows).sort_values("relative_time").reset_index(drop=True)


def plot_event_study(event_df, reference=-1, title=None):
    plot_df = event_df.copy()
    if reference not in set(plot_df["relative_time"]):
        ref = pd.DataFrame({"relative_time": [reference], "estimate": [0.0], "std_error": [0.0]})
        plot_df = pd.concat([plot_df, ref], ignore_index=True)
    plot_df = plot_df.sort_values("relative_time")
    fig, ax = plt.subplots()
    ax.errorbar(
        plot_df["relative_time"],
        plot_df["estimate"],
        yerr=1.96 * plot_df["std_error"],
        marker="o",
        linestyle="-",
        capsize=3,
    )
    ax.axhline(0, color="black", linewidth=1)
    ax.axvline(reference, color="gray", linestyle="--", linewidth=1)
    if 0 in set(plot_df["relative_time"]) and reference != 0:
        ax.axvline(0, color="gray", linestyle=":", linewidth=1)
    ax.set_xlabel("Time relative to treatment")
    ax.set_ylabel("Coefficient relative to period " + str(reference))
    ax.set_title(title or "Event-study estimates")
    return ax
