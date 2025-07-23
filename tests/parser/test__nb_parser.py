"""Tests nbforager.parser.nb_parser"""
from logging import WARNING

import pytest

from nbforager.parser import nb_parser
from nbforager.parser.nb_parser import NbParser
from nbforager.types_ import LStr, DAny
from tests.parser import params__nb_parser as p


@pytest.fixture
def nbp(params: DAny) -> NbParser:
    """Create NbValue instance based on the params."""
    return NbParser(**params)


@pytest.mark.parametrize("keys, params, expected", p.ANY)
def test__any(nbp, keys: LStr, params, expected):
    """NbParser.any()."""
    actual = nbp.any(*keys)
    assert actual == expected


@pytest.mark.parametrize("keys, params, expected", p.BOOL)
def test__bool(nbp, keys: LStr, params, expected):
    """NbParser.bool()."""
    if isinstance(expected, bool):
        actual = nbp.bool(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbp.bool(*keys)


@pytest.mark.parametrize("keys, params, expected, exp_log", [
    # site bool
    (["site", "bool"], {"data": p.PREFIX_SITE_D}, True, [WARNING]),
    (["site", "bool"], {"data": p.PREFIX_SITE_D, "version": "4.1"}, True, []),
    (["site", "bool"], {"data": p.PREFIX_SITE_D, "version": "4.2"}, True, [WARNING]),
    (["site", "tenant", "bool"], {"data": p.PREFIX_SITE_D}, True, [WARNING]),
    (["site", "tenant", "bool"], {"data": p.PREFIX_SITE_D, "version": "4.1"}, True, []),
    (["site", "tenant", "bool"], {"data": p.PREFIX_SITE_D, "version": "4.2"}, True, [WARNING]),
    (["site", "tenant", "bool"], {"data": p.PREFIX_SCOPE_D}, False, [WARNING]),
    (["site", "tenant", "bool"], {"data": p.PREFIX_SCOPE_D, "version": "4.1"}, False, []),
    (["site", "tenant", "bool"], {"data": p.PREFIX_SCOPE_D, "version": "4.2"}, False, [WARNING]),
    # scope bool
    (["scope", "bool"], {"data": p.PREFIX_SITE_D}, False, []),
    (["scope", "bool"], {"data": p.PREFIX_SITE_D, "version": "4.1"}, False, []),
    (["scope", "bool"], {"data": p.PREFIX_SITE_D, "version": "4.2"}, False, []),
    (["scope", "bool"], {"data": p.PREFIX_SCOPE_D}, True, []),
    (["scope", "bool"], {"data": p.PREFIX_SCOPE_D, "version": "4.1"}, True, []),
    (["scope", "bool"], {"data": p.PREFIX_SCOPE_D, "version": "4.2"}, True, []),
])
def test__bool__site(caplog, nbp, keys: LStr, params, expected, exp_log):
    """NbParser.bool() site v4.2."""
    actual = nbp.bool(*keys)

    assert actual == expected
    act_logs = [r.levelno for r in caplog.records]
    assert act_logs == exp_log


@pytest.mark.parametrize("keys, params, expected", p.DICT)
def test__dict(nbp, keys: LStr, params, expected):
    """NbParser.dict()."""
    if isinstance(expected, dict):
        actual = nbp.dict(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbp.dict(*keys)


@pytest.mark.parametrize("keys, params, expected, exp_log", [
    # site id
    (["site", "tenant"], {"data": p.PREFIX_SITE_D}, p.TENANT_D, [WARNING]),
    (["site", "tenant"], {"data": p.PREFIX_SITE_D, "version": "4.1"}, p.TENANT_D, []),
    (["site", "tenant"], {"data": p.PREFIX_SITE_D, "version": "4.2"}, p.TENANT_D, [WARNING]),
    (["site", "tenant"], {"data": p.PREFIX_SCOPE_D}, {}, [WARNING]),
    (["site", "tenant"], {"data": p.PREFIX_SCOPE_D, "version": "4.1"}, {}, []),
    (["site", "tenant"], {"data": p.PREFIX_SCOPE_D, "version": "4.2"}, {}, [WARNING]),
    # scope id
    (["scope", "tenant"], {"data": p.PREFIX_SITE_D}, {}, []),
    (["scope", "tenant"], {"data": p.PREFIX_SITE_D, "version": "4.1"}, {}, []),
    (["scope", "tenant"], {"data": p.PREFIX_SITE_D, "version": "4.2"}, {}, []),
    (["scope", "tenant"], {"data": p.PREFIX_SCOPE_D}, p.TENANT_D, []),
    (["scope", "tenant"], {"data": p.PREFIX_SCOPE_D, "version": "4.1"}, p.TENANT_D, []),
    (["scope", "tenant"], {"data": p.PREFIX_SCOPE_D, "version": "4.2"}, p.TENANT_D, []),
])
def test__dict__site(caplog, nbp, keys: LStr, params, expected, exp_log):
    """NbParser.dict() site v4.2."""
    actual = nbp.dict(*keys)

    assert actual == expected
    act_logs = [r.levelno for r in caplog.records]
    assert act_logs == exp_log


@pytest.mark.parametrize("keys, params, expected", p.INT)
def test__int(nbp, keys: LStr, params, expected):
    """NbParser.int()."""
    if isinstance(expected, int):
        actual = nbp.int(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbp.int(*keys)


@pytest.mark.parametrize("keys, params, expected, exp_log", [
    # site id
    (["site", "id"], {"data": p.PREFIX_SITE_D}, p.S1, [WARNING]),
    (["site", "id"], {"data": p.PREFIX_SITE_D, "version": "4.1"}, p.S1, []),
    (["site", "id"], {"data": p.PREFIX_SITE_D, "version": "4.2"}, p.S1, [WARNING]),
    (["site", "tenant", "id"], {"data": p.PREFIX_SITE_D}, p.T1, [WARNING]),
    (["site", "tenant", "id"], {"data": p.PREFIX_SITE_D, "version": "4.1"}, p.T1, []),
    (["site", "tenant", "id"], {"data": p.PREFIX_SITE_D, "version": "4.2"}, p.T1, [WARNING]),
    (["site", "tenant", "id"], {"data": p.PREFIX_SCOPE_D}, 0, [WARNING]),
    (["site", "tenant", "id"], {"data": p.PREFIX_SCOPE_D, "version": "4.1"}, 0, []),
    (["site", "tenant", "id"], {"data": p.PREFIX_SCOPE_D, "version": "4.2"}, 0, [WARNING]),
    # scope id
    (["scope", "id"], {"data": p.PREFIX_SITE_D}, 0, []),
    (["scope", "id"], {"data": p.PREFIX_SITE_D, "version": "4.1"}, 0, []),
    (["scope", "id"], {"data": p.PREFIX_SITE_D, "version": "4.2"}, 0, []),
    (["scope", "id"], {"data": p.PREFIX_SCOPE_D}, p.S1, []),
    (["scope", "id"], {"data": p.PREFIX_SCOPE_D, "version": "4.1"}, p.S1, []),
    (["scope", "id"], {"data": p.PREFIX_SCOPE_D, "version": "4.2"}, p.S1, []),
])
def test__int__site(caplog, nbp, keys: LStr, params, expected, exp_log):
    """NbParser.int() site v4.2."""
    actual = nbp.int(*keys)

    assert actual == expected
    act_logs = [r.levelno for r in caplog.records]
    assert act_logs == exp_log


@pytest.mark.parametrize("keys, params, expected", p.LIST)
def test__list(nbp, keys: LStr, params, expected):
    """NbParser.list()."""
    if isinstance(expected, list):
        actual = nbp.list(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbp.list(*keys)


@pytest.mark.parametrize("keys, params, expected, exp_log", [
    # site name
    (["site", "name"], {"data": p.PREFIX_SITE_D}, [], [WARNING]),
    (["site", "name"], {"data": p.PREFIX_SITE_D, "version": "4.1"}, [], []),
    (["site", "name"], {"data": p.PREFIX_SITE_D, "version": "4.2"}, [], [WARNING]),
    (["site", "tenant", "tags"], {"data": p.PREFIX_SITE_D}, [p.TAG_D], [WARNING]),
    (["site", "tenant", "tags"], {"data": p.PREFIX_SITE_D, "version": "4.1"}, [p.TAG_D], []),
    (["site", "tenant", "tags"], {"data": p.PREFIX_SITE_D, "version": "4.2"}, [p.TAG_D], [WARNING]),
    (["site", "name"], {"data": p.PREFIX_SCOPE_D}, [], [WARNING]),
    (["site", "name"], {"data": p.PREFIX_SCOPE_D, "version": "4.1"}, [], []),
    (["site", "name"], {"data": p.PREFIX_SCOPE_D, "version": "4.2"}, [], [WARNING]),
    # scope name
    (["scope", "name"], {"data": p.PREFIX_SITE_D}, [], []),
    (["scope", "name"], {"data": p.PREFIX_SITE_D, "version": "4.1"}, [], []),
    (["scope", "name"], {"data": p.PREFIX_SITE_D, "version": "4.2"}, [], []),
    (["scope", "name"], {"data": p.PREFIX_SCOPE_D}, [], []),
    (["scope", "name"], {"data": p.PREFIX_SCOPE_D, "version": "4.1"}, [], []),
    (["scope", "name"], {"data": p.PREFIX_SCOPE_D, "version": "4.2"}, [], []),
])
def test__list__site(caplog, nbp, keys: LStr, params, expected, exp_log):
    """NbParser.list() site v4.2."""
    actual = nbp.list(*keys)

    assert actual == expected
    act_logs = [r.levelno for r in caplog.records]
    assert act_logs == exp_log


@pytest.mark.parametrize("keys, params, expected", p.STR)
def test__str(nbp, keys: LStr, params, expected):
    """NbParser.str()."""
    if isinstance(expected, str):
        actual = nbp.str(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nbp.str(*keys)


@pytest.mark.parametrize("keys, params, expected, exp_log", [
    # site name
    (["site", "name"], {"data": p.PREFIX_SITE_D}, "TST1", [WARNING]),
    (["site", "name"], {"data": p.PREFIX_SITE_D, "version": "4.1"}, "TST1", []),
    (["site", "name"], {"data": p.PREFIX_SITE_D, "version": "4.2"}, "TST1", [WARNING]),
    (["site", "tenant", "name"], {"data": p.PREFIX_SITE_D}, "NOC", [WARNING]),
    (["site", "tenant", "name"], {"data": p.PREFIX_SITE_D, "version": "4.1"}, "NOC", []),
    (["site", "tenant", "name"], {"data": p.PREFIX_SITE_D, "version": "4.2"},
     "NOC", [WARNING]),
    (["site", "name"], {"data": p.PREFIX_SCOPE_D}, "", [WARNING]),
    (["site", "name"], {"data": p.PREFIX_SCOPE_D, "version": "4.1"}, "", []),
    (["site", "name"], {"data": p.PREFIX_SCOPE_D, "version": "4.2"}, "", [WARNING]),
    # scope name
    (["scope", "name"], {"data": p.PREFIX_SITE_D}, "", []),
    (["scope", "name"], {"data": p.PREFIX_SITE_D, "version": "4.1"}, "", []),
    (["scope", "name"], {"data": p.PREFIX_SITE_D, "version": "4.2"}, "", []),
    (["scope", "name"], {"data": p.PREFIX_SCOPE_D}, "TST1", []),
    (["scope", "name"], {"data": p.PREFIX_SCOPE_D, "version": "4.1"}, "TST1", []),
    (["scope", "name"], {"data": p.PREFIX_SCOPE_D, "version": "4.2"}, "TST1", []),
])
def test__str__site(caplog, nbp, keys: LStr, params, expected, exp_log):
    """NbParser.str() site v4.2."""
    actual = nbp.str(*keys)

    assert actual == expected
    act_logs = [r.levelno for r in caplog.records]
    assert act_logs == exp_log

@pytest.mark.parametrize("keys, params, exp_log", [
    # circuits/circuit-terminations
    # site name
    ("site", {"data": p.CIRCUIT_TERMINATION_SITE_D}, [WARNING]),
    ("site", {"data": p.CIRCUIT_TERMINATION_SITE_D, "version": "4.1"}, []),
    ("site", {"data": p.CIRCUIT_TERMINATION_SITE_D, "version": "4.2"}, [WARNING]),
    ("site", {"data": p.CIRCUIT_TERMINATION_TERMINATION_D}, [WARNING]),
    ("site", {"data": p.CIRCUIT_TERMINATION_TERMINATION_D, "version": "4.1"}, []),
    ("site", {"data": p.CIRCUIT_TERMINATION_TERMINATION_D, "version": "4.2"}, [WARNING]),
    # scope name
    (["scope", "name"], {"data": p.PREFIX_SITE_D}, []),
    (["scope", "name"], {"data": p.PREFIX_SITE_D, "version": "4.1"}, []),
    (["scope", "name"], {"data": p.PREFIX_SITE_D, "version": "4.2"}, []),
    (["scope", "name"], {"data": p.PREFIX_SCOPE_D}, []),
    (["scope", "name"], {"data": p.PREFIX_SCOPE_D, "version": "4.1"}, []),
    (["scope", "name"], {"data": p.PREFIX_SCOPE_D, "version": "4.2"}, []),
    # ipam/prefix
    # site name
    ("site", {"data": p.PREFIX_SITE_D}, [WARNING]),
    ("site", {"data": p.PREFIX_SITE_D, "version": "4.1"}, []),
    ("site", {"data": p.PREFIX_SITE_D, "version": "4.2"}, [WARNING]),
    ("site", {"data": p.PREFIX_SCOPE_D}, [WARNING]),
    ("site", {"data": p.PREFIX_SCOPE_D, "version": "4.1"}, []),
    ("site", {"data": p.PREFIX_SCOPE_D, "version": "4.2"}, [WARNING]),
    # scope name
    (["scope", "name"], {"data": p.PREFIX_SITE_D}, []),
    (["scope", "name"], {"data": p.PREFIX_SITE_D, "version": "4.1"}, []),
    (["scope", "name"], {"data": p.PREFIX_SITE_D, "version": "4.2"}, []),
    (["scope", "name"], {"data": p.PREFIX_SCOPE_D}, []),
    (["scope", "name"], {"data": p.PREFIX_SCOPE_D, "version": "4.1"}, []),
    (["scope", "name"], {"data": p.PREFIX_SCOPE_D, "version": "4.2"}, []),
])
def test__log_prefix_site(caplog, nbp, keys, params, exp_log):
    """NbParser._log_prefix_site()"""
    nbp._log_ipam_prefix_site(keys)

    act_logs = [r.levelno for r in caplog.records]
    assert act_logs == exp_log


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
