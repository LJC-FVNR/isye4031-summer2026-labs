# ISYE 4031 Summer 2026 Python Labs

This repository hosts browser-runnable Python lab modules for ISYE 4031.

## Student Links

- [01 Regression Foundations](https://ljc-fvnr.github.io/isye4031-summer2026-labs/modules/01_regression_foundations/lab/index.html?path=00_START_HERE.ipynb)

## Local Preview

Build the site:

```powershell
python -m pip install -r modules/01_regression_foundations/requirements-lite-build.txt
jupyter lite build --lite-dir modules/01_regression_foundations --output-dir public/modules/01_regression_foundations
```

Serve it locally:

```powershell
python -m http.server 8899 -d public
```

Then open:

```text
http://127.0.0.1:8899/modules/01_regression_foundations/lab/index.html?path=00_START_HERE.ipynb
```

