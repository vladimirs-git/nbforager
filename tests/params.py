# pylint: disable=too-many-lines
"""Parameters for tests."""

from nbforager.types_ import DAny

HOSTNAME1 = "DEVICE1"
HOSTNAME2 = "DEVICE2"
HOSTNAME3 = "DEVICE3"
HOSTNAME4 = "DEVICE4"
HOSTNAME5 = "DEVICE5"  # virtual machine
D1 = 1
D2 = 2
D3 = 3
D4 = 4
D5 = 5

ETHERNET11 = "GigabitEthernet1/0/1"
ETHERNET12 = "GigabitEthernet1/0/2"
ETHERNET21 = "GigabitEthernet2/0/1"
VIRTUAL_ETH1 = "eth1"
CONSOLE = "console1"
D1P1 = 11
D1P2 = 12
D2P1 = 13
D3P1 = 14
D4P1 = 15
D5P1 = 16
D1C1 = 17

# circuits
PROVIDER = "PROVIDER1"
PR1 = 30
CIRCUIT_TYPE = "WAN link"
CT1 = 31
CID1 = "CID1"
CID2 = "CID2"
C1 = 32
C2 = 33
TR1 = 34
TR2 = 35
# cables
CB1 = 41
CB2 = 42
CB3 = 43

# sites
RIX1 = "RIX1"
RIX1_ = "rix1"
RIX2 = "RIX2"
RIX2_ = "rix2"
RIX3 = "RIX3"
RIX3_ = "rix3"
S1 = 51
S2 = 52
S3 = 53
TENANT1 = "TENANT1"
TENANT1_ = "tenant1"
TN1 = 53

# tags
TAG1 = "TAG1"
TAG2 = "TAG2"
TAG3 = "TAG3"
T1 = 61
T2 = 62
T3 = 63

# prefixes
AGGREGATE1 = "10.0.0.0/16"
AGGREGATE2 = "1.0.0.0/16"
AG1 = 1
AG2 = 2
PREFIX1 = "10.0.0.0/24"  # global, vrf
PREFIX2 = "1.0.0.0/24"  # public
PREFIX4 = "10.0.0.0/31"
PREFIX5 = "10.0.0.0/32"
P1 = 11
P2 = 12
P3 = 13
P4 = 14
P5 = 15
ADDRESS1 = "10.0.0.1/24"
ADDRESS2 = "1.0.0.2/24"  # public
ADDRESS3 = "10.0.0.3/24"
ADDRESS4 = "10.0.0.4/24"
A1 = 21
A2 = 22
A3 = 23
A4 = 24
ROLE1 = "ROLE1"
ROLE1_ = "role1"
ROLE2 = "ROLE2"
ROLE2_ = "role2"
ROLE3 = "ROLE3"
ROLE3_ = "role3"
R1 = 31
R2 = 32
R3 = 33

PROVIDER1_D: DAny = {
    "id": PR1,
    "url": f"/api/circuits/providers/{PR1}/",
    "name": PROVIDER,
    "slug": "provider1",
    "asns": {"id": 1, "url": "/api/ipam/asns/1/", "asn": 65001},
}
PROVIDERS = {d["id"]: d for d in [PROVIDER1_D]}

PROVIDER_ACCOUNT1_D: DAny = {
    "id": 1,
    "url": "/api/circuits/provider-accounts/1/",
    "name": "PROVIDER ACCOUNT1",
    "provider": {"id": PR1, "url": f"/api/circuits/providers/{PR1}/", "name": PROVIDER},
}
PROVIDER_ACCOUNTS = {d["id"]: d for d in [PROVIDER_ACCOUNT1_D]}

PROVIDER_NETWORK1_D: DAny = {
    "id": 1,
    "url": "/api/circuits/provider-networks/1/",
    "name": "PROVIDER NETWORK1",
    "provider": {"id": PR1, "url": f"/api/circuits/providers/{PR1}/", "name": PROVIDER},
}
PROVIDER_NETWORKS = {d["id"]: d for d in [PROVIDER_NETWORK1_D]}

CIRCUIT_TYPE1_D: DAny = {
    "id": CT1,
    "url": f"/api/circuits/circuit-types/{CT1}/",
    "name": CIRCUIT_TYPE,
    "slug": "wan-link",
}
CIRCUIT_TYPES = {d["id"]: d for d in [CIRCUIT_TYPE1_D]}

# D1_INTERFACE1--CABLE1--TERM_A-CIRCUIT1-TERM_Z--CABLE2--D2_INTERFACE1
CABLE1_D: DAny = {
    "id": CB1,
    "url": f"/api/dcim/cables/{CB1}/",
    "display": f"#{CB1}",
    "a_terminations": [
        {
            "object_id": TR1,
            "object_type": "circuits.circuittermination",
            "object": {
                "id": TR1,
                "url": f"/api/circuits/circuit-terminations/{TR1}/",
                "circuit": {"id": C1, "url": f"/api/circuits/circuits/{C1}/", "cid": CID1},
                "term_side": "A",
                "cable": CB1,
                "_occupied": True,
            },
        },
    ],
    "b_terminations": [
        {
            "object_id": D1P1,
            "object_type": "dcim.interface",
            "object": {
                "id": D1P1,
                "url": f"/api/dcim/interfaces/{D1P1}/",
                "name": ETHERNET11,
                "device": {"id": D1, "url": f"/api/dcim/devices/{D1}/", "name": HOSTNAME1},
                "cable": CB1,
                "_occupied": True
            },
        },
    ],
    "status": {"value": "connected"},
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
}
CABLE2_D: DAny = {
    "id": CB2,
    "url": f"/api/dcim/cables/{CB2}/",
    "display": f"#{CB2}",
    "a_terminations": [
        {
            "object_id": TR2,
            "object_type": "circuits.circuittermination",
            "object": {
                "id": TR2,
                "url": f"/api/circuits/circuit-terminations/{TR2}/",
                "circuit": {"id": C1, "url": f"/api/circuits/circuits/{C1}/", "cid": CID1},
                "term_side": "Z",
                "cable": CB2,
                "_occupied": True,
            },
        }
    ],
    "b_terminations": [
        {
            "object_id": D2P1,
            "object_type": "dcim.interface",
            "object": {
                "id": D2P1,
                "url": f"/api/dcim/interfaces/{D2P1}/",
                "name": ETHERNET11,
                "device": {"id": D2, "url": f"/api/dcim/devices/{D2}/", "name": HOSTNAME2},
                "cable": CB2,
                "_occupied": True
            },
        },
    ],
    "status": {"value": "connected"},
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
}
CIRCUIT1_D: DAny = {
    "id": C1,
    "url": f"/api/circuits/circuits/{C1}/",
    "cid": CID1,
    "provider": {"id": PR1, "url": f"/api/circuits/providers/{PR1}/", "name": PROVIDER},
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
    "type": {"id": CT1, "url": f"/api/circuits/circuit-types/{CT1}/", "name": CIRCUIT_TYPE},
    "termination_a": {
        "id": TR1,
        "url": f"/api/circuits/circuit-terminations/{TR1}/",
        "site": {"id": S1, "url": f"/api/dcim/sites/{S1}/", "name": RIX1, "slug": RIX1_},
    },
    "termination_z": {
        "id": TR2,
        "url": f"/api/circuits/circuit-terminations/{TR2}/",
        "site": {"id": S2, "url": f"/api/dcim/sites/{S2}/", "name": RIX2, "slug": RIX2_},
    },
}
CIRCUITS = {d["id"]: d for d in [CIRCUIT1_D]}

