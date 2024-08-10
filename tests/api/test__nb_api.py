"""Tests nb_pai.py."""
import inspect
from copy import copy
from typing import Any

import pytest
import requests_mock
from _pytest.monkeypatch import MonkeyPatch
from requests import Response, Session
from requests_mock import Mocker

from nbforager import helpers as h
from nbforager.exceptions import NbApiError
from nbforager.nb_api import NbApi
from nbforager.nb_tree import NbTree
from nbforager.types_ import DAny
from tests.api.test__base_c import mock_session

ATTRS = [
    "self",
    "host",
    "token",
    "scheme",
    "port",
    "verify",
    "limit",
    "url_length",
    "threads",
    "interval",
    "timeout",
    "max_retries",
    "sleep",
    "strict",
    "extended_get",
    "default_get",
    "loners",
    "kwargs",
]


@pytest.fixture
def api():
    """Init API"""
    return NbApi(host="netbox")


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
        actual = h.attr_name(obj=app_o)
        assert actual == app

        actual = app_o.__class__.__name__
        expected = "".join([f"{s.capitalize()}" for s in app.split("_")]) + "AC"
        assert actual == expected

        for model in getattr(tree, app).models():
            model_o = getattr(app_o, model)
            actual = h.attr_name(model_o)
            assert actual == model

            actual = model_o.__class__.__name__
            expected = "".join([f"{s.capitalize()}" for s in model.split("_")]) + "C"
            assert actual == expected


def test__init__(api: NbApi):
    """NbApi.__init__()."""
    actual = list(inspect.signature(type(api).__init__).parameters)

    expected = ATTRS
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


def test__threads():
    """NbApi.threads."""
    api = NbApi(host="netbox")
    assert api.threads == 1

    api.threads = 2

    expected = 2
    assert api.threads == expected
    assert api.dcim.devices.threads == expected


def test__version(
        api: NbApi,
        mock_requests_status: Mocker,  # pylint: disable=unused-argument
):
    """NbApi.version()."""
    actual = api.version()
    assert actual == "3.6.5"


@pytest.mark.parametrize("host, expected", [
    ("netbox2", "netbox2"),
])
def test__copy(api: NbApi, host, expected):
    """NbApi.copy()."""
    api_: NbApi = api.copy(host=host)

    actual = api_.host
    assert actual == expected


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
