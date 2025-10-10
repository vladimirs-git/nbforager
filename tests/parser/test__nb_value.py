"""Tests nb_value.py."""

import pytest

from nbforager.exceptions import NbParserError
from nbforager.parser.nb_value import NbValue
from nbforager.types_ import DAny
from tests.parser import params__nb_value as p


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
    ({"data": p.NB_DEVICE_DEVICE_ROLE_WO_URL, "strict": False}, 0),
    ({"data": {"device_role": {"id": 0}}, "strict": False}, 0),
    ({"data": {"device_role": None}, "strict": False}, 0),
    ({"data": None, "strict": False}, 0),
    # strict
    ({"data": p.NB_DEVICE_DEVICE_ROLE, "strict": True}, 2),
    ({"data": p.NB_DEVICE_DEVICE_ROLE_WO_URL, "strict": True}, NbParserError),  # no url
    ({"data": {"device_role": {"id": ""}}, "strict": True}, NbParserError),  # no url
    ({"data": {"device_role": None}, "strict": True}, NbParserError),  # no url
    ({"data": None, "strict": True}, NbParserError),  # no url
])
def test__device_role_id(nbv, params, expected):
    """NbValue.device_role_id()."""
    if isinstance(expected, int):
        actual = nbv.device_role_id()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.device_role_id()


@pytest.mark.parametrize("params, data, expected", [
    # dcim/devices.device_role
    ({"version": "4.1"}, p.NB_DEVICE_DEVICE_ROLE, 2),
    ({"version": "4.1"}, p.NB_DEVICE_DEVICE_ROLE_WO_URL, 0),
    ({"version": "4.2"}, p.NB_DEVICE_DEVICE_ROLE, 2),
    ({"version": "4.2"}, p.NB_DEVICE_DEVICE_ROLE_WO_URL, 0),
    # dcim/devices.device_role strict
    ({"version": "4.1", "strict": True}, p.NB_DEVICE_DEVICE_ROLE, 2),
    ({"version": "4.1", "strict": True}, p.NB_DEVICE_DEVICE_ROLE_WO_URL, NbParserError),
    ({"version": "4.2", "strict": True}, p.NB_DEVICE_DEVICE_ROLE, 2),
    ({"version": "4.2", "strict": True}, p.NB_DEVICE_DEVICE_ROLE_WO_URL, NbParserError),
    # dcim/devices.role
    ({"version": "4.1"}, p.NB_DEVICE_ROLE, 2),
    ({"version": "4.1"}, p.NB_DEVICE_ROLE_WO_URL, 0),
    ({"version": "4.2"}, p.NB_DEVICE_ROLE, 2),
    ({"version": "4.2"}, p.NB_DEVICE_ROLE_WO_URL, 0),
    # dcim/devices.role strict
    ({"version": "4.1", "strict": True}, p.NB_DEVICE_ROLE, 2),
    ({"version": "4.1", "strict": True}, p.NB_DEVICE_ROLE_WO_URL, NbParserError),
    ({"version": "4.2", "strict": True}, p.NB_DEVICE_ROLE, 2),
    ({"version": "4.2", "strict": True}, p.NB_DEVICE_ROLE_WO_URL, NbParserError),
])
def test__device_role_id__version(params: DAny, data, expected):
    """NbValue.device_role_id() with specified version."""
    params["data"] = data
    nbv_ = NbValue(**params)
    if isinstance(expected, int):
        actual = nbv_.device_role_id()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv_.device_role_id()


@pytest.mark.parametrize("params, expected", [
    ({"data": p.NB_DEVICE_DEVICE_ROLE_WO_URL, "strict": False}, "Name"),
    ({"data": {"device_role": {"name": ""}}, "strict": False}, ""),
    ({"data": {"device_role": None}, "strict": False}, ""),
    ({"data": None, "strict": False}, ""),
    # strict
    ({"data": p.NB_DEVICE_DEVICE_ROLE, "strict": True}, "Name"),
    ({"data": p.NB_DEVICE_DEVICE_ROLE_WO_URL, "strict": True}, NbParserError),  # no url
    ({"data": {"device_role": {"name": ""}}, "strict": True}, NbParserError),  # no url
    ({"data": {"device_role": None}, "strict": True}, NbParserError),  # no url
    ({"data": None, "strict": True}, NbParserError),  # no url
])
def test__device_role_name(nbv, params, expected):
    """NbValue.device_role_name()."""
    if isinstance(expected, str):
        actual = nbv.device_role_name()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.device_role_name()


