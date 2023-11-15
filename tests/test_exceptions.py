from thoughtspot_tml.exceptions import TMLDecodeError
from thoughtspot_tml import Answer
from ward import test, raises

from . import _const


@test("TMLDecodeError on text input")
def _():
    with raises(TMLDecodeError) as exc:
        Answer.loads(tml_document="😅: INVALID")

    assert "supplied data does not produce a valid TML (Answer) document" in str(exc.raised)


@test("TMLDecodeError on invalid file input")
def _():
    fp = _const.TESTS_DIR / "data" / "BAD_DUMMY.answer.tml"

    with raises(TMLDecodeError) as exc:
        Answer.load(path=fp)

    assert "is not a valid TML (Answer) file" in str(exc.raised)
    assert "syntax error on line 2, around column 9" in str(exc.raised)