TERMINATION1_D: DAny = {
    "id": TR1,
    "url": f"/api/circuits/circuit-terminations/{TR1}/",
    "display": f"{CID1}: Termination A",
    "circuit": {"id": C1, "url": f"/api/circuits/circuits/{C1}/", "cid": CID1},
    "term_side": "A",
    "site": {"id": S1, "url": f"/api/dcim/sites/{S1}/", "name": RIX1, "slug": RIX1_},
    "link_peers_type": "dcim.interface",
    "link_peers": [
        {
            "id": D1P1,
            "url": f"/api/dcim/interfaces/{D1P1}/",
            "name": ETHERNET11,
            "device": {"id": D1, "url": f"/api/dcim/devices/{D1}/", "name": HOSTNAME1},
        },
    ],
}
TERMINATION2_D: DAny = {
    "id": TR2,
    "url": f"/api/circuits/circuit-terminations/{TR2}/",
    "display": f"{CID1}: Termination Z",
    "circuit": {"id": C1, "url": f"/api/circuits/circuits/{C1}/", "cid": CID1},
    "term_side": "Z",
    "site": {"id": S2, "url": f"/api/dcim/sites/{S2}/", "name": RIX2, "slug": RIX2_},
    "link_peers_type": "dcim.interface",
    "link_peers": [
        {
            "id": D2P1,
            "url": f"/api/dcim/interfaces/{D2P1}/",
            "name": ETHERNET11,
            "device": {"id": D2, "url": f"/api/dcim/devices/{D2}/", "name": HOSTNAME2},
        },
    ],
}
TERMINATIONS = {int(d["id"]): d for d in [TERMINATION1_D, TERMINATION2_D]}

# D1_INTERFACE2--CABLE3--D3_INTERFACE1
CABLE3_D: DAny = {
    "id": CB3,
    "url": f"/api/dcim/cables/{CB3}/",
    "display": f"#{CB3}",
    "a_terminations": [
        {
            "object_id": D1P2,
            "object_type": "dcim.interface",
            "object": {
                "id": D1P2,
                "name": ETHERNET12,
                "url": f"/api/dcim/interfaces/{D1P2}/",
                "device": {"id": D1, "url": f"/api/dcim/devices/{D1}/", "name": HOSTNAME1},
                "cable": CB3,
                "_occupied": True,
            },
        }
    ],
    "b_terminations": [
        {
            "object_id": D3P1,
            "object_type": "dcim.interface",
            "object": {
                "id": D3P1,
                "name": ETHERNET11,
                "url": f"/api/dcim/interfaces/{D3P1}/",
                "device": {"id": D3, "url": f"/api/dcim/devices/{D3}/", "name": HOSTNAME3},
                "cable": CB3,
                "_occupied": True,
            },
        }
    ],
    "status": {"value": "connected"},
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
}
CABLES = {d["id"]: d for d in [CABLE1_D, CABLE2_D, CABLE3_D]}

CONSOLE1_D: DAny = {
    "id": D1C1,
    "url": f"/api/dcim/console-ports/{D1C1}/",
    "name": CONSOLE,
    "device": {"id": D1, "url": f"/api/dcim/devices/{D1}/", "name": HOSTNAME1},
}
CONSOLES = {d["id"]: d for d in [CONSOLE1_D]}

DEVICE_ROLE1_D: DAny = {
    "id": 1,
    "url": "/api/dcim/device-roles/1/",
    "name": "DEVICE ROLE1",
    "slug": "device-role1",
}
DEVICE_ROLE3_D: DAny = {
    "id": 3,
    "url": "/api/dcim/device-roles/3/",
    "name": "DEVICE ROLE3",
    "slug": "device-role3",
}
DEVICE_ROLES = {d["id"]: d for d in [DEVICE_ROLE1_D, DEVICE_ROLE3_D]}

DEVICE_TYPE1_D: DAny = {
    "id": 1,
    "url": "/api/dcim/device-types/1/",
    "name": "MODEL1",
    "slug": "model1",
    "manufacturer": {"id": 1, "url": "/api/dcim/manufacturers/1/", "name": "MANUFACTURER1"},
}
DEVICE_TYPES = {d["id"]: d for d in [DEVICE_TYPE1_D]}

DEVICE_TYPE3_D: DAny = {
    "id": 3,
    "url": "/api/dcim/device-types/3/",
    "name": "MODEL3",
    "slug": "model3",
    "manufacturer": {"id": 1, "url": "/api/dcim/manufacturers/1/", "name": "MANUFACTURER1"},
}
MANUFACTURER1_D: DAny = {
    "id": 1,
    "url": "/api/dcim/manufacturers/1/",
    "name": "MANUFACTURER1",
    "slug": "manufacturer1",
}
MANUFACTURERS = {d["id"]: d for d in [MANUFACTURER1_D]}

PLATFORM1_D: DAny = {
    "id": 1,
    "url": "/api/dcim/platforms/1/",
    "name": "PLATFORM1",
    "slug": "platform1",
}
PLATFORMS = {d["id"]: d for d in [PLATFORM1_D]}