@pytest.mark.parametrize("params, data, expected", [
    # dcim/devices.device_role
    ({"version": "4.1"}, p.NB_DEVICE_DEVICE_ROLE, "Name"),
    ({"version": "4.1"}, p.NB_DEVICE_DEVICE_ROLE_WO_URL, "Name"),
    ({"version": "4.2"}, p.NB_DEVICE_DEVICE_ROLE, "Name"),
    ({"version": "4.2"}, p.NB_DEVICE_DEVICE_ROLE_WO_URL, "Name"),
    # dcim/devices.device_role strict
    ({"version": "4.1", "strict": True}, p.NB_DEVICE_DEVICE_ROLE, "Name"),
    ({"version": "4.1", "strict": True}, p.NB_DEVICE_DEVICE_ROLE_WO_URL, NbParserError),
    ({"version": "4.2", "strict": True}, p.NB_DEVICE_DEVICE_ROLE, "Name"),
    ({"version": "4.2", "strict": True}, p.NB_DEVICE_DEVICE_ROLE_WO_URL, NbParserError),
    # dcim/devices.role
    ({"version": "4.1"}, p.NB_DEVICE_ROLE, "Name"),
    ({"version": "4.1"}, p.NB_DEVICE_ROLE_WO_URL, ""),
    ({"version": "4.2"}, p.NB_DEVICE_ROLE, "Name"),
    ({"version": "4.2"}, p.NB_DEVICE_ROLE_WO_URL, ""),
    # dcim/devices.role strict
    ({"version": "4.1", "strict": True}, p.NB_DEVICE_ROLE, "Name"),
    ({"version": "4.1", "strict": True}, p.NB_DEVICE_ROLE_WO_URL, NbParserError),
    ({"version": "4.2", "strict": True}, p.NB_DEVICE_ROLE, "Name"),
    ({"version": "4.2", "strict": True}, p.NB_DEVICE_ROLE_WO_URL, NbParserError),
])
def test__device_role_name__version(params: DAny, data, expected):
    """NbValue.device_role_name() with specified version."""
    params["data"] = data
    nbv_ = NbValue(**params)
    if isinstance(expected, str):
        actual = nbv_.device_role_name()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv_.device_role_name()


@pytest.mark.parametrize("params, expected", [
    ({"data": p.NB_DEVICE_DEVICE_ROLE_WO_URL, "strict": False}, "name"),
    ({"data": {"device_role": {"slug": ""}}, "strict": False}, ""),
    ({"data": {"device_role": None}, "strict": False}, ""),
    ({"data": None, "strict": False}, ""),
    # strict
    ({"data": p.NB_DEVICE_DEVICE_ROLE, "strict": True}, "name"),
    ({"data": p.NB_DEVICE_DEVICE_ROLE_WO_URL, "strict": True}, NbParserError),  # no url
    ({"data": {"device_role": {"slug": ""}}, "strict": True}, NbParserError),  # no url
    ({"data": {"device_role": None}, "strict": True}, NbParserError),  # no url
    ({"data": None, "strict": True}, NbParserError),  # no url
])
def test__device_role_slug(nbv, params, expected):
    """NbValue.device_role_slug()."""
    if isinstance(expected, str):
        actual = nbv.device_role_slug()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.device_role_slug()


