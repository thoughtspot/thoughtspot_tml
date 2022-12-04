from dataclasses import dataclass, asdict
import typing
import copy
import uuid

from thoughtspot_tml.types import ConnectionMetadata, GUID
from thoughtspot_tml import _tml, _scriptability, _yaml


@dataclass
class Connection(_tml.TML):
    """
    Representation of a ThoughtSpot System Table TML.
    """

    guid: typing.Optional[GUID]
    connection: _scriptability.ConnectionDoc

    @classmethod
    def _loads(cls, tml_document):
        document = _yaml.load(tml_document)

        if "guid" not in document:
            document = {"guid": None, "connection": document}

        return document

    @classmethod
    def load(cls, path):
        instance = super().load(path)

        try:
            instance.guid = str(uuid.UUID(path.stem, version=4))
        except ValueError:
            pass

        return instance

    def _to_dict(self):
        data = asdict(self)
        return data["connection"]

    def to_rest_api_v1_metadata(self) -> ConnectionMetadata:
        """
        Return a mapping of configuration attributes, as well as database, schema, and table objects.

        The `connection/update` REST API endpoint requires a `metadata` parameter.
        """
        data = {"configuration": {kv.key: kv.value for kv in self.connection.properties}, "externalDatabases": []}
        this_database = {"name": None, "isAutoCreated": False, "schemas": []}
        this_schema = {"name": None, "tables": []}

        # external_databases are nested dict of list of dict.. database -> schema -> table -> columns
        # if we sort first, we can guarantee the insertion order with simple iteration
        for table in sorted(self.connection.table, key=lambda t: (t.external_table.db_name, t.external_table.schema_name)):  # fmt: skip

            # if it's a new schema, append it this database's schema and reset
            if table.external_table.schema_name != this_schema["name"]:
                if this_schema["name"] is not None:
                    this_database["schemas"].append(copy.deepcopy(this_schema))

                this_schema["name"] = table.external_table.schema_name
                this_schema["tables"] = []

            # if it's a new database, append it to response and reset
            if table.external_table.db_name != this_database["name"]:
                if this_database["name"] is not None:
                    data["externalDatabases"].append(copy.deepcopy(this_database))

                this_database["name"] = table.external_table.db_name
                this_database["schemas"] = []

            this_schema["tables"].append(
                {
                    "name": table.external_table.table_name,
                    "type": "TABLE",
                    "description": "",
                    "selected": True,
                    "linked": True,
                    "columns": [
                        {
                            "name": column.external_column,
                            "type": column.data_type,
                            "canImport": True,
                            "selected": True,
                            "isLinkedActive": True,
                            "isImported": False,
                            "dbName": table.external_table.db_name,
                            "schemaName": table.external_table.schema_name,
                            "tableName": table.external_table.table_name,
                        }
                        for column in table.column
                    ],
                }
            )

        # stick the last known data into the response object
        this_database["schemas"].append(copy.deepcopy(this_schema))
        data["externalDatabases"].append(copy.deepcopy(this_database))

        return data


@dataclass
class Table(_tml.TML):
    """
    Representation of a ThoughtSpot System Table TML.
    """

    guid: GUID
    table: _scriptability.LogicalTableEDocProto

    @property
    def name(self) -> str:
        return self.table.name


@dataclass
class View(_tml.TML):
    """
    Representation of a ThoughtSpot View TML.
    """

    guid: GUID
    view: _scriptability.ViewEDocProto

    @property
    def name(self) -> str:
        return self.view.name


@dataclass
class SQLView(_tml.TML):
    """
    Representation of a ThoughtSpot SQLView TML.
    """

    guid: GUID
    sql_view: _scriptability.SqlViewEDocProto

    @property
    def name(self) -> str:
        return self.sql_view.name


@dataclass
class Worksheet(_tml.TML):
    """
    Representation of a ThoughtSpot Worksheet TML.
    """

    guid: GUID
    worksheet: _scriptability.WorksheetEDocProto

    @property
    def name(self) -> str:
        return self.worksheet.name


@dataclass
class Answer(_tml.TML):
    """
    Representation of a ThoughtSpot Answer TML.
    """

    guid: GUID
    answer: _scriptability.AnswerEDocProto

    @property
    def name(self) -> str:
        return self.answer.name


@dataclass
class Liveboard(_tml.TML):
    """
    Representation of a ThoughtSpot Liveboard TML.
    """

    guid: GUID
    liveboard: _scriptability.PinboardEDocProto

    @property
    def name(self) -> str:
        return self.liveboard.name

    @classmethod
    def _loads(cls, tml_document):
        document = _yaml.load(tml_document)

        # @boonhapus, 2022/11/25
        # SCAL-134095 - SpotApp export_associated uses `pinboard` for Liveboard edoc
        if "pinboard" in document:
            document["liveboard"] = document.pop("pinboard")

        return document


@dataclass
class Pinboard(_tml.TML):
    """
    Representation of a ThoughtSpot Pinboard TML.

    DEPRECATED :: https://docs.thoughtspot.com/software/latest/deprecation
      As part of the May 2022 ThoughtSpot release, we rebranded pinboards as Liveboards.
    """

    guid: GUID
    pinboard: _scriptability.PinboardEDocProto

    @property
    def name(self) -> str:
        return self.pinboard.name

    @classmethod
    def _loads(cls, tml_document):
        document = _yaml.load(tml_document)

        # @boonhapus, 2022/11/25
        # SCAL-134095 - SpotApp export_associated uses `pinboard` for Liveboard edoc
        if "liveboard" in document:
            document["pinboard"] = document.pop("liveboard")

        return document
