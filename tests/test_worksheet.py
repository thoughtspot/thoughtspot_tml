from thoughtspot_tml import Worksheet
from ward import test

from . import _const


@test("Worksheet deep attribute access")
def _():
    t = Worksheet.load(_const.DUMMY_WORKSHEET)

    assert type(t) is Worksheet

    t.guid
    t.worksheet
    t.worksheet.tables
    t.worksheet.tables[0].name
    t.worksheet.joins
    t.worksheet.joins[0].type
    t.worksheet.table_paths
    t.worksheet.table_paths[0].table
    t.worksheet.table_paths[0].join_path
    t.worksheet.table_paths[0].join_path[0].join
    t.worksheet.formulas
    t.worksheet.formulas[0].expr
    t.worksheet.worksheet_columns
    t.worksheet.worksheet_columns[0].properties
    t.worksheet.worksheet_columns[0].properties.index_type
    t.worksheet.properties
    t.worksheet.properties.is_bypass_rls


@test("Worksheet roundtrips")
def _():
    before_t = _const.DUMMY_WORKSHEET.read_text()
    t = Worksheet.loads(before_t)
    after_t = t.dumps()

    assert type(before_t) is str
    assert type(t) is Worksheet
    assert type(after_t) is str
    assert before_t == after_t
