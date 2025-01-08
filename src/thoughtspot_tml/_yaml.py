from __future__ import annotations

from typing import Any
import re

import yaml

from thoughtspot_tml import _compat

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


def _double_quote_when_special_char(dumper: yaml.Dumper | yaml.CDumper, data: str) -> yaml.ScalarNode:
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
    else:
        style = ""

    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


yaml.add_representer(str, _double_quote_when_special_char, Dumper=_compat.Dumper)

# BUG: pyyaml #89 ==> resolved by #635
yaml.Loader.yaml_implicit_resolvers.pop("=")


def load(document: str) -> dict[str, Any]:
    """
    Load a TML object.
    """
    try:
        return yaml.load(document, Loader=_compat.Loader)

    # FALL BACK TO THE SLOWER PYTHON LOADER IF WE CAN'T FULLY PARSE UNICODE
    except yaml.scanner.ScannerError:
        return yaml.load(document, Loader=yaml.SafeLoader)


def dump(document: dict[str, Any]) -> str:
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
    NEARLY_INFINITY = 999999999  # This used to be math.inf, but C has no concept of infinity. ;)

    options = {
        "width": NEARLY_INFINITY,
        "default_flow_style": False,
        "sort_keys": False,
        "allow_unicode": True,
    }
    try:
        return yaml.dump(document, Dumper=_compat.Dumper, **options)  # type: ignore[call-overload]

    # FALL BACK TO THE SLOWER PYTHON DUMPER IF WE CAN'T FULLY PARSE UNICODE
    except UnicodeEncodeError:
        return yaml.dump(document, Dumper=yaml.SafeDumper, **options)  # type: ignore[call-overload]
