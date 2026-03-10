"""Example NbValue."""

from nbforager import NbApi, NbValue

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# Get object from Netbox
sites = nb.dcim.sites.get(tag="alpha")
site = sites[0]

# Getting the same data using dictionary keys as usual, just to compare with NbValue
tags = [d["slug"] for d in site["tags"]]
print(tags)
# ["alpha", "bravo", "golf"]

# Get the tag slug using the NbValue object.
nbv = NbValue(data=site)
tags = nbv.tag_slugs()
print(tags)
# ["alpha", "bravo", "golf"]
