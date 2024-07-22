"""Example NbApi.ipam.ip_addresses.create() NbApi.ipam.ip_addresses.delete()."""
import logging

from nbforager import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

address = "10.1.1.2/24"

if not nb.ipam.ip_addresses.get(address=address):
    data = nb.ipam.ip_addresses.create_d(address=address)
    response = nb.ipam.ip_addresses.delete(id=data["id"])
    response = nb.ipam.ip_addresses.delete(id=11111111111111111)
    print(response)
