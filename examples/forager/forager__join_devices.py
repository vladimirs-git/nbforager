"""Example NbForager.join_tree() join devices."""
import logging
from pprint import pprint

from nbforager import NbForager

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nbf = NbForager(host=HOST, token=TOKEN)

# SITE
# Get only 1 device and site from Netbox.
# Note that the site in the device only contains basic data and
# does not include tags, region and other extended data.
nbf.dcim.devices.get(id=1)
nbf.dcim.sites.get()
pprint(nbf.root.dcim.devices)
# {88: {"id": 88,
#       "name": "PP:B117",
#       "site": {"id": 21,
#      ...

# Assemble objects within self.
# Note that the device now includes site region and all other data.
nbf.join_tree()
pprint(nbf.tree.dcim.devices)
# {88: {"id": 88,
#       "name": "PP:B117",
#       "site": {"id": 21,
#                "region": {"id": 40,
#                           "name": "North Carolina",
#                           "url": "https://demo.netbox.dev/api/dcim/regions/40/",
#      ...

# You can access any site attribute through a device.
print(list(nbf.tree.dcim.devices.values())[0]["site"]["region"]["name"])  # North Carolina

# Get devices with site data using nested=True.
nbf.clear()
device_id = 5393
nbf.dcim.devices.get(id=device_id, nested=True)
nbf.join_tree()
print(list(nbf.tree.dcim.devices.values())[0]["site"]["region"]["name"])  # North Carolina

# INTERFACES
# Get only 1 device and related interfaces from Netbox.
nbf.dcim.devices.get(id=device_id)
nbf.dcim.interfaces.get(device_id=device_id)
nbf.join_tree(dcim=True)
pprint(nbf.tree.dcim.devices)
# {5393: {"id": 5393,
#       "name": "rix3-03-p015-cnx",
#       "interfaces": {"Ethernet1/1": {"id": 66510, "name": "Ethernet1/1", ... }
#                      "Ethernet1/2": {"id": 66511, "name": "Ethernet1/2", ... }
#      ...
