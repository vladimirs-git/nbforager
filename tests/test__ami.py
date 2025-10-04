"""Tests ami.py."""
from typing import Any

import pytest

from nbforager import ami
from nbforager.exceptions import NbApiError
from nbforager.nb_forager import NbForager


@pytest.mark.parametrize("app, model, expected", [
    ("dcim", "console_port_templates", "dcim.consoleporttemplate"),
    ("dcim", "interfaces", "dcim.interface"),
    ("dcim", "virtual_chassis", "dcim.virtualchassis"),
    ("ipam", "ip_addresses", "ipam.ipaddress"),
    ("ipam", "prefixes", "ipam.prefix"),
    ("virtualization", "interfaces", "virtualization.vminterface"),
])
def test__am_to_object_type(app, model, expected):
    """ami.am_to_object_type()."""
    actual = ami.am_to_object_type(app=app, model=model)

    assert actual == expected


@pytest.mark.parametrize("obj, expected", [
    (NbForager(host="netbox"), "nb_forager"),
    (NbForager(host="netbox").ipam, "ipam"),
])
def test__attr_name(obj, expected):
    """ami.attr_name()"""
    actual = ami.attr_name(obj)
    assert actual == expected


def test__attr_names():
    """ami.attr_names()"""
    nbf = NbForager(host="netbox")
    actual = ami.attr_names(nbf.wireless)
    expected = ["wireless_lan_groups", "wireless_lans", "wireless_links"]
    assert actual == expected


@pytest.mark.parametrize("model, expected", [
    ("", ""),
    ("model", "model"),
    ("model-group", "model-group"),
    ("model_group", "model-group"),
    ("-model--group-", "-model--group-"),
    ("_model__group_", "-model--group-"),
])
def test__attr_to_model(model, expected):
    """ami.attr_to_model()"""
    actual = ami.attr_to_model(model)
    assert actual == expected


@pytest.mark.parametrize("model, expected", [
    ("", ""),
    ("model", "model"),
    ("model-group", "model_group"),
    ("model_group", "model_group"),
    ("-model--group-", "_model__group_"),
    ("_model__group_", "_model__group_"),
])
def test__model_to_attr(model, expected):
    """ami.model_to_attr()"""
    actual = ami.model_to_attr(model)
    assert actual == expected


@pytest.mark.parametrize("nb_objects, expected", [
    ([], []),
    ([{"url": "a"}], ["a"]),
    ([{"tags": ["a"]}], []),
    ([{"tags": [{"a": "a"}]}], []),
    ([{"tags": [{"url": "a"}]}], ["a"]),
    ([{"tags": {"a": "a"}}], []),
    ([{"tags": {"url": "a"}}], ["a"]),
    ([{"url": "a", "tags": [{"url": "b"}, {"url": "c"}]}], ["a", "b", "c"]),
    ([{"tags": [{"url": "a"}, {"url": "a"}]}], ["a"]),
])
def test__nested_urls(nb_objects, expected):
    """ami.nested_urls()"""
    actual = ami.nested_urls(nb_objects=nb_objects)
    assert actual == expected


@pytest.mark.parametrize("path, expected", [
    ("", ValueError),
    ("typo", ValueError),
    ("app/model", ("app", "model")),
    ("/app/model/", ("app", "model")),
    ("app/model_group", ("app", "model_group")),
    ("app/model-group", ("app", "model_group")),
])
def test__path_to_attrs(path, expected: Any):
    """ami.path_to_attrs()"""
    if isinstance(expected, tuple):
        actual = ami.path_to_attrs(path)
        assert actual == expected
    else:
        with pytest.raises(expected):
            ami.path_to_attrs(path)


@pytest.mark.parametrize("plural, expected", [
    ("console_port_templates", "consoleporttemplate"),
    ("console-port-templates", "consoleporttemplate"),
    ("interfaces", "interface"),
    ("virtual_chassis", "virtualchassis"),
    ("ip_addresses", "ipaddress"),
    ("prefixes", "prefix"),
    ("interfaces", "interface"),
])
def test__model_singular(plural, expected):
    """ami.model_singular()."""
    actual = ami.model_singular(plural=plural)

    assert actual == expected


@pytest.mark.parametrize("word, expected", [
    ("", ""),
    ("Text", "text"),
    ("TextText", "text_text"),
    ("TextTextText", "text_text_text"),
])
def test__replace_upper(word, expected):
    """ami.replace_upper()"""
    actual = ami.replace_upper(word)
    assert actual == expected