# DEVICE1 is similar to DEVICE2
DEVICE1_D: DAny = {
    "id": D1,
    "url": f"/api/dcim/devices/{D1}/",
    "name": HOSTNAME1,
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "primary_ip4": {"address": "10.1.1.1/24"},
    "serial": "SERIAL1",
    "device_role": {"id": 1, "url": "/api/dcim/device-roles/1/", "name": "DEVICE ROLE1"},
    "device_type": {"id": 1, "url": "/api/dcim/device-types/1/", "name": "MODEL1"},
    "location": {"id": 1, "url": "/api/dcim/locations/1/", "name": "LOCATION1"},
    "platform": {"id": 1, "url": "/api/dcim/platforms/1/", "name": "PLATFORM1"},
    "rack": {"id": 1, "url": "/api/dcim/racks/1/", "name": "RACK1"},
    "site": {"id": S1, "url": f"/api/dcim/sites/{S1}/", "name": RIX1, "slug": RIX1_},
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
    "interface_count": 2,  # D1_INTERFACE1, D1_INTERFACE2
    "console_port_count": 1,
    "virtual_chassis": None,
    "vc_position": None,
    "vc_priority": None,
}
DEVICE2_D: DAny = {
    "id": D2,
    "url": f"/api/dcim/devices/{D2}/",
    "name": HOSTNAME2,
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "primary_ip4": {"address": "10.2.2.2/24"},
    "serial": "SERIAL2",
    "device_role": {"id": 1, "url": "/api/dcim/device-roles/1/", "name": "DEVICE ROLE1"},
    "device_type": {"id": 1, "url": "/api/dcim/device-types/1/", "name": "MODEL1"},
    "location": {"id": 1, "url": "/api/dcim/locations/1/", "name": "LOCATION1"},
    "platform": {"id": 1, "url": "/api/dcim/platforms/1/", "name": "PLATFORM1"},
    "rack": {"id": 1, "url": "/api/dcim/racks/1/", "name": "RACK1"},
    "site": {"id": S1, "url": f"/api/dcim/sites/{S1}/", "name": RIX1, "slug": RIX1_},
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
    "interface_count": 1,  # D2_INTERFACE1
    "console_port_count": 0,
    "virtual_chassis": None,
    "vc_position": None,
    "vc_priority": None,
}
# virtual chassis master
DEVICE3_D: DAny = {
    "id": D3,
    "url": f"/api/dcim/devices/{D3}/",
    "name": HOSTNAME3,
    "tags": [{"id": T3, "url": f"/api/extras/tags/{T3}/", "name": TAG3}],  # different
    "primary_ip4": {"address": "10.3.3.3/24"},
    "serial": "SERIAL1",  # the same as in DEVICE1
    "device_role": {"id": 3, "url": "/api/dcim/device-roles/3/", "name": "DEVICE ROLE3"},
    "device_type": {"id": 1, "url": "/api/dcim/device-types/3/", "name": "MODEL3"},
    "location": {"id": 1, "url": "/api/dcim/locations/1/", "name": "LOCATION1"},
    "platform": {"id": 1, "url": "/api/dcim/platforms/1/", "name": "PLATFORM1"},
    "rack": {"id": 1, "url": "/api/dcim/racks/1/", "name": "RACK1"},
    "site": {"id": S1, "url": f"/api/dcim/sites/{S1}/", "name": RIX1, "slug": RIX1_},
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
    "interface_count": 1,  # D3_INTERFACE1
    "console_port_count": 0,
    # virtual-chassis
    "virtual_chassis": {
        "id": 1,
        "url": "/api/dcim/virtual-chassis/1/",
        "name": HOSTNAME3,
        "master": {"id": D3, "url": f"/api/dcim/devices/{D3}/", "name": HOSTNAME3}
    },
    "vc_position": 1,
    "vc_priority": 1,
}
# virtual chassis member
DEVICE4_D: DAny = {
    "id": D4,
    "url": f"/api/dcim/devices/{D4}/",
    "name": HOSTNAME4,
    "tags": [],
    "primary_ip4": None,
    "serial": "SERIAL4",
    "device_role": {"id": 3, "url": "/api/dcim/device-roles/3/", "name": "DEVICE ROLE3"},
    "device_type": {"id": 1, "url": "/api/dcim/device-types/3/", "name": "MODEL3"},
    "location": {"id": 1, "url": "/api/dcim/locations/1/", "name": "LOCATION1"},
    "platform": {"id": 1, "url": "/api/dcim/platforms/1/", "name": "PLATFORM1"},
    "rack": {"id": 1, "url": "/api/dcim/racks/1/", "name": "RACK1"},
    "site": {"id": S1, "url": f"/api/dcim/sites/{S1}/", "name": RIX1, "slug": RIX1_},
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
    "interface_count": 1,  # D4_INTERFACE1
    "console_port_count": 0,
    # virtual-chassis
    "virtual_chassis": {
        "id": 1,
        "url": "/api/dcim/virtual-chassis/1/",
        "name": HOSTNAME3,
        "master": {"id": D3, "url": f"/api/dcim/devices/{D3}/", "name": HOSTNAME3}
    },
    "vc_position": 2,
    "vc_priority": 2,
}
DEVICES = {d["id"]: d for d in [DEVICE1_D, DEVICE2_D, DEVICE3_D, DEVICE4_D]}

VIRTUAL_CHASSIS1_D: DAny = {
    "id": 1,
    "url": "/api/dcim/virtual-chassis/1/",
    "name": HOSTNAME3,
    "domain": "DOMAIN1",
    "master": {"id": D3, "url": f"/api/dcim/devices/{D3}/", "name": HOSTNAME3},
    "tags": [],
    "custom_fields": {},
    "member_count": 2,  # DEVICE3, DEVICE4
}
VIRTUAL_CHASSIS = {d["id"]: d for d in [VIRTUAL_CHASSIS1_D]}

