"""Example NbApi.graphql()."""
import logging

from nbforager import NbApi

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All dcim/sites
query = """
query {
    site_list {
        id
        name
        tenant { id name }
    }
}
"""
response = nb.graphql(query)
print(response) # <Response [200]>
data = response.json()["data"]
print(data) # {"site_list": [{"id": "1", "name": "SITE1", "tenant": {"id": 1, ...

# Filter dcim/sites
query = """
query {
    site_list (
        filters: {
          status: {exact: STATUS_RETIRED}, 
          name: {exact: "SITE1"},
        }
    ) {
        id name status tenant { id name }
    }
}
"""
response = nb.graphql(query)
print(response) # <Response [200]>
data = response.json()["data"]
print(data)  # {"site_list": [{"id": "1", "name": "SITE1", "tenant": {"id": "1", "name": "NAME"}}]}

# Single dcim/sites by ID
query = """
query {
    site (id: 1) {
        id
        name
    }
}
"""
response = nb.graphql(query)
print(response) # <Response [200]>
data = response.json()["data"]
print(data) # {"site": {"id": "1", "name": "SITE1"}}

# Syntax error
response = nb.graphql(query="query { site_list")
print(response) # <Response [200]>
errors = response.json()["errors"]
print(errors) # [{'locations': [{'column': 18, 'line': 1}], ...