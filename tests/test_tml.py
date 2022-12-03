from thoughtspot_tml.exceptions import TMLExtensionWarning
from thoughtspot_tml import Connection
from thoughtspot_tml import Table, View, SQLView, Worksheet
from thoughtspot_tml import Answer, Liveboard, Pinboard
from ward import test
import warnings

from . import _const


for tml_cls in (Connection, Table, View, SQLView, Worksheet, Answer, Liveboard, Pinboard):
    tml_type = tml_cls.__name__.lower()

    @test("{tml_cls.__name__} rountrips")
    def _(tml_cls=tml_cls, tml_type=tml_type):
        path = _const.DATA_DIR / f"DUMMY.{tml_type}.tml"
        temp = _const.TEMP_DIR / f"DUMMY.{tml_type}.tml"
        tml_cls.load(path).dump(temp)
        assert path.read_text() == temp.read_text()

    @test("{tml_cls.__name__}.dump warns on non-standard extension (.{tml_type}.tml)")
    def _(tml_cls=tml_cls, tml_type=tml_type):
        path = _const.DATA_DIR / f"DUMMY.{tml_type}.tml"
        temp = _const.TEMP_DIR / f"DUMMY.{tml_type}.yaml"
        tml = tml_cls.load(path)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            tml.dump(temp)

            assert len(w) == 1
            assert issubclass(w[-1].category, TMLExtensionWarning)
            assert f"saving to '{temp}'" in str(w[-1].message)
