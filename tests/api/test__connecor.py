"""Tests nbforager/api/connector.py."""
import json
from typing import Any

import pytest
from _pytest.monkeypatch import MonkeyPatch
from requests import Response, Session, HTTPError

from nbforager.types import DAny, LDAny
from tests.fixtures import api_, mock_session


@pytest.mark.parametrize("data, expected", [
    ({"address": "10.0.0.1/24"}, 201),
    ({}, 400),
])
def test__create(api_, monkeypatch: MonkeyPatch, data: DAny, expected: int):
    """Connector.create()."""
    monkeypatch.setattr(Session, "post", mock_session(expected))

    response: Response = api_.ipam.ip_addresses.create(**data)

    actual = response.status_code
    assert actual == expected


@pytest.mark.parametrize("data, status_code, content", [
    ({"id": 1, "status": "active"}, 201, json.dumps({"id": 1, "status": "active"})),
    ({"id": 9, "status": "active"}, 400, ""),
])
def test__create_d(api_, monkeypatch: MonkeyPatch, data: DAny, status_code: int, content: str):
    """Connector.create_d()."""
    monkeypatch.setattr(Session, "post", mock_session(status_code, content))

    actual: DAny = api_.ipam.ip_addresses.create_d(**data)

    if content:
        assert actual == data
    else:
        assert actual == {}


@pytest.mark.parametrize("content, expected", [
    ('{"results": [{"id": 1, "url": ""}]}', [1]),
    ('{"results": []}', []),
])
def test__get(api_, monkeypatch: MonkeyPatch, content, expected):
    """Connector.get()."""
    monkeypatch.setattr(Session, "get", mock_session(200, content=content))

    items: LDAny = api_.ipam.ip_addresses.get()

    actual = [d["id"] for d in items]
    assert actual == expected


@pytest.mark.parametrize("params, expected", [
    ({"address": "10.0.0.1/24"}, 1),
])
def test__get_count(api_, monkeypatch: MonkeyPatch, params, expected):
    """Connector.get_count()."""
    content = '{"results": [], "count": 1}'
    monkeypatch.setattr(Session, "get", mock_session(200, content=content))

    actual = api_.ipam.ip_addresses.get_count(**params)

    assert actual == expected


@pytest.mark.parametrize("params, content, expected", [
    ({"fields": "id"}, '{"data": {"site_list": [{"id": 1}]}}', [1]),  # ok
    ({"fields": "id"}, '{"data": null}', HTTPError),  # no data
    ({"fields": "id"}, '{"data": {"site": {"id", 1}}}', HTTPError),  # not list
    ({}, '{"data": {"site_list": [{"id": 1}]}}', TypeError),  # fields is required
])
def test__graphql(api_, monkeypatch: MonkeyPatch, params, content, expected):
    """Connector.graphql()."""
    monkeypatch.setattr(Session, "post", mock_session(200, content=content))

    if isinstance(expected, list):
        items: LDAny = api_.ipam.ip_addresses.graphql(**params)

        actual = [d["id"] for d in items]
        assert actual == expected
    else:
        with pytest.raises(expected):
            api_.ipam.ip_addresses.graphql(**params)


@pytest.mark.parametrize("data, expected", [
    ({"id": 1, "status": "active"}, 200),
    ({}, ValueError),
])
def test__update(api_, monkeypatch: MonkeyPatch, data: DAny, expected: Any):
    """Connector.update()."""
    monkeypatch.setattr(Session, "patch", mock_session(expected))
    if isinstance(expected, int):

        response: Response = api_.ipam.ip_addresses.update(**data)

        actual = response.status_code
        assert actual == expected
    else:
        with pytest.raises(expected):
            api_.ipam.ip_addresses.update(**data)


@pytest.mark.parametrize("data, status_code, content", [
    ({"id": 1, "status": "active"}, 200, json.dumps({"id": 1, "status": "active"})),
    ({"id": 9, "status": "active"}, 400, ""),
])
def test__update_d(api_, monkeypatch: MonkeyPatch, data: DAny, status_code: int, content: str):
    """Connector.update_d()."""
    monkeypatch.setattr(Session, "patch", mock_session(status_code, content))

    actual: DAny = api_.ipam.ip_addresses.update_d(**data)

    if content:
        assert actual == data
    else:
        assert actual == {}
