
.. :changelog:

CHANGELOG
=========

0.3.0 (2024-07-21)
------------------

**Added:** NbTree.clear()

**Added:** extra_key dcim.devices _virtual_chassis_members

**Changed:** Joiner with **kwargs filters

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
