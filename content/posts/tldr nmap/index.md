---
title: "🚀 TL;DR - nmap"
date: 2021-05-04 12:30:00
summary: "Maybe the most used tool when it comes to network discovery and port knocking."
tags: ["tldr", "nmap"]
categories: ["TL;DR"]
author: "0xNinja"
---

## `nmap`

Maybe the most used tool when it comes to network discovery and port knocking.

### Network discovery

```sh
nmap -sn 10.10.10.0/24
```

### Machine scan

```sh
nmap 10.10.10.1 # classic soft scan
nmap 10.10.10.1 -sU # UDP scan
nmap 10.10.10.1 -p 80,443 # scan only ports 80 and 443
nmap 10.10.10.1 -p 1000-2000 # scan all ports between 1000 and 2000
nmap 10.10.10.1 -p- # scan all ports
nmap 10.10.10.1 -sV # get services and versions running on open ports
nmap 10.10.10.1 -sC # use default scripts when scanning
nmap 10.10.10.1 -O # detect OS
nmap 10.10.10.1 -A # equivalent to `nmap 10.10.10.1 -O -sV -sC --traceroute`
```

### Global switches

```sh
-o{N,X,S,G} output_file # save results in output_file in different formats
-T{1..5} # use from 1 to 5 threads
-6 # enable IPv6
-S ip # spoof given IP
-e interface # use given interface
```

### Resources

* https://nmap.org/book/man-briefoptions.html
* https://github.com/OxNinja/Network-Visualizer
