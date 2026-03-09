"""Base Connector."""

from __future__ import annotations

import json

import netports
import requests
from requests import Session, Response, HTTPError

from nbforager import ami
from nbforager.types import LDAny, DLStr, DStr, DAny, LStr


class BaseC:
    """Base Connector."""

    def __init__(self, **kwargs):
        """Initialize BaseC.

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
        """
        self.host: str = _init_host(**kwargs)
        self.token: str = str(kwargs.get("token") or "")
        self.scheme: str = _init_scheme(**kwargs)
        self.port: int = _init_port(**kwargs)
        self.verify: bool = _init_verify(**kwargs)
        self.limit: int = int(kwargs.get("limit") or 1000)
        self.url_length = int(kwargs.get("url_length") or 2047)
        # Multithreading
        self.threads: int = _init_threads(**kwargs)
        self.interval: float = float(kwargs.get("interval") or 0.0)
        # Errors processing
        self.timeout: int = int(kwargs.get("timeout") or 60)
        self.max_retries: int = int(kwargs.get("max_retries") or 0)
        self.sleep: int = int(kwargs.get("sleep") or 10)
        self.strict: bool = bool(kwargs.get("strict"))
        # Settings
        self.extended_get: bool = bool(kwargs.get("extended_get"))
        self.loners: DLStr = dict(kwargs.get("loners") or {})
        # Session
        self._results: LDAny = []  # cache for received objects from Netbox
        self._session: Session = requests.session()

    def __repr__(self) -> str:
        """__repr__."""
        name = self.__class__.__name__
        return f"<{name}: {self.host}>"

    # ============================= property =============================

    @property
    def url_api(self) -> str:
        """Base URL without the application and model path."""
        url = f"{self.scheme}://{self.host}"

        # port
        port = 0
        if self.scheme == "http":
            if self.port != 80:
                port = self.port
        elif self.scheme == "https":
            if self.port != 443:
                port = self.port
        if port:
            url += f":{port}"

        return f"{url}/api/"

    @property
    def url_graphql(self) -> str:
        """Netbox URL to GraphQL API."""
        return self.url_api.removesuffix("/api/") + "/graphql/"

    # ============================= graphql ==============================

    def _post_graphql(self, query: str) -> Response:
        """Request data from Netbox GraphQL API.

        :param query: GraphQL query string.

        :return: Session response.

            - <Response [200]> - Request is successful or has syntax errors in the query.
        :rtype: Response
        """
        response: Response = self._session.post(
            url=self.url_graphql,
            data=json.dumps({"query": query}),
            headers=self._headers(),
            verify=self.verify,
            timeout=self.timeout,
        )
        return response

    def _graphql(self, path: str, fields: str, filters: str = "") -> LDAny:
        """Request data from Netbox GraphQL API.

        :param path: app/model path.
        :param fields: Fields to include in the query.
        :param filters: Parameters to filter Netbox objects.
        :return: List of dictionary objets.
        :raises HTTPError: Response status != 200 or contains ERROR messages.
        """
        query: str = _make_graphql_query(path=path, fields=fields, filters=filters)

        # response
        response: Response = self._post_graphql(query)
        response.raise_for_status()
        response.encoding = "utf-8"
        status_code = response.status_code
        url = response.url

        # json
        try:
            response_d: DAny = response.json()
        except Exception as ex:
            raise HTTPError(f"{status_code} Response is not JSON for {url=}") from ex

        # check api errors
        if "errors" in response_d:
            errors_d = response_d["errors"]
            msg: str = json.dumps(errors_d)
            msg = f"{status_code} Response errors: {msg} for {url=}"
            raise HTTPError(msg, response=response)
        if "data" not in response_d:
            raise HTTPError(f"{status_code} Response: 'data' is expected for {url=}")

        data: DAny = response_d["data"]
        if data is None:
            data = {}

        # TypeError
        if not isinstance(data, dict):
            msg = f"{status_code} Response: {dict} is expected for {url=}"
            raise HTTPError(msg, response=response)

        # List of dict
        keys: LStr = list(data)
        count = len(keys)
        if count != 1:
            msg = (
                f"{status_code} Response: {count=} of {keys=}. Only one key is expected for {url=}"
            )
            raise HTTPError(msg, response=response)
        for items in data.values():
            if isinstance(items, list):
                return items

        # TypeError
        raise HTTPError(f"200 Response: {list} is expected for {query=}")

    # ============================== others ==============================

    def _headers(self) -> DStr:
        """Session headers with token."""
        headers: DStr = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
        }
        return headers


# ============================= helpers ==============================


def _init_host(**kwargs) -> str:
    """Initialize Netbox host name."""
    host = str(kwargs.get("host") or "")
    if not host:
        raise ValueError("Host is required.")
    return host


def _init_port(**kwargs) -> int:
    """Initialize port."""
    if port := int(kwargs.get("port") or 0):
        if netports.check_port(port, strict=True):
            return port

    port = 443
    scheme = str(kwargs.get("scheme") or "").lower()
    if scheme == "http":
        port = 80
    return port


def _init_scheme(**kwargs) -> str:
    """Initialize scheme: https or http."""
    scheme = str(kwargs.get("scheme") or "").lower()
    expected = ["https", "http"]
    if scheme not in expected:
        raise ValueError(f"{scheme=}, {expected=}")
    return scheme


def _init_threads(**kwargs) -> int:
    """Initialize threads count, default 1."""
    threads = int(kwargs.get("threads") or 1)
    threads = max(threads, 1)
    return int(threads)


def _init_verify(**kwargs) -> bool:
    """Initialize verify. False - Requests will accept any TLS certificate."""
    verify = kwargs.get("verify")
    if verify is None:
        return True
    if not isinstance(verify, bool):
        raise TypeError(f"{verify=} {bool} is expected.")
    return verify


def _make_graphql_query(path: str, fields: str = "", filters: str = "") -> str:
    """Create GraphQL query and update with ``limit`` and ``offset``.

    :param path: app/model path.
    :param fields: Fields to include in the query.
    :param filters: Parameters to filter Netbox objects.
    :return: GraphQL query string.
    """
    query_l: LStr = []

    # model
    _, model = ami.path_to_attrs(path)
    model = ami.model_singular(model, splitter="_")
    model = f"{model}_list"
    query_l.append(model)

    # pagination, filters
    filters_l: LStr = []
    pagination_l: LStr = []
    if pagination_l:
        pagination = ", ".join(pagination_l)
        filters_l.append(f"pagination: {{ {pagination} }}")
    if filters:
        filters_l.append(f"filters: {filters}")
    if filters_l:
        filters_s = ", ".join(filters_l)
        query_l.append(f"( {filters_s} )")

    # fields
    if not fields:
        fields = "id"
    fields = f"{{ {fields} }}"
    query_l.append(fields)

    # build query
    query = " ".join(query_l)
    query = f"query {{ {query} }}"
    return query
