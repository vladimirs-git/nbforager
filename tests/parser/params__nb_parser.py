"""Params."""
from copy import deepcopy

from nbforager.exceptions import NbParserError
from nbforager.types_ import DAny

PREFIX = "10.0.0.0/24"
NAME = "name"
IP0 = "1.1.1.1"
IP32 = "1.1.1.1/32"

# ====================== universal get methods =======================

# test__any
ANY = [
    (["a"], {"a": None}, True, None),
    (["a"], {"a": None}, False, None),
    (["a"], {"a": "A"}, True, "A"),
    (["a"], {"a": "A"}, False, "A"),
    (["a"], {"a": 1}, True, 1),
    (["a"], {"a": 1}, False, 1),
    (["a"], {"a": {}}, True, {}),
    (["a"], {"a": {}}, False, {}),
    (["a"], {"a": {"k": "A"}}, True, {"k": "A"}),
    (["a"], {"a": {"k": "A"}}, False, {"k": "A"}),
    (["a", "b"], {"a": {"b": None}}, True, None),
    (["a", "b"], {"a": {"b": None}}, False, None),
    (["a", "b"], {"a": {"b": "A"}}, True, "A"),
    (["a", "b"], {"a": {"b": "A"}}, False, "A"),
    (["a", "b"], {"a": {"b": 1}}, True, 1),
    (["a", "b"], {"a": {"b": 1}}, False, 1),
    (["a", "b"], {"a": {"b": {"k": "B"}}}, True, {"k": "B"}),
    (["a", "b"], {"a": {"b": {"k": "B"}}}, False, {"k": "B"}),
    (["a", "b", "c"], {"a": {"b": {"c": None}}}, True, None),
    (["a", "b", "c"], {"a": {"b": {"c": None}}}, False, None),
    (["a", "b", "c"], {"a": {"b": {"c": "A"}}}, True, "A"),
    (["a", "b", "c"], {"a": {"b": {"c": "A"}}}, False, "A"),
    (["a", "b", "c"], {"a": {"b": {"c": 1}}}, True, 1),
    (["a", "b", "c"], {"a": {"b": {"c": 1}}}, False, 1),
    (["a", "b", "c"], {"a": {"b": {"c": {}}}}, True, {}),
    (["a", "b", "c"], {"a": {"b": {"c": {}}}}, False, {}),
    (["a", "b", "c"], {"a": {"b": {"c": {"k": "C"}}}}, True, {"k": "C"}),
    (["a", "b", "c"], {"a": {"b": {"c": {"k": "C"}}}}, False, {"k": "C"}),
    # list
    (["a", 0, "b"], {"a": [{"b": None}]}, False, None),
    (["a", 0, "b"], {"a": [{"b": None}]}, True, None),
    (["a", 0, "b"], {"a": [{"b": "B"}]}, False, "B"),
    (["a", 0, "b"], {"a": [{"b": "B"}]}, True, "B"),
    (["a", 0, "b"], {"a": {"b": "B"}}, False, None),
    (["a", 0, "b"], {"a": {"b": "B"}}, True, None),
]

# test__bool
BOOL = [
    (["a"], {"a": None}, True, NbParserError),
    (["a"], {"a": None}, False, False),
    (["a"], {"a": 1}, True, NbParserError),
    (["a"], {"a": 1}, False, False),
    (["a"], {"a": True}, True, True),
    (["a"], {"a": True}, False, True),
    (["a"], {"a": False}, True, False),
    (["a"], {"a": False}, False, False),
    (["a", "b"], {"a": {"b": True}}, True, True),
    (["a", "b"], {"a": {"b": True}}, False, True),
    (["a", "b"], {"a": {"b": None}}, True, NbParserError),
    (["a", "b"], {"a": {"b": None}}, False, False),
    (["a", "b", "c"], {"a": {"b": {"c": True}}}, True, True),
    (["a", "b", "c"], {"a": {"b": {"c": True}}}, False, True),
    (["a", "b", "c"], {"a": {"b": {"c": None}}}, True, NbParserError),
    (["a", "b", "c"], {"a": {"b": {"c": None}}}, False, False),
    # list
    (["a", 0, "b"], {"a": [{"b": None}]}, False, False),
    (["a", 0, "b"], {"a": [{"b": None}]}, True, NbParserError),
    (["a", 0, "b"], {"a": [{"b": True}]}, False, True),
    (["a", 0, "b"], {"a": [{"b": True}]}, True, True),
    (["a", 0, "b"], {"a": {"b": True}}, False, False),
    (["a", 0, "b"], {"a": {"b": True}}, True, NbParserError),
]

