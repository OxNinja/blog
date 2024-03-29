---
title: "🔎 Creating a VM for fun - Part 1: ASM"
date: 2022-03-17T10:39:42+02:00
summary: "The first part of my series on low-level learning journey, sit back, relax and enjoy me struggling for basic stuff."
tags: ["assembly", "low-level", "reverse"]
categories: ["Custom VM"]
author: "0xNinja"
draft: true
series: ["Custom VM"]
series_order: 1
resources:
- name: "featured-image"
  src: "featured-image.png"
---

To make things short, I saw [How to write a virtual machine in order to hide your viruses and break your brain forever](https://tmpout.sh/2/7.html) by [@s01den](https://twitter.com/s01den) published in [tmp.out](https://tmpout.sh)'s second edition. This new paper made me enjoy (once again) low-level. I wanted to know more about this abstract subject of "virtual machines" in reverse engineering, so I read it and started to implement my own VM in assembly!

> You will find my code on [my Github repo](https://github.com/OxNinja/nasm_/blob/main/vm/vm.asm)

## Why assembly?

I wanted to understand everything I did during this process, and needed to stick with the lowest level I could, I will talk about the future of this project at the end of the post.

I was also already familiar with assembly, especially nasm for Linux, and wanted to test my knowledge.

## Design

Before staring to type very fast on my keyboard, I needed to put things on a paper, in order to have a clear overview of the project.

I had to answer a few questions:

* What is an instruction?

  It's like a function, or an alias to some code to execute
  
* How does the CPU knows what to do with an instruction?

  The code an instruction represents is written for the CPU, so it is seamless
  
* How can I make custom instructions?

  Just implemet some functions or code blocks, then map them to a custom "OPcode"
  
* How can I make the CPU execute my custom instructions?

  Make a simple condition on the custom OPcode, and execute the code mapped to it
  

## PoC

### Registers

To (re)set registers, code is very straightforward and don't really need explainations, right?

```asm
reset_registers:
  push rbp
  mov rbp, rsp

  xor rax, rax
  xor rbx, rbx
  xor rcx, rcx
  xor rdx, rdx
  xor r8, r8

  leave
  ret
```

### Instructions

I decided to implement a very low amount of instructions, as I already plan to upgrade this project in the future. I only need a proof of concept before going big.

| OPcode | Instruction | NASM                     |
|--------|-------------|--------------------------|
| `0x1`  | `mov a, b`  | ``` mov rbx, rcx  ```    |
| `0x2`  | `push a`    | ``` push rbx  ```        |
| `0x3`  | `add a, b`  | ``` add rbx, rcx  ```    |
| `0x4`  | `jmp a`     | ``` jmp rbx  ```         |

Yes, some very basic instructions.

### Execution

The concept here is to compare `rax`, our opcode register and then call the corresponding function:

```asm
;; if opcode == 0x1:
;;   mov_a_b()
cmp rax, 0x1
je mov_a_b

cmp rax, 0x2
je push_a

cmp rax, 0x3
je add_a_b

;; and so on with every opcode

call _exit ;; default if unrecognized opcode
```

## Future

In a future post I will cover how to improve this VM, especially using a fully emulated virtual memory, using C. :sunglasses:
