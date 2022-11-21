def _get_version() -> str:
    """
    Retrieve the version string.
    """
    import pathlib
    import re

    project_dir = pathlib.Path(__file__).parent.parent.parent
    pyproject_toml = (project_dir / "pyproject.toml").read_text()
    version = re.search(r"version = .(.*).", pyproject_toml, flags=re.M).group(1)
    return version


__version__ = _get_version()
