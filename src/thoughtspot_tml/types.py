from typing import TYPE_CHECKING
from typing import Dict, List, Union
from uuid import UUID
import pathlib
import os

from thoughtspot_tml._compat import Literal, TypedDict, ZipPath

if TYPE_CHECKING:
    from thoughtspot_tml.tml import Table, View, SQLView, Worksheet, Answer, Liveboard


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Reused Types ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PathLike = Union[str, bytes, os.PathLike, pathlib.Path, ZipPath]
TMLObject = Union["Table", "View", "SQLView", "Worksheet", "Answer", "Liveboard"]
TMLType = Literal["table", "view", "sqlview", "worksheet", "answer", "liveboard", "pinboard"]
GUID = UUID

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ /metadata/tml/export Response Data Structure ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class FileInfo(TypedDict):
    name: str
    filename: str


class TMLDocInfo(TypedDict):
    name: str
    filename: str
    status: Dict[Literal["status"], str]
    type: str
    id: GUID
    dependency: List[FileInfo]


class EDocExportResponse(TypedDict):
    info: TMLDocInfo
    edoc: TMLObject
