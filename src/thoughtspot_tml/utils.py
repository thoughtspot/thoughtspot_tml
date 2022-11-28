from typing import Any, Callable, Dict, Tuple, Union
import pathlib
import json

from thoughtspot_tml.exceptions import TMLError
from thoughtspot_tml.types import GUID, TMLObject, TMLDocInfo, PathLike
from thoughtspot_tml.tml import Connection
from thoughtspot_tml.tml import Table, View, SQLView, Worksheet
from thoughtspot_tml.tml import Answer, Liveboard, Pinboard


def determine_tml_type(*, info: TMLDocInfo = None, path: PathLike = None) -> Union[Connection, TMLObject]:
    """
    Get the appropriate TML class based on input data.

    Parameters
    ----------
    info : TMLDocInfo
      API edoc info response

    path : PathLike
      filepath to parse 

    Returns
    -------
    tml_cls : TML (Connection or TMLObject)

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

        if path.suffix.lower() == ".yaml":
            tml_type = "connection"
        else:
            tml_type, _, _ = ".".join(_[1:] for _ in path.suffixes).partition(".")

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
