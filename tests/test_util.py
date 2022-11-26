from thoughtspot_tml.exceptions import TMLError
from thoughtspot_tml.utils import determine_tml_type
from thoughtspot_tml.tml import Connection
from thoughtspot_tml.tml import Table, View, SQLView, Worksheet
from thoughtspot_tml.tml import Answer, Liveboard, Pinboard
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


@test("Object errors on unknown type")
def _():
    bad_type = "dashboard"

    with raises(TMLError) as exc:
        determine_tml_type(info={"type": bad_type})

    assert str(exc.raised) == f"could not parse TML type from 'info' or 'path', got '{bad_type}'"


@test("Object utility requires one of: 'info' or 'path'")
def _():

    with raises(TypeError) as exc:
        determine_tml_type()

    assert str(exc.raised) == "determine_tml_type() missing at least 1 required keyword-only argument: 'info' or 'path'"
