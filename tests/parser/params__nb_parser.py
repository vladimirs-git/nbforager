"""Params."""
from copy import deepcopy

from nbforager.exceptions import NbParserError
from nbforager.types_ import DAny

# ====================== universal get methods =======================

ANY = [
    (["a"], {"data": {"a": None}, "strict": True}, None),
    (["a"], {"data": {"a": None}, "strict": False}, None),
    (["a"], {"data": {"a": "A"}, "strict": True}, "A"),
    (["a"], {"data": {"a": "A"}, "strict": False}, "A"),
    (["a"], {"data": {"a": 1}, "strict": True}, 1),
    (["a"], {"data": {"a": 1}, "strict": False}, 1),
    (["a"], {"data": {"a": {}}, "strict": True}, {}),
    (["a"], {"data": {"a": {}}, "strict": False}, {}),
    (["a"], {"data": {"a": {"k": "A"}}, "strict": True}, {"k": "A"}),
    (["a"], {"data": {"a": {"k": "A"}}, "strict": False}, {"k": "A"}),
    (["a", "b"], {"data": {"a": {"b": None}}, "strict": True}, None),
    (["a", "b"], {"data": {"a": {"b": None}}, "strict": False}, None),
    (["a", "b"], {"data": {"a": {"b": "A"}}, "strict": True}, "A"),
    (["a", "b"], {"data": {"a": {"b": "A"}}, "strict": False}, "A"),
    (["a", "b"], {"data": {"a": {"b": 1}}, "strict": True}, 1),
    (["a", "b"], {"data": {"a": {"b": 1}}, "strict": False}, 1),
    (["a", "b"], {"data": {"a": {"b": {"k": "B"}}}, "strict": True}, {"k": "B"}),
    (["a", "b"], {"data": {"a": {"b": {"k": "B"}}}, "strict": False}, {"k": "B"}),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": None}}}, "strict": True}, None),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": None}}}, "strict": False}, None),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": "A"}}}, "strict": True}, "A"),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": "A"}}}, "strict": False}, "A"),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": 1}}}, "strict": True}, 1),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": 1}}}, "strict": False}, 1),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": {}}}}, "strict": True}, {}),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": {}}}}, "strict": False}, {}),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": {"k": "C"}}}}, "strict": True}, {"k": "C"}),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": {"k": "C"}}}}, "strict": False}, {"k": "C"}),
    # list
    (["a", 0, "b"], {"data": {"a": [{"b": None}]}, "strict": False}, None),
    (["a", 0, "b"], {"data": {"a": [{"b": None}]}, "strict": True}, None),
    (["a", 0, "b"], {"data": {"a": [{"b": "B"}]}, "strict": False}, "B"),
    (["a", 0, "b"], {"data": {"a": [{"b": "B"}]}, "strict": True}, "B"),
    (["a", 0, "b"], {"data": {"a": {"b": "B"}}, "strict": False}, None),
    (["a", 0, "b"], {"data": {"a": {"b": "B"}}, "strict": True}, None),
]

BOOL = [
    (["a"], {"data": {"a": None}, "strict": True}, NbParserError),
    (["a"], {"data": {"a": None}, "strict": False}, False),
    (["a"], {"data": {"a": 1}, "strict": True}, NbParserError),
    (["a"], {"data": {"a": 1}, "strict": False}, False),
    (["a"], {"data": {"a": True}, "strict": True}, True),
    (["a"], {"data": {"a": True}, "strict": False}, True),
    (["a"], {"data": {"a": False}, "strict": True}, False),
    (["a"], {"data": {"a": False}, "strict": False}, False),
    (["a", "b"], {"data": {"a": {"b": True}}, "strict": True}, True),
    (["a", "b"], {"data": {"a": {"b": True}}, "strict": False}, True),
    (["a", "b"], {"data": {"a": {"b": None}}, "strict": True}, NbParserError),
    (["a", "b"], {"data": {"a": {"b": None}}, "strict": False}, False),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": True}}}, "strict": True}, True),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": True}}}, "strict": False}, True),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": None}}}, "strict": True}, NbParserError),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": None}}}, "strict": False}, False),
    # list
    (["a", 0, "b"], {"data": {"a": [{"b": None}]}, "strict": False}, False),
    (["a", 0, "b"], {"data": {"a": [{"b": None}]}, "strict": True}, NbParserError),
    (["a", 0, "b"], {"data": {"a": [{"b": True}]}, "strict": False}, True),
    (["a", 0, "b"], {"data": {"a": [{"b": True}]}, "strict": True}, True),
    (["a", 0, "b"], {"data": {"a": {"b": True}}, "strict": False}, False),
    (["a", 0, "b"], {"data": {"a": {"b": True}}, "strict": True}, NbParserError),
]

