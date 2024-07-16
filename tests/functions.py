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
from tests.params import (
    AGGREGATE1,
    AGGREGATE2,
    ASN1,
    ASN2,
    ASN_RANGE1,
    CABLE1,
    CIRCUIT1,
    CIRCUIT_TYPE1,
    CLUSTER1,
    CLUSTER_GROUP1,
    CLUSTER_TYPE1,
    CONSOLE_PORT1,
    D1_INTERFACE1,
    D1_INTERFACE2,
    D2_INTERFACE1,
    D3_INTERFACE1,
    DEVICE1,
    DEVICE2,
    DEVICE3,
    DEVICE_ROLE1,
    DEVICE_ROLE3,
    DEVICE_TYPE1,
    IP_ADDRESS1,
    IP_ADDRESS2,
    IP_ADDRESS3,
    IP_ADDRESS4,
    LOCATION1,
    MANUFACTURER1,
    PLATFORM1,
    PREFIX1,
    PREFIX2,
    PREFIX3,
    PREFIX4,
    PREFIX5,
    PROVIDER1,
    PROVIDER_ACCOUNT1,
    PROVIDER_NETWORK1,
    RACK1,
    RACK_ROLE1,
    REGION1,
    RIR1,
    RIR2,
    ROLE1,
    ROLE2,
    ROLE3,
    ROLE4,
    ROLE5,
    ROUTE_TARGET1,
    SITE1,
    SITE2,
    SITE_GROUP1,
    TAG1,
    TAG3,
    TENANT1,
    TENANT_GROUP1,
    TERMINATION1,
    TERMINATION2,
    VIRTUAL_INTERFACE1,
    VIRTUAL_MACHINE1,
    VLAN1,
    VLAN2,
    VLAN_GROUP1,
    VRF1,
)


def full_tree() -> NbTree:
    """Init tree with data, ready for tests."""
    _interfaces = [D1_INTERFACE1, D1_INTERFACE2, D2_INTERFACE1, D3_INTERFACE1]
    tree = NbTree(
        circuits=CircuitsM(
            circuit_terminations={int(d["id"]): d for d in [TERMINATION1, TERMINATION2]},
            circuit_types={d["id"]: d for d in [CIRCUIT_TYPE1]},
            circuits={d["id"]: d for d in [CIRCUIT1]},
            provider_accounts={d["id"]: d for d in [PROVIDER_ACCOUNT1]},
            provider_networks={d["id"]: d for d in [PROVIDER_NETWORK1]},
            providers={d["id"]: d for d in [PROVIDER1]},
        ),
        dcim=DcimM(
            cable_terminations={},
            cables={d["id"]: d for d in [CABLE1]},
            # connected_device, is not model
            console_port_templates={},
            console_ports={d["id"]: d for d in [CONSOLE_PORT1]},
            console_server_port_templates={},
            console_server_ports={},
            device_bay_templates={},
            device_bays={},
            device_roles={d["id"]: d for d in [DEVICE_ROLE1, DEVICE_ROLE3]},
            device_types={d["id"]: d for d in [DEVICE_TYPE1]},
            devices={d["id"]: d for d in [DEVICE1, DEVICE2, DEVICE3]},
            front_port_templates={},
            front_ports={},
            interface_templates={},
            interfaces={d["id"]: d for d in _interfaces},
            inventory_item_roles={},
            inventory_item_templates={},
            inventory_items={},
            locations={d["id"]: d for d in [LOCATION1]},
            manufacturers={d["id"]: d for d in [MANUFACTURER1]},
            module_bay_templates={},
            module_bays={},
            module_types={},
            modules={},
            platforms={d["id"]: d for d in [PLATFORM1]},
            power_feeds={},
            power_outlet_templates={},
            power_outlets={},
            power_panels={},
            power_port_templates={},
            power_ports={},
            rack_reservations={},
            rack_roles={d["id"]: d for d in [RACK_ROLE1]},
            racks={d["id"]: d for d in [RACK1]},
            rear_port_templates={},
            rear_ports={},
            regions={d["id"]: d for d in [REGION1]},
            site_groups={d["id"]: d for d in [SITE_GROUP1]},
            sites={d["id"]: d for d in [SITE1, SITE2]},
            virtual_chassis={},
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
            tags={d["id"]: d for d in [TAG1, TAG3]},
            webhooks={},
        ),
        ipam=IpamM(
            aggregates={d["id"]: d for d in [AGGREGATE1, AGGREGATE2]},
            asn_ranges={d["id"]: d for d in [ASN_RANGE1]},
            asns={d["id"]: d for d in [ASN1, ASN2]},
            fhrp_group_assignments={},
            fhrp_groups={},
            ip_addresses={d["id"]: d for d in [IP_ADDRESS1, IP_ADDRESS2, IP_ADDRESS3, IP_ADDRESS4]},
            ip_ranges={},
            l2vpn_terminations={},
            l2vpns={},
            prefixes={d["id"]: d for d in [PREFIX1, PREFIX2, PREFIX3, PREFIX4, PREFIX5]},
            rirs={d["id"]: d for d in [RIR1, RIR2]},
            roles={d["id"]: d for d in [ROLE1, ROLE2, ROLE3, ROLE4, ROLE5]},
            route_targets={d["id"]: d for d in [ROUTE_TARGET1]},
            service_templates={},
            services={},
            vlan_groups={d["id"]: d for d in [VLAN_GROUP1]},
            vlans={d["id"]: d for d in [VLAN1, VLAN2]},
            vrfs={d["id"]: d for d in [VRF1]},
        ),
        tenancy=TenancyM(
            contact_assignments={},
            contact_groups={},
            contact_roles={},
            contacts={},
            tenant_groups={d["id"]: d for d in [TENANT_GROUP1]},
            tenants={d["id"]: d for d in [TENANT1]},
        ),
        virtualization=VirtualizationM(
            cluster_groups={d["id"]: d for d in [CLUSTER_GROUP1]},
            cluster_types={d["id"]: d for d in [CLUSTER_TYPE1]},
            clusters={d["id"]: d for d in [CLUSTER1]},
            interfaces={d["id"]: d for d in [VIRTUAL_INTERFACE1]},
            virtual_machines={d["id"]: d for d in [VIRTUAL_MACHINE1]},
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
        vrf = deepcopy(VRF1)
        vrf["id"] = id_
        data[id_] = vrf
    return data