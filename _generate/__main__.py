"""
@boonhapus, 2022/11/18

At this time, we will not expose the entire EDoc protocol due to privacy concerns in the
internal data format. External applications follow a public, approved interface.

If you truly need to understand this package to build a new version, please consult one
of the maintainers of this library.
"""
import subprocess as sp
import pathlib
import ast
import re

from rich.console import Console

import _proto_local


console = Console()
HERE = pathlib.Path(__file__).parent
EDOC_PROTO = HERE / "edoc.proto"
EDOC_IMPORTS = """
package scriptability;
option java_package = "com.thoughtspot.callosum.metadata";
option java_outer_classname = "EDoc";
"""
EDOC_PY = HERE / "scriptability" / "__init__.py"

PACKAGE_SRC = HERE.parent / "src" / "thoughtspot_tml"
SCRIPTABILITY_PY = PACKAGE_SRC / "_scriptability.py"


def _subprocess_run(*cmd):
    # Run a shell command but output to rich.
    #
    console.log(f"[green]Running :: [white]{' '.join(cmd)}")

    with sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT) as proc:
        for line in proc.stdout:
            console.log(f"[cyan]  {line.decode().strip()}")

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
    localized_import_info = [
        {
            "regex_import": "a3/monitor/public/monitor_rule.proto",
            "regex_package": r"a3.metric_monitor\.",
            "localized_cleansed": _proto_local.PROTO_MONITOR_SUPPLEMENTAL,
        },
        {
            "regex_import": "atlas/public/metadata.proto",
            "regex_package": r"atlas\.",
            "localized_cleansed": _proto_local.PROTO_ATLAS_ACTION_CONTEXT,
        },
        {
            "regex_import": "common/common.proto",
            "regex_package": r"common\.(?!proto_validation)",
            "localized_cleansed": _proto_local.PROTO_COMMON,
        },
        {
            "regex_import": "protos/number_format.proto",
            "regex_package": r"blink.numberFormatConfig\.",
            "localized_cleansed": _proto_local.PROTO_NUMBER_FORMAT_CONFIG,
        },
    ]

    for localized_import in localized_import_info:
        re_import_statement = rf"""(import "{localized_import['regex_import']}")"""

        if re.search(re_import_statement, text, flags=re.M):
            text = re.sub(re_import_statement, r"// \1", text, flags=re.M)
            text = re.sub(rf"{localized_import['regex_package']}(.+)", r"\1", text)
            imports, package, rest = text.partition(EDOC_IMPORTS)
            text = "\n".join([imports, package, localized_import["localized_cleansed"], rest])

    # comment out validations import and strip out all their annotations
    text = re.sub(r'(import "common/proto_validation/annotation.proto";)', r"// \1", text, flags=re.M)
    text = re.sub(r" \[\s*?\(common.proto_validation.(.|\n)*?\]", r"", text, flags=re.M)

    EDOC_PROTO.write_text(text)


def _run_protoc():
    # @boonhapus, 2022/11/19
    #
    # Run protoc and move the output files, then clean up the temporary files.
    #
    # /_generate/scriptability/__init__.py   -->   /src/thoughtspot_tml/_scriptability.py
    #
    # Don't have protoc?
    #   >>> brew install protobuf
    #
    _subprocess_run(
        # fmt: off
        "protoc",
        "-I", HERE.as_posix(),
        "--python_betterproto_out", HERE.as_posix(),
        EDOC_PROTO.as_posix(),
        # fmt: on
    )

    EDOC_PY.replace(SCRIPTABILITY_PY)
    EDOC_PY.parent.rmdir()
    EDOC_PY.parent.with_name("__init__.py").unlink()


def _clean_scriptability():  # noqa: C901
    # @boonhapus, 2022/11/19
    #
    # python-betterproto isn't perfect, but 2.0.0 is in beta and we only need it to
    # translate from protobuf -> python.
    #
    # As of right now, betterproto (v2.0.0b5) does not allow optionality.
    #
    class ThoughtSpotVisitor(ast.NodeVisitor):
        # RULES:
        # - rewrite Format.*Config dataclasses to have camelCase attributes
        # - rewrite plot_as_band to be a camelCase attribute again

        @staticmethod
        def snake_to_camel(snake_case: str) -> str:
            components = snake_case.split("_")
            # We capitalize the first letter of each component except the first one
            # with the 'title' method and join them together.
            return components[0] + "".join(x.title() for x in components[1:])

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            if "dataclass" in [deco.func.id for deco in node.decorator_list]:
                for attribute in node.body:
                    # if it's a Foramt.*Config, camelize its name
                    if node.name.startswith("Format") and node.name.endswith("Config"):
                        attribute.target.id = self.snake_to_camel(attribute.target.id)

                    if isinstance(attribute, ast.AnnAssign) and attribute.target.id == "plot_as_band":
                        attribute.target.id = self.snake_to_camel(attribute.target.id)

            self.generic_visit(node)

    class BetterProtoVisitor(ast.NodeVisitor):
        OPTIONAL_FIELDS = (
            "string_field",
            "double_field",
            "bool_field",
            "message_field",
            "int32_field",
            "enum_field",
        )
        KW_OPTIONAL = ast.keyword(arg="optional", value=ast.Constant(True))  # optional=True

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            if "dataclass" in [deco.func.id for deco in node.decorator_list]:
                attrs = []
                rest = []

                for attribute in node.body:
                    if isinstance(attribute, ast.AnnAssign):
                        attrs.append(attribute)

                        if attribute.value.func.attr in self.OPTIONAL_FIELDS:
                            attribute.value.keywords.append(self.KW_OPTIONAL)
                    else:
                        rest.append(attribute)

                # sort body so that all fields are numerically ordered
                node.body = [*sorted(attrs, key=lambda e: e.value.args[0].value), *rest]

            self.generic_visit(node)

    text = SCRIPTABILITY_PY.read_text()
    warning, plugin, code = text.partition("# plugin: python-betterproto")
    tree = ast.parse(code, filename=SCRIPTABILITY_PY)
    ThoughtSpotVisitor().visit(tree)
    BetterProtoVisitor().visit(tree)
    text = ast.unparse(tree)

    SCRIPTABILITY_PY.write_text("\n".join([warning + plugin, text]))
    _subprocess_run("black", SCRIPTABILITY_PY.as_posix(), "-v")


if __name__ == "__main__":
    import sys

    if sys.version_info < (3, 8):
        raise RuntimeError("The ThoughtSpot TML SDK must be generated from py38 or greater.")

    with console.status("Working..", spinner="smiley"):
        _clean_edoc_proto()
        _run_protoc()
        _clean_scriptability()

    console.bell()
