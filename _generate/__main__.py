"""
@boonhapus, 2024/11/09

At this time, we will not expose the entire EDoc protocol due to privacy concerns in the
internal data format. External applications are allowed to consume only the exposed TML
spec.
"""

from __future__ import annotations

import ast
import datetime as dt
import re
import subprocess as sp

import _clean
import _const


def _subprocess_run(*cmd: str) -> None:
    """Run a shell command, but output to rich console."""
    _const.RICH_CONSOLE.log(f"[green]Running :: [white]{' '.join(cmd)}")

    # fmt: off
    popen_streaming_options = {
        "stdout": sp.PIPE,
        "stderr": sp.STDOUT,
        "text": True,
        "bufsize": 1,
    }
    # fmt: on

    with sp.Popen(cmd, **popen_streaming_options) as proc:  # type: ignore[call-overload]
        assert proc.stdout is not None, "Unexpected output stream"

        for line in iter(proc.stdout.readline, ""):
            _const.RICH_CONSOLE.log(f"[cyan]  {line}")

        _const.RICH_CONSOLE.log()


def _clean_edoc_proto() -> None:
    """
    Sanitize the edoc.proto for external consumption.

    edoc.proto is an internal spec and not all parts can be exposed to customers.

    Additionally, _scriptability.py should be a single file, whereas the edoc spec is
    composed from multiple separate protos.
    """
    # fmt: off
    SCRIPTABILITY_PACKAGE_INFO = (
        'package scriptability;'
        '\noption java_package = "com.thoughtspot.callosum.metadata";'
        '\noption java_outer_classname = "EDoc";'
    )
    # fmt: on

    # READ THE LATEST edoc.proto
    text = _const.LATEST_EDOC_PROTO.read_text(encoding="utf-8")

    # REMOVE ALL COMMENTS
    text = re.sub(r"//.*", _const.VOID, text)
    text = re.sub(r"\/\*\*(?:.|\n)*?\*\/", _const.VOID, text)

    # REMOVE VALIDATION ANNOTATIONS (we won't use these in python).
    text = re.sub(r'^import "common/proto_validation/annotation.proto";$', _const.VOID, text, flags=re.MULTILINE)
    # WHY TWICE? Because some teams have complex validation... :')
    text = re.sub(r"\[\s?\(common.proto_validation\S+\).*?\]", _const.VOID, text, flags=re.MULTILINE | re.DOTALL)
    text = re.sub(r",\s+\(common.proto_validation\S+\).+", _const.VOID, text, flags=re.MULTILINE)

    for preprocessor in _clean.preprocessors:
        # REMOVE THE IMPORT STATEMENT SINCE WE ARE LOCALIZING OR STRIPPING THE PROTO
        text = re.sub(rf'^import "{preprocessor.import_name}";$', _const.VOID, text, flags=re.MULTILINE)

        # STRIP OFF THE PACKAGE IDENTITY (and not following by an underscore, with an optional path separator)
        # fmt: off
        text = re.sub(rf"(?<=\s){preprocessor.package}(?!_)\.?", preprocessor.replace, text, flags=re.MULTILINE | re.DOTALL)  # noqa: E501
        # fmt: on

        # DIVIDE THE edoc.proto INTO 3 PARTS, INJECT THE LOCAL PROTO, STICK IT BACK TOGETHER
        imports, package_info, edoc_contents = text.partition(SCRIPTABILITY_PACKAGE_INFO)
        text = "\n".join([imports, package_info, preprocessor.local, edoc_contents])

    # SAVE BACK TO edoc.proto
    _const.LATEST_EDOC_PROTO.write_text(text, encoding="utf-8")


def _run_protoc() -> None:
    """
    Run protoc, move the output files, then clean up the temporary files.

    Don't have protoc?
      >>> brew install protobuf
    """
    # fmt: off
    _subprocess_run(
        "protoc",
        "--proto_path", _const.LATEST_EDOC_PROTO.parent.as_posix(),
        "--python_betterproto_out", _const.THIS_DIR.as_posix(),
        _const.LATEST_EDOC_PROTO.as_posix(),
    )
    # fmt: on

    # protoc GENERATES AN __init__.py FILE IN THE SCRIPTABILITY PACKAGE (because
    # edoc.proto names its package as scriptability)
    edoc_py = _const.THIS_DIR / "scriptability" / "__init__.py"

    # BUT WE WANT TO RENAME IT TO _scriptability.py INSTEAD
    edoc_py.replace(_const._SCRIPTABILITY_PY)

    # THEN CLEAN UP protoc's WORK
    edoc_py.parent.rmdir()
    edoc_py.parent.with_name("__init__.py").unlink()


def _clean_scriptability_py() -> None:
    """Perform post-processing of the output _scriptability.py file."""
    # READ THE _scriptability.py
    text = _const._SCRIPTABILITY_PY.read_text()

    # SPLIT THE FILE INTO NON-CODE AND CODE PARTS
    warning, plugin, code_as_text = text.partition("# plugin: python-betterproto")

    # RUN THE CODE THROUGH THE POST-PROCESSORS
    code_as_tree = ast.parse(code_as_text, filename=_const._SCRIPTABILITY_PY)

    for postprocessor in _clean.postprocessors:
        postprocessor.visit(code_as_tree)

    code_as_text = ast.unparse(code_as_tree)

    # SAVE BACK TO _scriptability.py
    _const._SCRIPTABILITY_PY.write_text("\n".join([warning + plugin, code_as_text]))

    # FINALLY, ENSURE THE OUTPUT FILE IS LINTED.
    _subprocess_run("ruff", "format", _const._SCRIPTABILITY_PY.as_posix(), "-v")


if __name__ == "__main__":
    if not _const.LATEST_EDOC_PROTO.exists():
        raise FileNotFoundError(f"Could not find edoc.proto in {_const.LATEST_EDOC_PROTO.parent}")

    with _const.RICH_CONSOLE.status("Working..", spinner="smiley"):
        # MAKE A BACKUP.
        backup = _const.LATEST_EDOC_PROTO.with_name(f"edoc.proto.{dt.datetime.now(tz=dt.timezone.utc):%Y%m%d}.backup")
        backup.write_text(_const.LATEST_EDOC_PROTO.read_text(encoding="utf-8"), encoding="utf-8")

        _clean_edoc_proto()
        _run_protoc()
        _clean_scriptability_py()

    _const.RICH_CONSOLE.bell()