@pytest.mark.parametrize("params, data, expected", [
    # dcim/devices.device_role
    ({"version": "4.1"}, p.NB_DEVICE_DEVICE_ROLE, "name"),
    ({"version": "4.1"}, p.NB_DEVICE_DEVICE_ROLE_WO_URL, "name"),
    ({"version": "4.2"}, p.NB_DEVICE_DEVICE_ROLE, "name"),
    ({"version": "4.2"}, p.NB_DEVICE_DEVICE_ROLE_WO_URL, "name"),
    # dcim/devices.device_role strict
    ({"version": "4.1", "strict": True}, p.NB_DEVICE_DEVICE_ROLE, "name"),
    ({"version": "4.1", "strict": True}, p.NB_DEVICE_DEVICE_ROLE_WO_URL, NbParserError),
    ({"version": "4.2", "strict": True}, p.NB_DEVICE_DEVICE_ROLE, "name"),
    ({"version": "4.2", "strict": True}, p.NB_DEVICE_DEVICE_ROLE_WO_URL, NbParserError),
    # dcim/devices.role
    ({"version": "4.1"}, p.NB_DEVICE_ROLE, "name"),
    ({"version": "4.1"}, p.NB_DEVICE_ROLE_WO_URL, ""),
    ({"version": "4.2"}, p.NB_DEVICE_ROLE, "name"),
    ({"version": "4.2"}, p.NB_DEVICE_ROLE_WO_URL, ""),
    # dcim/devices.role strict
    ({"version": "4.1", "strict": True}, p.NB_DEVICE_ROLE, "name"),
    ({"version": "4.1", "strict": True}, p.NB_DEVICE_ROLE_WO_URL, NbParserError),
    ({"version": "4.2", "strict": True}, p.NB_DEVICE_ROLE, "name"),
    ({"version": "4.2", "strict": True}, p.NB_DEVICE_ROLE_WO_URL, NbParserError),
])
def test__device_role_slug__version(params: DAny, data, expected):
    """NbValue.device_role_slug() with specified version."""
    params["data"] = data
    nbv_ = NbValue(**params)
    if isinstance(expected, str):
        actual = nbv_.device_role_slug()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv_.device_role_slug()


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
    ({"data": p.NB_DEVICE_PRIMARY_IP4, "strict": False}, "10.0.0.1/32"),
    ({"data": p.NB_DEVICE_PRIMARY_IP6, "strict": False}, "::ffff:10.0.0.1/128"),
    ({"data": {"primary_ip": {"address": ""}}, "strict": False}, ""),
    ({"data": {"primary_ip": {"address": None}}, "strict": False}, ""),
    ({"data": {"primary_ip": None}, "strict": False}, ""),
    # strict
    ({"data": p.NB_DEVICE_PRIMARY_IP4, "strict": True}, "10.0.0.1/32"),
    ({"data": p.NB_DEVICE_PRIMARY_IP6, "strict": True}, "::ffff:10.0.0.1/128"),
    ({"data": {"primary_ip": {"address": "10.0.0.1"}}, "strict": True}, NbParserError),
    ({"data": {"primary_ip": {"address": "10.0.0.1_32"}}, "strict": True}, NbParserError),
    ({"data": {"primary_ip": {"address": ""}}, "strict": True}, NbParserError),
    ({"data": {"primary_ip": {"address": None}}, "strict": True}, NbParserError),
    ({"data": {"primary_ip": None}, "strict": True}, NbParserError),
])
def test__primary_ip_address(nbv, params, expected):
    """NbValue.primary_ip_address()."""
    if isinstance(expected, str):
        actual = nbv.primary_ip_address()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.primary_ip_address()


