"""Tests foragers."""

import pytest

from nbforager import nb_tree
from nbforager.api.base_c import BaseC
from nbforager.foragers.ipv4 import IPv4
from nbforager.foragers.joiner import Joiner
from nbforager.nb_tree import NbTree
from tests import objects


@pytest.fixture
def joiner() -> Joiner:
    """Init Joiner with root data."""
    tree: NbTree = objects.full_tree()
    tree = nb_tree.join_tree(tree)
    joiner_ = Joiner(tree=tree)
    joiner_.init_extra_keys()
    return joiner_


@pytest.mark.parametrize("model, network", [
    ("aggregates", "10.0.0.0/16"),
    ("prefixes", "10.0.0.0/24"),
    ("ip_addresses", "10.0.0.1/24"),
])
def test__init_extra_keys(joiner: Joiner, model, network):
    """Joiner.init_extra_keys()."""
    data = getattr(joiner.tree.ipam, model)[1]
    assert data["_ipv4"] == IPv4(network)
    assert data.get("_aggregate") == {}
    assert data.get("_super_prefix") == {}
    assert data.get("_sub_prefixes") == []
    assert data.get("_ip_addresses") == []


def test__join_dcim_devices(joiner: Joiner):
    """Joiner.join_dcim_devices()."""
    joiner.join_dcim_devices()

    # device
    device_d = joiner.tree.dcim.devices[1]
    reserved_keys = BaseC._reserved_keys["dcim/devices/"]
    for key in reserved_keys:
        isinstance(device_d[key], dict)
    assert device_d["_interfaces"]["GigabitEthernet1/0/1"]["name"] == "GigabitEthernet1/0/1"
    assert device_d["_console_ports"]["CONSOLE PORT1"]["name"] == "CONSOLE PORT1"

    # interface
    interface_d = joiner.tree.dcim.interfaces[1]
    reserved_keys = BaseC._reserved_keys["dcim/interfaces/"]
    for key in reserved_keys:
        isinstance(interface_d[key], dict)
    assert interface_d["_ip_addresses"]["10.0.0.1/24"]["address"] == "10.0.0.1/24"


def test__join_virtualization_virtual_machines(joiner: Joiner):
    """Joiner.join_virtualization_virtual_machines()."""
    joiner.init_extra_keys()
    joiner.join_virtualization_virtual_machines()

    # vm
    machine_d = joiner.tree.virtualization.virtual_machines[1]
    reserved_keys = BaseC._reserved_keys["virtualization/virtual-machines/"]
    for key in reserved_keys:
        isinstance(machine_d[key], dict)
    assert machine_d["_interfaces"]["VIRTUAL_INTERFACE1"]["name"] == "VIRTUAL_INTERFACE1"

    # interface
    interface_d = joiner.tree.virtualization.interfaces[1]
    reserved_keys = BaseC._reserved_keys["virtualization/interfaces/"]
    for key in reserved_keys:
        isinstance(interface_d[key], dict)
    assert interface_d["_ip_addresses"]["10.0.0.4/24"]["address"] == "10.0.0.4/24"


def test__join_ipam_ipv4(joiner: Joiner):
    """Joiner.join_ipam_ipv4()."""
    joiner.join_ipam_ipv4()

    aggregate = joiner.tree.ipam.aggregates[1]
    assert aggregate["prefix"] == "10.0.0.0/16"
    assert aggregate["_ipv4"] == IPv4("10.0.0.0/16")
    assert aggregate["_aggregate"] == {}
    assert aggregate["_super_prefix"] == {}
    assert [d["prefix"] for d in aggregate["_sub_prefixes"]] == ["10.0.0.0/24"]
    assert aggregate["_ip_addresses"] == []

    prefix = joiner.tree.ipam.prefixes[1]
    assert prefix["prefix"] == "10.0.0.0/24"
    assert prefix["_ipv4"] == IPv4("10.0.0.0/24")
    assert prefix["_aggregate"]["prefix"] == "10.0.0.0/16"
    assert prefix["_super_prefix"] == {}
    assert [d["prefix"] for d in prefix["_sub_prefixes"]] == ["10.0.0.0/31"]
    assert [d["address"] for d in prefix["_ip_addresses"]] == ["10.0.0.1/24"]

    prefix = joiner.tree.ipam.prefixes[4]
    assert prefix["prefix"] == "10.0.0.0/31"
    assert prefix["_ipv4"] == IPv4("10.0.0.0/31")
    assert prefix["_aggregate"]["prefix"] == "10.0.0.0/16"
    assert prefix["_super_prefix"]["prefix"] == "10.0.0.0/24"
    assert [d["prefix"] for d in prefix["_sub_prefixes"]] == ["10.0.0.0/32"]
    assert prefix["_ip_addresses"] == []

    prefix = joiner.tree.ipam.prefixes[5]
    assert prefix["prefix"] == "10.0.0.0/32"
    assert prefix["_ipv4"] == IPv4("10.0.0.0/32")
    assert prefix["_aggregate"]["prefix"] == "10.0.0.0/16"
    assert prefix["_super_prefix"]["prefix"] == "10.0.0.0/31"
    assert prefix["_sub_prefixes"] == []
    assert prefix["_ip_addresses"] == []

    ip_address = joiner.tree.ipam.ip_addresses[1]
    assert ip_address["address"] == "10.0.0.1/24"
    assert ip_address["_ipv4"] == IPv4("10.0.0.1/24")
    assert ip_address["_aggregate"]["prefix"] == "10.0.0.0/16"
    assert ip_address["_super_prefix"]["prefix"] == "10.0.0.0/24"
    assert ip_address["_sub_prefixes"] == []
    assert ip_address["_ip_addresses"] == []


