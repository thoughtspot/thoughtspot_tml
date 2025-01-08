from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from yaml import error

if TYPE_CHECKING:
    from collections.abc import Iterable
    from pathlib import Path

    from thoughtspot_tml.types import GUID, TMLObject


class TMLDeprecationWarning(DeprecationWarning):
    """
    Deprecations in thoughtspot_tml derive from this Exception.
    """


class TMLError(Exception):
    """
    All errors in thoughtspot_tml derive from this Exception.
    """


class TMLExtensionWarning(UserWarning):
    """
    Alerts when a user saves a TML file without the proper extension.
    """


class MissingGUIDMappedValueWarning(UserWarning):
    """
    Alerts when a GUID mapping is generated, but is missing across environments.
    """


class TMLDecodeError(TMLError):
    """
    Raised when a TML object cannot be instantiated from input data.
    """

    def __init__(self, tml_cls: type[TMLObject], *, exc: Exception, document: str, filepath: Optional[Path] = None):
        self.tml_cls = tml_cls
        self.parent_exc = exc
        self.document = document
        self.filepath = filepath

    def with_filepath(self, filepath) -> TMLDecodeError:
        """Add the file which generated the exception."""
        self.filepath = filepath
        return self

    def __str__(self) -> str:
        lines: list[str] = []

        if isinstance(self.parent_exc, TypeError):
            _, _, attribute = str(self.parent_exc).partition(" unexpected keyword argument ")
            lines.append(f"Unrecognized attribute in the TML spec: {attribute}")

        if self.filepath is not None:
            lines.append("\n")
            lines.append(f"File '{self.filepath}' may not be a valid {self.tml_cls.__name__} file")

        if isinstance(self.parent_exc, error.MarkedYAMLError):
            if mark := self.parent_exc.problem_mark:
                lines.append("\n")
                lines.append(f"Syntax error on line {mark.line + 1}, around column {mark.column + 1}")

                if snippet := mark.get_snippet():
                    lines.append(snippet)

        if not lines:
            lines.append(str(self.parent_exc))

        return "\n".join(lines).strip()


class TMLDisambiguationError(TMLError):
    """
    Raised when a TML file (or files) does not have the FQN property.
    """

    def __init__(self, tml_guids: Iterable[GUID]):
        self.tml_guids = tml_guids

    def __str__(self) -> str:
        guids = ", ".join(self.tml_guids)
        return f"No FQN found on: {guids}, was metadata/tml/export ran with parameter: export_fqn = true ?"
