Title: OpenStack Cinder and Ceph: snapshots and volumes
Date: 2015-04-02
Category: OpenStack
Tags: openstack, cinder, ceph
Status: draft

When you want to deploy OpenStack you have to make a lot of decisions, like
what networking gear you are gonna use, what hypervisor and so on, when it
gets to 'what cinder backend' a common decision is to use
[Ceph](http://ceph.com/), but how cinder uses ceph?, here I'm trying to
provide some answers and solutions to known quirks.


Volumes
=======

Each "cinder volume" maps to a
["ceph image"](http://ceph.com/docs/master/rbd/rados-rbd-cmds/) inside of a
["ceph pool"](http://ceph.com/docs/master/rados/operations/pools/), the ceph
pool used by cinder is defined in /etc/cinder/cinder.conf configuration key
`rbd_pool`, if you're using juju to deploy your cloud then this is set to `cinder-ceph`

In the ceph world is all about how to optimize disk space usage, so every time
a user creates a snapshot, which is a cheap operation in ceph, a reference to
that point in time is created, this is read-only and at the beginning it won't
be using disk space, but as the volume snapshoted starts to change, then the
snapshot starts using space on disk.

Another operation after you created a snapshot is create a new cinder volume
using as source (or based on) a snapshot, at this point ceph will create a
copy-on-write image, so if the user creates a volume but it's not used, then
actual disk space used is minimum.


