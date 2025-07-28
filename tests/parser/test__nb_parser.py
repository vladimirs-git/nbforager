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
    (["site", "tenant", "bool"], {"version": "4.1", "data": p.V3_PREFIX_D}, True),
    (["site", "tenant", "bool"], {"version": "4.2", "data": p.V3_PREFIX_D}, NbVersionError),
    (["scope", "tenant", "bool"], {"version": "4.1", "data": p.V4_PREFIX_D}, True),
    (["scope", "tenant", "bool"], {"version": "4.2", "data": p.V4_PREFIX_D}, True),
    # ipam/prefixes.site bool
    (["site", "tenant", "bool"], {"data": p.V3_PREFIX_D}, NbVersionError),
    (["site", "tenant", "bool"], {"data": p.V4_PREFIX_D}, NbVersionError),
    (["scope", "bool"], {"data": p.V3_PREFIX_D}, False),
    (["scope", "bool"], {"data": p.V4_PREFIX_D}, True),
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
    # version
    (["site", "tenant"], {"version": "4.1", "data": p.V3_PREFIX_D}, p.TENANT_D),
    (["site", "tenant"], {"version": "4.2", "data": p.V3_PREFIX_D}, NbVersionError),
    (["scope", "tenant"], {"version": "4.1", "data": p.V3_PREFIX_D}, {}),
    (["scope", "tenant"], {"version": "4.2", "data": p.V3_PREFIX_D}, {}),
    # ipam/prefixes.site dict
    (["site", "tenant"], {"data": p.V3_PREFIX_D}, NbVersionError),
    (["site", "tenant"], {"data": p.V4_PREFIX_D}, NbVersionError),
    (["scope", "tenant"], {"data": p.V3_PREFIX_D}, {}),
    (["scope", "tenant"], {"data": p.V4_PREFIX_D}, p.TENANT_D),
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
    # version
    (["site", "id"], {"version": "4.1", "data": p.V3_PREFIX_D}, p.S1),
    (["site", "id"], {"version": "4.2", "data": p.V4_PREFIX_D}, NbVersionError),
    (["scope", "id"], {"version": "4.1", "data": p.V3_PREFIX_D}, 0),
    (["scope", "id"], {"version": "4.2", "data": p.V4_PREFIX_D}, p.S1),
    # ipam/prefixes.site.id
    (["site", "id"], {"data": p.V3_PREFIX_D}, NbVersionError),
    (["site", "tenant", "id"], {"data": p.V3_PREFIX_D}, NbVersionError),
    (["scope", "id"], {"data": p.V4_PREFIX_D}, p.S1),
    (["scope", "tenant", "id"], {"data": p.V4_PREFIX_D}, p.T1),
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
    # version
    (["site", "tags"], {"version": "4.1", "data": p.V3_PREFIX_D}, [p.TAG_D]),
    (["site", "tags"], {"version": "4.2", "data": p.V3_PREFIX_D}, NbVersionError),
    (["scope", "tags"], {"version": "4.1", "data": p.V4_PREFIX_D}, [p.TAG_D]),
    (["scope", "tags"], {"version": "4.2", "data": p.V4_PREFIX_D}, [p.TAG_D]),
    # ipam/prefixes.site list
    (["site", "tags"], {"data": p.V3_PREFIX_D}, NbVersionError),
    (["site", "tenant", "tags"], {"data": p.V3_PREFIX_D}, NbVersionError),
    (["scope", "tags"], {"data": p.V4_PREFIX_D}, [p.TAG_D]),
    (["scope", "tenant", "tags"], {"data": p.V4_PREFIX_D}, [p.TAG_D]),

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
    # version
    (["site", "name"], {"version": "4.1", "data": p.V3_PREFIX_D}, "TST1"),
    (["site", "name"], {"version": "4.2", "data": p.V3_PREFIX_D}, NbVersionError),
    (["scope", "name"], {"version": "4.1", "data": p.V4_PREFIX_D}, "TST1"),
    (["scope", "name"], {"version": "4.2", "data": p.V4_PREFIX_D}, "TST1"),
    # site name
    (["site", "name"], {"data": p.V3_PREFIX_D}, NbVersionError),
    (["site", "tenant", "name"], {"data": p.V3_PREFIX_D}, NbVersionError),
    (["scope", "name"], {"data": p.V4_PREFIX_D}, "TST1"),
    (["scope", "tenant", "name"], {"data": p.V4_PREFIX_D}, "NOC"),
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
    ("site", {"version": "4.1", "data": p.V3_CIRCUIT_TERMINATION_D}, []),
    ("site", {"version": "4.2", "data": p.V3_CIRCUIT_TERMINATION_D}, NbVersionError),
    ("termination", {"version": "4.1", "data": p.V4_CIRCUIT_TERMINATION_D}, []),
    ("termination", {"version": "4.2", "data": p.V4_CIRCUIT_TERMINATION_D}, []),
    # circuits/circuit-terminations.site.name
    ("site", {"data": p.V3_CIRCUIT_TERMINATION_D}, NbVersionError),
    ("termination", {"data": p.V4_CIRCUIT_TERMINATION_D}, []),
    # ipam/prefix.site.name
    ("site", {"data": p.V3_PREFIX_D}, NbVersionError),
    ("scope", {"data": p.V4_PREFIX_D}, []),
    # dcim/platforms.napalm_driver
    ("napalm_driver", {"data": p.V3_PLATFORM_D}, NbVersionError),
    ("napalm_driver", {"data": p.V4_PLATFORM_D}, []),
    # extras/object-changes moved to core/object-changes
    ("prechange_data", {"data": p.V3_OBJECT_CHANGE_D}, NbVersionError),
    ("prechange_data", {"data": p.V4_OBJECT_CHANGE_D}, []),
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


@pytest.mark.parametrize("keys, params, expected", [
    # version
    (["component", "cable"], {"version": "4.1", "data": p.V3_INVENTORY_ITEM_D}, []),
    (["component", "cable"], {"version": "4.2", "data": p.V3_INVENTORY_ITEM_D}, NbVersionError),
    (["component", "cable"], {"version": "4.1", "data": p.V4_INVENTORY_ITEM_D}, []),
    (["component", "cable"], {"version": "4.2", "data": p.V4_INVENTORY_ITEM_D}, []),
    # dcim/inventory-items.component.cable int/dict
    (["component", "cable"], {"data": p.V3_INVENTORY_ITEM_D}, NbVersionError),
    (["component", "cable"], {"data": p.V4_INVENTORY_ITEM_D}, []),
    # dcim/power-outlets.power_port.cable int/dict
    (["power_port", "cable"], {"data": p.V3_POWER_OUTLET_D}, NbVersionError),
    (["component", "cable"], {"data": p.V4_POWER_OUTLET_D}, []),
    # dcim/devices.primary_ip.family int/dict
    (["primary_ip", "family"], {"data": p.V3_DEVICE_D}, NbVersionError),
    (["primary_ip", "family"], {"data": p.V4_DEVICE_D}, []),
])
def test__raise_deprecated_type(caplog, nbp, keys, params, expected):
    """NbParser._raise_deprecated_type()"""
    if isinstance(expected, list):
        nbp._raise_deprecated_type(keys)
        act_logs = [r.levelno for r in caplog.records]
        assert act_logs == expected
    else:
        with pytest.raises(expected):
            nbp._raise_deprecated_type(keys)


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
