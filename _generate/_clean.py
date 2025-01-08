from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import ast

import _const
import _proto_local

# =====================================================
# PRE-PROCESSORS  (edits the source .proto files)
# =====================================================


@dataclass
class ProtobufPreprocessor:
    """All preprocessor text are raw strings passed to a regex.sub method."""

    # Relative path of the proto spec to import, including extension.
    import_name: str

    # Package name of the imported proto spec.
    package: str

    # If we are localizing a proto, what to replace the package name with.
    replace: str = _const.VOID

    # Local representation of the proto spec.
    local: str = _const.VOID


preprocessors = [
    # DEVNOTE: @boonhapus, 2024/11/09
    # THIS IS IN A PRIORITY ORDER
    ProtobufPreprocessor(
        import_name=r"a3/monitor/public/monitor_rule.proto",
        package=r"a3.metric_monitor",
        local=_proto_local.PROTO_KPI_MONITOR,
    ),
    ProtobufPreprocessor(
        import_name=r"atlas/public/metadata.proto",
        package=r"atlas",
        local=_proto_local.PROTO_ATLAS,
    ),
    ProtobufPreprocessor(
        import_name=r"common/common.proto",
        package=r"common(?!.proto_validation)",
        local=_proto_local.PROTO_COMMON,
    ),
    ProtobufPreprocessor(
        import_name=r"protos/number_format.proto",
        package=r"blink.numberFormatConfig",
        local=_proto_local.PROTO_NUMBER_FORMAT_CONFIG,
    ),
    ProtobufPreprocessor(
        import_name=r"sage/public/common.proto",
        package=r"sage",
        local=_proto_local.PROTO_SAGE,
    ),
    ProtobufPreprocessor(
        import_name="callosum/public/cohort.proto",
        package=r"callosum",
        local=_proto_local.PROTO_CALLOSUM_COHORT,
    ),
    ProtobufPreprocessor(
        import_name="callosum/public/metadata/answer_spec.proto",
        package=r"entitylib",
        local=_proto_local.PROTO_CALLOSUM_ANSWER_SPEC,
    ),
    ProtobufPreprocessor(
        import_name="datamanager/public/query_triggers.proto",
        package=r"datamanager",
        local=_proto_local.PROTO_DATAMANAGER_QUERY_TRIGGERS,
    ),
]

# =====================================================
# POST-PROCESSORS (edits the resulting .py files)
# =====================================================


# class ThoughtSpotLintingFormatter(ast.NodeVisitor):
class ThoughtSpotLintingFormatter(ast.NodeTransformer):
    # NOTE: @boonhapus, 2024/11/09
    # INTERNAL PROTOS HAVE LINTING STANDARDS, BUT SOME TEAMS VIOLATE THEM.
    # SEE THE CLASS DEFINITION VISITOR BELOW FOR THE SET OF OVERRIDES.

    @staticmethod
    def snake_to_camel(snake_case: str) -> str:
        """Convert the text to camelCase."""
        return "".join(word if not i else word.title() for i, word in enumerate(snake_case.split("_")))

    @staticmethod
    def is_dataclass(node: ast.ClassDef) -> bool:
        """Determine if the class is a dataclass."""
        for deco in node.decorator_list:
            # @dataclass
            if isinstance(deco, ast.Name) and deco.id == "dataclass":
                return True

            # @dataclass(...)
            if isinstance(deco, ast.Call) and isinstance(deco.func, ast.Name) and deco.func.id == "dataclass":
                return True

        return False

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef | None:
        """Rewrite specific class attributes to be camelCase."""
        if self.is_dataclass(node):
            for cls_attr in node.body:
                # SKIP THE CONSTRUCTOR
                if isinstance(cls_attr, ast.FunctionDef) and cls_attr.name == "__post_init__":
                    continue

                assert isinstance(cls_attr, ast.AnnAssign), "Attempting to camelCase a non-assignment expression."
                assert isinstance(cls_attr.target, ast.Name), "Attempting to camelCase a non-assignment expression."

                overrides: set[bool] = set()

                # IF MORE OVERIDES ARE NECESSARY, JUST ADD THEM BELOW.
                #
                # 1. WE ARE A FormatConfig PROTO.
                overrides.add("FormatConfig" in node.name)
                # 2. WE HAVE AN ATTRIBUTE CALLED plot_as_band.
                overrides.add(cls_attr.target.id == "plot_as_band")
                # 3. WE ARE AN ATTRIBUTE CALLED geometry_type.
                overrides.add(cls_attr.target.id == "geometry_type")

                if any(overrides):
                    # "node.target.id" IS THE LHS NAME OF AN ASSIGNMENT EXPRESSION
                    cls_attr.target.id = self.snake_to_camel(cls_attr.target.id)

        return node


class BetterprotoBetaCleaner(ast.NodeTransformer):
    # NOTE: @boonhapus, 2024/11/09
    # INJECTING OPTIONALITY INTO EVERY FIELD IS WHAT STRONGLY ALLOWS US TO BE BACKWARDS COMPATIBLE IN TML.

    @staticmethod
    def is_dataclass(node: ast.ClassDef) -> bool:
        """Determine if the class is a dataclass."""
        for deco in node.decorator_list:
            # @dataclass
            if isinstance(deco, ast.Name) and deco.id == "dataclass":
                return True

            # @dataclass(...)
            if isinstance(deco, ast.Call) and isinstance(deco.func, ast.Name) and deco.func.id == "dataclass":
                return True

        return False

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef | None:
        """Inject optionality to dataclass attributes."""
        if self.is_dataclass(node):
            # IF betterproto CREATED A CLASS WITH NO FIELDS, JUST DROP IT
            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                return None

            optional_keyword = ast.keyword(arg="optional", value=ast.Constant(True))  # betterproto.field(optional=True)
            cls_attrs: list[ast.AnnAssign] = []
            cls_other: list[Any] = []

            for cls_attr in node.body:
                if not isinstance(cls_attr, ast.AnnAssign):
                    cls_other.append(cls_attr)
                    continue

                cls_attrs.append(cls_attr)

                raw_attr_str = ast.unparse(cls_attr)

                if "map_field" not in raw_attr_str and "betterproto" in raw_attr_str and "field" in raw_attr_str:
                    assert isinstance(cls_attr.value, ast.Call), "Attempting to add optionality to a non-function call."
                    cls_attr.value.keywords.append(optional_keyword)

            # DEV NOTE: betterproto WON'T SORT FIELDS AUTOMATICALLY, SORT ALL THE FIELDS BASED ON THEIR ORDER.
            node.body = [*sorted(cls_attrs, key=lambda e: e.value.args[0].value), *cls_other]  # type: ignore[union-attr]

        # CONTINUE PROCESSING
        return node


postprocessors = [
    # DEVNOTE: @boonhapus, 2024/11/09
    # THIS IS IN A PRIORITY ORDER
    #
    BetterprotoBetaCleaner(),
    ThoughtSpotLintingFormatter(),
]
