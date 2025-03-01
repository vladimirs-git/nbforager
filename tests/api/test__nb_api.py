"""Tests nb_pai.py."""
import inspect
from copy import copy
from typing import Any

import pytest
import requests_mock
from _pytest.monkeypatch import MonkeyPatch
from requests import Response, Session
from requests_mock import Mocker

from nbforager import helpers as h
from nbforager.exceptions import NbApiError
from nbforager.nb_api import NbApi
from nbforager.nb_tree import NbTree
from nbforager.types_ import DAny, LDAny
from tests.api.test__base_c import mock_session

ATTRS = [
    "self",
    "host",
    "token",
    "scheme",
    "port",
    "verify",
    "limit",
    "url_length",
    "threads",
    "interval",
    "timeout",
    "max_retries",
    "sleep",
    "strict",
    "extended_get",
    "default_get",
    "loners",
    "kwargs",
]


@pytest.fixture
def api():
    """Init API"""
    return NbApi(host="netbox")


@pytest.fixture
def mock_get():
    """Mock Session GET."""
    vrf1 = {"id": 1, "url": "https://netbox/api/ipam/vrfs/1/", "name": "VRF 1"}
    vrf2 = {"id": 2, "url": "https://netbox/api/ipam/vrfs/2/", "name": "VRF 1"}
    with requests_mock.Mocker() as mock:
        mock.get(url="https://netbox/api/ipam/vrfs/", json={"results": [vrf1, vrf2]})
        yield mock


@pytest.fixture
def mock_get_d():
    """Mock Session GET."""
    vrf1 = {"id": 1, "url": "https://netbox/api/ipam/vrfs/1/", "name": "VRF 1"}
    with requests_mock.Mocker() as mock:
        mock.get(
            url="https://netbox/api/ipam/vrfs/?id=1&limit=1000&offset=0",
            json={"results": [vrf1]},
        )
        yield mock


@pytest.fixture
def mock_requests_status():
    """Mock request for vrf searching."""
    with requests_mock.Mocker() as mock:
        mock.get("https://netbox/api/status/", json={"netbox-version": "3.6.5"})
        yield mock


def test__app_model(api: NbApi):
    """NbApi has the same models as NbTree object"""
    tree = NbTree()
    for app in tree.apps():
        app_o = getattr(api, app)
        actual = h.attr_name(obj=app_o)
        assert actual == app

        actual = app_o.__class__.__name__
        expected = "".join([f"{s.capitalize()}" for s in app.split("_")]) + "AC"
        assert actual == expected

        for model in getattr(tree, app).models():
            model_o = getattr(app_o, model)
            actual = h.attr_name(model_o)
            assert actual == model

            actual = model_o.__class__.__name__
            expected = "".join([f"{s.capitalize()}" for s in model.split("_")]) + "C"
            assert actual == expected


def test__init__(api: NbApi):
    """NbApi.__init__()."""
    actual = list(inspect.signature(type(api).__init__).parameters)

    expected = ATTRS
    assert set(actual).symmetric_difference(set(expected)) == set()
    assert actual == expected


def test__copy__(api: NbApi):
    """NbApi.__copy__()."""
    api_: NbApi = copy(api)

    actual = api_.host
    expected = "netbox"
    assert actual == expected


@pytest.mark.parametrize("params, expected", [
    ({"host": "netbox"}, "https://netbox/api/"),
    ({"host": "netbox", "scheme": "https"}, "https://netbox/api/"),
    ({"host": "netbox", "scheme": "http"}, "http://netbox/api/"),
])
def test__url(params, expected):
    """NbApi.url."""
    api = NbApi(**params)
    actual = api.url
    assert actual == expected


def test__threads():
    """NbApi.threads."""
    api = NbApi(host="netbox")
    assert api.threads == 1

    api.threads = 2

    expected = 2
    assert api.threads == expected
    assert api.dcim.devices.threads == expected


# ============================= methods ==============================


def test__apps(api: NbApi):
    """NbApi.apps()."""
    actual = api.apps()

    expected = [
        "circuits",
        "core",
        "dcim",
        "extras",
        "ipam",
        "plugins",
        "tenancy",
        "users",
        "virtualization",
        "wireless",
    ]
    assert actual == expected


