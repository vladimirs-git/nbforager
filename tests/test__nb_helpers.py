"""Tests nb_helpers.py."""
from typing import Any
from urllib.parse import urlencode

import pytest

from nbforager import nb_helpers
from tests import params__helpers as p


@pytest.mark.parametrize("dependency, expected", [
    (nb_helpers.DEPENDENT_MODELS, p.ORDERED_MODELS),
    ({"a": ["b"], "b": ["a"]}, ValueError),  # circular dependency
])
def test__dependency_ordered_paths(dependency, expected):
    """nb_helpers.dependency_ordered_paths()."""
    if isinstance(expected, list):
        actual = nb_helpers.dependency_ordered_paths(dependency)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nb_helpers.dependency_ordered_paths(dependency)


@pytest.mark.parametrize("need_split, params_d, expected", [
    ([], {}, []),

    ([], {"a": [1]}, [{"a": [1]}]),
    ([], {"a": [1, 1]}, [{"a": [1, 1]}]),
    ([], {"a": [1, 2]}, [{"a": [1, 2]}]),
    ([], {"a": [1], "b": [1]}, [{"a": [1], "b": [1]}]),
    ([], {"or_a": [1, 2]}, [{"or_a": [1]}, {"or_a": [2]}]),
    (["a"], {}, []),
    (["a"], {"a": [1, 1]}, [{"a": [1]}, {"a": [1]}]),
    (["a"], {"a": [1, 2]}, [{"a": [1]}, {"a": [2]}]),
    (["a"], {"a": [1], "b": [1]}, [{"a": [1], "b": [1]}]),
    (["a"], {"a": [1, 2], "b": [1]}, [{"a": [1], "b": [1]}, {"a": [2], "b": [1]}]),
    (["a", "b"], {"a": [1, 2], "b": [1, 2]},
     [{"a": [1], "b": [1]}, {"a": [1], "b": [2]}, {"a": [2], "b": [1]}, {"a": [2], "b": [2]}]),
    (["a", "b"], {"a": [1, 2], "b": [1, 2], "c": [1, 2], "d": [1]},
     [{"a": [1], "b": [1], "c": [1, 2], "d": [1]},
      {"a": [1], "b": [2], "c": [1, 2], "d": [1]},
      {"a": [2], "b": [1], "c": [1, 2], "d": [1]},
      {"a": [2], "b": [2], "c": [1, 2], "d": [1]}]),
])
def test__make_combinations(need_split, params_d, expected):
    """nb_helpers.make_combinations()."""
    actual = nb_helpers.make_combinations(need_split=need_split, params_d=params_d)
    assert actual == expected


@pytest.mark.parametrize("need_split, params_d, expected", [
    ([], {}, set()),
    ([], {"or_a": [1, 2], "b": [1, 2]}, {"or_a"}),
    (["a"], {"a": [1, 2], "b": [1, 2]}, {"a"}),
])
def test__get_keys_need_split(need_split, params_d, expected):
    """nb_helpers._get_keys_need_split()."""
    actual = nb_helpers._get_keys_need_split(need_split=need_split, params_d=params_d)
    assert actual == expected


@pytest.mark.parametrize("params_ld, expected", [
    ([], []),
    ([{"a_or": [1]}], [{"a_or": [1]}]),
    ([{"or_a": [1]}], [{"a": [1]}]),
    ([{"or_a": [1]}, {"or_a": [2]}, {"a_or": [3]}], [{"a": [1]}, {"a": [2]}, {"a_or": [3]}]),
])
def test__change_params_or(params_ld, expected):
    """nb_helpers.change_params_or()."""
    actual = nb_helpers.change_params_or(params_ld=params_ld)
    assert actual == expected


@pytest.mark.parametrize("max_len, values, expected", [
    (2047, [], [(0, 1)]),
    (2047, [p.IP1], [(0, 1)]),
    (1, [p.IP1], [(0, 1)]),
    (1, [p.IP1, p.IP2], [(0, 1), (1, 2)]),
    (1, [p.IP1, p.IP2, p.IP3], [(0, 1), (1, 2), (2, 3)]),
    (130, [p.IP1, p.IP2, p.IP3], [(0, 2), (2, 3)]),
    (130, [p.IP1, p.IP2, p.IP3, p.IP4], [(0, 2), (2, 4)]),
    (145, [p.IP1, p.IP2, p.IP3, p.IP4], [(0, 3), (3, 4)]),
])
def test__generate_slices(max_len, values, expected):
    """nb_helpers.generate_slices()."""
    query: str = urlencode([("family", 4), ("status", "active"), ("offset", 1000), ("limit", 1000)])
    actual = nb_helpers.generate_slices(
        url=f"https://domain.com?{query}",
        max_len=max_len,
        key="address",
        values=values,
    )
    assert actual == expected


