from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, Any
import copy
import json
import uuid
import warnings

from thoughtspot_tml import _compat, _scriptability, _tml, _yaml, exceptions

if TYPE_CHECKING:
    from typing import Optional
    import pathlib

    from thoughtspot_tml.types import (
        GUID,
        ConnectionMetadata,
        ExternalDatabase,
        ExternalSchema,
    )


@dataclass
class Connection(_tml.TML):
    """
    Representation of a ThoughtSpot System Table TML.
    """

    guid: Optional[GUID]
    connection: _scriptability.ConnectionDoc

    @property
    def name(self) -> str:
        return self.connection.name

    @classmethod
    def _loads(cls, tml_document: str) -> dict[str, Any]:
        # Handle backwards incompatible changes.
        document = _yaml.load(tml_document)

        # DEV NOTE: @boonhapus, 2024/02/14
        # Old connections do not offer a TML component, so we'll fake it.
        if "guid" not in document:
            document = {"guid": None, "connection": document}

        return document

    @classmethod
    def load(cls, path: pathlib.Path) -> _compat.Self:
        # Handle backwards incompatible changes.
        instance = super().load(path)

        # DEV NOTE: @boonhapus, 2024/02/14
        # Old connections do not offer a TML component, so we'll fake it.
        # The convention that follows is that the pathname contains the connection guid.
        try:
            name, _, ext = path.name.partition(".")
            instance.guid = str(uuid.UUID(name, version=4))
        except ValueError:
            pass

        return instance

    def _to_dict(self):
        data = asdict(self)

        # DEV NOTE: @boonhapus, 2024/02/14
        # Old connections do not offer a TML component, so we'll fake it.
        if self.guid is None:
            data = data["connection"]

        return data

    def to_rest_api_v1_metadata(self) -> ConnectionMetadata:
        """
        Return a mapping of configuration attributes, as well as database, schema, and table objects.

        The `connection/update` REST API endpoint requires a `metadata` parameter.
        """
        data: ConnectionMetadata = {
            "configuration": {kv.key: kv.value for kv in self.connection.properties},
            "externalDatabases": [],
        }
        this_database: ExternalDatabase = {
            "name": None,
            "isAutoCreated": False,
            "schemas": [],
        }
        this_schema: ExternalSchema = {"name": None, "tables": []}

        # this connection has 0 tables (very popular "initial state" structure TS 9.0.0+)
        if self.connection.table is None:
            return data

        # external_databases are nested dict of list of dict.. database -> schema -> table -> columns
        # if we sort first, we can guarantee the insertion order with simple iteration
        for table in sorted(
            self.connection.table,
            key=lambda t: (t.external_table.db_name, t.external_table.schema_name),
        ):
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
                },
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

    @classmethod
    def loads(cls, tml_document: str) -> _compat.Self:
        """
        Deserialize a TML document to a Python object.

        Parameters
        ----------
        tml_document : str
          text to parse into a TML object

        Raises
        ------
        TMLDecodeError, when the document string cannot be parsed or receives extra data
        """
        # DEV NOTE: @boonhapus, 2024/08/01
        # Models have been standardized into thier own object types, if a worksheet
        # include the python-reserved word "with:", then it's a V1.5 worksheet and
        # we'll return a model instead.
        if "with:" in tml_document:
            warnings.warn(
                "Detected Worksheet V1.5, returning a Model instead of Worksheet.",
                exceptions.TMLDeprecationWarning,
                stacklevel=2,
            )

            tml_document = tml_document.replace("worksheet:", "model:")
            return Model.loads(tml_document)  # type: ignore[return-value]

        return super().loads(tml_document)


@dataclass
class Model(_tml.TML):
    """
    Representation of a ThoughtSpot Model TML.
    """

    guid: GUID
    model: _scriptability.WorksheetEDocProto

    @property
    def name(self) -> str:
        return self.model.name

    @classmethod
    def _loads(cls, tml_document: str) -> dict[str, Any]:
        # DEV NOTE: @boonhapus, 2024/02/14
        # The Worksheet V2 update include a python reserved word in the spec, which
        # python-betterproto automatically adds a trailing sunder to. This reverses it.
        if "with:" in tml_document:
            tml_document = tml_document.replace("- with:", "- with_:")

        return _yaml.load(tml_document)

    def _to_dict(self) -> dict[str, Any]:
        # DEV NOTE: @boonhapus, 2024/02/14
        # The Worksheet V2 update include a python reserved word in the spec, which
        # python-betterproto automatically adds a trailing sunder to. This reverses it.
        data = asdict(self)
        text = json.dumps(data)
        text = text.replace('"with_"', '"with"')
        data = json.loads(text)

        return data


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
        # @boonhapus, 2022/11/25
        # SCAL-134095 - SpotApp export_associated uses `pinboard` for Liveboard edoc
        if "pinboard:" in tml_document:
            tml_document = tml_document.replace("pinboard:", "liveboard:")

        return _yaml.load(tml_document)


@dataclass
class Cohort(_tml.TML):
    """
    Representation of a ThoughtSpot Cohort TML.
    """

    guid: GUID
    cohort: _scriptability.CohortEDocProto

    @property
    def name(self) -> str:
        return self.cohort.name

    @property
    def is_column_set(self) -> bool:
        """Determines if the COHORT is a ColumnSet."""
        return self.cohort.config.cohort_type == _scriptability.CohortTypeE.SIMPLE

    @property
    def is_query_set(self) -> bool:
        """Determines if the COHORT is a QuerySet."""
        return self.cohort.config.cohort_type == _scriptability.CohortTypeE.ADVANCED


def __getattr__(name: str) -> Any:
    # DEPRECATED :: https://docs.thoughtspot.com/software/latest/deprecation
    #   As part of the May 2022 ThoughtSpot release, we rebranded pinboards as Liveboards.
    if name == "Pinboard":
        warnings.warn(
            "ThoughtSpot deprecated 'Pinboard' in May 2022, use 'Liveboard' instead.",
            exceptions.TMLDeprecationWarning,
            stacklevel=2,
        )
        return Liveboard

    raise AttributeError(f"module 'thoughtspot_tml' has no attribute '{name}'")
