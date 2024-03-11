"""Examples with PyNetbox."""
import logging

import dictdiffer
import pynetbox
from pynetbox.models.ipam import Aggregates

from nbforager import NbApi
from nbforager.types_ import DAny

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)
pynb = pynetbox.api(url=f"https://{HOST}", token=TOKEN)

# Get aggregate by pynetbox
obj1: Aggregates = pynb.ipam.aggregates.get(prefix="10.0.0.0/8")
id1 = obj1.id
data1: DAny = dict(obj1)

# Get aggregate by NbApi
aggrs = nb.ipam.aggregates.get(prefix="10.0.0.0/8")
data2: DAny = aggrs[0]

# Check object is the same
diff = list(dictdiffer.diff(data1, data2))
print(f"{diff=}")  # diff=[]

# Update aggregate by pynetbox based on the NbApi data
obj2: Aggregates = Aggregates(data2, obj1.api, obj1.endpoint)
print(f"{obj2.comments=}")  # obj2.comments="COMMENT1"
obj2.update({"comments": f"{obj2.comments} updated"})

obj3: Aggregates = pynb.ipam.aggregates.get(prefix="10.0.0.0/8")
print(f"{obj3.comments=}")  # obj3.comments="COMMENT1 updated"
