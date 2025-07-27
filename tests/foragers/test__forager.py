"""Tests forager.py."""
from typing import Any, Tuple

import dictdiffer  # type: ignore
import pytest
import requests_mock
from requests_mock import Mocker

from nbforager import nb_tree
from nbforager.nb_forager import NbForager
from nbforager.types_ import LT2StrDAny, DAny
from tests import params as p
from tests.foragers import params__forager as pf
from tests.functions import full_tree


@pytest.fixture
def nbf() -> NbForager:
    """Init NbForager without data."""
    return NbForager(host="netbox")


@pytest.fixture
def nbf_r() -> NbForager:
    """Init NbForager with NbForager.root data."""
    nbf_ = NbForager(host="netbox")
    nb_tree.insert_tree(src=full_tree(), dst=nbf_.root)
    return nbf_


@pytest.fixture
def nbf_t() -> NbForager:
    """Init NbForager."""
    nbf_ = NbForager(host="netbox")
    nb_tree.insert_tree(src=full_tree(), dst=nbf_.tree)
    return nbf_


@pytest.fixture
def connector_results(nbf: NbForager) -> Tuple[NbForager, LT2StrDAny]:
    """Fixture with common connector_results test data."""
    nb_termination: DAny = {"url": "circuit/circuit-terminations/1"}
    nbf.api.circuits.circuit_terminations._results = [nb_termination]

    nb_vrf: DAny = {"url": "ipam/vrfs/1"}
    nbf.api.ipam.vrfs._results = [nb_vrf]

    params_termination = ("circuits/circuit-terminations", {"id": [1, 2]})
    params_vrf = ("ipam/vrfs", {"id": [1, 2]})
    return nbf, [params_termination, params_vrf]


def test__interval():
    """Forager.interval()."""
    nbf = NbForager(host="netbox", interval=0.5)
    assert nbf.ipam.vrfs.interval == 0.5
    assert nbf.api.ipam.vrfs.interval == 0.5


def test__threads():
    """Forager.threads()."""
    nbf = NbForager(host="netbox", threads=2)

    expected = 2
    assert nbf.threads == expected
    assert nbf.ipam.vrfs.threads == expected
    assert nbf.api.ipam.vrfs.threads == expected

    nbf.threads = 3

    expected = 3
    assert nbf.threads == expected
    assert nbf.ipam.vrfs.threads == expected
    assert nbf.api.ipam.vrfs.threads == expected


def test__count(nbf: NbForager):
    """Forager.count()."""
    nbf.circuits.circuit_terminations.root_d.update({1: {}})
    nbf.dcim.device_roles.root_d.update({1: {}, 2: {}})
    nbf.ipam.aggregates.root_d.update({1: {}, 2: {}, 3: {}})
    nbf.tenancy.tenant_groups.root_d.update({1: {}, 2: {}, 3: {}, 4: {}})

    assert nbf.circuits.circuit_terminations.count() == 1
    assert nbf.circuits.circuit_types.count() == 0
    assert nbf.dcim.device_roles.count() == 2
    assert nbf.dcim.device_types.count() == 0
    assert nbf.ipam.aggregates.count() == 3
    assert nbf.ipam.asn_ranges.count() == 0
    assert nbf.tenancy.tenant_groups.count() == 4
    assert nbf.tenancy.tenants.count() == 0

    assert len(nbf.root.circuits.circuit_terminations) == 1
    assert len(nbf.circuits.circuit_terminations.root_d) == 1
    assert f"{nbf.circuits.circuit_terminations!r}" == "<CircuitTerminationsF: 1>"


@pytest.mark.parametrize("path, expected", [
    ("circuits/circuit-terminations", "CircuitTerminationsC"),
    ("circuits/circuit_terminations", "CircuitTerminationsC"),
    ("circuits/circuits", "CircuitsC"),
    ("ipam/ip-addresses", "IpAddressesC"),
    ("ipam/ip_addresses", "IpAddressesC"),
    ("ipam/vrfs", "VrfsC"),
    ("typo/circuits", AttributeError),
    ("circuits/typo", AttributeError),
    ("circuits", ValueError),
])
def test__get_connector(nbf: NbForager, path, expected: Any):
    """Forager.get_connector()."""
    if isinstance(expected, str):
        connector = nbf.ipam.vrfs.get_connector(path)
        actual = connector.__class__.__name__
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbf.ipam.vrfs.get_connector(path)

@pytest.mark.parametrize("nb_objects, nbf_data, expected", [
    # without root data
    ([p.VRF1_D], {}, p.NESTED_URLS_VRF1),
    ([p.VRF1_D, p.VRF2_D], {}, p.NESTED_URLS_VRF2),
    # with root data
    ([p.VRF1_D], {p.VR1: p.VRF1_D}, p.NESTED_URLS_WO_VRF1),
    ([p.VRF1_D, p.VRF2_D], {}, p.NESTED_URLS_VRF2),
    # bordr condition
    ([], {}, []),
])
def test__collect_nested_urls(nbf, nb_objects, nbf_data, expected):
    """Forager._collect_nested_urls()."""
    nbf.root.ipam.vrfs.update(nbf_data)

    actual = nbf.ipam.vrfs._collect_nested_urls(nb_objects=nb_objects)
    assert actual == expected


