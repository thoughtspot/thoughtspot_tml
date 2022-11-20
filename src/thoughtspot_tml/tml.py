from dataclasses import dataclass, fields, is_dataclass, asdict
from typing import TYPE_CHECKING, get_origin, get_args
import pathlib
import typing
import os

from thoughtspot_tml import _scriptability
from thoughtspot_tml import _yaml

if TYPE_CHECKING:
    PathLike = typing.Union[str, bytes, os.PathLike]
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

        # python-betterproto doesn't support optional map_fields
        if value == {}:
            setattr(instance, field.name, None)
            continue

        # it's a dataclass
        if is_dataclass(field.type) and isinstance(value, dict):
            new_value = field.type(**value)
            _recursive_complex_attrs_to_dataclasses(new_value)

        # it's an Annotation
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

        else:
            continue

        setattr(instance, field.name, new_value)


def _recursive_remove_null(mapping: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    """
    Drop all keys with null values, they're optional.
    """
    new = {}

    for k, v in mapping.items():
        if isinstance(v, dict):
            new[k] = _recursive_remove_null(v)

        elif isinstance(v, list):
            new[k] = [_recursive_remove_null(element) if isinstance(element, dict) else element for element in v]

        elif v is not None:
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
        return cls(**document)

    @classmethod
    def load(cls, fp: "PathLike") -> "TTML":
        """
        Deserialize a TML document located at filepath to a Python object.
        """
        path = pathlib.Path(fp)
        return cls.loads(path.read_text())

    def dumps(self) -> str:
        """
        Serialize this object as a YAML-formatted str.
        """
        data = _recursive_remove_null(asdict(self))
        document = _yaml.dump(data)
        return document

    def dump(self, fp: "PathLike") -> None:
        """
        Serialize this object as a YAML-formatted stream to a filepath.
        """
        path = pathlib.Path(fp)
        document = self.dumps()
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
class SQLView(TML):
    """
    Representation of a ThoughtSpot SQLView TML.
    """

    guid: str
    sql_view: _scriptability.SqlViewEDocProto


@dataclass
class Answer(TML):
    """
    Representation of a ThoughtSpot Answer TML.
    """

    guid: str
    answer: _scriptability.AnswerEDocProto
