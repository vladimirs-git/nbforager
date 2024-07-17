"""Params nbforager.nb_forager.py."""

FIND = [
    ({}, [1, 2, 3, 4]),
    ({"id": 1}, [1]),
    ({"id": 9}, []),
    ({"id": [1, 2, 9]}, [1, 2]),  # list
    ({"id": (1, 2, 9)}, [1, 2]),  # tuple
    ({"id": {1, 2, 9}}, [1, 2]),  # set
    ({"name": "DEVICE1"}, [1]),
    ({"name": ["DEVICE1", "DEVICE2", "typo"]}, [1, 2]),
    ({"serial": "SERIAL1"}, [1, 3]),
    ({"name": "DEVICE1", "serial": "SERIAL1"}, [1]),
    ({"name": "DEVICE1", "serial": "SERIAL2"}, []),
    ({"name": ["DEVICE1", "DEVICE3"], "serial": ["SERIAL1", "typo"]}, [1, 3]),
    ({"name": ["DEVICE1", "DEVICE2"], "serial": ["SERIAL1", "SERIAL2"]}, [1, 2]),
    ({"name": ["DEVICE1", "DEVICE3"], "serial": ["SERIAL1", "SERIAL2"]}, [1, 3]),
    # "__"
    ({"device_type__name": "MODEL1"}, [1, 2]),
    ({"device_type__name": "MODEL3"}, [3, 4]),
    ({"device_type__name_typo": "MODEL3"}, []),
    ({"device_type__name": ["MODEL1", "MODEL3"], "serial": ["SERIAL1"]}, [1, 3]),
    ({"device_type__name": ["MODEL1", "MODEL3"], "serial": ["SERIAL2"]}, [2]),
    ({"device_type__name": ["MODEL1", "MODEL3"], "serial": ["SERIAL1", "SERIAL2"]}, [1, 2, 3]),
    # tags
    ({"tags__name": "TAG1"}, [1, 2]),
    ({"tags__name": ["TAG3"]}, [3]),
    ({"tags__name__typo": "TAG3"}, ValueError),
]
