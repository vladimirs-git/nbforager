"""Fixtures nbforager/foragers/forager.py."""
from typing import Tuple

import pytest

from nbforager.nb_forager import NbForager
from nbforager.types import LT2StrDAny, DAny


@pytest.fixture
def connector_results(nbf_: NbForager) -> Tuple[NbForager, LT2StrDAny]:
    """Fixture with common connector_results test data."""
    nb_termination: DAny = {"url": "circuit/circuit-terminations/1"}
    nbf_.api.circuits.circuit_terminations._results = [nb_termination]

    nb_vrf: DAny = {"url": "ipam/vrfs/1"}
    nbf_.api.ipam.vrfs._results = [nb_vrf]

    params_termination = ("circuits/circuit-terminations", {"id": [1, 2]})
    params_vrf = ("ipam/vrfs", {"id": [1, 2]})
    return nbf_, [params_termination, params_vrf]
