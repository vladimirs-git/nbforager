"""Tests py_tree.py."""

from nbforager.py_tree import PyTree


def test__pynb_tree():
    """PyTree"""
    tree = PyTree()
    actual = list(tree.__annotations__)
    expected = [
        "circuits",
        "core",
        "dcim",
        "extras",
        "ipam",
        "tenancy",
        "users",
        "virtualization",
        "wireless",
    ]
    assert actual == expected