DICT = [
    (["a"], {"data": {"a": None}, "strict": True}, NbParserError),
    (["a"], {"data": {"a": None}, "strict": False}, {}),
    (["a"], {"data": {"a": 1}, "strict": True}, NbParserError),
    (["a"], {"data": {"a": 1}, "strict": False}, {}),
    (["a"], {"data": {"a": {}}, "strict": True}, {}),
    (["a"], {"data": {"a": {}}, "strict": False}, {}),
    (["a"], {"data": {"a": {"k": "A"}}, "strict": True}, {"k": "A"}),
    (["a"], {"data": {"a": {"k": "A"}}, "strict": False}, {"k": "A"}),
    (["a", "b"], {"data": {"a": {"b": {"k": "B"}}}, "strict": True}, {"k": "B"}),
    (["a", "b"], {"data": {"a": {"b": {"k": "B"}}}, "strict": False}, {"k": "B"}),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": {"k": "C"}}}}, "strict": True}, {"k": "C"}),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": {"k": "C"}}}}, "strict": False}, {"k": "C"}),
    # list
    (["a", 0, "b"], {"data": {"a": [{"b": None}]}, "strict": False}, {}),
    (["a", 0, "b"], {"data": {"a": [{"b": None}]}, "strict": True}, NbParserError),
    (["a", 0, "b"], {"data": {"a": [{"b": {"k": "B"}}]}, "strict": False}, {"k": "B"}),
    (["a", 0, "b"], {"data": {"a": [{"b": {"k": "B"}}]}, "strict": True}, {"k": "B"}),
    (["a", 0, "b"], {"data": {"a": {"b": {"k": "B"}}}, "strict": False}, {}),
    (["a", 0, "b"], {"data": {"a": {"b": {"k": "B"}}}, "strict": True}, NbParserError),
]

INT = [
    (["id"], {"data": {"id": "1"}, "strict": True}, 1),
    (["id"], {"data": {"id": "1"}, "strict": False}, 1),
    (["id"], {"data": {"id": 0}, "strict": True}, 0),
    (["id"], {"data": {"id": 0}, "strict": False}, 0),
    (["id"], {"data": {"id": "0"}, "strict": True}, 0),
    (["id"], {"data": {"id": "0"}, "strict": False}, 0),
    (["a", "b"], {"data": {"a": {"b": 1}}, "strict": True}, 1),
    (["a", "b"], {"data": {"a": {"b": 1}}, "strict": False}, 1),
    (["a", "b"], {"data": {"a": {"b": None}}, "strict": True}, NbParserError),
    (["a", "b"], {"data": {"a": {"b": None}}, "strict": False}, 0),
    (["a", "b"], {"data": {"a": {"b": "1"}}, "strict": True}, 1),
    (["a", "b"], {"data": {"a": {"b": "1"}}, "strict": False}, 1),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": 3}}}, "strict": True}, 3),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": "3"}}}, "strict": True}, 3),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": None}}}, "strict": True}, NbParserError),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": None}}}, "strict": False}, 0),
    (["id"], {"data": None, "strict": True}, NbParserError),
    (["id"], {"data": None, "strict": False}, 0),
    # list
    (["a", 0, "b"], {"data": {"a": [{"b": None}]}, "strict": False}, 0),
    (["a", 0, "b"], {"data": {"a": [{"b": None}]}, "strict": True}, NbParserError),
    (["a", 0, "b"], {"data": {"a": [{"b": 1}]}, "strict": False}, 1),
    (["a", 0, "b"], {"data": {"a": [{"b": 1}]}, "strict": True}, 1),
    (["a", 0, "b"], {"data": {"a": {"b": 1}}, "strict": False}, 0),
    (["a", 0, "b"], {"data": {"a": {"b": 1}}, "strict": True}, NbParserError),
]

