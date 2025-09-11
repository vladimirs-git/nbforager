"""Params."""
from copy import deepcopy

from nbforager.exceptions import NbParserError
from nbforager.types_ import DAny

# ====================== universal get methods =======================

STRICT_DICT = [
    (["a"], {"data": {"a": {"k": "v"}}, "strict": True}, {"k": "v"}),
    (["a"], {"data": {"a": {"k": "v"}}, "strict": False}, {"k": "v"}),
    (["a"], {"data": {"a": 0}, "strict": True}, NbParserError),
    (["a"], {"data": {"a": 0}, "strict": False}, NbParserError),
    (["a"], {"data": {"url": "https://"}, "strict": True}, NbParserError),
    (["a"], {"data": {"url": "https://"}, "strict": False}, NbParserError),
]

STRICT_INT = [
    (["a"], {"data": {"a": 1}, "strict": True}, 1),
    (["a"], {"data": {"a": 1}, "strict": False}, 1),
    (["a"], {"data": {"a": 0}, "strict": True}, NbParserError),
    (["a"], {"data": {"a": 0}, "strict": False}, NbParserError),
    (["a"], {"data": {"url": "https://"}, "strict": True}, NbParserError),
    (["a"], {"data": {"url": "https://"}, "strict": False}, NbParserError),
]

STRICT_LIST = [
    (["a"], {"data": {"a": ["A"]}, "strict": True}, ["A"]),
    (["a"], {"data": {"a": ["A"]}, "strict": False}, ["A"]),
    (["a"], {"data": {"a": []}, "strict": True}, NbParserError),
    (["a"], {"data": {"a": []}, "strict": False}, NbParserError),
    (["a"], {"data": {"url": "https://"}, "strict": True}, NbParserError),
    (["a"], {"data": {"url": "https://"}, "strict": False}, NbParserError),
]

STRICT_STR = [
    (["a"], {"data": {"a": "A"}, "strict": True}, "A"),
    (["a"], {"data": {"a": "A"}, "strict": False}, "A"),
    (["a"], {"data": {"a": ""}, "strict": True}, NbParserError),
    (["a"], {"data": {"a": ""}, "strict": False}, NbParserError),
    (["a"], {"data": {"url": "https://"}, "strict": True}, NbParserError),
    (["a"], {"data": {"url": "https://"}, "strict": False}, NbParserError),
]

# ============================= methods ==============================


GROUP_NAME = [
    ({"data": {"group": {"name": "name"}}, "strict": True}, "name"),
    ({"data": {"group": {"name": "name"}}, "strict": False}, "name"),
    ({"data": {"group": {"name": ""}}, "strict": True}, NbParserError),
    ({"data": {"group": {"name": ""}}, "strict": False}, ""),
    ({"data": {"group": None}, "strict": True}, NbParserError),
    ({"data": {"group": None}, "strict": False}, ""),
    ({"data": None, "strict": True}, NbParserError),
    ({"data": None, "strict": False}, ""),
]

GET_VID = [
    ({"data": {"vid": "1"}, "strict": True}, 1),
    ({"data": {"vid": "1"}, "strict": False}, 1),
    ({"data": {"vid": 0}, "strict": True}, 0),
    ({"data": {"vid": 0}, "strict": False}, 0),
    ({"data": {"vid": "0"}, "strict": True}, 0),
    ({"data": {"vid": "0"}, "strict": False}, 0),
    ({"data": None, "strict": True}, NbParserError),
    ({"data": None, "strict": False}, 0),
]

PLATFORM_D: DAny = {
    "url": "/api/dcim/devices/",
    "primary_ip4": {"address": "10.0.0.1/24"},
    "platform": {"name": "Cisco IOS", "slug": "cisco_ios"},
}
PLATFORM_D_W_VALID_NAME = deepcopy(PLATFORM_D)
PLATFORM_D_W_VALID_NAME["platform"]["name"] = "cisco_ios"
PLATFORM_D_W_VALID_SLUG = deepcopy(PLATFORM_D)
PLATFORM_D_W_VALID_SLUG["platform"]["slug"] = "cisco-ios"
PLATFORM_D_WO_URL = deepcopy(PLATFORM_D)
del PLATFORM_D_WO_URL["url"]
PLATFORM_D_W_INVALID_ADDRESS = deepcopy(PLATFORM_D)
PLATFORM_D_W_INVALID_ADDRESS["primary_ip4"]["address"] = "typo"
PLATFORM_D_WO_ADDRESS = deepcopy(PLATFORM_D)
del PLATFORM_D_WO_ADDRESS["primary_ip4"]["address"]
PLATFORM_D_WO_PRIMARY_IP4 = deepcopy(PLATFORM_D)
del PLATFORM_D_WO_PRIMARY_IP4["primary_ip4"]
PLATFORM_D_WO_SLUG = deepcopy(PLATFORM_D)
del PLATFORM_D_WO_SLUG["platform"]["slug"]
PLATFORM_D_WO_PLATFORM = deepcopy(PLATFORM_D)
del PLATFORM_D_WO_PLATFORM["platform"]

