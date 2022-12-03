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
