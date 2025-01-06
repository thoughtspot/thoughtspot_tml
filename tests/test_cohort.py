# ruff: noqa: B018
from __future__ import annotations

from thoughtspot_tml import Cohort
from ward import skip, test

from . import _const

for file in (_const.TESTS_DIR / "data").glob("DUMMY_*cohort.tml"):

    @skip("Not yet released in ThoughtSpot.")
    @test("{file.name} Cohort deep attribute access")
    def _(file=file):
        t = Cohort.load(file)

        assert type(t) is Cohort

        t.guid
        t.cohort
        t.cohort.name
        t.cohort.config
        t.cohort.config.anchor_column.id
        t.cohort.worksheet
        t.cohort.worksheet.name
