"""Example NbApi.dcim.locations.get()."""
import logging

from nbforager import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.dcim.locations.get()

# WEB UI Filter parameters
objects = nb.dcim.locations.get(q=["LOCATION"])
objects = nb.dcim.locations.get(tag="tag1")
objects = nb.dcim.locations.get(or_tag=["tag1", "tag2"])

# Attributes
objects = nb.dcim.locations.get(region=["REGION1", "REGION2"])
objects = nb.dcim.locations.get(region_id=[1, 2])
objects = nb.dcim.locations.get(site_group=["SITE GROUP1", "SITE GROUP2"])
objects = nb.dcim.locations.get(site_group_id=[1, 2])
objects = nb.dcim.locations.get(site=["SITE1", "SITE2"])
objects = nb.dcim.locations.get(site_id=[1, 2])
objects = nb.dcim.locations.get(parent=["LOCATION2"])
objects = nb.dcim.locations.get(parent_id=[1, 2])
objects = nb.dcim.locations.get(status=["active", "planned"])

# Tenant
objects = nb.dcim.locations.get(tenant_group=["TENANT GROUP1", "TENANT GROUP2"])
objects = nb.dcim.locations.get(tenant_group_id=[1, 2])
objects = nb.dcim.locations.get(tenant=["TENANT1", "TENANT2"])
objects = nb.dcim.locations.get(tenant_id=[1, 2])

# Data Filter parameters
objects = nb.dcim.locations.get(id=[1, 2])
objects = nb.dcim.locations.get(name=["LOCATION1", "LOCATION2"])
objects = nb.dcim.locations.get(slug=["location1", "location2"])
objects = nb.dcim.locations.get(description=["DESCRIPTION1", "DESCRIPTION2"])