LIST = [
    (["a"], {"data": {"a": None}, "strict": True}, NbParserError),
    (["a"], {"data": {"a": None}, "strict": False}, []),
    (["a"], {"data": {"a": 1}, "strict": True}, NbParserError),
    (["a"], {"data": {"a": 1}, "strict": False}, []),
    (["a"], {"data": {"a": ["A"]}, "strict": True}, ["A"]),
    (["a"], {"data": {"a": ["A"]}, "strict": False}, ["A"]),
    (["a"], {"data": {"a": [""]}, "strict": True}, [""]),
    (["a"], {"data": {"a": [""]}, "strict": False}, [""]),
    (["a", "b"], {"data": {"a": {"b": ["B"]}}, "strict": True}, ["B"]),
    (["a", "b"], {"data": {"a": {"b": ["B"]}}, "strict": False}, ["B"]),
    (["a", "b"], {"data": {"a": {"b": None}}, "strict": True}, NbParserError),
    (["a", "b"], {"data": {"a": {"b": None}}, "strict": False}, []),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": ["C"]}}}, "strict": True}, ["C"]),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": ["C"]}}}, "strict": False}, ["C"]),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": None}}}, "strict": True}, NbParserError),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": None}}}, "strict": False}, []),
    # list
    (["a", 0, "b"], {"data": {"a": [{"b": "B"}]}, "strict": False}, []),
    (["a", 0, "b"], {"data": {"a": [{"b": "B"}]}, "strict": True}, NbParserError),
    (["a", 0, "b"], {"data": {"a": [{"b": ["B"]}]}, "strict": False}, ["B"]),
    (["a", 0, "b"], {"data": {"a": [{"b": ["B"]}]}, "strict": True}, ["B"]),
    (["a", 0, "b"], {"data": {"a": {"b": ["B"]}}, "strict": False}, []),
    (["a", 0, "b"], {"data": {"a": {"b": ["B"]}}, "strict": True}, NbParserError),
]

STR = [
    (["a"], {"data": {"a": None}, "strict": True}, NbParserError),
    (["a"], {"data": {"a": None}, "strict": False}, ""),
    (["a"], {"data": {"a": 1}, "strict": True}, NbParserError),
    (["a"], {"data": {"a": 1}, "strict": False}, ""),
    (["a"], {"data": {"a": "A"}, "strict": True}, "A"),
    (["a"], {"data": {"a": "A"}, "strict": False}, "A"),
    (["a"], {"data": {"a": ""}, "strict": True}, ""),
    (["a"], {"data": {"a": ""}, "strict": False}, ""),
    (["a", "b"], {"data": {"a": {"b": "B"}}, "strict": True}, "B"),
    (["a", "b"], {"data": {"a": {"b": "B"}}, "strict": False}, "B"),
    (["a", "b"], {"data": {"a": {"b": None}}, "strict": True}, NbParserError),
    (["a", "b"], {"data": {"a": {"b": None}}, "strict": False}, ""),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": "C"}}}, "strict": True}, "C"),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": "C"}}}, "strict": False}, "C"),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": None}}}, "strict": True}, NbParserError),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": None}}}, "strict": False}, ""),
    # list
    (["a", 0, "b"], {"data": {"a": [{"b": None}]}, "strict": False}, ""),
    (["a", 0, "b"], {"data": {"a": [{"b": None}]}, "strict": True}, NbParserError),
    (["a", 0, "b"], {"data": {"a": [{"b": "B"}]}, "strict": False}, "B"),
    (["a", 0, "b"], {"data": {"a": [{"b": "B"}]}, "strict": True}, "B"),
    (["a", 0, "b"], {"data": {"a": {"b": "B"}}, "strict": False}, ""),
    (["a", 0, "b"], {"data": {"a": {"b": "B"}}, "strict": True}, NbParserError),
]

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
    "tags": [TAG_D],
    "bool": True,  # need for boolean test
}
S1 = 168
SITE_D: DAny = {
    "id": S1,
    "url": f"/api/dcim/sites/{S1}/",
    "display": "TST1",
    "name": "TST1",
    "slug": "tst1",
    "bool": True,  # need for boolean test
    "tenant": TENANT_D,  # need for dict test
}
CT1 = 101
CIRCUIT_TERMINATION_SITE_D: DAny = {
    "id": CT1,
    "url": f"/api/circuits/circuit-terminations/{CT1}/",
    "site": SITE_D,
}
CT1 = 101
CIRCUIT_TERMINATION_TERMINATION_D: DAny = {
    "id": CT1,
    "url": f"/api/circuits/circuit-terminations/{CT1}/",
    "termination": SITE_D,
}
P1 = 1
PREFIX_SITE_D: DAny = {
    "id": P1,
    "url": f"/api/ipam/prefixes/{P1}/",
    "prefix": "10.0.0.0/24",
    "site": SITE_D,
}
P2 = 2
PREFIX_SCOPE_D: DAny = {
    "id": P2,
    "url": f"/api/ipam/prefixes/{P2}/",
    "scope": SITE_D,
}
