from thoughtspot_tml import Connection
from ward import test

from . import _const


@test("Connection deep attribute access")
def _():
    t = Connection.load(_const.TESTS_DIR / "data" / "connection.yaml")

    assert type(t) is Connection

    t.name
    t.properties
    t.properties[0].key
    t.table
    t.table[0].id
    t.table[0].external_table
    t.table[0].external_table.db_name
    t.table[0].column
    t.table[0].column[0].external_column


@test("Connection roundtrips")
def _():
    before_t = (_const.TESTS_DIR / "data" / "connection.yaml").read_text()
    t = Connection.loads(before_t)
    after_t = t.dumps()

    assert type(before_t) is str
    assert type(t) is Connection
    assert type(after_t) is str
    assert before_t == after_t
