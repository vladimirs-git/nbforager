"""Tests base_c.py."""
from typing import Any

import pytest
import requests_mock
from _pytest.monkeypatch import MonkeyPatch
from netports import NetportsValueError
from requests import Response, Session
from requests_mock import Mocker

from nbforager.api import base_c
from nbforager.exceptions import NbApiError
from nbforager.nb_api import NbApi
from nbforager.nb_forager import NbForager
from nbforager.types_ import DAny, LDAny


@pytest.fixture
def api(params: DAny) -> NbApi:
    """Initializeialize NbApi."""
    return NbApi(host="nb", **params)


@pytest.fixture
def nbf(params: DAny) -> NbForager:
    """Initialize NbForager."""
    return NbForager(host="nb", **params)



@pytest.fixture
def mock_requests_vrf():
    """Mock Session."""
    with requests_mock.Mocker() as mock:
        url = "https://nb/api/ipam/vrfs/?limit=1000&offset=0"
        json = {"results": [{"id": 1, "name": "VRF 1"}, {"id": 2, "name": "VRF 2"}]}
        mock.get(url=url, json=json)
        yield mock


def mock_session(status_code: int, content: str = ""):
    """Mock Session, set Response status_code and text."""

    def mock(*args, **kwargs):
        _ = args, kwargs  # noqa
        response = Response()
        response.status_code = status_code
        response._content = content.encode()
        response.url = kwargs.get("url", "")
        return response

    return mock


@pytest.mark.parametrize("params, expected", [
    ({}, "https://nb/api/ipam/vrfs/"),
    ({"scheme": "http"}, "http://nb/api/ipam/vrfs/"),
    ({"scheme": "http", "port": 80}, "http://nb/api/ipam/vrfs/"),
    ({"scheme": "http", "port": 1}, "http://nb:1/api/ipam/vrfs/"),
    ({"scheme": "https"}, "https://nb/api/ipam/vrfs/"),
    ({"scheme": "https", "port": 443}, "https://nb/api/ipam/vrfs/"),
    ({"scheme": "https", "port": 1}, "https://nb:1/api/ipam/vrfs/"),
])
def test__url(api, nbf, params, expected):
    """BaseC.url."""
    actual = api.ipam.vrfs.url
    assert actual == expected

    actual = nbf.api.ipam.vrfs.url
    assert actual == expected


@pytest.mark.parametrize("params, expected", [
    ({}, "https://nb/ipam/vrfs/"),
    ({"scheme": "http"}, "http://nb/ipam/vrfs/"),
    ({"scheme": "http", "port": 80}, "http://nb/ipam/vrfs/"),
    ({"scheme": "http", "port": 1}, "http://nb:1/ipam/vrfs/"),
    ({"scheme": "https"}, "https://nb/ipam/vrfs/"),
    ({"scheme": "https", "port": 443}, "https://nb/ipam/vrfs/"),
    ({"scheme": "https", "port": 1}, "https://nb:1/ipam/vrfs/"),
])
def test__url_ui(api, params, expected):
    """BaseC.url_ui."""
    actual = api.ipam.vrfs.url_ui
    assert actual == expected


@pytest.mark.parametrize("params, app, model, expected", [
    ({}, "extras", "object_changes", "https://nb/extras/changelog/"),
    ({}, "core", "object_changes", "https://nb/core/changelog/"),
    ({}, "ipam", "ip_addresses", "https://nb/ipam/ip-addresses/"),
])
def test__url_ui__changelog(api, params, app, model, expected):
    """BaseC.url_ui."""
    connector = getattr(getattr(api, app), model)

    actual = connector.url_ui

    assert actual == expected


@pytest.mark.parametrize("params, expected", [
    ({}, "https://nb/api/"),
    ({"scheme": "http"}, "http://nb/api/"),
    ({"scheme": "http", "port": 80}, "http://nb/api/"),
    ({"scheme": "http", "port": 1}, "http://nb:1/api/"),
    ({"scheme": "https"}, "https://nb/api/"),
    ({"scheme": "https", "port": 443}, "https://nb/api/"),
    ({"scheme": "https", "port": 1}, "https://nb:1/api/"),
])
def test__url_base(api, nbf, params, expected):
    """BaseC.url_base."""
    actual = api.circuits.circuit_terminations.url_base
    assert actual == expected

    actual = nbf.api.circuits.circuit_terminations.url_base
    assert actual == expected


