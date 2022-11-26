from thoughtspot_tml.tml import Connection
from thoughtspot_tml.tml import Table, View, SQLView, Worksheet
from thoughtspot_tml.tml import Answer, Liveboard, Pinboard
from thoughtspot_tml.utils import determine_tml_type
from ward import test, raises

from . import _const


for file, tml_type in (
    (_const.DUMMY_CONNECTION, Connection),
    (_const.DUMMY_TABLE, Table),
    (_const.DUMMY_VIEW, View),
    (_const.DUMMY_SQL_VIEW, SQLView),
    (_const.DUMMY_WORKSHEET, Worksheet),
    (_const.DUMMY_ANSWER, Answer),
    (_const.DUMMY_LIVEBOARD, Liveboard),
    (_const.DUMMY_PINBOARD, Pinboard),
):
    @test("Determine object utility for {intended_type.__name__}")
    def _(file=file, intended_type=tml_type):
        t = determine_tml_type(path=file)
        assert t is intended_type


@test("Object utility requires one of: 'info' or 'filepath'")
def _():

    with raises(TypeError) as exc:
        determine_tml_type()

    assert str(exc.raised) == "determine_tml_type() missing at least 1 required keyword-only argument: 'info' or 'filepath'"
