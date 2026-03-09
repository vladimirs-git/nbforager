"""Example NbApi.dcim.devices.graphql()."""
import logging

from nbforager import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All dcim/devices
devices = nb.dcim.devices.graphql(fields="id name")
print(devices)  # [{"id": 1, "name": "DEVICE1"}, ...

# Filter dcim/devices
fields="""
id
name
primary_ip4 { id address }
tenant { id slug }
platform { id slug }
role { id slug }
"""
filters_v454='''
{
    status: {exact: STATUS_ACTIVE},
    primary_ip4: {id: {is_null: false}},
    tenant: {slug: {exact: "dunder-mifflin"}},
    platform: {slug: {exact: "cisco-ios"}},
    role: {slug: {exact: "router"}},
}
'''
filters_v446='''
{
    status: STATUS_ACTIVE,
    primary_ip4: {address: {is_null: false}},
    tenant: {slug: {in_list: ["itbo-noc", "noc"]}},
    platform: {slug: {exact: "paloalto_panos"}},
    role: {slug: {exact: "firewall"}},
}
'''
devices = nb.dcim.devices.graphql(fields=fields, filters=filters_v454)
print(devices)  # [{"id": 1, "name": "DEVICE1"}, ...