# test__dict
DICT = [
    (["a"], {"a": None}, True, NbParserError),
    (["a"], {"a": None}, False, {}),
    (["a"], {"a": 1}, True, NbParserError),
    (["a"], {"a": 1}, False, {}),
    (["a"], {"a": {}}, True, {}),
    (["a"], {"a": {}}, False, {}),
    (["a"], {"a": {"k": "A"}}, True, {"k": "A"}),
    (["a"], {"a": {"k": "A"}}, False, {"k": "A"}),
    (["a", "b"], {"a": {"b": {"k": "B"}}}, True, {"k": "B"}),
    (["a", "b"], {"a": {"b": {"k": "B"}}}, False, {"k": "B"}),
    (["a", "b", "c"], {"a": {"b": {"c": {"k": "C"}}}}, True, {"k": "C"}),
    (["a", "b", "c"], {"a": {"b": {"c": {"k": "C"}}}}, False, {"k": "C"}),
    # list
    (["a", 0, "b"], {"a": [{"b": None}]}, False, {}),
    (["a", 0, "b"], {"a": [{"b": None}]}, True, NbParserError),
    (["a", 0, "b"], {"a": [{"b": {"k": "B"}}]}, False, {"k": "B"}),
    (["a", 0, "b"], {"a": [{"b": {"k": "B"}}]}, True, {"k": "B"}),
    (["a", 0, "b"], {"a": {"b": {"k": "B"}}}, False, {}),
    (["a", 0, "b"], {"a": {"b": {"k": "B"}}}, True, NbParserError),
]

# test__int
INT = [
    (["id"], {"id": "1"}, True, 1),
    (["id"], {"id": "1"}, False, 1),
    (["id"], {"id": 0}, True, 0),
    (["id"], {"id": 0}, False, 0),
    (["id"], {"id": "0"}, True, 0),
    (["id"], {"id": "0"}, False, 0),
    (["a", "b"], {"a": {"b": 1}}, True, 1),
    (["a", "b"], {"a": {"b": 1}}, False, 1),
    (["a", "b"], {"a": {"b": None}}, True, NbParserError),
    (["a", "b"], {"a": {"b": None}}, False, 0),
    (["a", "b"], {"a": {"b": "1"}}, True, 1),
    (["a", "b"], {"a": {"b": "1"}}, False, 1),
    (["a", "b", "c"], {"a": {"b": {"c": 3}}}, True, 3),
    (["a", "b", "c"], {"a": {"b": {"c": "3"}}}, True, 3),
    (["a", "b", "c"], {"a": {"b": {"c": None}}}, True, NbParserError),
    (["a", "b", "c"], {"a": {"b": {"c": None}}}, False, 0),
    (["id"], None, True, NbParserError),
    (["id"], None, False, 0),
    # list
    (["a", 0, "b"], {"a": [{"b": None}]}, False, 0),
    (["a", 0, "b"], {"a": [{"b": None}]}, True, NbParserError),
    (["a", 0, "b"], {"a": [{"b": 1}]}, False, 1),
    (["a", 0, "b"], {"a": [{"b": 1}]}, True, 1),
    (["a", 0, "b"], {"a": {"b": 1}}, False, 0),
    (["a", 0, "b"], {"a": {"b": 1}}, True, NbParserError),
]

