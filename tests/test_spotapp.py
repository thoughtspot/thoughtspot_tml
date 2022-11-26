import tempfile
import zipfile

from thoughtspot_tml.spotapp import SpotApp
from ward import test

from . import _const


@test("SpotApp read")
def _():
    s = SpotApp.read(_const.DUMMY_SPOTAPP)

    assert s.manifest is not None
    assert len(s.tml) > 0


@test("SpotApp save")
def _():
    s = SpotApp.read(_const.DUMMY_SPOTAPP)

    assert len(s.tml) > 0

    with tempfile.NamedTemporaryFile() as f:
        s.save(f)

        assert zipfile.is_zipfile(f) is True


@test("SpotApp TML access")
def _():
    s = SpotApp.read(_const.DUMMY_SPOTAPP)

    assert s.manifest is not None
    assert len(s.tml) == 5
    assert len(s.tables) == 3
    assert len(s.views) == 0
    assert len(s.sql_views) == 0
    assert len(s.worksheets) == 1
    assert len(s.answers) == 0
    assert len(s.liveboards) == 1
