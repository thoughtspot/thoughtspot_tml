from __future__ import annotations

from collections.abc import Collection
from dataclasses import asdict, dataclass, fields, is_dataclass
from typing import TYPE_CHECKING, ForwardRef, Optional, get_args, get_origin
import functools as ft
import json
import keyword
import pathlib
import re
import warnings

from thoughtspot_tml import _scriptability, _yaml
from thoughtspot_tml._compat import Self
from thoughtspot_tml.exceptions import TMLDecodeError, TMLExtensionWarning

if TYPE_CHECKING:
    from typing import Any

    from thoughtspot_tml.types import GUID

RE_CAMEL_CASE = re.compile(r"[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+")


def attempt_resolve_type(type_hint: Any) -> Any:
    """Resolves string type hints to actual types."""
    # IF IT'S A ForwardRef, RESOLVE IT.
    # Further Reading:
    #   https://docs.python.org/3/library/typing.html#typing.ForwardRef
    if isinstance(type_hint, ForwardRef):
        return type_hint.__forward_value__

    # IF IT'S A STRING, ATTEMPT TO LOOK IT UP IN _scriptability.py
    if isinstance(type_hint, str):
        return getattr(_scriptability, type_hint.replace("_scriptability.", ""), type_hint)
    return type_hint


def origin_or_fallback(type_hint: Any, *, default: Any) -> Any:
    """
    Get the unsubscripted version of a type, with optional fallback.

    Further Reading:
      https://docs.python.org/3/library/typing.html#typing.get_origin
    """
    return get_origin(type_hint) or default


def recursive_complex_attrs_to_dataclasses(instance: Any) -> None:
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
    RESOLVED_TYPEHINT_HAS_CHILDREN = ft.partial(lambda hint, expr: is_dataclass(hint) and isinstance(expr, dict))
    cls = type(instance)

    for field in fields(cls):
        value = getattr(instance, field.name)

        if value is None:
            continue

        # TRY TO RESOLVE STRING REFERENCES FROM _scriptability.py
        # eg. ActionObjectEDocProto , ConnectionEDocProto , etc ..
        #
        # NOTE: this falls back to the original type_hint when it can't be resolved.
        field_type = attempt_resolve_type(field.type)

        # ORIGIN TYPES ARE THE X in X[a, b, c] hints.. but does not include native types
        # eg.  typing.List[str] but NOT list[str]
        origin_type = origin_or_fallback(field_type, default=field_type)

        # RECURSE INTO RESOLVED _scripatability.py HINTS
        if RESOLVED_TYPEHINT_HAS_CHILDREN(hint=field_type, expr=value):
            new_value = field_type(**value)
            recursive_complex_attrs_to_dataclasses(new_value)

        # list IS USED TO DENOTE THAT A TML OBJECT CAN CONTAIN MULTIPLE HOMOGENOUS
        # CHILDREN SO WE TAKE JUST THE FIRST ELEMENT AND ATTEMPT TO RESOLVE IT.
        elif origin_type is list:
            homo_type = next(iter(get_args(field_type)))
            item_type = attempt_resolve_type(homo_type)

            new_value = []

            for item in value:
                # RECURSE INTO RESOLVED _scripatability.py HINTS
                if RESOLVED_TYPEHINT_HAS_CHILDREN(hint=item_type, expr=item):
                    item = item_type(**_sanitize_reserved_keyword_keys(item))
                    recursive_complex_attrs_to_dataclasses(item)

                new_value.append(item)

        # IF OUR VALUE IS EMPTY, IT IS OPTIONAL AND SO WE'RE GOING TO DROP IT.
        elif origin_type is dict and not value:
            new_value = None

        # DEV NOTE: @boonhapus, 2025/01/08
        #   Q. WHY NO (origin_type is dict and value) LIKE WE HAVE FOR LISTS?
        #   A. Currently the edoc spec does not maintain complex mapping types. If we
        #      need to support them, we'll need to add them at this priority (below
        #      empty dicts -- so we continue to support optionality).

        # SIMPLE TYPES DO NOT NEED RECURSION.
        else:
            continue

        setattr(instance, field.name, new_value)


def _sanitize_reserved_keyword_keys(mapping: dict[str, Any]) -> dict[str, Any]:
    """
    Replace reserved keywords with a trailing sunder.
    """
    return {(f"{k}_" if keyword.iskeyword(k) else k): v for k, v in mapping.items()}


def _recursive_remove_null(mapping: dict[str, Any]) -> dict[str, Any]:
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

    guid: Optional[GUID]

    @property
    def tml_type_name(self) -> str:
        """Return the type name of the TML object."""
        cls_name = type(self).__name__
        camels = RE_CAMEL_CASE.findall(cls_name)
        snakes = "_".join(camels)
        return snakes.lower()

    @property
    def name(self) -> str:
        """This should be implemented in child classes."""
        raise NotImplementedError

    def __post_init__(self):
        recursive_complex_attrs_to_dataclasses(self)

    @classmethod
    def _loads(cls, tml_document: str) -> dict[str, Any]:
        # DEV NOTE: @boonhapus
        #  DO NOT OVERRIDE THIS!!
        #    These exist to handle backwards compatible changes between TML versions.
        return _yaml.load(tml_document)

    def _to_dict(self) -> dict[str, Any]:
        # DEV NOTE: @boonhapus
        #  DO NOT OVERRIDE THIS!!
        #    These exist to handle backwards compatible changes between TML versions.
        return asdict(self)

    @classmethod
    def loads(cls, tml_document: str) -> Self:
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
            data = cls._loads(tml_document)
            instance = cls(**data)
        except Exception as e:
            raise TMLDecodeError(cls, exc=e, document=tml_document) from None

        return instance

    @classmethod
    def load(cls, path: pathlib.Path) -> Self:
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
            # INTERCEPT AND INJECT THE FILEPATH.
            e.filepath = path
            raise e from None

        return instance

    def to_dict(self) -> dict[str, Any]:
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
