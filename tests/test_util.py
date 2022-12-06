import json

from thoughtspot_tml.exceptions import TMLError
from thoughtspot_tml.utils import determine_tml_type, disambiguate, EnvironmentGUIDMapper
from thoughtspot_tml.utils import _recursive_scan
from thoughtspot_tml.tml import Connection
from thoughtspot_tml.tml import Table, View, SQLView, Worksheet
from thoughtspot_tml.tml import Answer, Liveboard, Pinboard
from thoughtspot_tml import _scriptability
from ward import test, raises

from . import _const


for file, tml_cls in (
    (_const.DUMMY_CONNECTION, Connection),
    (_const.DUMMY_TABLE, Table),
    (_const.DUMMY_VIEW, View),
    (_const.DUMMY_SQL_VIEW, SQLView),
    (_const.DUMMY_WORKSHEET, Worksheet),
    (_const.DUMMY_ANSWER, Answer),
    (_const.DUMMY_LIVEBOARD, Liveboard),
    (_const.DUMMY_PINBOARD, Pinboard),
):

    @test("determine object utility for {intended_type.__name__}")
    def _(file=file, intended_type=tml_cls):
        t = determine_tml_type(path=file)
        assert t is intended_type


@test("object errors on unknown type")
def _():
    bad_type = "dashboard"

    with raises(TMLError) as exc:
        determine_tml_type(info={"type": bad_type})

    assert f"could not parse TML type from 'info' or 'path', got '{bad_type}'" in str(exc.raised)


@test("object utility requires one of: 'info' or 'path'")
def _():

    with raises(TypeError) as exc:
        determine_tml_type()

    assert str(exc.raised) == "determine_tml_type() missing at least 1 required keyword-only argument: 'info' or 'path'"


for method, envt in (
    (str.lower, "dev"),
    (str.upper, "DEV"),
    (str.title, "Dev"),
):

    @test("mapper environment transformer: {method.__name__}")
    def _(method=method, envt=envt):
        d = EnvironmentGUIDMapper(environment_transformer=method)

        assert len(d.get("d00f3754-15a9-4a7a-a3d5-3248ad19aa9d", default={})) == 0
        assert ("d00f3754-15a9-4a7a-a3d5-3248ad19aa9d" in d) is False

        d["d00f3754-15a9-4a7a-a3d5-3248ad19aa9d"] = ("dev", "d00f3754-15a9-4a7a-a3d5-3248ad19aa9d")

        assert len(d.get("d00f3754-15a9-4a7a-a3d5-3248ad19aa9d", default={})) == 1
        assert ("d00f3754-15a9-4a7a-a3d5-3248ad19aa9d" in d) is True

        assert str(d) == json.dumps(
            {
                "d00f3754-15a9-4a7a-a3d5-3248ad19aa9d": {
                    envt: "d00f3754-15a9-4a7a-a3d5-3248ad19aa9d",
                },
            },
            indent=4,
        )


@test("mapper single guid")
def _():
    d = EnvironmentGUIDMapper()

    assert len(d.get("d00f3754-15a9-4a7a-a3d5-3248ad19aa9d", default={})) == 0
    assert ("d00f3754-15a9-4a7a-a3d5-3248ad19aa9d" in d) is False

    d["d00f3754-15a9-4a7a-a3d5-3248ad19aa9d"] = ("dev", "d00f3754-15a9-4a7a-a3d5-3248ad19aa9d")

    assert len(d.get("d00f3754-15a9-4a7a-a3d5-3248ad19aa9d", default={})) == 1
    assert ("d00f3754-15a9-4a7a-a3d5-3248ad19aa9d" in d) is True

    assert str(d) == json.dumps(
        {
            "d00f3754-15a9-4a7a-a3d5-3248ad19aa9d": {
                "DEV": "d00f3754-15a9-4a7a-a3d5-3248ad19aa9d",
            },
        },
        indent=4,
    )


