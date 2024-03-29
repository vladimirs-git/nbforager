"""Example NbApi.dcim.regions.get()."""
import logging

from nbforager import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.dcim.regions.get()

# WEB UI Filter parameters
objects = nb.dcim.regions.get(q=["REGION"])
objects = nb.dcim.regions.get(tag="tag1")
objects = nb.dcim.regions.get(or_tag=["tag1", "tag2"])
objects = nb.dcim.regions.get(parent=["REGION1"])
objects = nb.dcim.regions.get(parent_id=[1, 2])

# not working
# Contacts
# objects = nb.dcim.regions.get(contact=["CONTACT1"])
# objects = nb.dcim.regions.get(contact_id=[1])
# objects = nb.dcim.regions.get(contact_role=["CONTACT1"])
# objects = nb.dcim.regions.get(contact_role_id=[1])
# objects = nb.dcim.regions.get(contact_group=["CONTACT ROLE1"])
# objects = nb.dcim.regions.get(contact_group_id=[1])

# Data Filter parameters
objects = nb.dcim.regions.get(id=[1, 2])
objects = nb.dcim.regions.get(name=["REGION1", "REGION2"])
objects = nb.dcim.regions.get(slug=["region1", "region2"])
objects = nb.dcim.regions.get(description=["DESCRIPTION1", "DESCRIPTION2"])
