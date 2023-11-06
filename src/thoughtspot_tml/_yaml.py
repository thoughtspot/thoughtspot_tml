from math import inf as INFINITY
from typing import Any, Dict
import re

import yaml


# TML column ids typically take the form..
#
#   LOGICAL_TABLE_NAME_#::LOGICAL_COLUMN_NAME
#
# Where both the logicals can contain any character except these: {}[].
#
_TML_ID_REGEX = re.compile(
    r"""
    ^              # beginning of string
    [^"]           #   cannot start with a double quote
    [^\[\]\{\}]+?  #     match as few characters as possible, disregarding collection characters
    ::             #     double colon separator
    [^\[\]\{\}]+?  #     match as few characters as possible, disregarding collection characters
    [^"]           #   cannot end with a double quote
    $              # end of string
    """,
    flags=re.VERBOSE,
)

# Reserve characters are defined as any terminator or value or flow entry token.
_TOKEN_CHARACTERS = set("[]{}:,")

# fmt: off
# Reserve words are anything that can convert to a boolean scalar in YAML.
_RESERVED_WORDS = (
    "y",   # Chart Axis
    "on",  # JOIN expressions
)
# fmt: on


def _double_quote_when_special_char(dumper: yaml.Dumper, data: str) -> yaml.ScalarNode:
    """
    Double quote the string when any condition is met.

      if..
          - it contains special tokens but not a TML ID (they don't need doublequotes!)
          - is a reserved word
          - it's empty
    """
    special = _TOKEN_CHARACTERS.intersection(set(data))
    is_tml_id = _TML_ID_REGEX.match(data)
    reserved = data in _RESERVED_WORDS
    empty_str = not data

    if (special and not is_tml_id) or reserved or empty_str:
        style = '"'
    # elif len(data.splitlines()) > 1:
    #     style = "|"
    else:
        style = ""

    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


yaml.add_representer(str, _double_quote_when_special_char)

# BUG: pyyaml #89 ==> resolved by #635
yaml.Loader.yaml_implicit_resolvers.pop("=")


def load(document: str) -> Dict[str, Any]:
    """
    Load a TML object.
    """
    return yaml.load(document, Loader=yaml.SafeLoader)


def dump(document: Dict[str, Any]) -> str:
    """
    Dump a TML object as YAML.

    The Java-based TML to YAML mapper includes these settings.

        Feature.ALLOW_COMMENTS = true
        Feature.MINIMIZE_QUOTES = true
        Feature.SPLIT_LINES = false
        Feature.WRITE_DOC_START_MARKER = false
        Feature.ALWAYS_QUOTE_NUMBERS_AS_STRINGS = true

    We'll attempt to reproduce them in Python.
    """
    return yaml.dump(document, width=INFINITY, default_flow_style=False, sort_keys=False, allow_unicode=True)
