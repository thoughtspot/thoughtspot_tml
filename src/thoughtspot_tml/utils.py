from dataclasses import fields, is_dataclass
from typing import Any, Callable, Dict, List, Tuple, Union
import pathlib
import json

from thoughtspot_tml.exceptions import TMLError
from thoughtspot_tml.types import GUID, TMLObject, TMLDocInfo, PathLike
from thoughtspot_tml.tml import Connection
from thoughtspot_tml.tml import Table, View, SQLView, Worksheet
from thoughtspot_tml.tml import Answer, Liveboard, Pinboard
from thoughtspot_tml import _scriptability, _compat


def _recursive_scan(scriptability_object: Any, check: Callable[Any, bool] = None) -> List[Any]:
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

            if check(element):
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
            tml_type = ""

    if info is not None:
        tml_type = info.get("type", "")

    if tml_type not in types:
        lines = [f"could not parse TML type from 'info' or 'path', got '{tml_type}'"]

        if path is not None:
            lines.append(f"from path, '{path}'")

        if info is not None:
            lines.append(f"from info, '{info}'")

        raise TMLError("\n".join(lines))

    return types[tml_type]


def disambiguate(tml: TMLObject, *, guid_mapping: Dict[str, GUID], delete_unmapped_guid: bool = False) -> TMLObject:
    """
    Deep scan the TML looking for fields to add FQNs to.

    This will explore all nested objects looking for Tables, Worksheets,
    etc to disambiguate.

    Parameters
    ----------
    tml : TMLObject
      the tml to scan

    guid_mapping : {str, GUID}
      a mapping of names or guids, to the FQN to add to the object

    delete_unmapped_guid : bool = False
      if a match could not be found, set the FQN to None
    """
    attrs = _recursive_scan(tml, check=lambda attr: isinstance(attr, _scriptability.Identity))

    if not attrs:
        raise TMLError("could not find any attributes to disambiguate")

    for attribute in attrs:
        # NAME -> GUID
        if attribute.name in guid_mapping:
            attribute.fqn = guid_mapping[attribute.name]
            continue

        # ENVT_A.GUID -> ENVT_B.GUID
        if attribute.fqn in guid_mapping:
            attribute.fqn = guid_mapping[attribute.fqn]
            continue

        if delete_unmapped_guid:
            attribute.fqn = None

    return tml
