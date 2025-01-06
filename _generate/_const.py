from __future__ import annotations

import pathlib

from rich.console import Console

VOID = r""

RICH_CONSOLE = Console()
THIS_DIR = pathlib.Path(__file__).parent

LATEST_EDOC_PROTO = THIS_DIR / "edoc" / "edoc.proto"
_SCRIPTABILITY_PY = THIS_DIR.parent / "src" / "thoughtspot_tml" / "_scriptability.py"