def test__clear_results(connector_results):
    """Forager._clear_results()."""
    nbf, path_params = connector_results

    nbf.ipam.vrfs._clear_results(path_params=path_params)

    assert nbf.api.circuits.circuit_terminations._results == []
    assert nbf.api.ipam.vrfs._results == []


def test__pop_connector_results(connector_results):
    """Forager._pop_connector_results()."""
    nbf, path_params = connector_results
    actual = nbf.ipam.vrfs._pop_connector_results(path_params=path_params)
    assert actual == [{"url": "circuit/circuit-terminations/1"}, {"url": "ipam/vrfs/1"}]
    assert nbf.api.circuits.circuit_terminations._results == []
    assert nbf.api.ipam.vrfs._results == []


@pytest.mark.parametrize("path, expected", [
    ("circuits/circuit-terminations", "A"),
    ("circuits/circuit_terminations", "A"),
    ("circuits/circuits", "B"),
    ("typo/circuits", AttributeError),
    ("circuits/typo", AttributeError),
    ("circuits", ValueError),
])
def test__get_root_data(nbf: NbForager, path, expected: Any):
    """Forager._get_root_data()."""
    nbf.root.circuits.circuit_terminations[1] = {"name": "A"}
    nbf.root.circuits.circuits[1] = {"name": "B"}
    if isinstance(expected, str):
        data = nbf.ipam.vrfs._get_root_data(path)
        actual = data[1]["name"]
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbf.ipam.vrfs.get_connector(path)


@pytest.fixture
def mock_requests_vrfs():
    """Mock Session."""
    rt1 = {"id": 1, "name": "65000:1", "url": "/ipam/route-targets/1"}
    rt2 = {"id": 2, "name": "65000:2", "url": "/ipam/route-targets/2"}
    vrf1 = {"id": 1, "name": "VRF1", "url": "ipam/vrfs/1", "import_targets": [rt1, rt2]}
    with requests_mock.Mocker() as mock:
        mock.get(
            "https://netbox/api/ipam/vrfs/?limit=1000&offset=0",
            json={"results": [vrf1]},
        )
        mock.get(
            "https://netbox/api/ipam/route-targets/?id=1&limit=1000&offset=0",
            json={"results": [rt1]},
        )
        mock.get(
            "https://netbox/api/ipam/route-targets/?id=2&limit=1000&offset=0",
            json={"results": [rt2]},
        )
        yield mock


@pytest.mark.skip(reason="Has blocking effect")
def test__get(mock_requests_vrfs: Mocker):  # pylint: disable=unused-argument
    """Forager.get().

    url_length=1 is required to check slice params and to
    mock 3 requests: ipam/vrfs, ipam/route-targets/?id=1, ipam/route-targets/?id=2.
    """
    nbf = NbForager(host="netbox", url_length=1, threads=2)
    nbf.ipam.vrfs.get()


@pytest.mark.parametrize("params, expected", pf.FIND)
def test__find_root(nbf_r: NbForager, params, expected: Any):
    """Forager.find_root().

    NbForager.tree and NbForager.root has 3 devices: DEVICE1, DEVICE2, DEVICE3.
    DEVICE1 has: tags=TAG1, device_role=DEVICE ROLE1, serial=SERIAL1
    DEVICE2 has: tags=TAG1, device_role=DEVICE ROLE1, serial=SERIAL2
    DEVICE3 has: tags=TAG3, device_role=DEVICE ROLE3, serial=SERIAL1
    """
    if isinstance(expected, list):
        results = nbf_r.dcim.devices.find_root(**params)
        actual = [d["id"] for d in results]
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbf_r.dcim.devices.find_root(**params)


@pytest.mark.parametrize("params, expected", pf.FIND)
def test__find_tree(nbf_t: NbForager, params, expected):
    """Forager.find_tree()."""
    if isinstance(expected, list):
        results = nbf_t.dcim.devices.find_tree(**params)
        actual = [d["id"] for d in results]
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbf_t.dcim.devices.find_tree(**params)


