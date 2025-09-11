"""Params nb_value.py."""
from copy import deepcopy

# dcim/devices.device_role.name
NB_DEVICE_DEVICE_ROLE = {
    "id": 1,
    "url": "/api/dcim/devices/1",
    "device_role": {"id": 2, "name": "Name", "slug": "name"},
}
NB_DEVICE_DEVICE_ROLE_WO_URL = {
    "device_role": {"name": "Name", "slug": "name"},
}

NB_DEVICE_ROLE = {
    "id": 1,
    "url": "/api/dcim/devices/1",
    "role": {"id": 2, "name": "Name", "slug": "name"},
}
NB_DEVICE_ROLE_WO_URL = {
    "role": {"id": 2, "name": "Name", "slug": "name"},
}

# dcim/devices.primary_ip4.address
NB_DEVICE_PRIMARY_IP4 = {
    "id": 1,
    "url": "/api/dcim/devices/1",
    "primary_ip": {"id": 2, "family": 4, "address": "10.0.0.1/32"},
    "primary_ip4": {"id": 2, "family": 4, "address": "10.0.0.1/32"},
}
NB_DEVICE_PRIMARY_IP4_WO_URL = deepcopy(NB_DEVICE_PRIMARY_IP4)
del NB_DEVICE_PRIMARY_IP4_WO_URL["id"]
del NB_DEVICE_PRIMARY_IP4_WO_URL["url"]

NB_DEVICE_PRIMARY_IP4_FAMILY = {
    "id": 1,
    "url": "/api/dcim/devices/1",
    "primary_ip": {"id": 2, "family": {"value": 4, "label": "IPv4"}, "address": "10.0.0.1/32"},
    "primary_ip4": {"id": 2, "family": {"value": 4, "label": "IPv4"}, "address": "10.0.0.1/32"},
}
NB_DEVICE_PRIMARY_IP4_FAMILY_WO_URL = deepcopy(NB_DEVICE_PRIMARY_IP4_FAMILY)
del NB_DEVICE_PRIMARY_IP4_FAMILY_WO_URL["id"]
del NB_DEVICE_PRIMARY_IP4_FAMILY_WO_URL["url"]

NB_DEVICE_PRIMARY_IP6 = {
    "id": 1,
    "url": "/api/dcim/devices/1",
    "primary_ip": {"id": 2, "family": 4, "address": "::ffff:10.0.0.1/128"},
    "primary_ip6": {"id": 2, "family": 4, "address": "::ffff:10.0.0.1/128"},
}

# ipam/prefixes.site.name
PREFIX_ID = 1
SITE_ID = 2
SCOPE_ID = 3
NB_PREFIX = {
    "id": PREFIX_ID,
    "url": "/api/ipam/prefixes/1",
    "site": {"id": SITE_ID, "name": "Name", "slug": "name"},
}
NB_PREFIX_WO_URL = {
    "site": {"id": SITE_ID, "name": "Name", "slug": "name"},
}

NB_PREFIX_SCOPE_SITE = {
    "id": PREFIX_ID,
    "url": "/api/ipam/prefixes/1",
    "scope_type": "dcim.site",
    "scope": {"id": SCOPE_ID, "name": "Name", "slug": "name"},
}
NB_PREFIX_SCOPE_SITE_WO_URL = {
    "scope_type": "dcim.site",
    "scope": {"id": SCOPE_ID, "name": "Name", "slug": "name"},
}

NB_PREFIX_SCOPE_REGION = {
    "id": PREFIX_ID,
    "url": "/api/ipam/prefixes/1",
    "scope_type": "dcim.region",
    "scope": {"id": SCOPE_ID, "name": "Name", "slug": "name"},
}
