from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional
import zipfile
import typing
import json

from thoughtspot_tml._compat import ZipPath
from thoughtspot_tml.utils import determine_tml_type
from thoughtspot_tml.tml import Table, View, SQLView, Worksheet, Answer, Liveboard, Pinboard
from thoughtspot_tml import _yaml

if TYPE_CHECKING:
    from thoughtspot.types import EDocExportResponse, TMLDocInfo
    from thoughtspot.types import TMLType
    from thoughtspot.types import PathLike

    TSpotApp = typing.TypeVar("TSpotApp", bound="SpotApp")


@dataclass
class Manifest:
    object: List["TMLDocInfo"]


@dataclass
class SpotApp:
    """
    A collection of Tables, Views, Worksheets, Answers, and Liveboards.

    This object is usually packaged together as a zip file.
    """

    tml: List["TMLType"]
    manifest: Optional[Manifest] = None

    @property
    def tables(self) -> List[Table]:
        return [tml for tml in self.tml if isinstance(tml, Table)]

    @property
    def views(self) -> List[View]:
        return [tml for tml in self.tml if isinstance(tml, View)]

    @property
    def sql_views(self) -> List[SQLView]:
        return [tml for tml in self.tml if isinstance(tml, SQLView)]

    @property
    def worksheets(self) -> List[Worksheet]:
        return [tml for tml in self.tml if isinstance(tml, Worksheet)]

    @property
    def answers(self) -> List[Answer]:
        return [tml for tml in self.tml if isinstance(tml, Answer)]

    @property
    def liveboards(self) -> List[Liveboard]:
        return [tml for tml in self.tml if isinstance(tml, (Liveboard, Pinboard))]

    @classmethod
    def from_api(cls, payload: "EDocExportResponse") -> "TSpotApp":
        """
        Load the SpotApp from file.

        Parameters
        ----------
        payload : EDocExportResponse
          api response data to parse
        """
        info = {"tml": [], "manifest": None}
        manifest_data = {"object": []}

        for edoc_info in payload["object"]:
            tml_cls = determine_tml_type(info=edoc_info["info"])
            document = json.loads(edoc_info["edoc"])
            manifest_data["object"].append(edoc_info["info"])
            tml = tml_cls(**document)
            info["tml"].append(tml)

        info["manifest"] = Manifest(**manifest_data)
        return cls(**info)

    @classmethod
    def read(cls, path: "PathLike") -> "TSpotApp":
        """
        Load the SpotApp from file.

        Parameters
        ----------
        path : PathLike
          filepath to read the SpotApp from
        """
        info = {"tml": [], "manifest": None}

        with zipfile.ZipFile(path, mode="r") as archive:
            for member in archive.infolist():
                path = ZipPath(archive, at=member.filename)

                if member.filename == "Manifest.yaml":
                    document = _yaml.load(path.read_text())
                    info["manifest"] = Manifest(**document)
                    continue

                tml_cls = determine_tml_type(path=member.filename)
                tml = tml_cls.load(path)
                info["tml"].append(tml)

        return cls(**info)

    def save(self, path: "PathLike") -> None:
        """
        Save the SpotApp to file.

        Parameters
        ----------
        path : PathLike
          filepath to save the zip file to
        """
        with zipfile.ZipFile(path, mode="w") as archive:
            for edoc in self.tml:
                edoc_type = type(edoc).__name__.lower()
                document = edoc.dumps()
                archive.writestr(f"{edoc.name}.{edoc_type}.tml", data=document)
