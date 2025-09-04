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
NB_PREFIX = {
    "id": 1,
    "url": "/api/ipam/prefixes/1",
    "site": {"name": "Name"},
}
NB_PREFIX_WO_URL = {
    "site": {"name": "Name"},
}
NB_PREFIX_SCOPE_SITE = {
    "id": 1,
    "url": "/api/ipam/prefixes/1",
    "scope_type": "dcim.site",
    "scope": {"name": "Name"},
}
NB_PREFIX_SCOPE_SITE_WO_URL = {
    "scope_type": "dcim.site",
    "scope": {"name": "Name"},
}
NB_PREFIX_SCOPE_REGION = {
    "id": 1,
    "url": "/api/ipam/prefixes/1",
    "scope_type": "dcim.region",
    "scope": {"name": "Name"},
}
