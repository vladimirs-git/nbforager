"""Tests nbforager.parser.nb_parser"""

import pytest

from nbforager.exceptions import NbParserError, NbVersionError
from nbforager.parser import nb_parser
from nbforager.parser.nb_parser import NbParser
from nbforager.types_ import LStr, DAny
from tests.parser import params__nb_parser as p


@pytest.fixture
def nbp(params: DAny) -> NbParser:
    """Create NbValue instance based on the params."""
    return NbParser(**params)


@pytest.mark.parametrize("keys, params, expected", [
    (["a"], {"data": {"a": None}, "strict": True}, None),
    (["a"], {"data": {"a": None}, "strict": False}, None),
    (["a"], {"data": {"a": "A"}, "strict": True}, "A"),
    (["a"], {"data": {"a": "A"}, "strict": False}, "A"),
    (["a"], {"data": {"a": 1}, "strict": True}, 1),
    (["a"], {"data": {"a": 1}, "strict": False}, 1),
    (["a"], {"data": {"a": {}}, "strict": True}, {}),
    (["a"], {"data": {"a": {}}, "strict": False}, {}),
    (["a"], {"data": {"a": {"k": "A"}}, "strict": True}, {"k": "A"}),
    (["a"], {"data": {"a": {"k": "A"}}, "strict": False}, {"k": "A"}),
    (["a", "b"], {"data": {"a": {"b": None}}, "strict": True}, None),
    (["a", "b"], {"data": {"a": {"b": None}}, "strict": False}, None),
    (["a", "b"], {"data": {"a": {"b": "A"}}, "strict": True}, "A"),
    (["a", "b"], {"data": {"a": {"b": "A"}}, "strict": False}, "A"),
    (["a", "b"], {"data": {"a": {"b": 1}}, "strict": True}, 1),
    (["a", "b"], {"data": {"a": {"b": 1}}, "strict": False}, 1),
    (["a", "b"], {"data": {"a": {"b": {"k": "B"}}}, "strict": True}, {"k": "B"}),
    (["a", "b"], {"data": {"a": {"b": {"k": "B"}}}, "strict": False}, {"k": "B"}),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": None}}}, "strict": True}, None),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": None}}}, "strict": False}, None),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": "A"}}}, "strict": True}, "A"),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": "A"}}}, "strict": False}, "A"),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": 1}}}, "strict": True}, 1),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": 1}}}, "strict": False}, 1),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": {}}}}, "strict": True}, {}),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": {}}}}, "strict": False}, {}),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": {"k": "C"}}}}, "strict": True}, {"k": "C"}),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": {"k": "C"}}}}, "strict": False}, {"k": "C"}),
    # list
    (["a", 0, "b"], {"data": {"a": [{"b": None}]}, "strict": False}, None),
    (["a", 0, "b"], {"data": {"a": [{"b": None}]}, "strict": True}, None),
    (["a", 0, "b"], {"data": {"a": [{"b": "B"}]}, "strict": False}, "B"),
    (["a", 0, "b"], {"data": {"a": [{"b": "B"}]}, "strict": True}, "B"),
    (["a", 0, "b"], {"data": {"a": {"b": "B"}}, "strict": False}, None),
    (["a", 0, "b"], {"data": {"a": {"b": "B"}}, "strict": True}, None),
])
def test__any(nbp, keys: LStr, params, expected):
    """NbParser.any()."""
    actual = nbp.any(*keys)
    assert actual == expected


