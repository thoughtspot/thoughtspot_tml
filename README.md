<div align="center">
  <h2><b>ThoughtSpot TML</b></h2>

  <i>a Python package for working with</i> <b>ThoughtSpot</b> <i>Modeling Language (TML) files programmatically.</i>

  <h3>
    <a href="#installation">Installation</a>
    <span> | </span>
    <a href="#a-basic-example">Example</a>
    <span> | </span>
    <a href="#migration-to-v130">Migration to v1.3.0</a>
    <span> | </span>
    <a href="#thoughtspot_tml-reference">Reference</a>
    <span> | </span>
    <a href="#notes-on-thoughtspot-modeling-language">Notes</a>
  </h3>
</div>

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

## A Basic Example

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
    parser = argparse.ArgumentParser()
    parser.add_argument("worksheet_tml", help="a worksheet.tml to remap", type=filepath)
    parser.add_argument("-s", "--src-prefix", metavar="SRC", default="DEV_", type=str, help="(default: %(default)s)")
    parser.add_argument("-d", "--dst-prefix", metavar="DST", default="TEST_", type=str, help="(default: %(default)s)")

    # Parse CLI input
    args = parser.parse_args()

    # Read from file
    tml = Worksheet.load(args.worksheet_tml)
    
    # Replace instances of DEV_ with TEST_
    for table in tml.worksheet.tables:
        table.name = table.name.replace(args.src_prefix, args.dst_prefix)

    # Save to file
    tml.dump(args.worksheet_tml)


if __name__ == '__main__':
    raise SystemExit(main())

```

```shell
>>> python worksheet_remapping.py -h

usage: [-h] [-s SRC] [-d DST] worksheet_tml

positional arguments:
  worksheet_tml         a worksheet.tml to remap

options:
  -h, --help                show this help message and exit
  -s SRC, --src-prefix SRC  (default: DEV_)
  -d DST, --dst-prefix DST  (default: TEST_)
```

A more complex version of this example, as well as more examples can be found in the [/examples directory][examples] in this repository.

## `thoughtspot_tml` Reference

<h5>
  <a href="#tml-objects">TML Objects</a>
  <span> | </span>
  <a href="#deserialization">Deserialization</a>
  <span> | </span>
  <a href="#serialization">Serialization</a>
  <span> | </span>
  <a href="#spotapp">SpotApp</a>
  <span> | </span>
  <a href="#utilities">Utilities</a>
</h5>

### TML Objects
```python
from thoughtspot_tml import Table, View, SQLView, Worksheet
from thoughtspot_tml import Answer, Liveboard, Pinboard

# aliases
from thoughtspot_tml import ThoughtSpotView    # View
from thoughtspot_tml import SavedAnswer        # Answer
from thoughtspot_tml import SystemTable        # Table
```

Each TML object takes the form of a top-level attribute for the globally unique identifier, or `GUID`, as well as the document form of the object it represents. This identically mirrors the TML specification you can find [in the __ThoughtSpot__ documentation][syntax-tml]. In addition, the `name` attribute of the TML document itself has been pulled into the top-level namespace.

```python
@dataclass
class Worksheet(TML):
    """
    Representation of a ThoughtSpot Worksheet TML.
    """

    guid: GUID
    worksheet: WorksheetEDocProto

    @property
    def name(self) -> str:
        return self.worksheet.name
```

---

The `Connection` is a special type of TML object. Connections (also known as "Embrace" Connections), were implemented prior to the TML spec being officially released. The `remapping.yaml` obtained from your platform (`Data > Connections > (...) in the top right > Remapping > Download`) defines how __ThoughtSpot__ table objects relate to the external data source.

```python
from thoughtspot_tml import Connection

# aliases
from thoughtspot_tml import EmbraceConnection  # Connection
```

The connection takes on a different form, but still contains other common TML methods.

```python
@dataclass
class Connection(TML):
    """
    Representation of a ThoughtSpot Connection YAML.
    """

    name: str
    type: str
    authentication_type: str
    properties: list[KeyValueStr]
    table: list[ConnectionDocTableDoc]
```

Each object contains multiple methods for serialization and deserialization.

### __Deserialization__

For deserialization of a TML document into a python object.

```python
ws = Worksheet.load(path: PathLike = "tests/data/DUMMY.worksheet.tml")
ws = Worksheet.loads(tml_document: str = ...)  # can be obtained from the ThoughtSpot REST API

