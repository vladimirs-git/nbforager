"""Tests nbforager/foragers/base_af.py."""

from tests.fixtures import nbf_


def test__init(nbf_):
    """BaseAF.__init__()."""
    assert nbf_.circuits.app == "circuits"
    assert nbf_.dcim.app == "dcim"
    assert nbf_.extras.app == "extras"
    assert nbf_.ipam.app == "ipam"
    assert nbf_.tenancy.app == "tenancy"
    assert nbf_.virtualization.app == "virtualization"


def test__count(nbf_):
    """BaseAF.count()."""
    nbf_.circuits.circuit_terminations.root_d.update({1: {}})
    nbf_.circuits.circuit_types.root_d.update({1: {}})
    nbf_.dcim.device_roles.root_d.update({1: {}})
    nbf_.dcim.device_types.root_d.update({1: {}, 2: {}})
    nbf_.ipam.aggregates.root_d.update({1: {}})
    nbf_.ipam.asn_ranges.root_d.update({1: {}, 2: {}, 3: {}})
    nbf_.tenancy.tenant_groups.root_d.update({1: {}})
    nbf_.tenancy.tenants.root_d.update({1: {}, 2: {}, 3: {}, 4: {}})
    assert nbf_.circuits.count() == 2
    assert nbf_.dcim.count() == 3
    assert nbf_.ipam.count() == 4
    assert nbf_.tenancy.count() == 5

    assert len(nbf_.root.circuits.circuit_terminations) == 1
    assert len(nbf_.circuits.circuit_terminations.root_d) == 1
    assert f"{nbf_.circuits!r}" == "<CircuitsAF: 2>"
