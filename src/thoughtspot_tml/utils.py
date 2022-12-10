from __future__ import annotations
from dataclasses import fields, is_dataclass
from typing import Any, Callable, Dict, List, Tuple, Union
import warnings
import logging
import pathlib
import json

from thoughtspot_tml.exceptions import TMLError, MissingGUIDMappedValueWarning
from thoughtspot_tml.types import GUID, TMLObject, TMLDocInfo, PathLike
from thoughtspot_tml.tml import Connection
from thoughtspot_tml.tml import Table, View, SQLView, Worksheet
from thoughtspot_tml.tml import Answer, Liveboard, Pinboard
from thoughtspot_tml import _scriptability, _compat

_UNDEFINED = object()
log = logging.getLogger(__name__)


def _recursive_scan(scriptability_object: Any, *, check: Callable[[Any], bool] = None) -> List[Any]:
    collect = []
    is_container_type = lambda t: len(_compat.get_args(t)) > 0

    for field in fields(scriptability_object):
        child = getattr(scriptability_object, field.name)

        if child is None:
            continue

        elements = [child] if not is_container_type(field.type) else child

        for element in elements:
            if is_dataclass(element):
                collect.extend(_recursive_scan(element, check=check))

            if check is not None and check(element):
                collect.append(element)

    return collect


def determine_tml_type(*, info: TMLDocInfo = None, path: PathLike = None) -> Union[Connection, TMLObject]:
    """
    Get the appropriate TML class based on input data.

    Parameters
    ----------
    info : TMLDocInfo
      API edoc info response

    path : PathLike
      filepath to parse

    Raises
    ------
    TMLError, when a valid TML type could not be found based on input
    """
    if info is None and path is None:
        raise TypeError("determine_tml_type() missing at least 1 required keyword-only argument: 'info' or 'path'")

    types = {
        "connection": Connection,
        "table": Table,
        "view": View,
        "sql_view": SQLView,
        "sqlview": SQLView,
        "worksheet": Worksheet,
        "answer": Answer,
        "liveboard": Liveboard,
        "pinboard": Pinboard,
    }

    if path is not None:
        path = pathlib.Path(path)

        if path.name.endswith(".tml"):
            tml_type, _, _ = ".".join(_[1:] for _ in path.suffixes).partition(".")
        elif path.name.lower() == "connection.yaml":
            tml_type = "connection"
        else:
            tml_type = next(
                (
                    # 3. remove the trailing colon, unless it's a connection.yaml then remap
                    "connection" if line == "properties:" else line[:-1]
                    # 1. scan the file's text
                    for line in path.read_text().split("\n")
                    # 2. look for top-level keys in the YAML
                    if line.endswith(":")
                    if not line.startswith(" ")
                ),
                # 4. if no matches found (eg. StopIteration is raised), use the default value
                default="NOT_FOUND",
            )

    if info is not None:
        tml_type = info.get("type", "NOT_FOUND")

    if tml_type not in types:
        lines = [f"could not parse TML type from 'info' or 'path', got '{tml_type}'"]

        if path is not None:
            lines.append(f"from path, '{path}'")

        if info is not None:
            lines.append(f"from info, '{info}'")

        raise TMLError("\n".join(lines))

    return types[tml_type]


