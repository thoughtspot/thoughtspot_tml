from __future__ import annotations

from thoughtspot_tml import Model
from ward import test

from . import _const

for file in (_const.DUMMY_MODEL_GA,):

    @test("Model deep attribute access")
    def _(file=file):
        t = Model.load(file)

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