@test("mapper multiple guids")
def _():
    d = EnvironmentGUIDMapper()

    assert len(d.get("d00f3754-15a9-4a7a-a3d5-3248ad19aa9d", default={})) == 0
    assert ("d00f3754-15a9-4a7a-a3d5-3248ad19aa9d" in d) is False
    assert ("d00f3754-15a9-4a7a-a3d5-3248ad19aa9e" in d) is False
    assert ("d00f3754-15a9-4a7a-a3d5-3248ad19aa9f" in d) is False

    d["d00f3754-15a9-4a7a-a3d5-3248ad19aa9d"] = ("dev", "d00f3754-15a9-4a7a-a3d5-3248ad19aa9d")

    assert len(d.get("d00f3754-15a9-4a7a-a3d5-3248ad19aa9d", default={})) == 1
    assert ("d00f3754-15a9-4a7a-a3d5-3248ad19aa9d" in d) is True
    assert ("d00f3754-15a9-4a7a-a3d5-3248ad19aa9e" in d) is False
    assert ("d00f3754-15a9-4a7a-a3d5-3248ad19aa9f" in d) is False

    d["d00f3754-15a9-4a7a-a3d5-3248ad19aa9d"] = ("test", "d00f3754-15a9-4a7a-a3d5-3248ad19aa9e")

    assert len(d.get("d00f3754-15a9-4a7a-a3d5-3248ad19aa9d", default={})) == 2
    assert ("d00f3754-15a9-4a7a-a3d5-3248ad19aa9d" in d) is True
    assert ("d00f3754-15a9-4a7a-a3d5-3248ad19aa9e" in d) is True
    assert ("d00f3754-15a9-4a7a-a3d5-3248ad19aa9f" in d) is False

    d["d00f3754-15a9-4a7a-a3d5-3248ad19aa9d"] = ("prod", "d00f3754-15a9-4a7a-a3d5-3248ad19aa9f")

    assert len(d.get("d00f3754-15a9-4a7a-a3d5-3248ad19aa9d", default={})) == 3
    assert ("d00f3754-15a9-4a7a-a3d5-3248ad19aa9d" in d) is True
    assert ("d00f3754-15a9-4a7a-a3d5-3248ad19aa9e" in d) is True
    assert ("d00f3754-15a9-4a7a-a3d5-3248ad19aa9f" in d) is True

    assert str(d) == json.dumps(
        {
            "d00f3754-15a9-4a7a-a3d5-3248ad19aa9d__d00f3754-15a9-4a7a-a3d5-3248ad19aa9e__d00f3754-15a9-4a7a-a3d5-3248ad19aa9f": {
                "DEV": "d00f3754-15a9-4a7a-a3d5-3248ad19aa9d",
                "TEST": "d00f3754-15a9-4a7a-a3d5-3248ad19aa9e",
                "PROD": "d00f3754-15a9-4a7a-a3d5-3248ad19aa9f",
            },
        },
        indent=4,
    )


for file, replace_type, to_replace, n_replacements, tml_cls in (
    (_const.DUMMY_TABLE, "name", "Retail - Apparel", 1, Table),
    (_const.DUMMY_VIEW, "name", "(Sample) Retail - Apparel", 2, View),
    (_const.DUMMY_VIEW, "fqn", "d00f3754-15a9-4a7a-a3d5-3248ad19aa9f", 1, View),
    (_const.DUMMY_SQL_VIEW, "name", "Retail - Apparel", 1, SQLView),
    (_const.DUMMY_WORKSHEET, "name", "fact_retapp_sales", 1, Worksheet),
    (_const.DUMMY_ANSWER, "name", "(Sample) Retail - Apparel", 1, Answer),
    (_const.DUMMY_LIVEBOARD, "name", "(Sample) Retail - Apparel", 2, Liveboard),
    (_const.DUMMY_PINBOARD, "name", "(Sample) Retail - Apparel", 1, Pinboard),
):

    @test("disambiguate {tml_cls.__name__} by {replace_type} ({n_replacements} times)")
    def _(file=file, replace_type=replace_type, to_replace=to_replace, n_replacements=n_replacements, tml_cls=tml_cls):
        FAKE_GUID = "99999999-9999-4999-9999-999999999999"
        tml = tml_cls.load(file)

        identities = _recursive_scan(tml, check=lambda x: isinstance(x, _scriptability.Identity))
        assert all((i.fqn != FAKE_GUID for i in identities)) is True

        tml = disambiguate(tml, guid_mapping={to_replace: FAKE_GUID})

        identities = _recursive_scan(tml, check=lambda x: isinstance(x, _scriptability.Identity))
        assert len(identities) >= n_replacements
        assert len([i for i in identities if i.fqn == FAKE_GUID]) == n_replacements
