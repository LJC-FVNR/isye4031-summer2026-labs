# Synthetic Evaluation Data Dictionary

- `evaluation_regression.csv`: simulated continuous response with signal and noise predictors.
- `evaluation_classification.csv`: simulated binary event data with mild class imbalance.
- `evaluation_timeseries.csv`: simulated monthly demand with trend, seasonality,
  and a late level shift. A random split leaks examples from the shifted regime
  into training, whereas a last-period holdout reproduces a real forecast origin.