# test__list
LIST = [
    (["a"], {"a": None}, True, NbParserError),
    (["a"], {"a": None}, False, []),
    (["a"], {"a": 1}, True, NbParserError),
    (["a"], {"a": 1}, False, []),
    (["a"], {"a": ["A"]}, True, ["A"]),
    (["a"], {"a": ["A"]}, False, ["A"]),
    (["a"], {"a": [""]}, True, [""]),
    (["a"], {"a": [""]}, False, [""]),
    (["a", "b"], {"a": {"b": ["B"]}}, True, ["B"]),
    (["a", "b"], {"a": {"b": ["B"]}}, False, ["B"]),
    (["a", "b"], {"a": {"b": None}}, True, NbParserError),
    (["a", "b"], {"a": {"b": None}}, False, []),
    (["a", "b", "c"], {"a": {"b": {"c": ["C"]}}}, True, ["C"]),
    (["a", "b", "c"], {"a": {"b": {"c": ["C"]}}}, False, ["C"]),
    (["a", "b", "c"], {"a": {"b": {"c": None}}}, True, NbParserError),
    (["a", "b", "c"], {"a": {"b": {"c": None}}}, False, []),
    # list
    (["a", 0, "b"], {"a": [{"b": "B"}]}, False, []),
    (["a", 0, "b"], {"a": [{"b": "B"}]}, True, NbParserError),
    (["a", 0, "b"], {"a": [{"b": ["B"]}]}, False, ["B"]),
    (["a", 0, "b"], {"a": [{"b": ["B"]}]}, True, ["B"]),
    (["a", 0, "b"], {"a": {"b": ["B"]}}, False, []),
    (["a", 0, "b"], {"a": {"b": ["B"]}}, True, NbParserError),
]

# test__str
STR = [
    (["a"], {"a": None}, True, NbParserError),
    (["a"], {"a": None}, False, ""),
    (["a"], {"a": 1}, True, NbParserError),
    (["a"], {"a": 1}, False, ""),
    (["a"], {"a": "A"}, True, "A"),
    (["a"], {"a": "A"}, False, "A"),
    (["a"], {"a": ""}, True, ""),
    (["a"], {"a": ""}, False, ""),
    (["a", "b"], {"a": {"b": "B"}}, True, "B"),
    (["a", "b"], {"a": {"b": "B"}}, False, "B"),
    (["a", "b"], {"a": {"b": None}}, True, NbParserError),
    (["a", "b"], {"a": {"b": None}}, False, ""),
    (["a", "b", "c"], {"a": {"b": {"c": "C"}}}, True, "C"),
    (["a", "b", "c"], {"a": {"b": {"c": "C"}}}, False, "C"),
    (["a", "b", "c"], {"a": {"b": {"c": None}}}, True, NbParserError),
    (["a", "b", "c"], {"a": {"b": {"c": None}}}, False, ""),
    # list
    (["a", 0, "b"], {"a": [{"b": None}]}, False, ""),
    (["a", 0, "b"], {"a": [{"b": None}]}, True, NbParserError),
    (["a", 0, "b"], {"a": [{"b": "B"}]}, False, "B"),
    (["a", 0, "b"], {"a": [{"b": "B"}]}, True, "B"),
    (["a", 0, "b"], {"a": {"b": "B"}}, False, ""),
    (["a", 0, "b"], {"a": {"b": "B"}}, True, NbParserError),
]

# test__strict_dict
STRICT_DICT = [
    (["a"], {"a": {"k": "v"}}, True, {"k": "v"}),
    (["a"], {"a": {"k": "v"}}, False, {"k": "v"}),
    (["a"], {"a": 0}, True, NbParserError),
    (["a"], {"a": 0}, False, NbParserError),
    (["a"], {"url": "https://"}, True, NbParserError),
    (["a"], {"url": "https://"}, False, NbParserError),
]

# test__strict_int
STRICT_INT = [
    (["a"], {"a": 1}, True, 1),
    (["a"], {"a": 1}, False, 1),
    (["a"], {"a": 0}, True, NbParserError),
    (["a"], {"a": 0}, False, NbParserError),
    (["a"], {"url": "https://"}, True, NbParserError),
    (["a"], {"url": "https://"}, False, NbParserError),
]

# test__strict_list
STRICT_LIST = [
    (["a"], {"a": ["A"]}, True, ["A"]),
    (["a"], {"a": ["A"]}, False, ["A"]),
    (["a"], {"a": []}, True, NbParserError),
    (["a"], {"a": []}, False, NbParserError),
    (["a"], {"url": "https://"}, True, NbParserError),
    (["a"], {"url": "https://"}, False, NbParserError),
]

# test__strict_str
STRICT_STR = [
    (["a"], {"a": "A"}, True, "A"),
    (["a"], {"a": "A"}, False, "A"),
    (["a"], {"a": ""}, True, NbParserError),
    (["a"], {"a": ""}, False, NbParserError),
    (["a"], {"url": "https://"}, True, NbParserError),
    (["a"], {"url": "https://"}, False, NbParserError),
]

# ============================= methods ==============================

