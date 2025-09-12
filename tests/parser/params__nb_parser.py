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

PLATFORM: DAny = {
    "url": "/api/dcim/devices/",
    "primary_ip4": {"address": "10.0.0.1/24"},
    "platform": {"name": "Cisco IOS", "slug": "cisco_ios"},
}
PLATFORM_W_VALID_NAME = deepcopy(PLATFORM)
PLATFORM_W_VALID_NAME["platform"]["name"] = "cisco_ios"
PLATFORM_W_VALID_SLUG = deepcopy(PLATFORM)
PLATFORM_W_VALID_SLUG["platform"]["slug"] = "cisco-ios"
PLATFORM_WO_URL = deepcopy(PLATFORM)
del PLATFORM_WO_URL["url"]
PLATFORM_W_INVALID_ADDRESS = deepcopy(PLATFORM)
PLATFORM_W_INVALID_ADDRESS["primary_ip4"]["address"] = "typo"
PLATFORM_WO_ADDRESS = deepcopy(PLATFORM)
del PLATFORM_WO_ADDRESS["primary_ip4"]["address"]
PLATFORM_WO_PRIMARY_IP4 = deepcopy(PLATFORM)
del PLATFORM_WO_PRIMARY_IP4["primary_ip4"]
PLATFORM_WO_SLUG = deepcopy(PLATFORM)
del PLATFORM_WO_SLUG["platform"]["slug"]
PLATFORM_WO_PLATFORM = deepcopy(PLATFORM)
del PLATFORM_WO_PLATFORM["platform"]

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
# extras/tags
TG1 = 361
TAG_D: DAny = {
    "id": TG1,
    "url": f"/api/extras/tags/{TG1}/",
    "display": "TAG1",
    "name": "TAG1",
    "slug": "tag1",
}

# tenancy/tenants
T1 = 2
TENANT: DAny = {
    "id": T1,
    "url": f"/api/tenancy/tenants/{T1}/",
    "display": "NOC",
    "name": "NOC",
    "slug": "noc",
    "tags": [TAG_D],  # list test
    "bool": True,  # boolean test
}

# tenancy/contact-groups
CG1 = 3
CONTACT_GROUP = {
    "id": CG1,
    "url": f"/api/tenancy/contact-groups/{CG1}/",
    "display": "IT Support",
    "name": "GROUP1",
    "slug": "group1",
}
# tenancy/contacts
TC1 = 2
V3_CONTACT: DAny = {
    "id": TC1,
    "url": f"/api/tenancy/contacts/{TC1}/",
    "group": CONTACT_GROUP,
    "name": "CONTACT1",
}
V4_CONTACT: DAny = {
    "id": TC1,
    "url": f"/api/tenancy/contacts/{TC1}/",
    "groups": [CONTACT_GROUP],
    "name": "CONTACT1",
}

# dcim/sites
S1 = 168
SITE: DAny = {
    "id": S1,
    "url": f"/api/dcim/sites/{S1}/",
    "display": "TST1",
    "name": "TST1",
    "slug": "tst1",
    "bool": True,  # boolean test
    "tenant": TENANT,  # dict test
    "tags": [TAG_D],  # list test
}
SITE_ = {k: v for k, v in SITE.items() if k in ["id", "url", "name", "slug"]}

# circuits/provider-networks
PN1 = 11
PROVIDER_NETWORK = {
    "id": PN1,
    "url": f"/api/circuits/provider-networks/{PN1}/",
    "name": "PROVIDER1"
}

# circuits/circuit-terminations
CT1 = 101
V3_C_TERMINATION: DAny = {
    "id": CT1,
    "url": f"/api/circuits/circuit-terminations/{CT1}/",
    "site": SITE_,
    "provider_network": PROVIDER_NETWORK,
}
CT1 = 101
V4_C_TERMINATION: DAny = {
    "id": CT1,
    "url": f"/api/circuits/circuit-terminations/{CT1}/",
    "termination": SITE_,
}

# dcim/cables
CB1 = 19083
CB1_ = f"#{CB1}"
CABLE: DAny = {
    "id": CB1,
    "url": f"/api/dcim/cables/{CB1}/",
    "display": f"#{CB1}",
    "a_terminations": [],
    "b_terminations": [],
    "status": {"value": "connected", "label": "Connected"},
}