@pytest.mark.parametrize("url, expected", [
    # ui
    ("", ("", "", "")),
    ("typo", ("", "", "")),
    ("https://nb", ("", "", "")),
    ("https://nb/app", ("", "", "")),
    ("https://nb/app/model", ("app", "model", "")),
    ("https://nb/app/model/12", ("app", "model", "12")),
    ("https://nb/app/model/12/path", ("app", "model", "12")),
    ("https://nb/app/model/12|path", ("app", "model", "12")),
    ("https://nb/app/model/12?k=v", ("app", "model", "12")),
    ("https://nb/app/model/12path", ("app", "model", "12")),
    ("https://nb/app/mo-del", ("app", "mo-del", "")),
    ("https://nb/app/mo-del/12", ("app", "mo-del", "12")),
    ("https://nb/app/model/typo", ("", "", "")),
    ("https://nb/app/model/typo/12", ("", "", "")),
    # api
    ("https://nb/api/app", ("", "", "")),
    ("https://nb/api/app/model", ("app", "model", "")),
    ("https://nb/api/app/model/12", ("app", "model", "12")),
    ("https://nb/api/app/model/12/path", ("app", "model", "12")),
    ("https://nb/api/app/model/12|path", ("app", "model", "12")),
    ("https://nb/api/app/model/12?k=v", ("app", "model", "12")),
    ("https://nb/api/app/model/12path", ("app", "model", "12")),
    ("https://nb/api/app/mo-del", ("app", "mo-del", "")),
    ("https://nb/api/app/mo-del/12", ("app", "mo-del", "12")),
    ("https://nb/api/app/model/typo", ("", "", "")),
    ("https://nb/api/app/model/typo/12", ("", "", "")),
])
def test__url_to_ami_items(url, expected):
    """ami.url_to_ami_items()"""
    actual = ami.url_to_ami_items(url=url)
    assert actual == expected


@pytest.mark.parametrize("url, path, expected", [
    # attr
    ("https://nb/api/ipam/ip-addresses/12", False, ("ipam", "ip_addresses", 12)),
    ("https://nb/api/ipam/ip-addresses/12/", False, ("ipam", "ip_addresses", 12)),
    ("https://nb/api/ipam/ip-addresses/12?k=v", False, ("ipam", "ip_addresses", 12)),
    ("https://nb/api/ipam/ip-addresses", False, ("ipam", "ip_addresses", 0)),
    ("https://nb/api/ipam/ip-addresses/", False, ("ipam", "ip_addresses", 0)),
    # path
    ("https://nb/api/ipam/ip-addresses/12", True, ("ipam", "ip-addresses", 12)),
    # invalid
    ("", False, NbApiError),
    ("typo", False, NbApiError),
    ("https://nb", False, NbApiError),
    ("https://nb/api", False, NbApiError),
    ("https://nb/api/ipam", False, NbApiError),
    ("https://nb/api/ipam/ip-addresses/path/1", False, NbApiError),
    ("https://nb/api/ipam/12/34", False, NbApiError),
    ("https://nb/api/1/ip-addresses/12", False, NbApiError),
])
def test__url_to_ami(url, path, expected):
    """ami.url_to_ami()"""
    if isinstance(expected, tuple):
        actual = ami.url_to_ami(url=url, path=path)
        assert actual == expected
    else:
        with pytest.raises(expected):
            ami.url_to_ami(url=url, path=path)


@pytest.mark.parametrize("url, expected", [
    ("https://nb/api/app/model/1?k=v", "app/model/"),
    ("https://nb/api/app/model/1/", "app/model/"),
    ("https://nb/api/app/model/1", "app/model/"),
    ("https://nb/api/app/model", "app/model/"),
    ("", ValueError),
    ("typo", ValueError),
])
def test__url_to_am_path(url, expected):
    """ami.url_to_am_path()"""
    if isinstance(expected, str):
        actual = ami.url_to_am_path(url=url)
        assert actual == expected
    else:
        with pytest.raises(expected):
            ami.url_to_am_path(url=url)


