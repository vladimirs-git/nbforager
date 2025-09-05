"""Params nb_value.py."""

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