def test__app_models(api: NbApi):
    """NbApi.app_models()."""
    actual = api.app_models()

    expected = [
        ("circuits", "circuit_terminations"),
        ("circuits", "circuit_types"),
        ("circuits", "circuits"),
        ("circuits", "provider_accounts"),
        ("circuits", "provider_networks"),
        ("circuits", "providers"),
        ("core", "data_files"),
        ("core", "data_sources"),
        ("core", "jobs"),
        ("dcim", "cable_terminations"),
        ("dcim", "cables"),
        ("dcim", "connected_device"),
        ("dcim", "console_port_templates"),
        ("dcim", "console_ports"),
        ("dcim", "console_server_port_templates"),
        ("dcim", "console_server_ports"),
        ("dcim", "device_bay_templates"),
        ("dcim", "device_bays"),
        ("dcim", "device_roles"),
        ("dcim", "device_types"),
        ("dcim", "devices"),
        ("dcim", "front_port_templates"),
        ("dcim", "front_ports"),
        ("dcim", "interface_templates"),
        ("dcim", "interfaces"),
        ("dcim", "inventory_item_roles"),
        ("dcim", "inventory_item_templates"),
        ("dcim", "inventory_items"),
        ("dcim", "locations"),
        ("dcim", "manufacturers"),
        ("dcim", "module_bay_templates"),
        ("dcim", "module_bays"),
        ("dcim", "module_types"),
        ("dcim", "modules"),
        ("dcim", "platforms"),
        ("dcim", "power_feeds"),
        ("dcim", "power_outlet_templates"),
        ("dcim", "power_outlets"),
        ("dcim", "power_panels"),
        ("dcim", "power_port_templates"),
        ("dcim", "power_ports"),
        ("dcim", "rack_reservations"),
        ("dcim", "rack_roles"),
        ("dcim", "racks"),
        ("dcim", "rear_port_templates"),
        ("dcim", "rear_ports"),
        ("dcim", "regions"),
        ("dcim", "site_groups"),
        ("dcim", "sites"),
        ("dcim", "virtual_chassis"),
        ("dcim", "virtual_device_contexts"),
        ("extras", "bookmarks"),
        ("extras", "config_contexts"),
        ("extras", "config_templates"),
        ("extras", "content_types"),
        ("extras", "custom_field_choice_sets"),
        ("extras", "custom_fields"),
        ("extras", "custom_links"),
        ("extras", "export_templates"),
        ("extras", "image_attachments"),
        ("extras", "journal_entries"),
        ("extras", "object_changes"),
        ("extras", "reports"),
        ("extras", "saved_filters"),
        ("extras", "scripts"),
        ("extras", "tags"),
        ("extras", "webhooks"),
        ("ipam", "aggregates"),
        ("ipam", "asn_ranges"),
        ("ipam", "asns"),
        ("ipam", "fhrp_group_assignments"),
        ("ipam", "fhrp_groups"),
        ("ipam", "ip_addresses"),
        ("ipam", "ip_ranges"),
        ("ipam", "l2vpn_terminations"),
        ("ipam", "l2vpns"),
        ("ipam", "prefixes"),
        ("ipam", "rirs"),
        ("ipam", "roles"),
        ("ipam", "route_targets"),
        ("ipam", "service_templates"),
        ("ipam", "services"),
        ("ipam", "vlan_groups"),
        ("ipam", "vlans"),
        ("ipam", "vrfs"),
        ("plugins", "installed_plugins"),
        ("tenancy", "contact_assignments"),
        ("tenancy", "contact_groups"),
        ("tenancy", "contact_roles"),
        ("tenancy", "contacts"),
        ("tenancy", "tenant_groups"),
        ("tenancy", "tenants"),
        ("users", "config"),
        ("users", "groups"),
        ("users", "permissions"),
        ("users", "tokens"),
        ("users", "users"),
        ("virtualization", "cluster_groups"),
        ("virtualization", "cluster_types"),
        ("virtualization", "clusters"),
        ("virtualization", "interfaces"),
        ("virtualization", "virtual_machines"),
        ("wireless", "wireless_lan_groups"),
        ("wireless", "wireless_lans"),
        ("wireless", "wireless_links"),
    ]
    assert actual == expected