@pytest.mark.parametrize("keys, params, expected", [
    (["a"], {"data": {"a": None}, "strict": True}, NbParserError),
    (["a"], {"data": {"a": None}, "strict": False}, False),
    (["a"], {"data": {"a": 1}, "strict": True}, NbParserError),
    (["a"], {"data": {"a": 1}, "strict": False}, False),
    (["a"], {"data": {"a": True}, "strict": True}, True),
    (["a"], {"data": {"a": True}, "strict": False}, True),
    (["a"], {"data": {"a": False}, "strict": True}, False),
    (["a"], {"data": {"a": False}, "strict": False}, False),
    (["a", "b"], {"data": {"a": {"b": True}}, "strict": True}, True),
    (["a", "b"], {"data": {"a": {"b": True}}, "strict": False}, True),
    (["a", "b"], {"data": {"a": {"b": None}}, "strict": True}, NbParserError),
    (["a", "b"], {"data": {"a": {"b": None}}, "strict": False}, False),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": True}}}, "strict": True}, True),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": True}}}, "strict": False}, True),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": None}}}, "strict": True}, NbParserError),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": None}}}, "strict": False}, False),
    # list
    (["a", 0, "b"], {"data": {"a": [{"b": None}]}, "strict": False}, False),
    (["a", 0, "b"], {"data": {"a": [{"b": None}]}, "strict": True}, NbParserError),
    (["a", 0, "b"], {"data": {"a": [{"b": True}]}, "strict": False}, True),
    (["a", 0, "b"], {"data": {"a": [{"b": True}]}, "strict": True}, True),
    (["a", 0, "b"], {"data": {"a": {"b": True}}, "strict": False}, False),
    (["a", 0, "b"], {"data": {"a": {"b": True}}, "strict": True}, NbParserError),
])
def test__bool(nbp, keys: LStr, params, expected):
    """NbParser.bool()."""
    if isinstance(expected, bool):
        actual = nbp.bool(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbp.bool(*keys)


@pytest.mark.parametrize("keys, params, expected", [
    # version
    (["site", "tenant", "bool"], {"version": "4.1", "data": p.V3_PREFIX}, True),
    (["site", "tenant", "bool"], {"version": "4.2", "data": p.V3_PREFIX}, NbVersionError),
    (["scope", "tenant", "bool"], {"version": "4.1", "data": p.V4_PREFIX}, True),
    (["scope", "tenant", "bool"], {"version": "4.2", "data": p.V4_PREFIX}, True),
    # ipam/prefixes.site bool
    (["site", "tenant", "bool"], {"data": p.V3_PREFIX}, NbVersionError),
    (["site", "tenant", "bool"], {"data": p.V4_PREFIX}, NbVersionError),
    (["scope", "bool"], {"data": p.V3_PREFIX}, False),
    (["scope", "bool"], {"data": p.V4_PREFIX}, True),
])
def test__bool__deprecated(nbp, keys, params, expected):
    """NbParser.bool() site v4.2."""
    if isinstance(expected, bool):
        actual = nbp.bool(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbp.bool(*keys)


@pytest.mark.parametrize("keys, params, expected", [
    (["a"], {"data": {"a": None}, "strict": True}, NbParserError),
    (["a"], {"data": {"a": None}, "strict": False}, {}),
    (["a"], {"data": {"a": 1}, "strict": True}, NbParserError),
    (["a"], {"data": {"a": 1}, "strict": False}, {}),
    (["a"], {"data": {"a": {}}, "strict": True}, {}),
    (["a"], {"data": {"a": {}}, "strict": False}, {}),
    (["a"], {"data": {"a": {"k": "A"}}, "strict": True}, {"k": "A"}),
    (["a"], {"data": {"a": {"k": "A"}}, "strict": False}, {"k": "A"}),
    (["a", "b"], {"data": {"a": {"b": {"k": "B"}}}, "strict": True}, {"k": "B"}),
    (["a", "b"], {"data": {"a": {"b": {"k": "B"}}}, "strict": False}, {"k": "B"}),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": {"k": "C"}}}}, "strict": True}, {"k": "C"}),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": {"k": "C"}}}}, "strict": False}, {"k": "C"}),
    # list
    (["a", 0, "b"], {"data": {"a": [{"b": None}]}, "strict": False}, {}),
    (["a", 0, "b"], {"data": {"a": [{"b": None}]}, "strict": True}, NbParserError),
    (["a", 0, "b"], {"data": {"a": [{"b": {"k": "B"}}]}, "strict": False}, {"k": "B"}),
    (["a", 0, "b"], {"data": {"a": [{"b": {"k": "B"}}]}, "strict": True}, {"k": "B"}),
    (["a", 0, "b"], {"data": {"a": {"b": {"k": "B"}}}, "strict": False}, {}),
    (["a", 0, "b"], {"data": {"a": {"b": {"k": "B"}}}, "strict": True}, NbParserError),
])
def test__dict(nbp, keys: LStr, params, expected):
    """NbParser.dict()."""
    if isinstance(expected, dict):
        actual = nbp.dict(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbp.dict(*keys)


@pytest.mark.parametrize("keys, params, expected", [
    # ipam/prefixes.site.tenant v3.5
    (["site", "tenant"], {"data": p.V3_PREFIX}, NbVersionError),
    (["site", "tenant"], {"data": p.V4_PREFIX}, NbVersionError),
    (["site", "tenant"], {"version": "4.1", "data": p.V3_PREFIX}, p.TENANT),
    (["site", "tenant"], {"version": "4.1", "data": p.V4_PREFIX}, {}),
    (["site", "tenant"], {"version": "4.2", "data": p.V3_PREFIX}, NbVersionError),
    (["site", "tenant"], {"version": "4.2", "data": p.V4_PREFIX}, NbVersionError),
    # ipam/prefixes.scope.tenant v3.5
    (["scope", "tenant"], {"data": p.V3_PREFIX}, {}),
    (["scope", "tenant"], {"data": p.V4_PREFIX}, p.TENANT),
    (["scope", "tenant"], {"version": "4.1", "data": p.V3_PREFIX}, {}),
    (["scope", "tenant"], {"version": "4.1", "data": p.V4_PREFIX}, p.TENANT),
    (["scope", "tenant"], {"version": "4.2", "data": p.V3_PREFIX}, {}),
    (["scope", "tenant"], {"version": "4.2", "data": p.V4_PREFIX}, p.TENANT),

    # extras/custom-fields.ui_visibility v3.5
    (["ui_visibility"], {"data": p.V3_CUSTOM_FIELD}, NbVersionError),
    (["ui_visibility"], {"data": p.V4_CUSTOM_FIELD}, NbVersionError),
    (["ui_visibility"], {"version": "4.1", "data": p.V3_CUSTOM_FIELD}, p.UI_VISIBILITY),
    (["ui_visibility"], {"version": "4.1", "data": p.V4_CUSTOM_FIELD}, {}),
    (["ui_visibility"], {"version": "4.2", "data": p.V3_CUSTOM_FIELD}, NbVersionError),
    (["ui_visibility"], {"version": "4.2", "data": p.V4_CUSTOM_FIELD}, NbVersionError),
    # extras/custom-fields.ui_visible v4.2
    (["ui_visible"], {"data": p.V3_CUSTOM_FIELD}, {}),
    (["ui_visible"], {"data": p.V4_CUSTOM_FIELD}, p.UI_VISIBLE),
    (["ui_visible"], {"version": "4.1", "data": p.V3_CUSTOM_FIELD}, {}),
    (["ui_visible"], {"version": "4.1", "data": p.V4_CUSTOM_FIELD}, p.UI_VISIBLE),
    (["ui_visible"], {"version": "4.2", "data": p.V3_CUSTOM_FIELD}, {}),
    (["ui_visible"], {"version": "4.2", "data": p.V4_CUSTOM_FIELD}, p.UI_VISIBLE),
])
def test__dict__deprecated(caplog, nbp, keys: LStr, params, expected):
    """NbParser.dict() site v4.2."""
    if isinstance(expected, dict):
        actual = nbp.dict(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbp.dict(*keys)



@pytest.mark.parametrize("keys, params, expected", [
    (["a"], {"data": {"a": 1.0}, "strict": True}, 1.0),
    (["a"], {"data": {"a": 1.0}, "strict": False}, 1.0),
    (["a"], {"data": {"a": "1.0"}, "strict": True}, 1.0),
    (["a"], {"data": {"a": "1.0"}, "strict": False}, 1.0),
    (["a"], {"data": {"a": "1.00"}, "strict": True}, 1.0),
    (["a"], {"data": {"a": "1.00"}, "strict": False}, 1.0),
    (["a"], {"data": {"a": 0.0}, "strict": True}, 0.0),
    (["a"], {"data": {"a": 0.0}, "strict": False}, 0.0),
    (["a"], {"data": {"a": "0.0"}, "strict": True}, 0.0),
    (["a"], {"data": {"a": "0.0"}, "strict": False}, 0.0),
    (["a", "b"], {"data": {"a": {"b": 1.0}}, "strict": True}, 1.0),
    (["a", "b"], {"data": {"a": {"b": 1.0}}, "strict": False}, 1.0),
    (["a", "b"], {"data": {"a": {"b": None}}, "strict": True}, NbParserError),
    (["a", "b"], {"data": {"a": {"b": None}}, "strict": False}, 0.0),
    (["a", "b"], {"data": {"a": {"b": "1.0"}}, "strict": True}, 1.0),
    (["a", "b"], {"data": {"a": {"b": "1.0"}}, "strict": False}, 1.0),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": 1.0}}}, "strict": True}, 1.0),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": "1.0"}}}, "strict": True}, 1.0),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": None}}}, "strict": True}, NbParserError),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": None}}}, "strict": False}, 0.0),
    (["a"], {"data": None, "strict": True}, NbParserError),
    (["a"], {"data": None, "strict": False}, 0.0),
    # list
    (["a", 0, "b"], {"data": {"a": [{"b": None}]}, "strict": False}, 0.0),
    (["a", 0, "b"], {"data": {"a": [{"b": None}]}, "strict": True}, NbParserError),
    (["a", 0, "b"], {"data": {"a": [{"b": 1.0}]}, "strict": False}, 1.0),
    (["a", 0, "b"], {"data": {"a": [{"b": 1.0}]}, "strict": True}, 1.0),
    (["a", 0, "b"], {"data": {"a": {"b": 1.0}}, "strict": False}, 0.0),
    (["a", 0, "b"], {"data": {"a": {"b": 1.0}}, "strict": True}, NbParserError),
])
def test__float(nbp, keys: LStr, params, expected):
    """NbParser.float()."""
    if isinstance(expected, float):
        actual = nbp.float(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbp.float(*keys)


@pytest.mark.parametrize("keys, params, expected", [
    (["id"], {"data": {"id": "1"}, "strict": True}, 1),
    (["id"], {"data": {"id": "1"}, "strict": False}, 1),
    (["id"], {"data": {"id": 0}, "strict": True}, 0),
    (["id"], {"data": {"id": 0}, "strict": False}, 0),
    (["id"], {"data": {"id": "0"}, "strict": True}, 0),
    (["id"], {"data": {"id": "0"}, "strict": False}, 0),
    (["a", "b"], {"data": {"a": {"b": 1}}, "strict": True}, 1),
    (["a", "b"], {"data": {"a": {"b": 1}}, "strict": False}, 1),
    (["a", "b"], {"data": {"a": {"b": None}}, "strict": True}, NbParserError),
    (["a", "b"], {"data": {"a": {"b": None}}, "strict": False}, 0),
    (["a", "b"], {"data": {"a": {"b": "1"}}, "strict": True}, 1),
    (["a", "b"], {"data": {"a": {"b": "1"}}, "strict": False}, 1),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": 3}}}, "strict": True}, 3),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": "3"}}}, "strict": True}, 3),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": None}}}, "strict": True}, NbParserError),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": None}}}, "strict": False}, 0),
    (["id"], {"data": None, "strict": True}, NbParserError),
    (["id"], {"data": None, "strict": False}, 0),
    # list
    (["a", 0, "b"], {"data": {"a": [{"b": None}]}, "strict": False}, 0),
    (["a", 0, "b"], {"data": {"a": [{"b": None}]}, "strict": True}, NbParserError),
    (["a", 0, "b"], {"data": {"a": [{"b": 1}]}, "strict": False}, 1),
    (["a", 0, "b"], {"data": {"a": [{"b": 1}]}, "strict": True}, 1),
    (["a", 0, "b"], {"data": {"a": {"b": 1}}, "strict": False}, 0),
    (["a", 0, "b"], {"data": {"a": {"b": 1}}, "strict": True}, NbParserError),
])
def test__int(nbp, keys: LStr, params, expected):
    """NbParser.int()."""
    if isinstance(expected, int):
        actual = nbp.int(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbp.int(*keys)


@pytest.mark.parametrize("keys, params, expected", [
    # circuits/circuit-terminations.provider_network.id v3.5
    (["provider_network", "id"], {"data": p.V3_C_TERMINATION}, NbVersionError),
    (["provider_network", "id"], {"data": p.V4_C_TERMINATION}, NbVersionError),
    (["provider_network", "id"], {"version": "4.1", "data": p.V3_C_TERMINATION}, p.PN1),
    (["provider_network", "id"], {"version": "4.1", "data": p.V4_C_TERMINATION}, 0),
    (["provider_network", "id"], {"version": "4.2", "data": p.V3_C_TERMINATION}, NbVersionError),
    (["provider_network", "id"], {"version": "4.2", "data": p.V4_C_TERMINATION}, NbVersionError),

    # circuits/circuit-terminations.site.id v3.5
    (["site", "id"], {"data": p.V3_C_TERMINATION}, NbVersionError),
    (["site", "id"], {"data": p.V4_C_TERMINATION}, NbVersionError),
    (["site", "id"], {"version": "4.1", "data": p.V3_C_TERMINATION}, p.S1),
    (["site", "id"], {"version": "4.1", "data": p.V4_C_TERMINATION}, 0),
    (["site", "id"], {"version": "4.2", "data": p.V3_C_TERMINATION}, NbVersionError),
    (["site", "id"], {"version": "4.2", "data": p.V4_C_TERMINATION}, NbVersionError),
    # circuits/circuit-terminations.termination.id v4.2
    (["termination", "id"], {"data": p.V3_C_TERMINATION}, 0),
    (["termination", "id"], {"data": p.V4_C_TERMINATION}, p.S1),
    (["termination", "id"], {"version": "4.1", "data": p.V3_C_TERMINATION}, 0),
    (["termination", "id"], {"version": "4.1", "data": p.V4_C_TERMINATION}, p.S1),
    (["termination", "id"], {"version": "4.2", "data": p.V3_C_TERMINATION}, 0),
    (["termination", "id"], {"version": "4.2", "data": p.V4_C_TERMINATION}, p.S1),

    # dcim/devices.primary_ip4.family v3.5
    (["primary_ip4", "family"], {"data": p.V3_DEVICE}, NbVersionError),
    (["primary_ip4", "family"], {"data": p.V4_DEVICE}, NbVersionError),
    (["primary_ip4", "family"], {"version": "4.1", "data": p.V3_DEVICE}, 4),
    (["primary_ip4", "family"], {"version": "4.1", "data": p.V4_DEVICE}, 0),
    (["primary_ip4", "family"], {"version": "4.2", "data": p.V3_DEVICE}, NbVersionError),
    (["primary_ip4", "family"], {"version": "4.2", "data": p.V4_DEVICE}, NbVersionError),
    # dcim/devices.primary_ip4.family.value v4.2
    (["primary_ip4", "family", "value"], {"data": p.V3_DEVICE}, 0),
    (["primary_ip4", "family", "value"], {"data": p.V4_DEVICE}, 4),
    (["primary_ip4", "family", "value"], {"version": "4.1", "data": p.V3_DEVICE}, 0),
    (["primary_ip4", "family", "value"], {"version": "4.1", "data": p.V4_DEVICE}, 4),
    (["primary_ip4", "family", "value"], {"version": "4.2", "data": p.V3_DEVICE}, 0),
    (["primary_ip4", "family", "value"], {"version": "4.2", "data": p.V4_DEVICE}, 4),

    # dcim/inventory-items.component.cable v3.5
    (["component", "cable"], {"data": p.V3_INV_ITEM}, NbVersionError),  # return <int>
    (["component", "cable"], {"data": p.V4_INV_ITEM}, NbVersionError),  # return <dict>
    (["component", "cable"], {"version": "4.1", "data": p.V3_INV_ITEM}, p.CB1),
    (["component", "cable"], {"version": "4.1", "data": p.V4_INV_ITEM}, 0),
    (["component", "cable"], {"version": "4.2", "data": p.V3_INV_ITEM}, NbVersionError),
    (["component", "cable"], {"version": "4.2", "data": p.V4_INV_ITEM}, NbVersionError),
    # dcim/inventory-items.component.cable.id v4.2
    (["component", "cable", "id"], {"data": p.V3_INV_ITEM}, 0),  # return <int>
    (["component", "cable", "id"], {"data": p.V4_INV_ITEM}, p.CB1),  # return <dict>
    (["component", "cable", "id"], {"version": "4.1", "data": p.V3_INV_ITEM}, 0),
    (["component", "cable", "id"], {"version": "4.1", "data": p.V4_INV_ITEM}, p.CB1),
    (["component", "cable", "id"], {"version": "4.2", "data": p.V3_INV_ITEM}, 0),
    (["component", "cable", "id"], {"version": "4.2", "data": p.V4_INV_ITEM}, p.CB1),

    # dcim/power-outlets.power_port.cable v3.5
    (["power_port", "cable"], {"data": p.V3_POWER_OUTLET}, NbVersionError),  # return <int>
    (["power_port", "cable"], {"data": p.V4_POWER_OUTLET}, NbVersionError),  # return <dict>
    (["power_port", "cable"], {"version": "4.1", "data": p.V3_POWER_OUTLET}, p.PP1),
    (["power_port", "cable"], {"version": "4.1", "data": p.V4_POWER_OUTLET}, 0),
    (["power_port", "cable"], {"version": "4.2", "data": p.V3_POWER_OUTLET}, NbVersionError),
    (["power_port", "cable"], {"version": "4.2", "data": p.V4_POWER_OUTLET}, NbVersionError),
    # dcim/power-outlets.power_port.cable.id v4.2
    (["power_port", "cable", "id"], {"data": p.V3_POWER_OUTLET}, 0),  # return <int>
    (["power_port", "cable", "id"], {"data": p.V4_POWER_OUTLET}, p.CB1),  # return <dict>
    (["power_port", "cable", "id"], {"version": "4.1", "data": p.V3_POWER_OUTLET}, 0),
    (["power_port", "cable", "id"], {"version": "4.1", "data": p.V4_POWER_OUTLET}, p.CB1),
    (["power_port", "cable", "id"], {"version": "4.2", "data": p.V3_POWER_OUTLET}, 0),
    (["power_port", "cable", "id"], {"version": "4.2", "data": p.V4_POWER_OUTLET}, p.CB1),

    # dcim/cable-terminations.termination.cable v3.5
    (["termination", "cable"], {"data": p.V3_CB_TERMINATION}, NbVersionError),  # return <int>
    (["termination", "cable"], {"data": p.V4_CB_TERMINATION}, NbVersionError),  # return <dict>
    (["termination", "cable"], {"version": "4.1", "data": p.V3_CB_TERMINATION}, p.CB1),
    (["termination", "cable"], {"version": "4.1", "data": p.V4_CB_TERMINATION}, 0),
    (["termination", "cable"], {"version": "4.2", "data": p.V3_CB_TERMINATION}, NbVersionError),
    (["termination", "cable"], {"version": "4.2", "data": p.V4_CB_TERMINATION}, NbVersionError),
    # dcim/power-outlets.termination.cable.id v4.2
    (["termination", "cable", "id"], {"data": p.V3_CB_TERMINATION}, 0),  # return <int>
    (["termination", "cable", "id"], {"data": p.V4_CB_TERMINATION}, p.CB1),  # return <dict>
    (["termination", "cable", "id"], {"version": "4.1", "data": p.V3_CB_TERMINATION}, 0),
    (["termination", "cable", "id"], {"version": "4.1", "data": p.V4_CB_TERMINATION}, p.CB1),
    (["termination", "cable", "id"], {"version": "4.2", "data": p.V3_CB_TERMINATION}, 0),
    (["termination", "cable", "id"], {"version": "4.2", "data": p.V4_CB_TERMINATION}, p.CB1),

    # ipam/ip-addresses.assigned_object.cable v3.5
    (["assigned_object", "cable"], {"data": p.V3_IP_ADDRESS}, NbVersionError),  # return <int>
    (["assigned_object", "cable"], {"data": p.V4_IP_ADDRESS}, NbVersionError),  # return <dict>
    (["assigned_object", "cable"], {"version": "4.1", "data": p.V3_IP_ADDRESS}, p.CB1),
    (["assigned_object", "cable"], {"version": "4.1", "data": p.V4_IP_ADDRESS}, 0),
    (["assigned_object", "cable"], {"version": "4.2", "data": p.V3_IP_ADDRESS}, NbVersionError),
    (["assigned_object", "cable"], {"version": "4.2", "data": p.V4_IP_ADDRESS}, NbVersionError),
    # ipam/ip-addresses.assigned_object.cable.id v4.2
    (["assigned_object", "cable", "id"], {"data": p.V3_IP_ADDRESS}, 0),  # return <int>
    (["assigned_object", "cable", "id"], {"data": p.V4_IP_ADDRESS}, p.CB1),  # return <dict>
    (["assigned_object", "cable", "id"], {"version": "4.1", "data": p.V3_IP_ADDRESS}, 0),
    (["assigned_object", "cable", "id"], {"version": "4.1", "data": p.V4_IP_ADDRESS}, p.CB1),
    (["assigned_object", "cable", "id"], {"version": "4.2", "data": p.V3_IP_ADDRESS}, 0),
    (["assigned_object", "cable", "id"], {"version": "4.2", "data": p.V4_IP_ADDRESS}, p.CB1),

    # ipam/prefixes.site.id v3.5
    (["site", "id"], {"data": p.V3_PREFIX}, NbVersionError),
    (["site", "id"], {"version": "4.1", "data": p.V3_PREFIX}, p.S1),
    (["site", "id"], {"version": "4.2", "data": p.V4_PREFIX}, NbVersionError),
    # ipam/prefixes.scope.id v4.2
    (["scope", "id"], {"data": p.V3_PREFIX}, 0),
    (["scope", "id"], {"version": "4.1", "data": p.V3_PREFIX}, 0),
    (["scope", "id"], {"version": "4.2", "data": p.V4_PREFIX}, p.S1),
    # ipam/prefixes id
    (["site", "id"], {"data": p.V3_PREFIX}, NbVersionError),
    (["scope", "id"], {"data": p.V4_PREFIX}, p.S1),
    (["site", "tenant", "id"], {"data": p.V3_PREFIX}, NbVersionError),
    (["scope", "tenant", "id"], {"data": p.V4_PREFIX}, p.P2),

    # ipam/vlan-groups.min_vid v3.5
    (["min_vid"], {"data": p.V3_VLAN_GROUP}, NbVersionError),
    (["min_vid"], {"data": p.V4_VLAN_GROUP}, NbVersionError),
    (["min_vid"], {"version": "4.1", "data": p.V3_VLAN_GROUP}, 1),
    (["min_vid"], {"version": "4.1", "data": p.V4_VLAN_GROUP}, 0),
    (["min_vid"], {"version": "4.2", "data": p.V3_VLAN_GROUP}, NbVersionError),
    (["min_vid"], {"version": "4.2", "data": p.V4_VLAN_GROUP}, NbVersionError),
    # ipam/vlan-groups.vid_ranges v4.2
    (["vid_ranges"], {"data": p.V3_VLAN_GROUP}, 0),
    (["vid_ranges"], {"data": p.V4_VLAN_GROUP}, 0),
    (["vid_ranges"], {"version": "4.1", "data": p.V3_VLAN_GROUP}, 0),
    (["vid_ranges"], {"version": "4.1", "data": p.V4_VLAN_GROUP}, 0),
    (["vid_ranges"], {"version": "4.2", "data": p.V3_VLAN_GROUP}, 0),
    (["vid_ranges"], {"version": "4.2", "data": p.V4_VLAN_GROUP}, 0),

    # extras/object-changes.action.id v3.5
    (["id"], {"data": p.V3_O_CHANGE}, NbVersionError),
    (["id"], {"data": p.V4_O_CHANGE}, p.OC1),
    (["id"], {"version": "4.1", "data": p.V3_O_CHANGE}, p.OC1),
    (["id"], {"version": "4.1", "data": p.V4_O_CHANGE}, p.OC1),
    (["id"], {"version": "4.2", "data": p.V3_O_CHANGE}, NbVersionError),
    (["id"], {"version": "4.2", "data": p.V4_O_CHANGE}, p.OC1),
    # core/object-changes.action.id v4.2
    (["id"], {"data": p.V3_O_CHANGE}, NbVersionError),
    (["id"], {"data": p.V4_O_CHANGE}, p.OC1),
    (["id"], {"version": "4.1", "data": p.V3_O_CHANGE}, p.OC1),
    (["id"], {"version": "4.1", "data": p.V4_O_CHANGE}, p.OC1),
    (["id"], {"version": "4.2", "data": p.V3_O_CHANGE}, NbVersionError),
    (["id"], {"version": "4.2", "data": p.V4_O_CHANGE}, p.OC1),
])
def test__int__deprecated(caplog, nbp, keys: LStr, params, expected):
    """NbParser.int() site v4.2."""
    if isinstance(expected, int):
        actual = nbp.int(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbp.int(*keys)


@pytest.mark.parametrize("keys, params, expected", [
    (["a"], {"data": {"a": None}, "strict": True}, NbParserError),
    (["a"], {"data": {"a": None}, "strict": False}, []),
    (["a"], {"data": {"a": 1}, "strict": True}, NbParserError),
    (["a"], {"data": {"a": 1}, "strict": False}, []),
    (["a"], {"data": {"a": ["A"]}, "strict": True}, ["A"]),
    (["a"], {"data": {"a": ["A"]}, "strict": False}, ["A"]),
    (["a"], {"data": {"a": [""]}, "strict": True}, [""]),
    (["a"], {"data": {"a": [""]}, "strict": False}, [""]),
    (["a", "b"], {"data": {"a": {"b": ["B"]}}, "strict": True}, ["B"]),
    (["a", "b"], {"data": {"a": {"b": ["B"]}}, "strict": False}, ["B"]),
    (["a", "b"], {"data": {"a": {"b": None}}, "strict": True}, NbParserError),
    (["a", "b"], {"data": {"a": {"b": None}}, "strict": False}, []),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": ["C"]}}}, "strict": True}, ["C"]),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": ["C"]}}}, "strict": False}, ["C"]),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": None}}}, "strict": True}, NbParserError),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": None}}}, "strict": False}, []),
    # list
    (["a", 0, "b"], {"data": {"a": [{"b": "B"}]}, "strict": False}, []),
    (["a", 0, "b"], {"data": {"a": [{"b": "B"}]}, "strict": True}, NbParserError),
    (["a", 0, "b"], {"data": {"a": [{"b": ["B"]}]}, "strict": False}, ["B"]),
    (["a", 0, "b"], {"data": {"a": [{"b": ["B"]}]}, "strict": True}, ["B"]),
    (["a", 0, "b"], {"data": {"a": {"b": ["B"]}}, "strict": False}, []),
    (["a", 0, "b"], {"data": {"a": {"b": ["B"]}}, "strict": True}, NbParserError),
])
def test__list(nbp, keys: LStr, params, expected):
    """NbParser.list()."""
    if isinstance(expected, list):
        actual = nbp.list(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbp.list(*keys)


@pytest.mark.parametrize("keys, params, expected", [
    # ipam/prefixes.site.tags v3.5
    (["site", "tags"], {"data": p.V3_PREFIX}, NbVersionError),
    (["site", "tags"], {"data": p.V4_PREFIX}, NbVersionError),
    (["site", "tags"], {"version": "4.1", "data": p.V3_PREFIX}, [p.TAG_D]),
    (["site", "tags"], {"version": "4.1", "data": p.V4_PREFIX}, []),
    (["site", "tags"], {"version": "4.2", "data": p.V3_PREFIX}, NbVersionError),
    (["site", "tags"], {"version": "4.2", "data": p.V4_PREFIX}, NbVersionError),
    # ipam/prefixes.scope.tags v3.5
    (["scope", "tags"], {"data": p.V3_PREFIX}, []),
    (["scope", "tags"], {"data": p.V4_PREFIX}, [p.TAG_D]),
    (["scope", "tags"], {"version": "4.1", "data": p.V3_PREFIX}, []),
    (["scope", "tags"], {"version": "4.1", "data": p.V4_PREFIX}, [p.TAG_D]),
    (["scope", "tags"], {"version": "4.2", "data": p.V3_PREFIX}, []),
    (["scope", "tags"], {"version": "4.2", "data": p.V4_PREFIX}, [p.TAG_D]),

    # extras/custom-fields.content_types v3.5
    (["content_types"], {"data": p.V3_CUSTOM_FIELD}, NbVersionError),
    (["content_types"], {"data": p.V4_CUSTOM_FIELD}, NbVersionError),
    (["content_types"], {"version": "4.1", "data": p.V3_CUSTOM_FIELD}, ["ipam.vlan"]),
    (["content_types"], {"version": "4.1", "data": p.V4_CUSTOM_FIELD}, []),
    (["content_types"], {"version": "4.2", "data": p.V3_CUSTOM_FIELD}, NbVersionError),
    (["content_types"], {"version": "4.2", "data": p.V4_CUSTOM_FIELD}, NbVersionError),
    # extras/custom-fields.object_types v4.2
    (["object_types"], {"data": p.V3_CUSTOM_FIELD}, []),
    (["object_types"], {"data": p.V4_CUSTOM_FIELD}, ["ipam.vlan"]),
    (["object_types"], {"version": "4.1", "data": p.V3_CUSTOM_FIELD}, []),
    (["object_types"], {"version": "4.1", "data": p.V4_CUSTOM_FIELD}, ["ipam.vlan"]),
    (["object_types"], {"version": "4.2", "data": p.V3_CUSTOM_FIELD}, []),
    (["object_types"], {"version": "4.2", "data": p.V4_CUSTOM_FIELD}, ["ipam.vlan"]),

    # extras/custom-fields.choices v3.5
    (["choices"], {"data": p.V3_CUSTOM_FIELD}, NbVersionError),
    (["choices"], {"data": p.V4_CUSTOM_FIELD}, NbVersionError),
    (["choices"], {"version": "4.1", "data": p.V3_CUSTOM_FIELD}, p.CHOICES),
    (["choices"], {"version": "4.1", "data": p.V4_CUSTOM_FIELD}, []),
    (["choices"], {"version": "4.2", "data": p.V3_CUSTOM_FIELD}, NbVersionError),
    (["choices"], {"version": "4.2", "data": p.V4_CUSTOM_FIELD}, NbVersionError),
    # extras/custom-fields.choice_set v4.2
    (["choice_set"], {"data": p.V3_CUSTOM_FIELD}, []),
    (["choice_set"], {"data": p.V4_CUSTOM_FIELD}, []),
    (["choice_set"], {"version": "4.1", "data": p.V3_CUSTOM_FIELD}, []),
    (["choice_set"], {"version": "4.1", "data": p.V4_CUSTOM_FIELD}, []),
    (["choice_set"], {"version": "4.2", "data": p.V3_CUSTOM_FIELD}, []),
    (["choice_set"], {"version": "4.2", "data": p.V4_CUSTOM_FIELD}, []),

])
def test__list__deprecated(caplog, nbp, keys: LStr, params, expected):
    """NbParser.list() site v4.2."""
    if isinstance(expected, list):
        actual = nbp.list(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbp.list(*keys)


@pytest.mark.parametrize("keys, params, expected", [
    (["a"], {"data": {"a": None}, "strict": True}, NbParserError),
    (["a"], {"data": {"a": None}, "strict": False}, ""),
    (["a"], {"data": {"a": 1}, "strict": True}, NbParserError),
    (["a"], {"data": {"a": 1}, "strict": False}, ""),
    (["a"], {"data": {"a": "A"}, "strict": True}, "A"),
    (["a"], {"data": {"a": "A"}, "strict": False}, "A"),
    (["a"], {"data": {"a": ""}, "strict": True}, ""),
    (["a"], {"data": {"a": ""}, "strict": False}, ""),
    (["a", "b"], {"data": {"a": {"b": "B"}}, "strict": True}, "B"),
    (["a", "b"], {"data": {"a": {"b": "B"}}, "strict": False}, "B"),
    (["a", "b"], {"data": {"a": {"b": None}}, "strict": True}, NbParserError),
    (["a", "b"], {"data": {"a": {"b": None}}, "strict": False}, ""),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": "C"}}}, "strict": True}, "C"),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": "C"}}}, "strict": False}, "C"),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": None}}}, "strict": True}, NbParserError),
    (["a", "b", "c"], {"data": {"a": {"b": {"c": None}}}, "strict": False}, ""),
    # list
    (["a", 0, "b"], {"data": {"a": [{"b": None}]}, "strict": False}, ""),
    (["a", 0, "b"], {"data": {"a": [{"b": None}]}, "strict": True}, NbParserError),
    (["a", 0, "b"], {"data": {"a": [{"b": "B"}]}, "strict": False}, "B"),
    (["a", 0, "b"], {"data": {"a": [{"b": "B"}]}, "strict": True}, "B"),
    (["a", 0, "b"], {"data": {"a": {"b": "B"}}, "strict": False}, ""),
    (["a", 0, "b"], {"data": {"a": {"b": "B"}}, "strict": True}, NbParserError),
])
def test__str(nbp, keys: LStr, params, expected):
    """NbParser.str()."""
    if isinstance(expected, str):
        actual = nbp.str(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbp.str(*keys)


@pytest.mark.parametrize("keys, params, expected", [
    # circuits/circuit-terminations.provider_network.name v3.5
    (["provider_network", "name"], {"data": p.V3_C_TERMINATION}, NbVersionError),
    (["provider_network", "name"], {"data": p.V4_C_TERMINATION}, NbVersionError),
    (["provider_network", "name"], {"version": "4.1", "data": p.V3_C_TERMINATION}, "PROVIDER1"),
    (["provider_network", "name"], {"version": "4.1", "data": p.V4_C_TERMINATION}, ""),
    (["provider_network", "name"], {"version": "4.2", "data": p.V3_C_TERMINATION}, NbVersionError),
    (["provider_network", "name"], {"version": "4.2", "data": p.V4_C_TERMINATION}, NbVersionError),

    # circuits/circuit-terminations.site.name v3.5
    (["site", "name"], {"data": p.V3_C_TERMINATION}, NbVersionError),
    (["site", "name"], {"data": p.V4_C_TERMINATION}, NbVersionError),
    (["site", "name"], {"version": "4.1", "data": p.V3_C_TERMINATION}, "TST1"),
    (["site", "name"], {"version": "4.1", "data": p.V4_C_TERMINATION}, ""),
    (["site", "name"], {"version": "4.2", "data": p.V3_C_TERMINATION}, NbVersionError),
    (["site", "name"], {"version": "4.2", "data": p.V4_C_TERMINATION}, NbVersionError),
    # circuits/circuit-terminations.termination.name v4.2
    (["termination", "name"], {"data": p.V3_C_TERMINATION}, ""),
    (["termination", "name"], {"data": p.V4_C_TERMINATION}, "TST1"),
    (["termination", "name"], {"version": "4.1", "data": p.V3_C_TERMINATION}, ""),
    (["termination", "name"], {"version": "4.1", "data": p.V4_C_TERMINATION}, "TST1"),
    (["termination", "name"], {"version": "4.2", "data": p.V3_C_TERMINATION}, ""),
    (["termination", "name"], {"version": "4.2", "data": p.V4_C_TERMINATION}, "TST1"),

    # dcim/inventory-items.component.cable v3.5
    (["component", "cable"], {"data": p.V3_INV_ITEM}, NbVersionError),  # return <int>
    (["component", "cable"], {"data": p.V4_INV_ITEM}, NbVersionError),  # return <dict>
    (["component", "cable"], {"version": "4.1", "data": p.V3_INV_ITEM}, ""),
    (["component", "cable"], {"version": "4.1", "data": p.V4_INV_ITEM}, ""),
    (["component", "cable"], {"version": "4.2", "data": p.V3_INV_ITEM}, NbVersionError),
    (["component", "cable"], {"version": "4.2", "data": p.V4_INV_ITEM}, NbVersionError),
    # dcim/inventory-items.component.cable.display v4.2
    (["component", "cable", "display"], {"data": p.V3_INV_ITEM}, ""),
    (["component", "cable", "display"], {"data": p.V4_INV_ITEM}, p.CB1_),
    (["component", "cable", "display"], {"version": "4.1", "data": p.V3_INV_ITEM}, ""),
    (["component", "cable", "display"], {"version": "4.1", "data": p.V4_INV_ITEM}, p.CB1_),
    (["component", "cable", "display"], {"version": "4.2", "data": p.V3_INV_ITEM}, ""),
    (["component", "cable", "display"], {"version": "4.2", "data": p.V4_INV_ITEM}, p.CB1_),

    # dcim/power-outlets.power_port.cable v3.5
    (["power_port", "cable"], {"data": p.V3_POWER_OUTLET}, NbVersionError),  # return <int>
    (["power_port", "cable"], {"data": p.V4_POWER_OUTLET}, NbVersionError),  # return <dict>
    (["power_port", "cable"], {"version": "4.1", "data": p.V3_POWER_OUTLET}, ""),
    (["power_port", "cable"], {"version": "4.1", "data": p.V4_POWER_OUTLET}, ""),
    (["power_port", "cable"], {"version": "4.2", "data": p.V3_POWER_OUTLET}, NbVersionError),
    (["power_port", "cable"], {"version": "4.2", "data": p.V4_POWER_OUTLET}, NbVersionError),
    # dcim/power-outlets.power_port.cable.display v4.2
    (["power_port", "cable", "display"], {"data": p.V3_POWER_OUTLET}, ""),
    (["power_port", "cable", "display"], {"data": p.V4_POWER_OUTLET}, p.CB1_),
    (["power_port", "cable", "display"], {"version": "4.1", "data": p.V3_POWER_OUTLET}, ""),
    (["power_port", "cable", "display"], {"version": "4.1", "data": p.V4_POWER_OUTLET}, p.CB1_),
    (["power_port", "cable", "display"], {"version": "4.2", "data": p.V3_POWER_OUTLET}, ""),
    (["power_port", "cable", "display"], {"version": "4.2", "data": p.V4_POWER_OUTLET}, p.CB1_),

    # dcim/cable-terminations.termination.cable v3.5
    (["termination", "cable"], {"data": p.V3_CB_TERMINATION}, NbVersionError),  # return <int>
    (["termination", "cable"], {"data": p.V4_CB_TERMINATION}, NbVersionError),  # return <dict>
    (["termination", "cable"], {"version": "4.1", "data": p.V3_CB_TERMINATION}, ""),
    (["termination", "cable"], {"version": "4.1", "data": p.V4_CB_TERMINATION}, ""),
    (["termination", "cable"], {"version": "4.2", "data": p.V3_CB_TERMINATION}, NbVersionError),
    (["termination", "cable"], {"version": "4.2", "data": p.V4_CB_TERMINATION}, NbVersionError),
    # dcim/cable-terminations.termination.cable.display v4.2
    (["termination", "cable", "display"], {"data": p.V3_CB_TERMINATION}, ""),
    (["termination", "cable", "display"], {"data": p.V4_CB_TERMINATION}, p.CB1_),
    (["termination", "cable", "display"], {"version": "4.1", "data": p.V3_CB_TERMINATION}, ""),
    (["termination", "cable", "display"], {"version": "4.1", "data": p.V4_CB_TERMINATION}, p.CB1_),
    (["termination", "cable", "display"], {"version": "4.2", "data": p.V3_CB_TERMINATION}, ""),
    (["termination", "cable", "display"], {"version": "4.2", "data": p.V4_CB_TERMINATION}, p.CB1_),

    # dcim/platforms.napalm_driver v3.5
    (["napalm_driver"], {"data": p.V3_PLATFORM}, NbVersionError),
    (["napalm_driver"], {"data": p.V4_PLATFORM}, NbVersionError),
    (["napalm_driver"], {"version": "4.1", "data": p.V3_PLATFORM}, "ios"),
    (["napalm_driver"], {"version": "4.1", "data": p.V4_PLATFORM}, ""),
    (["napalm_driver"], {"version": "4.2", "data": p.V3_PLATFORM}, NbVersionError),
    (["napalm_driver"], {"version": "4.2", "data": p.V4_PLATFORM}, NbVersionError),

    # dcim/racks.type.value v3.5
    (["type", "value"], {"data": p.V3_RACK}, NbVersionError),
    (["type", "value"], {"data": p.V4_RACK}, NbVersionError),
    (["type", "value"], {"version": "4.1", "data": p.V3_RACK}, "4-post"),
    (["type", "value"], {"version": "4.1", "data": p.V4_RACK}, ""),
    (["type", "value"], {"version": "4.2", "data": p.V3_RACK}, NbVersionError),
    (["type", "value"], {"version": "4.2", "data": p.V4_RACK}, NbVersionError),
    # dcim/racks.form_factor.value v4.2
    (["form_factor", "value"], {"data": p.V3_RACK}, ""),
    (["form_factor", "value"], {"data": p.V4_RACK}, "4-post"),
    (["form_factor", "value"], {"version": "4.1", "data": p.V3_RACK}, ""),
    (["form_factor", "value"], {"version": "4.1", "data": p.V4_RACK}, "4-post"),
    (["form_factor", "value"], {"version": "4.2", "data": p.V3_RACK}, ""),
    (["form_factor", "value"], {"version": "4.2", "data": p.V4_RACK}, "4-post"),

    # ipam/prefixes.site.name v3.5
    (["site", "name"], {"data": p.V3_PREFIX}, NbVersionError),
    (["site", "name"], {"data": p.V4_PREFIX}, NbVersionError),
    (["site", "name"], {"version": "4.1", "data": p.V3_PREFIX}, "TST1"),
    (["site", "name"], {"version": "4.1", "data": p.V4_PREFIX}, ""),
    (["site", "name"], {"version": "4.2", "data": p.V3_PREFIX}, NbVersionError),
    (["site", "name"], {"version": "4.2", "data": p.V4_PREFIX}, NbVersionError),
    # ipam/prefixes.scope.name v4.2
    (["scope", "name"], {"data": p.V3_PREFIX}, ""),
    (["scope", "name"], {"data": p.V4_PREFIX}, "TST1"),
    (["scope", "name"], {"version": "4.1", "data": p.V3_PREFIX}, ""),
    (["scope", "name"], {"version": "4.1", "data": p.V4_PREFIX}, "TST1"),
    (["scope", "name"], {"version": "4.2", "data": p.V3_PREFIX}, ""),
    (["scope", "name"], {"version": "4.2", "data": p.V4_PREFIX}, "TST1"),
    # with tenant, used in NbTree
    (["site", "tenant", "name"], {"data": p.V3_PREFIX}, NbVersionError),
    (["scope", "tenant", "name"], {"data": p.V4_PREFIX}, "NOC"),

    # ipam/services.device.name v3.5
    (["device", "name"], {"data": p.V3_SERVICE}, NbVersionError),
    (["device", "name"], {"data": p.V4_SERVICE}, NbVersionError),
    (["device", "name"], {"version": "4.1", "data": p.V3_SERVICE}, "DEVICE1"),
    (["device", "name"], {"version": "4.1", "data": p.V4_SERVICE}, ""),
    (["device", "name"], {"version": "4.2", "data": p.V3_SERVICE}, NbVersionError),
    (["device", "name"], {"version": "4.2", "data": p.V4_SERVICE}, NbVersionError),
    # ipam/services.parent.name v4.2
    (["parent", "name"], {"data": p.V3_SERVICE}, ""),
    (["parent", "name"], {"data": p.V4_SERVICE}, "DEVICE1"),
    (["parent", "name"], {"version": "4.1", "data": p.V3_SERVICE}, ""),
    (["parent", "name"], {"version": "4.1", "data": p.V4_SERVICE}, "DEVICE1"),
    (["parent", "name"], {"version": "4.2", "data": p.V3_SERVICE}, ""),
    (["parent", "name"], {"version": "4.2", "data": p.V4_SERVICE}, "DEVICE1"),

    # extras/custom-fields.object_type v3.5
    (["object_type"], {"data": p.V3_CUSTOM_FIELD}, NbVersionError),
    (["object_type"], {"data": p.V4_CUSTOM_FIELD}, NbVersionError),
    (["object_type"], {"version": "4.1", "data": p.V3_CUSTOM_FIELD}, "ipam.vlan"),
    (["object_type"], {"version": "4.1", "data": p.V4_CUSTOM_FIELD}, ""),
    (["object_type"], {"version": "4.2", "data": p.V3_CUSTOM_FIELD}, NbVersionError),
    (["object_type"], {"version": "4.2", "data": p.V4_CUSTOM_FIELD}, NbVersionError),
    # extras/custom-fields.related_object_type v4.2
    (["related_object_type"], {"data": p.V3_CUSTOM_FIELD}, ""),
    (["related_object_type"], {"data": p.V4_CUSTOM_FIELD}, "ipam.vlan"),
    (["related_object_type"], {"version": "4.1", "data": p.V3_CUSTOM_FIELD}, ""),
    (["related_object_type"], {"version": "4.1", "data": p.V4_CUSTOM_FIELD}, "ipam.vlan"),
    (["related_object_type"], {"version": "4.2", "data": p.V3_CUSTOM_FIELD}, ""),
    (["related_object_type"], {"version": "4.2", "data": p.V4_CUSTOM_FIELD}, "ipam.vlan"),

    # extras/custom-fields.ui_visibility.value v3.5
    (["ui_visibility", "value"], {"data": p.V3_CUSTOM_FIELD}, NbVersionError),
    (["ui_visibility", "value"], {"data": p.V4_CUSTOM_FIELD}, NbVersionError),
    (["ui_visibility", "value"], {"version": "4.1", "data": p.V3_CUSTOM_FIELD}, "read-write"),
    (["ui_visibility", "value"], {"version": "4.1", "data": p.V4_CUSTOM_FIELD}, ""),
    (["ui_visibility", "value"], {"version": "4.2", "data": p.V3_CUSTOM_FIELD}, NbVersionError),
    (["ui_visibility", "value"], {"version": "4.2", "data": p.V4_CUSTOM_FIELD}, NbVersionError),
    # extras/custom-fields.ui_visible.value v4.2
    (["ui_visible", "value"], {"data": p.V3_CUSTOM_FIELD}, ""),
    (["ui_visible", "value"], {"data": p.V4_CUSTOM_FIELD}, "always"),
    (["ui_visible", "value"], {"version": "4.1", "data": p.V3_CUSTOM_FIELD}, ""),
    (["ui_visible", "value"], {"version": "4.1", "data": p.V4_CUSTOM_FIELD}, "always"),
    (["ui_visible", "value"], {"version": "4.2", "data": p.V3_CUSTOM_FIELD}, ""),
    (["ui_visible", "value"], {"version": "4.2", "data": p.V4_CUSTOM_FIELD}, "always"),

    # extras/object-changes.action.value v3.5
    (["action", "value"], {"data": p.V3_O_CHANGE}, NbVersionError),
    (["action", "value"], {"data": p.V4_O_CHANGE}, "update"),
    (["action", "value"], {"version": "4.1", "data": p.V3_O_CHANGE}, "update"),
    (["action", "value"], {"version": "4.1", "data": p.V4_O_CHANGE}, "update"),
    (["action", "value"], {"version": "4.2", "data": p.V3_O_CHANGE}, NbVersionError),
    (["action", "value"], {"version": "4.2", "data": p.V4_O_CHANGE}, "update"),
    # core/object-changes.action.value v4.2
    (["action", "value"], {"data": p.V3_O_CHANGE}, NbVersionError),
    (["action", "value"], {"data": p.V4_O_CHANGE}, "update"),
    (["action", "value"], {"version": "4.1", "data": p.V3_O_CHANGE}, "update"),
    (["action", "value"], {"version": "4.1", "data": p.V4_O_CHANGE}, "update"),
    (["action", "value"], {"version": "4.2", "data": p.V3_O_CHANGE}, NbVersionError),
    (["action", "value"], {"version": "4.2", "data": p.V4_O_CHANGE}, "update"),

    # extras/object-changes.prechange_data.last_updated v3.5
    (["prechange_data", "last_updated"], {"data": p.V3_O_CHANGE}, NbVersionError),
    (["prechange_data", "last_updated"], {"data": p.V4_O_CHANGE}, ""),
    (["prechange_data", "last_updated"], {"version": "4.1", "data": p.V3_O_CHANGE}, p.UPDATED),
    (["prechange_data", "last_updated"], {"version": "4.1", "data": p.V4_O_CHANGE}, ""),
    (["prechange_data", "last_updated"], {"version": "4.2", "data": p.V3_O_CHANGE}, NbVersionError),
    (["prechange_data", "last_updated"], {"version": "4.2", "data": p.V4_O_CHANGE}, ""),
    # core/object-changes.prechange_data.last_updated v4.2
    (["prechange_data", "last_updated"], {"data": p.V3_O_CHANGE}, NbVersionError),
    (["prechange_data", "last_updated"], {"data": p.V4_O_CHANGE}, ""),
    (["prechange_data", "last_updated"], {"version": "4.1", "data": p.V3_O_CHANGE}, p.UPDATED),
    (["prechange_data", "last_updated"], {"version": "4.1", "data": p.V4_O_CHANGE}, ""),
    (["prechange_data", "last_updated"], {"version": "4.2", "data": p.V3_O_CHANGE}, NbVersionError),
    (["prechange_data", "last_updated"], {"version": "4.2", "data": p.V4_O_CHANGE}, ""),

    # tenancy/contacts.group.name v3.5
    (["group", "name"], {"data": p.V3_CONTACT}, NbVersionError),
    (["group", "name"], {"data": p.V4_CONTACT}, NbVersionError),
    (["group", "name"], {"version": "4.1", "data": p.V3_CONTACT}, "GROUP1"),
    (["group", "name"], {"version": "4.1", "data": p.V4_CONTACT}, ""),
    (["group", "name"], {"version": "4.2", "data": p.V3_CONTACT}, NbVersionError),
    (["group", "name"], {"version": "4.2", "data": p.V4_CONTACT}, NbVersionError),
    # tenancy/contacts.groups[0].name v4.2
    (["groups", "name"], {"data": p.V3_CONTACT}, ""),
    (["groups", "name"], {"data": p.V4_CONTACT}, ""),
    (["groups", "name"], {"version": "4.1", "data": p.V3_CONTACT}, ""),
    (["groups", "name"], {"version": "4.1", "data": p.V4_CONTACT}, ""),
    (["groups", "name"], {"version": "4.2", "data": p.V3_CONTACT}, ""),
    (["groups", "name"], {"version": "4.2", "data": p.V4_CONTACT}, ""),
])
def test__str__deprecated(caplog, nbp, keys: LStr, params, expected):
    """NbParser.str() site v4.2."""
    if isinstance(expected, str):
        actual = nbp.str(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbp.str(*keys)


@pytest.mark.parametrize("key, params, expected", [
    # version
    ("site", {"version": "4.1", "data": p.V3_C_TERMINATION}, []),
    ("site", {"version": "4.2", "data": p.V3_C_TERMINATION}, NbVersionError),
    ("termination", {"version": "4.1", "data": p.V4_C_TERMINATION}, []),
    ("termination", {"version": "4.2", "data": p.V4_C_TERMINATION}, []),
    # circuits/circuit-terminations.site.name
    ("site", {"data": p.V3_C_TERMINATION}, NbVersionError),
    ("termination", {"data": p.V4_C_TERMINATION}, []),
    # ipam/prefix.site.name
    ("site", {"data": p.V3_PREFIX}, NbVersionError),
    ("scope", {"data": p.V4_PREFIX}, []),
    # dcim/platforms.napalm_driver
    ("napalm_driver", {"data": p.V3_PLATFORM}, NbVersionError),
    ("napalm_driver", {"data": p.V4_PLATFORM}, NbVersionError),
    # extras/object-changes moved to core/object-changes
    ("prechange_data", {"data": p.V3_O_CHANGE}, NbVersionError),
    ("prechange_data", {"data": p.V4_O_CHANGE}, []),
])
def test__raise_deprecated_key(caplog, nbp, key, params, expected):
    """NbParser._raise_deprecated_key()"""
    if isinstance(expected, list):
        nbp._raise_deprecated_key(key)
        act_logs = [r.levelno for r in caplog.records]
        assert act_logs == expected
    else:
        with pytest.raises(expected):
            nbp._raise_deprecated_key(key)


@pytest.mark.parametrize("keys, type_req, params, exp_logs", [
    # dcim/inventory-items.component.cable int/dict
    (["component", "cable"], int, {"data": p.V3_INV_ITEM}, NbVersionError),
    (["component", "cable"], int, {"data": p.V4_INV_ITEM}, NbVersionError),
    (["component", "cable"], dict, {"data": p.V4_INV_ITEM}, []),
    (["component", "cable"], int, {"version": "4.1", "data": p.V3_INV_ITEM}, []),
    (["component", "cable"], int, {"version": "4.1", "data": p.V4_INV_ITEM}, []),
    (["component", "cable"], dict, {"version": "4.1", "data": p.V4_INV_ITEM}, []),
    (["component", "cable"], int, {"version": "4.2", "data": p.V3_INV_ITEM}, NbVersionError),
    (["component", "cable"], int, {"version": "4.2", "data": p.V4_INV_ITEM}, NbVersionError),
    (["component", "cable"], dict, {"version": "4.2", "data": p.V4_INV_ITEM}, []),
    (["component", "cable"], int, {"data": p.V3_POWER_OUTLET}, []),  # other app/model
    (["component", "cable"], int, {"data": p.V4_POWER_OUTLET}, []),  # other app/model
    # dcim/power-outlets.power_port.cable int/dict
    (["power_port", "cable"], int, {"data": p.V3_POWER_OUTLET}, NbVersionError),
    (["power_port", "cable"], int, {"data": p.V4_POWER_OUTLET}, NbVersionError),
    (["power_port", "cable"], dict, {"data": p.V4_POWER_OUTLET}, []),
    # dcim/devices.primary_ip.family int/dict
    (["primary_ip", "family"], int, {"data": p.V3_DEVICE}, NbVersionError),
    (["primary_ip", "family"], int, {"data": p.V4_DEVICE}, NbVersionError),
    (["primary_ip", "family"], dict, {"data": p.V4_DEVICE}, []),
])
def test__raise_deprecated_type(caplog, nbp, keys, type_req, params, exp_logs):
    """NbParser._raise_deprecated_type()"""
    if isinstance(exp_logs, list):
        nbp._raise_deprecated_type(keys=keys, type_req=type_req)
        act_logs = [r.levelno for r in caplog.records]
        assert act_logs == exp_logs
    else:
        with pytest.raises(exp_logs):
            nbp._raise_deprecated_type(keys=keys, type_req=type_req)


@pytest.mark.parametrize("keys, params, expected", p.STRICT_DICT)
def test__strict_dict(nbp, keys: LStr, params, expected):
    """NbParser.strict_dict()."""
    if isinstance(expected, dict):
        actual = nbp.strict_dict(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbp.strict_dict(*keys)


@pytest.mark.parametrize("keys, params, expected", p.STRICT_INT)
def test__strict_int(nbp, keys: LStr, params, expected):
    """NbParser.strict_int()."""
    if isinstance(expected, int):
        actual = nbp.strict_int(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbp.strict_int(*keys)


@pytest.mark.parametrize("keys, params, expected", p.STRICT_LIST)
def test__strict_list(nbp, keys: LStr, params, expected):
    """NbParser.strict_list()."""
    if isinstance(expected, list):
        actual = nbp.strict_list(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbp.strict_list(*keys)


@pytest.mark.parametrize("keys, params, expected", p.STRICT_STR)
def test__strict_str(nbp, keys: LStr, params, expected):
    """NbParser.strict_str()."""
    if isinstance(expected, str):
        actual = nbp.strict_str(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbp.strict_str(*keys)


@pytest.mark.parametrize("objects, params, expected", [
    ([{"id": 1}, {"id": 2}], {}, [1, 2]),
    ([{"id": 1}, {"id": 2}], {"id": 1}, [1]),
    ([{"id": 1}, {"id": 2}], {"id": 2}, [2]),
    ([{"id": 1, "k1": "A"}, {"id": 2, "k1": "B"}], {"k1": "A"}, [1]),
    ([{"id": 1, "k1": "A"}, {"id": 2, "k1": "B"}], {"k1": "B"}, [2]),
    ([{"id": 1, "k1": {"k2": "A"}}, {"id": 2, "k1": {"k2": "B"}}], {"k1__k2": "A"}, [1]),
    ([{"id": 1, "k1": {"k2": "A"}}, {"id": 2, "k1": {"k2": "B"}}], {"k1__k2": "B"}, [2]),
    ([{"id": 1}, {"id": 2}], {"id": 3}, []),
    ([], {}, []),
])
def test__find_objects(objects, params, expected):
    """nb_nbp.find_objects()."""
    results = nb_parser.find_objects(objects=objects, **params)
    actual = [d["id"] for d in results]
    assert actual == expected
