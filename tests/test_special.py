from thoughtspot_tml.utils import determine_tml_type
from ward import test

from . import _const


for file in (_const.TESTS_DIR / "data").glob("SPECIAL_*"):

    @test("Special TML parsing: {file.name}")
    def _(file=file):
        tml_cls = determine_tml_type(path=file)
        tml = tml_cls.load(file)
        assert type(tml) is tml_cls
