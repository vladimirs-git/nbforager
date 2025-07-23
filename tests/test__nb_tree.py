"""Tests nb_tree.py."""
import difflib
from typing import Any

import pytest

from nbforager import nb_tree, NbApi
from nbforager.nb_tree import NbTree
from nbforager.types_ import DAny, LStr
from tests import functions as func
from tests import params as p


def test__insert_tree():
    """models.tree.insert_tree()"""
    src = NbTree()
    src.ipam.vrfs.update(func.vrf_d([1]))
    dst = NbTree()

    nb_tree.insert_tree(src=src, dst=dst)
    assert src.ipam.vrfs[1]["id"] == 1
    assert dst.ipam.vrfs[1]["id"] == 1

    src.ipam.vrfs[1]["id"] = 2
    assert src.ipam.vrfs[1]["id"] == 2
    assert dst.ipam.vrfs[1]["id"] == 2


def test__apps():
    """NbTree.apps()"""
    tree = NbTree()
    api = NbApi(host="netbox")

    actual = tree.apps()
    expected = [s for s in api.apps() if s != "plugins"]

    diff: LStr = list(difflib.ndiff(actual, expected))
    diff = [s for s in diff if s.startswith("- ") or s.startswith("+ ")]
    assert not diff


def test__clear():
    """NbTree.clear()"""
    tree = NbTree()
    tree.circuits.circuit_terminations.update({1: {}})
    tree.dcim.device_roles.update({1: {}})
    tree.ipam.aggregates.update({1: {}})
    tree.tenancy.tenant_groups.update({1: {}})
    assert tree.circuits.count() == 1
    assert tree.dcim.count() == 1
    assert tree.ipam.count() == 1
    assert tree.tenancy.count() == 1

    tree.clear()

    assert tree.circuits.count() == 0
    assert tree.dcim.count() == 0
    assert tree.ipam.count() == 0
    assert tree.tenancy.count() == 0


def test__count():
    """NbTree.count()"""
    tree = NbTree()
    tree.circuits.circuit_terminations.update({1: {}})
    tree.circuits.circuit_types.update({1: {}})
    tree.dcim.device_roles.update({1: {}})
    tree.dcim.device_types.update({1: {}, 2: {}})
    tree.ipam.aggregates.update({1: {}})
    tree.ipam.asn_ranges.update({1: {}, 2: {}, 3: {}})
    tree.tenancy.tenant_groups.update({1: {}})
    tree.tenancy.tenants.update({1: {}, 2: {}, 3: {}, 4: {}})
    assert tree.circuits.count() == 2
    assert tree.dcim.count() == 3
    assert tree.ipam.count() == 4
    assert tree.tenancy.count() == 5
    assert tree.count() == 14


def test__models():
    """NbTree.models()"""
    tree = NbTree()
    api = NbApi(host="netbox")
    apps: LStr = [s for s in api.apps() if s != "plugins"]

    for app in apps:
        actual: LStr = list(getattr(tree, app).__annotations__)
        expected: LStr = [s for s in dir(getattr(api, app)) if s[0].islower()]
        expected = [s for s in expected if s not in ["connected_device", "config"]]

        diff: LStr = list(difflib.ndiff(actual, expected))
        diff = [s for s in diff if s.startswith("- ") or s.startswith("+ ")]
        assert not diff


@pytest.mark.parametrize("child, exp_id, exp_object", [
    # url
    ({"url": f"/dcim/cables/{p.CB1}"}, p.CB1, None),
    ({"url": f"/dcim/cables/{p.CB1}/"}, p.CB1, None),  # slash
    ({"url": f"/circuits/circuit-terminations/{p.TR1}"}, p.TR1, None),
    ({"url": "/"}, AttributeError, None),
    ({"url": f"/typo/ip_addresses/{p.A1}"}, AttributeError, None),
    ({"url": f"/ipam/typo/{p.A1}"}, AttributeError, None),
    ({"url": f"/ipam/{p.A1}"}, AttributeError, None),
    ({"url": "/ipam/ip_addresses/typo"}, ValueError, None),
    ({"id": 9, "url": "/ipam/ip_addresses/9/"}, None, None),
    ({"id": 9, "url": ""}, None, None),
    ({"id": 9}, None, None),
    # object
    ({"object_id": p.CB1, "object": {"url": f"/dcim/cables/{p.CB1}"}}, None, p.CB1),
    ({"object_id": p.CB1, "object": "typo"}, None, None),
])
def test__get_child(child: Any, exp_id, exp_object):
    """nb_tree._get_child() for dict"""
    tree = func.full_tree()
    if isinstance(exp_object, int):
        assert child["object"].get("id") is None

    if isinstance(exp_id, (int, type(None))):
        child_full = nb_tree._get_child(child=child, tree=tree)
        actual = child_full.get("id")
        assert actual == exp_id

        if isinstance(exp_object, int):
            actual = child["object"].get("id")
            assert actual == exp_object

    else:
        with pytest.raises(exp_id):
            nb_tree._get_child(child=child, tree=tree)


