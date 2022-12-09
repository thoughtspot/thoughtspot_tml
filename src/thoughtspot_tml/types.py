from __future__ import annotations
from typing import TYPE_CHECKING, NewType
from typing import Any, Dict, List, Union
import pathlib
import os

from thoughtspot_tml._compat import Literal, TypedDict, ZipPath

if TYPE_CHECKING:
    from thoughtspot_tml.tml import Table, View, SQLView, Worksheet, Answer, Liveboard


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Reused Types ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PathLike = Union[str, os.PathLike, pathlib.Path, ZipPath]
TMLObject = Union["Table", "View", "SQLView", "Worksheet", "Answer", "Liveboard"]
TMLType = Literal["table", "view", "sqlview", "worksheet", "answer", "liveboard", "pinboard"]
GUID = NewType("GUID", str)  # UUID4

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


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ /connection/* Metadata Data Structure ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ExternalColumn(TypedDict):
    name: str
    type: str
    canImport: bool
    selected: bool
    isLinkedActive: bool
    isImported: bool
    tableName: str
    schemaName: str
    dbName: str


class ExternalTable(TypedDict):
    name: str
    type: str
    description: str
    selected: bool
    linked: bool
    columns: List[ExternalColumn]


class ExternalSchema(TypedDict):
    name: str
    tables: List[ExternalTable]


class ExternalDatabase(TypedDict):
    name: str
    isAutoCreated: bool
    schemas: List[ExternalSchema]


class ConnectionMetadata(TypedDict):
    # for a full list of connection configurations
    #  https://developers.thoughtspot.com/docs/?pageid=connections-api#connection-metadata
    configuration: Dict[str, Any]
    externalDatabases: List[ExternalDatabase]
