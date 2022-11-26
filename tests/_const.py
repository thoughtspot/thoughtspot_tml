import pathlib


TESTS_DIR = pathlib.Path(__file__).parent

DUMMY_CONNECTION = TESTS_DIR / "data" / "DUMMY.yaml"
DUMMY_TABLE = TESTS_DIR / "data" / "DUMMY.table.tml"
DUMMY_VIEW = TESTS_DIR / "data" / "DUMMY.view.tml"
DUMMY_SQL_VIEW = TESTS_DIR / "data" / "DUMMY.sqlview.tml"
DUMMY_WORKSHEET = TESTS_DIR / "data" / "DUMMY.worksheet.tml"
DUMMY_ANSWER = TESTS_DIR / "data" / "DUMMY.answer.tml"
DUMMY_PINBOARD = TESTS_DIR / "data" / "DUMMY.pinboard.tml"
DUMMY_LIVEBOARD = TESTS_DIR / "data" / "DUMMY.liveboard.tml"
DUMMY_SPOTAPP = TESTS_DIR / "data" / "DUMMY_spot_app.zip"