# ============================== helper ==============================

@pytest.mark.parametrize("params", [
    {},
])
def test__loners(api, params):
    """BaseC._loners default."""
    assert api.dcim.devices._loners == ["q", "airflow"]
    assert api.ipam.aggregates._loners == ["q", "family", "prefix"]
    assert api.ipam.prefixes._loners == ["q", "family", "within_include"]
    assert api.ipam.ip_addresses._loners == ["q", "family"]


# noinspection PyTestUnpassedFixture
@pytest.mark.parametrize("loners, expected", [
    ({}, ["q", "family", "prefix"]),
    ({"any": ["a1"], "ipam/aggregates/": ["a2"], "ipam/prefixes/": ["a3"]}, ["a1", "a2"]),
])
def test__init_loners(loners, expected):
    """BaseC._init_loners()."""
    api_ = NbApi(host="nb", loners=loners)
    actual = api_.ipam.aggregates._loners
    assert actual == expected

    api_.ipam.aggregates.loners = loners
    actual = api_.ipam.aggregates._init_loners()
    assert actual == expected

    nbf_ = NbForager(host="nb", loners=loners)
    actual = nbf_.api.ipam.aggregates._loners
    assert actual == expected


@pytest.mark.parametrize("params, items, expected", [
    ({}, [], None),
    ({}, [{"url": "ipam/prefixes/", "aggregate": {}}], None),
    ({}, [{"url": "ipam/prefixes/", "id": 1}], None),
    ({}, [{"url": "ipam/prefixes/", "_aggregate": {}}], NbApiError),
])
def test__check_extra_keys__ipam_prefixes(api, params, items, expected):
    """BaseC._check_extra_keys() ipam/prefixes/."""
    if expected is None:
        api.ipam.prefixes._check_extra_keys(items=items)
    else:
        with pytest.raises(expected):
            api.ipam.prefixes._check_extra_keys(items=items)


@pytest.mark.parametrize("params, items, expected", [
    ({}, [], None),
    ({}, [{"url": "dcim/devices/", "id": 1}], None),
    ({}, [{"url": "dcim/devices/", "interfaces": {}}], None),
    ({}, [{"url": "dcim/devices/", "_interfaces": {}}], NbApiError),
])
def test__check_extra_keys__dcim_devices(api, params, items, expected: Any):
    """BaseC._check_extra_keys(). dcim/devices/"""
    if expected is None:
        api.dcim.devices._check_extra_keys(items=items)
    else:
        with pytest.raises(expected):
            api.dcim.devices._check_extra_keys(items=items)


@pytest.mark.parametrize("extended_get, params_d, expected", [
    (True, {"a": ["A"]}, {"a": ["A"]}),
    (True, {"a": ["A", "B"]}, {"a": ["A", "B"]}),
    (True, {"vrf": ["null"]}, {"vrf": ["null"]}),
    (True, {"vrf": ["typo"]}, {"vrf": ["typo"]}),
    (True, {"vrf": ["VRF 1"]}, {"vrf_id": [1]}),
    (True, {"vrf": ["VRF 1", "VRF 2"]}, {"vrf_id": [1, 2]}),
    (True, {"vrf": ["VRF 1", "typo"]}, {"vrf_id": [1]}),
    (True, {"vrf": ["typo"]}, {"vrf": ["typo"]}),
    (True, {"or_vrf": ["VRF 1"]}, {"vrf_id": [1]}),
    (True, {"or_vrf": ["VRF 1", "VRF 2"]}, {"vrf_id": [1, 2]}),
    (True, {"present_in_vrf": ["null"]}, {"present_in_vrf": ["null"]}),
    (True, {"present_in_vrf": ["VRF 1"]}, {"present_in_vrf_id": [1]}),
    (True, {"present_in_vrf": ["VRF 1"], "vrf": ["VRF 2"]},
     {"present_in_vrf_id": [1], "vrf_id": [2]}),
    (False, {"a": ["A", "B"]}, {"a": ["A", "B"]}),
    (False, {"vrf": ["VRF 1"]}, {"vrf": ["VRF 1"]}),
])
def test__change_params_name_to_id(
        mock_requests_vrf: Mocker,  # pylint: disable=unused-argument
        extended_get,
        params_d: DAny,
        expected: DAny,
):
    """BaseC._change_params_name_to_id()."""
    api_ = NbApi(host="nb", extended_get=extended_get)

    actual = api_.ipam.ip_addresses._change_params_name_to_id(params_d=params_d)

    assert actual == expected