@pytest.mark.parametrize("params, expected", [
    # dcim/devices.primary_ip.family
    ({"data": p.NB_DEVICE_PRIMARY_IP4, "strict": False}, 4),
    ({"data": {"primary_ip": {"family": 0}}, "strict": False}, 0),
    ({"data": {"primary_ip": {"family": None}}, "strict": False}, 0),
    ({"data": {"primary_ip": None}, "strict": False}, 0),
    # dcim/devices.primary_ip.family strict
    ({"data": p.NB_DEVICE_PRIMARY_IP4, "strict": True}, 4),
    ({"data": {"primary_ip": {"family": ""}}, "strict": True}, NbParserError),
    ({"data": {"primary_ip": {"family": None}}, "strict": True}, NbParserError),
    ({"data": {"primary_ip": None}, "strict": True}, NbParserError),
    # dcim/devices.primary_ip.family.value
    ({"data": p.NB_DEVICE_PRIMARY_IP4_FAMILY, "strict": False}, 4),
    ({"data": {"primary_ip": {"family": {"value": 0}}}, "strict": False}, 0),
    ({"data": {"primary_ip": {"family": {"value": None}}}, "strict": False}, 0),
    ({"data": {"primary_ip": {"family": None}}, "strict": False}, 0),
    ({"data": {"primary_ip": None}, "strict": False}, 0),
    # dcim/devices.primary_ip.family.value strict
    ({"data": p.NB_DEVICE_PRIMARY_IP4_FAMILY, "strict": True}, 4),
    ({"data": {"primary_ip": {"family": ""}}, "strict": True}, NbParserError),
    ({"data": {"primary_ip": {"family": None}}, "strict": True}, NbParserError),
    ({"data": {"primary_ip": None}, "strict": True}, NbParserError),
])
def test__primary_ip_family(nbv, params, expected):
    """NbValue.primary_ip_family()."""
    if isinstance(expected, int):
        actual = nbv.primary_ip_family()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.primary_ip_family()


@pytest.mark.parametrize("params, expected", [
    ({"data": p.NB_DEVICE_PRIMARY_IP4, "strict": False}, "10.0.0.1/32"),
    ({"data": {"primary_ip4": {"address": ""}}, "strict": False}, ""),
    ({"data": {"primary_ip4": {"address": None}}, "strict": False}, ""),
    ({"data": {"primary_ip4": None}, "strict": False}, ""),
    # strict
    ({"data": p.NB_DEVICE_PRIMARY_IP4, "strict": True}, "10.0.0.1/32"),
    ({"data": {"primary_ip4": {"address": "10.0.0.1"}}, "strict": True}, NbParserError),
    ({"data": {"primary_ip4": {"address": "10.0.0.1_32"}}, "strict": True}, NbParserError),
    ({"data": {"primary_ip4": {"address": ""}}, "strict": True}, NbParserError),
    ({"data": {"primary_ip4": {"address": None}}, "strict": True}, NbParserError),
    ({"data": {"primary_ip4": None}, "strict": True}, NbParserError),
])
def test__primary_ip4_address(nbv, params, expected):
    """NbValue.primary_ip4_address()."""
    if isinstance(expected, str):
        actual = nbv.primary_ip4_address()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.primary_ip4_address()


@pytest.mark.parametrize("params, expected", [
    # dcim/devices.primary_ip4.family
    ({"data": p.NB_DEVICE_PRIMARY_IP4, "strict": False}, 4),
    ({"data": {"primary_ip4": {"family": 0}}, "strict": False}, 0),
    ({"data": {"primary_ip4": {"family": None}}, "strict": False}, 0),
    ({"data": {"primary_ip4": None}, "strict": False}, 0),
    # dcim/devices.primary_ip4.family strict
    ({"data": p.NB_DEVICE_PRIMARY_IP4, "strict": True}, 4),
    ({"data": {"primary_ip4": {"family": ""}}, "strict": True}, NbParserError),
    ({"data": {"primary_ip4": {"family": None}}, "strict": True}, NbParserError),
    ({"data": {"primary_ip4": None}, "strict": True}, NbParserError),
    # dcim/devices.primary_ip4.family.value
    ({"data": p.NB_DEVICE_PRIMARY_IP4_FAMILY, "strict": False}, 4),
    ({"data": {"primary_ip4": {"family": {"value": 0}}}, "strict": False}, 0),
    ({"data": {"primary_ip4": {"family": {"value": None}}}, "strict": False}, 0),
    ({"data": {"primary_ip4": {"family": None}}, "strict": False}, 0),
    ({"data": {"primary_ip4": None}, "strict": False}, 0),
    # dcim/devices.primary_ip4.family.value strict
    ({"data": p.NB_DEVICE_PRIMARY_IP4_FAMILY, "strict": True}, 4),
    ({"data": {"primary_ip4": {"family": ""}}, "strict": True}, NbParserError),
    ({"data": {"primary_ip4": {"family": None}}, "strict": True}, NbParserError),
    ({"data": {"primary_ip4": None}, "strict": True}, NbParserError),
])
def test__primary_ip4_family(nbv, params, expected):
    """NbValue.primary_ip4_family()."""
    if isinstance(expected, int):
        actual = nbv.primary_ip4_family()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.primary_ip4_family()


