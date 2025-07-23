"""Tests nbforager.foragers.joiner.py."""
import pytest
from netports import IPv4

from nbforager import nb_tree
from nbforager.api.base_c import BaseC
from nbforager.foragers.joiner import Joiner
from nbforager.nb_tree import NbTree
from nbforager.types_ import LStr, DAny
from tests import functions as func
from tests import params as p


@pytest.fixture
def joiner() -> Joiner:
    """Init Joiner with root data."""
    tree: NbTree = func.full_tree()
    tree = nb_tree.join_tree(tree)
    joiner_ = Joiner(tree=tree)
    joiner_.init_extra_keys()
    return joiner_


@pytest.mark.parametrize("model, idx, network", [
    ("aggregates", p.AG1, p.AGGREGATE1),
    ("prefixes", p.P1, p.PREFIX1),
    ("ip_addresses", p.A1, p.ADDRESS1),
])
def test__init_extra_keys(joiner: Joiner, model, idx, network):
    """Joiner.init_extra_keys() executed in fixture."""
    data = getattr(joiner.tree.ipam, model)[idx]
    assert data["_ipv4"] == IPv4(network)
    assert data.get("_aggregate") == {}
    assert data.get("_super_prefix") == {}
    assert data.get("_sub_prefixes") == []
    assert data.get("_ip_addresses") == []


@pytest.mark.parametrize("idx, exp_hostname, exp_intfs, exp_addrs, exp_consoles", [
    (p.D1, p.HOSTNAME1, [p.ETHERNET11, p.ETHERNET12], [[p.ADDRESS1], []], [p.CONSOLE]),
    (p.D2, p.HOSTNAME2, [p.ETHERNET11], [[p.ADDRESS3]], []),
    (p.D3, p.HOSTNAME3, [p.ETHERNET11, p.ETHERNET21], [[], []], []),  # vc_master with member intfs
    (p.D4, p.HOSTNAME4, [p.ETHERNET21], [[]], []),
])
def test__join_dcim_devices(joiner: Joiner, idx, exp_hostname, exp_intfs, exp_addrs, exp_consoles):
    """Joiner.join_dcim_devices() interface, ip address."""
    joiner.join_dcim_devices()

    # extra_keys
    nb_device: DAny = joiner.tree.dcim.devices[idx]
    extra_keys: LStr = BaseC._extra_keys["dcim/devices/"]
    for key in extra_keys:
        isinstance(nb_device[key], dict)

    # device
    assert nb_device["name"] == exp_hostname
    act_intfs = list(nb_device["_interfaces"])
    assert act_intfs == exp_intfs
    act_addrs = [list(d["_ip_addresses"]) for d in nb_device["_interfaces"].values()]
    assert act_addrs == exp_addrs
    act_consoles = list(nb_device["_console_ports"])
    assert act_consoles == exp_consoles


def test__join_virtual_chassis(joiner: Joiner):
    """Joiner._join_virtual_chassis()."""
    joiner._join_virtual_chassis()

    actual = {}
    for id_, device_d in joiner.tree.dcim.devices.items():
        actual[id_] = list(device_d["_vc_members"])
    expected = {p.D1: [], p.D2: [], p.D3: [p.D4], p.D4: []}
    assert actual == expected


def test__join_ipam_ipv4(joiner: Joiner):
    """Joiner.join_ipam_ipv4()."""
    joiner.join_ipam_ipv4()

    aggregate = joiner.tree.ipam.aggregates[p.AG1]
    assert aggregate["prefix"] == p.AGGREGATE1
    assert aggregate["_ipv4"] == IPv4(p.AGGREGATE1)
    assert aggregate["_aggregate"] == {}
    assert aggregate["_super_prefix"] == {}
    assert [d["prefix"] for d in aggregate["_sub_prefixes"]] == [p.PREFIX1]
    assert aggregate["_ip_addresses"] == []

    prefix = joiner.tree.ipam.prefixes[p.P1]
    assert prefix["prefix"] == p.PREFIX1
    assert prefix["_ipv4"] == IPv4(p.PREFIX1)
    assert prefix["_aggregate"]["prefix"] == p.AGGREGATE1
    assert prefix["_super_prefix"] == {}
    assert [d["prefix"] for d in prefix["_sub_prefixes"]] == [p.PREFIX4]
    assert [d["address"] for d in prefix["_ip_addresses"]] == [p.ADDRESS1]

    prefix = joiner.tree.ipam.prefixes[p.P4]
    assert prefix["prefix"] == p.PREFIX4
    assert prefix["_ipv4"] == IPv4(p.PREFIX4)
    assert prefix["_aggregate"]["prefix"] == p.AGGREGATE1
    assert prefix["_super_prefix"]["prefix"] == p.PREFIX1
    assert [d["prefix"] for d in prefix["_sub_prefixes"]] == [p.PREFIX5]
    assert prefix["_ip_addresses"] == []

    prefix = joiner.tree.ipam.prefixes[p.P5]
    assert prefix["prefix"] == p.PREFIX5
    assert prefix["_ipv4"] == IPv4(p.PREFIX5)
    assert prefix["_aggregate"]["prefix"] == p.AGGREGATE1
    assert prefix["_super_prefix"]["prefix"] == p.PREFIX4
    assert prefix["_sub_prefixes"] == []
    assert prefix["_ip_addresses"] == []

    ip_address = joiner.tree.ipam.ip_addresses[p.A1]
    assert ip_address["address"] == p.ADDRESS1
    assert ip_address["_ipv4"] == IPv4(p.ADDRESS1)
    assert ip_address["_aggregate"]["prefix"] == p.AGGREGATE1
    assert ip_address["_super_prefix"]["prefix"] == p.PREFIX1
    assert ip_address["_sub_prefixes"] == []
    assert ip_address["_ip_addresses"] == []


