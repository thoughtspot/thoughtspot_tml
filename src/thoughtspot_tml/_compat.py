import sys

import yaml


try:
    Dumper = yaml.CDumper
    Loader = yaml.CSafeLoader
except AttributeError:
    Dumper = yaml.Dumper
    Loader = yaml.SafeLoader

if sys.version_info < (3, 10):
    # https://bugs.python.org/issue40564#msg377884
    # :: zipfile.Path with several files prematurely closes zip
    # => Use zipp 3.2.0 on Python 3.9 and earlier for the improved behavior
    from zipp import Path as ZipPath
else:
    # AVAILABLE IN PYTHON 3.8
    from zipfile import Path as ZipPath

if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self