# global routing, 10.0.0.1/24
D1_INTERFACE1_D: DAny = {
    "id": D1P1,
    "url": f"/api/dcim/interfaces/{D1P1}/",
    "name": ETHERNET11,
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "device": {"id": D1, "url": f"/api/dcim/devices/{D1}/", "name": HOSTNAME1},
    "vdcs": [],
    "module": None,
    "label": "LABEL1",
    "type": {"value": "1000base-x-sfp", "label": "SFP (1GE)"},
    "enabled": True,
    "parent": None,
    "bridge": None,
    "lag": None,
    "mtu": 1500,
    "mac_address": "00:00:00:00:00:01",
    "speed": 1000000,
    "duplex": {"value": "auto", "label": "Auto"},
    "wwn": None,
    "mgmt_only": True,
    "description": "DESCRIPTION1",
    "mode": {"value": "tagged", "label": "Tagged"},
    "rf_role": None,
    "rf_channel": None,
    "poe_mode": None,
    "poe_type": None,
    "rf_channel_frequency": None,
    "rf_channel_width": None,
    "tx_power": 1,
    "untagged_vlan": {"id": 1, "url": "/api/ipam/vlans/1/", "vid": 1, "name": "VLAN1"},
    "tagged_vlans": [{"id": 2, "url": "/api/ipam/vlans/2/", "vid": 2, "name": "VLAN2"}],
    "mark_connected": True,
    "cable": {"id": CB1, "url": f"/api/dcim/cables/{CB1}/"},
    "cable_end": "A",
    "wireless_link": None,
    "link_peers_type": "circuits.circuittermination",
    "link_peers": [
        {
            "id": TR1,
            "url": f"/api/circuits/circuit_terminations/{TR1}/",
            "display": f"{CID1}: Termination A",
            "circuit": {"id": C1, "url": f"/api/circuits/circuits/{C1}/", "cid": CID1},
            "term_side": "A",
            "cable": CB1,
            "_occupied": True,
        },
    ],
    "connected_endpoints_type": "dcim.interface",
    "connected_endpoints_reachable": True,
    "connected_endpoints": [
        {
            "id": D2P1,
            "url": f"api/dcim/interfaces/{D2P1}/",
            "name": ETHERNET11,
            "device": {"id": D2, "url": f"/api/dcim/devices/{D2}/", "name": HOSTNAME2},
            "cable": C2,
            "_occupied": True,
        }
    ],
    "wireless_lans": [],
    "vrf": {"id": 1, "url": "/api/ipam/vrfs/1/", "name": "VRF1"},
    "l2vpn_termination": None,
    "custom_fields": {},
    "count_ipaddresses": 1,
}
# vrf VRF1, 10.0.0.3/24
D1_INTERFACE2_D: DAny = {
    "id": D1P2,
    "url": f"/api/dcim/interfaces/{D1P2}/",
    "name": ETHERNET12,
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "device": {"id": D1, "url": f"/api/dcim/devices/{D1}/", "name": HOSTNAME1},
    "vdcs": [],
    "module": None,
    "label": "LABEL2",
    "type": {"value": "1000base-x-sfp", "label": "SFP (1GE)"},
    "enabled": True,
    "parent": None,
    "bridge": None,
    "lag": None,
    "mtu": 1500,
    "mac_address": "00:00:00:00:00:02",
    "speed": 1000000,
    "duplex": {"value": "auto", "label": "Auto"},
    "wwn": None,
    "mgmt_only": True,
    "description": "DESCRIPTION2",
    "mode": {"value": "tagged", "label": "Tagged"},
    "rf_role": None,
    "rf_channel": None,
    "poe_mode": None,
    "poe_type": None,
    "rf_channel_frequency": None,
    "rf_channel_width": None,
    "tx_power": 1,
    "untagged_vlan": {"id": 1, "url": "/api/ipam/vlans/1/", "vid": 1, "name": "VLAN1"},
    "tagged_vlans": [{"id": 2, "url": "/api/ipam/vlans/2/", "vid": 2, "name": "VLAN2"}],
    "mark_connected": True,
    "cable": {"id": CB3, "url": f"/api/dcim/cables/{CB3}/"},
    "cable_end": "A",
    "link_peers_type": "dcim.interface",
    "link_peers": [
        {
            "id": D3P1,
            "url": f"/api/dcim/interfaces/{D3P1}/",
            "name": ETHERNET11,
            "device": {"id": D3, "url": f"/api/dcim/devices/{D3}/", "name": HOSTNAME3},
            "cable": CB3,
            "_occupied": True,
        }
    ],
    "connected_endpoints_type": "dcim.interface",
    "connected_endpoints_reachable": True,
    "connected_endpoints": [
        {
            "id": D3P1,
            "url": f"/api/dcim/interfaces/{D3P1}/",
            "name": ETHERNET11,
            "device": {"id": D3, "url": f"/api/dcim/devices/{D3}/", "name": HOSTNAME3},
            "cable": CB3,
            "_occupied": True,
        }
    ],
    "wireless_link": None,
    "wireless_lans": [],
    "vrf": {"id": 1, "url": "/api/ipam/vrfs/1/", "name": "VRF1"},
    "l2vpn_termination": None,
    "custom_fields": {},
    "count_ipaddresses": 1,
}
D2_INTERFACE1_D: DAny = {
    "id": D2P1,
    "url": f"/api/dcim/interfaces/{D2P1}/",
    "name": ETHERNET11,
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "device": {"id": D2, "url": f"/api/dcim/devices/{D2}/", "name": HOSTNAME2},
    "vdcs": [],
    "module": None,
    "label": "LABEL1",
    "type": {"value": "1000base-x-sfp", "label": "SFP (1GE)"},
    "enabled": True,
    "parent": None,
    "bridge": None,
    "lag": None,
    "mtu": 1500,
    "mac_address": "00:00:00:00:00:01",
    "speed": 1000000,
    "duplex": {"value": "auto", "label": "Auto"},
    "wwn": None,
    "mgmt_only": True,
    "description": "DESCRIPTION1",
    "mode": {"value": "tagged", "label": "Tagged"},
    "rf_role": None,
    "rf_channel": None,
    "poe_mode": None,
    "poe_type": None,
    "rf_channel_frequency": None,
    "rf_channel_width": None,
    "tx_power": 1,
    "untagged_vlan": {"id": 1, "url": "/api/ipam/vlans/1/", "vid": 1, "name": "VLAN1"},
    "tagged_vlans": [{"id": 2, "url": "/api/ipam/vlans/2/", "vid": 2, "name": "VLAN2"}],
    "mark_connected": True,
    "cable": {"id": CB2, "url": f"/api/dcim/cables/{CB2}/"},
    "cable_end": "B",
    "wireless_link": None,
    "link_peers_type": "circuits.circuittermination",
    "link_peers": [
        {
            "id": TR2,
            "url": f"/api/circuits/circuit_terminations/{TR2}/",
            "display": f"{CID1}: Termination Z",
            "circuit": {"id": C1, "url": f"/api/circuits/circuits/{C1}/", "cid": CID1},
            "term_side": "Z",
            "cable": CB2,
            "_occupied": True,
        },
    ],
    "connected_endpoints_type": "dcim.interface",
    "connected_endpoints_reachable": True,
    "connected_endpoints": [
        {
            "id": D1P1,
            "url": f"api/dcim/interfaces/{D1P1}/",
            "name": ETHERNET11,
            "device": {"id": D1, "url": f"/api/dcim/devices/{D1}/", "name": HOSTNAME1},
            "cable": C1,
            "_occupied": True,
        }
    ],
    "wireless_lans": [],
    "vrf": None,
    "l2vpn_termination": None,
    "custom_fields": {},
    "count_ipaddresses": 0,
}
D3_INTERFACE1_D: DAny = {
    "id": D3P1,
    "url": f"/api/dcim/interfaces/{D3P1}/",
    "name": ETHERNET11,
    "tags": [],
    "device": {"id": D3, "url": f"/api/dcim/devices/{D3}/", "name": HOSTNAME3},
    "vdcs": [],
    "module": None,
    "label": "LABEL1",
    "type": {"value": "1000base-x-sfp", "label": "SFP (1GE)"},
    "enabled": True,
    "parent": None,
    "bridge": None,
    "lag": None,
    "mtu": 1500,
    "mac_address": "00:00:00:00:00:02",
    "speed": 1000000,
    "duplex": {"value": "auto", "label": "Auto"},
    "wwn": None,
    "mgmt_only": True,
    "description": "DESCRIPTION1",
    "mode": {"value": "tagged", "label": "Tagged"},
    "rf_role": None,
    "rf_channel": None,
    "poe_mode": None,
    "poe_type": None,
    "rf_channel_frequency": None,
    "rf_channel_width": None,
    "tx_power": 1,
    "untagged_vlan": {"id": 1, "url": "/api/ipam/vlans/1/", "vid": 1, "name": "VLAN1"},
    "tagged_vlans": [{"id": 2, "url": "/api/ipam/vlans/2/", "vid": 2, "name": "VLAN2"}],
    "mark_connected": True,
    "cable": {"id": CB3, "url": f"/api/dcim/cables/{CB3}/"},
    "cable_end": "B",
    "link_peers_type": "dcim.interface",
    "link_peers": [
        {
            "id": D1P2,
            "url": f"/api/dcim/interfaces/{D1P2}/",
            "name": ETHERNET12,
            "device": {"id": D1, "url": f"/api/dcim/devices/{D1}/", "name": HOSTNAME1},
            "cable": CB3,
            "_occupied": True,
        }
    ],
    "connected_endpoints_type": "dcim.interface",
    "connected_endpoints_reachable": True,
    "connected_endpoints": [
        {
            "id": D1P2,
            "url": f"/api/dcim/interfaces/{D1P2}/",
            "name": ETHERNET12,
            "device": {"id": D1, "url": f"/api/dcim/devices/{D1}/", "name": HOSTNAME1},
            "cable": CB3,
            "_occupied": True,
        }
    ],
    "wireless_link": None,
    "wireless_lans": [],
    "vrf": None,
    "l2vpn_termination": None,
    "custom_fields": {},
    "count_ipaddresses": 0,
}
D4_INTERFACE1_D: DAny = {
    "id": D4P1,
    "url": f"/api/dcim/interfaces/{D4P1}/",
    "name": ETHERNET21,
    "tags": [],
    "device": {"id": D4, "url": f"/api/dcim/devices/{D4}/", "name": HOSTNAME4},
    "vdcs": [],
    "module": None,
    "label": "LABEL2",
    "type": {"value": "1000base-x-sfp", "label": "SFP (1GE)"},
    "enabled": True,
    "parent": None,
    "bridge": None,
    "lag": None,
    "mtu": 1500,
    "mac_address": "00:00:00:00:00:02",
    "speed": 1000000,
    "duplex": {"value": "auto", "label": "Auto"},
    "wwn": None,
    "mgmt_only": True,
    "description": "DESCRIPTION2",
    "mode": {"value": "tagged", "label": "Tagged"},
    "rf_role": None,
    "rf_channel": None,
    "poe_mode": None,
    "poe_type": None,
    "rf_channel_frequency": None,
    "rf_channel_width": None,
    "tx_power": 1,
    "untagged_vlan": None,
    "tagged_vlans": [],
    "mark_connected": True,
    "cable": None,
    "cable_end": "",
    "link_peers_type": None,
    "link_peers": [],
    "connected_endpoints": None,
    "connected_endpoints_type": None,
    "connected_endpoints_reachable": None,
    "wireless_link": None,
    "wireless_lans": [],
    "vrf": None,
    "l2vpn_termination": None,
    "custom_fields": {},
    "count_ipaddresses": 0,
}
INTERFACES_ = [D1_INTERFACE1_D, D1_INTERFACE2_D, D2_INTERFACE1_D, D3_INTERFACE1_D, D4_INTERFACE1_D]
INTERFACES = {d["id"]: d for d in INTERFACES_}

