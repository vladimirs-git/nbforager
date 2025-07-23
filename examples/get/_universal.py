"""Example of universal parameters."""
import logging

from nbforager import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.ipam.prefixes.get(family=[4], status="active")
id1 = objects[3]["id"]

# Get using offset
count = nb.ipam.prefixes.get_count(family=[4], status="active")
objects_ = nb.ipam.prefixes.get(family=[4], status="active", limit=2, offset=3)
id2 = objects_[0]["id"]
assert len(objects_) == 2
assert id1 == id2
