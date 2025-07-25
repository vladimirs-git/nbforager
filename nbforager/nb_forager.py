# pylint: disable=R0801,R0902,R0913,R0914,R0915

"""NbForager."""

from __future__ import annotations

import copy
import logging
from copy import deepcopy
from datetime import datetime
from pathlib import Path

from vhelpers import vstr

from nbforager import nb_tree
from nbforager.foragers.circuits import CircuitsAF
from nbforager.foragers.core import CoreAF
from nbforager.foragers.dcim import DcimAF
from nbforager.foragers.extras import ExtrasAF
from nbforager.foragers.ipam import IpamAF
from nbforager.foragers.joiner import Joiner
from nbforager.foragers.tenancy import TenancyAF
from nbforager.foragers.users import UsersAF
from nbforager.foragers.virtualization import VirtualizationAF
from nbforager.foragers.vpn import VpnAF
from nbforager.foragers.wireless import WirelessAF
from nbforager.messages import Messages
from nbforager.nb_api import NbApi
from nbforager.nb_cache import NbCache
from nbforager.nb_tree import NbTree
from nbforager.parser.nb_value import NbValue
from nbforager.types_ import LStr, DAny, DiDAny, ODLStr


class NbForager:
    """Forages data from Netbox for further processing.

    - Requests data from Netbox (using NbApi) and save in the NbForager.root object,
    - Assemble objects within itself as a multidimensional dictionary in NbForager.tree object,
    - Read/write objects from/to the cache pickle file,
    """

    def __init__(
        self,
        host: str,
        token: str = "",
        scheme: str = "https",
        port: int = 0,
        verify: bool = True,
        limit: int = 1000,
        url_length: int = 2047,
        threads: int = 1,
        interval: float = 0.0,
        # Errors processing
        timeout: int = 60,
        max_retries: int = 0,
        sleep: int = 10,
        strict: bool = False,
        # Settings
        extended_get: bool = True,
        loners: ODLStr = None,
        cache: str = "",
        **kwargs,
    ):
        """Init NbForager.

        :param cache: Path to cache. If the value ends with .pickle,
            it is the path to a file; otherwise, it is the path to a directory.
            The default value is NbCache.{host}.pickle.

        NbApi parameters:

        :param str host: Netbox host name.

        :param str token: Netbox token.

        :param str scheme: Access method: `https` or `http`. Default is `https`.

        :param int port: TCP port.
            Default is `443` for scheme=`https`, `80` for scheme=`http`.

        :param bool verify: Transport Layer Security.
            `True` - A TLS certificate required,
            `False` - Requests will accept any TLS certificate.
            Default is `True`.

        :param int limit: Split the query to multiple requests
            if the count of objects exceeds this value. Default is `1000`.

        :param int url_length: Split the query to multiple requests
            if the URL length exceeds maximum length due to a long list of
            GET parameters. Default is `2047`.

        :param int threads: Threads count. <=1 is loop mode, >=2 is threading mode.
            Default id `1`.

        :param float interval: Wait this time between the threading requests (seconds).
            Default is `0`. Useful to optimize session spikes and achieve
            script stability in Docker with limited resources.

        :param int timeout: Session timeout (seconds). Default is `60`.

        :param int max_retries: Retries the request multiple times if the Netbox API
            does not respond or responds with a timeout. Default is `0`. This is useful
            for scheduled scripts in cron jobs, when the connection to Netbox server is
            not stable.

        :param int sleep: Interval (seconds) before the next retry after
            session timeout reached. Default is `10`.

        :param bool strict: When querying objects by tag, if there are no tags present,
            the Netbox API response returns a status_code=400.
            True - ConnectionError is raised when status_code=400.
            False - WARNING message is logged and an empty list is returned with status_code=200.
            Default is `False`.

        :param bool extended_get: True - Extend filtering parameters in GET request,
            ``{parameter}`` can be used instead of ``{parameter}_id``. Default is `True`.

        :param dict loners: Set :ref:`Filtering parameters in an OR manner`.

        Data attributes:

        :ivar obj root: :py:class:`NbTree` object that holds raw Netbox objects.
            It is data source for the tree.
        :ivar obj tree: :py:class:`NbTree` object that holds joined Netbox objects.
        :ivar dict status: Result from Netbox status endpoint. Netbox version.

        Application/model foragers:

        :ivar obj circuits: :py:class:`.CircuitsAF` :doc:`CircuitsAF`.
        :ivar obj core: :py:class:`.CoreAF` :doc:`CoreAF`.
        :ivar obj dcim: :py:class:`.DcimAF` :doc:`DcimAF`.
        :ivar obj extras: :py:class:`.ExtrasAF` :doc:`ExtrasAF`.
        :ivar obj ipam: :py:class:`.IpamAF` :doc:`IpamAF`.
        :ivar obj tenancy: :py:class:`.TenancyAF` :doc:`TenancyAF`.
        :ivar obj users: :py:class:`.UsersAF` :doc:`UsersAF`.
        :ivar obj virtualization: :py:class:`.VirtualizationAF` :doc:`VirtualizationAF`.
        :ivar obj wireless: :py:class:`.WirelessAF` :doc:`WirelessAF`.
        """
        kwargs = {
            "host": host,
            "token": token,
            "scheme": scheme,
            "port": port,
            "verify": verify,
            "limit": limit,
            "url_length": url_length,
            "threads": threads,
            "interval": interval,
            "timeout": timeout,
            "max_retries": max_retries,
            "sleep": sleep,
            "strict": strict,
            "extended_get": extended_get,
            "loners": loners,
            **kwargs,
        }
        # data
        self.root: NbTree = NbTree()  # original data
        self.tree: NbTree = NbTree()  # data with joined objects within itself
        self.status: DAny = {}  # updated Netbox status data

        self.api = NbApi(**kwargs)
        self.cache: str = make_cache_path(cache, **kwargs)
        self.msgs = Messages(name=self.api.host)

        # application foragers
        self.circuits = CircuitsAF(self.api, self.root, self.tree)
        self.core = CoreAF(self.api, self.root, self.tree)
        self.dcim = DcimAF(self.api, self.root, self.tree)
        self.extras = ExtrasAF(self.api, self.root, self.tree)
        self.ipam = IpamAF(self.api, self.root, self.tree)
        self.tenancy = TenancyAF(self.api, self.root, self.tree)
        self.users = UsersAF(self.api, self.root, self.tree)
        self.virtualization = VirtualizationAF(self.api, self.root, self.tree)
        self.vpn = VpnAF(self.api, self.root, self.tree)
        self.wireless = WirelessAF(self.api, self.root, self.tree)

    def __repr__(self) -> str:
        """__repr__."""
        attrs = list(NbTree().model_dump())
        params_d = {s: getattr(self, s).count() for s in attrs}
        params = vstr.repr_info(**params_d)
        name = self.__class__.__name__
        return f"<{name}: {params}>"

    def __copy__(self) -> NbForager:
        """Copy NbForager.root and tree objects.

        :return: Copy of NbForager object.
        """
        connector = self.api.circuits.circuits
        params_d = {s: getattr(connector, s) for s in getattr(connector, "_init_params")}
        nbf = NbForager(**params_d)
        nb_tree.insert_tree(src=self.root, dst=nbf.root)
        return nbf

    @property
    def host(self) -> str:
        """Netbox host name."""
        return self.api.host

    @property
    def url(self) -> str:
        """Netbox URL."""
        return self.api.url

    @property
    def threads(self) -> int:
        """Threads count."""
        return self.api.threads

    @threads.setter
    def threads(self, threads: int) -> None:
        """Set the number of threads.

        :param threads: Threads count to set.

        :return: None. Update threads in all connectors.
        """
        self.api.threads = threads

    # =========================== method =============================

    def clear(self, root: bool = True, tree: bool = True) -> None:
        """Clear objects by resetting the NbForager.root and NbForager.tree.

        :param root: If True, clear data in NbForager.root.
        :param tree: If True, reset NbForager.tree.
        :return: None. Update self object.
        """
        if root:
            for app in self.root.apps():
                for model in getattr(self.root, app).models():
                    data: dict = getattr(getattr(self.root, app), model)
                    data.clear()
        if tree:
            self.tree.clear()

    def copy(self) -> NbForager:
        """Copy data in the NbForager.root and NbForager.tree.

        :return: Copy of NbForager object.

        :rtype: NbForager
        """
        return copy.copy(self)

    def count(self) -> int:
        """Count of the Netbox objects in the NbForager.root object.

        :return: Count of the Netbox objects.

        :rtype: int
        """
        counts = []
        for app in self.root.apps():
            count = getattr(self, app).count()
            counts.append(count)
        return sum(counts)

    def get_status(self) -> None:
        """Retrieve status from the Netbox, save data to the NbForager.status.

        :return: None. Update self object.
        """
        status = self.api.status.get()
        if not isinstance(status, dict):
            status = {}
        self.status = status

    def join_tree(self, dcim: bool = False, ipam: bool = False) -> None:
        """Assemble Netbox objects in NbForager.tree within itself.

        The Netbox objects are represented as a multidimensional dictionary.

        :param dcim: True - Create additional keys to represent Netbox dcim objects.
            False - Only join objects that are present in the API response.

            In dcim.devices, virtualization.virtual_machines:

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

            In dcim.interfaces, virtualization.interfaces:

            - ``_ip_addresses``

        :param ipam: True - Create additional keys to represent Netbox ipam objects.
            False - Only join objects that are present in the API response.

            In ipam.aggregate, ipam.prefixes, ipam.ip_addresses:

            - ``_ipv4`` IPv4 object
            - ``_aggregate`` Aggregate data for ipam.prefixes and ipam.ip_addresses
            - ``_super_prefix`` Related parent prefix data for ipam.prefixes and ipam.ip_addresses
            - ``_sub_prefixes`` Related child prefixes data for ipam.prefixes and ipam.ip_addresses
            - ``_ip_addresses`` Related IP addresses data for ipam.aggregates and ipam.prefixes

        :return: NbTree object with the joined Netbox objects.

        :rtype: NbTree
        """
        tree: NbTree = deepcopy(self.root)
        Joiner(tree).init_extra_keys()
        tree = nb_tree.join_tree(tree)
        nb_tree.insert_tree(src=tree, dst=self.tree)

        joiner = Joiner(self.tree)
        if dcim:
            joiner.join_dcim_devices()
        if ipam:
            joiner.join_ipam_ipv4()

    def read_cache(self) -> None:
        """Read cached data from a pickle file.

        Save data to the NbForager.root and NbForager.status.

        :return: None. Update self object.
        """
        cache = NbCache(cache=self.cache)
        tree, status = cache.read_cache()
        nb_tree.insert_tree(src=tree, dst=self.root)
        self.status = status

    def write_cache(self) -> None:
        """Write NbForager.root nad NbForager.status to a pickle file.

        :return: None. Update a pickle file.
        """
        status: DAny = self.status.copy()
        status["meta"] = {
            "host": self.api.host,
            "url": self.api.url,
            "write_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        }

        cache = NbCache(tree=self.root, status=status, cache=self.cache)
        cache.write_cache()

    def version(self) -> str:
        """Get Netbox version from the NbForager.status.

        Before getting the version, you need to update the NbForager.status by
        using the get_status() or read_cache() method.

        :return: Netbox version if version >= 3, otherwise empty string.
        """
        return str(self.status.get("netbox-version") or "0.0.0")

    # =========================== data methods ===========================

    def _devices_primary_ip4(self) -> LStr:
        """Return the primary IPv4 addresses of Netbox devices with these settings.

        :return: primary_ip4 addresses of devices.
        """
        ip4s: LStr = []
        for device in self.root.dcim.devices.values():  # pylint: disable=E1101
            if ip4 := NbValue(device).primary_ip4():
                ip4s.append(ip4)
        return ip4s

    def _set_ipam_ip_addresses_mask_32(self) -> None:
        """Change mask to /32 for all Netbox ip-addresses.

        :return: None. Update self object.
        """
        for data in self.root.ipam.ip_addresses.values():  # pylint: disable=E1101
            if data["address"].find("/") >= 0:
                ip_ = data["address"].split("/")[0]
                data["address"] = ip_ + "/32"

    def _print_warnings(self) -> None:
        """Print WARNINGS if found some errors/warnings in data processing."""
        for app in self.root.apps():
            for model in getattr(self.root, app).models():
                nb_objects: DiDAny = getattr(getattr(self.root, app), model)
                for nb_object in nb_objects.values():
                    if warnings := nb_object.get("warnings") or []:
                        for warning in warnings:
                            logging.warning(warning)


# noinspection PyIncorrectDocstring
def make_cache_path(cache: str = "", **kwargs) -> str:
    """Make path to pickle file.

    :param cache: Path to pickle file.
    :param name: Parent object name.
    :param host: Netbox host name.

    :return: Path to cache pickle file.
    """
    if cache.endswith(".pickle"):
        return cache
    name = str(kwargs.get("name") or "")
    host = str(kwargs.get("host") or "")
    if not (name or host):
        name = NbCache().__class__.__name__
    file_items = [name, host, "pickle"]
    file_items = [s for s in file_items if s]
    name = ".".join(file_items)
    path = Path(cache, name)
    return str(path)