@pytest.mark.parametrize("params, expected", [
    ({"data": p.NB_PREFIX_WO_URL, "strict": False}, 2),
    ({"data": {"site": {"name": ""}}, "strict": False}, 0),
    ({"data": {"site": None}, "strict": False}, 0),
    ({"data": None, "strict": False}, 0),
    # strict
    ({"data": p.NB_PREFIX, "strict": True}, 2),
    ({"data": p.NB_PREFIX_WO_URL, "strict": True}, NbParserError),  # no url
    ({"data": {"site": {"name": ""}}, "strict": True}, NbParserError),  # no url
    ({"data": {"site": None}, "strict": True}, NbParserError),  # no url
    ({"data": None, "strict": True}, NbParserError),  # no url
])
def test__site_id(nbv, params, expected):
    """NbValue.site_id()."""
    if isinstance(expected, int):
        actual = nbv.site_id()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.site_id()


@pytest.mark.parametrize("params, data, expected", [
    # ipam/prefixes.site
    ({"version": "4.1"}, p.NB_PREFIX, 2),
    ({"version": "4.1"}, p.NB_PREFIX_WO_URL, 2),
    ({"version": "4.2"}, p.NB_PREFIX, 2),
    ({"version": "4.2"}, p.NB_PREFIX_WO_URL, 2),
    # ipam/prefixes.site strict
    ({"version": "4.1", "strict": True}, p.NB_PREFIX, 2),
    ({"version": "4.1", "strict": True}, p.NB_PREFIX_WO_URL, NbParserError),
    ({"version": "4.2", "strict": True}, p.NB_PREFIX, 2),
    ({"version": "4.2", "strict": True}, p.NB_PREFIX_WO_URL, NbParserError),
    # ipam/prefixes.scope
    ({"version": "4.1"}, p.NB_PREFIX_SCOPE_SITE, 3),
    ({"version": "4.1"}, p.NB_PREFIX_SCOPE_SITE_WO_URL, 0),
    ({"version": "4.1"}, p.NB_PREFIX_SCOPE_REGION, NbParserError),
    ({"version": "4.2"}, p.NB_PREFIX_SCOPE_SITE, 3),
    ({"version": "4.2"}, p.NB_PREFIX_SCOPE_SITE_WO_URL, 0),
    ({"version": "4.2"}, p.NB_PREFIX_SCOPE_REGION, NbParserError),
    # ipam/prefixes.scope strict
    ({"version": "4.1", "strict": True}, p.NB_PREFIX_SCOPE_SITE, 3),
    ({"version": "4.1", "strict": True}, p.NB_PREFIX_SCOPE_SITE_WO_URL, NbParserError),
    ({"version": "4.1", "strict": True}, p.NB_PREFIX_SCOPE_REGION, NbParserError),
    ({"version": "4.2", "strict": True}, p.NB_PREFIX_SCOPE_SITE, 3),
    ({"version": "4.2", "strict": True}, p.NB_PREFIX_SCOPE_SITE_WO_URL, NbParserError),
    ({"version": "4.2", "strict": True}, p.NB_PREFIX_SCOPE_REGION, NbParserError),
])
def test__site_id__version(params: DAny, data, expected):
    """NbValue.site_id() with specified version."""
    params["data"] = data
    nbv_ = NbValue(**params)
    if isinstance(expected, int):
        actual = nbv_.site_id()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv_.site_id()


