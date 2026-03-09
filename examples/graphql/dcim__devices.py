"""Example NbApi.dcim.devices.graphql()."""
import logging

from requests import HTTPError

from nbforager import NbApi, NbForager

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# # All dcim/devices
# devices = nb.dcim.devices.graphql(fields="id name")
# print(devices)  # [{"id": 1, "name": "DEVICE1"}, ...

# Filter dcim/devices
filters='''
{
    status: {exact: STATUS_ACTIVE},
    primary_ip4: {},
}
'''
devices = nb.dcim.devices.graphql(fields="id name primary_ip4", filters=filters)
print(devices)  # [{"id": 1, "name": "DEVICE1"}, ...
x = 1