# ISYE 4031 Summer 2026 Python Labs

This repository hosts browser-runnable Python lab modules for ISYE 4031.

Students can work in the browser and export both the completed `.ipynb` notebook and a PDF report from JupyterLite.

## Student Links

- [00 Student Onboarding](https://ljc-fvnr.github.io/isye4031-summer2026-labs/modules/00_student_onboarding/lab/index.html?path=00_START_HERE.ipynb)
- [01 Regression Foundations](https://ljc-fvnr.github.io/isye4031-summer2026-labs/modules/01_regression_foundations/lab/index.html?path=00_START_HERE.ipynb)
- [02 Multiple Regression](https://ljc-fvnr.github.io/isye4031-summer2026-labs/modules/02_multiple_regression/lab/index.html?path=00_START_HERE.ipynb)
- [03 Diagnostics and Variable Selection](https://ljc-fvnr.github.io/isye4031-summer2026-labs/modules/03_diagnostics_variable_selection/lab/index.html?path=00_START_HERE.ipynb)
- [04 Time Series Foundations](https://ljc-fvnr.github.io/isye4031-summer2026-labs/modules/04_time_series_foundations/lab/index.html?path=00_START_HERE.ipynb)
- [05 Smoothing and Forecasting](https://ljc-fvnr.github.io/isye4031-summer2026-labs/modules/05_smoothing_forecasting/lab/index.html?path=00_START_HERE.ipynb)
- [06 Box-Jenkins ARIMA](https://ljc-fvnr.github.io/isye4031-summer2026-labs/modules/06_box_jenkins/lab/index.html?path=00_START_HERE.ipynb)
- [07 Difference-in-Differences](https://ljc-fvnr.github.io/isye4031-summer2026-labs/modules/07_difference_in_differences/lab/index.html?path=00_START_HERE.ipynb)
- [10 Data Preparation and Feature Engineering](https://ljc-fvnr.github.io/isye4031-summer2026-labs/modules/10_data_preparation_feature_engineering/lab/index.html?path=00_START_HERE.ipynb)
- [11 Model Selection and Evaluation](https://ljc-fvnr.github.io/isye4031-summer2026-labs/modules/11_model_selection_evaluation/lab/index.html?path=00_START_HERE.ipynb)
- [12 Logistic Regression and Classification](https://ljc-fvnr.github.io/isye4031-summer2026-labs/modules/12_logistic_regression_classification/lab/index.html?path=00_START_HERE.ipynb)
- [13 Shrinkage Methods: Ridge and LASSO](https://ljc-fvnr.github.io/isye4031-summer2026-labs/modules/13_shrinkage_ridge_lasso/lab/index.html?path=00_START_HERE.ipynb)
- [14 PCA, KNN, and K-means](https://ljc-fvnr.github.io/isye4031-summer2026-labs/modules/14_pca_knn_kmeans/lab/index.html?path=00_START_HERE.ipynb)
- [15 Project Methods Clinic](https://ljc-fvnr.github.io/isye4031-summer2026-labs/modules/15_project_methods_clinic/lab/index.html?path=00_START_HERE.ipynb)

## Local Preview

Build the site:

```powershell
python -m pip install -r modules/00_student_onboarding/requirements-lite-build.txt
python -m pip install -r modules/01_regression_foundations/requirements-lite-build.txt
python -m pip install -r modules/02_multiple_regression/requirements-lite-build.txt
python -m pip install -r modules/03_diagnostics_variable_selection/requirements-lite-build.txt
python -m pip install -r modules/04_time_series_foundations/requirements-lite-build.txt
python -m pip install -r modules/05_smoothing_forecasting/requirements-lite-build.txt
python -m pip install -r modules/06_box_jenkins/requirements-lite-build.txt
python -m pip install -r modules/07_difference_in_differences/requirements-lite-build.txt
python -m pip install -r modules/10_data_preparation_feature_engineering/requirements-lite-build.txt
python -m pip install -r modules/11_model_selection_evaluation/requirements-lite-build.txt
python -m pip install -r modules/12_logistic_regression_classification/requirements-lite-build.txt
python -m pip install -r modules/13_shrinkage_ridge_lasso/requirements-lite-build.txt
python -m pip install -r modules/14_pca_knn_kmeans/requirements-lite-build.txt
python -m pip install -r modules/15_project_methods_clinic/requirements-lite-build.txt
jupyter lite build --lite-dir modules/00_student_onboarding --output-dir public/modules/00_student_onboarding
jupyter lite build --lite-dir modules/01_regression_foundations --output-dir public/modules/01_regression_foundations
jupyter lite build --lite-dir modules/02_multiple_regression --output-dir public/modules/02_multiple_regression
jupyter lite build --lite-dir modules/03_diagnostics_variable_selection --output-dir public/modules/03_diagnostics_variable_selection
jupyter lite build --lite-dir modules/04_time_series_foundations --output-dir public/modules/04_time_series_foundations
jupyter lite build --lite-dir modules/05_smoothing_forecasting --output-dir public/modules/05_smoothing_forecasting
jupyter lite build --lite-dir modules/06_box_jenkins --output-dir public/modules/06_box_jenkins
jupyter lite build --lite-dir modules/07_difference_in_differences --output-dir public/modules/07_difference_in_differences
jupyter lite build --lite-dir modules/10_data_preparation_feature_engineering --output-dir public/modules/10_data_preparation_feature_engineering
jupyter lite build --lite-dir modules/11_model_selection_evaluation --output-dir public/modules/11_model_selection_evaluation
jupyter lite build --lite-dir modules/12_logistic_regression_classification --output-dir public/modules/12_logistic_regression_classification
jupyter lite build --lite-dir modules/13_shrinkage_ridge_lasso --output-dir public/modules/13_shrinkage_ridge_lasso
jupyter lite build --lite-dir modules/14_pca_knn_kmeans --output-dir public/modules/14_pca_knn_kmeans
jupyter lite build --lite-dir modules/15_project_methods_clinic --output-dir public/modules/15_project_methods_clinic
```

Serve it locally:

```powershell
python -m http.server 8899 -d public
```

Then open:

```text
http://127.0.0.1:8899/modules/00_student_onboarding/lab/index.html?path=00_START_HERE.ipynb
http://127.0.0.1:8899/modules/01_regression_foundations/lab/index.html?path=00_START_HERE.ipynb
http://127.0.0.1:8899/modules/02_multiple_regression/lab/index.html?path=00_START_HERE.ipynb
http://127.0.0.1:8899/modules/03_diagnostics_variable_selection/lab/index.html?path=00_START_HERE.ipynb
http://127.0.0.1:8899/modules/04_time_series_foundations/lab/index.html?path=00_START_HERE.ipynb
http://127.0.0.1:8899/modules/05_smoothing_forecasting/lab/index.html?path=00_START_HERE.ipynb
http://127.0.0.1:8899/modules/06_box_jenkins/lab/index.html?path=00_START_HERE.ipynb
http://127.0.0.1:8899/modules/07_difference_in_differences/lab/index.html?path=00_START_HERE.ipynb
http://127.0.0.1:8899/modules/10_data_preparation_feature_engineering/lab/index.html?path=00_START_HERE.ipynb
http://127.0.0.1:8899/modules/11_model_selection_evaluation/lab/index.html?path=00_START_HERE.ipynb
http://127.0.0.1:8899/modules/12_logistic_regression_classification/lab/index.html?path=00_START_HERE.ipynb
http://127.0.0.1:8899/modules/13_shrinkage_ridge_lasso/lab/index.html?path=00_START_HERE.ipynb
http://127.0.0.1:8899/modules/14_pca_knn_kmeans/lab/index.html?path=00_START_HERE.ipynb
http://127.0.0.1:8899/modules/15_project_methods_clinic/lab/index.html?path=00_START_HERE.ipynb
```
