"""Print paths and models  dependency mapping for Netbox v3.5

Used in `python3 /opt/netbox/netbox/manage.py shell` to create helpers.dependency_paths()
"""

from pprint import pprint

from circuits.models import (
    CircuitTermination,
    CircuitType,
    Circuit,
    ProviderAccount,
    ProviderNetwork,
    Provider
)
from core.models import (
    DataFile,
    DataSource,
    Job
)
from dcim.models import (
    CableTermination,
    Cable,
    # ConnectedDevice,
    ConsolePortTemplate,
    ConsolePort,
    ConsoleServerPortTemplate,
    ConsoleServerPort,
    DeviceBayTemplate,
    DeviceBay,
    DeviceRole,
    DeviceType,
    Device,
    FrontPortTemplate,
    FrontPort,
    InterfaceTemplate,
    Interface,
    InventoryItemRole,
    InventoryItemTemplate,
    InventoryItem,
    Location,
    Manufacturer,
    ModuleBayTemplate,
    ModuleBay,
    ModuleType,
    Module,
    Platform,
    PowerFeed,
    PowerOutletTemplate,
    PowerOutlet,
    PowerPanel,
    PowerPortTemplate,
    PowerPort,
    RackReservation,
    RackRole,
    Rack,
    RearPortTemplate,
    RearPort,
    Region,
    SiteGroup,
    Site,
    VirtualChassis,
    VirtualDeviceContext
)
from extras.models import (
    Tag,
    ConfigContext,
    ConfigTemplate,
    ContentType,
    # CustomFieldChoiceSet,
    CustomField,
    CustomLink,
    # ExportTemplate,
    # ImageAttachment,
    # JournalEntry,
    # ObjectChange,
    # Report,
    # SavedFilter,
    # Script,
    # Webhook,
)
from ipam.models import (
    Aggregate,
    ASNRange,
    ASN,
    FHRPGroupAssignment,
    FHRPGroup,
    IPAddress,
    IPRange,
    L2VPNTermination,
    L2VPN,
    Prefix,
    RIR,
    Role,
    RouteTarget,
    ServiceTemplate,
    Service,
    VLANGroup,
    VLAN,
    VRF
)
# from plugins.models import InstalledPlugin
from tenancy.models import (
    Tenant,
    TenantGroup,
    ContactAssignment,
    ContactGroup,
    ContactRole,
    Contact
)
from users.models import (
    # Config,
    Group,
    # Permission,
    Token,
    User,
)
from virtualization.models import (
    ClusterGroup,
    ClusterType,
    Cluster,
    # Interface,
    VirtualMachine
)
from wireless.models import (
    WirelessLANGroup,
    WirelessLAN,
    WirelessLink
)

