from thoughtspot_tml import SQLView
from ward import test

from . import _const


@test("SQLView deep attribute access")
def _():
    t = SQLView.load(_const.DUMMY_SQL_VIEW)

    assert type(t) is SQLView

    t.guid
    t.sql_view
    t.sql_view.connection
    t.sql_view.connection.fqn
    t.sql_view.joins_with[0]
    t.sql_view.joins_with[0].destination
    t.sql_view.joins_with[0].on


@test("SQLView roundtrips")
def _():
    before_t = _const.DUMMY_SQL_VIEW.read_text()
    t = SQLView.loads(before_t)
    after_t = t.dumps()

    assert type(before_t) is str
    assert type(t) is SQLView
    assert type(after_t) is str
    assert before_t == after_t
