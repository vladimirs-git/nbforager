"""Tests nbforager.parser.nb_parser"""
from typing import Any

import pytest

from nbforager.parser import nb_parser
from nbforager.parser.nb_parser import NbParser
from nbforager.types_ import LStr
from tests.parser_ import params__nb_parser as p


@pytest.mark.parametrize("keys, data, strict, expected", p.ANY)
def test__any(keys: LStr, data: dict, strict: bool, expected: Any):
    """NbParser.any()."""
    parser = NbParser(data=data, strict=strict)
    actual = parser.any(*keys)
    assert actual == expected


@pytest.mark.parametrize("keys, data, strict, expected", p.BOOL)
def test__bool(keys: LStr, data: dict, strict: bool, expected: Any):
    """NbParser.bool()."""
    parser = NbParser(data=data, strict=strict)
    if isinstance(expected, bool):
        actual = parser.bool(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.bool(*keys)


@pytest.mark.parametrize("keys, data, strict, expected", p.DICT)
def test__dict(keys: LStr, data: dict, strict: bool, expected: Any):
    """NbParser.dict()."""
    parser = NbParser(data=data, strict=strict)
    if isinstance(expected, dict):
        actual = parser.dict(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.dict(*keys)


@pytest.mark.parametrize("keys, data, strict, expected", p.INT)
def test__int(keys: LStr, data: dict, strict: bool, expected: Any):
    """NbParser.int()."""
    parser = NbParser(data=data, strict=strict)
    if isinstance(expected, int):
        actual = parser.int(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.int(*keys)


@pytest.mark.parametrize("keys, data, strict, expected", p.LIST)
def test__list(keys: LStr, data: dict, strict: bool, expected: Any):
    """NbParser.list()."""
    parser = NbParser(data=data, strict=strict)
    if isinstance(expected, list):
        actual = parser.list(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.list(*keys)


@pytest.mark.parametrize("keys, data, strict, expected", p.STR)
def test__str(keys: LStr, data: dict, strict: bool, expected: Any):
    """NbParser.str()."""
    parser = NbParser(data=data, strict=strict)
    if isinstance(expected, str):
        actual = parser.str(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.str(*keys)


@pytest.mark.parametrize("keys, data, strict, expected", p.STRICT_DICT)
def test__strict_dict(keys: LStr, data: dict, strict: bool, expected: Any):
    """NbParser.strict_dict()."""
    parser = NbParser(data=data, strict=strict)
    if isinstance(expected, dict):
        actual = parser.strict_dict(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.strict_dict(*keys)


@pytest.mark.parametrize("keys, data, strict, expected", p.STRICT_INT)
def test__strict_int(keys: LStr, data: dict, strict: bool, expected: Any):
    """NbParser.strict_int()."""
    parser = NbParser(data=data, strict=strict)
    if isinstance(expected, int):
        actual = parser.strict_int(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.strict_int(*keys)


@pytest.mark.parametrize("keys, data, strict, expected", p.STRICT_LIST)
def test__strict_list(keys: LStr, data: dict, strict: bool, expected: Any):
    """NbParser.strict_list()."""
    parser = NbParser(data=data, strict=strict)
    if isinstance(expected, list):
        actual = parser.strict_list(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.strict_list(*keys)


@pytest.mark.parametrize("keys, data, strict, expected", p.STRICT_STR)
def test__strict_str(keys: LStr, data: dict, strict: bool, expected: Any):
    """NbParser.strict_str()."""
    parser = NbParser(data=data, strict=strict)
    if isinstance(expected, str):
        actual = parser.strict_str(*keys)
        assert actual == expected
    else:
        with pytest.raises(expected):
            parser.strict_str(*keys)


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
    """nb_parser.find_objects()."""
    results = nb_parser.find_objects(objects=objects, **params)
    actual = [d["id"] for d in results]
    assert actual == expected