@pytest.mark.parametrize("extended_get, params_d, expected", [
    (True, {"site_id": [1], "region_id": [2]}, {"site": [1], "region_id": [2]}),
    (False, {"site_id": [1], "region_id": [2]}, {"site_id": [1], "region_id": [2]}),
])
def test__change_params_exceptions(
        mock_requests_vrf: Mocker,  # pylint: disable=unused-argument
        extended_get,
        params_d: DAny,
        expected: DAny,
):
    """BaseC._change_params_exceptions()."""
    api_ = NbApi(host="nb", extended_get=extended_get)

    actual = api_.ipam.vlan_groups._change_params_exceptions(params_d=params_d)

    assert actual == expected


@pytest.mark.parametrize("params, resp_status_code, resp_text, error", [
    # strict=True
    ({"strict": True}, 200, "any", None),
    ({"strict": True}, 400, "choice ... is not one of the available choices", ConnectionError),
    ({"strict": True}, 403, "Invalid token", ConnectionError),
    ({"strict": True}, 500, "any server error", ConnectionError),
    ({"strict": True, "timeout": 1, "max_retries": 1, "sleep": 1}, 200, "any", None),
    ({"strict": True, "timeout": 1, "max_retries": 2, "sleep": 1}, 504, "Session timeout",
     ConnectionError),  # max_retries used in old version
    # strict=False
    ({"strict": False}, 200, "any", None),
    ({"strict": False}, 400, "choice ... is not one of the available choices", None),
    ({"strict": False}, 403, "Invalid token", ConnectionError),
    ({"strict": False}, 500, "any server error", ConnectionError),
    ({"strict": False, "timeout": 1, "max_retries": 1, "sleep": 1}, 200, "any", None),
    ({"strict": False, "timeout": 1, "max_retries": 2, "sleep": 1}, 504, "Session timeout",
     ConnectionError),  # max_retries used in old version
])
def test__retry_requests(api, monkeypatch: MonkeyPatch,
                         params, resp_status_code, resp_text, error):
    """BaseC._retry_requests()."""
    monkeypatch.setattr(Session, "get", mock_session(resp_status_code, resp_text))
    if error:
        with pytest.raises(error):
            api.ipam.ip_addresses._retry_requests(url="")
    else:
        response = api.ipam.ip_addresses._retry_requests(url="")
        actual = response.status_code
        assert actual == resp_status_code


@pytest.mark.parametrize("strict, status_code, text, error", [
    # strict=False
    (False, 100, "any", ConnectionError),
    (False, 200, "any", None),
    (False, 300, "any", ConnectionError),
    (False, 400, "any", None),
    (False, 403, "any", ConnectionError),
    (False, 500, "any", ConnectionError),
    (False, 600, "any", ConnectionError),
    # strict=True
    (True, 100, "any", ConnectionError),
    (True, 200, "any", None),
    (True, 300, "any", ConnectionError),
    (True, 400, "any", ConnectionError),
    (True, 403, "any", ConnectionError),
    (True, 500, "any", ConnectionError),
    (True, 600, "any", ConnectionError),
])
def test__handle_server_error(strict, status_code, text, error):
    """BaseC._handle_server_error()."""
    api_ = NbApi(host="nb", strict=strict)

    response = Response()
    response.status_code = status_code
    response._content = str.encode(text)

    if error is None:
        api_.ipam.ip_addresses._handle_server_error(response=response)
    else:
        with pytest.raises(error):
            api_.ipam.ip_addresses._handle_server_error(response=response)


def test__response_gateway_timeout():
    """BaseC._response_gateway_timeout()."""
    api_ = NbApi(host="nb")

    response_ = api_.ipam.ip_addresses._response_gateway_timeout()

    assert response_.status_code == 504
    assert response_.reason == "Gateway Timeout"
    assert response_.text == "max_retries=0 reached."


# ============================= helpers ==============================


