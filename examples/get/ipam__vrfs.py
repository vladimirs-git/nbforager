"""Example NbApi.ipam.vrfs.get()."""
import logging

from nbforager import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.ipam.vrfs.get()

# WEB UI Filter parameters
objects = nb.ipam.vrfs.get(q=["VRF"])
objects = nb.ipam.vrfs.get(tag="tag1")
objects = nb.ipam.vrfs.get(or_tag=["tag1", "tag2"])

# Route Targets
objects = nb.ipam.vrfs.get(import_target=["65101:1", "65102:1"])
objects = nb.ipam.vrfs.get(import_target_id=[1, 2])
objects = nb.ipam.vrfs.get(export_target=["65101:1", "65102:1"])
objects = nb.ipam.vrfs.get(export_target_id=[1, 2])

# Tenant
objects = nb.ipam.vrfs.get(tenant_group=["TENANT GROUP1", "TENANT GROUP2"])
objects = nb.ipam.vrfs.get(tenant_group_id=[1, 2])
objects = nb.ipam.vrfs.get(tenant=["TENANT1", "TENANT2"])
objects = nb.ipam.vrfs.get(tenant_id=[1, 2])

# Data Filter parameters
objects = nb.ipam.vrfs.get(id=[1, 2])
objects = nb.ipam.vrfs.get(name=["VRF1", "VRF2"])
objects = nb.ipam.vrfs.get(slug=["vrf1", "vrf2"])
objects = nb.ipam.vrfs.get(description=["DESCRIPTION1", "DESCRIPTION2"])
