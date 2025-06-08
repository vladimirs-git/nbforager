"""Tests ipv4.py."""
import pytest

from nbforager.foragers.ipv4 import IPv4


def test__init():
    """IPv4.__init__()."""
    ipv4 = IPv4("10.0.0.1/24")
    assert ipv4.ip == "10.0.0.1"
    assert ipv4.ipv4 == "10.0.0.1/24"
    assert ipv4.net == "10.0.0.0/24"
    assert ipv4.prefixlen == 24

    with pytest.raises(ValueError):
        IPv4("10.0.0.1/24", strict=True)

    ipv4 = IPv4("10.0.0.1/32")
    assert ipv4.ip == "10.0.0.1"
    assert ipv4.ipv4 == "10.0.0.1/32"
    assert ipv4.net == "10.0.0.1/32"
    assert ipv4.prefixlen == 32


@pytest.mark.parametrize("cidr1, cidr2, expected", [
    ("10.0.0.0/24", "10.0.0.0/24", True),  # same prefix
    ("10.0.0.1/24", "10.0.0.1/24", True),  # same address
    ("10.0.0.1/24", "10.0.0.0/24", False),  # different IPs, same prefix
    ("10.0.0.0/24", "10.0.0.0/25", False),  # different prefix
    ("10.0.0.1/24", "10.0.0.1/25", False),  # different prefix
    ("10.0.1.0/24", "10.0.0.0/24", False),  # different prefix
])
def test__eq__(cidr1, cidr2, expected):
    """Test IPv4.__eq__()."""
    actual = IPv4(cidr1) == IPv4(cidr2)
    assert actual is expected

@pytest.mark.parametrize("cidr1, cidr2, expected", [
    ("10.0.0.0/23", "10.0.0.0/24", True),  # network < network
    ("10.0.0.0/23", "10.0.0.1/24", True),    # network < host IP
    ("10.0.0.0/24", "10.0.0.1/24", True),    # network < host IP
    ("10.0.0.1/24", "10.0.0.2/24", True),    # IP .1 < IP .2
    ("10.0.0.2/24", "10.0.0.1/24", False),   # IP .2 !< IP .1
])
def test__lt__(cidr1, cidr2, expected):
    """Test IPv4.__lt__()."""
    actual = IPv4(cidr1) < IPv4(cidr2)
    assert actual is expected

@pytest.mark.parametrize("cidr1, expected", [
    (["10.0.0.0/24", "10.0.0.0/23", "10.0.0.1/24", "10.0.0.1/23"],
     ["10.0.0.0/23", "10.0.0.0/24", "10.0.0.1/23", "10.0.0.1/24"]),
])
def test__lt__sorting(cidr1, expected):
    """Test IPv4.__lt__() sorting."""
    results = sorted(cidr1)

    actual = [str(o) for o in results]
    assert actual == expected

@pytest.mark.parametrize("subnet, supernet, expected", [
    ("10.0.0.0/24", "10.0.0.0/23", True),
    ("10.0.0.1/24", "10.0.0.0/23", True),
    ("10.0.0.0/24", "10.0.0.0/24", True),
    ("10.0.0.1/24", "10.0.0.0/24", True),
    ("10.0.0.0/24", "10.0.0.0/25", False),
    ("10.0.0.1/24", "10.0.0.0/25", False),
    ("10.0.0.0/32", "10.0.0.0/32", True),
    ("10.0.0.1/32", "10.0.0.0/32", False),

])
def test__contains__(subnet, supernet, expected):
    """IPv4.__contains__()."""
    actual = IPv4(subnet) in IPv4(supernet)
    assert actual == expected