# NetBox app/model paths
model_names = [
    "circuits/circuit-terminations",
    "circuits/circuit-types",
    "circuits/circuits",
    "circuits/provider-accounts",
    "circuits/provider-networks",
    "circuits/providers",
    "core/data-files",
    "core/data-sources",
    "core/jobs",
    "dcim/cable-terminations",
    "dcim/cables",
    "dcim/connected-device",
    "dcim/console-port-templates",
    "dcim/console-ports",
    "dcim/console-server-port-templates",
    "dcim/console-server-ports",
    "dcim/device-bay-templates",
    "dcim/device-bays",
    "dcim/device-roles",
    "dcim/device-types",
    "dcim/devices",
    "dcim/front-port-templates",
    "dcim/front-ports",
    "dcim/interface-templates",
    "dcim/interfaces",
    "dcim/inventory-item-roles",
    "dcim/inventory-item-templates",
    "dcim/inventory-items",
    "dcim/locations",
    "dcim/manufacturers",
    "dcim/module-bay-templates",
    "dcim/module-bays",
    "dcim/module-types",
    "dcim/modules",
    "dcim/platforms",
    "dcim/power-feeds",
    "dcim/power-outlet-templates",
    "dcim/power-outlets",
    "dcim/power-panels",
    "dcim/power-port-templates",
    "dcim/power-ports",
    "dcim/rack-reservations",
    "dcim/rack-roles",
    "dcim/racks",
    "dcim/rear-port-templates",
    "dcim/rear-ports",
    "dcim/regions",
    "dcim/site-groups",
    "dcim/sites",
    "dcim/virtual-chassis",
    "dcim/virtual-device-contexts",
    "extras/bookmarks",
    "extras/config-contexts",
    "extras/config-templates",
    "extras/content-types",
    "extras/custom-field-choice-sets",
    "extras/custom-fields",
    "extras/custom-links",
    "extras/export-templates",
    "extras/image-attachments",
    "extras/journal-entries",
    "extras/object-changes",
    "extras/reports",
    "extras/saved-filters",
    "extras/scripts",
    "extras/tags",
    "extras/webhooks",
    "ipam/aggregates",
    "ipam/asn-ranges",
    "ipam/asns",
    "ipam/fhrp-group-assignments",
    "ipam/fhrp-groups",
    "ipam/ip-addresses",
    "ipam/ip-ranges",
    "ipam/l2vpn-terminations",
    "ipam/l2vpns",
    "ipam/prefixes",
    "ipam/rirs",
    "ipam/roles",
    "ipam/route-targets",
    "ipam/service-templates",
    "ipam/services",
    "ipam/vlan-groups",
    "ipam/vlans",
    "ipam/vrfs",
    "plugins/installed-plugins",
    "tenancy/contact-assignments",
    "tenancy/contact-groups",
    "tenancy/contact-roles",
    "tenancy/contacts",
    "tenancy/tenant-groups",
    "tenancy/tenants",
    "users/config",
    "users/groups",
    "users/permissions",
    "users/tokens",
    "users/users",
    "virtualization/cluster-groups",
    "virtualization/cluster-types",
    "virtualization/clusters",
    "virtualization/interfaces",
    "virtualization/virtual-machines",
    "wireless/wireless-lan-groups",
    "wireless/wireless-lans",
    "wireless/wireless-links",
]

