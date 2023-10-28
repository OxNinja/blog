---
title: "🔎 Creating a VM for fun - Part 3: C virtual stack"
date: 2023-10-28T10:39:42+02:00
summary: "This time I am going to show you how I implemented my custom virtual stack"
tags: ["c", "low-level", "reverse"]
categories: ["Custom VM"]
author: "0xNinja"
draft: true
series: ["Custom VM"]
series_order: 3
resources:
- name: "featured-image"
  src: "featured-image.png"
---

**The code is here: https://github.com/OxNinja/C-VM**


## First stack implementation

This is propably the most difficult thing in this project for me, as I had to figure out how to implement a virtual stack and related stuff.

I first thought about using a pointer to a `malloc`ed chunck as the stack, where I could store pointers to the values, so here is the struct:

```c
typedef struct Stack {
  // LIFO stack

  // max size of the stack
  int max_size;

  // pointers for the stack
  int *stack, *stack_base, *stack_end, **stack_pointer;
  
} Stack;
```

A few explanations about this propably cursed struct:

* `max_size` is the size of the stack (max number of pointer that could be stored in it).
* `*stack` is a pointer to the allocated chunk in memory to store the pointers.
* `*stack_base` is a pointer to the base of the stack (the first place to store pointers at).
* `*stack_end` is a pointer to the end of the stack (the limit of its size).
* `**stack_pointer` is a pointer of the current "cursor" in the stack, pointing to the stored pointer in it.

{{< mermaid >}}
flowchart LR
  subgraph Stack
    direction LR
    subgraph *stack
        direction LR
        0x00 --> 0x55ff1111
        0x08 --> 0x55ff2222
        0x10 --> 0x55ff3333
        0x18 --> 0x55ff4444
        ... --> 0x...
        max_size --> ???
    end
    **stack_pointer --> 0x18
    *stack_base --> 0x00
    *stack_end --> max_size
  end
{{< /mermaid >}}

Feel free to visit the project's repo to check if I finished this implementation, but by now I am for sure struggling with this.

In fact with this virtual stack the VM is now able to `push` & `pop` and all that stuff, here is how I implemented them:

```c
void my_push(Registers *regs, Stack *stack, int shellcode) {
  // get the value to push
  int value = shellcode & 0x00ffffff;
  // get a pointer to the value
  int *pointer = &value;
  // make the stack pointer pointing to the pointer :brain: :point_right: :point_left:
  *stack->stack_pointer = pointer;
  // increment the cursor for the top of the stack
  stack_inc(stack);
}
```

The same goes for the `pop`, except that we first decrement the stack pointer index, as we incremented it last, and then we store the value pointed into the corresponding register.

I then stumbled upon other bugs in my code, which discouraged me to continue further.

## Second attempt

Maybe one year later or so I deceided to continue this project.

I settled for a more kernel-like approach: using chained list instead of `malloc`ing a big chunk of memory.

Here is my go:

{{< mermaid >}}
flowchart LR
  subgraph list
    direction LR
    a[*first] --> a1[0xff5500aa]
    b[*last] --> b1[0xff5500bb]
    subgraph "node @0xff5500aa"
      direction LR
      A1[*prev] --> D1[NULL]
      B1[data] --> 0
      C1[*next] --> E1[0xff5500bb]
    end
    subgraph "node @0xff5500bb"
      direction LR
      A2[*prev] --> E2[0xff5500aa]
      B2[data] --> 1
      C2[*next] --> D2[NULL]
    end
  end
{{< /mermaid >}}

Which might be simpler to code, and to understand.

Here are the associated structs:

```c
struct node {
  struct node *prev;
  struct node *next;
  int data;
} typedef node;

struct list {
  struct node *first;
  struct node *last;
} typedef list;
```

Very basic, therefore effective.

The idea afterwards is to create the `list` pointer, which will be our LIFO stack. All the new `node`s will be allocated in the heap for us -- the real heap, not our VM's.

### Code

As a PoC for this new stack concept, here is how I did it, plus some performance indicators:

#### main.h

```c 
#include <stdio.h>
#include <stdlib.h>

struct node {
    struct node *prev;
    struct node *next;
    int data;
} typedef node;

struct list {
    struct node *first;
    struct node *last;
} typedef list;

node * node_create(int d) {
    node *p = (node*) calloc(1, sizeof(node));
    p->prev = NULL;
    p->data = d;
    p->next = NULL;

    return p;
}

void node_print(node *p) {
    printf("%d\n", p->data);
}

list * list_create(void) {
    node *n = node_create(0);
    list *p = (list*) calloc(1, sizeof(list));
    p->first = n;
    p->last = n;

    return p;
}

int list_push(list *l, int d) {
    int err = 1;

    node *n = node_create(d);
    node *last = l->last;

    n->prev = last;
    last->next = n;
    l->last = n;

    err = 0;
    return err;
}

int list_pop(list *l) {
    int err = 1;

    node *last = l->last;
    node *slast = last->prev;

    slast->next = NULL;
    l->last = slast;
    free(last);

    err = 0;
    return err;
}

void list_print(list *l) {
    printf("===== (%p)\nlist first ->\t%p\nlist last ->\t%p\n", l, l->first, l->last);
    node *p = l->first;
    while(p != NULL) {
        printf("(%p)\nprev -> %p\ndata -> %d\nnext -> %p\n-----\n", p, p->prev, p->data, p->next);
        p = p->next;
    }

    printf("\n");
}
```

#### main.c

```c 
#include "main.h" 

int main(void) {
    list *l = list_create();

    int i = 1;        
    while(i<2000000) {      
        list_push(l, i);
        i++;
    }          

    while(i>1) {      
        list_pop(l);
        i--;
    }                       

    list_print(l);          

    return 0;   
}
```

For pushing, then poping 2M nodes on my list it took no time:

```
time ./bin.out
===== (0x55ab7ff042c0)
list first ->	0x55ab7ff042a0
list last ->	0x55ab7ff042a0
(0x55ab7ff042a0)
prev -> (nil)
data -> 0
next -> (nil)
-----

./bin.out  0.10s user 0.02s system 99% cpu 0.121 total
```

### Implementation

It is now time for me to add this code in the VM!
