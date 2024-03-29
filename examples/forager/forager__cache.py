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
nbf.join_tree()

pprint(nbf.root.ipam.aggregates)
# {1: {"id": 1,
#      "prefix": "10.0.0.0/8",
#      ...

pprint(nbf.tree.ipam.aggregates)
# {1: {"prefix": "10.0.0.0/8",
#      "ipv4": <IPv4Obj 10.0.0.0/8>,
# "sub_prefixes": [{"prefix": "10.112.0.0/15",
#                   "ipv4": <IPv4Obj 10.112.0.0/15>,
#                   "aggregate": <Recursion on dict with id=2625332189056>,
#                   "super_prefix": {},
#                   "sub_prefixes": [{"prefix": "10.112.0.0/17",
#                                     "ipv4": <IPv4Obj 10.112.0.0/17>,
#                                     "aggregate": <Recursion on dict with id=2625332189056>,
#                                     "super_prefix": <Recursion on dict with id=2625332190912>,
#                                     "sub_prefixes": [],
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
#      "url": "https://demo.netbox.dev/api/ipam/aggregates/1/"},
#      ...
pprint(nbf.status["meta"])
# {"host": "demo.netbox.dev",
#  "url": "https://demo.netbox.dev/api/",
#  "write_time": "2020-12-31 23:59:59"}