def test__join_dcim_devices__circuit():
    """nb_tree.join_tree() circuit termination."""
    tree: NbTree = func.full_tree()

    tree = nb_tree.join_tree(tree)

    # D1_INTERFACE1--CABLE1--TERM_A-CIRCUIT1-TERM_Z--CABLE2--D2_INTERFACE1
    # D1_INTERFACE1
    nb_intf: DAny = tree.dcim.interfaces[p.D1P1]
    assert nb_intf["cable_end"] == "A"
    assert nb_intf["cable"]["id"] == p.CB1
    assert nb_intf["cable"]["a_terminations"][0]["object_type"] == "circuits.circuittermination"
    assert nb_intf["cable"]["a_terminations"][0]["object_id"] == p.TR1
    assert nb_intf["cable"]["a_terminations"][0]["object"]["circuit"]["cid"] == p.CID1
    assert nb_intf["cable"]["b_terminations"][0]["object_type"] == "dcim.interface"
    assert nb_intf["cable"]["b_terminations"][0]["object_id"] == p.D1P1
    assert nb_intf["cable"]["b_terminations"][0]["object"]["name"] == p.ETHERNET11
    assert nb_intf["link_peers_type"] == "circuits.circuittermination"
    assert nb_intf["link_peers"][0]["circuit"]["id"] == p.C1
    assert nb_intf["link_peers"][0]["link_peers_type"] == "dcim.interface"
    assert nb_intf["link_peers"][0]["link_peers"][0]["name"] == p.ETHERNET11
    # CABLE1
    nb_cable: DAny = tree.dcim.cables[p.CB1]
    assert nb_cable["a_terminations"][0]["object_type"] == "circuits.circuittermination"
    assert nb_cable["a_terminations"][0]["object_id"] == p.TR1
    assert nb_cable["a_terminations"][0]["object"]["circuit"]["cid"] == p.CID1
    assert nb_cable["b_terminations"][0]["object_type"] == "dcim.interface"
    assert nb_cable["b_terminations"][0]["object_id"] == p.D1P1
    assert nb_cable["b_terminations"][0]["object"]["name"] == p.ETHERNET11
    # CIRCUIT
    nb_circuit: DAny = tree.circuits.circuits[p.C1]
    assert nb_circuit["termination_a"]["id"] == p.TR1
    assert nb_circuit["termination_a"]["circuit"]["cid"] == p.CID1
    assert nb_circuit["termination_a"]["link_peers_type"] == "dcim.interface"
    assert nb_circuit["termination_a"]["link_peers"][0]["name"] == p.ETHERNET11
    assert nb_circuit["termination_z"]["id"] == p.TR2
    assert nb_circuit["termination_z"]["circuit"]["cid"] == p.CID1
    assert nb_circuit["termination_z"]["link_peers_type"] == "dcim.interface"
    assert nb_circuit["termination_z"]["link_peers"][0]["name"] == p.ETHERNET11
    # CABLE2
    nb_cable = tree.dcim.cables[p.CB2]
    assert nb_cable["a_terminations"][0]["object_type"] == "circuits.circuittermination"
    assert nb_cable["a_terminations"][0]["object_id"] == p.TR2
    assert nb_cable["a_terminations"][0]["object"]["circuit"]["cid"] == p.CID1
    assert nb_cable["b_terminations"][0]["object_type"] == "dcim.interface"
    assert nb_cable["b_terminations"][0]["object_id"] == p.D2P1
    assert nb_cable["b_terminations"][0]["object"]["name"] == p.ETHERNET11
    # D2_INTERFACE1
    nb_intf = tree.dcim.interfaces[p.D2P1]
    assert nb_intf["cable_end"] == "B"
    assert nb_intf["cable"]["id"] == p.CB2
    assert nb_intf["cable"]["a_terminations"][0]["object_type"] == "circuits.circuittermination"
    assert nb_intf["cable"]["a_terminations"][0]["object_id"] == p.TR2
    assert nb_intf["cable"]["a_terminations"][0]["object"]["circuit"]["cid"] == p.CID1
    assert nb_intf["cable"]["b_terminations"][0]["object_type"] == "dcim.interface"
    assert nb_intf["cable"]["b_terminations"][0]["object_id"] == p.D2P1
    assert nb_intf["cable"]["b_terminations"][0]["object"]["name"] == p.ETHERNET11
    assert nb_intf["link_peers_type"] == "circuits.circuittermination"
    assert nb_intf["link_peers"][0]["circuit"]["id"] == p.C1
    assert nb_intf["link_peers"][0]["link_peers_type"] == "dcim.interface"
    assert nb_intf["link_peers"][0]["link_peers"][0]["name"] == p.ETHERNET11

    # D1_INTERFACE2--CABLE3--D3_INTERFACE1
    # D1_INTERFACE2
    nb_intf = tree.dcim.interfaces[p.D1P2]
    assert nb_intf["cable_end"] == "A"
    assert nb_intf["cable"]["id"] == p.CB3
    assert nb_intf["cable"]["a_terminations"][0]["object_type"] == "dcim.interface"
    assert nb_intf["cable"]["a_terminations"][0]["object_id"] == p.D1P2
    assert nb_intf["cable"]["a_terminations"][0]["object"]["name"] == p.ETHERNET12
    assert nb_intf["cable"]["b_terminations"][0]["object_type"] == "dcim.interface"
    assert nb_intf["cable"]["b_terminations"][0]["object_id"] == p.D3P1
    assert nb_intf["cable"]["b_terminations"][0]["object"]["name"] == p.ETHERNET11
    assert nb_intf["link_peers_type"] == "dcim.interface"
    assert nb_intf["link_peers"][0]["cable"]["id"] == p.CB3
    assert nb_intf["link_peers"][0]["link_peers_type"] == "dcim.interface"
    assert nb_intf["link_peers"][0]["link_peers"][0]["name"] == p.ETHERNET12
    # CABLE1
    nb_cable = tree.dcim.cables[p.CB3]
    assert nb_cable["a_terminations"][0]["object_type"] == "dcim.interface"
    assert nb_cable["a_terminations"][0]["object_id"] == p.D1P2
    assert nb_cable["a_terminations"][0]["object"]["name"] == p.ETHERNET12
    assert nb_cable["b_terminations"][0]["object_type"] == "dcim.interface"
    assert nb_cable["b_terminations"][0]["object_id"] == p.D3P1
    assert nb_cable["b_terminations"][0]["object"]["name"] == p.ETHERNET11
    # D3_INTERFACE1
    nb_intf = tree.dcim.interfaces[p.D3P1]
    assert nb_intf["cable_end"] == "B"
    assert nb_intf["cable"]["id"] == p.CB3
    assert nb_intf["cable"]["a_terminations"][0]["object_id"] == p.D1P2
    assert nb_intf["cable"]["a_terminations"][0]["object"]["name"] == p.ETHERNET12
    assert nb_intf["cable"]["b_terminations"][0]["object_id"] == p.D3P1
    assert nb_intf["cable"]["b_terminations"][0]["object"]["name"] == p.ETHERNET11
    assert nb_intf["link_peers_type"] == "dcim.interface"
    assert nb_intf["link_peers"][0]["name"] == p.ETHERNET12
    assert nb_intf["link_peers"][0]["link_peers_type"] == "dcim.interface"
    assert nb_intf["link_peers"][0]["link_peers"][0]["name"] == p.ETHERNET11


