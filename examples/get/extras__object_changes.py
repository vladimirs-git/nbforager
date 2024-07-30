"""Example NbApi.extras.object_changes.get()."""
import logging

from nbforager import NbApi

# Enable logging DEBUG mode
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

HOST = "demo.netbox.dev"
TOKEN = "1234567890123456789012345678901234567890"
nb = NbApi(host=HOST, token=TOKEN)

# All objects
# objects = nb.extras.object_changes.get()

# WEB UI Filter parameters
interface = "GigabitEthernet1/0/1"
objects = nb.extras.object_changes.get(q=interface)
objects = nb.extras.object_changes.get(q=interface, time_before="2024-07-30 05:23:42")
objects = nb.extras.object_changes.get(q=interface, time_after="2024-07-30 05:23:42")
objects = nb.extras.object_changes.get(q=interface, action="create")
objects = nb.extras.object_changes.get(q=interface, action="update")
objects = nb.extras.object_changes.get(q=interface, action="delete")
objects = nb.extras.object_changes.get(q=interface, user_id="1")  # admin
objects = nb.extras.object_changes.get(q=interface, name="admin")
objects = nb.extras.object_changes.get(q=interface, user_name="admin")
objects = nb.extras.object_changes.get(q=interface, changed_object_type_id=39)  # dcim.interfaces
objects = nb.extras.object_changes.get(q=interface, changed_object_type="dcim.interface")
objects = nb.extras.object_changes.get(changed_object_id=1721)  # interface id
