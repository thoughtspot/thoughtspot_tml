from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Literal, TypedDict, Union

from thoughtspot_tml import TML, Answer, Cohort, Liveboard, Model, SQLView, Table, View, Worksheet

if TYPE_CHECKING:
    from typing import Any, Optional

    from thoughtspot_tml.spotapp import Manifest


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Reused Types ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TMLObject = Union[Table, View, SQLView, Worksheet, Answer, Liveboard, Cohort, Model, TML]
TMLObjectType = type[TMLObject]
TMLType = Literal["table", "view", "sqlview", "worksheet", "answer", "liveboard", "pinboard", "cohort", "model"]
TMLDocument = Annotated[str, "a TMLObject represented as a YAML 1.1 document"]
GUID = Annotated[str, "A globally unique ID represented as a stringified UUID4"]


class SpotAppInfo(TypedDict):
    tml: list[TMLObject]
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
    dependency: list[FileInfo]


class EDocExportResponse(TypedDict):
    info: TMLDocInfo
    edoc: TMLDocument


class EDocExportResponses(TypedDict):
    object: list[EDocExportResponse]


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
    columns: list[ExternalColumn]


class ExternalSchema(TypedDict):
    name: Optional[str]
    tables: list[ExternalTable]


class ExternalDatabase(TypedDict):
    name: Optional[str]
    isAutoCreated: bool
    schemas: list[ExternalSchema]


class ConnectionMetadata(TypedDict):
    # for a full list of connection configurations
    #  https://developers.thoughtspot.com/docs/?pageid=connections-api#connection-metadata
    configuration: dict[str, Any]
    externalDatabases: list[ExternalDatabase]
