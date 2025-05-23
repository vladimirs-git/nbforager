# pylint: disable=R0902,R0903

"""IPAM Forager."""

from nbforager.foragers.base_fa import BaseAF
from nbforager.foragers.forager import Forager
from nbforager.nb_api import NbApi
from nbforager.nb_tree import NbTree


class IpamAF(BaseAF):
    """IPAM Forager."""

    def __init__(self, api: NbApi, root: NbTree, tree: NbTree):
        """Init IpamAF.

        :param api: NbApi object, connector to Netbox API.
        :param root: NbTree object where raw data from Netbox needs to be saved.
        :param tree: NbTree object where transformed data from Netbox needs to be saved.
        """
        super().__init__(api, root, tree)
        self.aggregates = self.AggregatesF(self)
        self.asn_ranges = self.AsnRangesF(self)
        self.asns = self.AsnsF(self)
        self.fhrp_group_assignments = self.FhrpGroupAssignmentsF(self)
        self.fhrp_groups = self.FhrpGroupsF(self)
        self.ip_addresses = self.IpAddressesF(self)
        self.ip_ranges = self.IpRangesF(self)
        self.l2vpn_terminations = self.L2vpnTerminationsF(self)
        self.l2vpns = self.L2vpnsF(self)
        self.prefixes = self.PrefixesF(self)
        self.rirs = self.RirsF(self)
        self.roles = self.RolesF(self)
        self.route_targets = self.RouteTargetsF(self)
        self.service_templates = self.ServiceTemplatesF(self)
        self.services = self.ServicesF(self)
        self.vlan_groups = self.VlanGroupsF(self)
        self.vlans = self.VlansF(self)
        self.vrfs = self.VrfsF(self)

    class AggregatesF(Forager):
        """AggregatesF."""

    class AsnRangesF(Forager):
        """AsnRangesF."""

    class AsnsF(Forager):
        """AsnsF."""

    class FhrpGroupAssignmentsF(Forager):
        """FhrpGroupAssignmentsF."""

    class FhrpGroupsF(Forager):
        """FhrpGroupsF."""

    class IpAddressesF(Forager):
        """IpAddressesF."""

    class IpRangesF(Forager):
        """IpRangesF."""

    class L2vpnTerminationsF(Forager):
        """L2vpnTerminationsF."""

    class L2vpnsF(Forager):
        """L2vpnsF."""

    class PrefixesF(Forager):
        """PrefixesF."""

    class RirsF(Forager):
        """RirsF."""

    class RolesF(Forager):
        """RolesF."""

    class RouteTargetsF(Forager):
        """RouteTargetsF."""

    class ServiceTemplatesF(Forager):
        """ServiceTemplatesF."""

    class ServicesF(Forager):
        """ServicesF."""

    class VlanGroupsF(Forager):
        """VlanGroupsF."""

    class VlansF(Forager):
        """VlansF."""

    class VrfsF(Forager):
        """VrfsF."""
