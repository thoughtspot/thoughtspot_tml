from typing import Union
import pathlib

from thoughtspot_tml.exceptions import TMLError
from thoughtspot_tml.types import TMLObject, TMLDocInfo, PathLike
from thoughtspot_tml.tml import Connection
from thoughtspot_tml.tml import Table, View, SQLView, Worksheet
from thoughtspot_tml.tml import Answer, Liveboard, Pinboard


def determine_tml_type(*, info: TMLDocInfo = None, path: PathLike = None) -> Union[Connection, TMLObject]:
    """ """
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
            name, tml_type, ext = path.name.split(".")

    if info is not None:
        tml_type = info["type"]

    if tml_type not in types:
        raise TMLError(f"could not parse TML type from 'info' or 'path', got '{tml_type}'")

    return types[tml_type]
