"""Helpers for tests."""
from copy import deepcopy

from nbforager.nb_tree import (
    CircuitsM,
    DcimM,
    ExtrasM,
    IpamM,
    NbTree,
    TenancyM,
    VirtualizationM,
    WirelessM,
)
from nbforager.types_ import DiDAny, LInt
from tests import params as p


def full_tree() -> NbTree:
    """Init tree with data, ready for tests."""
    tree = NbTree(
        circuits=CircuitsM(
            circuit_terminations=p.TERMINATIONS,
            circuit_types=p.CIRCUIT_TYPES,
            circuits=p.CIRCUITS,
            provider_accounts=p.PROVIDER_ACCOUNTS,
            provider_networks=p.PROVIDER_NETWORKS,
            providers=p.PROVIDERS,
        ),
        dcim=DcimM(
            cable_terminations={},
            cables=p.CABLES,
            # connected_device, is not model
            console_port_templates={},
            console_ports=p.CONSOLES,
            console_server_port_templates={},
            console_server_ports={},
            device_bay_templates={},
            device_bays={},
            device_roles=p.DEVICE_ROLES,
            device_types=p.DEVICE_TYPES,
            devices=p.DEVICES,
            front_port_templates={},
            front_ports={},
            interface_templates={},
            interfaces=p.INTERFACES,
            inventory_item_roles={},
            inventory_item_templates={},
            inventory_items={},
            locations=p.LOCATIONS,
            manufacturers=p.MANUFACTURERS,
            module_bay_templates={},
            module_bays={},
            module_types={},
            modules={},
            platforms=p.PLATFORMS,
            power_feeds={},
            power_outlet_templates={},
            power_outlets={},
            power_panels={},
            power_port_templates={},
            power_ports={},
            rack_reservations={},
            rack_roles=p.RACK_ROLES,
            racks=p.RACKS,
            rear_port_templates={},
            rear_ports={},
            regions=p.REGIONS,
            site_groups=p.SITE_GROUPS,
            sites=p.SITES,
            virtual_chassis=p.VIRTUAL_CHASSIS,
            virtual_device_contexts={},
        ),
        extras=ExtrasM(
            bookmarks={},
            config_contexts={},
            config_templates={},
            content_types={},
            custom_field_choice_sets={},
            custom_fields={},
            custom_links={},
            export_templates={},
            image_attachments={},
            journal_entries={},
            object_changes={},
            reports={},
            saved_filters={},
            scripts={},
            tags=p.TAGS,
            webhooks={},
        ),
        ipam=IpamM(
            aggregates=p.AGGREGATES,
            asn_ranges=p.ASN_RANGES,
            asns=p.ASNS,
            fhrp_group_assignments={},
            fhrp_groups={},
            ip_addresses=p.IP_ADDRESSES,
            ip_ranges={},
            l2vpn_terminations={},
            l2vpns={},
            prefixes=p.PREFIXES,
            rirs=p.RIRS,
            roles=p.ROLES,
            route_targets=p.ROUTE_TARGETS,
            service_templates={},
            services={},
            vlan_groups=p.VLAN_GROUPS,
            vlans=p.VLANS,
            vrfs=p.VRFS,
        ),
        tenancy=TenancyM(
            contact_assignments={},
            contact_groups={},
            contact_roles={},
            contacts={},
            tenant_groups=p.TENANT_GROUPS,
            tenants=p.TENANTS,
        ),
        virtualization=VirtualizationM(
            cluster_groups=p.CLUSTER_GROUPS,
            cluster_types=p.CLUSTER_TYPES,
            clusters=p.CLUSTERS,
            interfaces=p.VIRTUAL_INTERFACES,
            virtual_machines=p.VIRTUAL_MACHINES,
        ),
        wireless=WirelessM(
            wireless_lan_groups={},
            wireless_lans={},
            wireless_links={},
        ),
    )
    return tree


def vrf_d(ids: LInt) -> DiDAny:
    """Init simple Netbox ipam vrf object."""
    data = {}
    for id_ in ids:
        vrf = deepcopy(p.VRF1_D)
        vrf["id"] = id_
        data[id_] = vrf
    return data
