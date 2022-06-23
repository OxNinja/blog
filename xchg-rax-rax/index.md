# 🔎 xchg rax, rax


## Forewords

{{< admonition tip "Note" >}}
So recently a coworker of mine showed a book about assembly poems, at first I was like "well this joke is very funny" and then I read the first page. 5 minutes later I ordered the same book for my own, and now that it has been received, I want to write my notes here.
{{< /admonition >}}

[There is an online and free version of the book.](https://www.xorpd.net/pages/xchg_rax/snip_00.html)

I will try to understand each 64 pages of this awesome work, in order to maintain my assembly knowledge and to learn new tricks.

Of course I can be wrong in my interpretations of certain code or instructions, if so, feel free to help me improve!

## 0x00

```asm
xor      eax,eax
lea      rbx,[0]
loop     $
mov      rdx,0
and      esi,0
sub      edi,edi
push     0
pop      rbp
```

The first page is pretty straightforward. As you can see every line sets one register to `0`.

Every instruction here is very common and easy to understand, but one thing caught my attention: `loop $`. So let's dig a bit here.

`loop <label>` can be resumed like so:

```asm
loop:
    ; if cx == 0 jmp to end
    test cx, cx
    jnz $+3

    dec cx
    jmp loop
```

As you can see, it decrements `cx` at each iteration until it is `0`. So a `loop $` would simply set `cx` to `0`, as the label to loop through is `$`, the symbol for the actual address.

Normally with `loop label` you would have some code between `label` and the loop instruction, but here there is none, so the loop only decrements `cx`.

Pretty sneaky trick.

## 0x01

```asm
.loop:
    xadd     rax,rdx
    loop     .loop
```

This one is a little trick and pretty obfuscated but was very quick to understand. In fact, this loop produces the fibonacci sequence for the first `cx` elements.

As we learnt about `loop` at [0x00](#0x00), it loops until `cx` equals `0`, and here there is one instruction which gets exectued within the loop.

`xadd` is quite uncommon, this instruction can be coded as:

```asm
xadd:
    ; swap rax and rdx
    xchg rax, rdx

    ; rdx = rdx + rax
    mov r8, rdx
    add r8, rax
    mov rdx, r8
```

One experienced programmer can spot the algorithm to compute the fibonacci sequence here, which calculate the sum of the two previous elements of the sequence.

## 0x02

```asm
neg      rax
sbb      rax,rax
neg      rax
```

This code was a bit tricky, after discussing with friends we agreed to say that this code tells if `rax` is different than `0`.

At first I said that it tells the sign of `rax`, but I missunderstood the `sbb` instruction, but I was wrong and overlooked the computing of the `sbb rax, rax`.

This code requires to look at `neg` at first, despite of switching the sign of the target, it also sets the carry flag `CF` accordingly with the sign.

We can now dig `sbb`, its code can be:

```asm
sbb:
    ; rax is argv[0]
    ; rbx is argv[1]
    mov r8, rax
    add r8, CF
    sub rbx, r8
```

By looking at the possible output values, we van see that it is a substraction by either `rax + 0` or `rax + 1` of `rbx`. Given that in this code, we have `sbb rax, rax`, we can sse that we will only get `rax = rax - (rax + CF)`, with `CF` at `0` or `1`, thus the output of the instruction is either `0` or `1`, corresponding to the initial sign of `rax`.

## 0x03

```asm
sub      rdx,rax
sbb      rcx,rcx
and      rcx,rdx
add      rax,rcx
```

With the previous experiences we now know about all the above instructions, we can deduce the behaviour of the code, which can be coded in a more high-level language like Python:

```py
def my_func(rax, rdx):
  if rax > rdx:
    rax += rdx
```

Yes, this is that simple. The tricky part comes from the `sbb` and `and` part.

* `sub rdx, rax` stores the difference in `rdx`, and sets the `CF` if needed.
* `sbb rcx, rcx` sets `rcx` to `neg CF` (either `0` or `0xffffffff`)
* `and rcx, rdx`
    - If `rax` was lower than `rdx` at line 1: `rcx` would be `0` and then the `and` sill still set `rcx` to `0`
    - If `rax` was greater than `rdx` at line 1: `rcx` would be `0xffffffff` and so, `rcx` becomes the value of `rdx`
* `add rax, rcx` is trivial now

So `0x03` adds `rdx` to `rax` if `rax > rdx`.

## 0x04

```asm
xor      al,0x20
```

This code was pretty simple to test, I was unsure of the exact behaviour of it, so I tested it:

```py 
for x in range(255):
  print(chr(x), chr(x ^ 0x20))
```

And as you can see by executing this code, the printable characters have their case swapped: lowercase letters become upperccase, and vice-versa.

## 0x05

```asm
sub      rax,5
cmp      rax,4
```

This code is so tiny that it seems complex, but fear not, I think I have the solution for it. This code shows the similarities and difference beteween `sub` and `cmp`.

* `sub rax, 5` actually overwrites the value of `rax`
* `cmp rax, 4` computes `sub rax, 4` and only stores the result in the flags, `rax` is not modified

## 0x06

```asm
not      rax
inc      rax
neg      rax
```

This code teaches the trick for those instructions:

* `not rax` does the two's-complement for the value -> `not 0x5 = 0xfffa`
* `inc rax; neg rax` does the same -> `neg 0x6 = 0xfffa`

## 0x07

```asm
inc      rax
neg      rax
inc      rax
neg      rax
```

This code shows us that the `inc; neg` is symetric: doing it twice leads us to the original value. Which is pretty logic as `inc; neg` is the same as `neg`.

## 0x08

```asm
add      rax,rdx
rcr      rax,1
```

