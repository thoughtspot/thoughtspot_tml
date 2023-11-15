from thoughtspot_tml._version import __version__

from thoughtspot_tml.tml import Connection
from thoughtspot_tml.tml import Table, View, SQLView, Worksheet
from thoughtspot_tml.tml import Answer, Liveboard, Pinboard
from thoughtspot_tml.spotapp import SpotApp

# aliases
from thoughtspot_tml.tml import Connection as EmbraceConnection
from thoughtspot_tml.tml import View as ThoughtSpotView
from thoughtspot_tml.tml import Answer as SavedAnswer
from thoughtspot_tml.tml import Table as SystemTable


__all__ = (
    "__version__",
    "Connection",
    "Table",
    "View",
    "SQLView",
    "Worksheet",
    "Answer",
    "Liveboard",
    "Pinboard",
    "SpotApp",
    "EmbraceConnection",
    "ThoughtSpotView",
    "SavedAnswer",
    "SystemTable",
)