@pytest.mark.parametrize("url, max_len, key, params_d, expected", [
    ("https://domain.com", 2047, "address", {"address": [p.IP1, p.IP2], "family": 4},
     [{"address": [p.IP1, p.IP2], "family": 4}]),
    ("https://domain.com", 50, "address", {"address": [p.IP1, p.IP2], "family": 4},
     [{"address": p.IP1, "family": 4}, {"address": p.IP2, "family": 4}]),
    ("https://domain.com", 50, "prefix", {"prefix": [p.IP1, p.IP2], "family": 4},
     [{"prefix": p.IP1, "family": 4}, {"prefix": p.IP2, "family": 4}]),
])
def test__slice_params_d(url, max_len, key, params_d, expected):
    """nb_helpers.slice_params_d()."""
    actual = nb_helpers.slice_params_d(url=url, max_len=max_len, key=key, params_d=params_d)
    assert actual == expected


@pytest.mark.parametrize("url, max_len, keys, params, expected", [
    ("https://domain.com", 2047, ["address"], [], [{}]),
    ("https://domain.com", 2047, ["address"], [{}], [{}]),  # no need slice
    ("https://domain.com", 50, [], [{"address": [p.IP1, p.IP2], "family": [4]}],
     [{"address": [p.IP1, p.IP2], "family": [4]}]),  # need slice

    ("https://domain.com", 50, ["prefix"], [{"address": [p.IP1, p.IP2], "family": [4]}],
     [{"address": [p.IP1, p.IP2], "family": [4]}]),  # no need slice
    ("https://domain.com", 50, ["address"], [{"address": [p.IP1, p.IP2], "family": [4]}],
     [{"address": p.IP1, "family": [4]}, {"address": p.IP2, "family": [4]}]),  # need slice
])
def test__slice_params_ld(url, max_len, keys, params, expected):
    """nb_helpers.slice_params_ld()."""
    actual = nb_helpers.slice_params_ld(url=url, max_len=max_len, keys=keys, params_ld=params)
    assert actual == expected


@pytest.mark.parametrize("urls, expected", [
    ([], []),
    (["a/b/c/d/1"], ["a/b/c/d?id=1"]),
    (["a/b/c/d/2", "a/b/c/d/1"], ["a/b/c/d?id=1&id=2"]),
    (["a/b/c/D/3", "a/b/c/d/2", "a/b/c/d/1"], ["a/b/c/D?id=3", "a/b/c/d?id=1&id=2"]),
    (["a/b/c/d/2", "a/b/c/d/1", "a/b/c/D/3"], ["a/b/c/D?id=3", "a/b/c/d?id=1&id=2"]),
])
def test__join_urls(urls, expected):
    """ami.join_urls()"""
    actual = nb_helpers.join_urls(urls=urls)
    assert actual == expected


@pytest.mark.parametrize("url, max_len, expected", [
    (f"https://domain.com?address={p.IP1}&address={p.IP2}", 2047,
     [f"https://domain.com?address={p.IP1_}&address={p.IP2_}"]),
    (f"https://domain.com?address={p.IP1}&address={p.IP2}", 50,
     [f"https://domain.com?address={p.IP1_}", f"https://domain.com?address={p.IP2_}"]),
])
def test__slice_url(url, max_len, expected):
    """nb_helpers.slice_url()."""
    actual = nb_helpers.slice_url(url=url, max_len=max_len)
    assert actual == expected


@pytest.mark.parametrize("values, expected", [
    ("", [""]),
    (0, [0]),
    ([], []),
    ([""], [""]),
    ([0], [0]),
    ([1, 2, 1], [1, 2]),
])
def test__validate_values(values, expected):
    """nb_helpers._validate_values()."""
    actual = nb_helpers._validate_values(values=values)
    assert actual == expected


@pytest.mark.parametrize("params_d, expected", [
    ({}, ""),
    ({"a": [1]}, "a"),
    ({"a": "1"}, "a"),
    ({"a": [100, 200], "b": ["0001", "0002"]}, "b"),
])
def test__get_key_of_longest_value(params_d, expected):
    """nb_helpers.get_key_of_longest_value()."""
    actual = nb_helpers.get_key_of_longest_value(params_d=params_d)
    assert actual == expected


@pytest.mark.parametrize("count, limit, params_d, expected", [
    (10, 10, {}, [{"limit": 10, "offset": 0}]),
    (10, 10, {"a": 1}, [{"a": 1, "limit": 10, "offset": 0}]),
    (20, 10, {}, [{"limit": 10, "offset": 0}, {"limit": 10, "offset": 10}]),
    (0, 10, {}, ValueError),
    (10, 0, {}, ValueError),
])
def test__generate_offsets(count: int, limit: int, params_d, expected: Any):
    """nb_helpers.generate_offsets()."""
    if isinstance(expected, list):
        actual = nb_helpers.generate_offsets(count, limit, params_d)
        assert actual == expected
    else:
        with pytest.raises(expected):
            nb_helpers.generate_offsets(count, limit, params_d)
