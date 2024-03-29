"""Example NbApi.tenancy.tenant_groups.get()."""
import logging

from nbforager import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.tenancy.tenant_groups.get()

# WEB UI filter parameters
objects = nb.tenancy.tenant_groups.get(q=["TENANT GROUP1"])
objects = nb.tenancy.tenant_groups.get(tag="tag1")
objects = nb.tenancy.tenant_groups.get(or_tag=["tag1", "tag2"])
objects = nb.tenancy.tenant_groups.get(parent=["TENANT GROUP1"])
objects = nb.tenancy.tenant_groups.get(parent_id=[1, 2])
# 
# Data filter parameters
objects = nb.tenancy.tenant_groups.get(id=[1, 2])
objects = nb.tenancy.tenant_groups.get(name=["TENANT GROUP1", "TENANT GROUP2"])
objects = nb.tenancy.tenant_groups.get(slug=["tenant-group1", "tenant-group2"])
