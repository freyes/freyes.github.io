Title: Mikrotik OpenVPN Setup
Date: 2016-8-14
Tags: mikrotik, openvpn, networking
Status: draft

# Scenario

* Site A
    * OpenVPN Server
    * LAN: 192.168.88.0/24
    * WAN connected to interface ether1-gateway
* Site B
    * OpenVpn Client
    * LAN: 192.168.20.0/24
* Road Warrior (laptop)


## Requirements

* Nodes connected to any network should be able to connect any other node via
routes

# Certificates creation

...

# Server configuration

1. Create bridge for the VPN clients

    ```
/interface bridge add bridge=vpn-bridge
    ```

1. Create a pool of IP addresses to be used by the dhcp clients without a
binding for their account

    ```
/ip pool add name=ovpn ranges=172.20.20.21-172.20.20.99
```

1. Create the default encryption profile to be used by the server

    ```
    /ppp profile
    set *FFFFFFFE \
  bridge=vpn-bridge \
  change-tcp-mss=default \
  local-address=172.20.20.1 \
  remote-address=ovpn \
  use-encryption=required
  ```

1. Create encryption profiles, you have to create 1 profile per client, this
   is needed to allow set specific IP addresses per client, and once they are
   connected they can be clearly identified and eventually apply firewall
   rules in case it's needed

    ```
/ppp profile add name=ovpn-siteA \
    bridge=vpn-bridge \
    local-address=172.20.20.30 \
    remote-address=172.20.20.31 \
    use-encryption=required
```

1. Create user, you have to create 1 user per client as the user is related to
   the encryption profile previously created

    ```/ppp secret add name=siteA password=foobar profile=ovpn-siteA service=ovpn
    ```

1. Configure the server (encryption methods, certificates, etc)

    ```
/interface ovpn-server \
  set auth=sha1 \
  certificate=deathstar.crt_0 \
  cipher=aes256 \
  default-profile=default \
  enabled=yes \
  keepalive-timeout=disabled \
  require-client-certificate=yes
  ```

1. Create 1 OpenVPN server binding pero user created. This will create a
   static interface per user allowing the manipulation of its traffic.

    ```/interface ovpn-server add name=ovpn-siteA user=siteA
    ```