ws.guid == "2ea7add9-0ccb-4ac1-90bb-231794ebb377"
```

`.load` a worksheet from a `.worksheet.tml` file, or as a string directly from the [`metadata/tml/export`][rest-api-export] API with `.loads`.

---

### __Serialization__

For serialization of a TML python object back into data.

```python
data = ws.to_dict()
data["guid"] == "2ea7add9-0ccb-4ac1-90bb-231794ebb377"

ws.dump(path="tests/data/DUMMY.worksheet.tml")
# DUMMY.worksheet.tml
#
# guid: 2ea7add9-0ccb-4ac1-90bb-231794ebb377
# worksheet:
#   ...

data_s = ws.dumps(format_type="YAML")
data = yaml.load(data_s)
data["guid"] == "2ea7add9-0ccb-4ac1-90bb-231794ebb377"

# -or-

data = ws.dumps(format_type="JSON")
data_s = json.loads(data_s)
data["guid"] == "2ea7add9-0ccb-4ac1-90bb-231794ebb377"
```

`.to_dict` to convert the entire object tree into python native types, or write back to a file with `.dump` as a TML-formatted string. The formatting can be overriden to JSON if the JSON file type is used (`.worksheet.json`). `.dumps` allows access to the formatted string directly, typically used as input for the [`metadata/tml/import`][rest-api-import] API.

### SpotApp

```python
from thoughtspot_tml import SpotApp
```

SpotApps are bundles of TML which can be obtained directly from the __ThoughtSpot__ user interace as a zip file archive, or from the `/metadata/tml/export` API endpoint using the `export_associated = true` query parameter.


```python
export_response = ...  # /metadata/tml/export
s = SpotApp.from_api(export_response)
print(s.tml)

# -or-

s = SpotApp.read("tests/data/DUMMY.worksheet.tml")
print(s.tml)  # => [Worksheet(...), Table(...), Table(...)]
print(s.manifest)  # => Manifest(...)
```

SpotApps can also be saved to a new zipfile archive through the `.save` method.

```python
s = SpotApp.read("tests/data/DUMMY.worksheet.tml")
s.save("tests/data/NEW_DUMMY.worksheet.tml")
```

### Utilities

```python
from thoughtspot_tml.utils import determine_tml_type

tml_type = determine_tml_type(path="/tests/data/DUMMY.worksheet.tml")
tml = tml_type.load(path="/tests/data/DUMMY.worksheet.tml")
type(tml) is Worksheet

# -or-

export_response = ...  # /metadata/tml/export
tml_type = determine_tml_type(info=export_response["object"][0]["info"])
tml = tml_type.loads(tml_document=export_response["object"][0]["edoc"])
type(tml) is Worksheet
```

## Migration to v1.3.0

**Lorem ipsum**

## Notes on __ThoughtSpot Modeling Language__

- TML is implemented in the YAML 1.1 spec.
- When importing a TML file, if the `guid` matches to an existing object, then that object will be updated. If the `guid` is missing or does not match an object, a new object is created with a new GUID.

## Want to contribute?

We welcome all help! :heart: For guidance on setting up a development environment, see our [Contributing Guide][contrib].

[examples]: examples/README.md
[contrib]: .github/CONTRIBUTING.md
[rest-api]: https://developers.thoughtspot.com/docs/?pageid=rest-apis
[rest-api-import]: https://developers.thoughtspot.com/docs/?pageid=tml-api#import
[rest-api-export]: https://developers.thoughtspot.com/docs/?pageid=tml-api#export
[syntax-tml]: https://docs.thoughtspot.com/cloud/latest/tml
[syntax-table]: https://docs.thoughtspot.com/cloud/latest/tml#syntax-tables
[syntax-view]: https://docs.thoughtspot.com/cloud/latest/tml#syntax-views
[syntax-sqlview]: https://docs.thoughtspot.com/cloud/latest/tml#syntax-sqlviews
[syntax-worksheet]: https://docs.thoughtspot.com/cloud/latest/tml#syntax-worksheets
[syntax-answer]: https://docs.thoughtspot.com/cloud/latest/tml#syntax-answers
[syntax-liveboard]: https://docs.thoughtspot.com/cloud/latest/tml#syntax-liveboards
