---
title: "Homelab - Part 1 - Basic network"
date: 2023-10-13T10:50:42+02:00
summary: "How to setup a basic homelab network with a pi-hole"
tags: ["network", "wireguard", "vpn", "pi-hole"]
categories: ["Homelab"]
series: ["Homelab"]
series_order: 1
author: "0xNinja"
draft: true
---

Let me guide you through my journey for a simple homelab.

## Introduction

The idea of this article is to document how I did things and why, and to help me remember how to setup X and Y if needed.

## Plans

We want to go from a basic setup to something simple:

| Before | After |
|---|---|
| {{< mermaid >}}
flowchart TD
    A[Internet] --> B[IAP box]
    B --> C[LAN]
{{< /mermaid >}} | {{< mermaid >}}
flowchart TD
    A[Internet] --> B[IAP box]
    B --> C[pi-hole]
    C --> D[LAN]
{{< /mermaid >}} |

Doing so will allow us to manage and customize our network using our pi-hole, it will be the authority for many core services such as DNS or DHCP.

In the future I will show different setups and how I did them.

## Setup your IAP box

In order to setup our network, we will need to do some tweaks:

* Force a static IP for our pi-hole
* Set the DNS to our pi-hole
* Disable the DHCP to let our pi-hole do it

Depending on your model and provider those steps will be different, google is your friend.

## Install pi-hole

First, assing a static IP on your machine if you can't set a static lease on your internet box.

I installed pi-hole on a RPI4 using `pip install pi-hole` (depending on your setup you will want to RTFM instead).

## Setup pi-hole

The setup wizard is very easy to use and understand, once again if stuck, go check the doc.

Once all setup you will want to manage your DHCP: change the IP range, set the local domain, set static leases... Don't forget to set your gateway to your internet box.

You can then add new DNS blacklist to block more ads domains.

You should be ready to go by now, all your connected devices will use the pi-hole, once their previous DHCP lease expire.

## Setup wireguard

Now that your local devices are safer from ads, you want to be able to block those from anywhere, and manage your local network remotely.

`apt install wireguard`

### Server

```sh
# generate keys
wg genkey > wg.key
cat wg.key | wg pubkey > wg.pub

# create conf
cat <<EOF > /etc/wireguard/wg.conf
[Interface]
Address = 10.0.0.1/24
SaveConfig = true
ListenPort = 51820
PrivateKey = <priv key in wg.key>

[Peer]
PublicKey = <peer pub key in home.pub>
AllowedIPs = 10.0.0.2/24
EOF

# allow forwarding
cat 'net.ipv4.ip_forward = 1' > /etc/sysctl.conf

# enable wg
systemctl enable --now wg-quick@wg

# check for service
wg show
```

### Client

```sh
# generate keys
wg genkey > home.key
cat home.key | wg pubkey > home.pub

# create conf
cat <<EOF > /etc/wireguard/home.conf
[Interface]
PrivateKey = <priv key in home.key>
Address = 10.0.0.2/24 # same as Peer.AllowedIPs in server's config
DNS = 10.0.0.1 # use pi-hole

[Peer]
PublicKey = <server pub key in wg.pub>
AllowedIPs = 10.0.0.0/24
Endpoint = <your box IP>:<forwarded port>
EOF
```

### Internet box

* Put your pi-hole in DMZ
* Create NAT/PAT rule for a port forwarding
    * From your box to pi-hole's wireguard port

Once everything is setup, on your client: `wg-quick up home` should connect you to your local network.

Also, you should be able to manage your local machines: `firefox http://pi.lan/admin` should lead you to your pi-hole interface.
