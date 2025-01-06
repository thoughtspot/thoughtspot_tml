# ruff: noqa: B018
from __future__ import annotations

from thoughtspot_tml import Model
from ward import test

from . import _const


@test("Model deep attribute access")
def _():
    t = Model.load(_const.DUMMY_MODEL_GA)

    assert type(t) is Model

    t.guid
    t.model
    t.model.formulas
    t.model.columns
    t.model.columns[0].properties
    t.model.columns[0].properties.column_type
    t.model.columns[0].properties.index_type
    t.model.properties
    t.model.properties.is_bypass_rls
    t.model.model_tables
