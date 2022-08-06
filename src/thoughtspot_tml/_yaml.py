from typing import Any, Union
from math import inf as INFINITY
import re

import yaml as yaml


# TML ids take the form..
#
#   LOGICAL_TABLE_NAME::LOGICAL_COLUMN_NAME
#
# Where both the logicals can contain spaces.
#
_TML_ID_REGEX = re.compile(r'^[^"][\w\s]+::[\w\s]+[^"]$')

# Reserve characters are defined as any terminator or value or flow entry token.
_TOKEN_CHARACTERS = set("[]{}:,")


def _double_quote_when_special_char(dumper: yaml.Dumper, data: Union[str, int, float]):
    """
    Double quote the string when any condition is met.

      if..
          - it contains special tokens but is not an TML ID
          - is a reserved word
          - it's empty
    """
    special = _TOKEN_CHARACTERS.intersection(set(data))
    reserved = data in ("y", "n")
    is_tml_id = _TML_ID_REGEX.match(data)
    empty_str = not data

    if (special and not is_tml_id) or reserved or empty_str:
        style = '"'
    else:
        style = ""

    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


yaml.add_representer(str, _double_quote_when_special_char)


def load(document: str) -> str:
    """
    Load a TML object.
    """
    return yaml.load(document, Loader=yaml.SafeLoader)


def dump(document: Any) -> str:
    """
    Dump a TML object as YAML.

    The Java TML to YAML mapper includes these settings.

        Feature.ALLOW_COMMENTS = true
        Feature.MINIMIZE_QUOTES = true
        Feature.SPLIT_LINES = false
        Feature.WRITE_DOC_START_MARKER = false
        Feature.ALWAYS_QUOTE_NUMBERS_AS_STRINGS = true

    We'll attempt to reproduce them in Python.
    """
    return yaml.dump(document, width=INFINITY, default_flow_style=False, sort_keys=False)
