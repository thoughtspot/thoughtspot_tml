from thoughtspot_tml import Worksheet
from ward import test

from . import _const


for version, file in (("V1", _const.DUMMY_WORKSHEET), ("V2", _const.DUMMY_MODEL)):

    @test("Worksheet {version} deep attribute access")
    def _(file=file, version=version):
        t = Worksheet.load(file)

        assert type(t) is Worksheet

        t.guid
        t.worksheet
        t.worksheet.formulas
        t.worksheet.formulas[0].expr
        t.worksheet.worksheet_columns
        t.worksheet.worksheet_columns[0].properties
        t.worksheet.worksheet_columns[0].properties.index_type
        t.worksheet.properties
        t.worksheet.properties.is_bypass_rls

        if version == "V1":
            assert t.is_model is False
            t.worksheet.tables
            t.worksheet.tables[0].name
            t.worksheet.joins
            t.worksheet.joins[0].type
            t.worksheet.table_paths
            t.worksheet.table_paths[0].table
            t.worksheet.table_paths[0].join_path
            t.worksheet.table_paths[0].join_path[0].join

        if version == "V2":
            assert t.is_model is True
            t.worksheet.schema
            t.worksheet.schema.tables
            t.worksheet.schema.tables[0].name
            t.worksheet.schema.tables[0].alias
