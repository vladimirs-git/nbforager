
.. :changelog:

CHANGELOG
=========

1.0.0 (2025-07-28)
-------------------

**Added:** all models in v4.3.4

**Changed:** Breaking changes. If offset is in filtering parameters, send only one request.

**Added:** loners "family" to ipam/aggregates, ipam/prefixes, ipam/ip-addresses

**Added:** Connector.get_count()

**Deleted:** default_get parameter


0.8.13 (2025-07-04)
-------------------

**Changed:** dependencies netports-1.1.0


0.8.12 (2025-06-30)
-------------------

**Changed:** dependencies python-3.8, netports-1.0.3


0.8.9 (2025-06-14)
------------------

**Deleted:** IPv4, moved to netports-0.18.1

**Changed:** IPv4.ipv4 > IPv4.cidr


0.8.5 (2025-06-10)
------------------

**Fixed:** IPv4(strict)


0.8.4 (2025-06-08)
------------------

**Changed:** IPv4 using ipaddress

**Deleted:** ciscoconfparse


0.8.3 (2025-06-01)
------------------

**Added:** helpers DEPENDENT_MODELS, dependency_ordered_paths()
**Added:** NbApi.connectors()
**Added:** BaseC._add_params_limit_offset()
**Fixed:** threading mode for nested URLs


0.7.0 (2025-05-17)
------------------

**Changed:** python 3.11, dependency


0.6.0 (2025-05-05)
------------------

**Deleted:** pynetbox


0.5.0 (2025-03-01)
------------------

**Fixed:** NbForager.clear() tree
**Fixed:** rename base_ca.py > base_ac.py
**Added:** APPS replaced by NbApi.apps()
**Changed:** dependencies


0.4.1 (2024-11-13)
------------------

**Added:** nb_tree.am_to_object_type()


0.4.0 (2024-10-30)
------------------

**Added:** NbApi.get()


0.3.8 (2024-10-29)
------------------

**Fixed:** object_type_to_am() vminterface


0.3.7 (2024-10-25)
------------------

**Fixed:** helpers.object_type_to_am()


0.3.6 (2024-10-23)
------------------

**Added:** helpers.object_type_to_am()

**Fixed:** BaseC._query_count() offset


0.3.5 (2024-09-14)
------------------

**Added:** helper.url_to_api_url()

**Added:** Forager._delete_existing_nested_ids()

**Added:** NbApi.threads

**Added:** copy(NbApi)

**Changed:** NbParser.str() by list index

**Changed:** Joiner.join_tree()

**Fixed:** Slice nested URLs in threading mode

**Fixed:** generate_slices()


0.3.0 (2024-07-23)
------------------

**Added:** helpers.url_to_ami_path(url)

**Added:** NbApi.create(url) NbApi.create_d(url) NbApi.delete(url) NbApi.update(url)

**Added:** NbTree.clear()

**Added:** extra_key dcim.devices _virtual_chassis_members

**Changed:** Joiner with kwargs filters

**Changed:** NbTree.__repr__()

**Changed:** netports.vdict.pop()

**Fixed:** NbCustom.platform_slug()


0.2.4 (2024-07-14)
------------------

**Changed:** poetry dependencies


0.2.3 (2024-06-09)
------------------

**Changed:** NbCache._create_dir() logging.info


0.2.2 (2024-05-11)
------------------

**Added:** BaseC._slices = ["device_id", ...]


0.2.1 (2024-03-29)
------------------

**Fixed:** BaseC._slice_params_counters()

**Changed:** NbForager.clear(root, tree)

**Changed:** NbForager.join_tree(dcim, ipam)


0.2.0 (2024-03-11)
------------------

**Fixed:** NbApi.extended_get = True, NbForager.extended_get = True

**Fixed:** NbApi.ipam.vlan_groups

**Changed:** NbValue.status() > NbValue.status_value() and similar methods

**Changed:** LONERS {"ipam/vlan-groups/": ["site"]}

**Added:** NbParser.bool()

**Added:** NbValue.slug() NbValue.vlan_name()

**Added:** NbCustom.cf_recommended_vlans() NbCustom.cf_required_env()


0.1.15 (2024-02-03)
-------------------
* [fix] NbCustom.platform_slug()


0.1.14 (2024-01-30)
-------------------

**Added:** init