CP1 = 3109
V3_CONSOLE_PORT = {
    "id": CP1,
    "url": f"/api/dcim/console-ports/{CP1}/",
    "display": "Console0",
    "device": {"id": 111},
}
# dcim/cable-terminations
CT1 = 1
V3_CB_TERMINATION: DAny = {
    "id": 1,
    "url": f"/api/dcim/cable-terminations/{CT1}/",
    "cable": CB1,
    "cable_end": "A",
    "termination_type": "dcim.consoleport",
    "termination_id": CP1,
    "termination": {
        "id": CP1,
        "url": f"/api/dcim/console-ports/{CP1}/",
        "device": V3_CONSOLE_PORT,
        "name": "Console0",
        "cable": CB1,
    },
}
V4_CB_TERMINATION: DAny = {
    "id": 1,
    "url": f"/api/dcim/cable-terminations/{CT1}/",
    "cable": CB1,
    "cable_end": "A",
    "termination_type": "dcim.consoleport",
    "termination_id": CP1,
    "termination": {
        "id": CP1,
        "url": f"/api/dcim/console-ports/{CP1}/",
        "device": V3_CONSOLE_PORT,
        "name": "Console0",
        "cable": CABLE,
    },
}

# dcim/inventory-items
I1 = 11807  # interface
II1 = 782  # inventory-items
V3_INV_ITEM: DAny = {
    "id": II1,
    "url": f"/api/dcim/inventory-items/{II1}/",
    "component": {
        "id": I1,
        "url": f"/api/dcim/interfaces/{I1}/",
        "name": "Ethernet1",
        "cable": CB1,
    },
}
V4_INV_ITEM: DAny = {
    "id": II1,
    "url": f"/api/dcim/inventory-items/{II1}/",
    "component": {
        "id": I1,
        "url": f"/api/dcim/interfaces/{I1}/",
        "name": "Ethernet1",
        "cable": CABLE,
    },
}

# dcim/power-ports
PP1 = 1556
V3_POWER_PORT: DAny = {
    "id": PP1,
    "url": f"/api/dcim/power-ports/{PP1}/",
    "name": "POWER PORT1",
    "cable": CABLE,
}
PO1 = 5982
V3_POWER_OUTLET: DAny = {
    "id": PO1,
    "url": f"/api/dcim/power-outlets/{PO1}/",
    "power_port": {
        "id": PP1,
        "url": f"/api/dcim/power-ports/{PP1}/",
        "cable": PP1,
    },
}
V4_POWER_OUTLET: DAny = {
    "id": PO1,
    "url": f"/api/dcim/power-outlets/{PO1}/",
    "power_port": {
        "id": PP1,
        "url": f"/api/dcim/power-ports/{PP1}/",
        "cable": CABLE,
    },
}

# dcim/racks
R1 = 401
V3_RACK: DAny = {
    "id": R1,
    "url": f"/api/dcim/racks/{R1}/",
    "type": {
        "value": "4-post",
        "label": "4-post"
    },
}
V4_RACK: DAny = {
    "id": R1,
    "url": f"/api/dcim/racks/{R1}/",
    "form_factor": {
        "value": "4-post",
        "label": "4-post"
    },
}

# dcim/devices
D1 = 569
V3_DEVICE: DAny = {
    "id": D1,
    "url": f"/api/dcim/devices/{D1}/",
    "name": "DEVICE1",
    "primary_ip": {"family": 4},
    "primary_ip4": {"family": 4},
}
V4_DEVICE: DAny = {
    "id": D1,
    "url": f"/api/dcim/devices/{D1}/",
    "name": "DEVICE1",
    "primary_ip": {"family": {"value": 4}},
    "primary_ip4": {"family": {"value": 4}},
}
PL1 = 953
V3_PLATFORM: DAny = {
    "id": PL1,
    "url": f"/api/dcim/platforms/{PL1}/",
    "napalm_driver": "ios",
    "napalm_args": {},
}
V4_PLATFORM: DAny = {
    "id": PL1,
    "url": f"/api/dcim/platforms/{PL1}/",
}

# ipam/prefixes
P1 = 1
V3_PREFIX: DAny = {
    "id": P1,
    "url": f"/api/ipam/prefixes/{P1}/",
    "prefix": "10.0.0.0/24",
    "site": SITE,  # with tenant, used in NbTree
}
P2 = 2
V4_PREFIX: DAny = {
    "id": P2,
    "url": f"/api/ipam/prefixes/{P2}/",
    "scope": SITE,  # with tenant, used in NbTree
}

