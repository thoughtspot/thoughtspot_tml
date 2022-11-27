try:
    # AVAILABLE IN PYTHON 3.8
    from typing import get_origin, get_args
    from typing import Literal, TypedDict
    from zipfile import Path as ZipPath
except ImportError:
    from typing_extensions import get_origin, get_args
    from typing_extensions import Literal, TypedDict
    from zipp import Path as ZipPath
