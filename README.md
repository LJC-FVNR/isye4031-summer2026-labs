# ISYE 4031 Summer 2026 Python Labs

This repository hosts browser-runnable Python lab modules for ISYE 4031.

Students can work in the browser and export both the completed `.ipynb` notebook and a PDF report from JupyterLite.

## Student Links

- [01 Regression Foundations](https://ljc-fvnr.github.io/isye4031-summer2026-labs/modules/01_regression_foundations/lab/index.html?path=00_START_HERE.ipynb)
- [02 Multiple Regression](https://ljc-fvnr.github.io/isye4031-summer2026-labs/modules/02_multiple_regression/lab/index.html?path=00_START_HERE.ipynb)
- [03 Diagnostics and Variable Selection](https://ljc-fvnr.github.io/isye4031-summer2026-labs/modules/03_diagnostics_variable_selection/lab/index.html?path=00_START_HERE.ipynb)

## Local Preview

Build the site:

```powershell
python -m pip install -r modules/01_regression_foundations/requirements-lite-build.txt
python -m pip install -r modules/02_multiple_regression/requirements-lite-build.txt
python -m pip install -r modules/03_diagnostics_variable_selection/requirements-lite-build.txt
jupyter lite build --lite-dir modules/01_regression_foundations --output-dir public/modules/01_regression_foundations
jupyter lite build --lite-dir modules/02_multiple_regression --output-dir public/modules/02_multiple_regression
jupyter lite build --lite-dir modules/03_diagnostics_variable_selection --output-dir public/modules/03_diagnostics_variable_selection
```

Serve it locally:

```powershell
python -m http.server 8899 -d public
```

Then open:

```text
http://127.0.0.1:8899/modules/01_regression_foundations/lab/index.html?path=00_START_HERE.ipynb
http://127.0.0.1:8899/modules/02_multiple_regression/lab/index.html?path=00_START_HERE.ipynb
http://127.0.0.1:8899/modules/03_diagnostics_variable_selection/lab/index.html?path=00_START_HERE.ipynb
```
