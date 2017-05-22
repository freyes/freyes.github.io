Title: Add remote lxd server as a cloud in Juju (2.x)
date: 2017-05-21
tags: juju, lxd, ubuntu

[Juju 2.x](https://jujucharms.com/) have the ability to add
[LXD](https://linuxcontainers.org/lxd/) as [a
provisioner](https://jujucharms.com/docs/stable/clouds-LXD), by default it can
easily use a local lxd (`juju bootstrap lxd`), but how could we use a remote
lxd?, the following instructions will guide you to achieve this:

SSH into the remote server (e.g. `192.168.10.2`) and configure lxd to accept
incoming connections and set a password.

```
(192.168.10.2)$ lxc config set core.https_address "[::]"
(192.168.10.2)$ lxc config set core.trust_password some-secret-string
```

Now in the machine where juju commands will be ran (A.K.A. juju client) add the
remote lxd daemon, this is done to easily get the server's certificate.

```
(juju-client)$ lxc remote add 192.168.10.2 --accept-certificate --password=some-secret-string
```

Create a yaml configuration file that will be used by juju to add the cloud,
this is how it should look like.

```yaml
# file: some-remote.yaml
clouds:
  some-remote:
    type: lxd
    auth-types: [interactive, certificate]
    regions:
      some-remote:
        endpoint: 192.168.10.2
```

Add the cloud definition to juju:

```
(juju-client)$ juju add-cloud some-remote some-remote.yaml
```

Create the credentials.yaml file:

```yaml
# file: credentials.yaml
some-remote:
  some-remote:
    auth-type: certificate
    client-cert: |
      -----BEGIN CERTIFICATE-----
      ...
      INSERT THE CONTENT OF ~/.config/lxc/client.crt
      ...
      -----END CERTIFICATE-----
    client-key: |
      -----BEGIN RSA PRIVATE KEY-----
      ...
      INSERT THE CONTENT OF ~/.config/lxc/client.key
      ...
      -----END RSA PRIVATE KEY-----
    server-cert: |
      -----BEGIN CERTIFICATE-----
      ...
      INSERT THE CONTENT OF ~/.config/lxc/client.crt
      ...
      -----END CERTIFICATE-----
```

Add the credentials to juju:

```
(juju-client)$ juju add-credential some-remote -f credentials.yaml
```

Verify the cloud was added correctly:

```
(juju-client)$ juju clouds
Cloud           Regions  Default          Type            Description
aws                  14  us-east-1        ec2             Amazon Web Services
aws-china             1  cn-north-1       ec2             Amazon China
aws-gov               1  us-gov-west-1    ec2             Amazon (USA Government)
azure                24  centralus        azure           Microsoft Azure
azure-china           2  chinaeast        azure           Microsoft Azure China
cloudsigma            5  hnl              cloudsigma      CloudSigma Cloud
google                7  us-east1         gce             Google Cloud Platform
joyent                6  eu-ams-1         joyent          Joyent Cloud
oracle-compute        5  uscom-central-1  oracle-compute  Oracle Cloud
rackspace             6  dfw              rackspace       Rackspace Cloud
localhost             1  localhost        lxd             LXD Container Hypervisor
some-remote           1  some-remote      lxd             LXD Container Hypervisor

Try 'list-regions <cloud>' to see available regions.
'show-cloud <cloud>' or 'regions --format yaml <cloud>' can be used to see region endpoints.
'add-cloud' can add private clouds or private infrastructure.
Update the known public clouds with 'update-clouds'.
```

Bootstrap a new controller using the added cloud provider

```
(juju-client)$ juju bootstrap some-remote
```

Once the bootstrap is done, verify the controller was correctly spun in the
remote lxd daemon:

```
(juju-client)$ lxc list 192.168.10.2:
+---------------+---------+--------------------------------+------+------------+-----------+
|     NAME      |  STATE  |              IPV4              | IPV6 |    TYPE    | SNAPSHOTS |
+---------------+---------+--------------------------------+------+------------+-----------+
| juju-ec8b3d-0 | RUNNING | 192.168.10.42 (eth0)           |      | PERSISTENT | 0         |
+---------------+---------+--------------------------------+------+------------+-----------+
(juju-client)$ juju status -m controller
Model       Controller   Cloud/Region             Version
controller  snowspeeder  snowspeeder/snowspeeder  2.1.2

App  Version  Status  Scale  Charm  Store  Rev  OS  Notes

Unit  Workload  Agent  Machine  Public address  Ports  Message

Machine  State    DNS            Inst id        Series  AZ  Message
0        started  192.168.10.42  juju-ec8b3d-0  xenial      Running

```