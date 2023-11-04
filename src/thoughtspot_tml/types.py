from __future__ import annotations
from typing import NewType
from typing import Any, Dict, List, Union, Optional, Type

from thoughtspot_tml._compat import Literal, TypedDict, Annotated
from thoughtspot_tml.spotapp import Manifest
from thoughtspot_tml.tml import Table, View, SQLView, Worksheet, Answer, Liveboard


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Reused Types ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TMLObject = Union[Table, View, SQLView, Worksheet, Answer, Liveboard]
TMLObjectType = Type[TMLObject]
TMLDocument = Annotated[str, "a TMLObject represented as a YAML 1.1 document"]
TMLType = Literal["table", "view", "sqlview", "worksheet", "answer", "liveboard", "pinboard"]
GUID = NewType("GUID", str)  # UUID4

class SpotAppInfo(TypedDict):
    tml: List[TMLObject]
    manifest: Optional[Manifest]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ /metadata/tml/export Response Data Structure ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class FileInfo(TypedDict):
    name: str
    filename: str


class StatusCode(TypedDict):
    status: str


class TMLDocInfo(TypedDict):
    name: str
    filename: str
    status: StatusCode
    type: str
    id: GUID
    dependency: List[FileInfo]


class EDocExportResponse(TypedDict):
    info: TMLDocInfo
    edoc: TMLDocument


class EDocExportResponses(TypedDict):
    object: List[EDocExportResponse]


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
    name: Optional[str]
    tables: List[ExternalTable]


class ExternalDatabase(TypedDict):
    name: Optional[str]
    isAutoCreated: bool
    schemas: List[ExternalSchema]


class ConnectionMetadata(TypedDict):
    # for a full list of connection configurations
    #  https://developers.thoughtspot.com/docs/?pageid=connections-api#connection-metadata
    configuration: Dict[str, Any]
    externalDatabases: List[ExternalDatabase]