@pytest.mark.parametrize("url, expected", [
    ("https://nb/api/app/model/1?k=v", "app/model/1/"),
    ("https://nb/api/app/model/1/", "app/model/1/"),
    ("https://nb/api/app/model/1", "app/model/1/"),
    ("https://nb/api/app/model", ValueError),
    ("", ValueError),
    ("typo", ValueError),
])
def test__url_to_ami_path(url, expected):
    """ami.url_to_ami_path()"""
    if isinstance(expected, str):
        actual = ami.url_to_ami_path(url=url)
        assert actual == expected
    else:
        with pytest.raises(expected):
            ami.url_to_ami_path(url=url)


@pytest.mark.parametrize("url, expected", [
    ("https://nb/api/ipam/ip-address/1?k=v", "/api/ipam/ip-address/1/"),
    ("https://nb/api/ipam/ip-address/1/", "/api/ipam/ip-address/1/"),
    ("https://nb/api/ipam/ip-address/1", "/api/ipam/ip-address/1/"),
    ("https://nb/api/ipam/ip-address", "/api/ipam/ip-address/"),
    ("https://nb/api/ipam", NbApiError),
    ("https://nb/api", NbApiError),
    ("https://nb", NbApiError),
    ("", NbApiError),
])
def test__url_to_ami_url(url, expected):
    """ami.url_to_ami_url()"""
    if isinstance(expected, str):
        actual = ami.url_to_ami_url(url=url)
        assert actual == expected
    else:
        with pytest.raises(expected):
            ami.url_to_ami_url(url=url)


@pytest.mark.parametrize("url, expected", [
    # ui
    ("https://nb/ipam/ip-address/1?k=v", "https://nb/api/ipam/ip-address/1/"),
    ("https://nb/ipam/ip-address/1/", "https://nb/api/ipam/ip-address/1/"),
    ("https://nb/ipam/ip-address/1", "https://nb/api/ipam/ip-address/1/"),
    ("https://nb/ipam/ip-address", "https://nb/api/ipam/ip-address/"),
    # api
    ("https://nb/api/ipam/ip-address/1?k=v", "https://nb/api/ipam/ip-address/1/"),
    ("https://nb/api/ipam/ip-address/1/", "https://nb/api/ipam/ip-address/1/"),
    ("https://nb/api/ipam/ip-address/1", "https://nb/api/ipam/ip-address/1/"),
    ("https://nb/api/ipam/ip-address", "https://nb/api/ipam/ip-address/"),
    # invalid
    ("https://nb/api/ipam", NbApiError),
    ("https://nb/api", NbApiError),
    ("https://nb", NbApiError),
    ("", NbApiError),
])
def test__url_to_api_url(url, expected):
    """ami.url_to_api_url()"""
    if isinstance(expected, str):
        actual = ami.url_to_api_url(url=url)
        assert actual == expected
    else:
        with pytest.raises(expected):
            ami.url_to_api_url(url=url)


@pytest.mark.parametrize("url, expected", [
    # ui
    ("https://nb/extras/changelog/", "https://nb/extras/changelog/"),
    ("https://nb/core/changelog/", "https://nb/core/changelog/"),
    ("https://nb/ipam/ip-address/1?k=v", "https://nb/ipam/ip-address/1?k=v"),
    ("https://nb/ipam/ip-address/1/", "https://nb/ipam/ip-address/1/"),
    ("https://nb/ipam/ip-address/1", "https://nb/ipam/ip-address/1"),
    ("https://nb/ipam/ip-address", "https://nb/ipam/ip-address"),
    # api
    ("https://nb/api/extras/object-changes/", "https://nb/extras/changelog/"),
    ("https://nb/api/core/object-changes/", "https://nb/core/changelog/"),
    ("https://nb/api/ipam/ip-address/1?k=v", "https://nb/ipam/ip-address/1?k=v"),
    ("https://nb/api/ipam/ip-address/1/", "https://nb/ipam/ip-address/1/"),
    ("https://nb/api/ipam/ip-address/1", "https://nb/ipam/ip-address/1"),
    ("https://nb/api/ipam/ip-address", "https://nb/ipam/ip-address"),
    # invalid
    ("https://nb/api/ipam", "https://nb/ipam"),
    ("https://nb/api", "https://nb/api"),
    ("https://nb", "https://nb"),
    ("", ""),

])
def test__url_to_ui(url, expected):
    """ami.url_to_ui()"""
    if isinstance(expected, str):
        actual = ami.url_to_ui(url=url)
        assert actual == expected
    else:
        with pytest.raises(expected):
            ami.url_to_ui(url=url)
