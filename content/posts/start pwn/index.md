---
title: "You want to start to pwn?"
date: 2021-09-01T13:00:28+02:00
summary: "So you want to start to pwn, don't you? Well, I did too! Those are my notes on the past year of binary exploitation."
tags: ["notes", "pwn", "writeup"]
author: "0xNinja"
showToc: true
TocOpen: false
draft: true
hidemeta: false
comments: false
disableShare: false
disableHLJS: false
hideSummary: false
searchHidden: true
ShowReadingTime: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
---

> There are **a lot** of high quality articles about pwn, but I want to share my experience and thus find my mistakes and complete my knowledge. Enjoy.

> :wrench: work in progress

## `pwn`?

Refering to the 'binary exploitation' category, `pwn` is about exploiting weaknesses in low-level and bad code issues. For exemple corrupting the memory if a program does not sanitise the user input.

I [did a walkthrough of a pwn lab a few years ago](https://fakenews.sh/blog/startingpwnt-rop-part-walkthrough/), I found it cool and wanted to share my experience in this post.