def test__app_paths(api: NbApi):
    """NbApi.app_paths()."""
    actual = api.app_paths()

    expected = [
        "circuits/circuit-terminations",
        "circuits/circuit-types",
        "circuits/circuits",
        "circuits/provider-accounts",
        "circuits/provider-networks",
        "circuits/providers",
        "core/data-files",
        "core/data-sources",
        "core/jobs",
        "dcim/cable-terminations",
        "dcim/cables",
        "dcim/connected-device",
        "dcim/console-port-templates",
        "dcim/console-ports",
        "dcim/console-server-port-templates",
        "dcim/console-server-ports",
        "dcim/device-bay-templates",
        "dcim/device-bays",
        "dcim/device-roles",
        "dcim/device-types",
        "dcim/devices",
        "dcim/front-port-templates",
        "dcim/front-ports",
        "dcim/interface-templates",
        "dcim/interfaces",
        "dcim/inventory-item-roles",
        "dcim/inventory-item-templates",
        "dcim/inventory-items",
        "dcim/locations",
        "dcim/manufacturers",
        "dcim/module-bay-templates",
        "dcim/module-bays",
        "dcim/module-types",
        "dcim/modules",
        "dcim/platforms",
        "dcim/power-feeds",
        "dcim/power-outlet-templates",
        "dcim/power-outlets",
        "dcim/power-panels",
        "dcim/power-port-templates",
        "dcim/power-ports",
        "dcim/rack-reservations",
        "dcim/rack-roles",
        "dcim/racks",
        "dcim/rear-port-templates",
        "dcim/rear-ports",
        "dcim/regions",
        "dcim/site-groups",
        "dcim/sites",
        "dcim/virtual-chassis",
        "dcim/virtual-device-contexts",
        "extras/bookmarks",
        "extras/config-contexts",
        "extras/config-templates",
        "extras/content-types",
        "extras/custom-field-choice-sets",
        "extras/custom-fields",
        "extras/custom-links",
        "extras/export-templates",
        "extras/image-attachments",
        "extras/journal-entries",
        "extras/object-changes",
        "extras/reports",
        "extras/saved-filters",
        "extras/scripts",
        "extras/tags",
        "extras/webhooks",
        "ipam/aggregates",
        "ipam/asn-ranges",
        "ipam/asns",
        "ipam/fhrp-group-assignments",
        "ipam/fhrp-groups",
        "ipam/ip-addresses",
        "ipam/ip-ranges",
        "ipam/l2vpn-terminations",
        "ipam/l2vpns",
        "ipam/prefixes",
        "ipam/rirs",
        "ipam/roles",
        "ipam/route-targets",
        "ipam/service-templates",
        "ipam/services",
        "ipam/vlan-groups",
        "ipam/vlans",
        "ipam/vrfs",
        "plugins/installed-plugins",
        "tenancy/contact-assignments",
        "tenancy/contact-groups",
        "tenancy/contact-roles",
        "tenancy/contacts",
        "tenancy/tenant-groups",
        "tenancy/tenants",
        "users/config",
        "users/groups",
        "users/permissions",
        "users/tokens",
        "users/users",
        "virtualization/cluster-groups",
        "virtualization/cluster-types",
        "virtualization/clusters",
        "virtualization/interfaces",
        "virtualization/virtual-machines",
        "wireless/wireless-lan-groups",
        "wireless/wireless-lans",
        "wireless/wireless-links",
    ]
    assert actual == expected


@pytest.mark.parametrize("host, expected", [
    ("netbox2", "netbox2"),
])
def test__copy(api: NbApi, host, expected):
    """NbApi.copy()."""
    api_: NbApi = api.copy(host=host)

    actual = api_.host
    assert actual == expected


@pytest.mark.parametrize("params, expected", [
    ({"url": "https://domain.com/ipam/vrfs/", "key": "value"}, [1, 2]),
])
def test__get(
        api: NbApi,
        mock_get: Mocker,  # pylint: disable=unused-argument
        params,
        expected,
):
    """NbApi.get()."""
    api = NbApi(host="netbox")

    objects: LDAny = api.get(**params)

    actual = [d["id"] for d in objects]
    assert actual == expected


