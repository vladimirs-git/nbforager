"""Example NbValue raise NbVersionError, for migration from Netbox v3.5 to v4.3.
"""
from pprint import pprint

import dictdiffer

from nbforager import NbValue

# v3.5 prefix with site
V3_PREFIX = {
    "id": 8452,
    "url": "/api/ipam/prefixes/8452/",
    "prefix": "10.23.34.0/24",
    "family": {"label": "IPv4", "value": 4},
    "site": {
        "display": "TST1",
        "id": 168,
        "name": "TST1",
        "slug": "tst1",
        "url": "/api/dcim/sites/168/",
    },
}

# v3.5 prefix without site
V3_PREFIX_ = {
    "id": 8452,
    "url": "/api/ipam/prefixes/8452/",
    "prefix": "10.23.34.0/24",
    "family": {"label": "IPv4", "value": 4},
    "site": None,
}

# v4.3 prefix with site
V4_PREFIX = {
    "id": 8452,
    "url": "/api/ipam/prefixes/8452/",
    "prefix": "10.23.34.0/24",
    "family": {"label": "IPv4", "value": 4},
    "scope_type": "dcim.site",
    "scope_id": 168,
    "scope": {
        "description": "",
        "display": "TST1",
        "id": 168,
        "name": "TST1",
        "slug": "tst1",
        "url": "/api/dcim/sites/168/",
    },
}

# difference between v3.5 and v4.3
pprint(list(dictdiffer.diff(V3_PREFIX, V4_PREFIX)), width=120)
print()
# [("add",
#   "",
#   [("scope_type", "dcim.site"),
#    ("scope_id", 168),
#    ("scope",
#     {"display": "TST1", "id": 168, "name": "TST1", "slug": "tst1"})]),
#  ("remove",
#   "",
#   [("site",
#     {"display": "TST1", "id": 168, "name": "TST1", "slug": "tst1"})])]


# get site name
site3_1 = V3_PREFIX["site"]["name"]
site3_2 = V3_PREFIX.get("site", {}).get("name", "")
site3_3 = str(dict(V3_PREFIX_.get("site") or {}).get("name") or "")
site3_4 = str(dict(V4_PREFIX.get("site") or {}).get("name") or "")
print(f"{site3_1=}")
print(f"{site3_2=}")
print(f"{site3_3=}")
print(f"{site3_4=}")
print()
# site3_1='TST1'
# site3_2='TST1'
# site3_3=''
# site3_4=''

# parse site name
try:
    site4_1 = NbValue(V3_PREFIX).str("site", "name")
    print(f"{site4_1=}")
except Exception as ex:
    print(f"site4_1: {ex}")
site4_2 = NbValue(V3_PREFIX).site_name()
site4_3 = NbValue(V4_PREFIX).site_name()
print(f"{site4_2=}")
print(f"{site4_3=}")
# site4_1: Deprecated model 'ipam/prefixes.site' in /api/ipam/prefixes/8452/, expected 'ipam/prefixes.scope'.
# site4_2='TST1'
# site4_3='TST1'
