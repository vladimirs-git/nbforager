"""Joiner."""

from operator import itemgetter

from netports import IPv4
from vhelpers import vlist

from nbforager import ami
from nbforager.api.base_c import BaseC
from nbforager.nb_tree import NbTree
from nbforager.parser import nb_parser
from nbforager.parser.nb_value import NbValue
from nbforager.types_ import LDAny, DAny, LStr, DiDAny, LInt, DiLDAny, SInt


class Joiner:
    """Helper methods are used to create additional keys in Netbox objects,

    representing them similarly to the WEB UI.
    """

    def __init__(self, tree: NbTree):
        """Initialize Joiner.
        :param NbTree tree: Contains Netbox that need to be updated similar to the WEB UI.
        """
        self.tree = tree

    # noinspection PyProtectedMember
    def init_extra_keys(self) -> None:
        """Initialize extra keys to represent Netbox objects similar to the WEB UI.

        :return: None. Update NbTree object.
        """
        for app, model in [
            ("dcim", "devices"),
            ("dcim", "interfaces"),
            ("virtualization", "virtual_machines"),
            ("virtualization", "interfaces"),
        ]:
            key = ami.attr_to_model(f"{app}/{model}/")
            extra_keys: LStr = BaseC._extra_keys[key]  # pylint: disable=W0212
            objects_d: DiDAny = getattr(getattr(self.tree, app), model)
            for object_d in objects_d.values():
                for _key in extra_keys:
                    object_d[_key] = {}

        for model, key, strict in [
            ("aggregates", "prefix", True),
            ("prefixes", "prefix", True),
            ("ip_addresses", "address", False),
        ]:
            objects: DiDAny = getattr(self.tree.ipam, model)
            for data in objects.values():
                nbv = NbValue(data=data)
                family: int = nbv.family_value()
                if family != 4:
                    continue
                snet = data[key]
                data["_ipv4"] = IPv4(snet, strict=strict)
                data["_aggregate"] = {}  # DAny
                data["_super_prefix"] = {}  # DAny
                data["_sub_prefixes"] = []  # LDAny
                data["_ip_addresses"] = []  # LDAny

    def join_dcim_devices(self) -> None:
        """Create additional keys to represent dcim.devices similar to the WEB UI.

            In dcim.devices:

            - ``_console_ports``
            - ``_console_server_ports``
            - ``_device_bays``
            - ``_front_ports``
            - ``_interfaces``
            - ``_inventory_items``
            - ``_module_bays``
            - ``_power_outlets``
            - ``_power_ports``
            - ``_rear_ports``
            - ``_vc_members``

            In dcim.interfaces:

            - ``_ip_addresses``

        :return: None. Update NbTree object.
        """
        self._join_virtual_chassis()
        intf_ids: LInt = self._join_dcim_devices()
        self._join_ip_addresses(intf_ids, app="dcim")

    def _join_virtual_chassis(self):
        """Add virtual-chassis members to master devices.

        :return: None. Update data in object.
        """
        app = "dcim"
        model = "devices"
        nbf_devices: DiDAny = getattr(getattr(self.tree, app), model)

        for member_id, device_d in nbf_devices.items():
            if device_d["virtual_chassis"]:
                master_id: int = device_d["virtual_chassis"]["master"]["id"]
                if member_id != master_id:
                    if master_d := nbf_devices.get(master_id, {}):
                        master_d["_vc_members"][member_id] = nbf_devices[member_id]

    def _join_dcim_devices(self) -> LInt:
        """Create additional key/values to represent devices similar to the WEB UI.

        Create key/values: _interfaces, _front_ports, _console_ports, etc.

        :return: IDs of joined ports. Update NbTree.dcim.devices object.
        """
        # models
        app = "dcim"
        model = "devices"
        # noinspection PyProtectedMember
        extra_keys: LStr = BaseC._extra_keys["dcim/devices/"]  # pylint: disable=W0212
        extra_keys = [s for s in extra_keys if s != "_vc_members"]
        extra_models: LStr = [s.lstrip("_") for s in extra_keys]
        nbf_devices: DiDAny = getattr(getattr(self.tree, app), model)

        # joined interfaces, need find assigned ip-addresses
        intf_ids: SInt = set()

        # set  _interfaces, _front_ports, etc.
        for extra_model in extra_models:
            ports_d: DiDAny = getattr(getattr(self.tree, app), extra_model)
            for nb_port in ports_d.values():
                port_name = nb_port["name"]
                device_id: int = nb_port["device"]["id"]
                nb_device: DAny = nbf_devices.get(device_id, {})
                extra_key = f"_{extra_model}"

                # if device has been downloaded from netbox
                if extra_key in nb_device:
                    nb_device[extra_key][port_name] = nb_port

                    # interface ids to assign ip_addresses
                    if extra_model == "interfaces":
                        intf_id = nb_port["id"]
                        intf_ids.add(intf_id)

        # join virtual chassis interfaces to master
        for device_id, nb_device in nbf_devices.items():
            for vc_member in nb_device["_vc_members"].values():
                master_id = vc_member["virtual_chassis"]["master"]["id"]
                if device_id == master_id:
                    for intf_name, nb_intf in vc_member["_interfaces"].items():
                        if intf_name not in nb_device["_interfaces"]:
                            nb_device["_interfaces"][intf_name] = nb_intf

        return sorted(intf_ids)

    def _join_ip_addresses(self, intf_ids: LInt, app: str) -> None:
        """Add NbTree.ipam.ip_address data to NbTree.dcim.interfaces._ip_addresses or VM.

        :param intf_ids: Interface IDs that was joined in device/VM.
        :param app: Application name: "dcim", "virtualization"

        :return: None. Update NbTree.ipam.ip_addresses.
        """
        model = "interfaces"
        object_type = "virtualization.vminterface" if app == "virtualization" else "dcim.interface"
        intfs_d: DiDAny = getattr(getattr(self.tree, app), model)
        params = {"id": intf_ids}
        intfs_d = {
            d["id"]: d for d in nb_parser.find_objects(objects=list(intfs_d.values()), **params)
        }

        app = "ipam"
        extra_model = "ip_addresses"
        extra_key = f"_{extra_model}"
        nbf_addresses: DiDAny = getattr(getattr(self.tree, app), extra_model)

        for nb_addr in nbf_addresses.values():
            address = nb_addr["address"]
            if nb_addr["assigned_object_type"] == object_type:
                if assigned_object_id := nb_addr["assigned_object_id"]:
                    nb_intf: DAny = intfs_d.get(assigned_object_id, {})  # pylint: disable=E1101

                    # if device has been downloaded from netbox
                    if extra_key in nb_intf:
                        nb_intf[extra_key][address] = nb_addr

    def join_ipam_ipv4(self, ipam: bool = False, ipam_prefixes: bool = False) -> None:
        """Create additional keys to represent ipam similar to the WEB UI.

            Add new attributes in ipam/aggregates, ipam/prefixes, ipam/ip-addresses:

            - ``_ipv4`` IPv4 object
            - ``_aggregate`` Aggregate data for ipam/prefixes and ipam/ip-addresses
            - ``_super_prefix`` Related parent prefix data for ipam/prefixes and ipam/ip-addresses
            - ``_sub_prefixes`` Related child prefixes data for ipam/prefixes and ipam/ip-addresses
            - ``_ip_addresses`` Related IP addresses data for ipam/aggregates and ipam/prefixes

        :param ipam: True - Create additional keys to represent Netbox ipam objects.
            Set all `ipam_{model}` arguments to True, to join related objects.

        :param ipam_prefixes: True - Join only ipam/prefixes, skip ipam/ip-addresses.

        :return: None. Update NbTree object.
        """
        if ipam or ipam_prefixes:
            self._join_ipam_aggregates()
            self._join_ipam_prefixes()
        if ipam:
            self._join_ipam_ip_addresses()
        if ipam or ipam_prefixes:
            self._join_update_sub_prefixes()

    def _join_ipam_aggregates(self) -> None:
        """Add prefixes to aggregates.

        :return: None. Update ipam/aggregates._sub_prefixes, ipam/prefixes._aggregate.
        """
        nb_aggregates: LDAny = self._filter_aggregates_ip4()
        depth_prefixes_dl: DiLDAny = self._group_prefixes_ip4()

        for nb_aggregate in nb_aggregates:
            for depth, nb_prefixes in depth_prefixes_dl.items():
                for nb_prefix in nb_prefixes:
                    aggregate: IPv4 = nb_aggregate["_ipv4"]
                    prefix: IPv4 = nb_prefix["_ipv4"]
                    if prefix in aggregate:
                        nb_prefix["_aggregate"] = nb_aggregate
                        if depth == 0:  # super-prefix
                            nb_aggregate["_sub_prefixes"].append(nb_prefix)

    def _join_ipam_ip_addresses(self) -> None:
        """Add prefixes to ip-addresses.

        :return: None. Update ipam/aggregates._sub_prefixes, ipam/prefixes._aggregate.
        """
        nb_addresses: LDAny = self._filter_ip_addresses_ip4()
        depth_prefixes_dl: DiLDAny = self._group_prefixes_ip4()
        depths: LInt = list(depth_prefixes_dl)
        depths.reverse()

        updated: LInt = []  # IDs of updated ipam/ip-addresses, to skip

        for depth in depths:
            nb_addresses_ = nb_addresses.copy()
            nb_prefixes: LDAny = depth_prefixes_dl.get(depth, [])
            for nb_address in nb_addresses_:
                address: IPv4 = nb_address["_ipv4"]
                for nb_prefix in nb_prefixes:
                    if nb_address["id"] in updated:
                        continue
                    prefix: IPv4 = nb_prefix["_ipv4"]
                    if address in prefix:
                        nb_address["_aggregate"] = nb_prefix["_aggregate"]
                        nb_address["_super_prefix"] = nb_prefix
                        nb_prefix["_ip_addresses"].append(nb_address)
                        updated.append(nb_address["id"])
            nb_addresses = [d for d in nb_addresses if d["id"] not in updated]

    def _join_ipam_prefixes(self) -> None:
        """Add prefixes to prefixes.

        :return: None. Update ipam/prefixes._sub_prefixes, ipam/prefixes._super_prefix.
        """
        nb_super_prefixes: LDAny = []
        depth_prefixes_dl: DiLDAny = self._group_prefixes_ip4()

        for depth, nb_sub_prefixes in enumerate(depth_prefixes_dl.values()):
            if not depth:
                nb_super_prefixes = nb_sub_prefixes
                continue
            for nb_super_prefix in nb_super_prefixes:
                super_prefix: IPv4 = nb_super_prefix["_ipv4"]
                if super_prefix == 32:
                    continue
                for nb_sub_prefix in nb_sub_prefixes:
                    sub_prefix: IPv4 = nb_sub_prefix["_ipv4"]
                    if sub_prefix in super_prefix:
                        nb_super_prefix["_sub_prefixes"].append(nb_sub_prefix)
                        nb_sub_prefix["_super_prefix"] = nb_super_prefix
            nb_super_prefixes = nb_sub_prefixes

    def _join_update_sub_prefixes(self) -> None:
        """Update _sub_prefixes in aggregates and prefixes.

        Remove duplicates, remove objects with improper depth, sort by IPv4.

        :return: None. Update ipam/aggregates._sub_prefixes, ipam/prefixes._sub_prefixes.
        """
        nb_aggregates: LDAny = self._filter_aggregates_ip4()
        for nb_aggregate in nb_aggregates:
            sub_prefixes: LDAny = vlist.no_dupl(nb_aggregate["_sub_prefixes"])
            sub_prefixes = [d for d in sub_prefixes if not d["_super_prefix"]]
            nb_aggregate["_sub_prefixes"] = sorted(sub_prefixes, key=itemgetter("_ipv4"))

        nb_prefixes: LDAny = self._filter_prefixes_ip4()
        for nb_prefix in nb_prefixes:
            sub_prefixes = vlist.no_dupl(nb_prefix["_sub_prefixes"])
            nb_prefix["_sub_prefixes"] = sorted(sub_prefixes, key=itemgetter("_ipv4"))
            ip_addresses = vlist.no_dupl(nb_prefix["_ip_addresses"])
            nb_prefix["_ip_addresses"] = sorted(ip_addresses, key=itemgetter("_ipv4"))

    # ============================= helpers ==============================

    def _filter_aggregates_ip4(self) -> LDAny:
        """Filter ipam/aggregates family=4, sorted by IPv4.

        :return: ipam/aggregates objects.
        """
        nb_aggregates: LDAny = []

        for nb_aggregate in self.tree.ipam.aggregates.values():
            if nb_aggregate["family"]["value"] == 4:
                nb_aggregates.append(nb_aggregate)

        return sorted(nb_aggregates, key=itemgetter("_ipv4"))

    def _filter_ip_addresses_ip4(self) -> LDAny:
        """Filter ipam/ip-addresses family=4 without VRF, sorted by IPv4.

        :return: ipam/ip-addresses objects.
        """
        ip_addresses: LDAny = []

        for ip_address in self.tree.ipam.ip_addresses.values():
            if ip_address["family"]["value"] == 4 and ip_address["vrf"] is None:
                ip_addresses.append(ip_address)

        return sorted(ip_addresses, key=itemgetter("_ipv4"))

    def _filter_prefixes_ip4(self) -> LDAny:
        """Filter ipam/prefixes family=4, sorted by IPv4.

        :return: ipam/prefixes objects.
        """
        nb_prefixes: LDAny = []

        for nb_prefix in self.tree.ipam.prefixes.values():
            if nb_prefix["family"]["value"] == 4 and nb_prefix["vrf"] is None:
                nb_prefixes.append(nb_prefix)

        return sorted(nb_prefixes, key=itemgetter("_ipv4"))

    def _group_prefixes_ip4(self) -> DiLDAny:
        """Group ipam/prefixes by depth counter.

        :return: A dictionary of prefixes where the key represents the depth
            and the value represents a list of imap/prefixes at that depth.
        """
        nb_prefixes: LDAny = self._filter_prefixes_ip4()
        depth_prefixes_dl: DiLDAny = {d["_depth"]: [] for d in nb_prefixes}

        for nb_prefix in nb_prefixes:
            depth: int = int(nb_prefix["_depth"])
            depth_prefixes_dl[depth].append(nb_prefix)

        return depth_prefixes_dl