def test__join_ipam_aggregates(joiner: Joiner):
    """Joiner._join_ipam_aggregates()."""
    joiner._join_ipam_aggregates()

    for idx, network, sub_prefixes in [
        (1, "10.0.0.0/16", ["10.0.0.0/24"]),
        (2, "1.0.0.0/16", ["1.0.0.0/24"]),
    ]:
        data = joiner.tree.ipam.aggregates[idx]
        assert data["_ipv4"] == IPv4(network)
        assert data["_aggregate"] == {}
        assert data["_super_prefix"] == {}
        assert [d["prefix"] for d in data["_sub_prefixes"]] == sub_prefixes
        assert data["_ip_addresses"] == []

    for idx, prefix, aggregate in [
        (1, "10.0.0.0/24", "10.0.0.0/16"),
        (2, "1.0.0.0/24", "1.0.0.0/16"),
        (3, "10.0.0.0/24", None),
        (4, "10.0.0.0/31", "10.0.0.0/16"),
        (5, "10.0.0.0/32", "10.0.0.0/16"),
    ]:
        data = joiner.tree.ipam.prefixes[idx]
        assert data["prefix"] == prefix
        assert data["_aggregate"].get("prefix") == aggregate


def test__extra__join_ipam_ip_addresses(joiner: Joiner):
    """Joiner._join_ipam_ip_addresses()."""
    joiner._join_ipam_aggregates()
    joiner._join_ipam_prefixes()
    joiner._join_ipam_ip_addresses()

    for idx, network, aggregate, super_prefix, vrf in [
        (1, "10.0.0.1/24", "10.0.0.0/16", "10.0.0.0/24", False),
        (2, "1.0.0.1/24", "1.0.0.0/16", "1.0.0.0/24", False),
        (3, "10.0.0.3/24", None, None, True),
    ]:
        data = joiner.tree.ipam.ip_addresses[idx]
        assert data["_ipv4"] == IPv4(network)
        assert data["_aggregate"].get("prefix") == aggregate
        assert data["_super_prefix"].get("prefix") == super_prefix
        assert [d["prefix"] for d in data["_sub_prefixes"]] == []
        assert data["_ip_addresses"] == []
        assert bool(data["vrf"]) is vrf


def test__join_ipam_prefixes(joiner: Joiner):
    """Joiner._join_ipam_prefixes()."""
    joiner._join_ipam_aggregates()
    joiner._join_ipam_prefixes()

    for idx, network, aggregate, super_prefix, sub_prefixes, vrf in [
        (1, "10.0.0.0/24", "10.0.0.0/16", None, ["10.0.0.0/31"], False),
        (2, "1.0.0.0/24", "1.0.0.0/16", None, [], False),
        (3, "10.0.0.0/24", None, None, [], True),
        (4, "10.0.0.0/31", "10.0.0.0/16", "10.0.0.0/24", ["10.0.0.0/32"], False),
        (5, "10.0.0.0/32", "10.0.0.0/16", "10.0.0.0/31", [], False),
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
    assert unsorted == ["10.0.0.0/16", "1.0.0.0/16"]

    aggregates = joiner._get_aggregates_ip4()
    actual = [d["prefix"] for d in aggregates]
    assert actual == ["1.0.0.0/16", "10.0.0.0/16"]


def test__get_ip_addresses_ip4(joiner: Joiner):
    """Joiner._get_ip_addresses_ip4()."""
    unsorted = [d["address"] for d in joiner.tree.ipam.ip_addresses.values()]
    assert unsorted == ["10.0.0.1/24", "1.0.0.1/24", "10.0.0.3/24", "10.0.0.4/24"]

    ip_addresses = joiner._get_ip_addresses_ip4()
    actual = [d["address"] for d in ip_addresses]
    assert actual == ["1.0.0.1/24", "10.0.0.1/24"]


def test__get_prefixes_ip4(joiner: Joiner):
    """Joiner._get_prefixes_ip4()."""
    unsorted = [d["prefix"] for d in joiner.tree.ipam.prefixes.values()]
    assert unsorted == ["10.0.0.0/24", "1.0.0.0/24", "10.0.0.0/24", "10.0.0.0/31", "10.0.0.0/32"]

    prefixes = joiner._get_prefixes_ip4()
    actual = [d["prefix"] for d in prefixes]
    assert actual == ["1.0.0.0/24", "10.0.0.0/24", "10.0.0.0/31", "10.0.0.0/32"]


def test__get_prefixes_ip4_d(joiner: Joiner):
    """Joiner._get_prefixes_ip4_d()."""
    unsorted = [d["prefix"] for d in joiner.tree.ipam.prefixes.values()]
    assert unsorted == ["10.0.0.0/24", "1.0.0.0/24", "10.0.0.0/24", "10.0.0.0/31", "10.0.0.0/32"]

    prefixes_d = joiner._get_prefixes_ip4_d()
    actual = {k: [d["prefix"] for d in ld] for k, ld in prefixes_d.items()}
    assert actual == {0: ["1.0.0.0/24", "10.0.0.0/24"], 1: ["10.0.0.0/31"], 2: ["10.0.0.0/32"]}