LOCATION1_D: DAny = {
    "id": 1,
    "url": "/api/dcim/locations/1/",
    "name": "LOCATION1",
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "site": {"id": S1, "url": f"/api/dcim/sites/{S1}/", "name": RIX1, "slug": RIX1_},
    "parent": None,
    "slug": "location1",
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
}
LOCATIONS = {d["id"]: d for d in [LOCATION1_D]}

RACK_ROLE1_D: DAny = {
    "id": 1,
    "url": "/api/dcim/rack-roles/1/",
    "name": "RACK ROLE1",
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "slug": "rack-role1",
}
RACK_ROLES = {d["id"]: d for d in [RACK_ROLE1_D]}

RACK1_D: DAny = {
    "id": 1,
    "url": "/api/dcim/racks/1/",
    "name": "RACK1",
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "site": {"id": S1, "url": f"/api/dcim/sites/{S1}/", "name": RIX1, "slug": RIX1_},
    "location": {"id": 1, "url": "/api/dcim/locations/1/", "name": "LOCATION1"},
    "role": {"id": 1, "url": "/api/dcim/rack-roles/1/", "name": "RACK ROLE1"},
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
    "tenant_group": {"id": 1, "url": "/api/tenancy/tenant-groups/1/", "name": "TENANT GROUP1"},
}
RACKS = {d["id"]: d for d in [RACK1_D]}

