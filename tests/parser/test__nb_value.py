"""Tests nb_value.py."""

import pytest

from nbforager.exceptions import NbParserError
from nbforager.parser.nb_value import NbValue
from nbforager.types_ import DAny


@pytest.fixture
def nbv(params: DAny) -> NbValue:
    """Create NbValue instance based on the params."""
    return NbValue(**params)


@pytest.mark.parametrize("params, expected", [
    ({"data": {"address": "10.0.0.0/24"}, "strict": False}, "10.0.0.0/24"),
    ({"data": {"address": "10.0.0.1"}, "strict": False}, "10.0.0.1"),
    ({"data": {"address": None}, "strict": False}, ""),
    ({"data": {"address": 1}, "strict": False}, ""),
    ({"data": None, "strict": False}, ""),
    # strict
    ({"data": {"address": "10.0.0.0/24"}, "strict": True}, "10.0.0.0/24"),
    ({"data": {"address": "10.0.0.1"}, "strict": True}, NbParserError),
    ({"data": {"address": None}, "strict": True}, NbParserError),
    ({"data": {"address": 1}, "strict": True}, NbParserError),
    ({"data": None, "strict": True}, NbParserError),
])
def test__address(nbv, params, expected):
    """NbValue.address()."""
    if isinstance(expected, str):
        actual = nbv.address()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.address()


@pytest.mark.parametrize("params, expected", [
    ({"data": {"assigned_object": {"device": {"name": "name"}}}, "strict": False}, "name"),
    ({"data": {"assigned_object": {"device": None}}, "strict": False}, ""),
    ({"data": {"assigned_object": None}, "strict": False}, ""),
    ({"data": None, "strict": False}, ""),
    # strict
    ({"data": {"assigned_object": {"device": {"name": "name"}}}, "strict": True}, "name"),
    ({"data": {"assigned_object": {"device": None}}, "strict": True}, NbParserError),
    ({"data": {"assigned_object": None}, "strict": True}, NbParserError),
    ({"data": None, "strict": True}, NbParserError),
]
                         )
def test__assigned_device_name(nbv, params, expected):
    """NbValue.assigned_device_name()."""
    if isinstance(expected, str):
        actual = nbv.assigned_device_name()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.assigned_device_name()


@pytest.mark.parametrize("params, expected", [
    ({"data": {"id": "1"}, "strict": False}, 1),
    ({"data": {"id": 0}, "strict": False}, 0),
    ({"data": {"id": "0"}, "strict": False}, 0),
    ({"data": None, "strict": False}, 0),
    # strict
    ({"data": {"id": "1"}, "strict": True}, 1),
    ({"data": {"id": 0}, "strict": True}, 0),
    ({"data": {"id": "0"}, "strict": True}, 0),
    ({"data": None, "strict": True}, NbParserError),
])
def test__id_(nbv, params, expected):
    """NbValue.id_()."""
    if isinstance(expected, int):
        actual = nbv.id_()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.id_()


@pytest.mark.parametrize("params, expected", [
    ({"data": {"family": {"value": 4}}, "strict": False}, 4),
    ({"data": {"family": {"value": 0}}, "strict": False}, 0),
    ({"data": {"family": None}, "strict": False}, 0),
    ({"data": None, "strict": False}, 0),
    # strict
    ({"data": {"family": {"value": 4}}, "strict": True}, 4),
    ({"data": {"family": {"value": "4"}}, "strict": True}, 4),
    ({"data": {"family": {"value": 0}}, "strict": True}, NbParserError),
    ({"data": {"family": None}, "strict": True}, NbParserError),
    ({"data": None, "strict": True}, NbParserError),
])
def test__family_value(nbv, params, expected):
    """NbValue.family_value()."""
    if isinstance(expected, int):
        actual = nbv.family_value()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.family_value()


@pytest.mark.parametrize("params, expected", [
    ({"data": {"group": {"name": "name"}}, "strict": False}, "name"),
    ({"data": {"group": {"name": ""}}, "strict": False}, ""),
    ({"data": {"group": None}, "strict": False}, ""),
    ({"data": None, "strict": False}, ""),
    # strict
    ({"data": {"group": {"name": "name"}}, "strict": True}, "name"),
    ({"data": {"group": {"name": ""}}, "strict": True}, NbParserError),
    ({"data": {"group": None}, "strict": True}, NbParserError),
    ({"data": None, "strict": True}, NbParserError),
])
def test__group_name(nbv, params, expected):
    """NbValue.group_name()."""
    if isinstance(expected, str):
        actual = nbv.group_name()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.group_name()


