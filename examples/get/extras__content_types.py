"""Example NbApi.extras.content_types.get().

extras/content-types < v4.5
extras/object-types >= v4.5
"""
import logging

from nbforager import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.extras.object_types.get()

# WEB UI Filter parameters

# Data Filter parameters
objects = nb.extras.object_types.get(q=["admin", "auth"])

objects1 = nb.extras.object_types.get(id=1)
objects = nb.extras.object_types.get(id=[1, 2])

objects = nb.extras.object_types.get(app_label="ipam", model="aggregate")

objects1 = nb.extras.object_types.get(app_label="dcim")
objects = nb.extras.object_types.get(app_label=["dcim", "ipam"])

objects1 = nb.extras.object_types.get(model="aggregate")
objects = nb.extras.object_types.get(model=["aggregate", "site"])
x = 1