@pytest.mark.parametrize("params, expected", [
    ({"data": p.NB_PREFIX_WO_URL, "strict": False}, "Name"),
    ({"data": {"site": {"name": ""}}, "strict": False}, ""),
    ({"data": {"site": None}, "strict": False}, ""),
    ({"data": None, "strict": False}, ""),
    # strict
    ({"data": p.NB_PREFIX, "strict": True}, "Name"),
    ({"data": p.NB_PREFIX_WO_URL, "strict": True}, NbParserError),  # no url
    ({"data": {"site": {"name": ""}}, "strict": True}, NbParserError),  # no url
    ({"data": {"site": None}, "strict": True}, NbParserError),  # no url
    ({"data": None, "strict": True}, NbParserError),  # no url
])
def test__site_name(nbv, params, expected):
    """NbValue.site_name()."""
    if isinstance(expected, str):
        actual = nbv.site_name()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.site_name()


@pytest.mark.parametrize("params, data, expected", [
    # ipam/prefixes.site
    ({"version": "4.1"}, p.NB_PREFIX, "Name"),
    ({"version": "4.1"}, p.NB_PREFIX_WO_URL, "Name"),
    ({"version": "4.2"}, p.NB_PREFIX, "Name"),
    ({"version": "4.2"}, p.NB_PREFIX_WO_URL, "Name"),
    # ipam/prefixes.site strict
    ({"version": "4.1", "strict": True}, p.NB_PREFIX, "Name"),
    ({"version": "4.1", "strict": True}, p.NB_PREFIX_WO_URL, NbParserError),
    ({"version": "4.2", "strict": True}, p.NB_PREFIX, "Name"),
    ({"version": "4.2", "strict": True}, p.NB_PREFIX_WO_URL, NbParserError),
    # ipam/prefixes.scope
    ({"version": "4.1"}, p.NB_PREFIX_SCOPE_SITE, "Name"),
    ({"version": "4.1"}, p.NB_PREFIX_SCOPE_SITE_WO_URL, ""),
    ({"version": "4.1"}, p.NB_PREFIX_SCOPE_REGION, NbParserError),
    ({"version": "4.2"}, p.NB_PREFIX_SCOPE_SITE, "Name"),
    ({"version": "4.2"}, p.NB_PREFIX_SCOPE_SITE_WO_URL, ""),
    ({"version": "4.2"}, p.NB_PREFIX_SCOPE_REGION, NbParserError),
    # ipam/prefixes.scope strict
    ({"version": "4.1", "strict": True}, p.NB_PREFIX_SCOPE_SITE, "Name"),
    ({"version": "4.1", "strict": True}, p.NB_PREFIX_SCOPE_SITE_WO_URL, NbParserError),
    ({"version": "4.1", "strict": True}, p.NB_PREFIX_SCOPE_REGION, NbParserError),
    ({"version": "4.2", "strict": True}, p.NB_PREFIX_SCOPE_SITE, "Name"),
    ({"version": "4.2", "strict": True}, p.NB_PREFIX_SCOPE_SITE_WO_URL, NbParserError),
    ({"version": "4.2", "strict": True}, p.NB_PREFIX_SCOPE_REGION, NbParserError),
])
def test__site_name__version(params: DAny, data, expected):
    """NbValue.site_name() with specified version."""
    params["data"] = data
    nbv_ = NbValue(**params)
    if isinstance(expected, str):
        actual = nbv_.site_name()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv_.site_name()


@pytest.mark.parametrize("params, expected", [
    ({"data": p.NB_PREFIX_WO_URL, "strict": False}, "name"),
    ({"data": {"site": {"name": ""}}, "strict": False}, ""),
    ({"data": {"site": None}, "strict": False}, ""),
    ({"data": None, "strict": False}, ""),
    # strict
    ({"data": p.NB_PREFIX, "strict": True}, "name"),
    ({"data": p.NB_PREFIX_WO_URL, "strict": True}, NbParserError),  # no url
    ({"data": {"site": {"name": ""}}, "strict": True}, NbParserError),  # no url
    ({"data": {"site": None}, "strict": True}, NbParserError),  # no url
    ({"data": None, "strict": True}, NbParserError),  # no url
])
def test__site_slug(nbv, params, expected):
    """NbValue.site_slug()."""
    if isinstance(expected, str):
        actual = nbv.site_slug()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.site_slug()


