"""Example NbForager.read_cache()."""
import logging
from pprint import pprint

from nbforager import NbForager

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
CACHE = "./demo.netbox.dev.pickle"
nbf = NbForager(host=HOST, token=TOKEN, cache=CACHE)

# Get objects from Netbox and save objects to the cache.
nbf.get_status()
nbf.ipam.aggregates.get()
nbf.ipam.prefixes.get()

pprint(nbf.root.ipam.aggregates)
# {1: {"id": 1,
#      "prefix": "10.0.0.0/8",
#      ...

# Write cache to pickle file
nbf.write_cache()

# Init new NbForager object and load cached objects.
# Note that you can use cached objects in scripts that have no network connectivity with Netbox API.
nbf = NbForager(host=HOST, cache=CACHE)
print(f"{nbf}")  # <NbForager: >
pprint(nbf.root.ipam.aggregates)
# {}

nbf.read_cache()
print(f"{nbf}")  # <NbForager: ipam=4, tenancy=6>
pprint(nbf.root.ipam.aggregates)
# {1: {"id": 1,
#      "prefix": "10.0.0.0/8",
#      ...

pprint(nbf.status["meta"])
# {"host": "demo.netbox.dev",
#  "url": "https://demo.netbox.dev/api/",
#  "write_time": "2020-12-31 23:59:59"}
