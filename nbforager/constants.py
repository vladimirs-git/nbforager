"""Constants for apps and models."""

from nbforager.types_ import DLStr

APPS = (
    "circuits",
    "core",
    "dcim",
    "extras",
    "ipam",
    "plugins",
    "tenancy",
    "users",
    "virtualization",
    "wireless",
)
"""Application names for NetBox v3.5."""

DEPENDENT_MODELS: DLStr = {
    "circuits/circuit-terminations": [
        "circuits/circuits",
        "circuits/provider-networks",
        "dcim/cable-terminations",
        "dcim/sites",
        "extras/tags",
    ],
    "circuits/circuit-types": ["extras/tags"],
    "circuits/circuits": [
        "circuits/circuit-types",
        "circuits/provider-accounts",
        "circuits/providers",
        "extras/tags",
        "tenancy/tenants",
    ],
    "circuits/provider-accounts": ["circuits/providers", "extras/tags"],
    "circuits/provider-networks": ["circuits/providers", "extras/tags"],
    "circuits/providers": ["extras/tags", "ipam/asns"],
    "core/data-files": ["core/data-sources"],
    "core/data-sources": ["extras/tags"],
    "core/jobs": ["extras/content-types"],
    "dcim/cable-terminations": [
        "dcim/cables",
        "dcim/devices",
        "dcim/locations",
        "dcim/racks",
        "dcim/sites",
    ],
    "dcim/cables": ["extras/tags", "tenancy/tenants"],
    "dcim/console-port-templates": ["dcim/device-types", "dcim/module-types"],
    "dcim/console-ports": [
        "dcim/cable-terminations",
        "dcim/devices",
        "dcim/modules",
        "extras/tags",
    ],
    "dcim/console-server-port-templates": ["dcim/device-types", "dcim/module-types"],
    "dcim/console-server-ports": [
        "dcim/cable-terminations",
        "dcim/devices",
        "dcim/modules",
        "extras/tags",
    ],
    "dcim/device-bay-templates": ["dcim/device-types"],
    "dcim/device-bays": ["dcim/devices", "extras/tags"],
    "dcim/device-roles": ["extras/config-templates", "extras/tags"],
    "dcim/device-types": ["dcim/manufacturers", "extras/tags"],
    "dcim/devices": [
        "dcim/device-roles",
        "dcim/device-types",
        "dcim/locations",
        "dcim/platforms",
        "dcim/racks",
        "dcim/sites",
        "dcim/virtual-chassis",
        "extras/config-templates",
        "extras/tags",
        "tenancy/tenants",
        "virtualization/clusters",
    ],
    "dcim/front-port-templates": [
        "dcim/device-types",
        "dcim/module-types",
        "dcim/rear-port-templates",
    ],
    "dcim/front-ports": [
        "dcim/cable-terminations",
        "dcim/devices",
        "dcim/modules",
        "dcim/rear-ports",
        "extras/tags",
    ],
    "dcim/interface-templates": ["dcim/device-types", "dcim/module-types"],
    "dcim/interfaces": [
        "dcim/cable-terminations",
        "dcim/devices",
        "dcim/modules",
        "dcim/virtual-device-contexts",
        "extras/tags",
        "ipam/ip-addresses",
        "ipam/l2vpn-terminations",
        "ipam/vlans",
        "ipam/vrfs",
        "virtualization/interfaces",
        "wireless/wireless-lans",
    ],
    "dcim/inventory-item-roles": ["extras/tags"],
    "dcim/inventory-item-templates": [
        "dcim/device-types",
        "dcim/inventory-item-roles",
        "dcim/manufacturers",
    ],
    "dcim/inventory-items": [
        "dcim/devices",
        "dcim/inventory-item-roles",
        "dcim/manufacturers",
        "extras/tags",
    ],
    "dcim/locations": ["dcim/sites", "extras/tags", "ipam/vlan-groups", "tenancy/tenants"],
    "dcim/manufacturers": ["extras/tags"],
    "dcim/module-bay-templates": ["dcim/device-types"],
    "dcim/module-bays": ["dcim/devices", "extras/tags"],
    "dcim/module-types": ["dcim/manufacturers", "extras/tags"],
    "dcim/modules": ["dcim/devices", "dcim/module-bays", "dcim/module-types", "extras/tags"],
    "dcim/platforms": ["dcim/manufacturers", "extras/config-templates", "extras/tags"],
    "dcim/power-feeds": [
        "dcim/cable-terminations",
        "dcim/power-panels",
        "dcim/racks",
        "extras/tags",
    ],
    "dcim/power-outlet-templates": [
        "dcim/device-types",
        "dcim/module-types",
        "dcim/power-port-templates",
    ],
    "dcim/power-outlets": [
        "dcim/cable-terminations",
        "dcim/devices",
        "dcim/modules",
        "dcim/power-ports",
        "extras/tags",
    ],
    "dcim/power-panels": ["dcim/locations", "dcim/sites", "extras/tags"],
    "dcim/power-port-templates": ["dcim/device-types", "dcim/module-types"],
    "dcim/power-ports": ["dcim/cable-terminations", "dcim/devices", "dcim/modules", "extras/tags"],
    "dcim/rack-reservations": ["dcim/racks", "extras/tags", "tenancy/tenants", "users/users"],
    "dcim/rack-roles": ["extras/tags"],
    "dcim/racks": [
        "dcim/locations",
        "dcim/rack-roles",
        "dcim/sites",
        "extras/tags",
        "ipam/vlan-groups",
        "tenancy/tenants",
    ],
    "dcim/rear-port-templates": ["dcim/device-types", "dcim/module-types"],
    "dcim/rear-ports": ["dcim/cable-terminations", "dcim/devices", "dcim/modules", "extras/tags"],
    "dcim/regions": ["extras/tags", "ipam/vlan-groups"],
    "dcim/site-groups": ["extras/tags", "ipam/vlan-groups"],
    "dcim/sites": [
        "dcim/regions",
        "dcim/site-groups",
        "extras/tags",
        "ipam/asns",
        "ipam/vlan-groups",
        "tenancy/tenants",
    ],
    "dcim/virtual-chassis": ["dcim/devices", "extras/tags"],
    "dcim/virtual-device-contexts": ["dcim/devices", "extras/tags", "tenancy/tenants"],
    "extras/config-contexts": [
        "dcim/device-roles",
        "dcim/device-types",
        "dcim/locations",
        "dcim/platforms",
        "dcim/regions",
        "dcim/site-groups",
        "dcim/sites",
        "extras/tags",
        "tenancy/tenant-groups",
        "tenancy/tenants",
        "virtualization/cluster-groups",
        "virtualization/cluster-types",
        "virtualization/clusters",
    ],
    "extras/config-templates": ["extras/tags"],
    "extras/content-types": [],
    "extras/custom-fields": ["extras/content-types"],
    "extras/custom-links": ["extras/content-types"],
    "extras/export-templates": ["extras/content-types"],
    "extras/image-attachments": ["extras/content-types"],
    "extras/journal-entries": ["extras/content-types", "extras/tags", "users/users"],
    "extras/object-changes": ["users/users"],
    "extras/saved-filters": ["extras/content-types", "users/users"],
    "extras/tags": [],
    "extras/webhooks": ["extras/content-types"],
    "ipam/aggregates": ["extras/tags", "ipam/rirs", "tenancy/tenants"],
    "ipam/asn-ranges": ["extras/tags", "ipam/rirs", "tenancy/tenants"],
    "ipam/asns": ["extras/tags", "ipam/rirs", "tenancy/tenants"],
    "ipam/fhrp-group-assignments": ["extras/content-types", "ipam/fhrp-groups"],
    "ipam/fhrp-groups": ["extras/tags", "ipam/ip-addresses"],
    "ipam/ip-addresses": ["extras/tags", "ipam/vrfs", "tenancy/tenants"],
    "ipam/ip-ranges": ["extras/tags", "ipam/roles", "ipam/vrfs", "tenancy/tenants"],
    "ipam/l2vpn-terminations": ["extras/tags", "ipam/l2vpns"],
    "ipam/l2vpns": ["extras/tags", "ipam/route-targets", "tenancy/tenants"],
    "ipam/prefixes": [
        "dcim/sites",
        "extras/tags",
        "ipam/roles",
        "ipam/vlans",
        "ipam/vrfs",
        "tenancy/tenants",
    ],
    "ipam/rirs": ["extras/tags"],
    "ipam/roles": ["extras/tags"],
    "ipam/route-targets": ["extras/tags", "tenancy/tenants"],
    "ipam/service-templates": ["extras/tags"],
    "ipam/services": [
        "dcim/devices",
        "extras/tags",
        "ipam/ip-addresses",
        "virtualization/virtual-machines",
    ],
    "ipam/vlan-groups": ["extras/content-types", "extras/tags"],
    "ipam/vlans": [
        "dcim/sites",
        "extras/tags",
        "ipam/l2vpn-terminations",
        "ipam/roles",
        "ipam/vlan-groups",
        "tenancy/tenants",
    ],
    "ipam/vrfs": ["extras/tags", "ipam/route-targets", "tenancy/tenants"],
    "tenancy/contact-assignments": [
        "extras/content-types",
        "tenancy/contact-roles",
        "tenancy/contacts",
    ],
    "tenancy/contact-groups": ["extras/tags"],
    "tenancy/contact-roles": ["extras/tags"],
    "tenancy/contacts": ["extras/tags", "tenancy/contact-groups"],
    "tenancy/tenant-groups": ["extras/tags"],
    "tenancy/tenants": ["extras/tags", "tenancy/tenant-groups"],
    "users/groups": [],
    "users/permissions": ["extras/content-types", "users/groups", "users/users"],
    "users/tokens": ["users/users"],
    "users/users": [],
    "virtualization/cluster-groups": ["extras/tags", "ipam/vlan-groups"],
    "virtualization/cluster-types": ["extras/tags"],
    "virtualization/clusters": [
        "dcim/sites",
        "extras/tags",
        "ipam/vlan-groups",
        "tenancy/tenants",
        "virtualization/cluster-groups",
        "virtualization/cluster-types",
    ],
    "virtualization/interfaces": [
        "extras/tags",
        "ipam/ip-addresses",
        "ipam/l2vpn-terminations",
        "ipam/vlans",
        "ipam/vrfs",
        "virtualization/virtual-machines",
    ],
    "virtualization/virtual-machines": [
        "dcim/device-roles",
        "dcim/devices",
        "dcim/platforms",
        "dcim/sites",
        "extras/tags",
        "tenancy/tenants",
        "virtualization/clusters",
    ],
    "wireless/wireless-lan-groups": ["extras/tags"],
    "wireless/wireless-lans": [
        "extras/tags",
        "ipam/vlans",
        "tenancy/tenants",
        "wireless/wireless-lan-groups",
    ],
    "wireless/wireless-links": ["extras/tags", "tenancy/tenants"],
}
"""Models dependency for Netbox v3.5."""
