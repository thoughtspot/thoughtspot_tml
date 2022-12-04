from thoughtspot_tml import Connection
from ward import test

from . import _const


for path in (_const.DUMMY_CONNECTION, _const.DATA_DIR / "connection.yaml"):

    @test("Connection deep attribute access ({path.name})")
    def _(path=path):
        t = Connection.load(path)

        assert type(t) is Connection

        t.guid
        t.connection.name
        t.connection.properties
        t.connection.properties[0].key
        t.connection.table
        t.connection.table[0].id
        t.connection.table[0].external_table
        t.connection.table[0].external_table.db_name
        t.connection.table[0].column
        t.connection.table[0].column[0].external_column


@test("Connection.to_rest_api_v1_metadata")
def _():
    t = Connection.load(_const.DUMMY_CONNECTION)
    d = t.to_rest_api_v1_metadata()

    assert d == {
        "configuration": {
            "accountName": "thoughtspot_partner",
            "user": "PMMUSER",
            "password": "",
            "role": "TS_PMM_RO_ROLE",
            "warehouse": "PMM_WH",
            "database": "PMMDB",
        },
        "externalDatabases": [
            {
                "name": "PMMDB",
                "isAutoCreated": False,
                "schemas": [
                    {
                        "name": "RETAILAPPAREL",
                        "tables": [
                            {
                                "name": "fact_retapp_sales",
                                "type": "TABLE",
                                "description": "",
                                "selected": True,
                                "linked": True,
                                "columns": [
                                    {
                                        "name": "salesid",
                                        "type": "INT64",
                                        "canImport": True,
                                        "selected": True,
                                        "isLinkedActive": True,
                                        "isImported": False,
                                        "dbName": "PMMDB",
                                        "schemaName": "RETAILAPPAREL",
                                        "tableName": "fact_retapp_sales",
                                    },
                                    {
                                        "name": "productid",
                                        "type": "INT64",
                                        "canImport": True,
                                        "selected": True,
                                        "isLinkedActive": True,
                                        "isImported": False,
                                        "dbName": "PMMDB",
                                        "schemaName": "RETAILAPPAREL",
                                        "tableName": "fact_retapp_sales",
                                    },
                                    {
                                        "name": "storeid",
                                        "type": "INT64",
                                        "canImport": True,
                                        "selected": True,
                                        "isLinkedActive": True,
                                        "isImported": False,
                                        "dbName": "PMMDB",
                                        "schemaName": "RETAILAPPAREL",
                                        "tableName": "fact_retapp_sales",
                                    },
                                    {
                                        "name": "quantitypurchased",
                                        "type": "INT64",
                                        "canImport": True,
                                        "selected": True,
                                        "isLinkedActive": True,
                                        "isImported": False,
                                        "dbName": "PMMDB",
                                        "schemaName": "RETAILAPPAREL",
                                        "tableName": "fact_retapp_sales",
                                    },
                                    {
                                        "name": "itemprice",
                                        "type": "DOUBLE",
                                        "canImport": True,
                                        "selected": True,
                                        "isLinkedActive": True,
                                        "isImported": False,
                                        "dbName": "PMMDB",
                                        "schemaName": "RETAILAPPAREL",
                                        "tableName": "fact_retapp_sales",
                                    },
                                    {
                                        "name": "sales",
                                        "type": "DOUBLE",
                                        "canImport": True,
                                        "selected": True,
                                        "isLinkedActive": True,
                                        "isImported": False,
                                        "dbName": "PMMDB",
                                        "schemaName": "RETAILAPPAREL",
                                        "tableName": "fact_retapp_sales",
                                    },
                                    {
                                        "name": "recorddate",
                                        "type": "DATE",
                                        "canImport": True,
                                        "selected": True,
                                        "isLinkedActive": True,
                                        "isImported": False,
                                        "dbName": "PMMDB",
                                        "schemaName": "RETAILAPPAREL",
                                        "tableName": "fact_retapp_sales",
                                    },
                                ],
                            },
                            {
                                "name": "dim_retapp_stores",
                                "type": "TABLE",
                                "description": "",
                                "selected": True,
                                "linked": True,
                                "columns": [
                                    {
                                        "name": "storeid",
                                        "type": "INT64",
                                        "canImport": True,
                                        "selected": True,
                                        "isLinkedActive": True,
                                        "isImported": False,
                                        "dbName": "PMMDB",
                                        "schemaName": "RETAILAPPAREL",
                                        "tableName": "dim_retapp_stores",
                                    },
                                    {
                                        "name": "storename",
                                        "type": "VARCHAR",
                                        "canImport": True,
                                        "selected": True,
                                        "isLinkedActive": True,
                                        "isImported": False,
                                        "dbName": "PMMDB",
                                        "schemaName": "RETAILAPPAREL",
                                        "tableName": "dim_retapp_stores",
                                    },
                                    {
                                        "name": "city",
                                        "type": "VARCHAR",
                                        "canImport": True,
                                        "selected": True,
                                        "isLinkedActive": True,
                                        "isImported": False,
                                        "dbName": "PMMDB",
                                        "schemaName": "RETAILAPPAREL",
                                        "tableName": "dim_retapp_stores",
                                    },
                                    {
                                        "name": "state",
                                        "type": "VARCHAR",
                                        "canImport": True,
                                        "selected": True,
                                        "isLinkedActive": True,
                                        "isImported": False,
                                        "dbName": "PMMDB",
                                        "schemaName": "RETAILAPPAREL",
                                        "tableName": "dim_retapp_stores",
                                    },
                                    {
                                        "name": "zipcode",
                                        "type": "VARCHAR",
                                        "canImport": True,
                                        "selected": True,
                                        "isLinkedActive": True,
                                        "isImported": False,
                                        "dbName": "PMMDB",
                                        "schemaName": "RETAILAPPAREL",
                                        "tableName": "dim_retapp_stores",
                                    },
                                    {
                                        "name": "county",
                                        "type": "VARCHAR",
                                        "canImport": True,
                                        "selected": True,
                                        "isLinkedActive": True,
                                        "isImported": False,
                                        "dbName": "PMMDB",
                                        "schemaName": "RETAILAPPAREL",
                                        "tableName": "dim_retapp_stores",
                                    },
                                    {
                                        "name": "latitude",
                                        "type": "DOUBLE",
                                        "canImport": True,
                                        "selected": True,
                                        "isLinkedActive": True,
                                        "isImported": False,
                                        "dbName": "PMMDB",
                                        "schemaName": "RETAILAPPAREL",
                                        "tableName": "dim_retapp_stores",
                                    },
                                    {
                                        "name": "longitude",
                                        "type": "DOUBLE",
                                        "canImport": True,
                                        "selected": True,
                                        "isLinkedActive": True,
                                        "isImported": False,
                                        "dbName": "PMMDB",
                                        "schemaName": "RETAILAPPAREL",
                                        "tableName": "dim_retapp_stores",
                                    },
                                    {
                                        "name": "region",
                                        "type": "VARCHAR",
                                        "canImport": True,
                                        "selected": True,
                                        "isLinkedActive": True,
                                        "isImported": False,
                                        "dbName": "PMMDB",
                                        "schemaName": "RETAILAPPAREL",
                                        "tableName": "dim_retapp_stores",
                                    },
                                ],
                            },
                            {
                                "name": "dim_retapp_products",
                                "type": "TABLE",
                                "description": "",
                                "selected": True,
                                "linked": True,
                                "columns": [
                                    {
                                        "name": "productid",
                                        "type": "INT64",
                                        "canImport": True,
                                        "selected": True,
                                        "isLinkedActive": True,
                                        "isImported": False,
                                        "dbName": "PMMDB",
                                        "schemaName": "RETAILAPPAREL",
                                        "tableName": "dim_retapp_products",
                                    },
                                    {
                                        "name": "productname",
                                        "type": "VARCHAR",
                                        "canImport": True,
                                        "selected": True,
                                        "isLinkedActive": True,
                                        "isImported": False,
                                        "dbName": "PMMDB",
                                        "schemaName": "RETAILAPPAREL",
                                        "tableName": "dim_retapp_products",
                                    },
                                    {
                                        "name": "producttype",
                                        "type": "VARCHAR",
                                        "canImport": True,
                                        "selected": True,
                                        "isLinkedActive": True,
                                        "isImported": False,
                                        "dbName": "PMMDB",
                                        "schemaName": "RETAILAPPAREL",
                                        "tableName": "dim_retapp_products",
                                    },
                                ],
                            },
                        ],
                    }
                ],
            }
        ],
    }
