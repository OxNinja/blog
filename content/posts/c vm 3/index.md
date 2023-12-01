---
title: "🔎 Creating a VM for fun - Part 4: Implementation and refacto"
date: 2023-10-29T10:39:42+02:00
summary: "Let's refacto the whole code, because this is how you dev, right?"
tags: ["c", "low-level", "reverse"]
categories: ["Custom VM"]
author: "0xNinja"
draft: true
series: ["Custom VM"]
series_order: 4
resources:
- name: "featured-image"
  src: "featured-image.png"
---

**The code is here: https://github.com/OxNinja/C-VM**

## Step 1: stack first

The first thing I did was implementing the stack, according to the previous posts of this series. I changed the code a little bit, but the idea stays the same.

The patched code for the stack:

```c
typedef struct stack_node {
  // Chained list
  struct stack_node *prev;
  struct stack_node *next;
  // Void pointer for values
  // each stack node will have a pointer towards the target value
  int *val;
} stack_node;

typedef struct stack {
  // Pointers to first and last elements
  stack_node *first;
  stack_node *last;
} stack;
```

My new take on this project was to code everything in the same `.h` file, to ease using this on other projects. The first version was composed of many `.h` and `.c` files, which helped while developping, but needed more work to implement on external projects.

Now, one shall only `#include "vm.h"` to get started!

## Step 2: add instructions

I then re-implemented my old code for the instructions and the parser. This was very easy, and needed 0 fix surprisingly, but who am I to spit like that.

So as the last version, here is the code:

```c
void vm_emulate(registers *regs, stack *s, int shellcode) {
  int opcode = (shellcode & 0xff000000) >> 0x18;
  
  // instructions is an array of pointers of function
  // each index points to the according function corresponding to the opcode
  // it is very easy to change the opcode for a certain function
  void (*instructions[10])(registers *, stack *, int);
  // no opcode 0 defined for the moment
  instructions[1] = vm_mov;
  instructions[2] = vm_push;
  instructions[3] = vm_add;
  instructions[4] = vm_sub;
  instructions[5] = vm_jmp;
  instructions[6] = vm_cmp;
  instructions[7] = vm_call;
  instructions[8] = vm_exit;
  instructions[9] = vm_pop;                                                 
  // this is not optimal, as this occurs every time we want to emulate code
  // one should declare this array once for all for better performance
  
  (*instructions[opcode])(regs, s, shellcode);
}
```

## Step 3: quick test

I could test my code with the following simple testcase:

```c
#include <stdio.h>
#include <stdlib.h>

#include "vm.h"

int main(void) {
  // init VM
  //   init stack
  stack *stack = stack_init();
  //   init heap?
  //   init registers
  registers *regs = registers_init(stack);

  registers_print(regs);

  // emulate some instructions
  // mov a, 0x45
  vm_emulate(regs, stack, 0x1100045);
  // mov c, 0x2
  vm_emulate(regs, stack, 0x1120002);
  registers_print(regs);
  // exit(a)
  vm_emulate(regs, stack, 0x8000000);

  return 0;
}
```

## Step 4: add push/pop

{{< alert >}}
Work in progress
{{< /alert >}}

Wrote code for stack-related stuff (push, pop).

## Step 5: test the whole
