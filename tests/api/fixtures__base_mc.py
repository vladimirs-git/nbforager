"""Fixtures nbforager/api/base_mc.py."""

import pytest
import requests_mock


@pytest.fixture
def mock_requests_vrf():
    """Mock Session."""
    with requests_mock.Mocker() as mock:
        url = "https://nb/api/ipam/vrfs/?limit=1000&offset=0"
        json = {
            "results": [
                {"id": 1, "name": "VRF 1"},
                {"id": 2, "name": "VRF 2"},
            ]
        }
        mock.get(url=url, json=json)
        yield mock
