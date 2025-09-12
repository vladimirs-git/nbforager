"""Tests nb_custom.py."""
from typing import Any

import pytest

from nbforager.exceptions import NbParserError
from nbforager.parser.nb_custom import NbCustom
from nbforager.types_ import DAny
from tests.parser import params__nb_parser as p


@pytest.fixture
def nbc(params: DAny) -> NbCustom:
    """Create NbValue instance based on the params."""
    return NbCustom(**params)


@pytest.mark.parametrize("params, expected", [
    ({"data": {}}, []),
    ({"data": {"custom_fields": {}}}, []),
    ({"data": {"custom_fields": {"recommended_vlans": ""}}}, []),
    ({"data": {"custom_fields": {"recommended_vlans": ","}}}, []),
    ({"data": {"custom_fields": {"recommended_vlans": "0"}}}, []),
    ({"data": {"custom_fields": {"recommended_vlans": "1,2"}}}, [1, 2]),
    ({"data": {"custom_fields": {"recommended_vlans": "2,1,0,2,"}}}, [2, 1]),
])
def test__cf_recommended_vlans(nbc, params, expected):
    """NbCustom.cf_recommended_vlans()."""
    actual = nbc.cf_recommended_vlans()
    assert actual == expected


@pytest.mark.parametrize("params, expected", [
    ({"data": {}}, False),
    ({"data": {"custom_fields": {}}}, False),
    ({"data": {"custom_fields": {"required_env": None}}}, False),
    ({"data": {"custom_fields": {"required_env": "typo"}}}, False),
    ({"data": {"custom_fields": {"required_env": False}}}, False),
    ({"data": {"custom_fields": {"required_env": True}}}, True),
])
def test__cf_required_env(nbc, params, expected: Any):
    """NbCustom.cf_required_env()."""
    actual = nbc.cf_required_env()
    assert actual == expected


@pytest.mark.parametrize("params, expected", [
    ({"data": {}}, NbParserError),
    ({"data": {"name": ""}}, NbParserError),
    ({"data": {"name": "NAME1"}}, "NAME1"),
])
def test__name(nbc, params, expected: Any):
    """NbCustom.name()."""
    if isinstance(expected, str):
        actual = nbc.name()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbc.name()


@pytest.mark.parametrize("params, expected", [
    ({"data": p.PLATFORM}, "cisco_ios"),
    ({"data": p.PLATFORM_W_VALID_NAME}, "cisco_ios"),
    ({"data": p.PLATFORM_W_VALID_SLUG}, "cisco_ios"),
    ({"data": {}}, NbParserError),
    ({"data": p.PLATFORM_WO_URL}, NbParserError),
    ({"data": p.PLATFORM_W_INVALID_ADDRESS}, NbParserError),
    ({"data": p.PLATFORM_WO_ADDRESS}, NbParserError),
    ({"data": p.PLATFORM_WO_PRIMARY_IP4}, NbParserError),
    ({"data": p.PLATFORM_WO_SLUG}, NbParserError),
    ({"data": p.PLATFORM_WO_PLATFORM}, NbParserError),
])
def test__platform_slug(nbc, params, expected: Any):
    """NbCustom.platform_slug()."""
    if isinstance(expected, str):
        actual = nbc.platform_slug()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbc.platform_slug()


@pytest.mark.parametrize("params, expected", p.HOSTS_IN_CF_FIREWALLS)
def test__hosts_in_cf_firewalls(nbc, params, expected):
    """NbCustom._hosts_in_cf_firewalls()."""
    actual = nbc._hosts_in_cf_firewalls()
    assert actual == expected


@pytest.mark.parametrize("params, expected", p.HOSTS_IN_AGGR_DESCR)
def test__hosts_in_aggr_descr(nbc, params, expected):
    """NbCustom._hosts_in_aggr_descr()."""
    if isinstance(expected, set):
        actual = nbc._hosts_in_aggr_descr()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbc._hosts_in_aggr_descr()


@pytest.mark.parametrize("params, expected", p.FIREWALLS__IN_AGGREGATE)
def test__firewalls__in_aggregate(nbc, params, expected):
    """NbCustom.firewalls__in_aggregate()."""
    actual = nbc.firewalls__in_aggregate()
    assert actual == expected
