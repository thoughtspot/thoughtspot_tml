import pathlib
import shutil
import os

import nox


ON_GITHUB = "GITHUB_ACTIONS" in os.environ
PY_VERSIONS = ["3.7", "3.8", "3.9", "3.10", "3.11"]


@nox.session(python=PY_VERSIONS, reuse_venv=not ON_GITHUB)
def tests(session: nox.Session) -> None:
    """
    Ensure we test our code.
    """
    session.install("-e", ".[dev]")
    session.run("ward", "test", "--test-output-style=dots-global", "--order=standard")


@nox.session(reuse_venv=not ON_GITHUB)
def black(session: nox.Session) -> None:
    """
    Lint.
    """
    session.run("black", ".", "--config", "pyproject.toml")


@nox.session(reuse_venv=not ON_GITHUB)
def mypy(session: nox.Session) -> None:
    """
    Lint.
    """
    session.run("mypy", "./src/thoughtspot_tml")
    # session.run("mypy", "--install-types")


@nox.session(reuse_venv=not ON_GITHUB)
def build(session: nox.Session) -> None:
    """
    Deploy.
    """
    package_dir = pathlib.Path(__package__).resolve()

    session.run("python", package_dir.joinpath("setup.py").as_posix(), "sdist", "bdist_wheel")
    # session.run("twine", "upload", "-r", "pypi", package_dir.joinpath("build").as_posix())

    shutil.rmtree(package_dir / "build")
    shutil.rmtree(package_dir / "dist")