# ipam/ip-address
IP1 = 680
V3_IP_ADDRESS = {
    "id": IP1,
    "url": f"/api/ipam/ip-addresses/{IP1}/",
    "address": "10.0.0.1/24",
    "assigned_object_type": "dcim.interface",
    "assigned_object_id": I1,
    "assigned_object": {
        "id": I1,
        "url": f"/api/dcim/interfaces/{I1}/",
        "name": "Ethernet1",
        "cable": CB1,
        "device": V3_DEVICE,
    },
}
V4_IP_ADDRESS = {
    "id": IP1,
    "url": f"/api/ipam/ip-addresses/{IP1}/",
    "address": "10.0.0.1/24",
    "assigned_object_type": "dcim.interface",
    "assigned_object_id": I1,
    "assigned_object": {
        "id": I1,
        "url": f"/api/dcim/interfaces/{I1}/",
        "name": "Ethernet1",
        "cable": CABLE,
        "device": V3_DEVICE,
    },
}

# ipam/vlan-groups
VG1 = 1
V3_VLAN_GROUP: DAny = {
    "id": VG1,
    "url": f"/api/ipam/vlan-groups/{VG1}/",
    "name": "tst1-office",
    "slug": "tst1-office",
    "scope_type": "dcim.site",
    "scope_id": S1,
    "scope": SITE_,
    "min_vid": 1,
    "max_vid": 4094,
}
V4_VLAN_GROUP: DAny = {
    "id": VG1,
    "url": f"/api/ipam/vlan-groups/{VG1}/",
    "name": "tst1-office",
    "slug": "tst1-office",
    "scope_type": "dcim.site",
    "scope_id": S1,
    "scope": SITE_,
    "vid_ranges": [[1, 4094]],
}

# ipam/services
V3_SERVICE = {
    "id": 20220,
    "url": "/api/ipam/services/20220/",
    "device": V3_DEVICE,
    "virtual_machine": None,
    "name": "SERVICE1",
}
V4_SERVICE = {
    "id": 20220,
    "url": "/api/ipam/services/20220/",
    "name": "SERVICE1",
    "parent_object_type": "virtualization.virtualmachine",
    "parent_object_id": 710,
    "parent": V4_DEVICE,
}

# extras/custom-fields
CF1 = 1
UI_VISIBILITY = {"value": "read-write", "label": "Read/Write"}
CHOICES = ["DATA_SRE", "DPT", "SRE", "TIER2", "RDBMS_SRE"]
V3_CUSTOM_FIELD = {
    "id": CF1,
    "url": f"/api/extras/custom-fields/{CF1}/",
    "display": "root_vlan",
    "content_types": ["ipam.vlan"],
    "type": {"value": "object", "label": "Object"},
    "object_type": "ipam.vlan",
    "ui_visibility": UI_VISIBILITY,
    "choices": CHOICES,
}
UI_VISIBLE = {"value": "always", "label": "Always"}
V4_CUSTOM_FIELD = {
    "id": CF1,
    "url": f"/api/extras/custom-fields/{CF1}/",
    "display": "root_vlan",
    "object_types": ["ipam.vlan"],
    "type": {"value": "object", "label": "Object"},
    "related_object_type": "ipam.vlan",
    "ui_visible": UI_VISIBLE,
    "ui_editable": {"value": "yes", "label": "Yes"},
    "choice_set": {
        "id": 16,
        "url": "https://netbox.tools-test.aws.evo-infra.com/api/extras/custom-field-choice-sets/16/",
        "display": "team Choices",
        "name": "team Choices",
        "description": "",
        "choices_count": 5
    },
}

# extras/object-changes
OC1 = 6271
UPDATED = "2000-12-31T00:00:00.000Z"
V3_OBJECT_CHANGE: DAny = {
    "id": OC1,
    "url": f"/api/extras/object-changes/{OC1}/",
    "action": {"value": "update", "label": "Updated"},
    "prechange_data": {"last_updated": UPDATED},
    "postchange_data": {"last_updated": UPDATED},
}
V4_OBJECT_CHANGE: DAny = {
    "id": OC1,
    "url": f"/api/core/object-changes/{OC1}/",
    "action": {"value": "update", "label": "Updated"},
    "prechange_data": {},
    "postchange_data": {},
}
