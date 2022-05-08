# You want to start to `pwn`?


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