# NetBox models mapping v3.5
models_map = {
    # tenancy
    "tenancy/tenants": Tenant,
    "tenancy/tenant-groups": TenantGroup,
    "tenancy/contact-assignments": ContactAssignment,
    "tenancy/contact-groups": ContactGroup,
    "tenancy/contact-roles": ContactRole,
    "tenancy/contacts": Contact,

    # extras
    "extras/tags": Tag,
    # "extras/bookmarks": Bookmark,
    "extras/config-contexts": ConfigContext,
    "extras/config-templates": ConfigTemplate,
    "extras/content-types": ContentType,
    # "extras/custom-field-choice-sets": CustomFieldChoiceSet,
    "extras/custom-fields": CustomField,
    "extras/custom-links": CustomLink,
    # "extras/export-templates": ExportTemplate,
    # "extras/image-attachments": ImageAttachment,
    # "extras/journal-entries": JournalEntry,
    # "extras/object-changes": ObjectChange,
    # "extras/reports": Report,
    # "extras/saved-filters": SavedFilter,
    # "extras/scripts": Script,
    # "extras/webhooks": Webhook,

    # circuits
    "circuits/circuit-terminations": CircuitTermination,
    "circuits/circuit-types": CircuitType,
    "circuits/circuits": Circuit,
    "circuits/provider-accounts": ProviderAccount,
    "circuits/provider-networks": ProviderNetwork,
    "circuits/providers": Provider,

    # core
    "core/data-files": DataFile,
    "core/data-sources": DataSource,
    "core/jobs": Job,

    # dcim
    "dcim/cable-terminations": CableTermination,
    "dcim/cables": Cable,
    # "dcim/connected-device": ConnectedDevice,
    "dcim/console-port-templates": ConsolePortTemplate,
    "dcim/console-ports": ConsolePort,
    "dcim/console-server-port-templates": ConsoleServerPortTemplate,
    "dcim/console-server-ports": ConsoleServerPort,
    "dcim/device-bay-templates": DeviceBayTemplate,
    "dcim/device-bays": DeviceBay,
    "dcim/device-roles": DeviceRole,
    "dcim/device-types": DeviceType,
    "dcim/devices": Device,
    "dcim/front-port-templates": FrontPortTemplate,
    "dcim/front-ports": FrontPort,
    "dcim/interface-templates": InterfaceTemplate,
    "dcim/interfaces": Interface,
    "dcim/inventory-item-roles": InventoryItemRole,
    "dcim/inventory-item-templates": InventoryItemTemplate,
    "dcim/inventory-items": InventoryItem,
    "dcim/locations": Location,
    "dcim/manufacturers": Manufacturer,
    "dcim/module-bay-templates": ModuleBayTemplate,
    "dcim/module-bays": ModuleBay,
    "dcim/module-types": ModuleType,
    "dcim/modules": Module,
    "dcim/platforms": Platform,
    "dcim/power-feeds": PowerFeed,
    "dcim/power-outlet-templates": PowerOutletTemplate,
    "dcim/power-outlets": PowerOutlet,
    "dcim/power-panels": PowerPanel,
    "dcim/power-port-templates": PowerPortTemplate,
    "dcim/power-ports": PowerPort,
    "dcim/rack-reservations": RackReservation,
    "dcim/rack-roles": RackRole,
    "dcim/racks": Rack,
    "dcim/rear-port-templates": RearPortTemplate,
    "dcim/rear-ports": RearPort,
    "dcim/regions": Region,
    "dcim/site-groups": SiteGroup,
    "dcim/sites": Site,
    "dcim/virtual-chassis": VirtualChassis,
    "dcim/virtual-device-contexts": VirtualDeviceContext,

    # ipam
    "ipam/aggregates": Aggregate,
    "ipam/asn-ranges": ASNRange,
    "ipam/asns": ASN,
    "ipam/fhrp-group-assignments": FHRPGroupAssignment,
    "ipam/fhrp-groups": FHRPGroup,
    "ipam/ip-addresses": IPAddress,
    "ipam/ip-ranges": IPRange,
    "ipam/l2vpn-terminations": L2VPNTermination,
    "ipam/l2vpns": L2VPN,
    "ipam/prefixes": Prefix,
    "ipam/rirs": RIR,
    "ipam/roles": Role,
    "ipam/route-targets": RouteTarget,
    "ipam/service-templates": ServiceTemplate,
    "ipam/services": Service,
    "ipam/vlan-groups": VLANGroup,
    "ipam/vlans": VLAN,
    "ipam/vrfs": VRF,

    # plugins
    # "plugins/installed-plugins": InstalledPlugin,

    # users
    # "users/config": Config,
    "users/groups": Group,
    # "users/permissions": Permission,
    "users/tokens": Token,
    "users/users": User,

    # virtualization
    "virtualization/cluster-groups": ClusterGroup,
    "virtualization/cluster-types": ClusterType,
    "virtualization/clusters": Cluster,
    "virtualization/interfaces": Interface,
    "virtualization/virtual-machines": VirtualMachine,

    # wireless
    "wireless/wireless-lan-groups": WirelessLANGroup,
    "wireless/wireless-lans": WirelessLAN,
    "wireless/wireless-links": WirelessLink,
}

# Dependency mapping, key is app/model path, value is list of dependent app/model paths
#  that needs to be created before the key model.
dependencies = {k: [] for k in models_map}

for parent, model in models_map.items():
    # if parent not in [
    #     "extras/tags",
    #     "dcim/devices",
    # ]:
    #     continue
    related_objects = list(model._meta.related_objects)
    for related_object in related_objects:
        meta = related_object.related_model._meta
        app = meta.app_label
        model = meta.model_name
        plural = meta.verbose_name_plural.replace(" ", "-").lower()
        child = f"{app}/{plural}"
        print(f"{parent=} {child=}")
        if child == parent:
            continue
        dependencies.setdefault(child, [])
        dependencies[child].append(parent)
        dependencies[child] = sorted(set(dependencies[child]))

pprint(dependencies)
