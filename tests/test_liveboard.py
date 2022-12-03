from thoughtspot_tml import Liveboard
from ward import test

from . import _const


@test("Liveboard deep attribute access")
def _():
    t = Liveboard.load(_const.DUMMY_LIVEBOARD)

    assert type(t) is Liveboard

    t.guid
    t.liveboard
    t.liveboard.name
    t.liveboard.visualizations
    t.liveboard.visualizations[0].viz_guid
    t.liveboard.visualizations[0].answer.search_query
    t.liveboard.visualizations[0].answer.tables[0].name
    t.liveboard.visualizations[0].answer.answer_columns[0].name