class EnvironmentGUIDMapper:
    """
    A dict-like container which maps guids from one environment to another.

    This can be a helpful way to track objects across environments.

    Produces a mapping file which takes the form below..

    {
        "guid1__guid2": {
            "ENVT_NAME_A": "guid1",
            "ENVT_NAME_B": "guid2",
            ...
        },
        ...
    }

    Usage of this object is as simple as..

    # create a new mapper
    mapper = EnvironmentGUIDMapper()  # or EnvironmentGUIDMapper.read(path=...)

    # add a brand brand new guid into the mapper
    mapper["guid1"] = ("PROD", "guid1")

    # map guid1 to a guid in another environment
    mapper["guid1"] = ("TEST", "guid2")

    # map a new guid3 to any of existing guid
    # this means all 3 guids represent the same object across environments
    mapper["guid2"] = ("PROD", "guid3")

    # persist the mapping file to disk
    mapper.save(path="marketing_thoughtspot_guid_mapping.json")

    Attributes
    ----------
    environment_transformer : Callable(str) -> str
      a function which transforms the ENV name before adding it to the mapping
    """

    def __init__(self, environment_transformer: Callable[[str], str] = str.upper):
        self.environment_transformer = environment_transformer
        self._mapping: Dict[str, Dict[str, GUID]] = {}

    def __setitem__(self, guid: GUID, value: Tuple[str, GUID]) -> None:
        environment, guid_to_add = value
        environment = self.environment_transformer(environment)

        try:
            envts: Dict[str, GUID] = self[guid]
        except KeyError:
            new_key = guid_to_add
            envts = {environment: guid_to_add}
        else:
            old_key = "__".join(envts.values())
            self._mapping.pop(old_key)

            envts[environment] = guid_to_add
            new_key = "__".join(envts.values())

        self._mapping.setdefault(new_key, {}).update(envts)

    def __getitem__(self, guid: GUID) -> Dict[str, GUID]:
        for guids_across_envts, envts in self._mapping.items():
            if guid in guids_across_envts.split("__"):
                return envts
        raise KeyError(f"no environment matches guid, got '{guid}'")

    def __contains__(self, guid: GUID) -> bool:
        return bool(self.get(guid, default=False))

    def set(self, src_guid: GUID, *, environment: str, guid: GUID) -> None:
        """
        Insert a new GUID into the mapping.

        Equivalent to..

        d = EnvironmentGUIDMapper()
        d[src_guid] = (environment, guid)
        """
        self[src_guid] = (environment, guid)

    def get(self, guid: GUID, *, default: Any = _UNDEFINED) -> Dict[str, GUID]:
        """
        Retrieve a GUID mapping.

        Equivalent to..

        d = EnvironmentGUIDMapper()
        d[src_guid]
        """
        try:
            retval = self[guid]
        except KeyError as e:
            if default is _UNDEFINED:
                raise e from None
            retval = default

        return retval

    def generate_mapping(self, from_environment: str, to_environment: str) -> Dict[GUID, GUID]:
        """
        Create a mapping of GUIDs between two environments.

        Parameters
        ----------
        from_environment : str
          the source environment to map TML objects from

        to_environment : str
          the target environment to map TML objects to
        """
        from_environment = self.environment_transformer(from_environment)
        to_environment = self.environment_transformer(to_environment)
        mapping: Dict[GUID, GUID] = {}

        for envts in self._mapping.values():
            envt_a = envts.get(from_environment, None)
            envt_b = envts.get(to_environment, None)

            if None in (envt_a, envt_b):
                message = [f"an incomplete mapping has been detected between {from_environment} and {to_environment}"]

                if envt_a is None:
                    message.append(f"no GUID found for '{from_environment}' ({to_environment}='{envt_b}')")

                if envt_b is None:
                    message.append(f"no GUID found for '{to_environment}' ({from_environment}='{envt_a}')")

                warnings.warn("\n".join(message), MissingGUIDMappedValueWarning, stacklevel=2)
                continue

            mapping[envt_a] = envt_b

        return mapping

    @classmethod
    def read(cls, path: PathLike, environment_transformer: Callable[[str], str] = str.upper):
        """
        Load the guid mapping from file.

        Parameters
        ----------
        path : PathLike
          filepath to read the mapping from

        environment_transformer : Callable(str) -> str
          a function which transforms the ENV name before adding it to the mapping
        """
        instance = cls(environment_transformer=environment_transformer)

        with pathlib.Path(path).open(mode="r", encoding="UTF-8") as j:
            data = json.load(j)

        data.pop("__INFO_for_comments_only", None)
        instance._mapping = data
        return instance

    def save(self, path: PathLike, *, info: Dict[str, Any] = None) -> None:
        """
        Save the guid mapping to file.

        Parameters
        ----------
        path : PathLike
          filepath to save the mapping to
        """
        data = {}

        if info is not None:
            data["__INFO_for_comments_only"] = info

        data = {**data, **self._mapping}

        with pathlib.Path(path).open(mode="w", encoding="UTF-8") as j:
            json.dump(data, j, indent=4)

    def __str__(self) -> str:
        return json.dumps(self._mapping, indent=4)


def disambiguate(
    tml: TMLObject,
    *,
    guid_mapping: Dict[str, GUID],
    remap_object_guid: bool = True,
    delete_unmapped_guids: bool = False,
) -> TMLObject:
    """
    Deep scan the TML looking for fields to add FQNs to.

    This will explore the top-level guid and all nested objects looking on
    Tables, Worksheets, etc to disambiguate.

    Parameters
    ----------
    tml : TMLObject
      the tml to scan

    guid_mapping : {str: GUID}
      a mapping of names or guids, to the FQN to add to the object

    remap_object_guid : bool = True
      whether or not to remap the tml.guid

    delete_unmapped_guids : bool = False
      if a match could not be found, set the FQN and object guid to None
    """
    if remap_object_guid:
        if tml.guid in guid_mapping:
            tml.guid = guid_mapping[tml.guid]

        elif delete_unmapped_guids:
            tml.guid = None

    # DEVNOTE: @boonhapus, might need to add another scan for PinnedVisualization.viz_guid
    attrs = _recursive_scan(tml, check=lambda attr: isinstance(attr, _scriptability.Identity))

    if not attrs:
        log.debug(f"could not find any attributes to disambiguate on {tml}")

    for attribute in attrs:
        # NAME -> GUID
        if attribute.name in guid_mapping:
            attribute.fqn = guid_mapping[attribute.name]

        # ENVT_A.GUID -> ENVT_B.GUID
        elif attribute.fqn in guid_mapping:
            attribute.fqn = guid_mapping[attribute.fqn]

        elif delete_unmapped_guids:
            attribute.fqn = None

    return tml
