# pylint: disable=R0902,R0903

"""Tenancy Virtualization."""

from nbforager.foragers.base_fa import BaseAF
from nbforager.foragers.forager import Forager
from nbforager.nb_api import NbApi
from nbforager.nb_tree import NbTree


class VirtualizationAF(BaseAF):
    """Virtualization Virtualization."""

    def __init__(self, api: NbApi, root: NbTree, tree: NbTree):
        """Init VirtualizationAF.

        :param api: NbApi object, connector to Netbox API.
        :param root: NbTree object where raw data from Netbox needs to be saved.
        :param tree: NbTree object where transformed data from Netbox needs to be saved.
        """
        super().__init__(api, root, tree)
        self.cluster_groups = self.ClusterGroupsF(self)
        self.cluster_types = self.ClusterTypesF(self)
        self.clusters = self.ClustersF(self)
        self.interfaces = self.InterfacesF(self)
        self.virtual_machines = self.VirtualMachinesF(self)

    class ClusterGroupsF(Forager):
        """ClusterGroupsF."""

    class ClusterTypesF(Forager):
        """ClusterTypesF."""

    class ClustersF(Forager):
        """ClustersF."""

    class InterfacesF(Forager):
        """InterfacesF."""

    class VirtualMachinesF(Forager):
        """VirtualMachinesF."""
