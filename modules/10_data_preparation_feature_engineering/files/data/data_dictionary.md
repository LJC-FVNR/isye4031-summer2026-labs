# Synthetic Retail Data Dictionary

These CSV files are synthetic and generated for teaching data preparation; they
do not describe a real retailer.

- `retail_sales_messy.csv`: store-week sales records with intentional missing
  values, one duplicate row, one negative price, one price recorded in cents
  rather than dollars, one extreme units outlier, and one unmatched store key.
- `store_metadata.csv`: store-level attributes used for joins.
- `weather_weekly.csv`: region-week covariates for optional feature engineering.

All monetary fields are intended to be in US dollars. Domain rules used in the
lesson (`price <= 0`, `price > 50`, and `units > 1000`) are teaching assumptions,
not universal cleaning rules.