# test__id_
ID_ = [
    (["id"], {"id": "1"}, True, 1),
    (["id"], {"id": "1"}, False, 1),
    (["id"], {"id": 0}, True, 0),
    (["id"], {"id": 0}, False, 0),
    (["id"], {"id": "0"}, True, 0),
    (["id"], {"id": "0"}, False, 0),
    (["id"], None, True, NbParserError),
    (["id"], None, False, 0),
]

# test__address
ADDRESS = [
    ({"address": PREFIX}, True, PREFIX),
    ({"address": PREFIX}, False, PREFIX),
    ({"address": "10.0.0.1"}, True, NbParserError),
    ({"address": "10.0.0.1"}, False, "10.0.0.1"),
    ({"address": None}, True, NbParserError),
    ({"address": None}, False, ""),
    ({"address": 1}, True, NbParserError),
    ({"address": 1}, False, ""),
    (None, True, NbParserError),
    (None, False, ""),
]

# test__group_name
GROUP_NAME = [
    ({"group": {"name": NAME}}, True, NAME),
    ({"group": {"name": NAME}}, False, NAME),
    ({"group": {"name": ""}}, True, NbParserError),
    ({"group": {"name": ""}}, False, ""),
    ({"group": None}, True, NbParserError),
    ({"group": None}, False, ""),
    (None, True, NbParserError),
    (None, False, ""),
]

# test__family_value
FAMILY_VALUE = [
    ({"family": {"value": 4}}, True, 4),
    ({"family": {"value": "4"}}, True, 4),
    ({"family": {"value": 4}}, False, 4),
    ({"family": {"value": 0}}, True, NbParserError),
    ({"family": {"value": 0}}, False, 0),
    ({"family": None}, True, NbParserError),
    ({"family": None}, False, 0),
    (None, True, NbParserError),
    (None, False, 0),
]

# test__name
NAME_ = [
    ({"name": NAME}, True, NAME),
    ({"name": NAME}, False, NAME),
    ({"name": ""}, True, NbParserError),
    ({"name": ""}, False, ""),
    (None, True, NbParserError),
    (None, False, ""),
]

# test__assigned_device
ASSIGNED_DEVICE_NAME = [
    ({"assigned_object": {"device": {"name": NAME}}}, True, NAME),
    ({"assigned_object": {"device": {"name": NAME}}}, False, NAME),
    ({"assigned_object": {"device": None}}, True, NbParserError),
    ({"assigned_object": {"device": None}}, False, ""),
    ({"assigned_object": None}, True, NbParserError),
    ({"assigned_object": None}, False, ""),
    (None, True, NbParserError),
    (None, False, ""),
]

# test__address
PREFIX_ = [
    ({"prefix": PREFIX}, True, PREFIX),
    ({"prefix": PREFIX}, False, PREFIX),
    ({"prefix": "10.0.0.0"}, True, NbParserError),
    ({"prefix": "10.0.0.0"}, False, "10.0.0.0"),
    ({"prefix": None}, True, NbParserError),
    ({"prefix": None}, False, ""),
    (None, True, NbParserError),
    (None, False, ""),
]

# test__primary_ip4
PRIMARY_IP4 = [
    ({"primary_ip4": {"address": IP32}}, True, IP32),
    ({"primary_ip4": {"address": IP32}}, False, IP32),
    ({"primary_ip4": {"address": IP0}}, True, IP0),
    ({"primary_ip4": {"address": IP0}}, False, IP0),
    ({"primary_ip4": {"address": f"{IP0}_32"}}, True, NbParserError),
    ({"primary_ip4": {"address": f"{IP0}_32"}}, False, f"{IP0}_32"),
    ({"primary_ip4": {"address": ""}}, True, NbParserError),
    ({"primary_ip4": {"address": ""}}, False, ""),
    ({"primary_ip4": {"address": None}}, True, NbParserError),
    ({"primary_ip4": {"address": None}}, False, ""),
    ({"primary_ip4": None}, True, NbParserError),
    ({"primary_ip4": None}, False, ""),
]

