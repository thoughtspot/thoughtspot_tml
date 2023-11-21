from __future__ import annotations

from collections.abc import Collection
from typing import TYPE_CHECKING
from dataclasses import asdict, dataclass, fields, is_dataclass
import warnings
import pathlib
import typing
import json
import re

import yaml

from thoughtspot_tml.exceptions import TMLDecodeError, TMLExtensionWarning
from thoughtspot_tml._compat import get_origin, get_args
from thoughtspot_tml import _scriptability, _yaml

if TYPE_CHECKING:
    from typing import Any, Dict


RE_CAMEL_CASE = re.compile(r"[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+")


def recursive_complex_attrs_to_dataclasses(instance: Any) -> None:  # noqa: C901
    """
    Convert all fields of type `dataclass` into an instance of the
    specified dataclass if the current value is a dict.

    Types will always be one of:
      - dataclass
      - basic type
      - dataclass annotation (aka, a str) - to be gathered from _scriptability
      - list of basic types
      - list of dataclass annotation
    """
    cls = type(instance)

    for field in fields(cls):
        value = getattr(instance, field.name)

        # ignore nulls, they get dropped to support optionality
        if value is None:
            continue

        # it's a dataclass
        if is_dataclass(field.type) and isinstance(value, dict):
            new_value = field.type(**value)
            recursive_complex_attrs_to_dataclasses(new_value)

        # it's an _scriptability dataclass Annotation that needs resolution
        elif isinstance(field.type, str) and isinstance(value, dict):
            if field.type.startswith("_scriptability"):
                _, _, field_type = field.type.partition(".")
            else:
                field_type = field.type

            type_ = getattr(_scriptability, field_type)
            new_value = type_(**value)
            recursive_complex_attrs_to_dataclasses(new_value)

        # it's a List of basic types or ForwardRefs
        elif get_origin(field.type) is list:
            new_value = []  # type: ignore[assignment]
            args = get_args(field.type)
            field_type = args[0].__forward_value__ if isinstance(args[0], typing.ForwardRef) else args[0]

            for item in value:
                if is_dataclass(field_type) and isinstance(item, dict):
                    item = field_type(**item)

                new_value.append(item)  # type: ignore[attr-defined]

                if is_dataclass(field_type):
                    recursive_complex_attrs_to_dataclasses(item)

        # it's an empty mapping, python-betterproto doesn't support optional map_fields
        elif get_origin(field.type) is dict and value == {}:
            new_value = None

        else:  # pragma: peephole optimizer
            continue

        setattr(instance, field.name, new_value)


def _recursive_remove_null(mapping: Dict[str, Any]) -> Dict[str, Any]:
    """
    Drop all keys with null values, they're optional.
    """
    new = {}

    for k, v in mapping.items():

        if isinstance(v, dict):
            v = _recursive_remove_null(v)

        if isinstance(v, list):
            v = [_recursive_remove_null(e) if isinstance(e, dict) else e for e in v if e is not None]

        # EXCEPTION:
        # - don't remove connection.yaml empty password
        # - historical client_state attribute
        if k in ("value", "client_state") and v == "":
            new[k] = v
            continue

        # If v is any form of EMPTY
        is_none = v is None
        is_empty_string = v == ""
        is_empty_collection = isinstance(v, Collection) and not isinstance(v, str) and not v

        if is_none or is_empty_string or is_empty_collection:  # pragma: peephole optimizer
            continue

        new[k] = v

    return new


@dataclass
class TML:
    """
    Base object for ThoughtSpot TML.
    """

    @property
    def tml_type_name(self) -> str:
        """Return the type name of the TML object."""
        cls_name = type(self).__name__
        camels = RE_CAMEL_CASE.findall(cls_name)
        snakes = "_".join(camels)
        return snakes.lower()

    def __post_init__(self):
        recursive_complex_attrs_to_dataclasses(self)

    @classmethod
    def _loads(cls, tml_document: str) -> Dict[str, Any]:
        # @boonhapus note: do not override this!!
        #   ONLY exists to enable a TML interface over Connections and fix SCAL-134095
        return _yaml.load(tml_document)

    def _to_dict(self) -> Dict[str, Any]:
        # @boonhapus note: do not override this!!
        #   ONLY exists to enable a TML interface over Connections and fix SCAL-134095
        return asdict(self)

    @classmethod
    def loads(cls, tml_document: str) -> TML:
        """
        Deserialize a TML document to a Python object.

        Parameters
        ----------
        tml_document : str
          text to parse into a TML object

        Raises
        ------
        TMLDecodeError, when the document string cannot be parsed or receives extra data
        """
        try:
            document = cls._loads(tml_document)
        except (yaml.scanner.ScannerError, yaml.parser.ParserError) as e:
            raise TMLDecodeError(cls, problem_mark=e.problem_mark) from None  # type: ignore[arg-type]

        try:
            instance = cls(**document)
        except TypeError as e:
            raise TMLDecodeError(cls, data=document, message=str(e)) from None  # type: ignore[arg-type]

        return instance

    @classmethod
    def load(cls, path: pathlib.Path) -> TML:
        """
        Deserialize a TML document located at filepath to a Python object.

        Parameters
        ----------
        path : PathLike
          filepath to load the TML document from

        Raises
        ------
        TMLDecodeError, when the document string cannot be parsed or receives extra data
        """
        if isinstance(path, str):
            path = pathlib.Path(path)

        try:
            instance = cls.loads(path.read_text(encoding="utf-8"))
        except TMLDecodeError as e:
            e.path = path
            raise e from None

        return instance

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize this object to native python data types.
        """
        return self._to_dict()

    def dumps(self, format_type: str = "YAML") -> str:
        """
        Serialize this object as a YAML- or JSON-formatted str.

        Parameters
        ----------
        format_type : str
          data format to save in .. one of, 'YAML' or 'JSON'
        """
        if format_type.upper() not in ("YAML", "JSON"):
            raise ValueError(f"format_type must be either 'YAML' or 'JSON' .. got, '{format_type}'")

        data = _recursive_remove_null(self.to_dict())

        if format_type.upper() == "YAML":
            document = _yaml.dump(data)

        if format_type.upper() == "JSON":
            document = json.dumps(data, indent=4, sort_keys=False)  # to match the yaml semantic

        return document

    def dump(self, path: pathlib.Path) -> None:
        """
        Serialize this object as a YAML-formatted stream to a filepath.

        Parameters
        ----------
        path : PathLike
          filepath to save the TML document to
        """
        if isinstance(path, str):
            path = pathlib.Path(path)

        if not path.name.endswith(".json") and not path.name.endswith(f"{self.tml_type_name}.tml"):
            warnings.warn(
                f"saving to '{path}', expected {path.stem}.{self.tml_type_name}.tml",
                TMLExtensionWarning,
                stacklevel=2,
            )

        document = self.dumps(format_type="JSON" if ".json" in path.suffix.lower() else "YAML")
        path.write_text(document, encoding="utf-8")
