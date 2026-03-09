"""Fixtures nbforager/api/nb_pai.py."""

import pytest
import requests_mock

from nbforager.nb_api import NbApi


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
        mock.get("https://nb/api/status/", json={"netbox-version": "3.6.5"})
        yield mock
