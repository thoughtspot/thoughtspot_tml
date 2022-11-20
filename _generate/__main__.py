"""
@boonhapus, 2022/11/18

At this time, we will not expose the entire EDoc protocol due to privacy concerns in the
internal data format. External applications follow a public, approved interface.

If you truly need to understand this package to build a new version, please consult one
of the maintainers of this library.
"""
import subprocess as sp
import pathlib
import re

from rich.console import Console

import _proto_local


console = Console()
HERE = pathlib.Path(__file__).parent
EDOC_PROTO = HERE / "edoc.proto"
EDOC_PY = HERE / "scriptability" / "__init__.py"

PACKAGE_SRC = HERE.parent / "src" / "thoughtspot_tml"
SCRIPTABILITY_PY = PACKAGE_SRC / "_scriptability.py"


def _subprocess_run(*cmd):
    # Run a shell command but output to rich.
    #
    console.log(f"[green]Running :: [white]{' '.join(cmd)}")

    with sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT) as proc:
        for line in proc.stdout:
            console.log(f"  {line.decode().strip()}")

        console.log()


def _clean_edoc_proto():
    # @boonhapus, 2022/11/19
    #
    # This method is idempotent.
    #
    # Building this package is done manually and not all files are included. Some common
    # parts of the EDoc spec are not included as part of the file itself. They're not
    # complicated, so we can add them manually.
    #
    # Additionally, we need to sanitize private parts of the spec.
    #
    text = EDOC_PROTO.read_text()

    # strip all comments except ones starting with `import`
    text = re.sub(r"//(?! import).*", r"", text)

    # replace missing protos with their local representation
    RE_COMMON_PROTO = r'(import "common/common.proto")'

    if re.search(rf"^{RE_COMMON_PROTO}", text, flags=re.M):
        text = re.sub(RE_COMMON_PROTO, r"// \1", text, flags=re.M)
        text = re.sub(r"common\.(?!proto_validation)(.+) ", r"\1", text)
        text += _proto_local.PROTO_COMMON

    # replace missing protos with their local representation
    RE_NUMBER_FORMAT_PROTO = r'(import "protos/number_format.proto")'

    if re.search(rf"^{RE_NUMBER_FORMAT_PROTO}", text, flags=re.M):
        text = re.sub(RE_NUMBER_FORMAT_PROTO, r"// \1", text, flags=re.M)
        text = re.sub(r"blink.numberFormatConfig\.(.+) ", r"\1", text)
        text += _proto_local.PROTO_NUMBER_FORMAT_CONFIG

    # comment out validations import and strip out all their annotations
    text = re.sub(r'^(?!// )(import "common/proto_validation/annotation.proto")', r"// \1", text, flags=re.M)
    text = re.sub(r" \[\(common.proto_validation.Annotation...*\]", r"", text)

    EDOC_PROTO.write_text(text)


def _run_protoc():
    # @boonhapus, 2022/11/19
    #
    # Run protoc and move the output files, then clean up the temporary files.
    #
    # /_generate/scriptability/__init__.py   -->   /src/thoughtspot_tml/_scriptability.py
    #
    _subprocess_run(
        *[
            # fmt: off
            "protoc",
            "-I", HERE.as_posix(),
            "--python_betterproto_out", HERE.as_posix(),
            EDOC_PROTO.as_posix(),
            # fmt: on
        ]
    )

    EDOC_PY.replace(SCRIPTABILITY_PY)
    EDOC_PY.parent.rmdir()
    EDOC_PY.parent.with_name("__init__.py").unlink()


def _clean_scriptability():
    # @boonhapus, 2022/11/19
    #
    # python-betterproto isn't perfect, but 2.0.0 is in beta and we only need it to
    # translate from protobuf -> python.
    #
    # As of right now, betterproto (v2.0.0b5) does not allow optionality.
    #
    some_ridiculous_easter_egg_magic_number = "20120601"

    # reformat the file to have no line-wrapping
    _subprocess_run(
        *[
            # fmt: off
            "black", SCRIPTABILITY_PY.as_posix(),
            "--line-length", some_ridiculous_easter_egg_magic_number,
            # fmt: on
        ]
    )

    text = SCRIPTABILITY_PY.read_text()

    # so our RegEx is simpler, and we can enforce optionality
    text = re.sub(r"((?:string|double|bool|message|int32)_field\(.*)\)", r"\1, optional=True)", text)

    SCRIPTABILITY_PY.write_text(text)


if __name__ == "__main__":
    with console.status("Working..", spinner="smiley"):
        _clean_edoc_proto()
        _run_protoc()
        _clean_scriptability()

    console.bell()
