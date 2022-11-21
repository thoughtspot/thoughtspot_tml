# thoughtspot_tml

__ThoughtSpot TML__ is a Python package for working with ThoughtSpot Modeling Language (TML) files programmatically.

## Features

 - __Supports__: Connections, [Tables][syntax-table], [Views][syntax-view], [SQLViews][syntax-sqlview], [Worksheets][syntax-worksheet], [Answers][syntax-answer], [Liveboards][syntax-liveboard]
 - Deep attribute access
 - Roundtripping from text or file

*This package will not perform validation of the constructed TML files or interact with your* __ThoughtSpot__ *cluster!*

Please leverage the [ThoughtSpot REST API][rest-api] for this purpose.

## Installation

`thoughtspot_tml` requires at least __Python 3.7__, *preferably* __Python 3.9__ and above.

__Installation is as simple as:__
```shell
pip install thoughtspot-tml
```

## A Simple Functional Example

```python
# worksheet_remapping.py
from thoughtspot_tml import Worksheet
import argparse
import pathlib


def filepath(fp: str) -> pathlib.Path:
    """
    Converts a string to a pathlib.Path.
    """
    path = pathlib.Path(fp)

    if not path.exists():
        raise argparse.ArgumentTypeError(f"path '{fp!r}' does not exist")

    if not path.is_file():
        raise argparse.ArgumentValueError(f"path must be a file, got '{fp!r}'")

    return path


def main():
    # Create a command line application
    #   - argument for a WORKSHEET.worksheet.tml
    #   - options for the "before" and "after" tabling naming conventions
    parser = argparse.ArgumentParser("worksheet")
    parser.add_argument("worksheet_tml", help="a worksheet.tml to remap", type=filepath)
    parser.add_argument("-s", "--src-prefix", metavar="SRC", default="DEV_", type=str, help="(default: %(default)s)")
    parser.add_argument("-d", "--dst-prefix", metavar="DST", default="", type=str, help="(default: %(default)s)")

    # Parse CLI input
    args = parser.parse_args()

    # Read from file
    tml = Worksheet.load(args.worksheet_tml)
    
    # Replace instances of DEV_ with nothing
    for table in tml.worksheet.tables:
        if table.name.startswith(args.source_prefix):
            _, prefix, name = table.name.partition(args.source_prefix)
            table.name = f'{args.target_prefix}{name}'

    # Save to file
    tml.dump(args.worksheet_tml)


if __name__ == '__main__':
    raise SystemExit(main())

```

```shell
>>> python worksheet_remapping.py -h

usage: worksheet [-h] [-s SRC] [-d DST] worksheet_tml

positional arguments:
  worksheet_tml         a worksheet.tml to remap

options:
  -h, --help                show this help message and exit
  -s SRC, --src-prefix SRC  (default: DEV_)
  -d DST, --dst-prefix DST  (default: )
```

More examples can be found in our [/examples directory][examples] in this repository.

## Want to contribute?

We welcome all contributions! :heart: For guidance on setting up a development environment, see our [Contributing Guide][contrib].

[examples]: examples/README.md
[contrib]: .github/CONTRIBUTING.md
[rest-api]: https://developers.thoughtspot.com/docs/?pageid=rest-apis
[syntax-table]: https://docs.thoughtspot.com/cloud/latest/tml#syntax-tables
[syntax-view]: https://docs.thoughtspot.com/cloud/latest/tml#syntax-views
[syntax-sqlview]: https://docs.thoughtspot.com/cloud/latest/tml#syntax-sqlviews
[syntax-worksheet]: https://docs.thoughtspot.com/cloud/latest/tml#syntax-worksheets
[syntax-answer]: https://docs.thoughtspot.com/cloud/latest/tml#syntax-answers
[syntax-liveboard]: https://docs.thoughtspot.com/cloud/latest/tml#syntax-liveboards