REGION1_D: DAny = {
    "id": 1,
    "url": "/api/dcim/regions/1/",
    "name": "REGION1",
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "parent": None,
    "slug": "region1",
}
REGIONS = {d["id"]: d for d in [REGION1_D]}

SITE_GROUP1_D: DAny = {
    "id": 1,
    "url": "/api/dcim/site-groups/1/",
    "name": "SITE GROUP1",
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "parent": None,
    "slug": "site-group1",
}
SITE_GROUPS = {d["id"]: d for d in [SITE_GROUP1_D]}

SITE1_D: DAny = {
    "id": S1,
    "url": f"/api/dcim/sites/{S1}/",
    "name": RIX1,
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "group": {"id": 1, "url": "/api/dcim/site-groups/1/", "name": "SITE GROUP1"},
    "region": {"id": 1, "url": "/api/dcim/regions/1/", "name": "REGION1"},
    "slug": "site1",
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
    "asns": {"id": 1, "url": "/api/ipam/asns/1/", "asn": 65001},
}
SITE2_D: DAny = {
    "id": S2,
    "url": f"/api/dcim/sites/{S2}/",
    "name": RIX2,
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "group": {"id": 1, "url": "/api/dcim/site-groups/1/", "name": "SITE GROUP1"},
    "region": {"id": 1, "url": "/api/dcim/regions/1/", "name": "REGION1"},
    "slug": "site2",
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
    "asns": {"id": 1, "url": "/api/ipam/asns/1/", "asn": 65001},
}
SITES = {d["id"]: d for d in [SITE1_D, SITE2_D]}

# extras
TAG1_D: DAny = {
    "id": 1,
    "url": "/api/extras/tags/1/",
    "name": TAG1,
    "slug": "tag1",
    "color": "aa1409",
}
TAG3_D: DAny = {
    "id": 3,
    "url": "/api/extras/tags/3/",
    "name": TAG3,
    "slug": "tag3",
    "color": "aa1409",
}
TAGS = {d["id"]: d for d in [TAG1_D, TAG3_D]}

# ipam
AGGREGATE1_D: DAny = {
    "id": AG1,
    "url": f"/api/ipam/aggregates/{AG1}/",
    "prefix": AGGREGATE1,
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "family": {"value": 4},
    "rir": {"id": 1, "url": "/api/ipam/rirs/1/", "name": "RFC 1918"},
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
}
AGGREGATE2_D: DAny = {
    "id": AG2,
    "url": f"/api/ipam/aggregates/{AG2}/",
    "prefix": AGGREGATE2,
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "family": {"value": 4},
    "rir": {"id": 1, "url": "/api/ipam/rirs/1/", "name": "RFC 1918"},
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
}
AGGREGATES = {d["id"]: d for d in [AGGREGATE1_D, AGGREGATE2_D]}

ASN_RANGE1_D: DAny = {
    "id": 1,
    "url": "/api/ipam/asn-ranges/1/",
    "name": "ASN RANGE1",
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "slug": "asn-range1",
    "rir": {"id": 2, "url": "/api/ipam/rirs/2/", "name": "RFC 6996"},
    "start": 65001,
    "end": 65002,
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
}
ASN_RANGES = {d["id"]: d for d in [ASN_RANGE1_D]}

ASN1_D: DAny = {
    "id": 1,
    "url": "/api/ipam/asns/1/",
    "asn": 65001,
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "rir": {"id": 2, "url": "/api/ipam/rirs/2/", "name": "RFC 6996"},
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
}
ASN2_D: DAny = {
    "id": 2,
    "url": "/api/ipam/asns/2/",
    "asn": 65002,
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "rir": {"id": 2, "url": "/api/ipam/rirs/2/", "name": "RFC 6996"},
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
}
ASNS = {d["id"]: d for d in [ASN1_D, ASN2_D]}

# global private
IP_ADDRESS1_D: DAny = {
    "id": A1,
    "url": f"/api/ipam/ip-addresses/{A1}/",
    "address": ADDRESS1,
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "family": {"value": 4},
    "status": {"value": "active"},
    "nat_inside": None,
    "nat_outside": [{"id": A2, "address": ADDRESS2}],
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
    "vrf": None,
    "role": {"label": "Loopback", "value": "loopback"},
    "assigned_object_type": "dcim.interface",
    "assigned_object_id": D1P1,
    "assigned_object": {
        "id": D1P1,
        "url": f"/api/dcim/interfaces/{D1P1}/",
        "name": ETHERNET11,
        "cable": 1,
        "device": {"id": D1, "url": f"/api/dcim/devices/{D1}/", "name": HOSTNAME1},
    },
}
# global public
IP_ADDRESS2_D: DAny = {
    "id": A2,
    "url": f"/api/ipam/ip-addresses/{A2}/",
    "address": ADDRESS2,
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "family": {"value": 4},
    "status": {"value": "active"},
    "nat_inside": {"id": A2, "address": ADDRESS2, "url": "/api/ipam/ip-addresses/1/"},
    "nat_outside": [],
    "tenant": None,
    "vrf": None,
    "role": {"label": "Secondary", "value": "secondary"},
    "assigned_object_type": "dcim.interface",
    "assigned_object_id": None,
    "assigned_object": None,
}
# vrf private
IP_ADDRESS3_D: DAny = {
    "id": A3,
    "url": f"/api/ipam/ip-addresses/{A3}/",
    "address": ADDRESS3,
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "family": {"value": 4},
    "status": {"value": "active"},
    "nat_inside": None,
    "nat_outside": [],
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
    "vrf": {"id": 1, "url": "/api/ipam/vrfs/1/", "name": "VRF1"},
    "role": None,
    "assigned_object_type": "dcim.interface",
    "assigned_object_id": D2P1,
    "assigned_object": {
        "id": D2P1,
        "url": f"/api/dcim/interfaces/{D2P1}/",
        "name": ETHERNET12,
        "cable": 1,
        "device": {"id": D1, "url": f"/api/dcim/devices/{D1}/", "name": HOSTNAME1},
    },
}
# global private, vm
IP_ADDRESS4_D: DAny = {
    "id": A4,
    "url": f"/api/ipam/ip-addresses/{A4}/",
    "address": ADDRESS4,
    "tags": [],
    "family": {"value": 4},
    "status": {"value": "active"},
    "nat_inside": None,
    "nat_outside": [],
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
    "vrf": {"id": 1, "url": "/api/ipam/vrfs/1/", "name": "VRF1"},
    "role": None,
    "assigned_object_type": "virtualization.vminterface",
    "assigned_object_id": 1,
    "assigned_object": {
        "id": D5P1,
        "url": f"/api/virtualization/interfaces/{D5P1}/",
        "name": VIRTUAL_ETH1,
        "virtual_machine": {"id": D5, "url": f"/api/dcim/devices/{D5}/", "name": HOSTNAME5},
    },
}
IP_ADDRESSES = {d["id"]: d for d in [IP_ADDRESS1_D, IP_ADDRESS2_D, IP_ADDRESS3_D, IP_ADDRESS4_D]}

