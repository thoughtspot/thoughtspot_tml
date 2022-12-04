import pathlib

# fmt: off
TESTS_DIR = pathlib.Path(__file__).parent
DATA_DIR  = pathlib.Path(__file__).parent / "data"
TEMP_DIR  = pathlib.Path(__file__).parent / "data" / "_temp"
# fmt: on

DUMMY_CONNECTION = DATA_DIR / "DUMMY.connection.tml"
DUMMY_TABLE = DATA_DIR / "DUMMY.table.tml"
DUMMY_VIEW = DATA_DIR / "DUMMY.view.tml"
DUMMY_SQL_VIEW = DATA_DIR / "DUMMY.sql_view.tml"
DUMMY_WORKSHEET = DATA_DIR / "DUMMY.worksheet.tml"
DUMMY_ANSWER = DATA_DIR / "DUMMY.answer.tml"
DUMMY_PINBOARD = DATA_DIR / "DUMMY.pinboard.tml"
DUMMY_LIVEBOARD = DATA_DIR / "DUMMY.liveboard.tml"
DUMMY_SPOTAPP = DATA_DIR / "DUMMY_spot_app.zip"
