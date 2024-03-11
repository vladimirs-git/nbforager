"""Unittests nb_value.py."""
from typing import Any

import pytest

from nbforager.parser.nb_value import NbValue
from nbforager.types_ import LStr
from tests.parser_ import params__nb_parser as p


@pytest.mark.parametrize("data, strict, expected", p.ADDRESS)
def test__address(data: dict, strict: bool, expected: Any):
    """NbValue.address()."""
    parser = NbValue(data=data, strict=strict)
    if isinstance(expected, str):
        actual = parser.address()
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.address()


@pytest.mark.parametrize("data, strict, expected", p.ASSIGNED_DEVICE_NAME)
def test__assigned_device_name(data: dict, strict: bool, expected: Any):
    """NbValue.assigned_device_name()."""
    parser = NbValue(data=data, strict=strict)
    if isinstance(expected, str):
        actual = parser.assigned_device_name()
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.assigned_device_name()


@pytest.mark.parametrize("keys, data, strict, expected", p.ID_)
def test__id_(keys: LStr, data: dict, strict: bool, expected: Any):
    """NbValue.id_()."""
    _ = keys  # noqa
    parser = NbValue(data=data, strict=strict)
    if isinstance(expected, int):
        actual = parser.id_()
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.id_()


@pytest.mark.parametrize("data, strict, expected", p.GROUP_NAME)
def test__group_name(data: dict, strict: bool, expected: Any):
    """NbValue.group_name()."""
    parser = NbValue(data=data, strict=strict)
    if isinstance(expected, str):
        actual = parser.group_name()
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.group_name()


@pytest.mark.parametrize("data, strict, expected", p.NAME_)
def test__name(data: dict, strict: bool, expected: Any):
    """NbValue.name()."""
    parser = NbValue(data=data, strict=strict)
    if isinstance(expected, str):
        actual = parser.name()
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.name()


@pytest.mark.parametrize("data, strict, expected", p.PREFIX_)
def test__prefix(data: dict, strict: bool, expected: Any):
    """NbValue.prefix()."""
    parser = NbValue(data=data, strict=strict)
    if isinstance(expected, str):
        actual = parser.prefix()
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.prefix()


@pytest.mark.parametrize("data, strict, expected", p.PRIMARY_IP4)
def test__primary_ip4(data: dict, strict: bool, expected: Any):
    """NbValue.primary_ip4()."""
    parser = NbValue(data=data, strict=strict)
    if isinstance(expected, str):
        actual = parser.primary_ip4()
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.primary_ip4()


@pytest.mark.parametrize("data, strict, expected", p.PRIMARY_IP)
def test__primary_ip(data: dict, strict: bool, expected: Any):
    """NbValue.primary_ip()."""
    parser = NbValue(data=data, strict=strict)
    if isinstance(expected, str):
        actual = parser.primary_ip()
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.primary_ip()


@pytest.mark.parametrize("data, strict, upper, expected", p.SITE_NAME)
def test__site_name(data: dict, strict: bool, upper: bool, expected: Any):
    """NbValue.site_name()."""
    parser = NbValue(data=data, strict=strict)
    if isinstance(expected, str):
        actual = parser.site_name(upper=upper)
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.site_name()


@pytest.mark.parametrize("data, strict, expected", p.TAGS)
def test__tags(data: dict, strict: bool, expected: Any):
    """NbValue.tags()."""
    parser = NbValue(data=data, strict=strict)
    if isinstance(expected, list):
        actual = parser.tags()
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.tags()


@pytest.mark.parametrize("data, strict, expected", p.GET_VID)
def test__vid(data: dict, strict: bool, expected: Any):
    """NbValue.vid()."""
    parser = NbValue(data=data, strict=strict)
    if isinstance(expected, int):
        actual = parser.vid()
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.vid()


@pytest.mark.parametrize("data, strict, expected", p.GET_VLAN_VID)
def test__vlan_vid(data: dict, strict: bool, expected: Any):
    """NbValue.vlan_vid()."""
    parser = NbValue(data=data, strict=strict)
    if isinstance(expected, int):
        actual = parser.vlan_vid()
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.vlan_vid()


@pytest.mark.parametrize("data, strict, expected", p.URL)
def test__url(data: dict, strict: bool, expected: Any):
    """NbValue.url()."""
    parser = NbValue(data=data, strict=strict)
    if isinstance(expected, str):
        actual = parser.url()
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.url()


# ============================== is ==================================


@pytest.mark.parametrize("data, strict, ipam, expected", p.IS_IPAM)
def test__is_ipam(data: dict, strict: bool, ipam: str, expected: Any):
    """NbValue.is_ipam()."""
    parser = NbValue(data=data, strict=strict)
    if isinstance(expected, bool):
        actual = parser.is_ipam(ipam)
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.is_ipam(ipam)


@pytest.mark.parametrize("data, strict, dcim, expected", p.IS_DCIM)
def test__is_dcim(data: dict, strict: bool, dcim: str, expected: Any):
    """NbValue.is_dcim()."""
    parser = NbValue(data=data, strict=strict)
    if isinstance(expected, bool):
        actual = parser.is_dcim(dcim)
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.is_dcim(dcim)


@pytest.mark.parametrize("data, strict, expected", p.IS_VRF)
def test__is_vrf(data: dict, strict: bool, expected: Any):
    """NbValue.is_vrf()."""
    parser = NbValue(data=data, strict=strict)
    if isinstance(expected, bool):
        actual = parser.is_vrf()
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.is_vrf()


# ============================= helpers ==============================


@pytest.mark.parametrize("subnet, expected", p.IS_PREFIX)
def test__is_prefix(subnet: str, expected: Any):
    """NbValue.is_prefix()."""
    parser = NbValue(data={})
    if isinstance(expected, bool):
        actual = parser._is_prefix(subnet)
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser._is_prefix(subnet)