@pytest.mark.parametrize("params, data, expected", [
    # ipam/prefixes.site
    ({"version": "4.1"}, p.NB_PREFIX, "name"),
    ({"version": "4.1"}, p.NB_PREFIX_WO_URL, "name"),
    ({"version": "4.2"}, p.NB_PREFIX, "name"),
    ({"version": "4.2"}, p.NB_PREFIX_WO_URL, "name"),
    # ipam/prefixes.site strict
    ({"version": "4.1", "strict": True}, p.NB_PREFIX, "name"),
    ({"version": "4.1", "strict": True}, p.NB_PREFIX_WO_URL, NbParserError),
    ({"version": "4.2", "strict": True}, p.NB_PREFIX, "name"),
    ({"version": "4.2", "strict": True}, p.NB_PREFIX_WO_URL, NbParserError),
    # ipam/prefixes.scope
    ({"version": "4.1"}, p.NB_PREFIX_SCOPE_SITE, "name"),
    ({"version": "4.1"}, p.NB_PREFIX_SCOPE_SITE_WO_URL, ""),
    ({"version": "4.1"}, p.NB_PREFIX_SCOPE_REGION, NbParserError),
    ({"version": "4.2"}, p.NB_PREFIX_SCOPE_SITE, "name"),
    ({"version": "4.2"}, p.NB_PREFIX_SCOPE_SITE_WO_URL, ""),
    ({"version": "4.2"}, p.NB_PREFIX_SCOPE_REGION, NbParserError),
    # ipam/prefixes.scope strict
    ({"version": "4.1", "strict": True}, p.NB_PREFIX_SCOPE_SITE, "name"),
    ({"version": "4.1", "strict": True}, p.NB_PREFIX_SCOPE_SITE_WO_URL, NbParserError),
    ({"version": "4.1", "strict": True}, p.NB_PREFIX_SCOPE_REGION, NbParserError),
    ({"version": "4.2", "strict": True}, p.NB_PREFIX_SCOPE_SITE, "name"),
    ({"version": "4.2", "strict": True}, p.NB_PREFIX_SCOPE_SITE_WO_URL, NbParserError),
    ({"version": "4.2", "strict": True}, p.NB_PREFIX_SCOPE_REGION, NbParserError),
])
def test__site_slug__version(params: DAny, data, expected):
    """NbValue.site_slug() with specified version."""
    params["data"] = data
    nbv_ = NbValue(**params)
    if isinstance(expected, str):
        actual = nbv_.site_slug()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv_.site_slug()


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
    ({"data": {"url": "/api/ipam/vrf/1/"}, "strict": False}, "/api/ipam/vrf/1/"),
    ({"data": {"url": ""}, "strict": False}, ""),
    ({"data": None, "strict": False}, ""),
    # strict
    ({"data": {"url": "/api/ipam/vrf/1/"}, "strict": True}, "/api/ipam/vrf/1/"),
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

@pytest.mark.parametrize("params, expected", [
    ({"data": {"url": "/api/ipam/vrf/1/"}, "strict": False}, "/ipam/vrf/1/"),
    ({"data": {"url": "/api/core/object-changes/1/"}, "strict": False}, "/core/changelog/1/"),
    ({"data": {"url": ""}, "strict": False}, ""),
    ({"data": None, "strict": False}, ""),
    # strict
    ({"data": {"url": "/api/ipam/vrf/1/"}, "strict": False}, "/ipam/vrf/1/"),
    ({"data": {"url": "/api/core/object-changes/1/"}, "strict": False}, "/core/changelog/1/"),
    ({"data": {"url": ""}, "strict": True}, NbParserError),
    ({"data": None, "strict": True}, NbParserError),
])
def test__url_ui(nbv, params, expected):
    """NbValue.url_ui()."""
    if isinstance(expected, str):
        actual = nbv.url_ui()
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbv.url_ui()

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
