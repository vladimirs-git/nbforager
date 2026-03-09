"""Tests nbforager/api/nb_pai.py."""
import difflib
import inspect
from copy import copy
from typing import Any

import pytest
from _pytest.monkeypatch import MonkeyPatch
from netports.types_ import LStr
from requests import Response, Session
from requests_mock import Mocker

from nbforager import ami
from nbforager.exceptions import NbApiError
from nbforager.nb_api import NbApi
from nbforager.nb_tree import NbTree
from nbforager.types import DAny, LDAny
from tests.fixtures import api, api_, mock_session
from tests import params__nb_api as p
from tests.fixtures__nb_api import mock_get, mock_get_d, mock_requests_status


def test__app_model(api_):
    """NbApi has the same models as NbTree object"""
    tree = NbTree()
    for app in tree.apps():
        app_o = getattr(api_, app)
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


def test__init__(api_):
    """NbApi.__init__()."""
    actual = list(inspect.signature(type(api_).__init__).parameters)

    expected = p.ATTRS
    assert set(actual).symmetric_difference(set(expected)) == set()
    assert actual == expected

@pytest.mark.parametrize("params", [
    ({"host": "nb", "token": "token", "scheme": "http", "port": 2, "verify": False, "limit": 2,
      "url_length": 2, "threads": 2, "interval": 2, "timeout": 2, "max_retries": 2, "sleep": 2,
      "strict": True, "extended_get": False, "loners": {"a": "a"}}),
])
def test__copy__(api, params):
    """NbApi.__copy__()."""
    api2 = copy(api)

    assert api2.host == "nb"
    # connector
    assert api2._base_c.host == "nb"
    assert api2._base_c.token == "token"
    assert api2._base_c.scheme == "http"
    assert api2._base_c.port == 2
    assert api2._base_c.verify is False
    assert api2._base_c.limit == 2
    assert api2._base_c.url_length == 2
    assert api2._base_c.threads == 2
    assert api2._base_c.interval == 2
    assert api2._base_c.timeout == 2
    assert api2._base_c.max_retries == 2
    assert api2._base_c.sleep == 2
    assert api2._base_c.strict is True
    assert api2._base_c.extended_get is False
    assert api2._base_c.loners == {"a": "a"}
    # app/model
    assert api2.host == "nb"
    assert api2.ipam.vrfs.host == "nb"
    assert api2.ipam.vrfs.token == "token"
    assert api2.ipam.vrfs.scheme == "http"
    assert api2.ipam.vrfs.port == 2
    assert api2.ipam.vrfs.verify is False
    assert api2.ipam.vrfs.limit == 2
    assert api2.ipam.vrfs.url_length == 2
    assert api2.ipam.vrfs.threads == 2
    assert api2.ipam.vrfs.interval == 2
    assert api2.ipam.vrfs.timeout == 2
    assert api2.ipam.vrfs.max_retries == 2
    assert api2.ipam.vrfs.sleep == 2
    assert api2.ipam.vrfs.strict is True
    assert api2.ipam.vrfs.extended_get is False
    assert api2.ipam.vrfs.loners == {"a": "a"}
    assert api2.ipam.vrfs.extended_get is False
    assert api2.ipam.vrfs.loners == {"a": "a"}


@pytest.mark.parametrize("params, expected", [
    ({}, "https://nb/api/"),
    ({"scheme": "https"}, "https://nb/api/"),
    ({"scheme": "http"}, "http://nb/api/"),
])
def test__url(api, params, expected):
    """NbApi.url."""
    actual = api.url

    assert actual == expected


@pytest.mark.parametrize("params, expected", [
    ({}, "https://nb/api/"),
    ({"scheme": "https"}, "https://nb/api/"),
    ({"scheme": "http"}, "http://nb/api/"),
])
def test__url_api(api, params, expected):
    """NbApi.url_api."""
    actual = api.url_api

    assert actual == expected


@pytest.mark.parametrize("threads, expected", [
    (2, 2),
])
def test__threads(api_, threads, expected):
    """NbApi.threads() setter."""
    assert api_.threads == 1

    api_.threads = threads

    assert api_.threads == expected
    assert api_.dcim.devices.threads == expected


# ============================= methods ==============================

@pytest.mark.parametrize("expected", [
    p.APPS,
])
def test__apps(api_, expected):
    """NbApi.apps()."""
    actual = api_.apps()

    assert actual == expected


@pytest.mark.parametrize("expected", [
    p.APP_MODELS,
])
def test__app_models(api_, expected):
    """NbApi.app_models()."""
    actual = api_.app_models()

    actual_ = [str(t) for t in actual]
    expected_ = [str(t) for t in expected]
    diff: LStr = list(difflib.ndiff(actual_, expected_))
    diff = [s for s in diff if s.startswith("- ") or s.startswith("+ ")]
    assert not diff