@pytest.mark.parametrize("params, expected", [
    ({"data": {"name": "name"}, "strict": False}, "name"),
    ({"data": {"name": ""}, "strict": False}, ""),
    ({"data": None, "strict": False}, ""),
    # strict
    ({"data": {"name": "name"}, "strict": True}, "name"),
    ({"data": {"name": ""}, "strict": True}, NbParserError),
    ({"data": None, "strict": True}, NbParserError),
])
def test__name(nbv, params, expected):
    """NbValue.name()."""
    if isinstance(expected, str):
        actual = nbv.name()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.name()


@pytest.mark.parametrize("params, expected", [
    ({"data": {"prefix": "10.0.0.0/24"}, "strict": False}, "10.0.0.0/24"),
    ({"data": {"prefix": "10.0.0.0"}, "strict": False}, "10.0.0.0"),
    ({"data": {"prefix": None}, "strict": False}, ""),
    ({"data": None, "strict": False}, ""),
    # strict
    ({"data": {"prefix": "10.0.0.0/24"}, "strict": True}, "10.0.0.0/24"),
    ({"data": {"prefix": "10.0.0.0"}, "strict": True}, NbParserError),
    ({"data": {"prefix": None}, "strict": True}, NbParserError),
    ({"data": None, "strict": True}, NbParserError),
])
def test__prefix(nbv, params, expected):
    """NbValue.prefix()."""
    if isinstance(expected, str):
        actual = nbv.prefix()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.prefix()


@pytest.mark.parametrize("params, expected", [
    ({"data": {"primary_ip4": {"address": "10.0.0.1/32"}}, "strict": False}, "10.0.0.1/32"),
    ({"data": {"primary_ip4": {"address": "10.0.0.1"}}, "strict": False}, "10.0.0.1"),
    ({"data": {"primary_ip4": {"address": f"10.0.0.1_32"}}, "strict": False}, f"10.0.0.1_32"),
    ({"data": {"primary_ip4": {"address": ""}}, "strict": False}, ""),
    ({"data": {"primary_ip4": {"address": None}}, "strict": False}, ""),
    ({"data": {"primary_ip4": None}, "strict": False}, ""),
    # strict
    ({"data": {"primary_ip4": {"address": "10.0.0.1/32"}}, "strict": True}, "10.0.0.1/32"),
    ({"data": {"primary_ip4": {"address": "10.0.0.1"}}, "strict": True}, "10.0.0.1"),
    ({"data": {"primary_ip4": {"address": f"10.0.0.1_32"}}, "strict": True}, NbParserError),
    ({"data": {"primary_ip4": {"address": ""}}, "strict": True}, NbParserError),
    ({"data": {"primary_ip4": {"address": None}}, "strict": True}, NbParserError),
    ({"data": {"primary_ip4": None}, "strict": True}, NbParserError),
])
def test__primary_ip4(nbv, params, expected):
    """NbValue.primary_ip4()."""
    if isinstance(expected, str):
        actual = nbv.primary_ip4()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.primary_ip4()


@pytest.mark.parametrize("params, expected", [
    ({"data": {"primary_ip4": {"address": "10.0.0.1/32"}}, "strict": False}, "10.0.0.1"),
    ({"data": {"primary_ip4": {"address": "10.0.0.1"}}, "strict": False}, "10.0.0.1"),
    ({"data": {"primary_ip4": {"address": f"10.0.0.1_32"}}, "strict": False}, f"10.0.0.1_32"),
    ({"data": {"primary_ip4": {"address": ""}}, "strict": False}, ""),
    ({"data": {"primary_ip4": {"address": None}}, "strict": False}, ""),
    ({"data": {"primary_ip4": None}, "strict": False}, ""),
    # strict
    ({"data": {"primary_ip4": {"address": "10.0.0.1/32"}}, "strict": True}, "10.0.0.1"),
    ({"data": {"primary_ip4": {"address": "10.0.0.1"}}, "strict": True}, "10.0.0.1"),
    ({"data": {"primary_ip4": {"address": f"10.0.0.1_32"}}, "strict": True}, NbParserError),
    ({"data": {"primary_ip4": {"address": ""}}, "strict": True}, NbParserError),
    ({"data": {"primary_ip4": {"address": None}}, "strict": True}, NbParserError),
    ({"data": {"primary_ip4": None}, "strict": True}, NbParserError),
])
def test__primary_ip(nbv, params, expected):
    """NbValue.primary_ip()."""
    if isinstance(expected, str):
        actual = nbv.primary_ip()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.primary_ip()


