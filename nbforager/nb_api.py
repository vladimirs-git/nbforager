"""NbApi, Python wrapper of Netbox REST API."""

from __future__ import annotations

from copy import deepcopy
from typing import Callable

from requests import Response

from nbforager import ami, helpers
from nbforager.api.base_c import BaseC
from nbforager.api.circuits import CircuitsAC
from nbforager.api.connector import Connector, GConnector
from nbforager.api.core import CoreAC
from nbforager.api.dcim import DcimAC
from nbforager.api.extras import ExtrasAC
from nbforager.api.ipam import IpamAC
from nbforager.api.plugins import PluginsAC
from nbforager.api.status import StatusC
from nbforager.api.tenancy import TenancyAC
from nbforager.api.users import UsersAC
from nbforager.api.virtualization import VirtualizationAC
from nbforager.api.vpn import VpnAC
from nbforager.api.wireless import WirelessAC
from nbforager.constants import APPS
from nbforager.parser.nb_parser import NbParser
from nbforager.types import ODLStr, DAny, LDAny, LStr, LT2Str


class NbApi:
    """NbApi, Python wrapper of Netbox REST API.

    It is a set of connectors to Netbox endpoints.
    Connectors are nested by principle ``{application}.{model}.{method}``,
    where:

    - **application** can be: ``circuits``, ``dcim``, ``ipam``, etc.;
    - **model** can be: ``circuit_terminations``, ``ip_addresses``, etc.;
    - **method** can be: ``create``, ``delete``, ``get``, ``update``.

    For example https://demo.netbox.dev/api/ipam/ip-addresses/
    can be reached by ``NbApi.ipam.ip_addresses.get()`` method.

    The parameters for the ``create``, ``delete``, ``update`` methods are
    identical in all models.
    The parameters for the ``get`` method are different for each model.
    Only ``NbApi.ipam.ip_addresses.get()`` is described in this documentation.
    Other models are implemented in a similar manner.
    Exact parameters can be found in `Schema`_.
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
        # Multithreading
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
        **kwargs,
    ):
        """Initialize NbApi.

        :param str host: Netbox host name.

        :param str token: Netbox token.

        :param str scheme: Access method: `https` or `http`. Default is `https`.

        :param int port: TCP port.
            Default is `443` for scheme=`https`, `80` for scheme=`http`.

        :param bool verify: Transport Layer Security.
            `True` - A TLS certificate is required,
            `False` - Requests will accept any TLS certificate.
            Default is `True`.

        :param int limit: Split the query to multiple requests
            if the count of objects exceeds this value. Default is `1000`.

        :param int url_length: Split the query to multiple requests
            if the URL length exceeds maximum length due to a long list of
            GET parameters. Default is `2047`.

        :param int threads: Threads count. <=1 is loop mode, >=2 is threading mode.
            Default is `1`.

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
            True - HTTPError is raised when status_code=400.
            False - WARNING message is logged and an empty list is returned with status_code=200.
            Default is `False`.

        :param bool extended_get: True - Extend filtering parameters in GET request,
            ``{parameter}`` can be used instead of ``{parameter}_id``. Default is `True`.

        :param dict loners: Set :ref:`Filtering parameters in an OR manner`.

        Application/model connectors:

        :ivar obj circuits: :py:class:`.CircuitsAC` :doc:`CircuitsAC`.
        :ivar obj core: :py:class:`.CoreAC` :doc:`CoreAC`.
        :ivar obj dcim: :py:class:`.DcimAC` :doc:`DcimAC`.
        :ivar obj extras: :py:class:`.ExtrasAC` :doc:`ExtrasAC`.
        :ivar obj ipam: :py:class:`.IpamAC` :doc:`IpamAC`.
        :ivar obj plugins: :py:class:`.PluginsAC` :doc:`PluginsAC`.
        :ivar obj tenancy: :py:class:`.TenancyAC` :doc:`TenancyAC`.
        :ivar obj users: :py:class:`.UsersAC` :doc:`UsersAC`.
        :ivar obj virtualization: :py:class:`.VirtualizationAC` :doc:`VirtualizationAC`.
        :ivar obj wireless: :py:class:`.WirelessAC` :doc:`WirelessAC`.
        """
        params: DAny = {
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
        self._base_c = BaseC(**params)
        # app/model
        self.circuits = CircuitsAC(**params)
        self.core = CoreAC(**params)
        self.dcim = DcimAC(**params)
        self.extras = ExtrasAC(**params)
        self.ipam = IpamAC(**params)
        self.plugins = PluginsAC(**params)
        self.status = StatusC(**params)
        self.tenancy = TenancyAC(**params)
        self.users = UsersAC(**params)
        self.vpn = VpnAC(**params)
        self.virtualization = VirtualizationAC(**params)
        self.wireless = WirelessAC(**params)

    def __repr__(self) -> str:
        """__repr__."""
        return repr(self._base_c)

    def __copy__(self) -> NbApi:
        """Create a duplicate of the object.

        :return: A copy of the current object.
        """
        base_c: BaseC = self._base_c
        return type(self)(
            host=base_c.host,
            token=base_c.token,
            scheme=base_c.scheme,
            port=base_c.port,
            verify=base_c.verify,
            limit=base_c.limit,
            url_length=base_c.url_length,
            threads=base_c.threads,
            interval=base_c.interval,
            timeout=base_c.timeout,
            max_retries=base_c.max_retries,
            sleep=base_c.sleep,
            strict=base_c.strict,
            extended_get=base_c.extended_get,
            loners=base_c.loners,
        )

    # ============================= property =============================

    @property
    def host(self) -> str:
        """Netbox host name."""
        return self._base_c.host

    @property
    def url(self) -> str:
        """Netbox URL to API endpoints."""
        return self._base_c.url_api

    @property
    def url_api(self) -> str:
        """Netbox URL to API endpoints."""
        return self._base_c.url_api

    @property
    def threads(self) -> int:
        """Threads count."""
        return self._base_c.threads

    @threads.setter
    def threads(self, threads: int) -> None:
        """Set the number of threads.

        :param threads: Threads count to set.

        :return: None. Updates threads in all connectors.
        """
        self._base_c.threads = threads
        for app in self.apps():
            models: LStr = [s for s in dir(getattr(self, app)) if s[0].islower()]
            for model in models:
                connector = self.connector_by_path(f"{app}/{model}")
                setattr(connector, "threads", threads)

    # ============================= methods ==============================

    @staticmethod
    def apps() -> LStr:
        """Get list of application names.

        :return: Applications.
        :rtype: List[str]
        """
        return list(APPS)

    def app_models(self) -> LT2Str:
        """Get list of application model names.

        :return: Application model names.
        :rtype: List[Tuple[str, str]]
        """
        app_models: LT2Str = []
        for app in self.apps():
            models: LStr = [s for s in dir(getattr(self, app)) if s[0].islower()]
            for model in models:
                app_models.append((app, model))
        return app_models

    def app_paths(self) -> LStr:
        """Get list of application/model paths.

        :return: Application/model paths.
        :rtype: List[str]
        """
        app_paths: LStr = []
        for app in self.apps():
            models: LStr = [s for s in dir(getattr(self, app)) if s[0].islower()]
            for model in models:
                connector: Connector = self.connector_by_path(f"{app}/{model}")
                path = getattr(connector, "path")
                path = path.rstrip("/")
                app_paths.append(path)
        return app_paths

    def connector_by_path(self, path: str) -> Connector:
        """Get Connector instance by app/model path.

        :param path: app/model path.

        :return: Connector to the Netbox API endpoint.

        :example:
            NbApi().get_connector("ipam/vrf") -> VrfsC()
        """
        app, model = ami.path_to_attrs(path)
        return getattr(getattr(self, app), model)

    def connectors(self) -> GConnector:
        """Return generator of Connector instances ordered based on dependencies.
            Connectors to models with the lowest count of dependencies will be first.

        :return: Generator of Connector instances.
        """
        paths: LStr = helpers.dependency_ordered_paths()
        for path in paths:
            connector: Connector = self.connector_by_path(path)
            yield connector

    def copy(self, **kwargs) -> NbApi:
        """Create a duplicate of the object.

        :param kwargs: Keyword arguments to replace in the original object.
        :return: A copy of the current object.
        """
        base_c: BaseC = self._base_c
        params: DAny = {
            "host": base_c.host,
            "token": base_c.token,
            "scheme": base_c.scheme,
            "port": base_c.port,
            "verify": base_c.verify,
            "limit": base_c.limit,
            "url_length": base_c.url_length,
            "threads": base_c.threads,
            "interval": base_c.interval,
            "timeout": base_c.timeout,
            "max_retries": base_c.max_retries,
            "sleep": base_c.sleep,
            "strict": base_c.strict,
            "extended_get": base_c.extended_get,
            "loners": deepcopy(base_c.loners),
        }
        params.update(kwargs)
        return type(self)(**params)

    def version(self) -> str:
        """Get Netbox version.

        :return: Netbox version if version >= 3, otherwise an empty string.
        """
        status_d: DAny = self.status.get()
        version = NbParser(status_d).str("netbox-version")
        return version

    # ======================== connector methods =========================

    def graphql(self, query: str) -> Response:
        """Request data from Netbox GraphQL API.

        :param query: GraphQL query string.

        :return: Session response.

            - <Response [200]> - Request is successful or has syntax errors in the query.
        :rtype: Response
        """
        return self._base_c._post_graphql(query=query)

    def get(self, **kwargs) -> LDAny:
        """Request objects from Netbox using the app/model in the provided URL.

        :param kwargs: Parameters of the object, only the URL is required.

        :return: List of dictionaries containing Netbox objects.
        :rtype: List[dict]
        """
        url = str(kwargs.get("url") or "")
        app, model, id_ = ami.url_to_ami(url)
        connector: Connector = self.connector_by_path(f"{app}/{model}")

        method: Callable = getattr(connector, "get")
        params = {"id": id_} if id_ else {}
        return method(**params)

    def get_d(self, **kwargs) -> DAny:
        """Request single object from Netbox using the app/model in the provided URL.

        :param kwargs: Parameters of the object, only the URL with an ID is required.

        :return: Dictionary containing Netbox object.
        :rtype: dict
        """
        url = str(kwargs.get("url") or "")
        app, model, id_ = ami.url_to_ami(url)
        if not id_:
            raise ValueError("ID is required in the URL.")
        connector: Connector = self.connector_by_path(f"{app}/{model}")

        method: Callable = getattr(connector, "get")
        if objects := method(id=id_):
            return objects[0]
        return {}

    def create(self, **kwargs) -> Response:
        """Create an object in Netbox using the app/model in the provided URL.

        :param kwargs: Parameters for creating a new object.
        The `url` and `id` parameters will be ignored.

        :return: Session response.

            - <Response [201]> Object successfully created,
            - <Response [400]> Object already exists.
        :rtype: Response
        """
        url = str(kwargs.get("url") or "")
        app, model, _ = ami.url_to_ami(url)
        connector: Connector = self.connector_by_path(f"{app}/{model}")

        method: Callable = getattr(connector, "create")
        data: DAny = {k: v for k, v in kwargs.items() if k not in ["url", "id"]}
        return method(**data)

    def create_d(self, **kwargs) -> DAny:
        """Create an object in Netbox using the app/model in the provided URL.

        :param kwargs: Parameters for creating a new object.
        The `url` and `id` parameters will be ignored.

        :return: Data of newly created object.
        :rtype: dict
        """
        url = str(kwargs.get("url") or "")
        app, model, _ = ami.url_to_ami(url)
        connector: Connector = self.connector_by_path(f"{app}/{model}")

        data: DAny = {k: v for k, v in kwargs.items() if k not in ["url", "id"]}
        method: Callable = getattr(connector, "create_d")
        return method(**data)

    def delete(self, **kwargs) -> Response:
        """Delete an object from Netbox using the ID in the provided URL.

        :param kwargs: Parameters of the object to delete. Only the URL of the object is required.
        :return: Session response.

            - <Response [204]> Object successfully deleted,
            - <Response [404]> Object not found.
        :rtype: Response
        """
        url = str(kwargs.get("url") or "")
        app, model, idx = ami.url_to_ami(url)
        connector: Connector = self.connector_by_path(f"{app}/{model}")

        method: Callable = getattr(connector, "delete")
        return method(id=idx)

    # noinspection PyIncorrectDocstring
    def update(self, **kwargs) -> Response:
        """Update an object in Netbox using the app/model in the provided URL.

        :param id: Netbox object ID to update.
        :type id: int

        :param kwargs: Parameters to update an object in Netbox.

        :return: Session response.

            - <Response [200]> Object successfully updated,
            - <Response [400]> Invalid data.
        :rtype: Response
        """
        url = str(kwargs.get("url") or "")
        app, model, idx = ami.url_to_ami(url)
        connector: Connector = self.connector_by_path(f"{app}/{model}")

        method: Callable = getattr(connector, "update")
        data: DAny = {k: v for k, v in kwargs.items() if k not in ["url"]}
        data["id"] = idx
        return method(**data)
