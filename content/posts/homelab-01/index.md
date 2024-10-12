---
title: "Homelab - Part 2 - Basics with Proxmox"
date: 2024-10-12T10:50:42+02:00
summary: "My basic setup using Portainer"
tags: ["proxmox", "homelab", "portainer", "docker"]
categories: ["Homelab"]
series: ["Homelab"]
series_order: 2
author: "0xNinja"
draft: true
resources:
- name: "featured-image"
  src: "featured-image.png"
---

I just setup my homelab using Proxmox. It is still very basic.

# Setup overview

{{< mermaid >}}
graph BT
    a[ISP Router]
    b[Configurable switch]
    subgraph Proxmox
        direction BT
        subgraph LXC1
            aa[Portainer]
        end
        subgraph LXC2
            aaa[Docker stack 1]
        end
        subgraph LXC3
            aba[Docker stack 2]
        end
    end

    subgraph Server
        ba[PiHole]
        bb[Wireguard]
    end

    b --> a
    Proxmox --> b
    Server --> b

    aaa -->|Portainer agent| aa
    aba -->|Portainer agent| aa
{{< /mermaid >}}

# Proxmox

I scraped my old gaming computer into my new hypervisor, so I don't have bleeding-edge ressources. Nothing really crazy here.

I chose to isolate my services in different LXC containers to manage them easilly, in case I want to shutdown only one of them, or setup VLANs for them.

Of course, I went with Alpine for my LXCs. **0.01% of 1 CPU, 80MB of RAM and 600MB of disk to run Portainer**, is very nice when dealing with limited ressources.

# Portainer

To manage all my services, I went with Portainer for the following reasons:

- I never used it before
- It is easy to create a new container from the web UI
- It can be used with a `docker-compose.yml` config
- I can migrate any stack from any host to any host in no time

By installing a Portainer agent on my LXCs I can manage each one of them from the Portainer dashboard, pretty handy.

# Docker services

Each Docker stack is hosted on its own LXC, to avoid having one service eating all the RAM and slowing down the hole infrastructure. I am talking about you, `gitlab` and `home-assistant`.