# global private
PREFIX1_D: DAny = {
    "id": P1,
    "url": f"/api/ipam/prefixes/{P1}/",
    "prefix": PREFIX1,  # 10.0.0.0/24
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "family": {"value": 4},
    "status": {"value": "active"},
    "role": {"id": R1, "url": f"/api/ipam/roles/{R1}/", "name": ROLE1, "slug": ROLE1_},
    "site": {"id": S1, "url": f"/api/dcim/sites/{S1}/", "name": RIX1, "slug": RIX1_},
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
    "vlan": {"id": 1, "url": "/api/ipam/vlans/1/", "vid": 1, "name": "VLAN1"},
    "vrf": None,
    "custom_fields": {"env": "ENV1"},
    "_depth": 0,
}
# global public
PREFIX2_D: DAny = {
    "id": P2,
    "url": f"/api/ipam/prefixes/{P2}/",
    "prefix": PREFIX2,  # 1.0.0.0/24
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "family": {"value": 4},
    "status": {"value": "active"},
    "role": None,
    "site": None,
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
    "vlan": {"id": 1, "url": "/api/ipam/vlans/1/", "vid": 1, "name": "VLAN1"},
    "vrf": None,
    "custom_fields": {},
    "_depth": 0,
}
# vrf
PREFIX3_D: DAny = {
    "id": P3,
    "url": f"/api/ipam/prefixes/{P3}/",
    "prefix": PREFIX1,  # 10.0.0.0/24
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "family": {"value": 4},
    "status": {"value": "active"},
    "role": {"id": R3, "url": f"/api/ipam/roles/{R3}/", "name": ROLE3, "slug": ROLE3_},
    "site": {"id": S3, "url": f"/api/dcim/sites/{S3}/", "name": RIX3, "slug": RIX3_},
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
    "vlan": {"id": 1, "url": "/api/ipam/vlans/1/", "vid": 1, "name": "VLAN1"},
    "vrf": {"id": 1, "url": "/api/ipam/vrfs/1/", "name": "VRF1"},
    "custom_fields": {"env": "ENV3"},
    "_depth": 0,
}
# global private sub_prefix
PREFIX4_D: DAny = {
    "id": P4,
    "url": f"/api/ipam/prefixes/{P4}/",
    "prefix": PREFIX4,  # 10.0.0.0/31
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "family": {"value": 4},
    "status": {"value": "active"},
    "role": {"id": R1, "url": f"/api/ipam/roles/{R1}/", "name": ROLE1, "slug": ROLE1_},
    "site": {"id": S2, "url": f"/api/dcim/sites/{S2}/", "name": RIX2, "slug": RIX2_},
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
    "vlan": {"id": 1, "url": "/api/ipam/vlans/1/", "vid": 1, "name": "VLAN1"},
    "vrf": None,
    "custom_fields": {"env": "ENV1"},
    "_depth": 1,
}
# global private sub_prefix
PREFIX5_D: DAny = {
    "id": P5,
    "url": f"/api/ipam/prefixes/{P5}/",
    "prefix": PREFIX5,  # 10.0.0.0/32
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "family": {"value": 4},
    "status": {"value": "active"},
    "role": {"id": R2, "url": f"/api/ipam/roles/{R2}/", "name": ROLE2, "slug": ROLE2_},
    "site": {"id": S2, "url": f"/api/dcim/sites/{S2}/", "name": RIX2, "slug": RIX2_},
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
    "vlan": {"id": 1, "url": "/api/ipam/vlans/1/", "vid": 1, "name": "VLAN1"},
    "vrf": None,
    "custom_fields": {"env": "ENV2"},
    "_depth": 2,
}
PREFIXES = {d["id"]: d for d in [PREFIX1_D, PREFIX2_D, PREFIX3_D, PREFIX4_D, PREFIX5_D]}

RIR1_D: DAny = {
    "id": 1,
    "url": "/api/ipam/rirs/1/",
    "name": "RFC 1918",
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "slug": "rfc-1918",
}
RIR2_D: DAny = {
    "id": 2,
    "url": "/api/ipam/rirs/2/",
    "name": "RFC 6996",
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "slug": "rfc-6996",
}
RIRS = {d["id"]: d for d in [RIR1_D, RIR2_D]}

ROLE1_D: DAny = {
    "id": R1,
    "url": f"/api/ipam/roles/{R1}/",
    "name": ROLE1,
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "slug": ROLE1_,
}
ROLE2_D: DAny = {
    "id": R2,
    "url": f"/api/ipam/roles/{R2}/",
    "name": ROLE2,
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "slug": ROLE2_,
}
ROLE3_D: DAny = {
    "id": R3,
    "url": f"/api/ipam/roles/{R3}/",
    "name": ROLE3,
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "slug": ROLE3_,
}
ROLES = {d["id"]: d for d in [ROLE1_D, ROLE2_D, ROLE3_D]}

ROUTE_TARGET1_D: DAny = {
    "id": 1,
    "url": "/api/ipam/route-targets/1/",
    "name": "65000:1",
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
}
ROUTE_TARGETS = {d["id"]: d for d in [ROUTE_TARGET1_D]}

