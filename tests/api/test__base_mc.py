"""Tests nbforager/api/base_mc.py."""
from typing import Any

import pytest
from _pytest.monkeypatch import MonkeyPatch
from requests import Session, HTTPError
from requests_mock import Mocker

from nbforager.api import base_mc
from nbforager.exceptions import NbApiError
from nbforager.nb_api import NbApi
from nbforager.nb_forager import NbForager
from nbforager.types import DAny, LDAny
from tests.fixtures import api, nbf, mock_session
from tests.api.fixtures__base_mc import mock_requests_vrf


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
    """BaseMC.url."""
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
    """BaseMC.url_ui."""
    actual = api.ipam.vrfs.url_ui
    assert actual == expected


@pytest.mark.parametrize("params, app, model, expected", [
    ({}, "extras", "object_changes", "https://nb/extras/changelog/"),
    ({}, "core", "object_changes", "https://nb/core/changelog/"),
    ({}, "ipam", "ip_addresses", "https://nb/ipam/ip-addresses/"),
])
def test__url_ui__changelog(api, params, app, model, expected):
    """BaseMC.url_ui."""
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
def test__url_api(api, nbf, params, expected):
    """BaseMC.url_api."""
    actual = api.circuits.circuit_terminations.url_api
    assert actual == expected

    actual = nbf.api.circuits.circuit_terminations.url_api
    assert actual == expected


# ============================== helper ==============================

@pytest.mark.parametrize("params", [
    {},
])
def test__loners(api, params):
    """BaseMC._loners default."""
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
    """BaseMC._init_loners()."""
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
    """BaseMC._check_extra_keys() ipam/prefixes/."""
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
    """BaseMC._check_extra_keys(). dcim/devices/"""
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
        mock_requests_vrf: Mocker, extended_get, params_d: DAny, expected: DAny,
):
    """BaseMC._change_params_name_to_id()."""
    api_ = NbApi(host="nb", extended_get=extended_get)

    actual = api_.ipam.ip_addresses._change_params_name_to_id(params_d=params_d)

    assert actual == expected


@pytest.mark.parametrize("extended_get, params_d, expected", [
    (True, {"site_id": [1], "region_id": [2]}, {"site": [1], "region_id": [2]}),
    (False, {"site_id": [1], "region_id": [2]}, {"site_id": [1], "region_id": [2]}),
])
def test__change_params_exceptions(
        mock_requests_vrf: Mocker, extended_get, params_d: DAny, expected: DAny,
):
    """BaseMC._change_params_exceptions()."""
    api_ = NbApi(host="nb", extended_get=extended_get)

    actual = api_.ipam.vlan_groups._change_params_exceptions(params_d=params_d)

    assert actual == expected


@pytest.mark.parametrize("params, resp_status_code, resp_text, error", [
    # strict=True
    ({"strict": True}, 200, "any", None),
    ({"strict": True}, 400, "choice ... is not one of the available choices", HTTPError),
    ({"strict": True}, 403, "Invalid token", HTTPError),
    ({"strict": True}, 500, "any server error", HTTPError),
    ({"strict": True, "timeout": 1, "max_retries": 1, "sleep": 1}, 200, "any", None),
    ({"strict": True, "timeout": 1, "max_retries": 2, "sleep": 1}, 504, "Session timeout",
     HTTPError),  # max_retries used in old version
    # strict=False
    ({"strict": False}, 200, "any", None),
    ({"strict": False}, 400, "choice ... is not one of the available choices", None),
    ({"strict": False}, 403, "Invalid token", HTTPError),
    ({"strict": False}, 500, "any server error", HTTPError),
    ({"strict": False, "timeout": 1, "max_retries": 1, "sleep": 1}, 200, "any", None),
    ({"strict": False, "timeout": 1, "max_retries": 2, "sleep": 1}, 504, "Session timeout",
     HTTPError),  # max_retries used in old version
])
def test__retry_requests(
    api, monkeypatch: MonkeyPatch, params, resp_status_code, resp_text, error,
):
    """BaseMC._retry_requests()."""
    monkeypatch.setattr(Session, "get", mock_session(resp_status_code, resp_text))
    if error:
        with pytest.raises(error):
            api.ipam.ip_addresses._retry_requests(url="")
    else:
        response = api.ipam.ip_addresses._retry_requests(url="")
        actual = response.status_code
        assert actual == resp_status_code


def test__response_gateway_timeout():
    """BaseMC._response_gateway_timeout()."""
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
    """BaseMC._add_default_limit_offset()."""
    api_ = NbApi(host="nb")

    actual = api_.ipam.ip_addresses._add_default_limit_offset(params_d=params_d)

    assert actual == expected


@pytest.mark.parametrize("params, results, expected", [
    ({}, [], []),
    ({}, [{"count": 1, "params_d": {}}], [{"limit": 1000, "offset": 0}]),
    ({}, [{"count": 1001, "params_d": {}}],
     [{"limit": 1000, "offset": 0}, {"limit": 1000, "offset": 1000}]),
])
def test__slice_params_counters(api, params, results, expected):
    """BaseMC._slice_params_counters()."""
    actual = api.ipam.ip_addresses._slice_params_counters(results=results)
    assert actual == expected


@pytest.mark.parametrize("params, expected", [
    ({}, {}),
    ({"a": 1}, {"a": [1]}),
    ({"a": [1, 1]}, {"a": [1]}),
    ({"a": (1, 2)}, {"a": [1, 2]}),
    ({"a": 1, "b": 3}, {"a": [1], "b": [3]}),
])
def test__lists_wo_dupl(params, expected: LDAny):
    """base_mc._lists_wo_dupl()."""
    actual = base_mc._lists_wo_dupl(kwargs=params)
    assert actual == expected
