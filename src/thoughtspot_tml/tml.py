from collections.abc import Collection
from dataclasses import dataclass, fields, is_dataclass, asdict
from typing import TYPE_CHECKING
import pathlib
import typing
import json

import yaml

from thoughtspot_tml._compat import get_origin, get_args
from thoughtspot_tml.exceptions import TMLDecodeError
from thoughtspot_tml.types import GUID
from thoughtspot_tml import _scriptability
from thoughtspot_tml import _yaml


if TYPE_CHECKING:
    from thoughtspot.types import PathLike

    TTML = typing.TypeVar("TTML", bound="TML")


def _recursive_complex_attrs_to_dataclasses(instance: typing.Any) -> typing.Any:
    """
    Convert all fields of type `dataclass` into an instance of the
    specified data class if the current value is of type dict.

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
            _recursive_complex_attrs_to_dataclasses(new_value)

        # it's an Annotation that needs resolution
        elif isinstance(field.type, str) and isinstance(value, dict):
            type_ = getattr(_scriptability, field.type)
            new_value = type_(**value)
            _recursive_complex_attrs_to_dataclasses(new_value)

        # it's a List of basic types or ForwardRefs
        elif get_origin(field.type) is list:
            new_value = []
            args = get_args(field.type)
            field_type = args[0].__forward_value__ if isinstance(args[0], typing.ForwardRef) else args[0]

            for item in value:
                if is_dataclass(field_type) and isinstance(item, dict):
                    item = field_type(**item)

                new_value.append(item)

                if is_dataclass(field_type):
                    _recursive_complex_attrs_to_dataclasses(item)

        # it's an empty mapping, python-betterproto doesn't support optional map_fields
        elif get_origin(field.type) is dict and not value:
            new_value = None

        else:  # pragma: peephole optimizer
            continue

        setattr(instance, field.name, new_value)


def _recursive_remove_null(mapping: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    """
    Drop all keys with null values, they're optional.
    """
    new = {}

    for k, v in mapping.items():

        if isinstance(v, dict):
            v = _recursive_remove_null(v)

        if isinstance(v, list):
            v = [_recursive_remove_null(e) if isinstance(e, dict) else e for e in v if e is not None]

        # if v is an empty collection, discard it
        if v is None or (isinstance(v, Collection) and not isinstance(v, str) and not v):  # pragma: peephole optimizer
            continue

        new[k] = v

    return new


@dataclass
class TML:
    """
    Base object for ThoughtSpot TML.
    """

    def __post_init__(self):
        _recursive_complex_attrs_to_dataclasses(self)

    @classmethod
    def loads(cls, tml_document: str) -> "TTML":
        """
        Deserialize a TML document to a Python object.
        """
        document = _yaml.load(tml_document)

        try:
            instance = cls(**document)
        except TypeError:
            raise TMLDecodeError(cls, data=document) from None

        return instance

    @classmethod
    def load(cls, path: "PathLike") -> "TTML":
        """
        Deserialize a TML document located at filepath to a Python object.
        """
        if isinstance(path, str):
            path = pathlib.Path(path)

        try:
            instance = cls.loads(path.read_text())
        except yaml.scanner.ScannerError as e:
            raise TMLDecodeError(cls, path=path, problem_mark=e.problem_mark) from None

        return instance

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        """
        Serialize this object to native python data types.
        """
        return asdict(self)

    def dumps(self, format_type: str = "YAML") -> str:
        """
        Serialize this object as a YAML- or JSON-formatted str.
        """
        data = _recursive_remove_null(self.to_dict())

        if format_type.upper() == "YAML":
            document = _yaml.dump(data)

        if format_type.upper() == "JSON":
            document = json.dumps(data, indent=4, sort_keys=False)  # to match the yaml semantic

        return document

    def dump(self, path: "PathLike") -> None:
        """
        Serialize this object as a YAML-formatted stream to a filepath.
        """
        if isinstance(path, str):
            path = pathlib.Path(path)

        document = self.dumps(format_type="JSON" if ".json" in path.suffix.lower() else "YAML")
        path.write_text(document)


@dataclass
class Connection(TML):
    """
    Representation of a ThoughtSpot Connection YAML.
    """

    # @boonhapus, 2022/11/20
    #
    # "Why is this one different?"
    # Connections do not yet have a TML representation. The TML data format is simply
    # the YAML 1.1 spec. Connections were the first text representation of metadata in
    # ThoughtSpot and leveraged the YAML extension.
    #
    name: str
    type: str
    authentication_type: str
    properties: typing.List[_scriptability.KeyValueStr]
    table: typing.List[_scriptability.ConnectionDocTableDoc]


@dataclass
class Table(TML):
    """
    Representation of a ThoughtSpot System Table TML.
    """

    guid: GUID
    table: _scriptability.LogicalTableEDocProto

    @property
    def name(self) -> str:
        return self.table.name


@dataclass
class View(TML):
    """
    Representation of a ThoughtSpot View TML.
    """

    guid: GUID
    view: _scriptability.ViewEDocProto

    @property
    def name(self) -> str:
        return self.view.name


@dataclass
class SQLView(TML):
    """
    Representation of a ThoughtSpot SQLView TML.
    """

    guid: GUID
    sql_view: _scriptability.SqlViewEDocProto

    @property
    def name(self) -> str:
        return self.sql_view.name


@dataclass
class Worksheet(TML):
    """
    Representation of a ThoughtSpot Worksheet TML.
    """

    guid: GUID
    worksheet: _scriptability.WorksheetEDocProto

    @property
    def name(self) -> str:
        return self.worksheet.name


@dataclass
class Answer(TML):
    """
    Representation of a ThoughtSpot Answer TML.
    """

    guid: GUID
    answer: _scriptability.AnswerEDocProto

    @property
    def name(self) -> str:
        return self.answer.name


@dataclass
class Liveboard(TML):
    """
    Representation of a ThoughtSpot Liveboard TML.
    """

    guid: GUID
    liveboard: _scriptability.PinboardEDocProto

    @property
    def name(self) -> str:
        return self.liveboard.name


@dataclass
class Pinboard(TML):
    """
    Representation of a ThoughtSpot Pinboard TML.

    DEPRECATED :: https://docs.thoughtspot.com/software/latest/deprecation
      As part of the May 2022 ThoughtSpot release, we rebranded pinboards as Liveboards.
    """

    guid: GUID
    pinboard: _scriptability.PinboardEDocProto

    @property
    def name(self) -> str:
        return self.pinboard.name