NAME1 = "a-b-c-d"
NAME2 = "A-B-C-D"
HOSTS_IN_CF_FIREWALLS = [
    ({"data": {"custom_fields": {"firewalls": f"{NAME1} {NAME2}"}}, "strict": True},
     {NAME1, NAME2}),
    ({"data": {"custom_fields": {"firewalls": f"{NAME1},{NAME2}"}}, "strict": True},
     {NAME1, NAME2}),
    ({"data": {"custom_fields": {"firewalls": f"{NAME1}, {NAME2}"}}, "strict": True},
     {NAME1, NAME2}),
    ({"data": {"custom_fields": {"firewalls": f"{NAME1}, {NAME2}"}}, "strict": False},
     {NAME1, NAME2}),
    ({"data": {"custom_fields": {"firewalls": ""}}, "strict": True}, set()),
    ({"data": {"custom_fields": {"firewalls": ""}}, "strict": False}, set()),
    ({"data": {"custom_fields": None}, "strict": True}, set()),
    ({"data": {"custom_fields": None}, "strict": False}, set()),
    ({"data": None, "strict": True}, set()),
    ({"data": None, "strict": False}, set()),
]

TAG = "noc_aggregates_belonging"
HOSTS_IN_AGGR_DESCR = [
    ({"data": {"description": f"\t{NAME1},{NAME2} a", "tags": [{"slug": TAG}]}, "strict": True},
     {NAME1, NAME2}),
    ({"data": {"description": f"a:{NAME1}, {NAME2}.a", "tags": [{"slug": TAG}]}, "strict": True},
     {NAME1, NAME2}),
    ({"data": {"description": f"{NAME1} {NAME2} a", "tags": [{"slug": TAG}]}, "strict": True},
     {NAME1, NAME2}),
    ({"data": {"description": f"{NAME1} {NAME2} a", "tags": [{"slug": TAG}]}, "strict": False},
     {NAME1, NAME2}),
    ({"data": {"description": "a", "tags": [{"slug": TAG}]}, "strict": True}, set()),
    ({"data": {"description": "a", "tags": [{"slug": TAG}]}, "strict": False}, set()),
    ({"data": {"description": "", "tags": [{"slug": TAG}]}, "strict": True}, set()),
    ({"data": {"description": "", "tags": [{"slug": TAG}]}, "strict": False}, set()),
    ({"data": {"description": "", "tags": [None]}, "strict": True}, NbParserError),
    ({"data": {"description": "", "tags": [None]}, "strict": False}, set()),
]

TAG = "noc_aggregates_belonging"
FIREWALLS__IN_AGGREGATE = [
    ({"data": {"custom_fields": {"firewalls": NAME1}}, "strict": True}, {NAME1}),
    ({"data": {"description": NAME1, "tags": [{"slug": TAG}]}, "strict": True}, {NAME1}),
    (
        {"data": {
            "custom_fields": {"firewalls": NAME1},
            "description": NAME2,
            "tags": [{"slug": TAG}],
        },
            "strict": True},
        {NAME1},
    ),
    (
        {"data": {
            "custom_fields": {"firewalls": "a"},
            "description": "a",
            "tags": [{"slug": TAG}],
        },
            "strict": True},
        set(),
    ),
]

