from thoughtspot_tml import Pinboard
from ward import test

from . import _const


@test("Pinboard deep attribute access")
def _():
    t = Pinboard.load(_const.DUMMY_PINBOARD)

    assert type(t) is Pinboard

    t.guid
    t.pinboard
    t.pinboard.name
    t.pinboard.visualizations
    t.pinboard.visualizations[0].viz_guid
    t.pinboard.visualizations[0].answer.search_query
    t.pinboard.visualizations[0].answer.tables[0].name
    t.pinboard.visualizations[0].answer.answer_columns[0].name
