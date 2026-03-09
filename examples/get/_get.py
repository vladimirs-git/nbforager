"""Example NbApi.get()."""
import logging

from nbforager import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All dcim/sites objects
objects = nb.get(url="/dcim/sites/")

# Single dcim/sites object filtered by id
objects = nb.get(url="/dcim/sites/1/")