@pytest.mark.parametrize("params, expected", [
    # 1 param
    ({}, [p.P1, p.P2, p.P3, p.P4, p.P5]),
    ({"role": "role1"}, [p.P1, p.P4]),
    ({"role": "role2"}, [p.P5]),
    ({"role": "role3"}, [p.P3]),
    ({"role": "role4"}, []),
    ({"site": p.RIX1_}, [p.P1]),
    ({"site": p.RIX2_}, [p.P4, p.P5]),
    ({"site": p.RIX3_}, [p.P3]),
    ({"site": "rix4"}, []),
    ({"env": "ENV1"}, [p.P1, p.P4]),
    ({"env": "ENV2"}, [p.P5]),
    ({"env": "ENV3"}, [p.P3]),
    ({"env": "ENV4"}, []),
    # 2 params
    ({"role": "role1", "site": p.RIX1_}, [p.P1]),
    ({"role": "role1", "site": p.RIX2_}, [p.P4]),
    ({"role": "role1", "site": p.RIX3_}, []),
    ({"role": "role2", "site": p.RIX1_}, []),
    ({"role": "role2", "site": p.RIX2_}, [p.P5]),
    ({"role": "role2", "site": p.RIX3_}, []),
    ({"role": "role3", "site": p.RIX1_}, []),
    ({"role": "role3", "site": p.RIX2_}, []),
    ({"role": "role3", "site": p.RIX3_}, [p.P3]),
    ({"role": "role1", "env": "ENV1"}, [p.P1, p.P4]),
    ({"role": "role1", "env": "ENV2"}, []),
    ({"role": "role1", "env": "ENV3"}, []),
    ({"role": "role2", "env": "ENV1"}, []),
    ({"role": "role2", "env": "ENV2"}, [p.P5]),
    ({"role": "role2", "env": "ENV3"}, []),
    ({"role": "role3", "env": "ENV1"}, []),
    ({"role": "role3", "env": "ENV2"}, []),
    ({"role": "role3", "env": "ENV3"}, [p.P3]),
    ({"site": p.RIX1_, "env": "ENV1"}, [p.P1]),
    ({"site": p.RIX1_, "env": "ENV2"}, []),
    ({"site": p.RIX1_, "env": "ENV3"}, []),
    ({"site": p.RIX2_, "env": "ENV1"}, [p.P4]),
    ({"site": p.RIX2_, "env": "ENV2"}, [p.P5]),
    ({"site": p.RIX2_, "env": "ENV3"}, []),
    # 3 params
    ({"role": "role1", "site": p.RIX1_, "env": "ENV1"}, [p.P1]),
    ({"role": "role1", "site": p.RIX1_, "env": "ENV2"}, []),
    ({"role": "role1", "site": p.RIX1_, "env": "ENV3"}, []),
    ({"role": "role1", "site": p.RIX2_, "env": "ENV1"}, [p.P4]),
    ({"role": "role1", "site": p.RIX2_, "env": "ENV2"}, []),
    ({"role": "role1", "site": p.RIX2_, "env": "ENV3"}, []),
    ({"role": "role2", "site": p.RIX1_, "env": "ENV1"}, []),
    ({"role": "role2", "site": p.RIX1_, "env": "ENV2"}, []),
    ({"role": "role2", "site": p.RIX1_, "env": "ENV3"}, []),
    ({"role": "role2", "site": p.RIX2_, "env": "ENV1"}, []),
    ({"role": "role2", "site": p.RIX2_, "env": "ENV2"}, [p.P5]),
    ({"role": "role2", "site": p.RIX2_, "env": "ENV3"}, []),
])
def test__find_rse(nbf_t: NbForager, params, expected: Any):
    """Forager.find_rse()."""
    if isinstance(expected, list):
        results = nbf_t.ipam.prefixes.find_rse(**params)
        actual = [d["id"] for d in results]
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbf_t.ipam.prefixes.find_rse(**params)


@pytest.mark.parametrize("kwargs, expected", [
    ({"id": [1]}, {}),  # nested=True
    ({"id": [2]}, {"id": [2]}),  # nested=False
    ({"id": [9]}, {"id": [9]}),  # absent
    ({"id": [1, 2, 9]}, {"id": [2, 9]}),  # combo
    ({"id": {1}}, {"id": {1}}),  # not list
    ({"id": 1}, {"id": 1}),  # not list
    ({"name": "DEVICE1"}, {"name": "DEVICE1"}),
    ({"name": ["DEVICE1"]}, {"name": ["DEVICE1"]}),
    ({}, {}),
])
def test__delete_existing_nested_ids(nbf_r: NbForager, kwargs, expected):
    """Forager._delete_existing_nested_ids().

    NbForager.tree and NbForager.root has 3 devices: DEVICE1, DEVICE2, DEVICE3.
    DEVICE1 has: tags=TAG1, device_role=DEVICE ROLE1, serial=SERIAL1
    DEVICE2 has: tags=TAG1, device_role=DEVICE ROLE1, serial=SERIAL2
    DEVICE3 has: tags=TAG3, device_role=DEVICE ROLE3, serial=SERIAL1
    """
    nbf_r.root.dcim.devices = {k: v for k, v in nbf_r.root.dcim.devices.items() if k in [1, 2]}
    nbf_r.root.dcim.devices[1]["_nested"] = True
    nbf_r.root.dcim.devices[2]["_nested"] = False

    actual = nbf_r.dcim.devices._delete_existing_nested_ids(**kwargs)

    diff = list(dictdiffer.diff(actual, expected))
    assert not diff
