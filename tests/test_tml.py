from thoughtspot_tml.exceptions import TMLExtensionWarning
from thoughtspot_tml import Connection
from thoughtspot_tml import Table, View, SQLView, Worksheet
from thoughtspot_tml import Answer, Liveboard, Pinboard
from ward import test
import warnings

from . import _const


for tml_cls, tml_type_name in (
    (Connection, "connection"),
    (Table, "table"),
    (View, "view"),
    (SQLView, "sql_view"),
    (Worksheet, "worksheet"),
    (Answer, "answer"),
    (Liveboard, "liveboard"),
    (Pinboard, "pinboard"),
):

    @test("{tml_cls.__name__} roundtrips")
    def _(tml_cls=tml_cls, tml_type_name=tml_type_name):
        path = _const.DATA_DIR / f"DUMMY.{tml_type_name}.tml"
        temp = _const.TEMP_DIR / f"DUMMY.{tml_type_name}.tml"
        tml_cls.load(path).dump(temp)
        assert path.read_text() == temp.read_text()

    @test("{tml_cls.__name__} type name is '{tml_type_name}'")
    def _(tml_cls=tml_cls, tml_type_name=tml_type_name):
        path = _const.DATA_DIR / f"DUMMY.{tml_type_name}.tml"
        tml = tml_cls.load(path)
        assert tml.tml_type_name == tml_type_name

    @test("{tml_cls.__name__}.dump warns on non-standard extension (.{tml_type_name}.tml)")
    def _(tml_cls=tml_cls, tml_type_name=tml_type_name):
        path = _const.DATA_DIR / f"DUMMY.{tml_type_name}.tml"
        temp = _const.TEMP_DIR / f"DUMMY.{tml_type_name}.yaml"
        tml = tml_cls.load(path)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            tml.dump(temp)

            assert len(w) == 1
            assert issubclass(w[-1].category, TMLExtensionWarning)
            assert f"saving to '{temp}'" in str(w[-1].message)