@pytest.mark.parametrize("urls, expected, errors", [
    ([], [], []),
    (["/api/ipam/vrfs/1"], [], []),
    (["/api/ipam/vrfs/9"], ["/api/ipam/vrfs/9"], []),
    (["/api/typo/vrfs/1"], [], [True]),
    (["/api/ipam/typo/1"], [], [True]),
])
def test__missed_urls(caplog, urls, expected, errors):
    """nb_tree.missed_urls()"""
    tree = func.full_tree()

    actual = nb_tree.missed_urls(urls=urls, tree=tree)

    assert actual == expected
    logs = [record.levelname == "ERROR" for record in caplog.records]
    assert logs == errors


@pytest.mark.parametrize("object_type, path, expected", [
    # path=False
    ("ipam.ipaddress", False, ("ipam", "ip_addresses")),
    ("dcim.interface", False, ("dcim", "interfaces")),
    ("dcim.vminterface", False, ("dcim", "interfaces")),
    # path=True
    ("ipam.ipaddress", True, ("ipam", "ip-addresses")),
    ("dcim.interface", True, ("dcim", "interfaces")),
    ("dcim.vminterface", True, ("dcim", "interfaces")),
    # errors
    ("ipam.typo", False, ValueError),
    ("", False, ValueError),
])
def test__object_type_to_am(object_type, path, expected: Any):
    """nb_tree.object_type_to_am()"""
    if isinstance(expected, tuple):
        actual = nb_tree.object_type_to_am(object_type=object_type, path=path)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nb_tree.object_type_to_am(object_type=object_type, path=path)