VLAN_GROUP1_D: DAny = {
    "id": 1,
    "url": "/api/ipam/vlan-groups/1/",
    "name": "VLAN GROUP1",
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "slug": "vlan-group1",
    "scope_type": "dcim.site",
    "scope_id": 1,
    "scope": {"id": S1, "url": f"/api/dcim/sites/{S1}/", "name": RIX1, "slug": RIX1_},
    "min_vid": 1,
    "max_vid": 4094,
}
VLAN_GROUPS = {d["id"]: d for d in [VLAN_GROUP1_D]}

VLAN1_D: DAny = {
    "id": 1,
    "url": "/api/ipam/vlans/1/",
    "vid": 1,
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "site": None,  # mutually exclusive: group, site
    "group": {"id": 1, "url": "/api/ipam/vlan-groups/1/", "name": "VLAN GROUP1"},
    "role": {"id": R1, "url": f"/api/ipam/roles/{R1}/", "name": ROLE1, "slug": ROLE1_},
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
}
VLAN2_D: DAny = {
    "id": 2,
    "url": "/api/ipam/vlans/2/",
    "vid": 2,
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "site": {"id": S1, "url": f"/api/dcim/sites/{S1}/", "name": RIX1, "slug": RIX1_},
    "group": None,  # mutually exclusive: group, site
    "role": {"id": R1, "url": f"/api/ipam/roles/{R1}/", "name": ROLE1, "slug": ROLE1_},
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
}
VLANS = {d["id"]: d for d in [VLAN1_D, VLAN2_D]}

VRF1_D: DAny = {
    "id": 1,
    "url": "/api/ipam/vrfs/1/",
    "name": "VRF1",
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
    "import_targets": [{"id": 1, "name": "65000:1"}],
    "export_targets": [{"id": 1, "name": "65000:1"}],
}
VRFS = {d["id"]: d for d in [VRF1_D]}

# tenancy
TNG = 1
TENANT_GROUP1 = "TENANT GROUP1"
TENANT_GROUP1_ = "tenant-group1"
TENANT_GROUP1_D: DAny = {
    "id": TNG,
    "url": f"/api/tenancy/tenant-groups/{TNG}/",
    "name": TENANT_GROUP1,
    "slug": TENANT_GROUP1_,
    "parent": None,
}
TENANT_GROUPS = {d["id"]: d for d in [TENANT_GROUP1_D]}

TENANT1_D: DAny = {
    "id": TN1,
    "url": f"/api/tenancy/tenants/{TN1}/",
    "name": TENANT1,
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "slug": TENANT1_,
    "group": {"id": TNG, "url": f"/api/tenancy/tenant-groups/{TNG}/", "name": TENANT_GROUP1},
}
TENANTS = {d["id"]: d for d in [TENANT1_D]}

# virtualization
CLUSTER_GROUP1_D: DAny = {
    "id": 1,
    "url": "/api/virtualization/cluster-groups/1/",
    "name": "CLUSTER GROUP1",
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "slug": "cluster-group1",
}
CLUSTER_GROUPS = {d["id"]: d for d in [CLUSTER_GROUP1_D]}

CLUSTER_TYPE1_D: DAny = {
    "id": 1,
    "url": "/api/virtualization/cluster-types/1/",
    "name": "CLUSTER TYPE1",
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "slug": "cluster-type1",
}
CLUSTER_TYPES = {d["id"]: d for d in [CLUSTER_TYPE1_D]}

CLUSTER1_D: DAny = {
    "id": 1,
    "url": "/api/virtualization/clusters/1/",
    "name": "CLUSTER1",
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "slug": "cluster1",
    "type": {"id": 1, "url": "/api/virtualization/cluster-types/1/", "name": "CLUSTER TYPE1"},
    "group": {"id": 1, "url": "/api/virtualization/cluster-groups/1/", "name": "CLUSTER GROUP1"},
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
    "site": {"id": S1, "url": f"/api/dcim/sites/{S1}/", "name": RIX1, "slug": RIX1_},
}
CLUSTERS = {d["id"]: d for d in [CLUSTER1_D]}

VIRTUAL_INTERFACE1_D: DAny = {
    "id": D5P1,
    "url": f"/api/virtualization/interfaces/{D5P1}/",
    "name": "VIRTUAL_INTERFACE1",
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "virtual_machine": {
        "id": D5,
        "url": f"/api/virtualization/virtual-machines/{D5}/",
        "name": "VIRTUAL MACHINE1",
    },
    "enabled": True,
    "parent": {"id": 1, "url": "/api/virtualization/interfaces/1/", "name": "INTERFACE1"},
    "bridge": {"id": 1, "url": "/api/virtualization/interfaces/1/", "name": "INTERFACE1"},
    "mtu": 1500,
    "mac_address": "00:00:00:00:00:01",
    "description": "DESCRIPTION1",
    "mode": {"value": "tagged", "label": "Tagged"},
    "untagged_vlan": {"id": 1, "url": "/api/ipam/vlans/1/", "vid": 1, "name": "VLAN1"},
    "tagged_vlans": [{"id": 2, "url": "/api/ipam/vlans/2/", "vid": 2, "name": "VLAN2"}],
    "vrf": {"id": 1, "url": "/api/ipam/vrfs/1/", "name": "VRF1"},
    "l2vpn_termination": None,
    "custom_fields": {},
}
VIRTUAL_INTERFACES = {d["id"]: d for d in [VIRTUAL_INTERFACE1_D]}
VIRTUAL_MACHINE1_D: DAny = {
    "id": D5,
    "url": f"/api/virtualization/virtual-machines/{D5}/",
    "name": "VIRTUAL MACHINE1",
    "tags": [{"id": T1, "url": f"/api/extras/tags/{T1}/", "name": TAG1}],
    "site": {"id": S1, "url": f"/api/dcim/sites/{S1}/", "name": RIX1, "slug": RIX1_},
    "cluster": {"id": 1, "url": "/api/virtualization/clusters/1/", "name": "CLUSTER1"},
    "device": {"id": D1, "url": f"/api/dcim/devices/{D1}/", "name": HOSTNAME1},
    "role": {"id": 1, "url": "/api/dcim/device-roles/1/", "name": "DEVICE ROLE1"},
    "tenant": {"id": TN1, "url": f"/api/tenancy/tenants/{TN1}/", "name": TENANT1},
    "platform": {"id": 1, "url": "/api/dcim/platforms/1/", "name": "PLATFORM1"},
}
VIRTUAL_MACHINES = {d["id"]: d for d in [VIRTUAL_MACHINE1_D]}