@pytest.mark.parametrize("expected", [
    p.APP_PATHS,
])
def test__app_paths(api_, expected):
    """NbApi.app_paths()."""
    actual = api_.app_paths()

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
def test__connector_by_path(api_, path, expected: Any):
    """Forager.connector_by_path()."""
    if isinstance(expected, str):
        connector = api_.connector_by_path(path)
        actual = connector.__class__.__name__
        assert actual == expected
    else:
        with pytest.raises(expected):
            api_.connector_by_path(path)


@pytest.mark.parametrize("expected", [
    p.CONNECTORS,
])
def test__connectors(api_, expected):
    """NbApi.connectors()."""
    generator_ = api_.connectors()

    actual = [o.__class__.__name__ for o in list(generator_)]
    assert actual == expected


@pytest.mark.parametrize("host, expected", [
    ("netbox2", "netbox2"),
])
def test__copy(api_, host, expected):
    """NbApi.copy()."""
    api2: NbApi = api_.copy(host=host)

    actual = api2.host
    assert actual == expected


@pytest.mark.parametrize("params, expected", [
    ({"url": "https://domain.com/ipam/vrfs/", "key": "value"}, [1, 2]),
])
def test__get(api_, mock_get: Mocker, params, expected):
    """NbApi.get()."""
    api_ = NbApi(host="netbox")

    objects: LDAny = api_.get(**params)

    actual = [d["id"] for d in objects]
    assert actual == expected


@pytest.mark.parametrize("params, expected", [
    ({"url": "https://domain.com/ipam/vrfs/1/", "key": "value"}, 1),
])
def test__get_d(api_, mock_get_d: Mocker, params, expected):
    """NbApi.get_d()."""
    api_ = NbApi(host="netbox")

    result: DAny = api_.get_d(**params)

    actual = result["id"]
    assert actual == expected


# noinspection DuplicatedCode
@pytest.mark.parametrize("params, expected", [
    ({"id": 1, "url": "https://domain.com/ipam/ip-addresses/1", "key": "value"}, 201),
    ({"id": 1, "url": "https://domain.com/ipam/typo/", "key": "value"}, AttributeError),
    ({"id": 1, "url": "https://domain.com/ipam/", "key": "value"}, NbApiError),
])
def test__create(api_, monkeypatch: MonkeyPatch, params: DAny, expected: Any):
    """NbApi.create()."""
    monkeypatch.setattr(Session, "post", mock_session(expected))
    if isinstance(expected, int):
        response: Response = api_.create(**params)

        actual = response.status_code
        assert actual == expected
    else:
        with pytest.raises(expected):
            api_.create(**params)


# noinspection DuplicatedCode
@pytest.mark.parametrize("params, expected", [
    ({"id": 1, "url": "https://domain.com/ipam/ip-addresses/1", "key": "value"}, 201),
    ({"id": 1, "url": "https://domain.com/ipam/typo/", "key": "value"}, AttributeError),
    ({"id": 1, "url": "https://domain.com/ipam/", "key": "value"}, NbApiError),
])
def test__create_d(api_, monkeypatch: MonkeyPatch, params: DAny, expected: Any):
    """NbApi.create_d()."""
    content = '{"1": {"id": "1"}}'
    monkeypatch.setattr(Session, "post", mock_session(status_code=expected, content=content))
    if isinstance(expected, int):
        actual: DAny = api_.create_d(**params)

        expected = {"1": {"id": "1"}}
        assert actual == expected
    else:
        with pytest.raises(expected):
            api_.create_d(**params)


@pytest.mark.parametrize("url, expected", [
    ("https://domain.com/ipam/ip-addresses/1", 204),
    ("https://domain.com/ipam/ip-addresses/9", 404),
    ("https://domain.com/ipam/ip-addresses/", ValueError),
])
def test__delete(api_, monkeypatch: MonkeyPatch, url: str, expected: Any):
    """NbApi.delete()."""
    monkeypatch.setattr(Session, "delete", mock_session(expected))
    if isinstance(expected, int):
        response: Response = api_.delete(url=url)

        actual = response.status_code
        assert actual == expected
    else:
        with pytest.raises(expected):
            api_.delete(url=url)


@pytest.mark.parametrize("params, expected", [
    ({"url": "https://domain.com/ipam/ip-addresses/1", "key": "value"}, 200),
    ({"url": "https://domain.com/ipam/ip-addresses/1", "key": "value"}, 200),
    ({"url": "https://domain.com/ipam/ip-addresses/9", "key": "value"}, 400),
    ({"url": "https://domain.com/ipam/ip-addresses/0", "key": "value"}, ValueError),
    ({"url": "https://domain.com/ipam/typo/", "key": "value"}, AttributeError),
    ({"url": "https://domain.com/ipam/", "key": "value"}, NbApiError),
])
def test__update(api_, monkeypatch: MonkeyPatch, params: DAny, expected: Any):
    """NbApi.update()."""
    monkeypatch.setattr(Session, "patch", mock_session(expected))
    if isinstance(expected, int):
        response: Response = api_.update(**params)

        actual = response.status_code
        assert actual == expected
    else:
        with pytest.raises(expected):
            api_.update(**params)


def test__version(api_, mock_requests_status: Mocker):
    """NbApi.version()."""
    actual = api_.version()
    assert actual == "3.6.5"
