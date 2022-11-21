from thoughtspot_tml import Answer
from ward import test

from . import _const


@test("Answer deep attribute access")
def _():
    t = Answer.load(_const.DUMMY_ANSWER)

    assert type(t) is Answer

    t.guid
    t.answer
    t.answer.name
    t.answer.tables
    t.answer.tables[0].name
    t.answer.search_query
    t.answer.answer_columns
    t.answer.answer_columns[0].name


@test("Answer roundtrips")
def _():
    before_t = _const.DUMMY_ANSWER.read_text()
    t = Answer.loads(before_t)
    after_t = t.dumps()

    assert type(before_t) is str
    assert type(t) is Answer
    assert type(after_t) is str
    assert before_t == after_t
