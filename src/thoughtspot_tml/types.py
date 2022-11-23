from typing import TYPE_CHECKING
from uuid import UUID
import typing
import os

from thoughtspot_tml._compat import Literal, TypedDict

if TYPE_CHECKING:
    from thoughtspot_tml.tml import Table, View, SQLView, Worksheet, Answer, Liveboard


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Reused Types ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PathLike = typing.Union[str, bytes, os.PathLike]
TMLTypes = Literal["table", "view", "sqlview", "worksheet", "answer", "liveboard", "pinboard"]
GUID = UUID

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ /metadata/tml/export Response Data Structure ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class EDocInfo(TypedDict):
    name: str
    filename: str
    status: typing.Dict[str, str]
    type: str
    id: GUID


class EDocExportResponse(TypedDict):
    info: EDocInfo
    edoc: typing.Union["Table", "View", "SQLView", "Worksheet", "Answer", "Liveboard"]
