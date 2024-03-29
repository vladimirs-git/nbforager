"""Example NbApi.circuits.provider_networks.get()."""
import logging

from nbforager import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
objects = nb.circuits.provider_networks.get()

# WEB UI Filter parameters
objects = nb.circuits.provider_networks.get(q=["PROVIDER NETWORK"])
objects = nb.circuits.provider_networks.get(tag="tag1")
objects = nb.circuits.provider_networks.get(or_tag=["tag1", "tag2"])

# Attributes
objects = nb.circuits.provider_networks.get(provider=["PROVIDER1", "PROVIDER2"])
objects = nb.circuits.provider_networks.get(provider_id=[1, 2])
objects = nb.circuits.provider_networks.get(service_id=["Service ID"])

# Data Filter parameters
objects = nb.circuits.provider_networks.get(id=[1, 2])
objects = nb.circuits.provider_networks.get(name=["PROVIDER NETWORK1", "PROVIDER NETWORK2"])
objects = nb.circuits.provider_networks.get(description=["DESCRIPTION1", "DESCRIPTION2"])
