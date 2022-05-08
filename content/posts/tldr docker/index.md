---
title: "🚀 TL;DR - Docker"
date: 2021-05-04 12:00:00
summary: "Wow you don't know yet what Docker is? 🤔 Let me introduce you this beautiful containerization tool!"
tags: ["docker", "tldr"]
categories: ["TL;DR"]
author: "0xNinja"
---

## Docker 🐋

> Wow, you don't know yet what is Docker? Well, let me introduce you this beautiful containerization tool.

### Containers?

* Container ~= virtual machine

**A container is like a virtual machine** that runs in background on your computer. It simulates a whole system in the same way.

* Container > virtual machnie

But, a container is **faster**, **better** ~~and stronger~~ than a classical VM. Because it is meant to be fast and light-weight.

### Images

Docker uses images to run containers. In short an image is a base container, which will be used by your container -- like said -- as a base. For example, I want to run an Ubuntu container, my Docker image will be something like:

```docker
FROM ubuntu:latest

RUN apt update
```

*This file is called a **Dockerfile**, because it produces the corresponding Docker container when built.*

When ran, this image will use the latest Ubuntu image in Docker's database, amd update it.

You can do so much in a Docker image!

### Build & run

Once you made your **Dockerfile**, you will use it to **build** your **Docker image**:

```sh
docker build -t my-image .
```

* `-t my-image`: the tag (or name if you want) to give to your image
* `.`: the directory where you put your `Dockerfile`

You now want to run it!

```sh
docker run my-image
```

And, voila! Your container is running!

### Resources

* `docker ps`: list all running containers
* `docker inspect`: get information about a given container
* `docker kill`: kill a running container
* `docker images`: list all stored Docker images
* https://docs.docker.com/get-started/overview/
* https://putaindecode.io/articles/introduction-a-docker/
* https://docker-curriculum.com/
* [Setup your database with Docker](/posts/setup-your-database-with-docker/)
