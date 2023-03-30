Title: Multiple Local Environments with Juju
date: 2015-01-23
tags: juju

![juju man](/images/JuJu-man.png)

[Juju](https://juju.ubuntu.com/) has the ability to use lxc or kvm to deploy
services, this is done by the
[local provider](https://juju.ubuntu.com/docs/config-local.html), but
sometimes during development you may want to have one environment up-n-running
all the time for testing and you may need another one to run
[amulet](https://juju.ubuntu.com/docs/tools-amulet.html) tests, well at the
beginning this wasn't obvious to me that this could be achieved, but then I
found how to do it :)

Here is how you can have two different environments:

    environments:
      local:
        type: local
        default-series: trusty
        lxc-clone: true
        container: kvm
        network-bridge: br0
      lxc:
        type: local
        default-series: trusty
        lxc-clone: true
        network-bridge: lxcbr0
        state-port: 37018
        api-port: 17071

That is the relevant portion of my `~/.juju/environments.yaml`, I use one environment with `kvm` and the other one with `lxc`.

If you're curious, the trick is to change the `state-port` and `api-port`.

I hope this helps you.
