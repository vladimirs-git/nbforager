"""Tests nb_pai.py."""
import difflib
import inspect
from copy import copy
from typing import Any

import pytest
import requests_mock
from _pytest.monkeypatch import MonkeyPatch
from netports.types_ import LStr
from requests import Response, Session
from requests_mock import Mocker

from nbforager import ami
from nbforager.exceptions import NbApiError
from nbforager.nb_api import NbApi
from nbforager.nb_tree import NbTree
from nbforager.types_ import DAny, LDAny
from tests.api import params__nb_api as p
from tests.api.test__base_c import mock_session


@pytest.fixture
def api():
    """Initialize API"""
    return NbApi(host="netbox")


@pytest.fixture
def mock_get():
    """Mock Session GET."""
    vrf1 = {"id": 1, "url": "https://netbox/api/ipam/vrfs/1/", "name": "VRF 1"}
    vrf2 = {"id": 2, "url": "https://netbox/api/ipam/vrfs/2/", "name": "VRF 1"}
    with requests_mock.Mocker() as mock:
        mock.get(url="https://netbox/api/ipam/vrfs/", json={"results": [vrf1, vrf2]})
        yield mock


@pytest.fixture
def mock_get_d():
    """Mock Session GET."""
    vrf1 = {"id": 1, "url": "https://netbox/api/ipam/vrfs/1/", "name": "VRF 1"}
    with requests_mock.Mocker() as mock:
        mock.get(
            url="https://netbox/api/ipam/vrfs/?id=1&limit=1000&offset=0",
            json={"results": [vrf1]},
        )
        yield mock


@pytest.fixture
def mock_requests_status():
    """Mock request for vrf searching."""
    with requests_mock.Mocker() as mock:
        mock.get("https://netbox/api/status/", json={"netbox-version": "3.6.5"})
        yield mock


def test__app_model(api: NbApi):
    """NbApi has the same models as NbTree object"""
    tree = NbTree()
    for app in tree.apps():
        app_o = getattr(api, app)
        actual = ami.attr_name(obj=app_o)
        assert actual == app

        actual = app_o.__class__.__name__
        expected = "".join([f"{s.capitalize()}" for s in app.split("_")]) + "AC"
        assert actual == expected

        for model in getattr(tree, app).models():
            model_o = getattr(app_o, model)
            actual = ami.attr_name(model_o)
            assert actual == model

            actual = model_o.__class__.__name__
            expected = "".join([f"{s.capitalize()}" for s in model.split("_")]) + "C"
            assert actual == expected


def test__init__(api: NbApi):
    """NbApi.__init__()."""
    actual = list(inspect.signature(type(api).__init__).parameters)

    expected = p.ATTRS
    assert set(actual).symmetric_difference(set(expected)) == set()
    assert actual == expected


def test__copy__(api: NbApi):
    """NbApi.__copy__()."""
    api_: NbApi = copy(api)

    actual = api_.host
    expected = "netbox"
    assert actual == expected


@pytest.mark.parametrize("params, expected", [
    ({"host": "netbox"}, "https://netbox/api/"),
    ({"host": "netbox", "scheme": "https"}, "https://netbox/api/"),
    ({"host": "netbox", "scheme": "http"}, "http://netbox/api/"),
])
def test__url(params, expected):
    """NbApi.url."""
    api = NbApi(**params)
    actual = api.url
    assert actual == expected


@pytest.mark.parametrize("params, threads, expected", [
    ({"host": "netbox"}, 2, 2),
])
def test__threads(api, params, threads, expected):
    """NbApi.threads() setter."""
    assert api.threads == 1

    api.threads = threads

    assert api.threads == expected
    assert api.dcim.devices.threads == expected


# ============================= methods ==============================

@pytest.mark.parametrize("expected", [
    p.APPS,
])
def test__apps(api: NbApi, expected):
    """NbApi.apps()."""
    actual = api.apps()

    assert actual == expected


@pytest.mark.parametrize("expected", [
    p.APP_MODELS,
])
def test__app_models(api: NbApi, expected):
    """NbApi.app_models()."""
    actual = api.app_models()

    actual_ = [str(t) for t in actual]
    expected_ = [str(t) for t in expected]
    diff: LStr = list(difflib.ndiff(actual_, expected_))
    diff = [s for s in diff if s.startswith("- ") or s.startswith("+ ")]
    assert not diff


@pytest.mark.parametrize("expected", [
    p.APP_PATHS,
])
def test__app_paths(api: NbApi, expected):
    """NbApi.app_paths()."""
    actual = api.app_paths()

    assert actual == expected


@pytest.mark.parametrize("path, expected", [
    ("circuits/circuit-terminations", "CircuitTerminationsC"),
    ("circuits/circuit_terminations", "CircuitTerminationsC"),
    ("circuits/circuits", "CircuitsC"),
    ("ipam/ip-addresses", "IpAddressesC"),
    ("ipam/ip_addresses", "IpAddressesC"),
    ("ipam/vrfs", "VrfsC"),
    ("typo/circuits", AttributeError),
    ("circuits/typo", AttributeError),
    ("circuits", ValueError),
])
def test__get_connector(api: NbApi, path, expected: Any):
    """Forager.get_connector()."""
    if isinstance(expected, str):
        connector = api.get_connector(path)
        actual = connector.__class__.__name__
        assert actual == expected
    else:
        with pytest.raises(expected):
            api.get_connector(path)


