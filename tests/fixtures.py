"""Fixtures."""

import pytest
from requests import Response

from nbforager import nb_tree
from nbforager.nb_api import NbApi
from nbforager.nb_forager import NbForager
from nbforager.nb_tree import NbTree
from nbforager.types import DAny
from nbforager.parser.nb_parser import NbParser
from nbforager.parser.nb_value import NbValue
from tests.functions import full_tree

HOST = "nb"

@pytest.fixture
def api(params: DAny) -> NbApi:
    """Initialize NbApi with parameters."""
    return create_api(**params)


@pytest.fixture
def api_() -> NbApi:
    """Initialize NbApi without parameters."""
    return create_api(host=HOST)


def create_api(**kwargs) -> NbApi:
    """Initialize NbApi with parameters."""
    if "host" not in kwargs:
        kwargs["host"] = HOST

    return NbApi(**kwargs)


@pytest.fixture
def nbf(params: DAny) -> NbForager:
    """Initialize NbForager."""
    return NbForager(host=HOST, **params)


@pytest.fixture
def nbf_() -> NbForager:
    """Initialize NbForager without params."""
    return NbForager(host=HOST)

@pytest.fixture
def nbf_r() -> NbForager:
    """Initialize NbForager with NbForager.root data."""
    nbf_ = NbForager(host=HOST)
    tree: NbTree = full_tree()
    nb_tree.insert_tree(src=tree, dst=nbf_.root)
    return nbf_


@pytest.fixture
def nbf_t() -> NbForager:
    """Initialize NbForager."""
    nbf_ = NbForager(host=HOST)
    nb_tree.insert_tree(src=full_tree(), dst=nbf_.tree)
    return nbf_


@pytest.fixture
def nbp(params: DAny) -> NbParser:
    """Create NbValue instance based on the params."""
    return NbParser(**params)


@pytest.fixture
def nbv(params: DAny) -> NbValue:
    """Create NbValue instance based on the params."""
    return NbValue(**params)


def mock_session(status_code: int, content: str = ""):
    """Mock Session GET, POST, PATCH, set Response status_code and text.

    :param status_code: Response status code.
    :param content: Response content, json data as string.
    :return: Mocked function for Session method.
    """

    def mock(*args, **kwargs):
        _ = args, kwargs  # noqa
        response = Response()
        response.status_code = status_code
        response._content = content.encode()
        response.url = str(kwargs.get("url") or "")
        return response

    return mock
