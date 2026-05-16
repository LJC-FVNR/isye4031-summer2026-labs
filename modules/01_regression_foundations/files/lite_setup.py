PACKAGES = ["numpy", "pandas", "matplotlib", "scipy", "statsmodels"]


async def ensure_packages():
    """Load the scientific Python packages used by this module in JupyterLite."""
    try:
        import piplite
    except ModuleNotFoundError:
        try:
            import micropip
        except ModuleNotFoundError:
            print("Using the current Python environment.")
            return
        await micropip.install(PACKAGES)
    else:
        await piplite.install(PACKAGES)

    print("Scientific Python packages are ready.")
