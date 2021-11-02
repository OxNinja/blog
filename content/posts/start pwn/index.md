---
title: "You want to start to `pwn`?"
date: 2021-09-01T13:00:28+02:00
summary: "So you want to start to pwn, don't you? Well, I did too! Those are my notes on the past year of binary exploitation."
tags: ["notes", "pwn"]
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

## Buffer overflow

### Theory

Re-write memory on the fly.

### Practice

## ROP

### Theory

Use 'code' in the binary to chain small instructions and re-write data.

### Practice

## ret2libc

### Theory

Use ROP to execute code, use compiled `libc` in the binary to jump to any `libc` function. Usefull to get a shell.

### Practice

## Resources

* [StartingPwnt](https://github.com/MaitreRenard/StartingPwnt)
* [StartingPwnt solutions](https://fakenews.sh/startingpwnt-rop-solve)