# test__primary_ip
PRIMARY_IP = [
    ({"primary_ip4": {"address": IP32}}, True, IP0),
    ({"primary_ip4": {"address": IP32}}, False, IP0),
    ({"primary_ip4": {"address": IP0}}, True, IP0),
    ({"primary_ip4": {"address": IP0}}, False, IP0),
    ({"primary_ip4": {"address": f"{IP0}_32"}}, True, NbParserError),
    ({"primary_ip4": {"address": f"{IP0}_32"}}, False, f"{IP0}_32"),
    ({"primary_ip4": {"address": ""}}, True, NbParserError),
    ({"primary_ip4": {"address": ""}}, False, ""),
    ({"primary_ip4": {"address": None}}, True, NbParserError),
    ({"primary_ip4": {"address": None}}, False, ""),
    ({"primary_ip4": None}, True, NbParserError),
    ({"primary_ip4": None}, False, ""),
]

# test__site_name
SITE_NAME = [
    ({"site": {"name": NAME}}, True, True, NAME.upper()),
    ({"site": {"name": NAME}}, True, False, NAME.lower()),
    ({"site": {"name": NAME}}, False, True, NAME.upper()),
    ({"site": {"name": NAME}}, False, False, NAME.lower()),
    ({"site": {"name": ""}}, True, True, NbParserError),
    ({"site": {"name": ""}}, True, False, NbParserError),
    ({"site": {"name": ""}}, False, True, ""),
    ({"site": {"name": ""}}, False, False, ""),
    ({"site": None}, True, False, NbParserError),
    ({"site": None}, False, False, ""),
    (None, True, False, NbParserError),
    (None, False, False, ""),
]

# test__vid
GET_VID = [
    ({"vid": "1"}, True, 1),
    ({"vid": "1"}, False, 1),
    ({"vid": 0}, True, 0),
    ({"vid": 0}, False, 0),
    ({"vid": "0"}, True, 0),
    ({"vid": "0"}, False, 0),
    (None, True, NbParserError),
    (None, False, 0),
]

# test__vlan
GET_VLAN_VID = [
    ({"vlan": {"vid": 1}}, True, 1),
    ({"vlan": {"vid": 1}}, False, 1),
    ({"vlan": {"vid": "1"}}, True, 1),
    ({"vlan": {"vid": "1"}}, False, 1),
    ({"vlan": {"vid": 0}}, True, 0),
    ({"vlan": {"vid": 0}}, False, 0),
    ({"vlan": {"vid": "0"}}, True, 0),
    ({"vlan": {"vid": "0"}}, False, 0),
    ({"vlan": {"vid": None}}, True, NbParserError),
    ({"vlan": {"vid": None}}, False, 0),
    ({"vlan": None}, True, NbParserError),
    ({"vlan": None}, False, 0),
    (None, True, NbParserError),
    (None, False, 0),
]

# test__tags
TAGS = [
    ({"tags": [{"slug": NAME}, {"slug": "tag2"}]}, True, [NAME, "tag2"]),
    ({"tags": [{"slug": NAME}, {"slug": "tag2"}]}, False, [NAME, "tag2"]),
    ({"tags": [{"slug": None}]}, True, NbParserError),
    ({"tags": [{"slug": None}]}, False, []),
    ({"tags": [None]}, True, NbParserError),
    ({"tags": [None]}, False, []),
    ({"tags": []}, True, []),
    ({"tags": []}, False, []),
    ({"tags": None}, True, NbParserError),
    ({"tags": None}, False, []),
    (None, True, NbParserError),
    (None, False, []),
]

# test__url
URL = [
    ({"url": NAME}, True, NAME),
    ({"url": NAME}, False, NAME),
    ({"url": ""}, True, NbParserError),
    ({"url": ""}, False, ""),
    (None, True, NbParserError),
    (None, False, ""),
]

# test__platform_slug
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

PLATFORM_SLUG = [
    (PLATFORM_D, "cisco_ios"),
    (PLATFORM_D_W_VALID_NAME, "cisco_ios"),
    (PLATFORM_D_W_VALID_SLUG, "cisco_ios"),
    ({}, NbParserError),
    (PLATFORM_D_WO_URL, NbParserError),
    (PLATFORM_D_W_INVALID_ADDRESS, NbParserError),
    (PLATFORM_D_WO_ADDRESS, NbParserError),
    (PLATFORM_D_WO_PRIMARY_IP4, NbParserError),
    (PLATFORM_D_WO_SLUG, NbParserError),
    (PLATFORM_D_WO_PLATFORM, NbParserError),
]