def test__join_ipam_aggregates(joiner: Joiner):
    """Joiner._join_ipam_aggregates()."""
    joiner._join_ipam_aggregates()

    for idx, network, sub_prefixes in [
        (p.AG1, p.AGGREGATE1, [p.PREFIX1]),
        (p.AG2, p.AGGREGATE2, [p.PREFIX2]),
    ]:
        data = joiner.tree.ipam.aggregates[idx]
        assert data["_ipv4"] == IPv4(network)
        assert data["_aggregate"] == {}
        assert data["_super_prefix"] == {}
        assert [d["prefix"] for d in data["_sub_prefixes"]] == sub_prefixes
        assert data["_ip_addresses"] == []

    for idx, prefix, aggregate in [
        (p.P1, p.PREFIX1, p.AGGREGATE1),
        (p.P2, p.PREFIX2, p.AGGREGATE2),
        (p.P3, p.PREFIX1, None),
        (p.P4, p.PREFIX4, p.AGGREGATE1),
        (p.P5, p.PREFIX5, p.AGGREGATE1),
    ]:
        data = joiner.tree.ipam.prefixes[idx]
        assert data["prefix"] == prefix
        assert data["_aggregate"].get("prefix") == aggregate


def test__extra__join_ipam_ip_addresses(joiner: Joiner):
    """Joiner._join_ipam_ip_addresses()."""
    joiner._join_ipam_aggregates()
    joiner._join_ipam_prefixes()
    joiner._join_ipam_ip_addresses()

    for idx, network, aggregate, super_prefix, is_vrf in [
        (p.A1, p.ADDRESS1, p.AGGREGATE1, p.PREFIX1, False),
        (p.A2, p.ADDRESS2, p.AGGREGATE2, p.PREFIX2, False),
        (p.A3, p.ADDRESS3, None, None, True),
    ]:
        data = joiner.tree.ipam.ip_addresses[idx]
        assert data["_ipv4"] == IPv4(network)
        assert data["_aggregate"].get("prefix") == aggregate
        assert data["_super_prefix"].get("prefix") == super_prefix
        assert [d["prefix"] for d in data["_sub_prefixes"]] == []
        assert data["_ip_addresses"] == []
        assert bool(data["vrf"]) is is_vrf


def test__join_ipam_prefixes(joiner: Joiner):
    """Joiner._join_ipam_prefixes()."""
    joiner._join_ipam_aggregates()
    joiner._join_ipam_prefixes()

    for idx, network, aggregate, super_prefix, sub_prefixes, vrf in [
        (p.P1, p.PREFIX1, p.AGGREGATE1, None, [p.PREFIX4], False),
        (p.P2, p.PREFIX2, p.AGGREGATE2, None, [], False),
        (p.P3, p.PREFIX1, None, None, [], True),
        (p.P4, p.PREFIX4, p.AGGREGATE1, p.PREFIX1, [p.PREFIX5], False),
        (p.P5, p.PREFIX5, p.AGGREGATE1, p.PREFIX4, [], False),
    ]:
        data = joiner.tree.ipam.prefixes[idx]
        assert data["_ipv4"] == IPv4(network)
        assert data["_aggregate"].get("prefix") == aggregate
        assert data["_super_prefix"].get("prefix") == super_prefix
        assert [d["prefix"] for d in data["_sub_prefixes"]] == sub_prefixes
        assert data["_ip_addresses"] == []
        assert bool(data["vrf"]) is vrf


# ============================= helpers ==============================

def test__get_aggregates_ip4(joiner: Joiner):
    """Joiner._get_aggregates_ip4()."""
    unsorted = [d["prefix"] for d in joiner.tree.ipam.aggregates.values()]
    assert unsorted == [p.AGGREGATE1, p.AGGREGATE2]

    aggregates = joiner._get_aggregates_ip4()
    actual = [d["prefix"] for d in aggregates]
    assert actual == [p.AGGREGATE2, p.AGGREGATE1]


def test__get_ip_addresses_ip4(joiner: Joiner):
    """Joiner._get_ip_addresses_ip4()."""
    unsorted = [d["address"] for d in joiner.tree.ipam.ip_addresses.values()]
    assert unsorted == [p.ADDRESS1, p.ADDRESS2, p.ADDRESS3, p.ADDRESS4]

    ip_addresses = joiner._get_ip_addresses_ip4()
    actual = [d["address"] for d in ip_addresses]
    assert actual == [p.ADDRESS2, p.ADDRESS1]


def test__get_prefixes_ip4(joiner: Joiner):
    """Joiner._get_prefixes_ip4()."""
    unsorted = [d["prefix"] for d in joiner.tree.ipam.prefixes.values()]
    assert unsorted == [p.PREFIX1, p.PREFIX2, p.PREFIX1, p.PREFIX4, p.PREFIX5]

    prefixes = joiner._get_prefixes_ip4()
    actual = [d["prefix"] for d in prefixes]
    assert actual == [p.PREFIX2, p.PREFIX1, p.PREFIX4, p.PREFIX5]


def test__get_prefixes_ip4_d(joiner: Joiner):
    """Joiner._get_prefixes_ip4_d()."""
    unsorted = [d["prefix"] for d in joiner.tree.ipam.prefixes.values()]
    assert unsorted == [p.PREFIX1, p.PREFIX2, p.PREFIX1, p.PREFIX4, p.PREFIX5]

    prefixes_d = joiner._get_prefixes_ip4_d()
    actual = {k: [d["prefix"] for d in ld] for k, ld in prefixes_d.items()}
    assert actual == {0: [p.PREFIX2, p.PREFIX1], 1: [p.PREFIX4], 2: [p.PREFIX5]}
