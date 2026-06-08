# Shared setup helper for the ISYE 4031 JupyterLite notebooks.
# Run `await ensure_packages()` before importing the scientific Python stack.

PACKAGES = ["numpy", "pandas", "matplotlib", "scipy", "statsmodels"]

async def ensure_packages(packages=PACKAGES):
    try:
        import micropip
    except ImportError:
        print("Running outside JupyterLite; assuming packages are already installed.")
        return
    installed = []
    for package in packages:
        try:
            await micropip.install(package)
            installed.append(package)
        except Exception as exc:
            print(f"Could not install {package}: {exc}")
            raise
    print("Ready: " + ", ".join(installed))
