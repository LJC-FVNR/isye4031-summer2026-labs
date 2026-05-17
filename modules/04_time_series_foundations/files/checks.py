def check_columns(df, expected):
    missing = [col for col in expected if col not in df.columns]
    if missing:
        raise ValueError("Missing expected columns: " + ", ".join(missing))
    return "Ready: found " + ", ".join(expected)


def check_no_missing(df, columns=None):
    columns = list(df.columns) if columns is None else columns
    counts = df[columns].isna().sum()
    bad = counts[counts > 0]
    if len(bad):
        raise ValueError("Missing values detected: " + bad.to_dict().__repr__())
    return "Ready: no missing values in selected columns"
