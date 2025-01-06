# ruff: noqa: B018
from __future__ import annotations

import warnings

from thoughtspot_tml import Liveboard, exceptions
from ward import test, xfail

from . import _const


@xfail("xfail until we move to pytest, ward has no way to test warnings")
@test("Importing Pinboard flashes DeprecrationWarning")
def _():
    with warnings.catch_warnings(record=True) as w:
        assert len(w) == 0

        assert len(w) == 1
        assert issubclass(w[0].category, exceptions.TMLDeprecationWarning)


@test("Pinboard deep attribute access")
def _():
    t = Liveboard.load(_const.DUMMY_PINBOARD)

    assert type(t) is Liveboard

    t.guid
    t.liveboard
    t.liveboard.name
    t.liveboard.visualizations
    t.liveboard.visualizations[0].viz_guid
    t.liveboard.visualizations[0].answer.search_query
    t.liveboard.visualizations[0].answer.tables[0].name
    t.liveboard.visualizations[0].answer.answer_columns[0].name
