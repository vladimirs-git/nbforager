"""Tests nb_custom.py."""
from typing import Any

import pytest

from nbforager.exceptions import NbParserError
from nbforager.parser.nb_custom import NbCustom
from tests.parser_ import params__nb_parser as p


@pytest.mark.parametrize("data, expected", [
    ({}, []),
    ({"custom_fields": {}}, []),
    ({"custom_fields": {"recommended_vlans": ""}}, []),
    ({"custom_fields": {"recommended_vlans": ","}}, []),
    ({"custom_fields": {"recommended_vlans": "0"}}, []),
    ({"custom_fields": {"recommended_vlans": "1,2"}}, [1, 2]),
    ({"custom_fields": {"recommended_vlans": "2,1,0,2,"}}, [2, 1]),
])
def test__cf_recommended_vlans(data, expected: Any):
    """NbCustom.cf_recommended_vlans()."""
    parser = NbCustom(data=data)
    if isinstance(expected, list):
        actual = parser.cf_recommended_vlans()
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.cf_recommended_vlans()


@pytest.mark.parametrize("data, expected", [
    ({}, False),
    ({"custom_fields": {}}, False),
    ({"custom_fields": {"required_env": None}}, False),
    ({"custom_fields": {"required_env": "typo"}}, False),
    ({"custom_fields": {"required_env": False}}, False),
    ({"custom_fields": {"required_env": True}}, True),
])
def test__cf_required_env(data, expected: Any):
    """NbCustom.cf_required_env()."""
    parser = NbCustom(data=data)
    if isinstance(expected, bool):
        actual = parser.cf_required_env()
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.cf_required_env()


@pytest.mark.parametrize("data, expected", [
    ({}, NbParserError),
    ({"name": ""}, NbParserError),
    ({"name": "NAME1"}, "NAME1"),
])
def test__name(data, expected: Any):
    """NbCustom.name()."""
    parser = NbCustom(data=data)
    if isinstance(expected, str):
        actual = parser.name()
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.name()


@pytest.mark.parametrize("data, expected", p.PLATFORM_SLUG)
def test__platform_slug(data, expected: Any):
    """NbCustom.platform_slug()."""
    parser = NbCustom(data=data)
    if isinstance(expected, str):
        actual = parser.platform_slug()
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.platform_slug()


@pytest.mark.parametrize("data, strict, expected", p.HOSTS_IN_CF_FIREWALLS)
def test__hosts_in_cf_firewalls(data: dict, strict: bool, expected: Any):
    """NbCustom._hosts_in_cf_firewalls()."""
    parser = NbCustom(data=data, strict=strict)
    if isinstance(expected, set):
        actual = parser._hosts_in_cf_firewalls()
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser._hosts_in_cf_firewalls()


@pytest.mark.parametrize("data, strict, expected", p.HOSTS_IN_AGGR_DESCR)
def test__hosts_in_aggr_descr(data: dict, strict: bool, expected: Any):
    """NbCustom._hosts_in_aggr_descr()."""
    parser = NbCustom(data=data, strict=strict)
    if isinstance(expected, set):
        actual = parser._hosts_in_aggr_descr()
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser._hosts_in_aggr_descr()


@pytest.mark.parametrize("data, strict, expected", p.FIREWALLS__IN_AGGREGATE)
def test__firewalls__in_aggregate(data: dict, strict: bool, expected: Any):
    """NbCustom.firewalls__in_aggregate()."""
    parser = NbCustom(data=data, strict=strict)
    if isinstance(expected, set):
        actual = parser.firewalls__in_aggregate()
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.firewalls__in_aggregate()
