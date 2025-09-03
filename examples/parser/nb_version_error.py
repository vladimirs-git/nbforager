"""Example NbValue raise NbVersionError."""
from nbforager import NbValue
from nbforager.exceptions import NbVersionError

# ipam/prefixes data for Netbox < v4.2
PREFIX_V3 = {
    "id": 1,
    "url": "/api/ipam/prefixes/1/",
    "prefix": "10.0.0.0/24",
    "site": {
        "id": 2,
        "url": "/api/dcim/sites/2/",
        "display": "TST1",
        "name": "TST1",
        "slug": "tst1"
    },
}

# ipam/prefixes data for Netbox >= v4.2
PREFIX_V4 = {
    "id": 1,
    "url": "/api/ipam/prefixes/1/",
    "prefix": "10.0.0.0/24",
    "scope": {
        "id": 2,
        "url": "/api/dcim/sites/2/",
        "display": "TST1",
        "name": "TST1",
        "slug": "tst1",
        "description": ""
    },
}

# Example that does not raise an error (not recommended)
site: str = PREFIX_V3.get("site", {}).get("name", "")  # aceptable in Netbox < v4.2
print(f"{site=}")
site: str = PREFIX_V4.get("site", {}).get("name", "")  # not aceptable in Netbox >= v4.2
print(f"{site=}")
# site="TST1"
# site=""

# Example that raises an error (recommended)
try:
    site: str = NbValue(PREFIX_V3).str("site", "name")
    print(f"{site=}")
except NbVersionError as ex:
    print(ex)
# Deprecated model "ipam/prefixes.site" in /api/ipam/prefixes/1/, please use "ipam/prefixes.scope".
