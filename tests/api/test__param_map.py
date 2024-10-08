"""Tests extended_get.py."""
import pytest

from nbforager.api import extended_get
from nbforager.api.extended_get import ParamPath


def test__param_path():
    """ParamPath()."""
    obj = ParamPath(param="name", path="app/name")
    assert obj.param == "name"
    assert obj.param_id == "name_id"
    assert obj.path == "app/name"
    assert obj.key == "name"


def test__data():
    """param_map.data() role."""
    # dcim devices
    data = extended_get.data(path="dcim/devices/")
    assert data["role"].path == "dcim/device-roles/"
    # dcim devices
    data = extended_get.data(path="dcim/racks/")
    assert data["role"].path == "dcim/rack-roles/"
    # dcim
    data = extended_get.data(path="dcim/sites/")
    assert data["circuit"].key == "cid"
    assert data["group"].path == "dcim/site-groups/"
    assert data.get("role") is None
    # ipam
    data = extended_get.data(path="ipam/ip-addresses/")
    assert data["circuit"].key == "cid"
    assert data.get("group") is None
    assert data["role"].path == "ipam/roles/"


@pytest.mark.parametrize("params_d, expected", [
    ({}, {}),
    ({"typo": [1]}, {}),
    ({"vrf": ["null"]}, {}),
    ({"vrf": ["a"]}, {"vrf": ["a"]}),
    ({"vrf": ["a", "null"]}, {"vrf": ["a", "null"]}),
    ({"present_in_vrf": ["a"]}, {"present_in_vrf": ["a"]}),
    ({"present_in_vrf": ["null"]}, {}),
    ({"circuit": ["CID1"]}, {"circuit": ["CID1"]}),
    ({"or_circuit": ["CID1"]}, {"circuit": ["CID1"]}),
    ({"or_typo": ["CID1"]}, {}),
])
def test__need_change(params_d, expected):
    """param_map.need_change()."""
    mapping = extended_get.data(path="ipam/vrfs/")
    actual = extended_get.need_change(params_d=params_d, mapping=mapping)
    assert actual == expected
