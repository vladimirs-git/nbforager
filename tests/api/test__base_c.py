"""Tests nbforager/api/base_c.py."""
from typing import Any

import dictdiffer
import pytest
from netports import NetportsValueError
from requests import Response, Session, HTTPError

from nbforager.api import base_c
from tests.api import params__base_c as p
from tests.fixtures import api, api_, nbf, mock_session


# ============================= property =============================

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
    """BaseC.url_api."""
    actual = api._base_c.url_api
    assert actual == expected

    actual = nbf.api._base_c.url_api
    assert actual == expected


@pytest.mark.parametrize("params, expected", [
    ({}, "https://nb/graphql/"),
    ({"scheme": "https"}, "https://nb/graphql/"),
    ({"scheme": "http"}, "http://nb/graphql/"),
])
def test__url_graphql(api, nbf, params, expected):
    """BaseC.url_graphql."""
    actual = api._base_c.url_graphql
    assert actual == expected

    actual = nbf.api._base_c.url_graphql
    assert actual == expected

# ============================= methods ==============================

@pytest.mark.parametrize("query, status_code, content, expected", [
    ("", 200, '{"data": {}}', {"data": {}}),
    ("", 200, "{}", {}),
    ("", 403, "{}", {}),
])
def test__post_graphql(api_, monkeypatch, query, status_code, content, expected):
    """BaseC._post_graphql."""
    monkeypatch.setattr(Session, "post", mock_session(status_code, content))

    response: Response = api_._base_c._post_graphql(query=query)

    actual = response.json()
    assert actual == expected
    assert response.status_code == status_code

@pytest.mark.parametrize("status_code, content, expected", [
    (200, '{"data": {"site_list": [{"id": 1}]}}', [{"id": 1}]),  # ok
    # errors
    (200, "typo", HTTPError),  # not json
    (200, '{"errors": {}}', HTTPError),  # response with errors
    (200, '{"typo": {}}', HTTPError),  # response without data
    (200, '{"data": []}', HTTPError),  # not dict
    (200, '{"data": {"device_list": [{"id": 2}], "site_list": [{"id": 1}]}}', HTTPError),  # keys
    (200, '{"data": {"site": {"id": 1}}}', HTTPError),  # not list
    (200, '{"data": null}', HTTPError),  # empty
    (403, "{}", HTTPError),  # status_code != 200
])
def test__graphql(api_, monkeypatch, status_code, content, expected):
    """BaseC._graphql."""
    monkeypatch.setattr(Session, "post", mock_session(status_code, content))

    if isinstance(expected, list):
        actual = api_._base_c._graphql(path="dcim/sites/", fields="", filters="")

        assert actual == expected
    else:
        with pytest.raises(HTTPError):
            api_._base_c._graphql(path="dcim/sites/", fields="", filters="")

# ============================= helpers ==============================

@pytest.mark.parametrize("params, expected", [
    ({"token": "TOKEN"}, p.HEADERS),
])
def test__headers(api, nbf, params, expected):
    """BaseC._headers."""
    actual = api._base_c._headers()

    diff = list(dictdiffer.diff(actual, expected))
    assert not diff

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
    ({}, 1),
    ({"threads": -1}, 1),
    ({"threads": 0}, 1),
    ({"threads": 1}, 1),
    ({"threads": 2}, 2),
])
def test__init_threads(params, expected: Any):
    """base_c._init_threads()"""
    actual = base_c._init_threads(**params)
    assert actual == expected


@pytest.mark.parametrize("params, expected", [
    ({}, True),
    ({"verify": True}, True),
    ({"verify": False}, False),
    ({"verify": 1}, TypeError),
])
def test__init_verify(params, expected: Any):
    """base_c._init_verify()"""
    if isinstance(expected, bool):
        actual = base_c._init_verify(**params)
        assert actual == expected
    else:
        with pytest.raises(expected):
            base_c._init_verify(**params)


@pytest.mark.parametrize("params, expected", [
    ({}, "query { site_list { id } }"),
    ({"fields": "id, name"}, "query { site_list { id, name } }"),
    ({"filters": "{ status: STATUS_ACTIVE }"},
     "query { site_list ( filters: { status: STATUS_ACTIVE } ) { id } }"),
])
def test__make_graphql_query(params, expected):
    """base_c._make_graphql_query()"""
    actual = base_c._make_graphql_query(path="dcim/sites", **params)
    assert actual == expected
