"""Example NbApi.dcim.sites.graphql()."""
import logging

from requests import HTTPError

from nbforager import NbApi, NbForager

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All dcim/sites
sites = nb.dcim.sites.graphql(fields="id name")
print(sites)  # [{"id": 1, "name": "SITE1"}, ...

# Filter dcim/sites
sites = nb.dcim.sites.graphql(
    fields="id name",
    filters='{status: {exact: STATUS_RETIRED}, name: {exact: "SITE1"}}',
)
print(sites)  # [{"id": 1, "name": "SITE1"}, ...

# Syntax error
try:
    sites = nb.dcim.sites.graphql(fields="id name", filters="{status: {")
except HTTPError as ex:
    print(ex)  # 200 Errors: [{"message": "Syntax Error: Expected Name, found ...


# Write cache
nbf = NbForager(host=HOST, token=TOKEN)
nbf.dcim.sites.graphql(fields="id name")
print(nbf.root.dcim.sites.values())  # [{"id": 1, "name": "SITE1", "url": "..."}, ...
nbf.write_cache()


# Read cache
nbf = NbForager(host=HOST, token=TOKEN)
nbf.read_cache()
print(nbf.root.dcim.sites.values())  # [{"id": 1, "name": "SITE1", "url": "..."}, ...