# test__hosts_in_cf_firewalls
NAME1 = "a-b-c-d"
NAME2 = "A-B-C-D"
HOSTS_IN_CF_FIREWALLS = [
    ({"custom_fields": {"firewalls": f"{NAME1} {NAME2}"}}, True, {NAME1, NAME2}),
    ({"custom_fields": {"firewalls": f"{NAME1},{NAME2}"}}, True, {NAME1, NAME2}),
    ({"custom_fields": {"firewalls": f"{NAME1}, {NAME2}"}}, True, {NAME1, NAME2}),
    ({"custom_fields": {"firewalls": f"{NAME1}, {NAME2}"}}, False, {NAME1, NAME2}),
    ({"custom_fields": {"firewalls": ""}}, True, set()),
    ({"custom_fields": {"firewalls": ""}}, False, set()),
    ({"custom_fields": None}, True, set()),
    ({"custom_fields": None}, False, set()),
    (None, True, set()),
    (None, False, set()),
]

# test__hosts_in_aggr_descr
TAG = "noc_aggregates_belonging"
HOSTS_IN_AGGR_DESCR = [
    ({"description": f"\t{NAME1},{NAME2} a", "tags": [{"slug": TAG}]}, True, {NAME1, NAME2}),
    ({"description": f"a:{NAME1}, {NAME2}.a", "tags": [{"slug": TAG}]}, True, {NAME1, NAME2}),
    ({"description": f"{NAME1} {NAME2} a", "tags": [{"slug": TAG}]}, True, {NAME1, NAME2}),
    ({"description": f"{NAME1} {NAME2} a", "tags": [{"slug": TAG}]}, False, {NAME1, NAME2}),
    ({"description": "a", "tags": [{"slug": TAG}]}, True, set()),
    ({"description": "a", "tags": [{"slug": TAG}]}, False, set()),
    ({"description": "", "tags": [{"slug": TAG}]}, True, set()),
    ({"description": "", "tags": [{"slug": TAG}]}, False, set()),
    ({"description": "", "tags": [None]}, True, NbParserError),
    ({"description": "", "tags": [None]}, False, set()),
]

# test__firewalls__in_aggregate
TAG = "noc_aggregates_belonging"
FIREWALLS__IN_AGGREGATE = [
    ({"custom_fields": {"firewalls": NAME1}}, True, {NAME1}),
    ({"description": NAME1, "tags": [{"slug": TAG}]}, True, {NAME1}),
    (
        {"custom_fields": {"firewalls": NAME1}, "description": NAME2, "tags": [{"slug": TAG}]},
        True,
        {NAME1},
    ),
    (
        {"custom_fields": {"firewalls": "a"}, "description": "a", "tags": [{"slug": TAG}]},
        True,
        set(),
    ),
]

# test__is_ipam
IS_IPAM = [
    ({"url": "/api/ipam/prefixes/"}, True, "prefixes", True),
    ({"url": "/api/ipam/prefixes/"}, False, "prefixes", True),
    ({"url": "/api/ipam/prefixes/"}, True, "aggregates", False),
    ({"url": "/api/ipam/prefixes/"}, False, "aggregates", False),
    ({"url": "/api/ipam/aggregates/"}, True, "aggregates", True),
    ({"url": "/api/ipam/aggregates/"}, False, "aggregates", True),
    ({"url": "/api/ipam/ip-addresses/"}, True, "ip-addresses", True),
    ({"url": "/api/ipam/ip-addresses/"}, False, "ip-addresses", True),
    ({"url": None}, True, "prefixes", NbParserError),
    ({"url": None}, False, "prefixes", False),
]

# test__is_dcim
IS_DCIM = [
    ({"url": "/api/dcim/devices/"}, True, "devices", True),
    ({"url": "/api/dcim/devices/"}, False, "devices", True),
    ({"url": "/api/dcim/devices/"}, True, "aggregates", False),
    ({"url": "/api/dcim/devices/"}, False, "aggregates", False),
    ({"url": None}, True, "devices", NbParserError),
    ({"url": None}, False, "devices", False),
]

# test__is_vrf
IS_VRF = [
    ({"vrf": NAME}, True, True),
    ({"vrf": NAME}, False, True),
    ({"vrf": ""}, True, False),
    ({"vrf": ""}, False, False),
]

# test__is_prefix
IS_PREFIX = [
    (PREFIX, True),
    (IP32, True),
    (IP0, False),
    ("", False),
]
