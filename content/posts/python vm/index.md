---
title: "🔎 Creating a VM for fun - Part 5: Python"
date: 2024-01-05T10:39:42+02:00
summary: "Same as before but in Python"
tags: ["python", "low-level", "reverse"]
categories: ["Custom VM"]
author: "0xNinja"
draft: true
series: ["Custom VM"]
series_order: 5
resources:
- name: "featured-image"
  src: "featured-image.png"
---

## Introduction

{{< github repo="OxNinja/Soft-Machine" >}}

As I wanted to continue my VM journey, I needed some changes and started once again from scratch, in Python this time.

This time I wanted to make a package with some purposes, with the following features:

- Exec compiled code 
- Assemble code into compiled code 
- Disassemble compiled code into assembly

## VM workflow

The idea as described above, as for me, required a CLI in order to be a one-for-all tool. I went for a Python package based on `click`.

Here is an overview of what I thought of:

{{< mermaid >}}
flowchart TB
  subgraph Parser
    1[Assemble]
    2[Disassemble]
  end

  subgraph VM
    direction RL
    A[Instructions]
    B[Stack]
    C[Heap]
  end

  subgraph CLI
    direction RL
    a[Exec]
    b[Assemble]
    c[Disassemble]
  end
{{< /mermaid >}}

## Instructions

As usual, I implemented every instructions and used a global list for each one of them:

```python 
INSTRUCTIONS = (
        mov,
        push,
        pop,
        add,
        sub,
        cmp,
        call,
        jmp,
        _exit
        )
```

Here is the code for the `mov` instruction:

```python 
def mov(vm, opcode):
    # first arg is always a register
    target = opcode >> (vm.opcode_size - 2) * 4 & 0xf
    if target < 0 or target >= len(vm.regs.regs):
        print(f"Unexpected value for target: {target}. Must be between 0 (included) and {len(vm.regs.regs)} (excluded).")
        exit(1)

    # second arg can be either a register, or a value
    is_reg = opcode >> (vm.opcode_size - 3) * 4 & 0xf

    if is_reg == 0:
        value = opcode & (16 ** (vm.opcode_size - 3) - 1)
    elif is_reg == 1:
        index = opcode >> (vm.opcode_size - 4) * 4 & 0xf
        if index < 0 or index >= len(vm.regs.regs):
            print(f"Unexpected value for index: {index}. Must be between 0 (included) and {len(vm.regs.regs)} (excluded).")
            exit(1)
        
        value = vm.regs.get(index)

    elif is_reg != 0 or is_reg != 1:
        print(f"Unexpected value for is_reg: {is_reg}. Must be either 0 or 1.")
        exit(1)

    vm.regs.set(target, value)
```

## VM

As you may have noticed, my code is more object-oriented. In addition, I made a class for every components of the project.

Here is the constructor for my VM:

```python 
class VM:
    def __init__(self):
        self.stack = Stack()
        self.regs = Registers()
        self.opcode_size = 8
```

Yes, as Python is more permissive than C, I asked myself "why not making the opcodes configurable?", leading to this `self.opcode_size` attribute.

In the future I would like to be able to fully manage the VM and making it really customizable, the same goes for the opcodes, the instructions, the stack, the heap...

There is not much more to look for this VM class, only the exec function, which redirects to the corresponding instruction.

## Exec test

Let's first manually compile the following assembly code into our VM's opcodes:

```asm
add a, 0x1000   ; 0x30001000
mov b, a        ; 0x01100000
sub b, 0x100    ; 0x41000100
```

We then exec this code:

```bash
softmachine exec -s "0x30001000;0x01100000;0x41000100"                                 
===== VM =====
Registers:
a: 4096
b: 3840
c: 0
d: 0
flags: 0
```

## Stack

As I represented the stack as a list, it is trivial to push/pop values:

```python 
class Stack:
    def __init__(self, max_size=0xffffff):
        self.stack = list()
        self.max_size = max_size
        self.size = len(self.stack)

    def push(self, value):
        if self.size < self.max_size:
            self.stack.append(value)
            self.update()

    def pop(self):
        if self.size > 0:
            self.stack.pop()
            self.update()

    def update(self):
        self.size = len(self.stack)
```

And here is the corresponding code for the `pop` instruction:

```python 
def pop(vm, opcode):
    if vm.stack.size < 1:
        print("Cannot pop, the stack is empty.")
        exit(1)

    # first arg is always a register
    target = opcode >> (vm.opcode_size - 2) * 4 & 0xf
    if target < 0 or target >= len(vm.regs.regs):
        print(f"Unexpected value for target: {target}. Must be between 0 (included) and {len(vm.regs.regs)} (excluded).")
        exit(1)

    value = vm.stack.stack[-1]
    vm.regs.set(target, value)
    vm.stack.pop()
```

So yeah, this is way easier to implement a VM in Python, as it abstracts a lot of things. The drawback is the loss of memory management.

## Performances

Let's talk a bit about performances.

To let myself track the differences regarding execution time, I made a stress test for the VM. Very simple in the first place because there are not that much features.

```python 
class VM:
    # ...

    def stress_test(self, n):
        for x in range(n):
            INSTRUCTIONS[1](self, 0x10ffffff)
        for x in range(n):
            INSTRUCTIONS[2](self, 0x20000000)
```

This does `n` times `push 0xffffff`, then `n` times `pop a`. I wanted not to put `push` and `pop` in the same loop cycle, in order to monitor the memory usage in case of many allocations.

Here are the results on my machine:

```bash 
time softmachine stresstest -n 10000   
# softmachine stresstest -n 10000  0.07s user 0.01s system 98% cpu 0.077 total

time softmachine stresstest -n 1000000
# softmachine stresstest -n 1000000  1.13s user 0.03s system 99% cpu 1.164 total

time softmachine stresstest -n 10000000
# softmachine stresstest -n 10000000  10.79s user 0.18s system 99% cpu 10.983 total
```

The execution time seems -- for the moment -- to be linear, depending on the number of instructions to execute.
