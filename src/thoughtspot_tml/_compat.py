import sys

if sys.version_info < (3, 8):
    from typing_extensions import get_origin, get_args
    from typing_extensions import Literal, TypedDict
else:
    # AVAILABLE IN PYTHON 3.8
    from typing import get_origin, get_args
    from typing import Literal, TypedDict

if sys.version_info < (3, 9):
    from typing_extensions import Annotated
else:
    from typing import Annotated

if sys.version_info < (3, 10):
    # https://bugs.python.org/issue40564#msg377884
    # :: zipfile.Path with several files prematurely closes zip
    # => Use zipp 3.2.0 on Python 3.9 and earlier for the improved behavior
    from zipp import Path as ZipPath
else:
    # AVAILABLE IN PYTHON 3.8
    from zipfile import Path as ZipPath