@pytest.mark.parametrize("params, expected", [
    ({"data": {"site": {"name": "name"}}, "strict": False}, "name"),
    ({"data": {"site": {"name": ""}}, "strict": False}, ""),
    ({"data": {"site": None}, "strict": False}, ""),
    ({"data": None, "strict": False}, ""),
    # strict
    ({"data": {"site": {"name": "name"}}, "strict": True}, "name"),
    ({"data": {"site": {"name": ""}}, "strict": True}, NbParserError),
    ({"data": {"site": None}, "strict": True}, NbParserError),
    ({"data": None, "strict": True}, NbParserError),
])
def test__site_name(nbv, params, expected):
    if isinstance(expected, str):
        actual = nbv.site_name()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.site_name()


@pytest.mark.parametrize("params, expected", [
    ({"data": {"tags": [{"slug": "name"}, {"slug": "tag2"}]}, "strict": False}, ["name", "tag2"]),
    ({"data": {"tags": [{"slug": None}]}, "strict": False}, []),
    ({"data": {"tags": [None]}, "strict": False}, []),
    ({"data": {"tags": []}, "strict": False}, []),
    ({"data": {"tags": None}, "strict": False}, []),
    ({"data": None, "strict": False}, []),
    # strict
    ({"data": {"tags": [{"slug": "name"}, {"slug": "tag2"}]}, "strict": True}, ["name", "tag2"]),
    ({"data": {"tags": [{"slug": None}]}, "strict": True}, NbParserError),
    ({"data": {"tags": [None]}, "strict": True}, NbParserError),
    ({"data": {"tags": []}, "strict": True}, []),
    ({"data": {"tags": None}, "strict": True}, NbParserError),
    ({"data": None, "strict": True}, NbParserError),
])
def test__tags(nbv, params, expected):
    """NbValue.tags()."""
    if isinstance(expected, list):
        actual = nbv.tags()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.tags()


@pytest.mark.parametrize("params, expected", [
    ({"data": {"vid": "1"}, "strict": False}, 1),
    ({"data": {"vid": 0}, "strict": False}, 0),
    ({"data": {"vid": "0"}, "strict": False}, 0),
    ({"data": None, "strict": False}, 0),
    # strict
    ({"data": {"vid": "1"}, "strict": True}, 1),
    ({"data": {"vid": 0}, "strict": True}, 0),
    ({"data": {"vid": "0"}, "strict": True}, 0),
    ({"data": None, "strict": True}, NbParserError),
])
def test__vid(nbv, params, expected):
    """NbValue.vid()."""
    if isinstance(expected, int):
        actual = nbv.vid()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.vid()


@pytest.mark.parametrize("params, expected", [
    ({"data": {"vlan": {"vid": 1}}, "strict": False}, 1),
    ({"data": {"vlan": {"vid": "1"}}, "strict": False}, 1),
    ({"data": {"vlan": {"vid": 0}}, "strict": False}, 0),
    ({"data": {"vlan": {"vid": "0"}}, "strict": False}, 0),
    ({"data": {"vlan": {"vid": None}}, "strict": False}, 0),
    ({"data": {"vlan": None}, "strict": False}, 0),
    ({"data": None, "strict": False}, 0),
    # strict
    ({"data": {"vlan": {"vid": 1}}, "strict": True}, 1),
    ({"data": {"vlan": {"vid": "1"}}, "strict": True}, 1),
    ({"data": {"vlan": {"vid": 0}}, "strict": True}, 0),
    ({"data": {"vlan": {"vid": "0"}}, "strict": True}, 0),
    ({"data": {"vlan": {"vid": None}}, "strict": True}, NbParserError),
    ({"data": {"vlan": None}, "strict": True}, NbParserError),
    ({"data": None, "strict": True}, NbParserError),
])
def test__vlan_vid(nbv, params, expected):
    """NbValue.vlan_vid()."""
    if isinstance(expected, int):
        actual = nbv.vlan_vid()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.vlan_vid()