@pytest.mark.parametrize("params, expected", [
    ({"url": "https://domain.com/ipam/vrfs/1/", "key": "value"}, 1),
])
def test__get_d(
        api: NbApi,
        mock_get_d: Mocker,  # pylint: disable=unused-argument
        params,
        expected,
):
    """NbApi.get_d()."""
    api = NbApi(host="netbox")

    result: DAny = api.get_d(**params)

    actual = result["id"]
    assert actual == expected


# noinspection DuplicatedCode
@pytest.mark.parametrize("params, expected", [
    ({"id": 1, "url": "https://domain.com/ipam/ip-addresses/1", "key": "value"}, 201),
    ({"id": 1, "url": "https://domain.com/ipam/typo/", "key": "value"}, AttributeError),
    ({"id": 1, "url": "https://domain.com/ipam/", "key": "value"}, NbApiError),
])
def test__create(
        api: NbApi,
        monkeypatch: MonkeyPatch,
        params: DAny,
        expected: Any,
):
    """NbApi.create()."""
    monkeypatch.setattr(Session, "post", mock_session(expected))
    if isinstance(expected, int):
        response: Response = api.create(**params)

        actual = response.status_code
        assert actual == expected
    else:
        with pytest.raises(expected):
            api.create(**params)


# noinspection DuplicatedCode
@pytest.mark.parametrize("params, expected", [
    ({"id": 1, "url": "https://domain.com/ipam/ip-addresses/1", "key": "value"}, 201),
    ({"id": 1, "url": "https://domain.com/ipam/typo/", "key": "value"}, AttributeError),
    ({"id": 1, "url": "https://domain.com/ipam/", "key": "value"}, NbApiError),
])
def test__create_d(
        api: NbApi,
        monkeypatch: MonkeyPatch,
        params: DAny,
        expected: Any,
):
    """NbApi.create_d()."""
    content = '{"1": {"id": "1"}}'
    monkeypatch.setattr(Session, "post", mock_session(status_code=expected, content=content))
    if isinstance(expected, int):
        actual: DAny = api.create_d(**params)

        expected = {"1": {"id": "1"}}
        assert actual == expected
    else:
        with pytest.raises(expected):
            api.create_d(**params)


@pytest.mark.parametrize("url, expected", [
    ("https://domain.com/ipam/ip-addresses/1", 204),
    ("https://domain.com/ipam/ip-addresses/9", 404),
    ("https://domain.com/ipam/ip-addresses/", ValueError),
])
def test__delete(
        api: NbApi,
        monkeypatch: MonkeyPatch,
        url: str,
        expected: Any,
):
    """NbApi.delete()."""
    monkeypatch.setattr(Session, "delete", mock_session(expected))
    if isinstance(expected, int):
        response: Response = api.delete(url=url)

        actual = response.status_code
        assert actual == expected
    else:
        with pytest.raises(expected):
            api.delete(url=url)


@pytest.mark.parametrize("params, expected", [
    ({"url": "https://domain.com/ipam/ip-addresses/1", "key": "value"}, 200),
    ({"url": "https://domain.com/ipam/ip-addresses/1", "key": "value"}, 200),
    ({"url": "https://domain.com/ipam/ip-addresses/9", "key": "value"}, 400),
    ({"url": "https://domain.com/ipam/ip-addresses/0", "key": "value"}, ValueError),
    ({"url": "https://domain.com/ipam/typo/", "key": "value"}, AttributeError),
    ({"url": "https://domain.com/ipam/", "key": "value"}, NbApiError),
])
def test__update(
        api: NbApi,
        monkeypatch: MonkeyPatch,
        params: DAny,
        expected: Any,
):
    """NbApi.update()."""
    monkeypatch.setattr(Session, "patch", mock_session(expected))
    if isinstance(expected, int):
        response: Response = api.update(**params)

        actual = response.status_code
        assert actual == expected
    else:
        with pytest.raises(expected):
            api.update(**params)


def test__version(
        api: NbApi,
        mock_requests_status: Mocker,  # pylint: disable=unused-argument
):
    """NbApi.version()."""
    actual = api.version()
    assert actual == "3.6.5"
