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
