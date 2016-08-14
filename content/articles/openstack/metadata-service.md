Title: The path of the metadata service in OpenStack
Tags: openstack, neutron, nova
Status: draft
Date: 2016-01-01

The intention of this article is to explain how the metadata service works
from an operator point of view, what you should be watching while you're
troubleshooting or what kind of things you could be considering as 'normal'.

# Scenario

- This is an environment using Neutron (nova-network is not in the picture)
- Neutron is configured to use openvswitch
- This applies to Juno, but as far as I know, Icehouse is not different.

# What is the metadata service?

Le