@pytest.mark.parametrize("expected", [
    p.CONNECTORS,
])
def test__connectors(api: NbApi, expected):
    """NbApi.connectors()."""
    generator_ = api.connectors()

    actual = [o.__class__.__name__ for o in list(generator_)]
    assert actual == expected


@pytest.mark.parametrize("host, expected", [
    ("netbox2", "netbox2"),
])
def test__copy(api: NbApi, host, expected):
    """NbApi.copy()."""
    api_: NbApi = api.copy(host=host)

    actual = api_.host
    assert actual == expected


@pytest.mark.parametrize("params, expected", [
    ({"url": "https://domain.com/ipam/vrfs/", "key": "value"}, [1, 2]),
])
def test__get(
        api: NbApi,
        mock_get: Mocker,  # pylint: disable=unused-argument
        params,
        expected,
):
    """NbApi.get()."""
    api = NbApi(host="netbox")

    objects: LDAny = api.get(**params)

    actual = [d["id"] for d in objects]
    assert actual == expected


@pytest.mark.parametrize("params, expected", [
    ({"url": "https://domain.com/ipam/vrfs/1/", "key": "value"}, 1),
])
def test__get_d(
        api: NbApi,
        mock_get_d: Mocker,  # pylint: disable=unused-argument
        params,
        expected,
):
    """NbApi.get_d()."""
    api = NbApi(host="netbox")

    result: DAny = api.get_d(**params)

    actual = result["id"]
    assert actual == expected


# noinspection DuplicatedCode
@pytest.mark.parametrize("params, expected", [
    ({"id": 1, "url": "https://domain.com/ipam/ip-addresses/1", "key": "value"}, 201),
    ({"id": 1, "url": "https://domain.com/ipam/typo/", "key": "value"}, AttributeError),
    ({"id": 1, "url": "https://domain.com/ipam/", "key": "value"}, NbApiError),
])
def test__create(
        api: NbApi,
        monkeypatch: MonkeyPatch,
        params: DAny,
        expected: Any,
):
    """NbApi.create()."""
    monkeypatch.setattr(Session, "post", mock_session(expected))
    if isinstance(expected, int):
        response: Response = api.create(**params)

        actual = response.status_code
        assert actual == expected
    else:
        with pytest.raises(expected):
            api.create(**params)


# noinspection DuplicatedCode
@pytest.mark.parametrize("params, expected", [
    ({"id": 1, "url": "https://domain.com/ipam/ip-addresses/1", "key": "value"}, 201),
    ({"id": 1, "url": "https://domain.com/ipam/typo/", "key": "value"}, AttributeError),
    ({"id": 1, "url": "https://domain.com/ipam/", "key": "value"}, NbApiError),
])
def test__create_d(
        api: NbApi,
        monkeypatch: MonkeyPatch,
        params: DAny,
        expected: Any,
):
    """NbApi.create_d()."""
    content = '{"1": {"id": "1"}}'
    monkeypatch.setattr(Session, "post", mock_session(status_code=expected, content=content))
    if isinstance(expected, int):
        actual: DAny = api.create_d(**params)

        expected = {"1": {"id": "1"}}
        assert actual == expected
    else:
        with pytest.raises(expected):
            api.create_d(**params)


@pytest.mark.parametrize("url, expected", [
    ("https://domain.com/ipam/ip-addresses/1", 204),
    ("https://domain.com/ipam/ip-addresses/9", 404),
    ("https://domain.com/ipam/ip-addresses/", ValueError),
])
def test__delete(
        api: NbApi,
        monkeypatch: MonkeyPatch,
        url: str,
        expected: Any,
):
    """NbApi.delete()."""
    monkeypatch.setattr(Session, "delete", mock_session(expected))
    if isinstance(expected, int):
        response: Response = api.delete(url=url)

        actual = response.status_code
        assert actual == expected
    else:
        with pytest.raises(expected):
            api.delete(url=url)


@pytest.mark.parametrize("params, expected", [
    ({"url": "https://domain.com/ipam/ip-addresses/1", "key": "value"}, 200),
    ({"url": "https://domain.com/ipam/ip-addresses/1", "key": "value"}, 200),
    ({"url": "https://domain.com/ipam/ip-addresses/9", "key": "value"}, 400),
    ({"url": "https://domain.com/ipam/ip-addresses/0", "key": "value"}, ValueError),
    ({"url": "https://domain.com/ipam/typo/", "key": "value"}, AttributeError),
    ({"url": "https://domain.com/ipam/", "key": "value"}, NbApiError),
])
def test__update(
        api: NbApi,
        monkeypatch: MonkeyPatch,
        params: DAny,
        expected: Any,
):
    """NbApi.update()."""
    monkeypatch.setattr(Session, "patch", mock_session(expected))
    if isinstance(expected, int):
        response: Response = api.update(**params)

        actual = response.status_code
        assert actual == expected
    else:
        with pytest.raises(expected):
            api.update(**params)


def test__version(
        api: NbApi,
        mock_requests_status: Mocker,  # pylint: disable=unused-argument
):
    """NbApi.version()."""
    actual = api.version()
    assert actual == "3.6.5"
