---
title: "🔎 Linux Kernel Module - Introduction"
date: 2022-12-18T10:50:42+02:00
summary: "How to create a basic Linux Kernel Module."
tags: ["c", "lkm", "low-level"]
categories: ["LKM"]
author: "0xNinja"
---

How to create a basic Linux Kernel Module.

A LKM is like a `.so` library, and can run kernel-land.

Writting your own kernel module will help you to understand how the system works and make you think about `malloc`ing in the kernel twice before running the code.

## Code

Here is the bare minimum you have to code to get a working LKM:

```c
#include <linux/module.h>
#include <linux/kernel.h>

// Specify module licence, GPL to not taint the kernel
MODULE_LICENSE("GPL");

// Called on module load
int init_module(void) {
  printk(KERN_INFO "MODULE loaded!\n");
  return 0;
}

// Called on module unload
void cleanup_module(void) {
  printk(KERN_INFO "MODULE unloaded!\n");
}
```

## Compile

The Makefile I use for my modules:

```make
obj-m += my_module.o

all:
    sudo make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

install:
    sudo insmod ./my_module.ko

uninstall:
    sudo rmmod my_module

clean:
    sudo make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
```

Then just run `make`. A new `my_module.ko` should be here, this is your kernel module.

## Install

```sh
sudo insmod ./my_module.ko
# or
make install
```

In `dmesg` you should have a new line containing `MODULE loaded!`. Your module is loaded in the kernel.

## Uninstall

```sh
sudo rmmod my_module
# or
make uninstall
```

In `dmesg` you should have a new line containing `MODULE unloaded!`. Your module is deleted form the kernel.

## MISC

* `dmesg -C` will clear the dmesg buffer
* `watch 'dmesg | grep MODULE'` will append the new messages of the module so you don't have to re-run the command

## Afterwords

Starting to create a kernel module is pretty easy, you just have to be careful with the functions you call and how you code them. There are a lot of specific functions for the kernel only, and you must check them out before using them.

In the future I will discuss more about the internals of Linux and why using a kernel module is insanely powerfull and at the same time a pain to code.