@pytest.mark.parametrize("params, expected", [
    ({"data": {"url": "name"}, "strict": False}, "name"),
    ({"data": {"url": ""}, "strict": False}, ""),
    ({"data": None, "strict": False}, ""),
    # strict
    ({"data": {"url": "name"}, "strict": True}, "name"),
    ({"data": {"url": ""}, "strict": True}, NbParserError),
    ({"data": None, "strict": True}, NbParserError),
])
def test__url(nbv, params, expected):
    """NbValue.url()."""
    if isinstance(expected, str):
        actual = nbv.url()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.url()


# ============================== is ==================================


@pytest.mark.parametrize("params, ipam, expected", [
    ({"data": {"url": "/api/ipam/prefixes/"}, "strict": False}, "prefixes", True),
    ({"data": {"url": "/api/ipam/prefixes/"}, "strict": False}, "aggregates", False),
    ({"data": {"url": "/api/ipam/aggregates/"}, "strict": False}, "aggregates", True),
    ({"data": {"url": "/api/ipam/ip-addresses/"}, "strict": False}, "ip-addresses", True),
    ({"data": {"url": None}, "strict": False}, "prefixes", False),
    # strict
    ({"data": {"url": "/api/ipam/prefixes/"}, "strict": True}, "prefixes", True),
    ({"data": {"url": "/api/ipam/prefixes/"}, "strict": True}, "aggregates", False),
    ({"data": {"url": "/api/ipam/aggregates/"}, "strict": True}, "aggregates", True),
    ({"data": {"url": "/api/ipam/ip-addresses/"}, "strict": True}, "ip-addresses", True),
    ({"data": {"url": None}, "strict": True}, "prefixes", NbParserError),
])
def test__is_ipam(nbv, params, ipam, expected):
    """NbValue.is_ipam()."""
    if isinstance(expected, bool):
        actual = nbv.is_ipam(ipam)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.is_ipam(ipam)


@pytest.mark.parametrize("params, dcim, expected", [
    ({"data": {"url": "/api/dcim/devices/"}, "strict": False}, "devices", True),
    ({"data": {"url": "/api/dcim/devices/"}, "strict": False}, "aggregates", False),
    ({"data": {"url": None}, "strict": False}, "devices", False),
    # strict
    ({"data": {"url": "/api/dcim/devices/"}, "strict": True}, "devices", True),
    ({"data": {"url": "/api/dcim/devices/"}, "strict": True}, "aggregates", False),
    ({"data": {"url": None}, "strict": True}, "devices", NbParserError),
])
def test__is_dcim(nbv, params, dcim, expected):
    """NbValue.is_dcim()."""
    if isinstance(expected, bool):
        actual = nbv.is_dcim(dcim)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.is_dcim(dcim)


@pytest.mark.parametrize("params, expected", [
    ({"data": {"vrf": "name"}, "strict": False}, True),
    ({"data": {"vrf": ""}, "strict": False}, False),
    # strict
    ({"data": {"vrf": "name"}, "strict": True}, True),
    ({"data": {"vrf": ""}, "strict": True}, False),
])
def test__is_vrf(nbv, params, expected):
    """NbValue.is_vrf()."""
    actual = nbv.is_vrf()
    assert actual == expected


# ============================= helpers ==============================


@pytest.mark.parametrize("params, subnet, expected", [
    ({"data": {}}, "10.0.0.0/24", True),
    ({"data": {}}, "10.0.0.1/32", True),
    ({"data": {}}, "10.0.0.1", False),
    ({"data": {}}, "", False),
])
def test__is_prefix(nbv, params, subnet, expected):
    """NbValue._is_prefix()."""
    actual = nbv._is_prefix(subnet)
    assert actual == expected
