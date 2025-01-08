from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional
import json
import pathlib
import zipfile

from thoughtspot_tml import _yaml
from thoughtspot_tml._compat import ZipPath
from thoughtspot_tml.tml import Answer, Cohort, Liveboard, Model, SQLView, Table, View, Worksheet
from thoughtspot_tml.utils import determine_tml_type

if TYPE_CHECKING:
    from thoughtspot_tml.types import EDocExportResponses, SpotAppInfo, TMLDocInfo, TMLObject


@dataclass
class Manifest:
    object: list[TMLDocInfo]


@dataclass
class SpotApp:
    """
    A collection of Tables, Views, Worksheets, Answers, and Liveboards.

    This object is usually packaged together as a zip file.
    """

    tml: list[TMLObject]
    manifest: Optional[Manifest] = None

    @property
    def tables(self) -> list[Table]:
        return [tml for tml in self.tml if isinstance(tml, Table)]

    @property
    def views(self) -> list[View]:
        return [tml for tml in self.tml if isinstance(tml, View)]

    @property
    def sql_views(self) -> list[SQLView]:
        return [tml for tml in self.tml if isinstance(tml, SQLView)]

    @property
    def worksheets(self) -> list[Worksheet]:
        return [tml for tml in self.tml if isinstance(tml, Worksheet)]

    @property
    def answers(self) -> list[Answer]:
        return [tml for tml in self.tml if isinstance(tml, Answer)]

    @property
    def liveboards(self) -> list[Liveboard]:
        return [tml for tml in self.tml if isinstance(tml, Liveboard)]

    @property
    def model(self) -> list[Model]:
        return [tml for tml in self.tml if isinstance(tml, Model)]

    @property
    def cohort(self) -> list[Cohort]:
        return [tml for tml in self.tml if isinstance(tml, Cohort)]

    @classmethod
    def from_api(cls, payload: EDocExportResponses) -> SpotApp:
        """
        Load the SpotApp from file.

        ThoughtSpot's TML Export API can be found here
          https://developers.thoughtspot.com/docs/?pageid=tml-api#export

        Parameters
        ----------
        payload : EDocExportResponse
          metadata/tml/export response data to parse
        """
        info: SpotAppInfo = {"tml": [], "manifest": None}
        manifest_data: dict[str, list[TMLDocInfo]] = {"object": []}

        for edoc_info in payload["object"]:
            tml_cls = determine_tml_type(info=edoc_info["info"])
            document = json.loads(edoc_info["edoc"])
            manifest_data["object"].append(edoc_info["info"])
            tml = tml_cls(**document)
            info["tml"].append(tml)

        info["manifest"] = Manifest(**manifest_data)
        return cls(**info)

    @classmethod
    def read(cls, path: pathlib.Path) -> SpotApp:
        """
        Load the SpotApp from file.

        Parameters
        ----------
        path : pathlib.Path
          filepath to read the SpotApp from
        """
        info: SpotAppInfo = {"tml": [], "manifest": None}

        with zipfile.ZipFile(path, mode="r") as archive:
            for member in archive.infolist():
                path = ZipPath(archive, at=member.filename)  # type: ignore[assignment]

                if member.filename == "Manifest.yaml":
                    document = _yaml.load(path.read_text())
                    info["manifest"] = Manifest(**document)
                    continue

                tml_cls = determine_tml_type(path=pathlib.Path(member.filename))
                tml = tml_cls.load(path)
                info["tml"].append(tml)

        return cls(**info)

    def save(self, path: pathlib.Path) -> None:
        """
        Save the SpotApp to file.

        Parameters
        ----------
        path : pathlib.Path
          filepath to save the zip file to
        """
        with zipfile.ZipFile(path, mode="w") as archive:
            for edoc in self.tml:
                edoc_type = type(edoc).__name__.lower()
                document = edoc.dumps()
                archive.writestr(f"{edoc.name}.{edoc_type}.tml", data=document)
