from thoughtspot_tml import Table
from ward import test

from . import _const


@test("Table deep attribute access")
def _():
    t = Table.load(_const.DUMMY_TABLE)

    assert type(t) is Table

    t.guid
    t.table
    t.table.db_table
    t.table.columns
    t.table.columns[0].properties
    t.table.columns[0].properties.index_type
    t.table.joins_with
    t.table.joins_with[0].destination
    t.table.joins_with[0].destination.name


@test("Table roundtrips")
def _():
    before_t = _const.DUMMY_TABLE.read_text()
    t = Table.loads(before_t)
    after_t = t.dumps()

    assert type(before_t) is str
    assert type(t) is Table
    assert type(after_t) is str
    assert before_t == after_t