# Netbox
TG1 = 361
TAG_D: DAny = {
    "id": TG1,
    "url": f"/api/extras/tags/{TG1}/",
    "display": "TAG1",
    "name": "TAG1",
    "slug": "tag1",
}
T1 = 2
TENANT_D: DAny = {
    "id": T1,
    "url": f"/api/tenancy/tenants/{T1}/",
    "display": "NOC",
    "name": "NOC",
    "slug": "noc",
    "tags": [TAG_D],  # list test
    "bool": True,  # boolean test
}
S1 = 168
SITE_D: DAny = {
    "id": S1,
    "url": f"/api/dcim/sites/{S1}/",
    "display": "TST1",
    "name": "TST1",
    "slug": "tst1",
    "bool": True,  # boolean test
    "tenant": TENANT_D,  # dict test
    "tags": [TAG_D],  # list test
}
CT1 = 101
V3_CIRCUIT_TERMINATION_D: DAny = {
    "id": CT1,
    "url": f"/api/circuits/circuit-terminations/{CT1}/",
    "site": SITE_D,
}
CT1 = 101
V4_CIRCUIT_TERMINATION_D: DAny = {
    "id": CT1,
    "url": f"/api/circuits/circuit-terminations/{CT1}/",
    "termination": SITE_D,
}
CB1 = 19083
CABLE_D: DAny = {
    "id": CB1,
    "url": f"/api/dcim/cables/{CB1}/",
    "display": f"#{CB1}",
    "a_terminations": [],
    "b_terminations": [],
    "status": {"value": "connected", "label": "Connected"},
}

P1 = 1
V3_PREFIX_D: DAny = {
    "id": P1,
    "url": f"/api/ipam/prefixes/{P1}/",
    "prefix": "10.0.0.0/24",
    "site": SITE_D,
}
P2 = 2
V4_PREFIX_D: DAny = {
    "id": P2,
    "url": f"/api/ipam/prefixes/{P2}/",
    "scope": SITE_D,
}

I1 = 11807  # interface
II1 = 782  # inventory-items
V3_INVENTORY_ITEM_D: DAny = {
    "id": II1,
    "url": f"/api/dcim/inventory-items/{II1}/",
    "component": {
        "id": I1,
        "url": f"/api/dcim/interfaces/{I1}/",
        "name": "Ethernet1",
        "cable": CB1,
    },
}
V4_INVENTORY_ITEM_D: DAny = {
    "id": II1,
    "url": f"/api/dcim/inventory-items/{II1}/",
    "component": {
        "id": I1,
        "url": f"/api/dcim/interfaces/{I1}/",
        "name": "Ethernet1",
        "cable": CABLE_D,
    },
}
PP1 = 1556
V3_POWER_PORT_D: DAny = {
    "id": PP1,
    "url": f"/api/dcim/power-ports/{PP1}/",
    "name": "POWER PORT1",
    "cable": CABLE_D,
}
PO1 = 5982
V3_POWER_OUTLET_D: DAny = {
    "id": PO1,
    "url": f"/api/dcim/power-outlets/{PO1}/",
    "power_port": {
        "id": PP1,
        "url": f"/api/dcim/power-ports/{PP1}/",
        "cable": PP1,
    },
}
V4_POWER_OUTLET_D: DAny = {
    "id": PO1,
    "url": f"/api/dcim/power-outlets/{PO1}/",
    "power_port": {
        "id": PP1,
        "url": f"/api/dcim/power-ports/{PP1}/",
        "cable": CABLE_D,
    },
}
D1 = 569
V3_DEVICE_D: DAny = {
    "id": D1,
    "url": f"/api/dcim/devices/{D1}/",
    "primary_ip": {"family": 4},
    "primary_ip4": {"family": 4},
}
V4_DEVICE_D: DAny = {
    "id": D1,
    "url": f"/api/dcim/devices/{D1}/",
    "primary_ip": {"family": {"value": 4}},
    "primary_ip4": {"family": {"value": 4}},
}
PL1 = 953
V3_PLATFORM_D: DAny = {
    "id": PL1,
    "url": f"/api/dcim/platforms/{PL1}/",
    "napalm_driver": "ios",
}
V4_PLATFORM_D: DAny = {
    "id": PL1,
    "url": f"/api/dcim/platforms/{PL1}/",
}

OC1 = 6271
V3_OBJECT_CHANGE_D: DAny = {
    "id": OC1,
    "url": f"/api/extras/object-changes/{OC1}/",
    "action": {"value": "update", "label": "Updated"},
    "prechange_data": {
        "last_updated": "2000-12-31T00:00:00.000Z",
    },
    "postchange_data": {
        "last_updated": "2000-12-31T00:00:00.000Z",
    },
}
V4_OBJECT_CHANGE_D: DAny = {
    "id": OC1,
    "url": f"/api/core/object-changes/{OC1}/",
    "action": {"value": "update", "label": "Updated"},
    "prechange_data": {},
    "postchange_data": {},
}