@pytest.mark.parametrize("params_d, expected", [
    ({}, {"limit": [1000], "offset": [0]}),
    ({"limit": [2]}, {"limit": [2], "offset": [0]}),
    ({"offset": [3]}, {"limit": [1000], "offset": [3]}),
    ({"limit": [2], "offset": [3]}, {"limit": [2], "offset": [3]}),
])
def test__add_default_limit_offset(params_d, expected):
    """BaseC._add_default_limit_offset()."""
    api_ = NbApi(host="nb")

    actual = api_.ipam.ip_addresses._add_default_limit_offset(params_d=params_d)

    assert actual == expected


@pytest.mark.parametrize("status_code, text, expected", [
    (400, "text", "status_code=400 text='text' url='nb'"),
    (400, "<title>Page Not Found. text<title>", "status_code=400 text='Page Not Found.' url='nb'"),
    (None, "text", ""),
])
def test__msg_status_code(status_code, text, expected):
    """BaseC._msg_status_code()."""
    api_ = NbApi(host="nb")
    if isinstance(status_code, int):
        response_ = Response()
        response_.status_code = status_code
        response_._content = str.encode(text)
        response_.url = "nb"
    else:
        response_ = None

    actual = api_.ipam.ip_addresses._msg_status_code(response=response_)

    assert actual == expected


@pytest.mark.parametrize("params, results, expected", [
    ({}, [], []),
    ({}, [{"count": 1, "params_d": {}}], [{"limit": 1000, "offset": 0}]),
    ({}, [{"count": 1001, "params_d": {}}],
     [{"limit": 1000, "offset": 0}, {"limit": 1000, "offset": 1000}]),
])
def test__slice_params_counters(api, params, results, expected):
    """BaseC._slice_params_counters()."""
    actual = api.ipam.ip_addresses._slice_params_counters(results=results)
    assert actual == expected


@pytest.mark.parametrize("params, expected", [
    ({}, ValueError),
    ({"host": ""}, ValueError),
    ({"host": "netbox"}, "netbox"),
])
def test__init_host(params, expected: Any):
    """base_c._init_host()"""
    if isinstance(expected, str):
        actual = base_c._init_host(**params)
        assert actual == expected
    else:
        with pytest.raises(expected):
            base_c._init_host(**params)


@pytest.mark.parametrize("params, expected", [
    ({}, 443),
    ({"port": ""}, 443),
    ({"port": 0}, 443),
    ({"port": -1}, NetportsValueError),
    ({"port": 1}, 1),
    ({"port": "1"}, 1),
    ({"scheme": "typo"}, 443),
    ({"scheme": "http"}, 80),
    ({"scheme": "HTTP"}, 80),
    ({"scheme": "https"}, 443),
    ({"scheme": "HTTPs"}, 443),
    ({"scheme": "http", "port": "1"}, 1),
    ({"scheme": "http", "port": 1}, 1),
    ({"scheme": "https", "port": "1"}, 1),
    ({"scheme": "https", "port": 1}, 1),
    ({"scheme": "typo", "port": "1"}, 1),
])
def test__init_port(params, expected: Any):
    """base_c._init_port()"""
    if isinstance(expected, int):
        actual = base_c._init_port(**params)
        assert actual == expected
    else:
        with pytest.raises(expected):
            base_c._init_port(**params)


@pytest.mark.parametrize("params, expected", [
    ({}, ValueError),
    ({"scheme": ""}, ValueError),
    ({"scheme": "typo"}, ValueError),
    ({"scheme": "http"}, "http"),
    ({"scheme": "HTTP"}, "http"),
    ({"scheme": "https"}, "https"),
    ({"scheme": "HTTPs"}, "https"),
])
def test__init_scheme(params, expected: Any):
    """base_c._init_scheme()"""
    if isinstance(expected, str):
        actual = base_c._init_scheme(**params)
        assert actual == expected
    else:
        with pytest.raises(expected):
            base_c._init_scheme(**params)


@pytest.mark.parametrize("params, expected", [
    ({}, {}),
    ({"a": 1}, {"a": [1]}),
    ({"a": [1, 1]}, {"a": [1]}),
    ({"a": (1, 2)}, {"a": [1, 2]}),
    ({"a": 1, "b": 3}, {"a": [1], "b": [3]}),
])
def test__lists_wo_dupl(params, expected: LDAny):
    """base_c._lists_wo_dupl()."""
    actual = base_c._lists_wo_dupl(kwargs=params)
    assert actual == expected
